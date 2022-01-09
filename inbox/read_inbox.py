import imaplib
import email

from email.header import decode_header
import os
import getpass

host = "imap.gmail.com"
user = input("Please enter your email: ")
password = getpass.getpass("Please enter password: ")


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)


def inbox():
    # create an IMAP4 class with SSL
    imap = imaplib.IMAP4_SSL(host)
    # authenticate
    imap.login(user, password)

    # select a mailbox (inbox, spam, etc)
    # imap.list() for all available mailboxes
    # messages - total number of msgs
    typ, messages = imap.select("INBOX")
    # isolate total number of emails from the response
    messages = int(messages[0])

    # change how many messages to display here
    total_emails = messages

    if messages == 0:
        print("There are no unseeen messages in this mailbox")
        return
    else:
        # loop over each email
        # loop from top to bottom
        # to get oldest message first, loop range(n)
        for i in range(messages, messages - total_emails, -1):
            # fetch email message by ID
            # returns type and data
            typ, msg = imap.fetch(str(i), "(RFC822)")

            for response in msg:
                if isinstance(response, tuple):
                    # Parse bytes into a msg object
                    # see all keys in the msg object with msg.keys()
                    msg = email.message_from_bytes(response[1])
                    print(msg)

                    # destructure the subject and encoding
                    # decode subject of the email
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # if subject is bytes, decode to str
                        subject = subject.decode(encoding)

                    # destructure the sender and encoding
                    # decode email sender
                    From, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes):
                        # if sender is bytes, decode to str
                        From = From.decode(encoding)

                    # destructure date and encoding
                    # decode the tuple
                    Date, encoding = decode_header(msg["Date"])[0]
                    print(decode_header(msg["Date"]))
                    if isinstance(Date, bytes):
                        Date = Date.decode(encoding)

                    print("Subject: ", subject)
                    print("From: ", From)
                    print("Date: ", Date)

                    # if email is multipart
                    if msg.is_multipart():
                        # iterate over parts
                        for email_part in msg.walk():
                            # get content type from the header
                            content_type = email_part.get_content_type()
                            # if email has attachment, detect it under "Content-Disposition" header tag
                            content_disposition = str(email_part.get("Content-Disposition"))
                            try:
                                # get email body
                                # return a reference to the payload
                                email_body = email_part.get_payload(decode=True).decode()
                            except:
                                pass

                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                # skip attachments and print plaintext
                                print(email_body)
                            elif "attachment" in content_disposition:
                                # download attachment
                                # return file name from payload
                                filename = email_part.get_filename()
                                if filename:
                                    folder_name = clean(subject)
                                    if not os.path.isdir(folder_name):
                                        # make folder for email, based on subject
                                        os.mkdir(folder_name)
                                    filepath = os.path.join(folder_name, filename)
                                    # download attachment and save
                                    open(filepath, "wb").write(email_part.get_payload(decode=True))
                    else:
                        # extract content-type of email
                        content_type = msg.get_content_type()
                        # get email body
                        email_body = msg.get_payload(decode=True).decode()
                        if content_type == 'text/plain':
                            # print only text email parts
                            print(email_body)

                    if content_type == 'text/html':
                        # if HTML, create a new HTML file
                        folder_name = clean(subject)
                        if not os.path.isdir(folder_name):
                            os.mkdir(folder_name)
                        filename = "index.html"
                        filepath = os.path.join(folder_name, filename)

                        # write file
                        open(filepath, "w").write(email_body)

                    print("-" * 100)

    # close connection
    imap.close()
    # logout
    imap.logout()


if __name__ == "__main__":
    inbox()
