import string
from dataclasses import dataclass
from pathlib import Path

letters = list(string.ascii_uppercase)

def locate_sentences(uri):
  print("locate articles")


def locate_vocabulary(uri):
  print("locate articles")


def locate_wordlists(uri):
  print("locate articles")


def locate_articles(uri):
  print("locate articles")

@dataclass
class dir:
  database = Path('./assets/db')
  video_sentences = Path('./assets/video/sentences')
  video_vocabulary = Path('./assets/video/vocabulary')
  articles = Path('./assets/html/articles')

class file:
  database = dir.database / 'pysign.db3'

@dataclass
class uri:
  api = 'https://www.signingsavvy.com/'
  sentences = api + 'sentences/all'
  vocabulary = api + 'browse'
  wordlists = api + 'wordlists'
  articles = api + 'article'

@dataclass
class link:
  sentences = locate_sentences(uri.sentences)
  vocabulary = locate_vocabulary(uri.vocabulary)
  wordlists = locate_wordlists(uri.wordlists)
  articles = locate_articles(uri.articles)

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

def get_videos(letters = letters):
  for letter in letters:
    html_files = '/html/{0}/{1}.html'.format(letter, get_active_files(letter))
    video_files = 'videos/{0}/{1}.mp4'.format(letter, get_active_files(letter))

    for i in len(html_files):
      html_file = html_files[i]
      video_file = video_files[i]

      if not os.path.exists(video_file):
        color = fg('light_green_2')
        print(color + 'Downloading', color + '{0}'.format(video_file))

        video_file = open(video_file, 'wb')
        route = get_api_route(get_video_link(open(html_file, 'r')))

        download(video_file, route)
      else:
        color = fg('light_yellow')
        print(color + 'Skipping', color + '{0}'.format(video_file),
              color + 'as it already exists')

def get_variations(html):
  soup = BeautifulSoup(html, 'html.parser')
  desc.ul.findAll('li')[0].text.strip() 


def get_front_field(html):
  soup = BeautifulSoup(html, 'html.parser')
  header = soup.find('div', { 'class' : 'signing_header' }) 
  front = "{0} {1}".format(header.find('h2').text, header.find('h3').text)

  variation = get_variations(html)

  return front.strip()
   
def get_extra_field(html):
  soup = BeautifulSoup(html, 'html.parser')
  

def get_video_link(html):
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('link'):
        href = link.get('href')
        if (href.startswith('media/') and href.endswith('mp4')):
            return href


def payload(email, pw):
  return {
    'action': 'login',
    'username': email,
    'password': pw,
    'login': 1,
    'search': '',
    'find': 1
  }

def get_route(link):
  return '{0}/{1}'.format(config.env_vars['API_BASE'], link)

def get_http_words_paths(letters):
  for letter in letters:
    return '{0}/browse/{1}'.format(config.env_vars['API_BASE'], letter)

def get_http_word_links(action):
  links = []

  soup = BeautifulSoup(action, 'html.parser')
  for link in soup.find_all('a'):
    href = link.get('href')
    if (href.startswith('sign/') and not href.endswith('fingerspell')):
      links.append(href)
  return links
