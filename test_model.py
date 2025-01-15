import joblib
from scipy.sparse import hstack

# Load the saved model and vectorizers
model = joblib.load('model.pkl')
vectorizer_subject = joblib.load('vectorizer_subject.pkl')
vectorizer_from = joblib.load('vectorizer_from.pkl')

# Define the function to test new data
def test_new_data(new_emails):
    # Extract and vectorize the subject and from fields
    subject_features = vectorizer_subject.transform([email["subject"] for email in new_emails])
    from_features = vectorizer_from.transform([email["from"] for email in new_emails])

    # Combine the features
    X_new = hstack([subject_features, from_features])

    # Make predictions
    predictions = model.predict(X_new)

    # Output the predictions
    for email, prediction in zip(new_emails, predictions):
        print(f"Subject: {email['subject']} | From: {email['from']} | Importance: {'Important' if prediction == 1 else 'Not Important'}")

# Test new emails
new_emails = [
    {"subject": "Job opportunity at XYZ", "from": "hr@xyz.com"},
    {"subject": "Discount on your next purchase", "from": "offers@store.com"},
    {"subject": "Important updates on your LinkedIn profile", "from": "jijff@linkedin.com"},
    {"subject": "Connect with professionals in your field", "from": "linkedin@linkedin.com"},
    {"subject": "Exclusive job offer - Apply now!", "from": "jobs@xyzcorporation.com"},
    {"subject": "Reminder: Your free trial is expiring soon", "from": "support@techservices.com"},
    {"subject": "New connection request from John Doe", "from": "linkedin@linkedin.com"},
    {"subject": "Monthly newsletter from XYZ Solutions", "from": "newsletter@xyzsolutions.com"},
    {"subject": "Your LinkedIn profile received a new recommendation", "from": "linkedin@linkedin.com"},
    {"subject": "Event invitation: Tech Conference 2025", "from": "events@grover.com"},
    {"subject": "fsafaf asdasd", "from": "events@techconference.com"},
    {"subject": "new items in stock", "from": "events@grover.com"},
    {"subject": "jobs here", "from": "events@xing.com"},

]

test_new_data(new_emails)
