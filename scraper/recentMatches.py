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


def scrape_recent_matches(url):
    recentMatches = []
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    # Find all recent matches
    recentMatchContent = soup.find_all("div", class_="sp-scr_wrp vevent")

    if not recentMatchContent:
        print("No recent matches found.")
        return []

    for match in recentMatchContent:
        # Extracting attributes
        description = match.find("span", class_="description")
        teams = match.find("span", class_="summary")
        dtstart = match.find("span", class_="dtstart")
        dtend = match.find("span", class_="dtend")
        location = match.find("span", class_="location")
        title = ""

        # Extract match result from "sp-scr_lnk url" → "scr_inf-wrp" → "scr_dt-red"
        match_result = match.find("a", class_="sp-scr_lnk url")
        title = match_result.find("div", class_="scr_txt-ony")
        if match_result:
            match_result = match_result.find_all("div", class_="scr_inf-wrp")[-1]
            if match_result:
                match_result = match_result.find("div", class_="scr_dt-red")
                # print(match_result.prettify())
                # print("-----------------------")
        
        # Extract team names and scores
        teams_scores = []
        team_wrappers = match.find_all("div", class_="scr_tm-wrp")

        for team in team_wrappers:
            team_name = team.find("div", class_="scr_tm-nm")
            team_score = team.find("span", class_="scr_tm-run")

            teams_scores.append({
                "team": team_name.text.strip() if team_name else "N/A",
                "score": team_score.text.strip() if team_score else "N/A",
            })

        # Get text safely
        match_data = {
            "description": description.text.strip() if description else "N/A",
            "teams": teams.text.strip() if teams else "N/A",
            "title": title.text.strip() if title else "N/A",
            "dtstart": format_iso_datetime(dtstart.text.strip()) if dtstart else "N/A",
            "dtend": format_iso_datetime(dtend.text.strip()) if dtend else "N/A",
            "location": location.text.strip() if location else "N/A",
            "status": "completed",
            "teams_scores": teams_scores,
            "match_result": match_result.text.strip() if match_result else "N/A",
        }

        recentMatches.append(match_data)

    return recentMatches
