import imaplib
import email
import datetime


def take_mess(last):
    """
    Checks email and draws up messages.
    :param last: int
    :return: text: str, lenght: int

    """
    text = ''
    conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    conn.login("urmail@gmail.com", "password")
    conn.select("INBOX")
    date = (datetime.date.today()).strftime("%d-%b-%Y")

    typ, data = conn.search(None, '(SENTSINCE {date})'.format(date=date))
    lenght = len(data[0].split())
    if lenght == last:
        return "NO", lenght
    if last > lenght:
        return "NO", 0

    message_ids = data[0].split()
    message_ids.reverse()
    for n in range(lenght - (lenght - last)):
        message_ids.pop()
    message_ids.reverse()

    for num in message_ids:
        typ, data = conn.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        # converts byte literal to string removing b''
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)
        mes = email_message.get_payload()
        text = text + "\n" + "Message from: " + str(email_message['From'].split(" ")[1]) + "\n" + "Head: "\
                    + str(email_message['subject']) + "\n" + str(mes)

    conn.close()
    conn.logout()
    return text, lenght
