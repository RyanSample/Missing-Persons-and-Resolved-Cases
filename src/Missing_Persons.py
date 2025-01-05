from bs4 import BeautifulSoup
#from bs4 import soupStrainer
from urllib.request import urlopen
import pandas as pd
import re
from tqdm import tqdm
import requests
import time

pathp60s = 'https://charleyproject.org/case-searches/chronological-cases?chronology=Pre-1960s'
path60s = 'https://charleyproject.org/case-searches/chronological-cases?chronology=1960s'
path70s = 'https://charleyproject.org/case-searches/chronological-cases?chronology=1970s'
path80s = 'https://charleyproject.org/case-searches/chronological-cases?chronology=1980s'
path90s = 'https://charleyproject.org/case-searches/chronological-cases?chronology=1990s'
path00s = 'https://charleyproject.org/case-searches/chronological-cases?chronology=2000s'
path10s = 'https://charleyproject.org/case-searches/chronological-cases?chronology=2010s'
path20s = 'https://charleyproject.org/case-searches/chronological-cases?chronology=2020s'

def extract_links(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
##results = soup.find_all('div', attrs={'class':'cases'})

    links = []
    for a_tag in soup.find_all('a'):
        href = a_tag.get('href') 
        if href and "https://charleyproject.org/case/" in href: 
            links.append(href)
    
#if contains 'https://charleyproject.org/case/ return to new df.
##pre_1960s = pd.DataFrame(pre_1960s)
    df = pd.DataFrame(links, columns=['Links:']) 
    df = df.dropna().reset_index(drop=True) 
    return df

pre_1960s = extract_links(pathp60s)
x_1960s = extract_links(path60s)
x_1970s = extract_links(path70s)
x_1980s = extract_links(path80s)
x_1990s = extract_links(path90s)
x_2000s = extract_links(path00s)
x_2010s = extract_links(path10s)
x_2020s = extract_links(path20s)

all_years_data = pd.concat([pre_1960s, x_1960s, x_1970s, x_1980s,
                            x_1990s, x_2000s, x_2010s, x_2020s], ignore_index=True)

print(all_years_data)

# Initialize an empty DataFrame to store all data 
missing_people_df = pd.DataFrame() 
# Iterate over each link in all_years_data 
for i in tqdm(range(all_years_data.shape[0])): 
    link_str = all_years_data.at[i, 'Links:'] 
    attempt_number = 0
    r2 = None
    # try 5 times to get the request
    while attempt_number < 5:
        # try to get the page
        try:
            r2 = requests.get(link_str)
        # if the connection times out then sleep for a bit and try again
        except requests.exceptions.ConnectTimeout:
            
            print(f"Connection timeout #{attempt_number+1}... Sleeping for 30 seconds and trying again")
            # sleep for a bit...
            time.sleep(30)
            attempt_number += 1
            # continue to the next loop iteration and request the page again
            continue
        # the request was successful so no need looping anymore
        break
    # if the request failed after 5 times then continue onto the next missing person link
    if r2 is None:
        continue
    soup2 = BeautifulSoup(r2.text, 'html.parser') 
    # Extract data 
    person = { "Links:": [link_str], 
              "name": [soup2.find('h1').get_text()] 
             } 
    for strong_tag in soup2.find_all('strong'): 
        k = strong_tag.text.strip() 
        v = strong_tag.next_sibling.strip() 
        person[k] = [v] 
        # Convert to DataFrame 
        persondf = pd.DataFrame(person) 
    # Merge with the main DataFrame 
    if not missing_people_df.empty: 
        missing_people_df = pd.concat([missing_people_df, persondf], ignore_index=True) 
    else: 
        missing_people_df = persondf 
# Display the final DataFrame 
print(missing_people_df)

with pd.ExcelWriter('Missing_People.xlsx') as writer:
    all_years_data.to_excel(excel_writer=writer, sheet_name='Links')
    missing_people_df.to_excel(excel_writer=writer, sheet_name='Missing Persons')