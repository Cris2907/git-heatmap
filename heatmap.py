#!/usr/bin/env python
# coding: utf-8

# # Importing libraries

# In[1]:


import pandas as pd
import csv
import datetime as dt
import seaborn as sns
import os
import requests
from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv
load_dotenv()  # This loads the .env file into environment variables


# # API

# In[2]:


import requests
import os

token = os.getenv("TOKEN")  # or hardcode it (not recommended)
username = os.getenv("USERNAME")  # or hardcode it (not recommended)
print(token)
print(username)
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github+json"
}

url = "https://api.github.com/user/repos"
params = {"per_page": 100, "page": 1}

response = requests.get(url, headers=headers, params=params)
codespaces = [] 
if response.status_code == 200:
    repos = response.json()
    for repo in repos:
        codespaces.append({
            "name": repo["name"],
            "private": repo["private"],
            "created_at": repo["created_at"],
            "updated_at": repo["updated_at"],
            "pushed_at": repo["pushed_at"],
            "url": repo["html_url"]
        })
else:
    print("Error:", response.status_code, response.text)
    
codespaces = pd.DataFrame(codespaces) 


# In[3]:


url_template = f"https://api.github.com/repos/{username}/"  
gmt_offset = timezone(timedelta(hours=-5))  # GMT-5

print(url_template)


headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github+json"
}



page = 1
commits = []

for _, codespace in codespaces.iterrows():
    name = codespace["name"]
    print(f"\nFetching commits for repo: {name}")
    
    page = 1
    while True:
        print(f"  Page {page}")
        url = f"{url_template}{name}/commits"
        params = {
            "author": "Cris2907",
            "per_page": 100,
            "page": page
        }

        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print("  Error:", response.status_code, response.text)
            break

        data = response.json()
        if not data:
            print("  No more commits.")
            break

        
        for commit in data:
            iso_timestamp = commit["commit"]["author"]["date"]
            dt_utc = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
            dt_local = dt_utc.astimezone(gmt_offset)

            commit_date = dt_local.date()
            commit_time = dt_local.time()

            commits.append({
                "repo": name,
                "date": commit_date,
                "time": commit_time,
                "message": commit["commit"]["message"],
            })

        page += 1


commits = pd.DataFrame(commits)

commits.to_csv("commits.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)


# # Importing Files

# In[4]:


hour_order = [
    '12AM', '1AM', '2AM', '3AM', '4AM', '5AM',
    '6AM', '7AM', '8AM', '9AM', '10AM', '11AM',
    '12PM', '1PM', '2PM', '3PM', '4PM', '5PM',
    '6PM', '7PM', '8PM', '9PM', '10PM', '11PM'
]

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


commits['date'] = pd.Categorical(commits['date'], categories=day_order, ordered=True)
commits['time'] = pd.Categorical(commits['time'], categories=hour_order, ordered=True)

full_grid = pd.DataFrame(
    [(d, h) for d in day_order for h in hour_order],
    columns=['date', 'time']
)

full_grid.info()


# In[ ]:





# In[5]:


# Read the CSV file into a DataFrame
commits = pd.read_csv('commits.csv')

commits = commits.astype({'date': 'datetime64[ns]', 'time': 'datetime64[ns]'}, errors='ignore')
commits['floored_hour'] =commits['time'].dt.floor('H').dt.time
commits.drop(columns=['time', 'repo'], inplace=True)
first_commit = commits['date'].min()
last_commit = commits['date'].max() 
print(f"First commit: {first_commit}")
print(f"Last commit: {last_commit}")

all_dates = pd.date_range(start=first_commit, end=last_commit)
weekday_counts = all_dates.to_series().dt.day_name().value_counts().to_dict()
print(weekday_counts)
commits = commits.groupby(['date', 'floored_hour']).size().reset_index(name='commits')
commits = commits.rename(columns={'floored_hour': 'time'}, inplace=False)
commits['date'] =  commits['date'].dt.day_name()
commits['day_count'] = commits['date'].map(weekday_counts)
commits['time'] = pd.to_datetime(commits['time'], format='%H:%M:%S').dt.strftime('%-I%p')  
commits = full_grid.merge(commits, on=['date', 'time'], how='left').fillna(0)
commits = commits.astype({'date': 'category', 'time': 'category', 'day_count':'int', 'commits':'int'}, errors='ignore')
# commits = commits.groupby(['date', 'time']).agg({'commits': 'mean'}).reset_index().rename(columns={'commits': 'avg_commits'})
commits['avg_commits'] = commits['commits'] / commits['day_count']
commits['avg_commits'] = commits['avg_commits'].fillna(0)

commits.to_csv('commits_by_date_processed.csv', index=False)

# commits.to_csv('commits_by_date_processed.csv', index=False)



# In[6]:


commits.to_csv('commits_by_date_processed.csv', index=False)


# In[7]:


commits['avg_commits'] = commits['avg_commits'].astype(float)


commits['date'] = pd.Categorical(commits['date'], categories=day_order, ordered=True)
commits['time'] = pd.Categorical(commits['time'], categories=hour_order, ordered=True)

# Optional: just to visually confirm order before pivoting
commits = commits.sort_values(['date', 'time'])
commits.to_csv('commits_by_date_processed.csv', index=False)


# # Plotting data

# In[8]:


commits = commits.groupby(['date', 'time'], as_index=False).agg({'avg_commits': 'mean'})


# In[9]:


commits = commits.pivot(index='date', columns='time', values='avg_commits').fillna(0).astype(float)


# In[10]:


commits


# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context("notebook", font_scale=1.1)  # Options: paper, notebook, talk, poster

plt.figure(figsize=(16, 9))  # Play with width/height to get the size you like


plt.title('Average Commits by Day and Hour', fontsize=16, weight='bold', pad=20)
plt.xlabel('Hour of Day', fontsize=12, labelpad=10)
plt.ylabel('Day of Week', fontsize=12, labelpad=10)

sns.heatmap(
    commits,
    annot=True,
    fmt=".1f",
    cmap="YlGnBu",
    linewidths=0.5,
    linecolor='none',
    cbar=True,
    square=True,
    xticklabels=True,
    yticklabels=True,
    annot_kws={"size": 8},
    cbar_kws={'label': 'Commits'}
).set(title='Average Commits by Day and Hour', xlabel='Hour of Day', ylabel='Day of Week')



plt.tight_layout()
plt.savefig('commit_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()


# In[ ]:



