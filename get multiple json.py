import requests
import lxml.html as lh
from bs4 import BeautifulSoup

year = "2018"

f1_gp_date = requests.get("https://en.wikipedia.org/wiki/"+year+"_Formula_One_World_Championship")
f1_gp_date = lh.fromstring(f1_gp_date.content)
f1_gp_date = f1_gp_date.xpath('//tr')

for item in f1_gp_date:
    print(item.text_content())

print(f1_gp_date)
