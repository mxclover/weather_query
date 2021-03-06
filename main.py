# -*- coding = utf-8 -*-
#!/usr/bin/env python
'''部署在Heroku上的在线实时天气查询应用
调用心知天气API(https://www.seniverse.com/doc#now)
可在线查询国内2567个市区县的实时天气状况
'''
import os
import requests
import json
from flask import Flask, render_template, request
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_sever_error(e):
	return render_template('500.html'), 500

@app.route('/', methods=['GET','POST'])
def index():
	weather = ''
	if request.method == 'POST':
		if 'query' in request.form.keys():
			city_name = request.form['city_name']
			weather = get_weather(city_name)
		elif 'history' in request.form.keys(): 
			history_info = get_history()
			return render_template('user.html',info=history_info)
		elif 'help' in request.form.keys():
			help_info = get_help()
			return render_template('user.html',info=help_info)
	return render_template('user.html',info=weather)

history_list = []

def get_weather(city_name):
	result = requests.get('https://api.seniverse.com/v3/weather/now.json',
		params={
		'key': 'rirkq6fizk96iefr',
		'location': city_name,
		'language': 'zh-Hans',
		'unit': 'c'
		})	
	result.raise_for_status()
	result.text
	print(result.text)

	if result.status_code == 200:
		data = result.json()
		city = data['results'][0]['location']['name']
		city_temperature = data['results'][0]['now']['temperature']
		city_text = data['results'][0]['now']['text'] 
		time = data['results'][0]['last_update']

		history_list.append(city + ' ' + city_text + ' ' + city_temperature + '°C')
		return [city + ' ' + city_text+ ' ' + city_temperature + '°C','\n',"更新时间:" + ' ' + time[:10] + ' ' + time[11:16]]
	else:
		return ["对不起，您输入的城市不在查询范围内，请重新输入"]

def get_history():
	return history_list

def get_help():
	info_help = ["请输入城市名，获取该城市最新天气情况", "点击「帮助」，获取帮助信息", "点击「历史」，获取历史查询信息"]
	return info_help


if __name__ == '__main__':
    app.run(debug=True)
