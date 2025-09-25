import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

SCAQMD_URL = "https://www.aqmd.gov/home/rules-compliance/rules/scaqmd-rule-book/regulation-xi"

response = requests.get(SCAQMD_URL)
response.encoding = "utf-8"
content = response.text

soup = BeautifulSoup(content, "html.parser")

# Find the table element
table = soup.find("table")
# print(table)

def clean_status(status):
    """Parse amended/adopted/etc string and return status and date object."""
    try:
        stat, date = status.split(" ", maxsplit=1)
        status_str = stat.removeprefix("(").strip()
        date_str = date.removesuffix(")").strip()
        date = datetime.strptime(date_str, '%B %d, %Y')
        print(f"Status: {status_str}")
        print(f"Date: {date}")
        return {
            'status': status_str,
            'date': date.date()
        }
    except ValueError as e:
        print(f"Error: {e}")
        print(f"Value: {status}")
        return {
            'status': None,
            'date': None
        }

def a_tag_w_title(tag):
    try:
        return tag.hasattr('href') and tag.hasattr('title')
    except TypeError as e:
        print(f"Error: {e}")
        print(f"Tag: {tag}")

# Extract headers and rows
headers = [th.text.strip() for th in table.find_all("th")]
rows_data = []
for row in table.find_all("tr"):
    rule = None
    link = None
    links = row.find_all("a")
    if links:
        for i in links:
            if a_tag_w_title(i):
                link = i.get("href").strip()
                rule = i.text.strip()
            else:
                continue
        name = row.find("strong").text.strip()
        status = row.find("em").text.strip()
        # print(f"Rule: {rule}")
        cleaned = clean_status(status)
        rows_data.append({
            'rule': rule,
            'name': name,
            'status': cleaned['status'],
            'date': cleaned['date'],
            'link': link
        })
    else:
        print(f"Links: {links}")

# print(headers)
# print(rows_data[:3])
# for i in rows_data[:3]:
#     stat = i['status']
#     clean_status(stat)




