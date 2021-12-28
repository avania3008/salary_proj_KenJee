# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 14:15:46 2021

@author: ASUS
"""

import glassdoor_scraper as gs
import pandas as pd

df = gs.get_jobs("data scientist", 500, False, 15)
print(df)

df.to_csv("glassdoor_ds_jobs.csv", index = False)