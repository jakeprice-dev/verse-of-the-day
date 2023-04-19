"""
Daily Bible Reading Notification
"""

import datetime
import re
import json
import requests
import yaml

# Configuration file:
with open("config.yml", "r", encoding="utf-8") as config:
    # Load config file:
    config_file = yaml.safe_load(config)

# Variables:
esv_api_token = config_file["esv_api_token"]
readings_file = config_file["readings_file"]
gotify_app_token = config_file["gotify_app_token"]
base_url = config_file["gotify_base_url"]

# API Headers:
headers = {
    "Authorization": f"Token {esv_api_token}",
}

# Open readings file:
with open("./year_1.txt", "r", encoding="utf-8") as readings:
    # Loop through each reading:
    for line in readings:
        # Get the current date:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")

        # Find the current date's reading:
        current_reading = re.match(rf"^{current_date}", line)

        if current_reading:
            # Remove the date from the reading so we can look it up:
            reading = line.strip(f"{current_date} ")

            # Provide parameters for the ESV API:
            params = {
                "q": reading,
                "include-first-verse-numbers": "false",
                "include-footnotes": "false",
                "include-headings": "false",
                "include-passage-references": "false",
                "include-short-copyright": "false",
                "include-verse-numbers": "false",
            }

            # Call the API:
            response = requests.get(
                "https://api.esv.org/v3/passage/text/", params=params, headers=headers, timeout=300
            )

            # Store the API response:
            response_data = response.json()

            # Store the full passage reference (John 3:16):
            canonical = response_data["canonical"]
            # Store the passage itself:
            passage = response_data["passages"][0]

            # Gotify API Configuration:
            api_url = f"/message?token={gotify_app_token}"

            # Setup the notification message:
            api_payload = {
                "priority": 4,
                "title": "Daily Bible",
                "message": f"""
### {canonical}

> {passage}

[{canonical}](https://www.esv.org/{reading}) - ESV
""",
                "extras": {
                    "client::display": {"contentType": "text/markdown"},
                },
            }

            # Create the API endpoint:
            api_endpoint = base_url + api_url

            # Post the message to the Gotify API (send the bible reading):
            response = requests.post(
                api_endpoint,
                headers={"Content-Type": "application/json"},
                data=json.dumps(api_payload),
                timeout=300
            )
