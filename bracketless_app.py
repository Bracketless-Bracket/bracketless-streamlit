%%writefile app.py

#@title STREAMLIT APP
# Import libraries
import streamlit as st
import numpy as np
import pandas as pd

from datetime import date, timedelta
import requests
#import json
#import ipywidgets as widgets

st.title('BRACKETLESS BRACKET 2024')

# Teams
team_list = [
    "Alabama",
    "Houston",
    "Kansas",
    "Purdue",

    "UCLA",
    "Texas",
    "Arizona",
    "Marquette",

    "Baylor",
    "Gonzaga",
    "Kansas St.",
    "Xavier",

    "UConn",
    "Tennessee",
    "Indiana",
    "Virginia",

    "San Diego St.",
    "Duke",
    "Saint Mary's",
    "Miami",

    "Iowa St.",
    "Creighton",
    "Kentucky",
    "TCU",

    "Texas A&M",
    "Michigan St.",
    "Missouri",
    "Northwestern",

    "Memphis",
    "Arkansas",
    "Maryland",
    "Iowa",

    # 9 Seeds
    "Florida Atlantic",
    "West Virginia",
    "Auburn",
    "Illinois",

    "Boise St.",
    "Penn St.",
    "USC",
    "Utah St.",

    "NC State",
    "Providence",
    "Mississippi St. / Pittsburgh",
    "Arizona St. / Nevada",

    "Charleston",
    "Oral Roberts",
    "Drake",
    "VCU",

    "Kent St.",
    "Iona",
    "Furman",
    "Louisiana",

    "Kennesaw St.",
    "UCSB",
    "Grand Canyon",
    "Montana St.",

    "Vermont",
    "Colgate",
    "Princeton",
    "UNC-Asheville",

    "Northern Kentucky",
    "Howard",
    "Texas A&M-CC / SE Missouri St.",
    "Texas Southern / Fairleigh Dickinson"
]

# Seed (assumes entered in S-Curve order)
seed_list = np.zeros(len(team_list), dtype="int")
for seed in range(len(seed_list)):
  seed_list[seed] = int(np.ceil((seed+1)/4))



# Range of Dates
print(f'Today is {date.today()}!')

# Dates for start of each round
date_r64 = date(2023, 3, 16)
date_r32 = date(2023, 3, 18)
date_r16 = date(2023, 3, 23)
date_r8 = date(2023, 3, 25)
date_r4 = date(2023, 4, 1)
date_r2 = date(2023, 4, 3)
date_end = date_r2 + timedelta(days=1)
# date_end = date_r32

# Create list of dates spanning whole tournament
dates = [date_r64 + timedelta(days=n)
         for n in range((date_end-date_r64).days)]


# Download entries
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRY2W5rB38deW_-u5CN58qVPhD34RAe1nsbAdDCj6SGfryh5k-21Rwyv7vSS3DrEpir_XBFUs29iPfQ/pub?gid=0&single=true&output=csv"

entry_df = pd.read_csv(url, skiprows=7, header=0,
                       names=["Name", "Affiliation", "Seed 1", "Seed 2",
                              "Seed 3", "Seed 4", "Seed 5", "Seed 6",
                              "Seed 7", "Seed 8", "Seed 9", "Seed 10",
                              "Seed 11", "Seed 12", "Seed 13", "Seed 14",
                              "Seed 15", "Seed 16"],
                       usecols=[1, 2, 3, 4, 5, 6,
                                7, 8, 9, 10, 11, 12,
                                13, 14, 15, 16, 17, 18])
# Alternate brackets
altentry_df = pd.read_csv(url, skiprows=0, nrows=7, header=0,
                       names=["Name", "Affiliation", "Seed 1", "Seed 2",
                              "Seed 3", "Seed 4", "Seed 5", "Seed 6",
                              "Seed 7", "Seed 8", "Seed 9", "Seed 10",
                              "Seed 11", "Seed 12", "Seed 13", "Seed 14",
                              "Seed 15", "Seed 16"],
                       usecols=[1, 2, 3, 4, 5, 6,
                                7, 8, 9, 10, 11, 12,
                                13, 14, 15, 16, 17, 18])

