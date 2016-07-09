from twilio.rest import TwilioRestClient

account = 'AC193ca6d2bc9ad6cad72f784b08bdb5ea'
token = 'edae3f8a9b63c6326ddf6dbb6e965ae1'
client = TwilioRestClient(account, token)

def send_sms():
    sms = client.messages.create(to='15714712696', from_='12245237427', body='hello')

for message in client.messages.list(from_='15714712696'):
    print(message.body)
    print(message.date_sent)
