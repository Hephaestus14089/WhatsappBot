from __future__ import print_function
import os.path
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

class Schedule:
    def __init__(self):
        self.date = None
        self.time = None

class Event_Schedule:
    def __init__(self):
        self.start = Schedule()
        self.end = Schedule()

    def date_format(self, date):
        return datetime.datetime.strptime(date, '%d-%b-%y').strftime('%y-%m-%d')

    def time_format(self, time):
        return datetime.datetime.strptime(time, '%I:%M%p').strftime('%H:%M:' + '00')

    def quick_input(self, start_date, end_date, start_time, end_time):
        self.start.date = self.date_format(start_date)
        self.end.date = self.date_format(end_date)
        self.start.time = self.time_format(start_time)
        self.end.time = self.time_format(end_time)

def create_event(event_details, event_schedule):
    event = {
        'summary': event_details['name'],
        'location': event_details['location'],
        'start': {
            'dateTime': f'{event_schedule.start.date}T{event_schedule.start.time}',
            'timeZone': event_details['timezone'],
        },
        'end': {
            'dateTime': f'{event_schedule.end.date}T{event_schedule.end.time}',
            'timeZone': event_details['timezone'],
        },
        'recurrence': event_details['recurrence'],
        'remainders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 10}
            ]
        }
    }


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
        service = build('calendar', 'v3', credentials = creds)
        events = service.events().insert(calendarId='primary', body = event).execute()
        print('Event created: %s' %(events.get('htmlLink')))
        return "Congratulations! Event created successfully"

    except HttpError as error:
        print('An error occured: %s' %(error))
        return "Couldn't create event :("


if __name__ == '__main__':
    dummy_data = {
        'start_date': "16-Oct-22",
        'end_date': "16-Oct-22",
        'start_time': "09:30AM",
        'end_time': "05:00PM"
    }

    event_details = {
        'name': "Blood Donation",
        'location': "Telinipara, Baburbajar-Barowaritala, Town Library Hall",
        'timezone': "Asia/Kolkata",
        'recurrence': "RRULE:FREQ=DAILY, COUNT=1"
    }

    event_schedule = Event_Schedule()
    event_schedule.quick_input(dummy_data['start_date'], dummy_data['end_date'], dummy_data['start_time'], dummy_data['end_time'])

    create_event(event_details, event_schedule)
