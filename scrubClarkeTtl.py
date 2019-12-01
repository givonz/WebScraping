# Find all chapter headings.

from bs4 import BeautifulSoup
from urllib.request import urlopen

ClarkeStart = urlopen("http://www.homeoint.org/books/kentrep/index.htm").read()
y=ClarkeStart.find_all("a")

#for link in ClarkeStart.find_all("a"):
#    print(link.get("href"))

