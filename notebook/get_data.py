#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

# URLs
team_url = "https://www.basketball-reference.com/leagues/NBA_2023.html"
salary_url = "https://hoopshype.com/salaries/2022-2023/"

# Define the directory to store the raw data
raw_data_dir = "data/raw"
os.makedirs(raw_data_dir, exist_ok=True)

# Function to download HTML content from URL
def download(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to download from {url}. Status code: {response.status_code}")
        return None

# Function to extract data from HTML content
def extract(html_content):
    if html_content is None:
        return None
    soup = BeautifulSoup(html_content, "html.parser")
    return soup

# Function to save DataFrame to CSV file
def save_to_csv(dataframe, filename):
    dataframe.to_csv(filename, index=False)
#     print(f"Data saved to {filename}.")

# Download content from salary URL
salary_d = download(salary_url)

# Extract salary data content
salary_data = extract(salary_d)

if salary_data is not None:
    salary_table = salary_data.find('table', class_='hh-salaries-ranking-table hh-salaries-table-sortable responsive')
    salary_df = pd.read_html(str(salary_table))[0]
    salary_csv_file = os.path.join(raw_data_dir, "salary_data.csv")
    save_to_csv(salary_df, salary_csv_file)

# Save players_data to data/raw directory
players_data = pd.read_csv('data/raw/nba_data_processed.csv')
players_data_file = os.path.join(raw_data_dir, "players_data.csv")
players_data.to_csv(players_data_file, index=False)

# Team data 
team_url = "https://www.basketball-reference.com/leagues/NBA_2023.html"
response = requests.get(team_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    teams = soup.find_all("div", class_="team__details")
    table = soup.find_all(id="totals-team")
    val = pd.read_html(str(table))[0]
    team_table = pd.DataFrame(val)
    team_table_file = os.path.join(raw_data_dir, "team_table.csv")
    team_table.to_csv(team_table_file, index=False)
    
else:
    print("Failed to retrieve data:", response.status_code)

