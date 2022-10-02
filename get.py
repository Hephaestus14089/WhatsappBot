from __future__ import print_function
import os.path
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_events(count = 10):
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    elif not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port = 0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        if count < 0:
            return "Invalid input! Enter a positive number"

        service = build('calendar', 'v3', credentials = creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'

        events_result = service.events().list(calendarId='primary', timeMin = now, maxResults = count, singleEvents = True, orderBy = 'startTime').execute()
        events = events_result.get('items', [])

        result = ""

        if not events:
            return "No upcoming events found."

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))

            date = start[0:10]
            time = start[11:19]

            date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')
            time = datetime.datetime.strptime(time, '%H:%M:%S').strftime('%I:%M %p')

            result += f"{date} {time} {event['summary']}\n"

        return result

    except HttpError as error:
        print('An error occured: %s' %(error))
        return "Couldn't list event :("


if __name__ == '__main__':
    events = get_events(2)
    events = events[0:len(events) - 1]
    print(events)
