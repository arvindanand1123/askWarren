import urllib
import urllib.request
from bs4 import BeautifulSoup
# import requests
# import json

# r = requests.session()

startDate = "20001001"
endDate = "20011001"
keyword = "microsoft"
headings = []

url = "https://www.nytimes.com/search?endDate=" + endDate + "&query=" + keyword + "&sort=newest&startDate=" + startDate
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, "html.parser")

# page = r.get(url)
# page = r.post("https://samizdat-graphql.nytimes.com/graphql/v2", data=json.dumps({"operationName":"SearchRootQuery","variables":{"first":10,"sort":"newest","beginDate":"20001001","endDate":"20011001","text":"microsoft","cursor":"YXJyYXljb25uZWN0aW9uOjk="},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"de2d6d889a070b5c320752f2db028cd84191b07fd4ebfaccb58cd93773f956c1"}}}))
# print(page.content)

# print(soup)

for heading in soup.find_all(attrs={"class": "Item-headline--3WqlT"}):
    heading = heading.text.strip()
    headings.append(heading)

print(headings)
