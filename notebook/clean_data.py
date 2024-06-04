#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os


# In[2]:


raw_data_path = "data/raw"
processed_data_path = "data/processed"
os.makedirs(processed_data_path, exist_ok=True)


players_d=pd.read_csv('data/raw/players_data.csv')
salary_data=pd.read_csv('data/raw/salary_data.csv')
team_table=pd.read_csv('data/raw/team_table.csv')


# ### Players data clean

# In[3]:


#columns required in player's data (Points, Rebounds, Assits, Steal, Blocks, Turnover,Team,Player)
players_d=players_d.drop_duplicates(subset=['Player']).reset_index(drop=True)
players_d=players_d.dropna()
players = players_d.rename(columns={'Tm': 'Team'})
players = players[players['Team'] != 'TOT']


# In[4]:


# A dictionary to map abbreviated team names 
team_name_mapping = {
    'ATL': 'Atlanta',
    'BOS': 'Boston',
    'BRK': 'Brooklyn',
    'CHI': 'Chicago',
    'CHO': 'Charlotte',
    'CLE': 'Cleveland',
    'DAL': 'Dallas',
    'DEN': 'Denver',
    'DET': 'Detroit',
    'GSW': 'Golden State',
    'HOU': 'Houston',
    'IND': 'Indiana',
    'LAC': 'LA Clippers',
    'LAL': 'LA Lakers',
    'MEM': 'Memphis',
    'MIA': 'Miami',
    'MIL': 'Milwaukee',
    'MIN': 'Minnesota',
    'NOP': 'New Orleans',
    'NYK': 'New York',
    'OKC': 'Oklahoma City',
    'ORL': 'Orlando',
    'PHI': 'Philadelphia',
    'PHO': 'Phoenix',
    'POR': 'Portland',
    'SAC': 'Sacramento',
    'SAS': 'San Antonio',
    'TOR': 'Toronto',
    'UTA': 'Utah',
    'WAS': 'Washington'
}

# Replace the values with mapped values
players['Team'] = players['Team'].replace(team_name_mapping)
players


# In[5]:


# Remove values not required for computation and rename columns in salary data
cols=['Team','2022/23']
salary_data=salary_data[cols]
salary_data['Team']
salary_data = salary_data.rename(columns={'2022/23': 'Cap Salary'})
salary_data


# In[6]:


#drop NaN Value in the team data 
team_table = team_table.dropna(subset=['Rk'])
#Map the team names based on abbrevations 
team_name_mapping = {
    'Sacramento Kings*': 'Sacramento',
    'Golden State Warriors*': 'Golden State',
    'Atlanta Hawks*': 'Atlanta',
    'Boston Celtics*': 'Boston',
    'Oklahoma City Thunder*': 'Oklahoma City',
    'Los Angeles Lakers*': 'LA Lakers',
    'Utah Jazz': 'Utah',
    'Milwaukee Bucks*': 'Milwaukee',
    'Memphis Grizzlies*': 'Memphis',
    'Indiana Pacers': 'Indiana',
    'New York Knicks*': 'New York',
    'Denver Nuggets*': 'Denver',
    'Minnesota Timberwolves*': 'Minnesota',
    'Philadelphia 76ers*': 'Philadelphia',
    'New Orleans Pelicans*': 'New Orleans',
    'Dallas Mavericks': 'Dallas',
    'Phoenix Suns*': 'Phoenix',
    'Los Angeles Clippers*': 'LA Clippers',
    'Portland Trail Blazers': 'Portland',
    'Brooklyn Nets*': 'Brooklyn',
    'Washington Wizards': 'Washington',
    'Chicago Bulls*': 'Chicago',
    'San Antonio Spurs': 'San Antonio',
    'Toronto Raptors*': 'Toronto',
    'Cleveland Cavaliers*': 'Cleveland',
    'Orlando Magic': 'Orlando',
    'Charlotte Hornets': 'Charlotte',
    'Houston Rockets': 'Houston',
    'Detroit Pistons': 'Detroit',
    'Miami Heat*':'Miami'
}
team_table = team_table.rename(columns={'Rk': 'Rank'})
team_table['Team'] = team_table['Team'].replace(team_name_mapping)
team_table


# In[7]:


team_table.to_csv(os.path.join(processed_data_path, "team_table.csv"), index=False)
salary_data.to_csv(os.path.join(processed_data_path, "salary_data.csv"), index=False)
players.to_csv(os.path.join(processed_data_path, "players.csv"), index=False)

