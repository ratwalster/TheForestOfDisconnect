from twilio.rest import Client
import os

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(ACCOUNT_SID, AUTH_TOKEN)

message = client.messages.create(
    body="Welcome to The Forest of Disconnect! Join 5 travelers on an interactive storybook journey. Start here: https://foreststory.app/begin Reply STOP to opt out.",
    from_="+18559270843",  # Your Toll-Free Number
    to="+14254288297"      # Recipient’s number
)
print(f"Sent SMS with SID: {message.sid}")
