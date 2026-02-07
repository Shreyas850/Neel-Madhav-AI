import os.path
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# SCOPES = What Diya is allowed to do
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/gmail.readonly']

creds = None

def authenticate_google():
    """Handles Google Login (Opens Browser Once)"""
    global creds
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                return False # Keys missing
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the login for next time
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return True

def get_calendar_events():
    """Reads next 5 events"""
    if not authenticate_google(): return "I need your 'credentials.json' file to access Google."
    
    service = build('calendar', 'v3', credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=5, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events: return "No upcoming events found."
    
    reply = "Here is your schedule: "
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        # Clean up time format
        time_str = start.split('T')[1].split('+')[0][:5] if 'T' in start else "All Day"
        reply += f"{event['summary']} at {time_str}. "
    return reply

def get_unread_emails():
    """Reads top 3 unread emails"""
    if not authenticate_google(): return "Please add 'credentials.json' to enable Email."
    
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD'], maxResults=3).execute()
    messages = results.get('messages', [])

    if not messages: return "You have no new emails."

    reply = "You have new emails from: "
    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = txt['payload']['headers']
        sender = [h['value'] for h in headers if h['name'] == 'From'][0]
        subject = [h['value'] for h in headers if h['name'] == 'Subject'][0]
        
        # Simplify sender name
        if "<" in sender: sender = sender.split("<")[0].strip().replace('"', '')
        reply += f"{sender} about '{subject}'. "
        
    return reply