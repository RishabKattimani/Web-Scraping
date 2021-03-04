# Imports
import requests
from bs4 import BeautifulSoup
import pandas as pd

#------------------------------------------------------
# 1st Part

url = 'https://www.marketwatch.com/tools/screener/premarket'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

#------------------------------------------------------
#2nd Part

title = soup.find_all('h1', class_='title')

#------------------------------------------------------
#3rd Part

for x in soup.find_all('h1', class_='title'):
    print(x.text)


#------------------------------------------------------
# 4th Part

table = soup.find_all('div', class_='element element--table table--fixed screener-table')
column_headers = ['Symbol', 'Price', 'Volume', 'Change$', 'Change%']
dataframe = pd.DataFrame(columns = column_headers)
symbol=''
price=''
volume=''
change = ''
change_percent = 0



for tr in soup.select('a'):
        tr.extract()

i = 1
for tr in table[0].find_all('tr'):
    i=0

    for td in tr.find_all('td'):
        i = i+1

        if(i==1):
            symbol=td.text.replace('\n', '')
        if(i==3):
            price=td.text.replace('\n', '')
        if(i==4):
            volume=td.text.replace('\n', '')
        if(i==5):
            change=td.text.replace('\n', '')
        if(i==6):
            change_percent = float(td.text.replace('\n', '').replace('%', ''))

    if (symbol!=''):
        dataframe = dataframe.append(
        pd.Series([
        symbol,
        price,
        volume,
        change,
        change_percent
        ],
        index = column_headers),
        ignore_index = True)
dataframe.sort_values("Change%", axis = 0, ascending = False,
             inplace = True, na_position ='last')

print(dataframe)
