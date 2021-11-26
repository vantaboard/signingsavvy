import os
import string

letters = list(string.ascii_uppercase)

def make_asset_dirs():
  try:
    os.makedirs(path.database)
    os.makedirs(path.video_sentences)
    
    for letter in letters:
      os.makedirs(path.video_vocabulary / letter)
  except FileExistsError:
    print('Warning: Some or all asset paths already exist.')
  except:
    print('An unknown error has occurred.')

def make():
  make_asset_dirs()