# Any clean up
# Drop duplicates by row number
# entryc2_df = entry_df.drop(4)
entryc2_df = entry_df
altentry2_df = altentry_df
altentry2_df.loc[:,"Affiliation"] = "Alternate"
altentry2_df.loc[8] = ["Best", "Alternate", "x", "x", "x", "x", "x", "x", "x", "x", 
                       "x", "x", "x", "x", "x", "x", "x", "x"]
altentry2_df.loc[9] = ["Worst", "Alternate", "x", "x", "x", "x", "x", "x", "x", "x", 
                       "x", "x", "x", "x", "x", "x", "x", "x"]
altentry2_df.loc[10] = ["Most Popular", "Alternate", "x", "x", "x", "x", "x", "x", "x", "x", 
                       "x", "x", "x", "x", "x", "x", "x", "x"]
altentry2_df.loc[11] = ["Least Popular", "Alternate", "x", "x", "x", "x", "x", "x", "x", "x", 
                       "x", "x", "x", "x", "x", "x", "x", "x"]

name_list = entryc2_df.loc[:, 'Name'].sort_values().tolist()
altname_list = altentry2_df.loc[:, 'Name'].sort_values().tolist()


# Scrape results
# Create blank lists outside of loop
winners_list64 = []
winners_list32 = []
winners_list16 = []
winners_list8 = []
winners_list4 = []
winners_list2 = []

for d in range(len(dates)):

  # Get the json content of the webpage - pulled from ESPN
  # Force the string format to be two digits
  month = '%02d' % dates[d].month
  day = '%02d' % dates[d].day
  year = '%04d' % dates[d].year

  # Scrape scores from ESPN - better than Sports Reference because it's live!
  url = f"http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard?dates={year}{month}{day}"
  page = requests.get(url)
  text = page.text
  data = json.loads(text)

  # Go through each event that day
  for game in range(len(data.get('events'))):

    # Search for completed games
    if data.get('events')[game].get('status').get('type').get('completed'):

      # Compare the two for the winner
      if data.get('events')[game].get('competitions')[0].get('competitors')[0].get('winner'):
        win_name = data.get('events')[game].get('competitions')[0].get('competitors')[0].get('team').get('shortDisplayName')
      elif data.get('events')[game].get('competitions')[0].get('competitors')[1].get('winner'):
        win_name = data.get('events')[game].get('competitions')[0].get('competitors')[1].get('team').get('shortDisplayName')

      # Adjust the name
      # # 2022
      # win_name = win_name.replace("St. Peter's", "Saint Peter's")
      # win_name = win_name.replace("UNC", "North Carolina")
      # win_name = win_name.replace("New Mexico State", "New Mexico St.")
      # win_name = win_name.replace("New Mexico St", "New Mexico St.")

      # win_name = win_name.replace("Miami", "Miami (FL)")
      # win_name = win_name.replace("Murray State", "Murray St.")

      # win_name = win_name.replace("Iowa State", "Iowa St.")
      # win_name = win_name.replace("Michigan State", "Michigan St.")
      # win_name = win_name.replace("Notre Dame", "Rutgers / Notre Dame")
      # win_name = win_name.replace("Ohio State", "Ohio St.")

      # 2023
      win_name = win_name.replace("Arizona St", "Arizona St. / Nevada")
      win_name = win_name.replace("Boise St", "Boise St.")
      win_name = win_name.replace("FAU", "Florida Atlantic")
      win_name = win_name.replace("Fair Dickinson", "Texas Southern / Fairleigh Dickinson")
      win_name = win_name.replace("Iowa State", "Iowa St.")
      win_name = win_name.replace("Kansas St", "Kansas St.")
      win_name = win_name.replace("Kennesaw St", "Kennesaw St.")
      win_name = win_name.replace("Kent State", "Kent St.")
      win_name = win_name.replace("Michigan St", "Michigan St.")
      win_name = win_name.replace("Montana St", "Montana St.")
      win_name = win_name.replace("N Kentucky", "Northern Kentucky")
      win_name = win_name.replace("Penn State", "Penn St.")
      win_name = win_name.replace("Pitt", "Mississippi St. / Pittsburgh")
      win_name = win_name.replace("San Diego St", "San Diego St.")
      win_name = win_name.replace("Texas A&M-CC", "Texas A&M-CC / SE Missouri St.")
      win_name = win_name.replace("UNC Asheville", "UNC-Asheville")
      win_name = win_name.replace("Utah State", "Utah St.")


      # Place winner in correct round based on date
      if dates[d] < date_r32:
        winners_list64.append(win_name)
      elif dates[d] >= date_r32 and dates[d] < date_r16:
        winners_list32.append(win_name)
      elif dates[d] >= date_r16 and dates[d] < date_r8:
        winners_list16.append(win_name)
      elif dates[d] >= date_r8 and dates[d] < date_r4:
        winners_list8.append(win_name)
      elif dates[d] >= date_r4 and dates[d] < date_r2:
        winners_list4.append(win_name)
      elif dates[d] >= date_r2 and dates[d] <= date_end:
        winners_list2.append(win_name)


