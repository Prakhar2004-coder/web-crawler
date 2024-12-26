import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Configure Chrome options
options = Options()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver
service = Service('path/to/chromedriver')  # Update with your path
driver = webdriver.Chrome(service=service, options=options)

# LinkedIn login credentials
username = "your_email@example.com"
password = "your_password"

# Function to log into LinkedIn
def login():
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(5)  # Wait for login to complete

# Function to scrape profiles
def scrape_profiles():
    profiles = []
    for page in range(1, 6):  # Scraping first 5 pages
        driver.get(f"https://www.linkedin.com/search/results/people/?page={page}")
        time.sleep(5)  # Wait for the page to load
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Find profile containers
        profile_cards = soup.find_all('li', class_='reusable-search__result-container')
        
        for card in profile_cards:
            name = card.find('span', {'aria-hidden': 'true'}).get_text(strip=True)
            profile_link = card.find('a', class_='app-aware-link')['href']
            profiles.append({'Name': name, 'Profile Link': profile_link})
    
    return profiles

# Function to save profiles to CSV
def save_to_csv(profiles):
    with open('linkedin_profiles.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Profile Link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for profile in profiles:
            writer.writerow(profile)

# Main execution
if __name__ == "__main__":
    login()
    profiles = scrape_profiles()
    save_to_csv(profiles)
    driver.quit()
    print("Scraping complete. Profiles saved to linkedin_profiles.csv.")