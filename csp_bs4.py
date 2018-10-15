import getLinks
import time
import json

# url = "https://django-final-beer-project.herokuapp.com"
url = "https://www.google.com"


def getAllLinks():
    allLinks = {}
    count=0;

    allLinks['main'] = getLinks.getAllLinks(url, "main"); 
    for intLink in allLinks['main']['internal']:
        allLinks['sublink' + str(count)] = getLinks.getAllLinks(intLink, 'main');
        count+=1
        time.sleep(0.33)
    return allLinks

links = getAllLinks()
links = json.dumps(links)
link = json.loads(links)
print(link)