# Finish putting into dataframe
wins_rd64 = np.zeros(64, dtype="int")
wins_rd32 = np.zeros(64, dtype="int")
wins_rd16 = np.zeros(64, dtype="int")
wins_rd8 = np.zeros(64, dtype="int")
wins_rd4 = np.zeros(64, dtype="int")
wins_rd2 = np.zeros(64, dtype="int")

# Only keep teams in the NCAA tourney (in case other games going on)
match64 = set(team_list).intersection(winners_list64)
match32 = set(team_list).intersection(winners_list32)
match16 = set(team_list).intersection(winners_list16)
match8 = set(team_list).intersection(winners_list8)
match4 = set(team_list).intersection(winners_list4)
match2 = set(team_list).intersection(winners_list2)


# Get the indices of matching teams, then change value to a 1
win_index64 = [team_list.index(n) for n in match64]
win_index32 = [team_list.index(n) for n in match32]
win_index16 = [team_list.index(n) for n in match16]
win_index8 = [team_list.index(n) for n in match8]
win_index4 = [team_list.index(n) for n in match4]
win_index2 = [team_list.index(n) for n in match2]

wins_rd64[win_index64] = 1
wins_rd32[win_index32] = 1
wins_rd16[win_index16] = 1
wins_rd8[win_index8] = 1
wins_rd4[win_index4] = 1
wins_rd2[win_index2] = 1



# Combine into single array
wins_list = np.zeros((len(team_list), 6), dtype="int")
wins_list[:, 0] = wins_rd64
wins_list[:, 1] = wins_rd32
wins_list[:, 2] = wins_rd16
wins_list[:, 3] = wins_rd8
wins_list[:, 4] = wins_rd4
wins_list[:, 5] = wins_rd2

wins_tot = np.sum(wins_list, axis=1)

# Points Multiplier
pts_list = np.zeros(len(team_list), dtype="int")
for pts in range(len(pts_list)):
  pts_list[pts] = 90 + 10 * seed_list[pts]

pts_tot = pts_list * wins_tot

team_df = pd.DataFrame(data={"Team": team_list,
                             "Total Points": pts_tot,
                             "Seed": seed_list,
                             "Points per Win": pts_list, "Total Wins": wins_tot,
                             "R64": wins_list[:,0], "R32": wins_list[:,1],
                             "R16": wins_list[:,2], "R8": wins_list[:,3],
                             "R4": wins_list[:,4], "R2": wins_list[:,5]})


