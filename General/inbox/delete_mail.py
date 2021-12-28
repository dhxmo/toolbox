import imaplib
import getpass

host = "imap.gmail.com"
username = input("Please enter gmail address: ")
password = getpass.getpass("Please enter your password: ")


def delete_mail():
    # connect to IMAP server
    imap = imaplib.IMAP4_SSL(host)
    # authenticate
    imap.login(username, password)

    # Change mailbox here
    # imap.select("[Gmail]/Bin")
    # imap.select("[Gmail]/Spam")
    imap.select("INBOX")

    # use keyword SINCE to delete all mails since date
    # use keyword ALL to delete all mails
    # use keyword FROM "<email>" to isolate one address and delete msgs
    # messages is a space-separated list of matching message numbers.
    status, messages_id_list = imap.search(None, 'ALL')

    # convert string id to a list of all searched mail IDs
    messages = messages_id_list[0].split(b' ')

    if messages == [b'']:
        print("Mailbox is empty")
        return
    else:
        print("Deleting mails... This may take a while")
        count = 1
        for mail in messages:
            # mark mail as deleted. Alters flag dispositions for messages in mailbox
            imap.store(mail, "+FLAGS", "\\Deleted")
            count += 1

        # Permanently remove deleted items from selected mailbox
        imap.expunge()
        print(f"{count} mails have been deleted. Logging out.")

    # Close currently selected mailbox
    imap.close()
    # logout
    imap.logout()


if __name__ == "__main__":
    delete_mail()
