def sign_href_to_file(href):
  return re.sub(r'/|\s|.*((?=.mp4)|(?=.html))', '', link)

def sign_file_to_href(file):
  file = sign_link_to_file(file)

  indices = re.finditer(r'(?<=sign)|(?<=sign[A-Z])|(?=\d$)', file)
  for index in indices:
    file.insert(index, '/')

  return file
