import os
import shutil
from upcomingMatches import scrape_upcoming_matches
from recentMatches import scrape_recent_matches

# URLs for scraping
upcomingMatchesUrl = "https://sports.ndtv.com/cricket/schedules-fixtures"
recentMatchesUrl = "https://sports.ndtv.com/cricket/results"

# Scraping the data
upcomingMatches = scrape_upcoming_matches(upcomingMatchesUrl)
recentMatches = scrape_recent_matches(recentMatchesUrl)

# Folder path
data_folder = "data"

# # Function to delete all files in the 'data' folder
# def clear_data_folder(folder):
#     if os.path.exists(folder):
#         shutil.rmtree(folder)  # Remove the entire folder
#     os.makedirs(folder, exist_ok=True)  # Recreate the folder

# # Clear the data folder before writing new files
# clear_data_folder(data_folder)

# File paths
upcoming_matches_file = os.path.join(data_folder, "upcoming_matches.txt")
recent_matches_file = os.path.join(data_folder, "recent_matches.txt")

# Function to write match data to a text file
def write_matches_to_txt(filename, matches, match_type):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{match_type} Matches:\n")
        f.write("=" * 40 + "\n\n")
        
        for match in matches:
            for key, value in match.items():
                if isinstance(value, list):  # Handling lists like team scores
                    f.write(f"{key.capitalize()}:\n")
                    for item in value:
                        if isinstance(item, dict):
                            for sub_key, sub_value in item.items():
                                f.write(f"  {sub_key.capitalize()}: {sub_value}\n")
                        else:
                            f.write(f"  {item}\n")
                else:
                    f.write(f"{key.capitalize()}: {value}\n")
            f.write("-" * 40 + "\n\n")

# Writing the data to text files
write_matches_to_txt(upcoming_matches_file, upcomingMatches, "Upcoming")
write_matches_to_txt(recent_matches_file, recentMatches, "Recent")

# print(f"Deleted old files and saved new data to {data_folder}/")
print(f"Upcoming matches saved to {upcoming_matches_file}")
print(f"Recent matches saved to {recent_matches_file}")