import os
import re
import string
import random
import requests
from bs4 import BeautifulSoup as BS
from urllib.request import urlretrieve
from utils import write

alpha_num = string.ascii_letters + string.digits

user_agents_url = 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Fuzzing/User-Agents/UserAgents-IE.txt'

os.makedirs('./tmp', exist_ok=True)
download_path = './tmp/user_agents.txt'

# download user-agents
if not os.path.exists(download_path):
    urlretrieve(user_agents_url, download_path)

# reading user-agents file
with open(download_path, 'r') as f:
    user_agents = f.readlines()
    user_agents = list(map(lambda x: x.strip('\n'), user_agents))

def return_user_agent():
    """
    this function returns different user agent randomly 
    """
    ua = random.choice(user_agents)
    # using this header to pretend as regular user so that we are not blocked by website
    headers = {
        'User-Agent': ua
    }
    return headers


def extract_para(url, dir, debug=None):
    """
    this function extracts paragraphs from website given its url
    """
    global count
    f = requests.get(url, headers=return_user_agent())
    soup = BS(f.content,'lxml')

    paragraphs = soup.find_all('p')
    paragraphs = list(map(lambda x: x.text, paragraphs))

    paragraphs = '\n'.join(paragraphs)

    title = soup.find('title')
    
    if title:
        title = title.text.split()
    else:
        title = random.choices(alpha_num, k=6)
        title = "".join(title)
        
    title = '-'.join(title[:4])
    if debug:
        file_name = title + '-' + str(debug) + '.txt'
    else:
        file_name = title + '.txt'

    write(dir, file_name, paragraphs)


def split_para(para):
    return re.split(r'\.[^0-9a-zA-Z]+', para)
