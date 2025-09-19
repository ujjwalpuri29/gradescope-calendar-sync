import os
import requests
import random
import time
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

GRADESCOPE_EMAIL = os.getenv("GRADESCOPE_EMAIL")
GRADESCOPE_PASSWORD = os.getenv("GRADESCOPE_PASSWORD")
GRADESCOPE_COURSE_URL = os.getenv("GRADESCOPE_COURSE_URL")
COURSE_ID = os.getenv("COURSE_ID")

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
    
    if "You must be logged in" in r.text:
        gs_login()
        r = session.get(GRADESCOPE_COURSE_URL)
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # with open("page.html", "w", encoding="utf-8") as file:
    #    file.write(str(soup))

    # with open("page.html") as fp:
    #    soup = BeautifulSoup(fp, 'html.parser')
        
    assignments = []
    assignment_table = soup.find("tbody")
    
    for row in assignment_table.select("tr"):
        title_ele = row.select_one("a")
        if not title_ele:
            title_ele = row.select_one("button")
        title = f"{COURSE_ID}: {title_ele.get_text().strip()}"
        
        due = row.select_one(".submissionTimeChart--dueDate").get('datetime')
        dt = datetime.strptime(due, "%Y-%m-%d %H:%M:%S %z")
        
        assignments.append({"title": title, "due": dt.isoformat()})
        
    return(assignments)