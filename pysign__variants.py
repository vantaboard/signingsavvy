from pysign_assets import get_active_files

from pysign__formatting import sign_href_to_file
from pysign__globals import LETTERS
from pysign__http import get_http_word_links, get_http_words_paths, get_route


def get_variations(action):
  soup = BeautifulSoup(action, 'html.parser')
  descs = soup.findAll('div', { 'class' : 'desc' })

  for desc in descs:
    if (desc.find("h5").text == "Sign Variations for this Word"):
      if (desc.ul):
        return desc.ul.findAll('li')

  return null

def get_other_variants(letters = LETTERS):
  for i in range(len(letters)):
    letter = letters[i]

    files = get_active_files(letter)
    paths = []
    for file in files:
      file = file[-1]
      file.append(1)
      html_paths.append(get_html_path(letter, file))

    html_paths = list(set(paths))

    for path in html_paths:
      variations = get_variations(path)[1:]
      
      if not os.path.exists(path):
        for url in variations:
          r = c.get(url)
          links = get_http_word_links(r.text)

          for link in links:
            route = get_route(link)
            print("Writing", file, "from route", route)

            req = c.get(route)
            file = open(file).write(req.text).close()
      else:
        print("Skipping", file, "as it already exists")

def get_first_variants(letters = LETTERS):
  paths = get_http_words_paths(letters)

  for i in len(letters):
    path = paths[i]
    letter = letters[i]

    req = c.get(path)
    links = browse_word_links(req.text)

    for link in links:
      file = 'html/{0}/{1}.html'.format(letter, sign_href_to_file(link))
      if not os.path.exists(sign_href_to_file(file)):
          color = fg('light_green_2')
          print(color + "Downloading", color + "{0}".format(file))

          open(file).write(res.text).close()
      else:
        color = fg('light_yellow')
        print(color + "Skipping", color + "{0}".format(file),
              color + "as it already exists")
