# Weather-Based Outfit Recommendation System

A Python-based outfit recommendation system that combines weather data, Google Calendar events, a personal wardrobe, and an LLM to recommend suitable outfits for the day. The system retrieves the day's weather and calendar events, considers the clothing available in the user's wardrobe, and generates a personalised outfit recommendation based on the user's schedule and expected conditions.

## Features

- Retrieves current and forecasted weather information
- Retrieves the user's Google Calendar events to understand upcoming plans
- Recommends outfits based on weather conditions and planned activities
- Restricts recommendations to clothing items that actually exist in the user's wardrobe
- Uses an LLM to combine weather, calendar, and wardrobe data into a personalised recommendation
- Generates an image representing the recommended outfit
- Sends the recommended outfit to the user by email
- Supports multiple outfit recommendations when needed, such as an additional outfit for later in the day
- Can run automatically via a scheduled task

## How it works

1. Weather retrieval — current and forecasted weather is retrieved from the weather API for the user's location.
2. Calendar retrieval — the Google Calendar API retrieves the user's events for the following day.
3. Wardrobe data — clothing items available in the user's wardrobe are provided to the LLM.
4. Recommendation generation — weather, calendar, and wardrobe data are combined into a structured prompt; the LLM generates a recommendation constrained to clothing that actually exists in the wardrobe.
5. Outfit generation — the recommendation is used to generate an image of the selected outfit.
6. Email delivery — the outfit image is sent to the user by email.

## Known Limitations

- The recommendation isn't always generated due to high traffic for Gemini
- The image model sometimes hallucinates and gives a bad outfit picture. It sometimes:
    - Returns the same reference image of the user wearing the same clothes in that image
    - Returns the outfit on the user but in a strange fitting, usually tucked in
    - Gets the right clothing but cuts off the length of the clothing (e.g. shirts become short-sleeved and trousers become shorts)
- Struggles with rendering outerwear along with the base outfit
- Location and time are dependant on the devices location so it doesn't work cleanly 
- Recommendations depend on the accuracy and completeness of the wardrobe information provided
- Weather recommendations depend on the availability and accuracy of the external weather API
- Email delivery and other parts of the workflow depend on external services being available

## Tech stack

Python, Google Calendar API, OpenWeatherMap API, LLM API, Google OAuth 2.0, SMTP/Gmail, python-dotenv

## Project structure

project/
├── main.py
├── wardrobe/
├── recordings/
├── static/
├── templates/
├── calendar/
├── .env
├── requirements.txt
└── README.md

The exact project structure may vary depending on the local version of the project.

## Setup

1. Clone the repository:
git clone https://github.com/Gollum728/WeatherAPI.git
cd WeatherAPI

2. Create and activate a virtual environment:
python -m venv venv

Windows: venv\Scripts\activate
macOS/Linux: source venv/bin/activate

3. Install dependencies:
pip install -r requirements.txt

4. Configure environment variables — create a .env file in the project root. The project uses environment variables for sensitive credentials such as API keys and email credentials. Example:

WEATHER_API_KEY=your_weather_api_key
EMAIL_APP_KEY=your_gmail_app_password

Do not commit the .env file to GitHub. Add it to .gitignore:

.env
token.json
calendar-credentials.json

5. Configure Google Calendar — a Google Cloud project must be configured with the Google Calendar API enabled and OAuth credentials created for the application. Place the OAuth client credentials in calendar-credentials.json. When the application is run for the first time, Google authentication is required. After authentication, a token.json file is generated and used for subsequent requests. The OAuth token provides the application with read-only access to the user's Google Calendar.

## Running locally

Once the dependencies and API credentials have been configured, run the application using:

python main.py

The application can then be accessed through the local Flask server. If Google Calendar authentication is required, the application will open the Google authentication flow. After authentication, the generated credentials are stored locally in token.json, so the application can retrieve calendar events without requiring authentication every time it runs.

## Email configuration

The system sends recommended outfits using Gmail's SMTP server. A Gmail App Password is used instead of the user's normal Gmail password. The email functionality uses smtp.gmail.com with an SSL connection. The application attaches the generated outfit image to the email before sending it. The email contains different messages depending on whether one or multiple outfits have been recommended.

## Google Calendar authentication

The application uses OAuth 2.0 with the following Calendar scope:

https://www.googleapis.com/auth/calendar.readonly

This allows the application to read calendar events without being able to modify them. The application stores the resulting access and refresh tokens in token.json so that authentication does not normally need to be repeated.

## Automated execution

The system is designed to be capable of running automatically rather than requiring the user to manually start the program each day. A scheduled execution can run the workflow once per day: retrieve weather, retrieve calendar events, generate outfit recommendation, generate outfit image, send email. This allows the system to provide the user with a daily outfit recommendation without requiring manual interaction.

## Security

Sensitive credentials should not be committed to the repository. The following files should remain private:

.env
token.json
calendar-credentials.json

API keys, OAuth credentials, and email app passwords should be stored using environment variables or other secure credential storage rather than being hard-coded into the source code.
