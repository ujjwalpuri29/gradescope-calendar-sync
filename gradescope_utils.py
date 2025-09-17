import os
import requests
import random
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

GRADESCOPE_EMAIL = os.getenv("GRADESCOPE_EMAIL")
GRADESCOPE_PASSWORD = os.getenv("GRADESCOPE_PASSWORD")
GRADESCOPE_COURSE_URL = os.getenv("GRADESCOPE_COURSE_URL")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}

session = requests.Session()
session.headers.update(HEADERS)

def human_delay(min_s=5, max_s=6):
    """Random short sleep to mimic human interaction."""
    time.sleep(random.uniform(min_s, max_s))

def gs_login():
    login_url = "https://www.gradescope.com/login"
    r = session.get(login_url)
    
    soup = BeautifulSoup(r.text, "html.parser")
    token = soup.find("input", {"name": "authenticity_token"})["value"]
    
    payload = {
        "session[email]": GRADESCOPE_EMAIL,
        "session[password]": GRADESCOPE_PASSWORD,
        "authenticity_token": token
    }
    session.post(login_url, data=payload)
    human_delay()

def get_assignments():
    r = session.get(GRADESCOPE_COURSE_URL)
    human_delay()
    soup = BeautifulSoup(r.text, "html.parser")
    
    # with open("page.html", "w", encoding="utf-8") as file:
    #    file.write(str(soup))
    
    num = 0
    assignments = []
    for row in soup.select("td.hidden-column"):
        title = f"Assignment {num // 2 + 1}"
        due = row.get_text(strip=True)
        assignments.append({"title": title, "due": due})
        num += 1

    return(assignments[1::2])