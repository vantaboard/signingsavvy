from dotenv import dotenv_values

config = dotenv_values('.env')

payload = {
  'action': 'login',
  'username': config['USER_NAME'],
  'password': config['PASSWORD'],
  'login': 1,
  'search': '',
  'find': 1
}
