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
from colored import attr, bg, fg
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

path_base = "D:\personal\code\signlanguage_cards"

def get_video_link(html):
  soup = BeautifulSoup(html, 'html.parser')
  for link in soup.find_all('link'):
    href = link.get('href')
    if (href.startswith('media/') and href.endswith('mp4')):
      return href

def download(file, url):
  req = requests.get(url)
  f = file

  for chunk in req.iter_content(chunk_size=255): 
    if chunk: f.write(chunk)

  f.close()

with session() as c:
  base = 'https://www.signingsavvy.com'
  c.post(base, data = payload)

  for letter in list(string.ascii_uppercase):
    path = r"{0}\html\{1}".format(path_base, letter)
    files = [f for f in listdir(path) if isfile(join(path, f))]

    for file in files:
      in_path = r"{0}\html\{1}\{2}".format(path_base, letter, file)
      in_f = open(in_path, "r")

      out_path = r"{0}\videos\{1}\{2}".format(path_base, letter, file)
      out_path = re.sub(r'html', 'mp4', out_path)

      if not os.path.exists(out_path):
        out_f = open(out_path, "wb")

        color = fg('light_green_2')
        uri = "{0}/{1}".format(base, get_video_link(in_f))
        print(color + "Downloading", color + "{0}".format(out_path))
        download(out_f, uri)
      else:
        color = fg('light_yellow')
        print(color + "Skipping", color + "{0}".format(out_path),
               color + "as it already exists")
