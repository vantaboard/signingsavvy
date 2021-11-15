import os
import re
import string
import time
from dataclasses import dataclass
from os import listdir
from os.path import isfile, join
from xml.dom import minidom

import requests
from bs4 import BeautifulSoup
from dotenv import dotenv_values
from requests import session

path_base = 'D:/personal/code/signlanguage_cards'

def get_variations(html):
  soup = BeautifulSoup(html, 'html.parser')
  descs = soup.findAll('div', { 'class' : 'desc' })

  for desc in descs:
    if (desc.find("h5").text == "Sign Variations for this Word"):
      if (desc.ul):
        return desc.ul.findAll('li')

  return ""

import re
import string
from dataclasses import dataclass
from xml.dom import minidom

from bs4 import BeautifulSoup
from dotenv import dotenv_values
from requests import session

config = dotenv_values('.env')

payload = {
    'action': 'login',
    'username': config['USER_NAME'],
    'password': config['PASSWORD'],
    'login': 1,
    'search': '',
    'find': 1
}

with session() as c:
  base = 'https://www.signingsavvy.com'
  c.post(base, data = payload)

  for letter in list(string.ascii_uppercase):
    path = '{0}/html/{1}'.format(path_base, letter)
    files = [f for f in listdir(path) if isfile(join(path, f))]

    for file in files:
      path = '{0}/html/{1}'.format(path_base, letter)
      html = open('{0}/{1}'.format(path, file), 'r')

      links = []
      variations = get_variations(html)
      if (len(variations) > 2):
        for variation in variations[2:]:
          for link in variation.find_all('a'):
            href = link.get('href')
            if (href.startswith('sign/')):
              links.append(href)

      if (links):
        for link in links:
          uri = '{0}/{1}'.format(base, link)
          file = "../html/{0}/{1}.html".format(letter,
            re.sub(r'/|\s', '', link))

          if not os.path.exists(file):
            req = c.get(uri)

            f = open(file, 'w')
            f.write(req.text)
            print("Writing", file)
            print(req.status_code, link)
            f.close()

          print("Skipping", file, "as it already exists")
