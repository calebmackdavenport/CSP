import requests
from bs4 import BeautifulSoup
import re

def getAllLinks(soupURL, soupKey):
    if(soupURL):
        if soupURL.startswith('http'):
            homepage = re.sub(r'https?:\\', '', soupURL)
        if soupURL.startswith('www.'):
            homepage = re.sub(r'www.', '', soupURL)

    page = requests.get(soupURL)
    soup = BeautifulSoup(page.content, 'html.parser')

    dictionary = {}
    dictionary['email'] = []
    dictionary['internal'] = []
    dictionary['external'] = []
    dictionary['suspicious'] = []

    links = []

    # main page links
    for a in soup.find_all('a', href=True):
            if ("mailto" in a['href']):
                    dictionary['email'].append(a['href'])
            elif ("/" == a['href'][0] or homepage in a['href']):
                if("/" == a['href'][0]):
                    if(homepage + a['href'] not in dictionary['internal']): dictionary['internal'].append(homepage + a['href'])
                else:
                    if(a['href'] not in dictionary['internal']): dictionary['internal'].append(a['href'])
            elif ("https://" in a['href']):
                    dictionary['external'].append(a['href'])
            else:
                if (a['href'][0] != '.' and a['href'] != '#'):
                    dictionary['suspicious'].append(a['href'])

    # internal page links
    count = 0;

    def internalLinks():
        for intLink in dictionary['internal']:
            intPage = requests.get(intLink)
            intSoup = BeautifulSoup(intPage.content, 'html.parser')
            soupKey = "intLink" + str(count); count+=1;

            dictionary = {}
            dictionary['link'] = []
            dictionary['email'] = []
            dictionary['internal'] = []
            dictionary['external'] = []
            dictionary['suspicious'] = []

            for a in intSoup.find_all('a', href=True):

                    if ("mailto" in a['href']):
                            dictionary['email'].append(a['href'])
                    elif ("/" == a['href'][0] or homepage in a['href']):
                        if("/" == a['href'][0]):
                            if(homepage + a['href'] not in dictionary['internal']): dictionary['internal'].append(homepage + a['href'])
                        else:
                            if(homepage + a['href'] not in dictionary['internal']): dictionary['internal'].append(a['href'])
                    elif ("https://" in a['href']):
                            dictionary['external'].append(a['href'])
                    else:
                            dictionary['suspicious'].append(a['href'])

    return dictionary