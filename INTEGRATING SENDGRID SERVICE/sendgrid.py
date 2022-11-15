import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

sg = sendgrid.SendGridAPIClient(api_key="APIKEY")
from_email = Email({{sender id}})  # Change to your verified sender
to_email = To("{{usermailID}}")  # Change to your recipient
subject = "EXPENDITURE LIMIT EXIST"
content = Content("text/plain", "Warning! Your this month  Expenditure Limit was Exist")
mail = Mail(from_email, to_email, subject, content)

# Get a JSON-ready representation of the Mail object
mail_json = mail.get()

# Send an HTTP POST request to /mail/send
response = sg.client.mail.send.post(request_body=mail_json)
print(response.status_code)
print(response.headers)