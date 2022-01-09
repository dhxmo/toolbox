import smtplib
import ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass

from template import Template


class UserInputs:
    username_input = input("Enter your gmail address: ")
    password_input = getpass.getpass("Type your password and press enter: ")

    host = "smtp.gmail.com"
    port = 587

    server = smtplib.SMTP(host, port)
    context = ssl.create_default_context()
    server.starttls(context=context)
    server.ehlo()

    user_logged = False

    try:
        server.login(username_input, password_input)
        user_logged = True
        print("Successfully logged in")

        # get mail recipients
        recipients = input("How many email recipients do you have? (Enter integer): ")
        while not (recipients.isnumeric()):
            print("Please enter a valid integer")
            recipients = input("How many email recipients do you have? (Enter integer): ")

        to_emails_input = []
        # create list of recipients
        for i in range(int(recipients)):
            n = input("Enter email Address: ")
            to_emails_input.append(n)

        subject_input = input("Enter subject: ")
        while len(subject_input) == 0:
            print("Subject cannot be empty")
            subject_input = input("Enter subject: ")

        template_name_input = input("Enter template you'd like to use: ")
        while len(template_name_input) == 0:
            print("template cannot be empty. Please enter a file name.")
            template_name_input = input("Enter template you'd like to use: ")

        context_key_input = input("Which property would you like to edit? ")
        while len(context_key_input) == 0:
            print("template cannot be empty. Please enter a file name.")
            context_key_input = input("Enter template you'd like to use: ")

        context_value_input = input("Enter enter value: ")
        while len(context_value_input) == 0:
            print("template cannot be empty. Please enter a file name.")
            context_value_input = input("Enter template you'd like to use: ")

        context_input = {context_key_input: context_value_input}
    except smtplib.SMTPAuthenticationError:
        print("Incorrect email/password")


class SendMail:
    # instantiate user inputs class
    user_inputs = UserInputs()

    username = user_inputs.username_input
    password = user_inputs.password_input
    to_emails = []
    subject = ""
    template_name = ""
    context_template = {}

    def __init__(self, subject="", template_name=None, context_template={}, to_emails=None):
        if template_name is None and subject is None:
            raise Exception("template/subject cannot be empty")

        self.subject = subject
        self.template_name = template_name
        self.context_template = context_template
        assert isinstance(to_emails, list)
        self.to_emails = to_emails

    def format_msg(self):
        # create a multipart email
        msg = MIMEMultipart('mixed')
        msg['Subject'] = self.subject
        msg['From'] = self.username
        msg['To'] = ", ".join(self.to_emails)

        if self.template_name is not None:
            template_str = Template(template_name=self.template_name, context=self.context_template)
            txt_part = MIMEText(template_str.render(), 'plain')
            print(txt_part)
            msg.attach(txt_part)

        # return the entire formatted msg as a string
        return msg.as_string()

    def send_mail_template(self):
        # create mail
        msg = self.format_msg()

        confirm = input("Are you ready to send the mail? (Y/n): ")
        confirm.lower()
        while confirm != 'y' and confirm != 'n':
            print("Please enter a valid character")
            confirm = input("Are you ready to send the mail? (Y/n): ")

        if confirm == 'y':
            try:
                user_inputs.server.sendmail(self.username, self.to_emails, msg)
                print("Your mail was sent successfully")
                user_inputs.server.quit()
            except smtplib.SMTPException:
                print("Error: BAD request")
        else:
            return "exiting without sending mail"


if __name__ == "__main__":
    user_inputs = UserInputs()
    if user_inputs.user_logged:
        mail = SendMail(user_inputs.subject_input, user_inputs.template_name_input,
                        user_inputs.context_input, user_inputs.to_emails_input)
        mail.send_mail_template()
