import requests
from pysign__globals import ANKI_BASE

def post(action, deck_name, model_name, front, extra,
  initial, source, tags, video_path, video_filename):
  req = requests.post(anki_base, json = {
    'action': action,
    'version': 6,
    'params': {
      'note': {
        'deckName': deck_name,
        'modelName': model_name,
        'fields': {
          'Front': front,
          'Back': '',
          'Extra': extra,
          'Initial': initial,
          'Source': source,
          'Mind': ''
        },
        'options': {
          'allowDuplicate': False,
          'duplicateScope': 'deck',
          'duplicateScopeOptions': {
            'deckName': deck_name,
            'checkChildren': False,
            'checkAllModels': False
          }
        },
        'tags': tags,
        'video': [{
          'path': video_path,
          'filename': video_filename,
          'fields': [ 'Back' ]
        }]
      }
    }
  })

  return req

'html/sign/{0}/{1}/{2}'.format(letter, id, variant_number)

tags = [ 'nonfiction::asl::vocabulary::{0}'.format(letter) ]
for synonym in get_synonyms(deckname, html):
  tags.append(synonym)

req = post('addNote', deck_name, model_name, get_front_field(html),
  get_extra_field(html), get_initial(html), get_source(html, letter, id,
  variation), tags, video_path, video_filename)

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

deck_name = 'nonfiction::asl'
model_name = 'basic_reverse_extra_initial'

def create_flashcards():
  for letter in list(string.ascii_uppercase):
      path = 'html/{0}'.format(letter)
      files = [f for f in listdir(path) if isfile(join(path, f))]

      for file in files:
          path = 'html/{0}'.format(letter)
          html = open('{0}/{1}'.format(path, file), 'r')

          path = 'videos/{0}'.format(letter)
          video_path = re.sub('html', 'mp4', '{0}/{1}'.format(path, file))
          video_filename = video_path.rsplit('/', 1)[-1]

          'html/sign/{0}/{1}/{2}'.format(letter, id, fingerspell)

          tags = [ 'nonfiction::asl::vocabulary::{0}'.format(letter) ]
          for synonym in get_synonyms(deckname, html):
            tags.append(synonym)

          req = post('addNote', deck_name, model_name, get_front_field(html),
            get_extra_field(html), get_initial(html), get_source(html, letter,
            id, fingerspell = True), tags, video_path, video_filename)

          print(req)
