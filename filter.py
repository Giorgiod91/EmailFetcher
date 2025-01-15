import imaplib
from dotenv import load_dotenv
import os
import argparse
import email 
import csv
from email.header import decode_header

# Load environment variables from .env file
load_dotenv()

# IMAP Configuration
imap_host = "imap.gmx.net"
imap_user = os.getenv("mail")
imap_pass = os.getenv("pw")

data = ["Email ID", "Subject", "From", "Importance"]
csv_file = "emails.csv"

def add_data_to_cv():
    if os.path.exists(csv_file):
        print(f"file allready exist")
        
    else:
        with open(csv_file, mode="w", newline="")as file:
            writer = csv.writer(file)
            writer.writerows(data)
            print(f"dataset: {csv_file} was created")

# delete data function if needed (should not be accesable to the user later on )

def delete_csv():
    if os.path.exists(csv_file):
        os.remove(csv_file)
        print(f"csv file {csv_file} delete succesfull !")


# boilerplate Function to decode MIME-encoded subjects
def decode_mime_subject(encoded_subject):
    decoded_subject, encoding = decode_header(encoded_subject)[0]
    if isinstance(decoded_subject, bytes):
        decoded_subject = decoded_subject.decode(encoding if encoding else 'utf-8')
    return decoded_subject

# filter function 1 for importany 0 for not important

def binary_filter(email_id, email_subject, email_from):
    # for practise now if the email contains linkedin it will be markes as 1 (important)
    important = 0
    if "linkedin" in email_from.lower():
        important = 1
        print(f"Email ID: {email_id} | Subject: {email_subject} | From: {email_from} is important.")
    else:
        print(f"Email ID: {email_id} | Subject: {email_subject} | From: {email_from} is not important.")

    decoded_subject = decode_mime_subject(email_subject)
    clean_email_from = email_from.replace("From: ", "").strip()
    
    # Add email to CSV with its importance
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([email_id, decoded_subject, clean_email_from, important])


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
                    binary_filter(email_id, email_subject, email_from)
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
    elif args.command == "dataset":
        add_data_to_cv()

    elif args.command == "del":
        delete_csv()
    

   

if __name__ == "__main__":
    main()


