from twilio.rest import Client
from smtplib import SMTP
import os


sms_account_sid = os.getenv("SMS_ACCOUNT_SID")
sms_auth_token = os.getenv("SMS_AUTH_TOKEN")
virtual_number = os.getenv("VIRTUAL_NUMBER")
verified_number = os.getenv("VERIFIED_NUMBER")
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(sms_account_sid, sms_auth_token)
    
    def notify_me(self, all_cheap_flight_details): # send sms
        message = self.client.messages.create(
            body=f'{all_cheap_flight_details}',
            from_=virtual_number, 
            to=verified_number,
        )
        print(message.sid)

    def send_emails(self, message: str, user_names: list, user_emails: list):
        connection = SMTP('smtp.gmail.com')
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        for name, email in zip(user_names, user_emails):
            try:
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email,
                    msg="Subject: Cheap Flight Deals - Flight Club \r\n" +
                      f"Hello, {name} \n{message}"
                )
            except:
                print(f"Error occured while sending email to {email} email id.")
        connection.close()
