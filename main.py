import sys
import threading
import datetime
import requests
import random
import string
from bs4 import BeautifulSoup

def get_random_string(length):
  letters = string.ascii_lowercase + string.digits
  result_str = ''.join(random.choice(letters) for i in range(length))  
  return result_str

def checkSite():
  while True:
    r = get_random_string(5)
    w = "http://pastelink.net/" + r

    try:
      response = requests.get(w)
    except:
      continue

    if(response.url != "https://pastelink.net/404"):
      scrapeContent(response.text)

def scrapeContent(html):
  global links_found
  soup = BeautifulSoup(html, "html.parser")

  content = soup.find(id="body-display")

  if(content == None):
    return

  links = content.find_all("a")

  for link in links:
    url = link["href"]
    if(url[8:15] == "mega.nz"):
      writeToFile(url)
      links_found+=1

def writeToFile(content):
  global file_name
  f = open("results/" + file_name + ".html", "a")
  text = "<a href=" + content + ">" + content + "</a><br>"
  f.write(text + "\n")
  f.close()

#############################################################################

file_name = datetime.datetime.now().strftime("%X")
file_name = file_name.replace(":", "-")

links_found = 0

if __name__ == '__main__':
  
  for i in range(0, 95):
    t = threading.Thread(target = checkSite)
    t.start()

  while True:
    sys.stdout.write("\rMega Links found: " + str(links_found))
    links_found2 = links_found
