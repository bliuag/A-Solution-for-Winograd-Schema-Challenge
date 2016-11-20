import requests
from bs4 import BeautifulSoup
import argparse
import re

parser = argparse.ArgumentParser(description='Get Google Count.')
parser.add_argument('word', help='word to count')
args = parser.parse_args()

r = requests.get('http://www.google.com/search',
                 params={'q':'"'+args.word+'"',
                         "tbs":"li:1"}
                )

soup = BeautifulSoup(r.text, "html.parser")
print(int(re.sub("[^0-9]", "", soup.find('div',{'id':'resultStats'}).text)))
