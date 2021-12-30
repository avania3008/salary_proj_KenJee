# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 09:51:06 2021

@author: ASUS
"""
import requests
from data_input import data_input

url = "http://127.0.0.1:5000/predict"
headers = {"Content-Type": "application/json"}
data = {"input": data_input}

r = requests.get(url, headers = headers, json = data)

r.json()