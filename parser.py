import requests
from bs4 import BeautifulSoup
startingPage = input("What page would you like to start at?\n")
requestType = input("What type of query would you like to do?\n1: Find all links in a page\n2: Link stream\n")
pagesToVisit = []
pageIndices = []
visitedPages = []
currentLinks = []
pagesToVisit.append(startingPage)
pageIndices.append(0)
if (requestType == "1"):
  while (len(pagesToVisit) != 0 and pageIndices[0] < 2):
    if (pagesToVisit[0] in visitedPages):
      pagesToVisit.pop(0)
      pageIndices.pop(0)
      continue
    visitedPages.append(pagesToVisit[0])
    if pageIndices[0] < 1:
      r = requests.get(f"https://en.wikipedia.org/wiki/{pagesToVisit[0]}")
      pagesToVisit.pop(0)
      soup = BeautifulSoup(r.content, 'html.parser')
      currentLinks = soup.find('div', attrs = {'id':'bodyContent'}).find_all('a', href=True)
      for link in currentLinks:
        if (link['href'][:6] == "/wiki/" and not "/" in link['href'][6:] and not ":" in link['href']):
          pagesToVisit.append(link['href'][6:])
          pageIndices.append(pageIndices[0] + 1)
    else:
      pagesToVisit.pop(0)
    pageIndices.pop(0)
else:
  while (pageIndices[0] < 500):
    visitedPages.append(pagesToVisit[0])
    r = requests.get(f"https://en.wikipedia.org/wiki/{pagesToVisit[0]}")
    pagesToVisit.pop(0)
    soup = BeautifulSoup(r.content, 'html.parser')
    currentLinks = soup.find('div', attrs = {'id':'bodyContent'}).find_all('a', href=True)
    currentLink = currentLinks[0]['href']
    while (currentLink[6:] in visitedPages or currentLink[:6] != "/wiki/" or "/" in currentLink[6:] or ":" in currentLink):
      currentLinks.pop(0)
      currentLink = currentLinks[0]['href']
    pagesToVisit.append(currentLink[6:])
    pageIndices.append(pageIndices[0] + 1)
    pageIndices.pop(0)

f = open("output.txt", "w")
f.write("\n".join(visitedPages))
f.close()