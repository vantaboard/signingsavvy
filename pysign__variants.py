from pysign_assets import get_html_files

from pysign__http import (get_api_route, get_http_word_links,
                          get_http_words_paths)

with session() as c:
  c.post(API_BASE, data = payload)

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
      files = get_html_files(letter)
      for file in files: file = '{0}1.html'.format(file[-6])
      files = list(set(files))

      for file in files:
        file = 'html/{0}/{1}'.format(letter, file)
        variations = get_variations(file)[1:]
        
        if not os.path.exists(file):
          for variation in variations:
            req = c.get(variation)
            links = get_http_word_links(req.text)

            for link in links:
              route = get_api_route(link)
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
      links = get_http_word_links(req.text)

      for link in links:
        file = 'html/{0}/{1}.html'.format(letter, format_sign_file(link))
        if not os.path.exists(format_sign_file(file)):
            color = fg('light_green_2')
            print(color + "Downloading", color + "{0}".format(file))

            open(file).write(res.text).close()
        else:
          color = fg('light_yellow')
          print(color + "Skipping", color + "{0}".format(file),
                color + "as it already exists")
