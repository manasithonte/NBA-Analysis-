**Project Name:** Analyzing National Basketball Association Player
Performance, Team Success, and Salary.

**Objective:**

The goal is to analyze the player performance by computing a composite
score based on advance metrics and eventually determining their ranks.
The composite score could also be calculated for each team and its
correlation with the team rank is determined. The relation of team Cap
Salary and team success is also determined.

**Install Dependencies:**

\`\`\`

pip install -r requirements.txt

\`\`\`

The third dataset is taken from kaggle and saved as csv in data/raw
folder as nba_data_processed.csv

**How to run the code:**

**a)** Use get_data.py script to get the required data in the form of
three datasets ( team_table, players_data, salary) and store the data
files in data/raw folder.

**b)** Use the clean_data.py script to remove discrepancies in the
datasets and save those datasets in the data/processed folder

**c)** Use the integrate_data.py script to merge the team_table and
salary_data and save the made changes in the team_table csv file in the
data/processed folder.

**d)** Use the analyze_visualize.py script to perform
computation on player data to get a composite score, and then computing
the cumulative composite score for the teams. The **merge_data**
function is used here to merge the computed composite score for the team
using the player data with team_table dataset. The **merge_data**
function is used by importing the **integrate_data.py** script.
