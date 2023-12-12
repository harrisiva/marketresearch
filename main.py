import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

# Extract the links of different club's smoothcomp page link from the given URL
clubs = []

try:
    print("Scrapping smoothcomp rankings")
    for i in range(0, 3000):
        # Request the landing page from smoothcomp
        page_number = i 
        response = requests.get(f"https://smoothcomp.com/en/club?search=&country=&continent=North%20America&page={page_number}")
        soup = bs(response.text, 'html.parser')
        # Extract the club's links from the current page along (discard all other information as they can be obtained from the next page)
        for item in soup.find_all('a'):
            _class = item.get("class")
            if _class and "color-inherit" in _class: 
                link = item.get('href')
                clubs.append(link)
        i+=1 # Increment the page number to capture a large set of clubs url's
        if i%10==0: print(f"\tScraped {i}th page")
except:
    print(f"Stopped/Crashed at page number:{i}.")

print(f"Acquired smoothcomp profiles of {len(clubs)} academies.")

print("Extracting club info...")
data = []
try:
    # Scrape information about each club from their smoothcomp profile to collect the required attributes information
    for i in range(0, len(clubs)):
        # Initialize dictionary for containing the current rows data (None as default when data not found)
        row = {"Name":None, "Location":None,"Contact Persons":None, "Affiliation":None} 
        # Extract information for the current club and pack into the dictionary if data exists
        response = requests.get(clubs[i])
        soup = bs(response.text, 'html.parser')
        row["Source"] = clubs[i]
        row["Name"] = soup.title.text.replace(" ","").replace("\n","").replace("-Smoothcomp","")
        club_info = [i for i in soup.find_all(id="clubInfo")[0].text.split('\n') if i]
        if "Location" in club_info: row["Location"] = club_info[int(club_info.index("Location")+1)]
        if "Contact Persons" in club_info: row["Contact Persons"] = club_info[int(club_info.index("Contact Persons")+1)]
        if "Affiliation" in club_info: row["Affiliation"] = club_info[int(club_info.index("Affiliation")+1)]
        # Append dictionary into the list of rows to convert into a pandas dataframe to work with
        data.append(row)
        i+=1 # Increment for next club
        if i%10==0:print(f"\ttScraped {i}th club")
except:
    print(f"\ttCompleted scrapping {i} clubs")

df = pd.DataFrame(data)
df.to_csv("ExtractedData.csv", encoding='utf-8', index=False) 
print(f"\n\nSaved csv with data on {len(df)} academies")
