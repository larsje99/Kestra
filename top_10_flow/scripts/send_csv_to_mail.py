import smtplib
import requests
from bs4 import BeautifulSoup
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

def SendCSVToMail():
    # SCRAPING FROM ULTRATOP
    print("SUCCES1")
    request = requests.get("https://www.ultratop.be/nl/ultratop50").text
    print("SUCCES2")
    soup = BeautifulSoup(request, "html.parser")

    songElements = soup.find_all("div", {"class": "chart_title"})

    songList = []  # Initialize an empty list to store the dictionaries

    for songIndex in range(0, 10):
        song = songElements[songIndex]
        artistName = song.find("b").get_text()
        songName = song.get_text().replace(artistName, "").strip()
        place = str(songIndex + 1) + "."

        songDict = {
            'Place': place,
            'artistName': artistName,
            'songName': songName
        }

        songList.append(songDict)  # Add the dictionary to the list

    data_list = songList
    dataframe = pd.DataFrame(data_list)
    dataframe.to_csv("csv_file.csv", index=False, sep=";")

    # Email configuration
    sender_email = 'lars.nolf@telenet.be'
    receiver_email = 'lars.nolf@telenet.be'
    subject = 'Weekly Top 10 Chart'
    message = 'Hello there! In the attachments you can find the list of top 10 songs of this week!'

    # Create a multipart message and set the headers
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, 'plain'))

    # Attach the CSV file
    # Open the file in bynary mode
    with open("csv_file.csv", 'rb') as file:
        # Add the file as an attachment
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())

    # Encode the file in ASCII characters to send by email    
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename="csv_file.csv")
    msg.attach(part)

    # SMTP server configuration (for Telenet account)
    smtp_server = 'smtp.telenet.be'
    smtp_port = 587
    smtp_username = 'lars.nolf@telenet.be'
    smtp_password = 'T.NN$fyk977!r_H'

    # Create a secure connection to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    # Send the email
    server.send_message(msg)

    # Close the SMTP server connection
    server.quit()