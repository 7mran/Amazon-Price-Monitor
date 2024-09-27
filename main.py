# Import Libraries
from bs4 import BeautifulSoup
import requests
import time
import csv
import pandas as pd
import re
import datetime
import os
import smtplib
from email.message import EmailMessage


urls = []# Insert the urls of the Amazon products you want to monitor

def check_price(urls):

    headers = {"User-Agent": "your-user-agent-string-here"}# Insert your user agent here
    file_exists = os.path.exists('priceMonitorDataFeed.csv')
    price_changed = False  # Flag to track if a price has changed
    price_change_details = ""  # String to collect details for the email alert

    for url in urls:
        try:
            # Attempting to retrieve the webpage content
            page = requests.get(url, headers=headers)
            page.raise_for_status()  # Raise an error if the page couldn't be retrieved

            # Scraping the relevant html from the webpages
            soup1 = BeautifulSoup(page.content, 'html.parser')
            soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

            # Extract product title and price
            title = soup2.find(id='productTitle').get_text(strip=True)
            price = soup2.find('span', class_='aok-offscreen').get_text(strip=True)
            price = re.search(r'£(\d+\.\d+)', price).group(1)

            today = datetime.date.today()

            header = ['Title', 'Price (GBP)', 'Date']
            data = [title, price, today]

            with open('priceMonitorDataFeed.csv', 'a+', newline='', encoding='UTF8') as file:
                writer = csv.writer(file)

                if not file_exists or os.stat('priceMonitorDataFeed.csv').st_size == 0:
                    writer.writerow(header)
                    file_exists = True

                writer.writerow(data)

                # Load the CSV data into a DataFrame to compare prices
                df = pd.read_csv('priceMonitorDataFeed.csv')

                # Acquire the previous price of the product
                product_history = df[df['Title'] == title]

                if len(product_history) > 1:
                    # Compare the last entry with the new entry for a change in price
                    last_price = product_history.iloc[-1]['Price (GBP)']

                    if float(price) != float(last_price):
                        print(
                            f"Price change detected for {title}: Old Price: £{last_price}, New Price: £{price}")
                        price_changed = True
                        price_change_details += f"{title}:\nOld Price: £{last_price}\nNew Price: £{price}\nProduct URL: {url}\n\n"
                    else:
                        print(f"No price change for {title}. Current Price: £{price}")
                else:
                    # If there are no previous entries, then the product will be logged for the first time
                    print(f"First entry for {title}. Price: £{price}")

        except Exception as e:
            # If any errors occur, skip and return the product that caused the error
            print(f"Unable to retrieve data for URL: {url}. Error: {str(e)}")

    return price_changed, price_change_details

# Basic function which enables the user to send notifications via email
def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg["subject"] = subject
    msg["to"] = to

    user = "insertyourgmail@gmail.com"# Enter your gmail
    msg['from'] = user
    password = "XXXXXXXXXXXXXXXX"# Enter your app password

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()


# Runs the check_price function after regular intervals, appending the data to the .csv file
while True:
    price_changed, price_change_details = check_price(urls)

    if price_changed:
        # Send email only if a price change is detected
        email_alert("Price Updates",price_change_details,"insertyourgmail@gmail.com")# Enter your gmail once more

    time.sleep(300)# Sleep for x seconds before repeating the process


