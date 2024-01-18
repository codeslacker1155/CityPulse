import requests
from bs4 import BeautifulSoup
import random
import re
import csv

# List of common email, phone, website, and user agent strings

API_KEY = "AIzaSyAcF8ERLF8k-AFsW3X2txaRE5-rh6bGmhc"
EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
EMAIL_LIST = ["@gmail.com", "@yahoo.com", "@icloud.com", "@protonmail.com"] #add more email providers
PHONE_REGEX = [r"^[1-9]\d{2}-\d{3}-\d{4}", r"^\(\d{3}\)\s\d{3}-\d{4}", r"^[1-9]\d{2}\s\d{3}\s\d{4}", r"^[1-9]\d{2}\.\d{3}\.\d{4}"]
SITE_LIST = ["facebook.com", "linkedin.com", "twitter.com", "instagram.com"]
USER_AGENT_SCRAPER_BASE_URL = 'http://www.useragentstring.com/pages/useragentstring.php?name='
POPULAR_BROWSERS = ['Chrome', 'Firefox', 'Mozilla', 'Safari', 'Opera', 'Opera Mini', 'Edge', 'Internet Explorer']
SEARCH_LIST = [] #add more search terms
NAME_REGEX = [r"^[A-Z][a-z]+, [A-Z][a-z]+", r"^[A-Z][a-z]+ [A-Z][a-z]+", r"^[A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+", r"^[A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+"]
NAME_LIST = [] #add more names
LOCATION_REGEX = [r"^[A-Z][a-z]+, [A-Z][a-z]+, [0-9]{5}", r"^[A-Z][a-z]+, [A-Z][a-z]+, [A-Z][a-z]+, [0-9]{5}"]
LOCATION_LIST = [] #add more locations


email_patterns = re.compile(EMAIL_REGEX)
phone_patterns = [re.compile(pattern) for pattern in PHONE_REGEX]
name_patterns = [re.compile(pattern) for pattern in NAME_REGEX]

def get_user_agent_strings_for_this_browser(browser):
    """
    Get the latest User-Agent strings of the given Browser
    :param browser: string of given Browser
    :return: list of User agents of the given Browser
    """

    url = USER_AGENT_SCRAPER_BASE_URL + browser
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    user_agent_links = soup.find('div', {'id': 'liste'}).findAll('a')[:20]

    return [str(user_agent.text) for user_agent in user_agent_links]


def get_user_agents():
    """
    Gather a list of some active User-Agent strings from
    http://www.useragentstring.com of some of the Popular Browsers
    :return: list of User-Agent strings
    """

    user_agents = []
    for browser in POPULAR_BROWSERS:
        user_agents.extend(get_user_agent_strings_for_this_browser(browser))
    return user_agents[3:] # Remove the first 3 Google Header texts from Chrome's user agents

proxy_user_agents = get_user_agents()
# To randomly select an User-Agent from the collected user-agent strings
random_user_agent = random.choice(proxy_user_agents)

# Print the menu for email
print("\nSelect an email to search for: ")
print("\n1. Gmail")
print("\n2. Yahoo")
print("\n3. iCloud")
print("\n4. ProtonMail")
email = input("\nSelect an email to search for: (1-4) ")
if email == "1":
    email = EMAIL_LIST[0]
elif email == "2":
    email = EMAIL_LIST[1]
elif email == "3":
    email = EMAIL_LIST[2]
elif email == "4":
    email = EMAIL_LIST[3]
#ask for input of search terms and location to search for and append constants
search = input("Enter a search term: (Ex. 'Realtor') ")
search = "inanchor:" + search
#search.append(SEARCH_LIST)
#ask for input of location to search for and append constants
location = input("Enter a location to search for: [City, State (Ex. 'SC'), ZIP (Optional)] ")
#if location is in correct format add to list
#if location in LOCATION_REGEX:
#    LOCATION_REGEX.append(LOCATION_LIST)
# Print menu of possible sites to search
# Print the menu
print("\nSelect a site to search: ")
print("\n1. Facebook")
print("\n2. LinkedIn")
print("\n3. Twitter")
print("\n4. Instagram")
site = input("\nSelect a site to search: (1-4) ")
if site == "1":
    site = SITE_LIST[0]
    site = "site:" + site
elif site == "2":
    site = SITE_LIST[1]
    site = "site:" + site
elif site == "3":
    site = SITE_LIST[2]
    site = "site:" + site
elif site == "4":
    site = SITE_LIST[3]
    site = "site:" + site

#use google search api to search for email, phone, name, and website
#use regex to find email, phone, name, and website
    

def google_search(query, API_KEY, CUSTOM_SEARCH_ENGINE_ID):
    # will use random user agent from the list
    headers = {'User-Agent': random_user_agent}
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url, headers=headers)
    #make the soup object global
    global soup
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for g in soup.find_all('div', class_='r'):
        text = g.get_text()
        email = [email for pattern in email_patterns for email in pattern.findall(text)]
        phone = [phone for pattern in phone_patterns for phone in pattern.findall(text)]
        name = [name for pattern in name_patterns for name in pattern.findall(text)]
        link = g.find('a')['href']
        results.append({'Name': name, 'Email': email, 'Phone': phone, 'Link': link})

    print(results)
    return results
    
    # Find the name, phone number, email, and grab link to website
    # Find this information in the search results or description
    # Use a for loop to iterate through the results of soup and grab the email from the title or description (use regex)
    # regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+{}')
    # #regex + email domain
    # e_mail = regex + email
    # # find email in soup object using regex
    # x = re.findall(e_mail, str(soup))
    # print(x)
    # y = re.findall("Realtor", str(soup))
    # print(y)
        # if statement to check if the name is in the title
        # if it is, append to name list
        # if statement to check if the email is in the title
        # if it is, append to email list
        # if statement to check if the phone number is in the title
        # if it is, append to phone list
        # if statement to check if the website is in the title
        # if it is, append to website list

    # Use a for loop to iterate through the results of soup and grab the phone number from the title or description
    # Use a for loop to iterate through the results of soup and grab the website/url
    # Use a for loop to iterate through the results of soup and grab the name from the title or description
    
    for g in soup.find_all('div', class_='r'):
        # declare name, email, phone, and website to their own lists
        name=[""]
        email=[""]
        phone=[""]
        website=[""]
        # if statement to check if the name is in the title
        # if it is, append to name list
        # if statement to check if the email is in the title
        # if it is, append to email list
        # if statement to check if the phone number is in the title
        # if it is, append to phone list
        # if statement to check if the website is in the title
        # if it is, append to website list

def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))

# Output the results to a csv file
# Use the csv module to write to a file
def write_to_csv():
    with open('results.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Name', 'Email', 'Phone', 'Website'])
        # Use placeholder values for writing the csv file
        for i in range (0, 50):
            csvwriter.writerow(['&', '&', '&', '&'])

# Run the program declare main function
if __name__ == '__main__':
    search_query = email + " " + search + " near " + location + " " + site
    google_search(search_query)
    prGreen("\n\n[Done]\n")
    print(f"\nUser-Agent: {random_user_agent}")
    print(f"\nGoogle Search: {search_query}")
#print results of search out of results in google_search function

# We want to extract the name, email, phone number from the title or the description
# We want to grab the link to the website
#then we want to write the results to a csv file
