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


urls = ["https://www.amazon.co.uk/Apple-Smartwatch-Midnight-Aluminium-Detection/dp/B0CHX9M2NP/ref=asc_df_B0CHX9M2NP/?tag=googshopuk-21&linkCode=df0&hvadid=696285193871&hvpos=&hvnetw=g&hvrand=8258149886473685580&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9046009&hvtargid=pla-2281435175938&psc=1&mcid=b8af23ca98ec3ca59f96a8b37231048e&th=1&psc=1&hvocijid=8258149886473685580-B0CHX9M2NP-&hvexpln=74&gad_source=1",
        "https://www.amazon.co.uk/Apple-Watch-Smartwatch-Aluminium-Always/dp/B0DGHYD4P4/ref=sr_1_3?crid=K7CPU7ZZGOPM&dib=eyJ2IjoiMSJ9.1GsX_-RzudiusB1CQqnoS0LplXkMydeKIyc75Kq51WusJ83BdkNu_KPKE305YbI_011UrpCAgaNIk4aElV5gzTbTd441KAdbxBVnTRYJCe0ueB1x9WlZv4qnryvhH_POpTsuuz8MyC1y6kz1_MIZNSI2wwiEdwLNwJ1a65D4LyQtAYESa0w-669nXZPbuRNxeNhOKUfCp3NaEqEMTbR9jLDvPEA3YgFYE-eQlZp7a0M.OOeX5SSXAhxRDqsv7xfiznFYzS3iGAmjbbUheUcTKaY&dib_tag=se&keywords=Apple+Watch+Series+10+GPS+42+mm+Smartwatch+with+Jet+Black+Aluminium+Case+with+Black+Sport+Band+-+S%2FM.+Fitness+Tracker%2C+ECG+App%2C+Always-On+Retina+Display%2C+Water+Resistant&qid=1726270527&sprefix=apple+watch+series+10+gps+42+mm+smartwatch+with+jet+black+aluminium+case+with+black+sport+band+-+s%2Fm.+fitness+tracker+ecg+app+always-on+retina+display+water+resistant%2Caps%2C60&sr=8-3",
        "https://www.amazon.co.uk/Apple-Cellular-Smartwatch-Aluminium-Always/dp/B0DGHPB9FH/ref=sr_1_4?crid=3DZZ5ZHGRJB4C&dib=eyJ2IjoiMSJ9.whKEp2NEwO0F80z0kUVJV4TJuHuotGuvS1Vg_reIQtX9p0-On3FPMJJ0VYL1oF1vk9K9BNLPQKQGWaktAl6NLm3PjeOaLmv3EyKHvgmvoVVpPmEkuoE6NSRBIKC4TLB5dg1T52Mvc6cTanL2kCJQ0de0M67m-N7HEt1m-HK-ozAL-sjkBQoHzX6fi74YKXFsGdjm2i5C6d2aChPI5TxYa_pWH1MeZME7Bxh9SoYAhxQ.cGNhYOaxedCyCD4nPuhjEQpXB8j4l8pJ_SKYE71H9jI&dib_tag=se&keywords=apple+watch+series+10&qid=1726270608&sprefix=apple+watch+sereis+10%2Caps%2C76&sr=8-4",
        "https://www.amazon.co.uk/Apple-iPad-Air-11-inch-Landscape/dp/B0D3J7Q6PS/ref=sr_1_1?crid=2DKEEV28AOPCQ&dib=eyJ2IjoiMSJ9.LvGe-sjB3jqDkQWeLhmb3RXCMs-RN9KPp7WyuUkfP50GnzAUdZgzcEjvn5y9zAz77YOcRWBvD0wbDoXQZkcqIyxt93ZB2zsLbHrqX3Ky8v6aWTGVFmvaDXGUCvDFvfJ_bVQRRHw8bMtEts3hZPqG0EpiJkWAhN5YbXWf3HK0qY3EwPV6gov2PCdMfhnzxpB0lrLP9TV3mXa7FdqTagB_VpBbnwfvap6_K50Yofo_Fnk.TIa6UttRnRfK9disGL1irFZRYWIq-_-CwytQT5WRUCQ&dib_tag=se&keywords=ipad+air+m2&qid=1726270665&sprefix=ipad+air+%2Caps%2C86&sr=8-1",
        "https://www.amazon.co.uk/Apple-iPhone-128-Intelligence-Ultramarine/dp/B0DGHV5FF8/ref=sr_1_3?crid=7XAGQZN97MK5&dib=eyJ2IjoiMSJ9.G4QLRhZZ1TDHFiQtjhYRFDrmVkIPOCqegsTX1-M7ru3qVeUYGmHuvU3uMRSEQgQo-27iwGboGGDeepfbGIN7dcXSu0ixHHTfboW9Fj-ICdhQnXrlBASCsKT42p8-3FGh3Rtrq2UDC3CIcjr8sYYQzCCxMBpraxpjsVgpu9b_DO3Xte5OppbTO6s_5E5LtB7kKV52xW4d0nEsOWDoiLIDuRkscXws0x5k9lf-YvVw1R8.VWklYycKPEFe7jka1qroWjx9gabus1Z6BNXc-1TvIrE&dib_tag=se&keywords=iphone+16&qid=1726270699&sprefix=iphone%2Caps%2C84&sr=8-3",
        "https://www.amazon.co.uk/Playstation-711719577157-PlayStation-Console-Slim/dp/B0CM9VHGY7/ref=sr_1_4?crid=1TGN1215BU95R&dib=eyJ2IjoiMSJ9.LkyEB4b8roL9SBGlmTuXTlhw1vNwQcOtOM8oTfVMAKTwgPyGfk4dsjVCKkbOgOqzXLUwVrGFXClHjg9ymdtqzuGsxnXAMCZ4k5UYCN2gBpC6A5kSUoTbrxXpm8123l1rigYpA7ikCMjGVnjXtEHlg8DrLXRJVx6L-y7rBEyEdsrlR1uStJc97Co3FGaYbh3QWDlFxdOXIAGlUGp9xsDUDikwtb7iN1P9YFXZ3Wj3d_Y.s1iKQTW8ifBVgAu4CjyZbhnRbQeBtgrGli3cEteBo04&dib_tag=se&keywords=ps5&qid=1726270842&sprefix=ps5%2Caps%2C88&sr=8-4",
        "https://www.amazon.co.uk/PlayStation-5-Digital-Console-Slim/dp/B0CM9VKQ5N/ref=sr_1_1?crid=VUP73NGN2CRK&dib=eyJ2IjoiMSJ9.LkyEB4b8roL9SBGlmTuXTkB_q8ig1BvBWUL7q5SPDRL4cEqUbvPONyn8uU-9BgjZgFk1h3CcXYDWwAUiwmGrRJY0gV2l82afYdz-5hUOrCg_IC1u15vXz2HstYgFqR5s2IfBDEcAb_SfpMhYlOVth0W8p3TPJnTQL9DVjXOKvjNDqoCrqmmbiQS4whWgfQWmgnq96vCGGN1pixK82E191JjEQdciaDS18wRGbMES8Bg.LOMTx0OHeGqZy3_SWJvUvxYBRtuKFfX3Uyb2dL8hlZw&dib_tag=se&keywords=ps5%2Bpro&qid=1726270979&sprefix=ps5%2Bpro%2Caps%2C78&sr=8-1&th=1",
        "https://www.amazon.co.uk/Apple-MU8F2ZM-A-Pencil-Generation/dp/B07K2PK3BV/ref=sr_1_4?crid=2LGR6DZYLYS0A&dib=eyJ2IjoiMSJ9.S3aK0T1H6AYgGDU1xJai9KM2Lg4ZSdV-J2POCvb9U7vTo-xvP2M15MJcr70eBdI3ZcIRZpqpU11OGJUD9G1JQuYw4OPA6f8Cu6uPW3CUPjZTPlSaYCKvxyZZWMEo7Bwo6gni1VGir106NLwOrpd2zwKvMJ2hmJ-TnvXF7mHCQrhWTQJiEe925SwYcjLQ1rP_m0yDhIlov0gti2rLy50s1O9rgziuqWiLi2Byct1-Kyo.HvdujxKh9KKZhgRQ4h-_x6g824oanasQXETOZSj9VB0&dib_tag=se&keywords=apple+pen&qid=1726271038&sprefix=apple+pen%2Caps%2C121&sr=8-4"]

def check_price(urls):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}
    file_exists = os.path.exists('priceMonitorDataFeed.csv')

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

            print(f"Successfully processed: {title}")

        except Exception as e:
            # If any error occurs, skip and return the product that caused the error
            print(f"Unable to retrieve data for URL: {url}. Error: {str(e)}")

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg["subject"] = subject
    msg["to"] = to

    user = "insertyourgmail@gmail.com"
    msg['from'] = user
    password = "xxxxxxxxxxxxxxxx"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()


# Runs the check_price function after regular intervals, appending the data to the .csv file
while(True):
    check_price(urls)
    data_feed = pd.read_csv(r'priceMonitorDataFeed.csv')
    print(data_feed)
    email_alert("Price Updates", "The price of a listing you have been monitoring has been updated", "insertyourgmail@gmail.com")
    time.sleep(300) # Sleep for x seconds before repeating the process