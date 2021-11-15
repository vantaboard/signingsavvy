def get_html_path(letter, fn):
  return 'html/{0}/{1}.html'.format(letter, fn)

def get_asset_files(letter, asset_folder, asset_ext):
  letter.toupper()
  raw_files = []
  folder = '../{0}/{1}'.format(asset_folder, letter)
  files = [f for f in listdir(folder) if isfile(join(folder, f))]

  for file in files:
    raw_files.append(file)

  return raw_files

def get_active_files(letter):
  return get_asset_files(letter, 'html', 'html')
