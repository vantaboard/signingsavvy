def get_asset_files(letter, asset_folder, asset_ext):
  letter.toupper()
  raw_files = []
  folder = '../{0}/{1}'.format(asset_folder, letter)
  files = [f for f in listdir(folder) if isfile(join(folder, f))]

  for file in files:
    file = format_sign_file(file)
    raw_files.append(file)

  return raw_files

def get_video_files(letter):
  return get_asset_files(letter, 'videos', 'mp4')

def get_html_files(letter):
  return get_asset_files(letter, 'html', 'html')