# Calculate best, worst, most popular, least popular
for seed in range(16):
  best = max(team_df.loc[team_df["Seed"]==(seed+1), "Total Points"])
  high = team_df.loc[(team_df["Seed"]==(seed+1)) & 
                     (team_df["Total Points"]==best), "Team"]
  altentry2_df.loc[8, "Seed " + str(seed+1)] = high.values[0]

  worst = min(team_df.loc[team_df["Seed"]==(seed+1), "Total Points"])
  low  = team_df.loc[(team_df["Seed"]==(seed+1)) & 
                     (team_df["Total Points"]==worst), "Team"]
  altentry2_df.loc[9, "Seed " + str(seed+1)] = low.values[0]

  altentry2_df.loc[10, "Seed " + str(seed+1)] = entryc2_df["Seed "+ str(seed+1)].value_counts().idxmax()
  altentry2_df.loc[11, "Seed " + str(seed+1)] = entryc2_df["Seed "+ str(seed+1)].value_counts().idxmin()

# Calculate total points
seed_pts = np.zeros((len(entryc2_df), max(seed_list)), dtype="int")
for name in range(len(entryc2_df)):

  # Go through list of entries
  name_temp = entryc2_df.iloc[name, :]

  for pick in range(max(seed_list)):

    # For each entry, choose their pick for each seed
    team_temp = name_temp["Seed " + str(pick+1)]

    # (1) Match the pick to the team list dataframe,
    # (2) Return the total points column,
    # (3) Strip away index
    pts_temp = team_df.loc[team_df["Team"]==team_temp,
                           "Total Points"].iloc[0]
    seed_pts[name, pick] = pts_temp

entryc2_df["Points"] = np.sum(seed_pts, axis=1)

# Calculate total points for first x alternate entries (entered)
seed_pts = np.zeros((len(altentry2_df), max(seed_list)), dtype="int")
for name in range(len(altentry2_df)):

  # Go through list of entries
  name_temp = altentry2_df.iloc[name, :]

  for pick in range(max(seed_list)):

    # For each entry, choose their pick for each seed
    team_temp = name_temp["Seed " + str(pick+1)]

    # (1) Match the pick to the team list dataframe,
    # (2) Return the total points column,
    # (3) Strip away index
    pts_temp = team_df.loc[team_df["Team"]==team_temp,
                           "Total Points"].iloc[0]
    seed_pts[name, pick] = pts_temp

altentry2_df["Points"] = np.sum(seed_pts, axis=1)


altentry2_df.loc[12] = ["Expected Value", "Alternate", "x", "x", "x", "x", "x", "x", "x", "x", 
                       "x", "x", "x", "x", "x", "x", "x", "x", 0]
avg_sum = 0
for seed in range(16):
  avg = np.mean(team_df.loc[team_df["Seed"]==(seed+1), "Total Points"])
  avg_sum = avg + avg_sum
altentry2_df.loc[12, "Points"] = round(avg_sum)

# View standings
def view_standings(group):
  # # This all works:
  # Return names and points in a sorted list (also hides the index column)
  print(group)

  if group=='Overall':
    standings = entryc2_df.sort_values(by=["Points"], ascending=False,
                                       ignore_index=True)[["Name", "Points"]]#.to_string(index=False)
    standings.index += 1

  elif group=='Alternate':
    standings = altentry2_df.loc[altentry2_df["Affiliation"]==group].sort_values(by=["Points"],
                                                                      ascending=False,
                                                                      ignore_index=True)[["Name", "Points"]]#.to_string(index=False)
    standings.index += 1

  # print(overall)
  # overall
  else:
    standings = entryc2_df.loc[entryc2_df["Affiliation"]==group].sort_values(by=["Points"],
                                                                             ascending=False,
                                                                             ignore_index=True)[["Name", "Points"]]#.to_string(index=False)
    standings.index += 1

  return standings

