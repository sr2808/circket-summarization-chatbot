import requests
from bs4 import BeautifulSoup
from datetime import datetime

def format_iso_datetime(date_str):
    try:
        # Convert ISO string to datetime object
        date_obj = datetime.fromisoformat(date_str)
        # Format it into a readable string
        return date_obj.strftime("%d %B %Y, %I:%M %p")
    except ValueError:
        return "Invalid Date Format"
    
def scrape_upcoming_matches(url):
    
    upcomingMatches = []
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all upcoming matches
    upcomingMatchesContent = soup.find_all("div", class_="sp-scr_wrp vevent")

    if not upcomingMatchesContent:
        print("No upcoming matches found.")
        return

    for match in upcomingMatchesContent:
        # Extracting attributes
        description = match.find("span", class_="description")
        teams = match.find("span", class_="summary")
        dtstart = match.find("span", class_="dtstart")
        dtend = match.find("span", class_="dtend")
        location = match.find("span", class_="location")

        # Get text safely
        match_data = {
            "description": description.text.strip() if description else "N/A",
            "teams": teams.text.strip() if teams else "N/A",
            "dtstart": format_iso_datetime(dtstart.text.strip()) if dtstart else "N/A",
            "dtend": format_iso_datetime(dtend.text.strip()) if dtend else "N/A",
            "location": location.text.strip() if location else "N/A",
            "status": "upcoming"
        }

        upcomingMatches.append(match_data)
    return upcomingMatches