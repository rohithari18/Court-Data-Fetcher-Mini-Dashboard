from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
def fetch_case_data(case_type,case_no,year):
   options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    url = "https://delhihighcourt.nic.in/case.asp"
    driver.get(url)
    driver.find_element("name", "ctype").send_keys(case_type)
    driver.find_element("name", "cno").send_keys(case_no)
    driver.find_element("name", "cyear").send_keys(year)
    driver.find_element("name", "submit").click()

    time.sleep(2)  

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    parties = soup.find("div", {"id": "parties"}).text.strip()
    hearing = soup.find("div", {"id": "next_hearing"}).text.strip()
    order_link = soup.find("a", text="Latest Order")["href"]

    driver.quit()

    return {
        "parties": parties,
        "next_hearing": hearing,
        "order_pdf": order_link
    }, html
  
