# -*- coding = utf-8 -*-
#!/usr/bin/env python
import os
import requests
import json
import psycopg2
import psycopg2.extras

result = requests.get('https://api.thinkpage.cn/v3/weather/now.json',
    params={
    'key': 'rirkq6fizk96iefr',
    'location': city_name,
    'language': 'zh-Hans',
    'unit': 'c'
    })  
result.raise_for_status()

data = result.json()
city = data['results'][0]['location']['name']
city_temperature = data['results'][0]['now']['temaperature']
city_text = data['results'][0]['now']['text']

conn = psycopg2.connect("dbname=mydb")
cur = conn.cursor()

_sql = '''INSERT INTO json_test (weather) VALUES('city_temperature');'''

cur.execute(_sql)
cur.execute("SELECT * FROM json_test WHERE weather = '晴';")
data = cur.fetchone()

conn.commit()
print(weather, type(weather))


cur.close()
conn.close()





