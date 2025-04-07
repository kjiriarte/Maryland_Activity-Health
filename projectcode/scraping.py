# Make sure you have these installed:
# pip install selenium webdriver-manager pandas

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Secure login input
EMAIL = "kxiriarte@gmail.com"
PASSWORD = "Crying77loud"

# Set up WebDriver with webdriver-manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Step 1: Log in to AllTrails
driver.get("https://www.alltrails.com/login")
time.sleep(3)

# Find login fields and fill them in
#driver.find_element(By.ID, "user_email").send_keys(EMAIL)
#driver.find_element(By.ID, "user_password").send_keys(PASSWORD)
#driver.find_element(By.ID, "user_password").send_keys(Keys.RETURN)
time.sleep(5)  # Wait for login to complete

# Step 2: Navigate to the Maryland trails page
driver.get("https://www.alltrails.com/us/maryland")
time.sleep(10)

# Step 3: Scroll to load more trails (adjust number of scrolls)
for _ in range(5):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(3)

# Step 4: Scrape trail cards
trail_cards = driver.find_elements(By.CLASS_NAME, "styles-module__trailCard__1F1lv")
trail_data = []

for card in trail_cards:
    try:
        name = card.find_element(By.CLASS_NAME, "styles-module__name__2FQbT").text
        length = card.find_element(By.CLASS_NAME, "styles-module__distance__1bH1n").text
        rating = card.find_element(By.CLASS_NAME, "styles-module__rating__3cjVy").text
        trail_data.append({
            "Trail Name": name,
            "Length (mi)": length,
            "Rating": rating
        })
    except Exception as e:
        print("Skipped one trail card due to error:", e)

# Step 5: Build DataFrame and clean
df = pd.DataFrame(trail_data)

# Optional cleanup
if "Length (mi)" in df.columns:
    df["Length (mi)"] = df["Length (mi)"].str.replace(" mi", "", regex=False).astype(float)
if "Rating" in df.columns:
    df["Rating"] = pd.to_numeric(df["Rating"], errors='coerce')

# Save to CSV
df.to_csv("maryland_trails.csv", index=False)
print("Scraping complete. Saved to 'maryland_trails.csv'.")

# Done!
driver.quit()
