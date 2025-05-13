import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import base64
from PIL import Image
import io

# Streamlit app configuration
st.set_page_config(page_title="Webpage Screenshot App", page_icon="📸")
st.title("Webpage Screenshot App")
st.write("Enter a URL to capture a screenshot of the webpage.")

# Input URL from user
url = st.text_input("Webpage URL", "https://example.com")
capture_button = st.button("Take Screenshot")

# Function to capture screenshot
def capture_screenshot(url, output_path):
    # Configure Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    # Set up ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Navigate to the URL
        driver.get(url)
        # Wait for page to load
        time.sleep(3)
        # Capture screenshot
        driver.save_screenshot(output_path)
        return True
    except Exception as e:
        st.error(f"Error capturing screenshot: {str(e)}")
        return False
    finally:
        driver.quit()

# Handle screenshot capture and display
if capture_button:
    if not url.startswith(("http://", "https://")):
        st.error("Please enter a valid URL starting with http:// or https://")
    else:
        with st.spinner("Capturing screenshot..."):
            screenshot_path = "screenshot.png"
            success = capture_screenshot(url, screenshot_path)
            if success:
                # Display the screenshot
                img = Image.open(screenshot_path)
                st.image(img, caption="Captured Screenshot", use_column_width=True)
                
                # Provide download option
                with open(screenshot_path, "rb") as file:
                    img_bytes = file.read()
                    st.download_button(
                        label="Download Screenshot",
                        data=img_bytes,
                        file_name="screenshot.png",
                        mime="image/png"
                    )
                # Clean up
                os.remove(screenshot_path)
