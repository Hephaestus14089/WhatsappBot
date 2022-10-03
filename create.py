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

def put_event(event_details, event_schedule):
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


def create_event(event_name, start_date, start_time, end_date, end_time):

    event_details = {
        'name': "",
        'location': "",
        'timezone': "Asia/Kolkata",
        'recurrence': "RRULE:FREQ=DAILY, COUNT=1"
    }
    event_details['name'] = event_name

    event_schedule = Event_Schedule()
    event_schedule.quick_input(start_date, end_date, start_time, end_time)

    return put_event(event_details, event_schedule)


if __name__ == '__main__':
    # create_event()
    pass
