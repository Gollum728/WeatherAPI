import datetime
from datetime import time, timedelta
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

email = ""

def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "calendar-credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
    print(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)
    calendar = service.calendarList().list().execute()
    email = calendar["items"][0]["id"]
    tomorrow = datetime.datetime.now() + timedelta(days=1)

    startOfDay = datetime.datetime.combine(
      tomorrow.date(),
      time.min,
      datetime.timezone.utc
    ).isoformat()

    endOfDay = datetime.datetime.combine(
      tomorrow.date(),
      time.max,
      datetime.timezone.utc
    ).isoformat()


    print(startOfDay)
    print(endOfDay)
    events = (
      service.events()
      .list(
        calendarId = "primary", #Gets the primary user's calendar
        timeMin = startOfDay, #The earliest time to look for events
        timeMax = endOfDay, #The latest time to look for events
        singleEvents = True, #Only gets 1 event of that type if there are multiple
        orderBy = "startTime",
      )
      .execute()
    )

    events = events.get("items", [])
    eventsHolder = []
    returnDict = {}
    returnDict["Email"] = email
    if not events:
      returnDict["Events"] = "No upcoming events"
    else:
      for event in events:
        startTime = datetime.datetime.fromisoformat(event["start"]["dateTime"])
        endTime = datetime.datetime.fromisoformat(event["end"]["dateTime"])
        print()
        dict = {}
        dict["Title"] = event["summary"]
        dict["Start time"] = datetime.datetime.strftime(startTime, "%H:%M")
        dict["End time"] = datetime.datetime.strftime(endTime, "%H:%M")
        eventsHolder.append(dict)
      returnDict["Events"] = eventsHolder
    print(returnDict)
    return returnDict

    # Call the Calendar API
    """
    now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])
    """

  except HttpError as error:
    print(f"An error occurred: {error}")



if __name__ == "__main__":
  main()