from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import sys
import os


def wait_for_page_load(driver, timeout=30):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


def wait_for_reservation_page(driver, timeout=30):
    WebDriverWait(driver, timeout).until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR,
                                                         "input[type='radio'].style_time_picker__radio__1c6YB"))
    )


# Refresh monitoring loop
def refresh_loop(driver) -> str:
    refresh_url = "https://ticket.expo2025.or.jp/en/myticket/"
    timer = 0
    while True:
        current_url = driver.current_url
        if current_url == refresh_url:
            if timer >= 120:
                print("[INFO] Trying to click the <li> element...")
                timer = 0
                try:
                    element = driver.find_element(
                        By.CSS_SELECTOR,
                        'li[data-menu-index="2"]'
                    )
                    element.click()
                    print("[INFO] Clicked the <li> element successfully.")
                except Exception as e:
                    print(f"[ERROR] Could not click the element: {e}")
            else:
                time.sleep(1)
                timer += 1
        elif "system_error" in current_url:
            print("[INFO] An error occurred on the webpage, trying to load the refresh URL...")
            timer = 0
            driver.get(refresh_url)
        else:
            input("Navigate to My Tickets page and press ENTER here to start refreshing, or "
                  "navigate to the reservation page and press ENTER here to start monitoring...")
            current_url = driver.current_url
            if current_url == refresh_url:
                print("[INFO] Refresh mode started. "
                      "Scroll the \"My Tickets\" button out of view to pause, or "
                      "navigate to the reservation page and press ENTER here to start monitoring.")
                continue
            else:
                print("[INFO] Reservation mode started.")
                # Get the current URL of the reservation page
                return current_url


def monitor_loop(driver, reservation_page: str):
    while True:
        try:
            # wait for the page to load completely
            wait_for_page_load(driver)

            # if not on reservation page, go back to refresh mode
            if driver.current_url != reservation_page:
                print("Not on reservation page, falling back to refresh mode...")
                return

            # wait for the reservation page to load
            wait_for_reservation_page(driver)

            # find all available time slot radio buttons
            radios = driver.find_elements(By.CSS_SELECTOR,
                                          "input[type='radio'].style_time_picker__radio__1c6YB:not([disabled])")

            if radios:
                print("Found available slot! Attempting to book...")

                # click the first available radio
                driver.execute_script("arguments[0].scrollIntoView(true);", radios[0])
                # time.sleep(1)
                radios[0].click()

                # find and click the submit button
                button = driver.find_element(By.CSS_SELECTOR,
                                             "button.basic-btn.type2.style_reservation_next_link__7gOxy")
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                # time.sleep(1)
                button.click()

                print("Reservation attempted!")
            else:
                print("No available slots yet...")

        except Exception as e:
            print(f"Error occurred: {e}")

        # wait a bit before retrying
        time.sleep(5)
        driver.refresh()


def main():
    edge_options = Options()
    # edge_options.add_argument("--start-maximized")
    driver_path = "msedgedriver.exe"
    if getattr(sys, 'frozen', False):
        driver_path = os.path.join(sys._MEIPASS, driver_path)
    service = Service(executable_path=driver_path)  # make sure msedgedriver is in the same folder or PATH
    driver = webdriver.Edge(service=service, options=edge_options)

    driver.get("https://ticket.expo2025.or.jp/en/")

    while True:
        reservation_page = refresh_loop(driver)
        monitor_loop(driver, reservation_page)


if __name__ == "__main__":
    main()
