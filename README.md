# Amazon Price Monitor

This is a Python-based web scraping tool that tracks product prices on Amazon UK. It periodically monitors specified product URLs and logs the prices in a CSV file. When a price change is detected, the tool sends an email alert with the updated details.

## Features

- **Price Monitoring**: Automatically scrapes and logs product prices from Amazon UK at regular intervals.
- **CSV Logging**: Appends the product name, price, and date to a CSV file (`priceMonitorDataFeed.csv`) for historical tracking.
- **Email Notifications**: Sends email alerts when price changes are detected.
- **Error Handling**: Robust handling of network errors or inaccessible product pages.

## Setup

### Prerequisites

- Python 3.x
- Required Python libraries:
  - `bs4` (BeautifulSoup for web scraping)
  - `requests` (for making HTTP requests)
  - `pandas` (for CSV data handling)
  - `re` (regular expressions for extracting price data)
  - `smtplib` (for sending emails)

### Gmail Setup for Email Alerts

1. Ensure **two-factor authentication (2FA)** is enabled on your Gmail account. If you haven't enabled 2FA, follow [this guide](https://support.google.com/accounts/answer/185839).
  
2. After enabling 2FA, generate an **App Password**. This password will be used in the script to send email alerts:
   - Go to [App Passwords](https://myaccount.google.com/apppasswords).
   - Under **Select App**, choose **Mail**.
   - Under **Select Device**, choose **Other (Custom name)** and enter a name like "Price Tracker".
   - Click **Generate** and copy the generated password. 

   > **Important:** Never share this app password with anyone else. It's like a special key that allows the script to send emails through your Gmail account.

3. Store this app password securely. You will need it for the next steps.

### Inserting Your User-Agent:

- The script requires your User-Agent string for web scraping.
- To find your User-Agent:
  - Visit https://httpbin.org/get.
  - In the JSON response, locate the "user-agent" field. It will look something like:
  ```bash
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
  ``` 
  - Copy your User-Agent string
  - Insert it in the headers variable within the code as shown:
  ```bash
  - headers = {
    "User-Agent": "your-user-agent-string-here"
    }
    ```
### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/amazon-price-tracker.git
    cd amazon-price-tracker
    ```

2. Install the required dependencies:
    ```bash
    pip install beautifulsoup4 requests pandas
    ```

3. Create a file named `config.py` to store your Gmail credentials securely:
    ```python
    EMAIL_USER = 'your-email@gmail.com'
    EMAIL_PASS = 'your-app-password-here'
    ```

   Replace `your-email@gmail.com` with your Gmail address and `your-app-password-here` with the app password you generated in the Gmail setup step.

4. Update the `urls` list with the Amazon UK product URLs you want to monitor in the `check_price` function.

## Usage

1. Run the script:
    ```bash
    python price_tracker.py
    ```

2. The script will monitor prices every 5 minutes (adjustable with the `time.sleep()` function) and log data into `priceMonitorDataFeed.csv`.

3. If a price change is detected, an email notification will be sent to the designated email address with the price change details.

### Example Email Notification

    Subject: Price Updates

    Apple Watch Series 10:
    Old Price: £399.00 
    New Price: £379.00 
    Product URL: https://www.amazon.co.uk/product-link
    
    iPhone 16: 
    Old Price: £1,199.00 
    New Price: £1,149.00 
    Product URL: https://www.amazon.co.uk/product-link

### CSV Format

The `priceMonitorDataFeed.csv` file will have the following structure:

| Title                    | Price (GBP) | Date       |
|---------------------------|-------------|------------|
| Apple Watch Series 10      | 399.00      | 2024-09-20 |
| iPhone 16                  | 1149.00     | 2024-09-20 |
| ...                        | ...         | ...        |

## Configuration

- **Email Settings**: The `email_alert` function uses Gmail SMTP for sending emails. Update the email and password details in the `config.py` file, ensuring the password is the app password you generated.
  
- **Monitoring Interval**: The interval between price checks is controlled by the `time.sleep(300)` function, which is set to 5 minutes (300 seconds) by default. You can adjust this as needed.

## Notes

- Make sure your Amazon UK URLs are correct and accessible. If the script cannot retrieve the webpage, it will log an error message but continue with the next URL.
- Keep in mind that Amazon can sometimes block scraping activities. If you experience issues, consider adding a proxy or using different headers to simulate a real browser.

## License

This project is open-source and available under the [MIT License](LICENSE).


