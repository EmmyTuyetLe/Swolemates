from twilio.rest import Client
import os
os.system("source secrets.sh")

#Twilio setup
from twilio.twiml.messaging_response import MessagingResponse
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token) #client setup for verify API

verification = client.verify.services('VA13c9cf80f68fb2bd1c7e3f4a0c8e52a5').verifications.create(to='emilytuyetle@gmail.com', channel='email') #send user the email with verification code
sms_verification = client.verify.services('VA13c9cf80f68fb2bd1c7e3f4a0c8e52a5').verifications.create(to='+17815348226', channel='sms')
print(verification.sid)

verification_check = client.verify.services('VA13c9cf80f68fb2bd1c7e3f4a0c8e52a5').verification_checks .create(to='emilytuyetle@gmail.com', code='123456') #make sure user entered right verification code
sms_verification_check = client.verify.services('VA13c9cf80f68fb2bd1c7e3f4a0c8e52a5').verification_checks .create(to='+17815348226', code='089087') #make sure user entered right verification code
print(verification_check.sid)

print(verification.sid)

