import imaplib
from dotenv import load_dotenv
import os
import argparse
import email 
import csv
from email.header import decode_header
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer

# Load environment variables from .env file
load_dotenv()

# IMAP Configuration
imap_host = "imap.gmx.net"
imap_user = os.getenv("mail")
imap_pass = os.getenv("pw")


data = ["Email ID", "Subject", "From", "Importance"]
csv_file = "emails.csv"






def add_data_to_cv(list_1, list_2, list_3, list_4):

    
    df = pd.DataFrame(data={"Email ID": list_1, "Subject": list_2, "From": list_3, "Importance": list_4})

    if os.path.exists(csv_file):
        df.to_csv(csv_file, mode='a', header=False, index=False)
        print(f"Appended to {csv_file}")
    else:
        df.to_csv(csv_file, index=False)
        print(f"Created new CSV file: {csv_file}")

# delete data function if needed (should not be accesable to the user later on )

def delete_csv():
    if os.path.exists(csv_file):
        os.remove(csv_file)
        print(f"csv file {csv_file} delete succesfull !")


# boilerplate Function to decode 
def decode_mime_subject(encoded_subject):
    decoded_subject, encoding = decode_header(encoded_subject)[0]
    if isinstance(decoded_subject, bytes):
        decoded_subject = decoded_subject.decode(encoding if encoding else 'utf-8')
    return decoded_subject

# filter function 1 for importany 0 for not important

def binary_filter(email_id, email_subject, email_from, list_1, list_2, list_3, list_4):
    # for practise now if the email contains linkedin it will be markes as 1 (important)
    important = 0
    if "linkedin" in email_from.lower():
        important = 1
        print(f"Email ID: {email_id} | Subject: {email_subject} | From: {email_from} is important.")
    else:
        print(f"Email ID: {email_id} | Subject: {email_subject} | From: {email_from} is not important.")

    decoded_subject = decode_mime_subject(email_subject)
    clean_email_from = email_from.replace("From: ", "").strip()

    list_1.append(email_id)  # Email ID
    list_2.append(decoded_subject)  # Subject
    list_3.append(clean_email_from)  # From
    list_4.append(important)  # Importance
    
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


    #appending list items to add those into the csv file
    list_1 = []
    list_2 = []
    list_3 = []
    list_4 = []  # Importance (1 or 0)



    # Fetch all email IDs
    status, email_ids = imap.search(None, "ALL")
    if status == "OK":
        email_ids = email_ids[0].split()
        for email_id in email_ids[-450:]:  # Get last 10 emails
            status, email_data = imap.fetch(email_id, "(BODY[HEADER.FIELDS (SUBJECT FROM)])")
            if status == "OK":
                email_subject = email_data[0][1].decode()
                email_from = email_data[0][1].decode().split("From: ")[1].split("\r\n")[0]
                emails.append(email_id)
                binary_filter(email_id, email_subject, email_from, list_1, list_2, list_3, list_4)

               # if "linkedin" in email_from.lower():
                #    print(f"Email ID: {email_id} | Subject: {email_subject} | From: {email_from}")
                 #   binary_filter(email_id, email_subject, email_from, list_1, list_2, list_3, list_4)
                  #  emails.append(email_id)


    
    else:
        print("No emails found.")

    

    
    
   
    imap.logout()
    add_data_to_cv(list_1, list_2, list_3, list_4)
    return list_1, list_2, list_3, list_4,emails

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

# get data for model training 
list_1, list_2, list_3, list_4, emails = fetch_specific()
x_training = [list_1, list_2, list_3] # x features (Email ID, Subject, From)
y_training = list_4 # importance should be my y in this case the models need to predict if its important mail or not

#logistic regression

def train():

    
    df = pd.DataFrame({
    "Subject": list_2,
    "From": list_3,
    "Importance": list_4
    })
    # vectorize text data
    # transforming text data into numerical features 
    vectorizer_subject = TfidfVectorizer(stop_words='english')
    X_subject = vectorizer_subject.fit_transform(df["Subject"])

    vectorizer_from = TfidfVectorizer(stop_words="english")
    X_from = vectorizer_from.fit_transform(df["From"])

    #combine both c features
    X_combined = hstack([X_subject, X_from])
    # define target value y
    y = df["Importance"]

    X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.2, random_state=42)

    model = LogisticRegression(C=0.1, class_weight='balanced')
    model.fit(X_train,y_train)

    predictions = model.predict(X_test)

    # boilerplate print statements
    print("Accuracy: ", accuracy_score(y_test, predictions))
    print("Classification Report:\n", classification_report(y_test, predictions))






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

    elif args.command == "train":
        train()
    

   

if __name__ == "__main__":
    main()


