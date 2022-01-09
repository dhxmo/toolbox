import tkinter
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import getpass
from tkinter import filedialog
import smtplib
import ssl


def multipart_email(msg_subject, from_mail, recipient_list, msg_body, msg_html, msg_attachment):
    # create a multipart email
    msg = MIMEMultipart('mixed')
    msg['Subject'] = msg_subject
    msg['From'] = from_mail
    msg['To'] = ", ".join(recipient_list)

    # text = format_msg(msg_body)
    # convert recipient_list MIMEText object
    txt_part = MIMEText(msg_body, "plain")
    print(txt_part)
    # add recipient_list MIME multipart email
    msg.attach(txt_part)

    html_part = MIMEText(msg_html, "html")
    msg.attach(html_part)

    if msg_attachment == 'y':
        # GUI recipient_list select multiple files
        root = tkinter.Tk()
        root.withdraw()
        # root.call('wm', 'attributes', '.', '-recipient_listpmost', True)
        files = filedialog.askopenfilename(multiple=True)
        var = root.tk.splitlist(files)
        files_recipient_list_send = []
        for f in var:
            files_recipient_list_send.append(f)

        for file in files_recipient_list_send:
            # open as read in bytes
            with open(file, "rb") as f:
                # read file contents
                data = f.read()
                # create attachment
                attach_part = MIMEBase("application", "octet-stream")
                attach_part.set_payload(data)

            # encode data recipient_list base64
            encoders.encode_base64(attach_part)
            # add header
            attach_part.add_header("Content-Disposition", f"attachment; filename= {file}")
            msg.attach(attach_part)

    # return the entire formatted msg as a string
    return msg.as_string()


def send():
    from_mail = input("Enter your gmail address: ")
    password = getpass.getpass("Type your password and press enter: ")

    # set up server instance
    host = "smtp.gmail.com"
    port = 587
    server = smtplib.SMTP(host, port)
    # start a secure connection
    context = ssl.create_default_context()
    server.starttls(context=context)
    # declare ESMPTP protocol as encryption happens on starting TLS connection
    server.ehlo()

    try:
        server.login(from_mail, password)
    except smtplib.SMTPAuthenticationError:
        print("Incorrect email/password")
        return False

    recipient_list = list()
    recipients = input("How many email recipients do you have? (Enter integer): ")
    while not (recipients.isnumeric()):
        print("Please enter a valid integer")
        recipients = input("How many email recipients do you have? (Enter integer): ")

    # create list of recipients
    for i in range(int(recipients)):
        n = input("Enter email Address: ")
        recipient_list.append(n)

    msg_subject = input("Enter subject: ")
    while len(msg_subject) == 0:
        print("Please enter a valid subject")
        msg_subject = input("Enter subject: ")

    msg_body = input("Enter body: ")
    while len(msg_body) == 0:
        print("Cannot send an empty mail. Please write something before sending mail.")
        msg_body = input("Enter body: ")

    msg_html: str = '''<h6>Mail sent using Python </h6>'''

    msg_attachments = input("Would you like to attach a file? (Y/n): ")
    msg_attachments.lower()
    while msg_attachments != 'y' and msg_attachments != 'n':
        print("Enter a valid character")
        msg_attachments = input("Would you like to attach a file? (Y/n): ")

    multipart_msg_str = multipart_email(msg_subject, from_mail, recipient_list, msg_body, msg_html, msg_attachments)

    confirm = input("Are you ready to send the mail? (Y/n): ")
    confirm.lower()
    while confirm != 'y' and confirm != 'n':
        print("Please enter a valid character")
        confirm = input("Are you ready to send the mail? (Y/n): ")
    if confirm == 'y':
        try:
            # send from_mail
            server.sendmail(from_mail, recipient_list, multipart_msg_str)
            # stop server session
            server.quit()
            print("Mail was sent successfully")
        except smtplib.SMTPException:
            print("Error: BAD request")
    else:
        return "exiting without sending mail"


# calls the function only when the module itself is called
if __name__ == "__main__":
    send()
