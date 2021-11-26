'''
import curses
import os
import sqlite3
import string
import sys
from curses import wrapper
from getpass import getpass

from bs4 import BeautifulSoup

from pysign import api, format

letters = list(string.ascii_uppercase)

def authenticate():
  stdscr = curses.initscr()
  return fetch_creds(stdscr)

def fetch_creds(stdscr):
  stdscr.clear()
  curses.echo()

  stdscr.addstr(0, 0, "=== Authenticate yourself ===")
  stdscr.addstr(1, 0, "Email: ")
  
  email = stdscr.getstr(1, 7).decode(encoding = 'utf-8')
  pw = getpass(prompt='Password: ', stream=None)

  return (email, pw)

def get_variations(action):
    soup = BeautifulSoup(action, 'html.parser')
    descs = soup.findAll('div', {'class': 'desc'})

    for desc in descs:
        if (desc.find("h5").text == "Sign Variations for this Word"):
            if (desc.ul):
                return desc.ul.findAll('li')

    return null


def get_other_variants(letters = letters):
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


def get_first_variants(letters = letters):
    paths = get_http_word_links(letters)

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


def get_http_word_links(action):
    links = []

    soup = BeautifulSoup(action, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if (href.startswith('sentences/')):
            links.append(href)
    return links


def get_all_sentences():
    route = get_route('sentences/all')
    req = c.get(route)
    links = scrape_sentences(req.text)

    files = get_available_sentences()
    paths = []
    for file in files:
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


paths = get_http_word_links(letters)

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


def connect(init=False):
    if not os.path.exists(_globals.file.database) and not init:
        print('Database not found.')
        raise FileNotFoundError

    con = sqlite3.connect(_globals.file.database)

    if con:
        print('Connected to database successfully.')
    else:
        print('Failed to open database.')

    return con


def create():
    print('Creating database...')
    con = connect(True)
    cur = con.cursor()

    # Create user table
    cur.execute("CREATE TABLE user (email text, pass text)")

    # Create vocabulary table
    cur.execute('''CREATE TABLE vocabulary
  (word_id integer, name text, variant integer,
  meaning text, type text, description text,
  mnemonic text, example text, notice text)''')

    # Create usage table
    cur.execute("CREATE table usage (word_id integer, value text)")

    # Create synonym table
    cur.execute("CREATE table synoynm (word_id integer, value text)")

    # Create variant table
    cur.execute("CREATE table variant (word_id integer, value integer)")

    cur.execute("INSERT INTO user VALUES ('{0}', '{1}')"
                .format(authenticate()))

    con.commit()
    con.close()
'''
