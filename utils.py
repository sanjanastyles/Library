import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

def send_email():
    toaddrs = input("To: ").split()

    msg = f"From: \r\nTo: {', '.join(toaddrs)}\r\n\r\n"

    print("Enter message, end with an empty line:")

    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            break
        msg += line + '\n'

    print("Message length is", len(msg))

    # Update SMTP server and port based on your configuration
  
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()


    # Provide your email credentials for authentication
    username = os.getenv("RESET_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")
    print(password,username)
    try:
        server.login(username, password)
    except smtplib.SMTPAuthenticationError as e:
        print(f"Authentication failed: {e}")
        server.quit()
        return

    server.sendmail(username, toaddrs, msg)
    server.quit()

#  try:
#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.starttls()
#         server.login(user, pwd)
#         server.sendmail(FROM, TO, message)
#         server.close()
#         print 'successfully sent the mail'
#     except:
#         print "failed to send mail"