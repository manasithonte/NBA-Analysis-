#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import integrate_data
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter


# In[2]:


processed_data_path="data/processed"
players=pd.read_csv('data/processed/players.csv')
salary_data=pd.read_csv('data/processed/salary_data.csv')
team_table=pd.read_csv('data/processed/team_table.csv')


# In[3]:


#Fantasy Point: An advanced metric for player performance calculation as per NBA official website
FP = {
    'PTS': 1,    
    'AST': 1.5,  
    'TRB': 1.2, 
    'STL': 3,
    'BLK': 3,
    'TOV':-1
}


# Fantasy points for each player
players['Fantasy Points'] = players[['PTS', 'AST', 'TRB', 'STL', 'BLK','TOV']].mul(FP).sum(axis=1)


# PER formula an advanced metric to determine player performance
uPER_coeffs = {
    
    'PTS': 0.667,
    'FG': 1,
    'MP':1.5,
    'FGA': -0.5,
    'FT': 0.5,
    'TRB': 0.75,
    'AST': 1,
    'STL': 1,
    'BLK': 1.5,
    'PF': -1,
    'TOV': -1
}


# PER calculations for each player
uPER = sum((players[col] * coeff)*(1/players['MP']) for col, coeff in uPER_coeffs.items())
players['uPER'] = uPER


# True Shooting (TS) an advanced metric for determining player performance
TS_coeffs = {
    'PTS': 1,
    'FGA': 2,
    'FTA': 0.44
}


# Calculate True Shooting % for each player 
TS_percentage = players['PTS'] / (TS_coeffs['FGA'] + TS_coeffs['FTA'] * 0.44)
players['TS%'] = TS_percentage


# Compute a composite score for each player using parameters like FP, PER, TS, eFG
players['Composite Score'] = players[['Fantasy Points', 'uPER', 'TS%', 'eFG%']].sum(axis=1)
players


# In[4]:


#Rank players according to their respective Composite Score, rank top 5 players in each team
players['Rank'] = players.groupby('Team')['Composite Score'].rank(ascending=False)
players = players.groupby('Team').apply(lambda x: x.nlargest(5, 'Composite Score'))

# Compute overall rank across all teams
players['Overall Rank'] = players['Composite Score'].rank(ascending=False)

# Reset index and remove 
players.reset_index(drop=True, inplace=True)
players


# In[5]:


#Compute cumulative composite score for each team
team_cscore = players.groupby('Team')['Composite Score'].sum().reset_index()
team_cscore.columns = ['Team', 'Composite Score']


# In[6]:


#Call merge data function from integrate.py script to add cummulative composite score for each team in team data
team_table=integrate_data.merge_data(team_table,team_cscore)


# In[7]:


# In Cap Salary remove the dollar sign and change it's datatype to int
team_table['Cap Salary'] = team_table['Cap Salary'].replace('[\$,]', '', regex=True)
team_table['Cap Salary'] = team_table['Cap Salary'].astype(int)
team_table


# In[8]:


# Find the top 50 players as per their overall rank
top_50_players = players.sort_values(by='Overall Rank').head(50)
#Count how many of these players belong to each team
team_counts = top_50_players['Team'].value_counts()

#Plot a pie chart representating the distribution of players of each team in top 50 players
custom_palette = sns.color_palette("husl", len(players['Team'].unique()))
plt.figure(figsize=(10, 10))
plt.pie(team_counts, labels=team_counts.index, autopct='%1.1f%%', startangle=140, colors=custom_palette)
plt.title('Percentage of Players from Each Team Among Top 50 Players (Based on Overall Rank)',pad=20)
plt.axis('equal')  
plt.show()


# In[9]:


# Correlation Matrix to determine relation between Cummulative Team Composite Rank and Team Rank
correlation_matrix = team_table[['Composite Score', 'Rank']].corr()

# Display correlation matrix
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='viridis', fmt=".2f", linewidths=.5)
plt.title('Correlation Matrix between Composite Score and Rank')
plt.show()


# In[10]:


# Group the data by team and find the player with the highest Composite Score in each team
most_influential_players = players.groupby('Team').apply(lambda x: x.loc[x['Composite Score'].idxmax()])

# Plot the Composite Score of the most influential player in each team
plt.figure(figsize=(10, 6))
plt.bar(most_influential_players['Team'] + ' - ' + most_influential_players['Player'], most_influential_players['Composite Score'], color='orange')
plt.title('Composite Score of Most Influential Player in Each Team')
plt.xlabel('Team - Player')
plt.ylabel('Composite Score')
plt.xticks(rotation=90, ha='right')
plt.tight_layout()
plt.show()


# In[11]:


#Plot a graph dispalying the cummulative composite as per team
plt.figure(figsize=(10, 6))
plt.bar(team_table['Team'], team_table['Composite Score'], color='skyblue')
plt.title('Composite Score by Team')
plt.xlabel('Team')
plt.ylabel('Composite Score')
plt.xticks(rotation=90, ha='right')
plt.tight_layout()
plt.show()


# In[12]:


# Correlation Matrix to determine relation between Cap Salary and Team Rank
correlation_matrix = team_table[['Cap Salary', 'Rank']].corr()

# Display correlation matrix
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Correlation Matrix between Cap Salary and Rank')
plt.show()


# In[13]:


# Plot team cap salary vs. team rank as a line plot
plt.figure(figsize=(10, 6))
plt.plot(team_table['Rank'], team_table['Cap Salary'], marker='o', linestyle='-')
plt.title('Team Cap Salary vs. Team Rank')
plt.xlabel('Rank')
plt.ylabel('Cap Salary')

# custom y-axis to reduce the gap between points
plt.ylim(min(team_table['Cap Salary']) - 5000000, max(team_table['Cap Salary']) + 5000000)
plt.yticks(range(int(min(team_table['Cap Salary'])), int(max(team_table['Cap Salary'])) + 10000000, 10000000))

# Display y-axis labels as complete dollar values
plt.gca().yaxis.set_major_formatter(StrMethodFormatter('${x:,.0f}'))
plt.grid(True)
plt.show()


# In[14]:


# Plot team rank vs composite score vs cap salary
# X-axis (Rank): The rank of each team. 
# Y-axis (Composite Score): The composite score for each team.
# Size of Points (Cap Salary): The size of each point on the plot corresponds to the cap salary of the team. Larger points represent teams with higher cap salaries, while smaller points represent teams with lower cap salaries.
plt.figure(figsize=(10, 8))
plt.scatter(team_table['Rank'], team_table['Composite Score'], s=team_table['Cap Salary'] / 1000000, alpha=0.7, c='blue')
plt.title('Team Rank vs Composite Score vs Cap Salary')
plt.xlabel('Rank')
plt.ylabel('Composite Score')
plt.colorbar(label='Cap Salary (in millions)')
plt.grid(True)
plt.tight_layout()
plt.show()

