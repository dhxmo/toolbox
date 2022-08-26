import random
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import smtplib

# email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# system date and time manipulation
import datetime

now = datetime.datetime.now()
load_dotenv()

# email content placeholder
content = ''

urls_dict = {
    'telecom': 'https://economictimes.indiatimes.com/industry/telecom',
    'transport': 'https://economictimes.indiatimes.com/industry/transportation',
    'services': 'https://economictimes.indiatimes.com/industry/services',
    'biotech': 'https://economictimes.indiatimes.com/industry/healthcare/biotech',
    'svs': 'https://economictimes.indiatimes.com/industry/indl-goods/svs',
    'energy': 'https://economictimes.indiatimes.com/industry/energy',
    'consumer_products': 'https://economictimes.indiatimes.com/industry/cons-products',
    'finance': 'https://economictimes.indiatimes.com/industry/banking/finance',
    'automobiles': 'https://economictimes.indiatimes.com/industry/auto'
}


def extract_news():
    todays_url = random.choice(list(urls_dict.values()))
    response = requests.get(todays_url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    headline_data = soup.find("ul", class_="list1")

    email_body = ''

    email_body += 'Good Morning kiddo. Heres what happening in the world today: <br />\n <br />\n'

    url = 'https://economictimes.indiatimes.com'
    for i, news in enumerate(headline_data.find_all("li")):
        link = '%s%s' % (url, news.a.get('href'))
        email_body += str(i + 1) + '. ' + '<a href="' + link + '">' + news.text + '</a>' + '<br />\n' + '<br />\n'

    email_body += '<br>---------------------------------<br>'
    email_body += '<br><br>Thats all for today. Byeeee'

    return email_body


def send_mail(news_body):
    SERVER = 'smtp.gmail.com'
    PORT = 587
    FROM = 'homesanct@gmail.com'
    TO = 'dhrvmohapatra@gmail.com'
    PASSWORD = os.getenv('password')

    msg = MIMEMultipart()
    msg['Subject'] = 'Good Morning Champ' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(
        now.year)
    msg['From'] = FROM
    msg['To'] = TO
    msg.attach(MIMEText(news_body, 'html'))

    print('initializing server')

    server = smtplib.SMTP(SERVER, PORT)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(FROM, PASSWORD)
    server.sendmail(FROM, TO, msg.as_string())

    print('Email Sent...')

    server.quit()


if __name__ == "__main__":
    data = extract_news()
    send_mail(data)
