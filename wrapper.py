from re import findall
import smtplib 
from email.message import EmailMessage

class Mail(object):

    __providers = {
        'gmail': {
            'server': 'smtp.gmail.com',
            'ssl': 465
        },
        'outlook': {
            'server': 'smtp-mail.outlook.com',
            'ssl': 465
        },
        'yahoo':{
            'server': 'smtp.mail.yahoo.com',
            'ssl': 465
        },
        'hotmail':{
            'server': 'smtp.live.com',
            'ssl': 587
        }
    }

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.__domain = findall(r'@(\w+)', self.email)[0]
        
        self.__msg = EmailMessage()
        self.__msg['From'] = self.email
 
        self.__reciver = None
        self.__subject = None
        self.__content = 'Sent from Python'
        self.__html = None

        self.__msg.set_content(str(self.__content))

    @property
    def reciver(self):
        return self.__reciver

    @property
    def subject(self):
        return self.__subject

    @property
    def content(self):
        return self.__content

    @property
    def html(self):
        return self.__html

    @reciver.setter
    def reciver(self, email):
        # For multiple recivers use an array ['email1', 'email2', ...]
        try:
            self.__reciver = email
            if (isinstance(email, list)):
                self.__msg['To'] = ', '.join(self.__reciver)
            if (isinstance(email, str)):
                self.__msg['To'] = self.__reciver
            else:
                raise TypeError
        except TypeError:
            print('Invalid reciver')

    @subject.setter
    def subject(self, subject):
        try:
            if (subject.strip()):
                self.__subject = str(subject)
                self.__msg['Subject'] = self.__subject
            else:
                raise TypeError
        except TypeError:
            print('Invalid subject')

    @content.setter
    def content(self, content):
        try:
            if (content):
                self.__content = content
            self.__msg.set_content(str(self.__content))
        except ValueError:
            print('Invalid content')

    @html.setter
    def html(self, html):
        self.__html = html
        self.__msg.add_alternative("""{}""".format(self.__html), subtype='html')

    def send(self):
        if (self.reciver and self.subject):
            with smtplib.SMTP_SSL(self.__providers[self.__domain]['server'],
             self.__providers[self.__domain]['ssl']) as smtp:
                smtp.login(self.email, self.password)
                smtp.send_message(self.__msg)

if __name__ == "__main__":
    your_email = 'example@gmail.com'
    your_password = 'password'

    m = Mail(your_email, your_password)

    # For demonstration set the reciver's email as your email.
    m.reciver = your_email

    m.subject = 'From Python'
    m.content = 'Hello world from Python'
    m.html = ''' <!DOCTYPE html>
<html>
<body>

<h1>My First Heading</h1>
<p>My first paragraph.</p>

</body>
</html>
'''
    m.send()