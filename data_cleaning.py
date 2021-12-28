# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 13:44:32 2021

@author: ASUS
"""

import pandas as pd
from datetime import date

df = pd.read_csv("glassdoor_ds_jobs.csv")

#about df columns
df.info()

#salary
#indication columns
df["Is Hourly"] = df["Salary Estimate"].apply(lambda x: 1 if "per hour" in x.lower() else 0)
df["Have Employer Provided"] = df["Salary Estimate"].apply(lambda x: 1 if "employer provided salary:" in x.lower() else 0)

#remove missing values in salary estimate
df = df[df["Salary Estimate"] != "-1"]

#preprocess to get the min and max number of salaries
salary = df["Salary Estimate"].apply(lambda x: x.split("(")[0])

#remove dollar sign and "K"
no_dollar_k = salary.apply(lambda x: x.replace("K","").replace("$",""))

#remove unnecessary text
min_hr = no_dollar_k.apply(lambda x: x.lower().replace("per hour","").replace("employer provided salary:",""))

#get the number of min and max salary from range, aslo the average salary
df["Min Salary"] = min_hr.apply(lambda x: x.split(" - ")[0])
df["Max Salary"] = min_hr.apply(lambda x: x.split(" - ")[1] if " - " in x else x)
df["Avg Salary"] = (df["Min Salary"].astype("int64") + df["Max Salary"].astype("int64"))/2

#company name
#remove rating in comp. name
def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False 

df["Company"] = df.apply(lambda x: x["Company Name"] if x["Rating"] < 0 else x["Company Name"][:-3], axis = 1)

#rating
#convert -1 into 0
df["Rating"] = df["Rating"].apply(lambda x: x if x > 0 else 0)

#size
#convert -1 into "Unknown"
df["Size"] = df["Size"].apply(lambda x: "Unknown" if x == "-1" else x)

#founded
#convert -1 to 0
df["Founded"] = df["Founded"].apply(lambda x: x if x > 0 else 0)

#type of ownership, industry, sector
#convert -1 into "Unknown"
df["Type of ownership"] = df["Type of ownership"].apply(lambda x: "Unknown" if x == "-1" else x)
df["Industry"] = df["Industry"].apply(lambda x: "Unknown" if x == "-1" else x)
df["Sector"] = df["Sector"].apply(lambda x: "Unknown" if x == "-1" else x)

#revenue
#convert -1 into "Unknown / Non-Applicable"
df["Revenue"] = df["Revenue"].apply(lambda x: "Unknown / Non-Applicable" if x == "-1" else x)

#company state
df["State"] = df["Location"].apply(lambda x: x.split(",")[1].strip() if ", " in x else x if x == "Remote" else "Unknown")
print(df["State"].value_counts())
#calculate age of company from 2021
year_now = date.today().year
df["Age of Company"] = df["Founded"].apply(lambda x: year_now - x if x > 0 else "Unknown")

#requirements
#requirements per type
df["python_ind"] = df["Job Description"].apply(lambda x: 1 if "python" in x.lower() else 0)
print(df["python_ind"].value_counts())

df["excel_ind"] = df["Job Description"].apply(lambda x: 1 if "excel" in x.lower() else 0)
print(df["excel_ind"].value_counts())

df["rstudio_ind"] = df["Job Description"].apply(lambda x: 1 if "r-studio" in x.lower() else 0)
print(df["rstudio_ind"].value_counts())

df["aws_ind"] = df["Job Description"].apply(lambda x: 1 if "aws" in x.lower() else 0)
print(df["aws_ind"].value_counts())

df["spark_ind"] = df["Job Description"].apply(lambda x: 1 if "spark" in x.lower() else 0)
print(df["spark_ind"].value_counts())

df["sql_ind"] = df["Job Description"].apply(lambda x: 1 if "sql" in x.lower() else 0)
print(df["sql_ind"].value_counts())

def reqs(desc):
    x = []
    
    if "python" in desc.lower():
        x.append("Python")
    if "excel" in desc.lower():
        x.append("Excel")
    if "r-studio" in desc.lower():
        x.append("R-Studio")
    if "aws" in desc.lower():
        x.append("AWS")
    if "spark" in desc.lower():
        x.append("Spark")
    if "sql" in desc.lower():
        x.append("SQL")
    
    if x:
        return ", ".join(x)
    else:
        return "No requirement specified"

#all requirements
df["Requirements"] = df["Job Description"].apply(reqs)
#print(df["Requirements"].value_counts())

skills = df[df["Requirements"] != "No requirement specified"]["Requirements"]
print(skills)

#save the clean data to csv
df.to_csv("glassdoor_ds_jobs_clean.csv", index = False)

#check
check = pd.read_csv("glassdoor_ds_jobs_clean.csv")