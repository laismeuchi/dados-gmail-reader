import azure.functions as func
import logging
import os
import base64
import google.auth
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Azure Blob Storage settings
STORAGE_CONNECTION_STRING = os.getenv('STORAGE_CONNECTION_STRING')
CREDENTIALS = os.getenv('CREDENTIALS')
CONTAINER_NAME = 'attachments'
FOLDER_PATH = 'shealth/'

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Function to authenticate with Gmail API
def authenticate_gmail():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']

    creds = None
    token_path = 'token.json'

    # Check if the token file exists
    if os.path.exists(token_path):
        creds = google.oauth2.credentials.Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            # Use the run_local_server method instead of run_console
            #flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=49919)
        
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds

# Function to get Samsung Health email
def get_samsung_health_email(service):
    try:
        # Query for the email with specific subject and sender
        results = service.users().messages().list(
            userId='me',
            q="from:laismeuchi@gmail.com subject:'Samsung Health'"
        ).execute()

        messages = results.get('messages', [])
        if messages:
            logging.info("Email found.")
            # Get the first email
            email_id = messages[0]['id']
            message = service.users().messages().get(userId='me', id=email_id).execute()
            return message
        else:
            logging.info("No emails found.")
            return None
    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        return None

# Function to save attachment to Azure Blob Storage
def save_attachment_to_blob(filename, content):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=FOLDER_PATH + filename)
        blob_client.upload_blob(content, overwrite=True)
        logging.info(f"Attachment {filename} uploaded to Azure Storage.")
    except Exception as e:
        logging.error(f"Error saving to blob: {str(e)}")

# Function to process email and extract attachments
def process_email_with_attachments(service, message):
    try:
        parts = message.get('payload').get('parts', [])
        for part in parts:
            if part['filename']:
                if 'data' in part['body']:
                    # Attachment is small and encoded in 'data'
                    attachment_data = part['body']['data']
                else:
                    # Attachment is large and needs to be retrieved
                    att_id = part['body']['attachmentId']
                    attachment = service.users().messages().attachments().get(
                        userId='me', messageId=message['id'], id=att_id
                    ).execute()
                    attachment_data = attachment['data']

                file_data = base64.urlsafe_b64decode(attachment_data.encode('UTF-8'))
                filename = part['filename']
                save_attachment_to_blob(filename, file_data)
    except HttpError as error:
        logging.error(f"An error occurred when processing attachments: {error}")


@app.route(route="http_trigger")
def read_email(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Gmail Monitoring Function triggered')

    # Step 1: Authenticate and build the Gmail API service
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)

    # Step 2: Fetch the Samsung Health email
    message = get_samsung_health_email(service)

    if message:
        # Step 3: Process the email and save attachments
        process_email_with_attachments(service, message)
    else:
        logging.info("No matching Samsung Health emails found.")

    return func.HttpResponse("Email processed.", status_code=200)