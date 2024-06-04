#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os


# In[2]:


processed_data_path="data/processed"
players=pd.read_csv('data/processed/players.csv')
salary_data=pd.read_csv('data/processed/salary_data.csv')
team_table=pd.read_csv('data/processed/team_table.csv')


# In[3]:


def merge_data(team_table,data):
    existing_col = set(team_table.columns)
    new_columns = [col for col in data.columns if col not in existing_col]
    if new_columns:
        team_table = pd.merge(team_table, data, on='Team', how='left')
    team_table.to_csv(os.path.join(processed_data_path, "team_table.csv"), index=False)
    return team_table


# In[4]:


existing_col = set(team_table.columns)
new_columns = [col for col in salary_data.columns if col not in existing_col]
if new_columns:
    team_table = pd.merge(team_table, salary_data, on='Team', how='left')


# In[5]:


team_table.to_csv(os.path.join(processed_data_path, "team_table.csv"), index=False)
salary_data.to_csv(os.path.join(processed_data_path, "salary_data.csv"), index=False)
players.to_csv(os.path.join(processed_data_path, "players.csv"), index=False)

