import imaplib
from dotenv import load_dotenv
import os
import argparse
import email 

# Load environment variables from .env file
load_dotenv()

# IMAP Configuration
imap_host = "imap.gmx.net"
imap_user = os.getenv("mail")
imap_pass = os.getenv("pw")



# Function to connect to the mail server and retrieve emails
def fetch_specific():
    # array to save emails to later use them in other function
    emails = []
    # Connecting to the IMAP server
    imap = imaplib.IMAP4_SSL(imap_host)
    imap.login(imap_user, imap_pass)

    # Select the INBOX folder
    status, messages = imap.select("INBOX")
    print(f"Select status: {status}, messages: {messages}")
    
    # List all folders
    status, folders = imap.list()
    print(folders)

    # Fetch all email IDs
    status, email_ids = imap.search(None, "ALL")
    if status == "OK":
        email_ids = email_ids[0].split()
        for email_id in email_ids[-10:]:  # Get last 10 emails
            status, email_data = imap.fetch(email_id, "(BODY[HEADER.FIELDS (SUBJECT FROM)])")
            if status == "OK":
                email_subject = email_data[0][1].decode()
                email_from = email_data[0][1].decode().split("From: ")[1].split("\r\n")[0]
                if "linkedin" in email_from.lower():
                    print(f"Email ID: {email_id} | Subject: {email_subject} | From: {email_from}")
                    emails.append(email_id)


    
    else:
        print("No emails found.")

    

    
    
   
    imap.logout()
    return emails

def fetch_first_ten_mails():
    # array to save emails to later use them in other function
    emails = []
    # Connecting to the IMAP server
    imap = imaplib.IMAP4_SSL(imap_host)
    imap.login(imap_user, imap_pass)

    # Select the INBOX folder
    status, messages = imap.select("INBOX")
    print(f"Select status: {status}, messages: {messages}")
    
    # List all folders
    status, folders = imap.list()
    print(folders)

    # Fetch all email IDs
    status, email_ids = imap.search(None, "ALL")
    if status == "OK":
        email_ids = email_ids[0].split()
        for email_id in email_ids[-10:]:  # Get last 10 emails
            status, email_data = imap.fetch(email_id, "(BODY[HEADER.FIELDS (SUBJECT FROM)])")
            if status == "OK":
                email_subject = email_data[0][1].decode()
                email_from = email_data[0][1].decode().split("From: ")[1].split("\r\n")[0]
                print(f"Email ID: {email_id} | Subject: {email_subject} | From: {email_from}")
                emails.append(email_id)


    
    else:
        print("No emails found.")

    

    
    
   
    imap.logout()
    return emails


def show(emails):
    
    print(f"which id u want to chech: {email}")
    id_to_check = input()
    id_to_check = str(id_to_check)
    imap = imaplib.IMAP4_SSL(imap_host)
    imap.login(imap_user, imap_pass)

    # Select the INBOX folder
    status, messages = imap.select("INBOX")

    if status =="OK":
        status, email_data = imap.fetch(id_to_check, "(BODY[TEXT])")
        print(f"email id to check: {id_to_check} body: {email_data[0][1]}" )
    else:
        print(f"error fetching email body from : {id_to_check}")

    imap.logout()



def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Trigger functions based on arguments.")
    parser.add_argument('command', type=str, help="Command to trigger the function")
    parser.add_argument('email_id', type=int, nargs='?', help="Email ID to show")

    # Parse the arguments
    args = parser.parse_args()


    if args.command == "show":
        emails= fetch_specific()
        show(emails)

    elif args.command == "fetch":
        fetch_specific()

    elif args.command == "all":
        fetch_first_ten_mails()
    

   

if __name__ == "__main__":
    main()

