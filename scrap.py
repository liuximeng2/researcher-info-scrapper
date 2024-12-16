from googlesearch import search
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import os
import base64

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium WebDriver (use the path to your ChromeDriver executable)
import chromedriver_autoinstaller

def scrape_med(url,
               name,
               save_path="images"):
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
    driver.get("http://www.python.org")

    try:
        driver.get(url)

        # Wait until the desired element is rendered
        wait = WebDriverWait(driver, 10)  # Timeout after 10 seconds
        profile_detail_container = wait.until(
            EC.presence_of_element_located((By.ID, "profile-detail-container"))
        )

        # Extract and print the text content
        profile_text = profile_detail_container.text

        readable_text = "\n".join(
            [line.strip() for line in profile_text.split("\n") if line.strip()]
        )    

        # Create directory to save images
        save_dir = os.path.join(save_path, "images", name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Extract images within the container
        images = profile_detail_container.find_elements(By.TAG_NAME, "img")
        for idx, img in enumerate(images):
            src = img.get_attribute("src")
            alt = img.get_attribute("alt")
            if src.startswith("data:image"):
                # Handle base64 image
                _, encoded = src.split(",", 1)
                image_data = base64.b64decode(encoded)
                image_path = os.path.join(save_dir, f"image_{idx + 1}.png")
                with open(image_path, "wb") as f:
                    f.write(image_data)
            else:
                # Handle URL image
                response = requests.get(src)
                if response.status_code == 200:
                    image_path = os.path.join(save_dir, f"image_{idx + 1}.png")
                    with open(image_path, "wb") as f:
                        f.write(response.content)

        return readable_text

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the browser
        driver.quit()

def save_image(name, url, img_urls, save_directory):
    """
    Save images from a list of URLs to a specified directory
    """
    # Create a directory to save images
    path = os.path.join(save_directory, name)
    if not os.path.exists(path):
        os.makedirs(path)

    for i, img_url in enumerate(img_urls):
        
        img_url = urljoin(url, img_url)
        
        try:
            img_data = requests.get(img_url).content
            img_name = os.path.join(path, f"image_{i+1}.jpg")

            with open(img_name, 'wb') as img_file:
                img_file.write(img_data)
            
            print(f"Saved {img_url} as {img_name}")
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")

def search(target_urls, query):
    try:
        # API endpoint
        url = "https://www.googleapis.com/customsearch/v1"
        
        # Parameters
        params = {
            "q": query,            # Search query
            "key": os.getenv("GOOGLE_API_KEY"),        # Your API key
            "cx": os.getenv("GOOGLE_SEARCH_ID"),              # Your Custom search engine ID
            "num": 1    # Number of results to return
        }
        
        # Make the request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses

        # print(f"Found URL: {response.json()}")

        for item in response.json().get("items", []):
            print("Link:", item["link"])
            print(len(target_urls))
            target_urls.append(item["link"])
            return target_urls

    except Exception as e:
        print(f"Search error: {e}")
        return None

def scrape(target_url, domain, name, need_images=False):

    website_text = []
    try:
        response = requests.get(target_url)

        if response.status_code != 200:
            print("Error accessing the target URL")
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        # extract key information from the website
        if domain != 'med':
            all_text = soup.get_text(separator='\n', strip=True)
        elif domain == 'med':
            all_text = scrape_med(target_url, name)
        
        if need_images:
            images = [img['src'] for img in soup.find_all('img', src=True)]
            images = [img for img in images if not img.endswith('.svg')]
            save_image(name, target_url, images, 'images')


    except Exception as e:
        print(f"Error scraping target URL: {e}")
        return None
        
    return all_text
