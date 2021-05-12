import smtplib
import time

reconnect_timeout_seconds = 10


class Message:
    def __init__(self, email, password, number, carrier):
        self.email = email
        self.password = password
        self.sms_gateway = "{}@".format(number)
        if "AT&T" in carrier:
            self.sms_gateway += "txt.att.net"
        elif "Sprint" in carrier:
            self.sms_gateway += "messaging.sprintpcs.com"
        elif "T-Mobile" in carrier:
            self.sms_gateway += "tmomail.net"
        elif "Verizon" in carrier:
            self.sms_gateway += "vtext.com"
        else:
            print("Carrier {} not currently supported. Exiting".format(carrier))
            exit(0)
        self.sender = "GPU Scraping Bot"
        self.subject = "GPU Scraping"
        self.smtp = "smtp.gmail.com"
        self.port = 587
        self.server = None
        self.smtp_connect()

    def smtp_connect(self):
        try:
            print("Starting email server")
            self.server = smtplib.SMTP(self.smtp, self.port)
            self.server.ehlo()
            print("Starting server")
            self.server.starttls()
            print("Logging into server with {}".format(self.email))
            self.server.login(self.email, self.password)
            print("Login successful")
            return True
        except Exception as error:
            print("Failed to connect with following error: {}".format(error))
            return False

    def send_message(self, status):
        print("Current update being sent:\nstatus:{}".format(status))
        message = "<{}>\r{}".format(self.sender, status)
        try:
            self.server.sendmail(self.email, self.sms_gateway, message)
        except smtplib.SMTPSenderRefused as error:
            print("smtplib.SMTPSenderRefused. Details:\n{}".format(error))
            print("Connection may be stale. Attempting reconnect...")
            reconnected = self.smtp_connect()
            if not reconnected:
                print("Reconnect attempt refused")
                print("Attempting to reconnect with {} second timeout".format(reconnect_timeout_seconds))
                for i in range(reconnect_timeout_seconds):
                    if self.smtp_connect():
                        print("Reconnect successful!")
                    else:
                        print(".", end="", flush=False)
                    time.sleep(0.95)

            print("Attempting to send message again through address {}...".format(self.email))
            print("Will try three extra attempts:")
            for i in range(3):
                print("Attempt: {}".format(i))
                try:
                    self.server.sendmail(self.email, self.sms_gateway, message)
                    print("Message successful. Continuing")
                    break
                except smtplib.SMTPSenderRefused:
                    print("Failed. Retrying")

    def quit_server(self):
        self.server.quit()
