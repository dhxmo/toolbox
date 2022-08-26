import random
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import smtplib
import itertools

# email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# system date and time manipulation
import datetime

now = datetime.datetime.now()
load_dotenv()

# email content placeholder
content = ''


def extract_news():
    todays_url = 'https://timesofindia.indiatimes.com/explainers'
    response = requests.get(todays_url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    headline_data = soup.find("div", class_="pE3Ep").find('ul')

    email_body = ''

    email_body += 'Good Morning kiddo. Today we read Times Of India Explainers. Try to digest ' \
                  'it without letting it affect your opinions much: <br />\n <br />\n'
    all_news = []

    # iterate over elements
    for i, news in enumerate(headline_data.find_all("li")):
        body = ''
        body += '<a href="' + news.a.get('href') + '">' \
                + news.text + '</a>' + '<br />\n' + '<br />\n'
        # add items to a list
        all_news.append(body)

    # shuffle the list
    random.shuffle(all_news)

    n = 5
    # iterate over the first 5 elements of the randomized list
    for i in itertools.islice(all_news, n):
        email_body += '- ' + i

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
