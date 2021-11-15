def format_sign_file(file):
  file = re.sub(r'/|\s', '', file)
  file = re.sub(r'.*((?=.mp4)|(?=.html))', '', file)

  return file
