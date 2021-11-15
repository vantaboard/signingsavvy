import os
import re
import string
import time
import requests
from requests import session
from dataclasses import dataclass
from os import listdir
from os.path import isfile, join
from xml.dom import minidom
from bs4 import BeautifulSoup
from dotenv import dotenv_values
from colored import attr, bg, fg
