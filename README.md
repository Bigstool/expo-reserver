# Expo Reserver

Helps you save a spot at your dream pavilion at Expo 2025 Osaka, Kansai, Japan. Works for both the first-come, first-served applications (starting 3 days before the day of visit) and the pavilions / events on site registration (on the day of visit).

## Usage guide

Download `reserver.exe` from the [latest release](https://github.com/Bigstool/expo-watch/releases/latest).

Download the latest [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver#downloads) from the `Stable`, `x64` channel. Extract the .zip file and move the contained `msedgedriver.exe` alongside `reserver.exe` (so that the two files are in the same folder).

Open `reserver.exe`. A **terminal window** and a **Microsoft Edge browser window** should appear.

In the browser window, log in as usual.

### Refresh mode

The refresh mode refreshes the EXPO2025 Digital Tickets website periodically to prevent your account from being automatically logged out due to inactivity. Useful before the start of first-come first-served applications when the website gets very crowded. It is recommended that you start `reserver.exe` before 10:00 PM JST, wait in the login queue, log in, and then start the refresh mode. You can then proceed to do other things while leaving it running, and return a few minutes before 12:00 AM JST, when the application starts.

To start the refresh mode, click the [My Tickets](https://ticket.expo2025.or.jp/en/myticket/) button in the navigation bar at the top of the website in the browser window. Then, in the terminal window, press `Enter`. You should see the following log in the terminal:

```
[INFO] Refresh mode started. Scroll the "My Tickets" button out of view to pause, or navigate to the reservation page and press ENTER here to start reserving.
```

This indicates that the refresh mode has started.

To pause the refresh mode, scroll the navigation bar at the top with the "My Tickets" button out of view.

To stop the refresh mode, navigate to a webpage other than the "My Tickets" (https://ticket.expo2025.or.jp/en/myticket/) page.

### Reserve mode

The reserve mode helps you reserve a slot in the pavilion you want to visit.

To start the reserve mode, go to the browser window, enter the first-come, first-served applications or pavilions / events on site registration page, select the ticket you want to use for reservation, search for the desired pavilion, and click into the pavilion. Then, in the terminal window, press `Enter`. Depending on the application type and the pavilion availability, you should see one of the following log in the terminal:

```
No available slots yet...
Found an available slot! Attempting to book...
Attempted on-site reservation.
```

These indicate that the reserve mode has started.

Reserve mode will continuously check for the availability of the pavilion and attempt to make a reservation for you, until you leave the reservation webpage of the pavilion.

It is recommended to leave it running until you reserve successfully, as the reservation slots will become available again if someone cancels their reservation.

You can open multiple instances of `reserve.exe` and run them in parallel for the same pavilion or different pavilions to increase your chances.

### Stop

To stop the reserver, simply close the terminal window. The browser window will close soon afterwards.

## Development guide

### Dependencies

- Python 3.10
- Selenium 4.35.0
- PyInstaller 6.15.0 (for packing the script into .exe)

### Use another browser

Simply substitute the `edge` occurrences in `selenium.webdriver.edge` and `webdriver.Edge` to another browser supported by Selenium. Get the corresponding webdriver for your browser (for example, [Geckodriver](https://github.com/mozilla/geckodriver) for Mozilla Firefox, [Chromedriver](https://developer.chrome.com/docs/chromedriver/downloads) for Google Chrome), and change `driver_path` accordingly.

### Use another OS

Refer to [Use another browser](#use-another-browser), get the corresponding webdriver for your OS, and change `driver_path` accordingly.

### Compile

Compile with:

```cmd
pyinstaller --onefile reserver.py
```

