import requests
import urllib
import uuid
import re
import csv
from bs4 import BeautifulSoup
import pandas as pd
import sys

df = pd.read_csv('1.csv', sep=',', header=None)
rows = df.values;
i = 0;
# print(len(rows))
# sys.exit(0);

for row in rows:
    # try:
    page = requests.get("https://in.finance.yahoo.com/quote/" + row[1] + "/key-statistics?p=" + row[1])
    soup = BeautifulSoup(page.content, 'html.parser')
    trTag = soup.find_all("tr")
    for tr in trTag:
        if re.match(".*Float.*", tr.text) is not None:
            d = tr.text;
            data = d.split();
            x = '"' + row[1] + '","' + data[1] + '"' + '\n'
            print(str(i)+". "+row[1]+"-->"+data[1])
            i = i +1;
            with open(uuid.uuid4().hex + ".csv", "w") as f:
                f.write(x)
    # except:
    #     print("error")
