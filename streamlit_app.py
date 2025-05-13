import streamlit as st
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from PIL import Image
import io
import base64

# Set up Streamlit page
st.title("Webpage Screenshot Generator")
st.write("Enter a URL to capture a screenshot of the webpage")

# Input field for URL
url = st.text_input("Website URL (include http:// or https://)", "https://example.com")

# Function to take screenshot
def take_screenshot(url, output_path):
    # Configure Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize driver with ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Navigate to URL
        driver.get(url)
        
        # Wait for page to load
        time.sleep(3)
        
        # Get page dimensions
        total_height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(1920, total_height)
        
        # Take screenshot
        driver.save_screenshot(output_path)
        
        return True
    except Exception as e:
        st.error(f"Error capturing screenshot: {str(e)}")
        return False
    finally:
        driver.quit()

# Button to trigger screenshot
if st.button("Take Screenshot"):
    if url:
        # Create temporary file path
        temp_file = "temp_screenshot.png"
        
        # Show loading spinner
        with st.spinner("Capturing screenshot..."):
            success = take_screenshot(url, temp_file)
        
        if success and os.path.exists(temp_file):
            # Display the screenshot
            st.success("Screenshot captured successfully!")
            
            # Open and display image
            img = Image.open(temp_file)
            st.image(img, caption=f"Screenshot of {url}", use_column_width=True)
            
            # Convert image to bytes for download
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            # Create download button
            st.download_button(
                label="Download Screenshot",
                data=buffered.getvalue(),
                file_name=f"screenshot_{url.replace('https://', '').replace('http://', '').replace('/', '_')}.png",
                mime="image/png"
            )
            
            # Clean up
            os.remove(temp_file)
        else:
            st.error("Failed to capture screenshot. Please check the URL and try again.")
    else:
        st.warning("Please enter a valid URL")
