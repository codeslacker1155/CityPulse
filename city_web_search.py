from googlesearch import search
import pandas as pd
import re
from datetime import datetime
import requests
from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup
import time
import re
from requests_html import HTMLSession
from bs4 import BeautifulSoup, SoupStrainer


def extract_emails_from_url(url, base_url):
    try:
        response = requests.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        return set()

    # Use SoupStrainer to parse only specific elements (e.g., 'a', 'p', 'div')
    parse_only = SoupStrainer(["a", "p", "div"])
    soup = BeautifulSoup(response.text, "html.parser", parse_only=parse_only)

    emails = set()

    # Extract emails from 'a' tags
    for anchor in soup.find_all("a", href=True):
        link = anchor["href"]

        # Handle relative URLs by joining with the base URL
        full_link = urljoin(base_url, link)

        new_emails = set(
            re.findall(
                r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", full_link, re.I
            )
        )
        emails.update(new_emails)

    # Extract emails from text content within 'p' and 'div' tags
    for tag in soup.find_all(["p", "div"]):
        text_content = tag.get_text()
        text_emails = set(
            re.findall(
                r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text_content, re.I
            )
        )
        emails.update(text_emails)

    EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""

    # initiate an HTTP session
    session = HTMLSession()

    try:
        # get the HTTP Response
        r = session.get(url)
        # for JavaScript-driven websites
        r.html.render()
        for re_match in re.finditer(EMAIL_REGEX, r.html.raw_html.decode()):
            httpemail = re_match.group()
            emails.add(httpemail)
    except Exception as e:
        print(f"Error fetching {url}: {e}")

    return emails


# Read search queries from a text file
with open("cities.txt", "r") as file:
    search_queries = file.read().splitlines()

all_emails = set()

region = "North Carolina"

# Iterate through each search query
for search_query in search_queries:
    print(f"Performing Google search for: {search_query} in {region}")

    # Perform Google search and get the first 5 results
    results = search(f"{search_query} enter your text here......", start=0, stop=2)

    # Extract emails from the first few websites in the search results
    for result in results:
        # Extract the base URL from the result
        base_url = "{0.scheme}://{0.netloc}".format(urlsplit(result))
        print(base_url)
        new_emails = extract_emails_from_url(result, base_url)

        # Check if any part of search_query is present in any email address
        if any(search_query.lower() in email.lower() for email in new_emails):
            all_emails.update(new_emails)

        # Append the new emails to the CSV file
        current_df = pd.DataFrame(new_emails, columns=["Email"])
        with open("NEWEmailOutput.csv", mode="a", encoding="utf-8", newline="") as f:
            current_df.to_csv(f, header=False, index=False, mode="a")

        # Add a timer to avoid being blocked by Google (adjust sleep time as needed)
        time.sleep(1)

print("================================================\n")
print(
    "Your data has been processed successfully!! Please check the output in the below file:"
)
print("NEWEmailOutput.csv\n")
print("================================================\n")
