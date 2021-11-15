from pysign_assets import get_html_files

from pysign__globals import LETTERS
from pysign__http import get_api_route


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

def get_videos(letters = LETTERS):
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
