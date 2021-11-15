from pysign__config import config

def get_route(link):
  return '{0}/{1}'.format(config['API_BASE'], link)

def get_http_words_paths(letters):
  for letter in letters:
    return '{0}/browse/{1}'.format(config['API_BASE'], letter)

def get_http_word_links(action):
  links = []

  soup = BeautifulSoup(action, 'html.parser')
  for link in soup.find_all('a'):
    href = link.get('href')
    if (href.startswith('sign/') and not href.endswith('fingerspell')):
      links.append(href)
  return links
