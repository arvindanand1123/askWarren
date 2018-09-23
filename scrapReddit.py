import urllib.request
from bs4 import BeautifulSoup
import json

extracted_records = []
url = "https://old.reddit.com/r/microsoft/new"
headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}
pagecount = 1

while(True):
    request = urllib.request.Request(url,headers=headers)
    html = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(html,'html.parser')
    #First lets get the HTML of the table called site Table where all the links are displayed
    main_table = soup.find("div",attrs={'id':'siteTable'})
    #Now we go into main_table and get every a element in it which has a class "title"
    links = main_table.find_all("a",class_="title")
    next = main_table.find(class_="next-button")
    if (next != None):
        next = next.find("a")
        print(next['href'])
        #List to store a dict of the data we extracted
        next = main_table.find(class_="next-button")
        next = next.find("a")
        next = next['href']
        print("Next url: " + next)
        print(pagecount)
        for link in links:
            title = link.text
            url = link['href']
            if not url.startswith('http'):
                url = "https://old.reddit.com"+url
            record = {
                'title':title,
                'url':url
                }
            extracted_records.append(record)
            url = next
        pagecount+=1
    else:
        break
print(extracted_records)
print(len(extracted_records))


#Lets write these to a JSON file for now.
with open('data.json', 'w') as outfile:
    json.dump(extracted_records, outfile, indent=4)
