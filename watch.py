from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import os

# --- SETUP ---

edge_options = Options()
# edge_options.add_argument("--start-maximized")
driver_path = "msedgedriver.exe"
if getattr(sys, 'frozen', False):
    driver_path = os.path.join(sys._MEIPASS, driver_path)
service = Service(executable_path=driver_path)  # make sure msedgedriver is in the same folder or PATH
driver = webdriver.Edge(service=service, options=edge_options)

driver.get("https://ticket.expo2025.or.jp/en/")

input("Navigate to the reservation page and press ENTER here to start monitoring...")
# Get the current URL of the reservation page
reservation_page = driver.current_url

# --- FUNCTIONS ---
def wait_for_reservation_page(driver, timeout=30):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='radio'].style_time_picker__radio__1c6YB"))
    )

# --- MAIN LOOP ---
while True:
    try:
        # wait for the page to load completely
        wait_for_reservation_page(driver)

        # if not on reservation page, reload it
        if driver.current_url != reservation_page:
            print("Not on reservation page, reloading...")
            time.sleep(5)
            driver.get(reservation_page)
            continue

        # find all available time slot radio buttons
        radios = driver.find_elements(By.CSS_SELECTOR, "input[type='radio'].style_time_picker__radio__1c6YB:not([disabled])")

        if radios:
            print("Found available slot! Attempting to book...")

            # click the first available radio
            driver.execute_script("arguments[0].scrollIntoView(true);", radios[0])
            # time.sleep(1)
            radios[0].click()

            # find and click the submit button
            button = driver.find_element(By.CSS_SELECTOR, "button.basic-btn.type2.style_reservation_next_link__7gOxy")
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            # time.sleep(1)
            button.click()

            print("Reservation attempted!")
            # Wait for an extra few seconds
            time.sleep(25)
        else:
            print("No available slots yet...")

    except Exception as e:
        print(f"Error occurred: {e}")

    # wait a bit before retrying
    time.sleep(5)
    driver.refresh()
