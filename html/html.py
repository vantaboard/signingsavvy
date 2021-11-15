from requests import session
from bs4 import BeautifulSoup
from dotenv import dotenv_values
from dataclasses import dataclass
from xml.dom import minidom
import string
import re

config = dotenv_values('.env')

payload = {
    'action': 'login',
    'username': config['USER_NAME'],
    'password': config['PASSWORD'],
    'login': 1,
    'search': '',
    'find': 1
}

def get_words(req):
    links = []

    soup = BeautifulSoup(req.text, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if (href.startswith('sign/') and not href.endswith('fingerspell')):
            links.append(href)
    return links

with session() as c:
    base = 'https://www.signingsavvy.com'
    c.post(base, data = payload)

    for letter in list(string.ascii_uppercase):
        uri = '{0}/browse/{1}'.format(base, letter)
        req = c.get(uri)

        for word in get_words(req):
            uri = '{0}/{1}{2}'.format(base, word[:-1], 1)
            req = c.get(uri)
            f = open("{0}{1}.html"
                    .format(re.sub(r'/|\s', '', word[:-1]), 1), 'w')
            f.write(req.text)
            f.close()

            uri = '{0}/{1}{2}'.format(base, word[:-1], 2)
            req = c.get(uri)
            f = open("{0}{1}.html"
                    .format(re.sub(r'/|\s', '', word[:-1]), 2), 'w')
            f.write(req.text)
            f.close()

