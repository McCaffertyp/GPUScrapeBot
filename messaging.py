import smtplib


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
        # Start email server
        self.server = smtplib.SMTP(self.smtp, self.port)
        self.init_server()

    def init_server(self):
        # Start server
        self.server.starttls()
        # Login to server
        self.server.login(self.email, self.password)

    def send_message(self, status):
        message = "<{}>\r{}".format(self.sender, status)
        self.server.sendmail(self.email, self.sms_gateway, message)
        self.server.quit()
