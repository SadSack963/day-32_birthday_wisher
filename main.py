import pandas
import random
from os import listdir
import datetime as dt
import smtplib
import os
from dotenv import load_dotenv


load_dotenv("E:/Python/EnvironmentVariables/.env")
YAHOO_SENDER = os.getenv("SMTP_YAHOO_SENDER")
YAHOO_USERNAME = os.getenv("SMTP_YAHOO_USERNAME")
YAHOO_EMAIL = os.getenv("SMTP_YAHOO_EMAIL")
YAHOO_PASSWORD = os.getenv("SMTP_YAHOO_PASSWORD")


def send_mail(to_addr):
    message = f"From: \"{YAHOO_SENDER}\" <{YAHOO_EMAIL}>\n" \
              f"To: {to_addr}\n" \
              f"Subject: Happy Birthday!\n\n" + letter
    # print(message)
    with smtplib.SMTP(host="smtp.mail.yahoo.co.uk", port=587) as connection:
        # Secure the connection
        connection.starttls()
        connection.login(user=YAHOO_USERNAME, password=YAHOO_PASSWORD)
        connection.sendmail(from_addr=YAHOO_EMAIL, to_addrs=to_addr, msg=message.encode("utf-8"))


# Read birthdays.csv as a Pandas DataFrame
df = pandas.read_csv("birthdays.csv")

# Get the current datetime
today = dt.datetime.now()

# Get a list of all files
# (directories would need filtering out if there were any)
list_files = listdir("./letter_templates")

for row in df.itertuples(index=False, name="person"):
    # Check if today matches a birthday in birthdays.csv
    if row.month == today.month and row.day == today.day:
        # Pick a random letter from letter templates
        filepath = "./letter_templates/" + random.choice(list_files)

        # Replace the [NAME] with the person's actual name from birthdays.csv
        letter = ""
        with open(filepath, mode="r") as file_in:
            for line in file_in:
                line = line.replace("[NAME]", row.name)
                letter = letter + line

        # Send the letter generated to that person's email address.
        send_mail(row.email)