group_list = ['Overall', 'Goshen', 'Champaign-Urbana', 'Harrisonburg', 'Alternate']
#widgets.interact(view_standings, group=group_list);

col1, col2, col3 = st.columns(3)
with col1:
  st.header('Current standings', divider='blue')
  choice_group = st.selectbox('Group', group_list)
  current_standing = view_standings(choice_group)
  st.dataframe(current_standing, height=38*len(current_standing))


# View individual brackets
def view_bracket(name):
  # Return specific bracket
  bracket = name
  name_temp = entryc2_df[entryc2_df["Name"]==bracket].squeeze()
  seed_col = np.zeros(16, dtype="int")
  wins_col = np.zeros(16, dtype="int")
  pts_col = np.zeros(16, dtype="int")

  for pick in range(max(seed_list)):
    team_temp = name_temp["Seed " + str(pick+1)]
    wins_temp = team_df.loc[team_df["Team"]==team_temp,
                            "Total Wins"].iloc[0]
    wins_col[pick] = wins_temp

    pts_temp = team_df.loc[team_df["Team"]==team_temp,
                           "Total Points"].iloc[0]
    pts_col[pick] = pts_temp
    seed_col[pick] = int(pick+1)

  bracket_list = entryc2_df[entryc2_df["Name"]==bracket].drop(columns=["Affiliation", "Points"]).T.values.ravel()
  wins_col = np.insert(wins_col, 0, np.sum(wins_col))
  pts_col = np.insert(pts_col, 0, np.sum(pts_col))
  seed_col = np.insert(seed_col, 0, 0)
  combined = pd.DataFrame(data={"Seed":seed_col, "Name":bracket_list,
                                "Wins":wins_col, "Points":pts_col})#.to_string(index=False)
  combined.iloc[0,0] = ""

  return combined

#widgets.interact(view_bracket, name=name_list);

# View alternate brackets
def view_altbracket(name):
  # Return specific bracket
  bracket = name
  name_temp = altentry2_df[altentry2_df["Name"]==bracket].squeeze()
  seed_col = np.zeros(16, dtype="int")
  wins_col = np.zeros(16, dtype="int")
  pts_col = np.zeros(16, dtype="int")

  for pick in range(max(seed_list)):
    team_temp = name_temp["Seed " + str(pick+1)]
    wins_temp = team_df.loc[team_df["Team"]==team_temp,
                            "Total Wins"].iloc[0]
    wins_col[pick] = wins_temp

    pts_temp = team_df.loc[team_df["Team"]==team_temp,
                           "Total Points"].iloc[0]
    pts_col[pick] = pts_temp
    seed_col[pick] = int(pick+1)

  bracket_list = altentry2_df[altentry2_df["Name"]==bracket].drop(columns=["Affiliation", "Points"]).T.values.ravel()
  wins_col = np.insert(wins_col, 0, np.sum(wins_col))
  pts_col = np.insert(pts_col, 0, np.sum(pts_col))
  seed_col = np.insert(seed_col, 0, 0)
  combined = pd.DataFrame(data={"Seed":seed_col, "Name":bracket_list,
                                "Wins":wins_col, "Points":pts_col})#.to_string(index=False)
  combined.iloc[0,0] = ""

  return combined

#widgets.interact(view_altbracket, name=altname_list);

with col2:
  # st.header("",divider='rainbow')
  st.header('Individual brackets', divider='rainbow')
  choice_name = st.selectbox('Name', name_list)
  current_name = view_bracket(choice_name)
  st.dataframe(current_name, hide_index=True, height=38*17)

with col3:
  st.header('Alternate brackets', divider='rainbow')
  choice_name = st.selectbox('Name', altname_list)
  current_name = view_altbracket(choice_name)
  st.dataframe(current_name, hide_index=True, height=38*17)
