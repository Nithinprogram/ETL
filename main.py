import requests
from bs4 import BeautifulSoup
import pandas as pd

#extract the data using bs4
url="https://www.fortuneindia.com/fortune-500/company-listing?year=2023&page=1&query=&per_page=500"
page=requests.get(url)
soup=BeautifulSoup(page.content ,'html.parser')
table=soup.find('table', class_='table')

th_tags = table.find_all('th', class_='f-500-tablehead primary-header')
col1 = []
for th_tag in th_tags:
    text = th_tag.get_text(strip=True)
    if text == "":
        col1.append('null')  
    else:
        col1.append(text)
#print(col1)

th_elements1 = table.find_all('th', class_='f-500-tablehead')
col2 =[]
for th in th_elements1:
    a_tag = th.find('a')
    if a_tag:
        span_tag = a_tag.find('span')
        if span_tag:
            col2.append(span_tag.text)
#print(col2)

header_row = ['rank2023', 'rank2022', 'rankchange', 'company', 'ownership', 
 'totalincome Rs cr', 'totalincome yoychange%', 'netincome Rs cr', 
 'netincome yoychange%', 'profit Rs cr', 'profit rank', 'profityoy change%', 
 'profit %of total income', 'interest cost Rs cr', 'interest cost %ebitda', 
 'cash&bankbalance Rs cr', 'total debt rs cr', 'debit-equity ratio(x)', 
 'total assests rs cr', 'total assests rank', 'total assests yoy change%', 
 'networth Rs cr', 'networth rank', 'networth yoy change%', 
 'ronw(%)', 'roce(%)', 'employees (in nos)', 'employees(rank)', 
 't12 avg m-cap Rs crore', 'tsr(%)'
]
all_rows_data=[]
rows = table.find_all('tr', class_='mpw-tr company-details-row')

for row in rows:
    row_data = [] 
    td_tags = row.find_all('td')
    for td in td_tags:
        td_text = td.get_text(strip=True)
        span = td.find('span')
        span_text = span.get_text(strip=True) if span else ""
        row_data.append(td_text)
        if span_text:
            row_data.append(span_text)
    #print(row_data)
    all_rows_data.append(row_data)
    
all_rows_data = [row[:len(header_row)] + [None]*(len(header_row) - len(row)) for row in all_rows_data]

# Create DataFrame
df = pd.DataFrame(all_rows_data, columns=header_row)

# Export the DataFrame to a CSV file
df.to_csv('output.csv', index=False)

print("CSV export complete.")


    








