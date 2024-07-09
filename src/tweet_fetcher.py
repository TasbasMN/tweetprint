import logging
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import requests
from io import BytesIO
from PIL import Image as PILImage

def get_profile_pic(driver):
    try:
        img_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'img'))
        )
        for img in img_elements:
            src = img.get_attribute('src')
            if 'profile_images' in src:
                response = requests.get(src)
                img = PILImage.open(BytesIO(response.content))
                img = img.convert('L')  # Convert to grayscale
                return img
        logging.warning("Profile picture not found")
        return None
    except Exception as e:
        logging.error(f"Failed to fetch profile picture: {str(e)}")
        return None
import re

def get_tweet_info_from_url(url):
    logging.info(f"Processing URL: {url}")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    with webdriver.Chrome(options=chrome_options) as driver:
        try:
            driver.get(url)
            logging.info("Page loaded")
            
            # Wait for the tweet content to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetText"]')))

            # Get the entire page source
            page_source = driver.page_source
            
            pattern = r'unset;">\s*(\w+)\s*</span>'
            matches = re.findall(pattern, page_source, re.DOTALL)
            
            print(matches)

            # Create a dictionary to store metrics
            metrics = {}
            for i in range(0, len(matches), 2):
                if i+1 < len(matches):
                    key, value = matches[i], matches[i+1]
                    if key.isdigit():
                        metrics[value.lower()] = key
                    else:
                        metrics[key.lower()] = value

            # Extract specific metrics
            views = metrics.get('views', '0')
            retweets = metrics.get('repost', '0')
            quotes = metrics.get('quote', '0')
            likes = metrics.get('likes', '0')
            bookmarks = metrics.get('bookmarks', '0')

            
            logging.info(f"Metrics found: {views} views, {retweets} reposts, {quotes} quotes, {likes} likes, {bookmarks} bookmarks")

            # Extract other information
            try:
                tweet_text = driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]').text
            except NoSuchElementException:
                tweet_text = ""
                logging.warning("Tweet text not found")

            try:
                user_info = driver.find_element(By.CSS_SELECTOR, '[data-testid="User-Name"]')
                full_name = user_info.find_element(By.CSS_SELECTOR, 'span').text
                username = user_info.find_elements(By.CSS_SELECTOR, 'span')[1].text
            except NoSuchElementException:
                full_name = username = ""
                logging.warning("User information not found")

            try:
                timestamp = driver.find_element(By.CSS_SELECTOR, 'time').get_attribute('datetime')
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).strftime('%I:%M %p · %b %d, %Y')
            except NoSuchElementException:
                timestamp = ""
                logging.warning("Timestamp not found")

            # Get profile picture
            profile_pic = get_profile_pic(driver)

        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return None
        

    return full_name, username, tweet_text, timestamp, likes, retweets, views, bookmarks, quotes, profile_pic

