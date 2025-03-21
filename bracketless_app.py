# %%writefile app.py
# @title STREAMLIT APP
# Import libraries
import streamlit as st
import numpy as np
import pandas as pd
import requests
from datetime import date, timedelta, datetime
from zoneinfo import ZoneInfo
from json import loads
#import ipywidgets as widgets

st.title('BRACKETLESS BRACKET')

# TO UPDATE EACH YEAR: add new year, update dates
year = st.selectbox("Year", ('2025','2024','2023','2022'))

# Countdown / Entry Form Page
# TO UPDATE: When tournament starts, change this to next year
if year=='2026':
  # st.write('The entry form is coming soon!')
  st.write('The entry form is live [here](https://forms.gle/KFMU2NFERRVyx8Pp9)!')
  if date.today() >= date(2025, 3, 9): # After daylight savings time
    tourneystart = datetime(2025, 3, 20, 17, 00).astimezone(ZoneInfo('America/New_York'))
  else:
    tourneystart = datetime(2025, 3, 20, 16, 00).astimezone(ZoneInfo('America/New_York'))
  wait = tourneystart - datetime.now(ZoneInfo('America/New_York'))
  waitdays = wait.days
  waithours = int(np.floor(wait.seconds/(3600)))
  st.write('The tournament starts in about ', wait.days,' days, ', waithours, ' hours!')
  
  def get_games():
    year = '%04d' % datetime.now(ZoneInfo('America/New_York')).year
    month = '%02d' % datetime.now(ZoneInfo('America/New_York')).month
    day = '%02d' % datetime.now(ZoneInfo('America/New_York')).day 
  
    # Scrape scores from ESPN - better than Sports Reference because it's live!
    url = f"http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard?dates={year}{month}{day}"
    page = requests.get(url)
    text = page.text
    data = loads(text)
  
    matchups = [] 
    matchups_live = []
    matchups_upcoming = []
    matchups_complete = []
  
    # Go through each event that day
    for game in range(len(data.get('events'))):
      if not data.get('events')[game].get('status').get('type').get('completed'):
        if data.get('events')[game].get('status').get('type').get('description')=='Scheduled':
          matchups_upcoming.append(data.get('events')[game].get('name'))
        else:
          matchups_live.append(data.get('events')[game].get('name'))
      else:
        matchups_complete.append(data.get('events')[game].get('name'))
    
    return matchups_live, matchups_upcoming, matchups_complete
  
  matchups_live, matchups_upcoming, matchups_complete = get_games()
  
  def view_matchups(see):
    if see=='Live':
      matchups_df = pd.DataFrame(data={"Live":matchups_live})
    elif see=='Upcoming':
      matchups_df = pd.DataFrame(data={"Upcoming":matchups_upcoming})
    elif see=='Completed':
      matchups_df = pd.DataFrame(data={"Completed":matchups_complete})
    return matchups_df
  matchup_options = ['Live', 'Upcoming', 'Completed']

  def get_entrants(year):
    # TO UPDATE EACH YEAR: Form of entries
    url = st.secrets["FormURLs"]["url2025"]
    entrants_df = pd.read_csv(url, skiprows=7, header=0,
                              names=["Name"],
                              usecols=[1]).sort_values(by=["Name"])
    return entrants_df

  check = st.checkbox('Was my entry received? (Updates hourly)')
  if check:
    entrants = get_entrants(year)
    st.dataframe(entrants, hide_index=True)
  
  see = st.radio('Today\'s Games', matchup_options)
  current_matchups = view_matchups(see)
  st.dataframe(current_matchups, hide_index=True, use_container_width = True)
  
# STANDINGS PAGE FOR SELECTED YEAR (INCLUDING CURRENT)
else:
  def get_teams(year):
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSr4KwdEzYPzj2hgc0WUW26t4hrbHXlkVk7oGyrL0m01AQ1A_7nvcKYNTka9gftwWyUd9kEOXTFouPV/pub?gid=0&single=true&output=csv"
    team_list_df = pd.read_csv(url)
    # TO UPDATE EACH YEAR: TEAM LIST
    if year=='2025':
      team_list = team_list_df["Teams2025"].to_list()
    elif year=='2024': 
      team_list = team_list_df["Teams2024"].to_list()
    elif year=='2023':
      team_list = team_list_df["Teams2023"].to_list()
    elif year=='2022':
      team_list = team_list_df["Teams2022"].to_list()
  
    # Seed (assumes entered in S-Curve order)
    seed_list = np.zeros(len(team_list), dtype="int")
    for seed in range(len(seed_list)):
      seed_list[seed] = int(np.ceil((seed+1)/4))
    
    return team_list, seed_list
  
  
  def get_dates(year):
    #print(f'Today is {date.today()} at {datetime.now().strftime("%H:%M")}!')
    # TO UPDATE EACH YEAR: Dates
    if year=='2025':
      # Range of Dates
      # Dates for start of each round
      date_r64 = date(2025, 3, 20)
      date_r32 = date(2025, 3, 22)
      date_r16 = date(2025, 3, 27)
      date_r8 = date(2025, 3, 29)
      date_r4 = date(2025, 4, 5)
      date_r2 = date(2025, 4, 7)
      date_end = date_r2 + timedelta(days=1)
      
    elif year=='2024':
      # Range of Dates
      # Dates for start of each round
      date_r64 = date(2024, 3, 21)
      date_r32 = date(2024, 3, 23)
      date_r16 = date(2024, 3, 28)
      date_r8 = date(2024, 3, 30)
      date_r4 = date(2024, 4, 6)
      date_r2 = date(2024, 4, 8)
      date_end = date_r2 + timedelta(days=1)
      
    elif year=='2023':
      # Range of Dates
      # Dates for start of each round
      date_r64 = date(2023, 3, 16)
      date_r32 = date(2023, 3, 18)
      date_r16 = date(2023, 3, 23)
      date_r8 = date(2023, 3, 25)
      date_r4 = date(2023, 4, 1)
      date_r2 = date(2023, 4, 3)
      date_end = date_r2 + timedelta(days=1)
      
    elif year=='2022':
      # Dates for start of each round
      date_r64 = date(2022, 3, 17)
      date_r32 = date(2022, 3, 19)
      date_r16 = date(2022, 3, 24)
      date_r8 = date(2022, 3, 26)
      date_r4 = date(2022, 4, 2)
      date_r2 = date(2022, 4, 4)
      date_end = date_r2 + timedelta(days=1)
  
    # Create list of dates spanning whole tournament
    dates = [date_r64 + timedelta(days=n)
            for n in range((date_end-date_r64).days)]
    round_dates = [date_r64, date_r32, date_r16, date_r8, date_r4, date_r2, date_end]
  
    return dates, round_dates
  
  @st.cache_data(ttl=3600) # Update every hour
  def get_entries(year):
    # TO UPDATE EACH YEAR: Download entries
    if year=='2025':
      # url = 0
      url = st.secrets["FormURLs"]["url2025"]
    if year=='2024':
      url = st.secrets["FormURLs"]["url2024"]
    elif year=='2023':
      url = st.secrets["FormURLs"]["url2023"]
    elif year=='2022':
      url = st.secrets["FormURLs"]["url2022"]
        
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
  
    # TO UPDATE EACH YEAR
    # Any clean up
    # Drop duplicates by row number
    if year=='2025':
      entryc2_df = entry_df    
    elif year=='2024':
      entryc2_df = entry_df    
    elif year=='2023':
      entryc2_df = entry_df
    elif year=='2022':
      entryc2_df = entry_df.drop(4)
    
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
    return entryc2_df, altentry2_df, name_list, altname_list
  
  @st.cache_data(ttl=60) # Change when tourney begins; update every minute
  def get_results(year, dates, round_dates):
    date_r64, date_r32, date_r16, date_r8, date_r4, date_r2, date_end = round_dates
  
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
      data = loads(text)
  
      # Go through each event that day
      for game in range(len(data.get('events'))):
        
        # Search for completed games
        if data.get('events')[game].get('status').get('type').get('completed'):
  
          # Compare the two for the winner
          if data.get('events')[game].get('competitions')[0].get('competitors')[0].get('winner'):
            win_name = data.get('events')[game].get('competitions')[0].get('competitors')[0].get('team').get('shortDisplayName')
          elif data.get('events')[game].get('competitions')[0].get('competitors')[1].get('winner'):
            win_name = data.get('events')[game].get('competitions')[0].get('competitors')[1].get('team').get('shortDisplayName')
      
          # TO UPDATE EACH YEAR: First-four winners
          if year=='2025':
            win_name = win_name.replace("SIUE", "SIU Edwardsville")
            win_name = win_name.replace("Xavier", "Texas / Xavier")
            win_name = win_name.replace("North Carolina", "San Diego St / North Carolina")
            win_name = win_name.replace("Alabama St", "Alabama St / St Francis Pa")
            win_name = win_name.replace("Mount St Marys", "American / Mount St Marys")
            
          elif year=='2024':
            win_name = win_name.replace("Colorado", "Boise St / Colorado")
            win_name = win_name.replace("Colorado St", "Virginia / Colorado St")
            win_name = win_name.replace("Grambling", "Montana St / Grambling")
            win_name = win_name.replace("Wagner", "Howard / Wagner")
            
          elif year=='2023':
            # Adjust the name
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
          
          elif year=='2022':
            # 2022
            win_name = win_name.replace("New Mexico St", "New Mexico St.")
            win_name = win_name.replace("Miami", "Miami (FL)")
            win_name = win_name.replace("Murray St", "Murray St.")
            win_name = win_name.replace("Iowa State", "Iowa St.")
            win_name = win_name.replace("Michigan St", "Michigan St.")
            win_name = win_name.replace("Notre Dame", "Rutgers / Notre Dame")
            win_name = win_name.replace("Ohio State", "Ohio St.")
  
  
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
    return team_df
  
  def setup_alt_brackets(team_df, altentry2_df, entryc2_df):
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
      
    return altentry2_df
  
  def calculate_pts(entryc2_df, seed_list, team_df, altentry2_df):
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
  
    return entryc2_df, altentry2_df
  
  
  
  # Call the functions
  # Setup
  team_list, seed_list = get_teams(year)
  dates, round_dates = get_dates(year)
  entryc2_df, altentry2_df, name_list, altname_list = get_entries(year)
  
  # Results
  team_df = get_results(year, dates, round_dates)
  
  
  # Calculations
  altentry2_df = setup_alt_brackets(team_df, altentry2_df, entryc2_df)
  entryc2_df, altentry2_df = calculate_pts(entryc2_df, seed_list, team_df, altentry2_df)
  
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
  
  
  with st.container():
    st.header('Current standings', divider='rainbow')
    choice_group = st.selectbox('Group', group_list)
    current_standing = view_standings(choice_group)
    st.dataframe(current_standing, height=40*10, use_container_width=True)
  
  col2, col3 = st.columns(2)
  with col2:
    # st.header("",divider='rainbow')
    st.header('Individual brackets', divider='orange')
    # if year=='2022': # For testing purposes
    # Randomize the start of the list
    if 'rand_num1' not in st.session_state:
      # rand_initial = np.random.randint(0, np.size(name_list))
      # choice_name = st.selectbox('Name', name_list, index=rand_initial)
      
      st.session_state['rand_num1'] = np.random.randint(0, np.size(name_list))
      # rand_initial = st.session_state['rand_num1']
      # choice_name = st.selectbox('Name', name_list, index=rand_initial)
    
    # else:
    elif rand_initial > np.size(name_list):
      rand_initial = np.size(name_list)
      
    rand_initial = st.session_state['rand_num1']
    choice_name = st.selectbox('Name', name_list, index=rand_initial)
    current_name = view_bracket(choice_name)
    
    # else:
    # choice_name = st.selectbox('Name', name_list)
    # current_name = view_bracket(choice_name)
      
    st.dataframe(current_name, hide_index=True, height=40*16, use_container_width=True)
  
  with col3:
    st.header('Alternate brackets', divider='violet')
    if 'rand_num2' not in st.session_state:
      st.session_state['rand_num2'] = np.random.randint(0, np.size(altname_list))
      rand_initial2 = st.session_state['rand_num2']
      choice_name = st.selectbox('Name', altname_list, index=rand_initial2)
    else:
      rand_initial2 = st.session_state['rand_num2']
      choice_name = st.selectbox('Name', altname_list, index=rand_initial2)
    
    # choice_name = st.selectbox('Name', altname_list)
    current_name = view_altbracket(choice_name)
    st.dataframe(current_name, hide_index=True, height=40*16, use_container_width=True)
  
  game_check = st.checkbox('See Today\'s Matchups?')
  if game_check:
    def get_games():
      year = '%04d' % datetime.now(ZoneInfo('America/New_York')).year
      month = '%02d' % datetime.now(ZoneInfo('America/New_York')).month
      day = '%02d' % datetime.now(ZoneInfo('America/New_York')).day

      # Scrape scores from ESPN - better than Sports Reference because it's live!
      # url = f"http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard?dates=20240210"
      url = f"http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard?dates={year}{month}{day}"
      page = requests.get(url)
      text = page.text
      data = loads(text)

      matchups = []
      matchups_live = []
      matchups_upcoming = []
      matchups_complete = []

      # Go through each event that day
      for game in range(len(data.get('events'))):
        # matchup = data.get('events')[game].get('name')
        # matchups.append(matchup)
        # print(data.get('events')[game].get('status').get('type').get('name'))

        if not data.get('events')[game].get('status').get('type').get('completed'):
          if data.get('events')[game].get('status').get('type').get('description')=='Scheduled':
            matchups_upcoming.append(data.get('events')[game].get('name'))
          else:
            matchups_live.append(data.get('events')[game].get('name'))
        else:
          matchups_complete.append(data.get('events')[game].get('name'))
      # print(matchups_live)
      # print(matchups_upcoming)
      # print(matchups_complete)
      return matchups_live, matchups_upcoming, matchups_complete

    def view_matchups(see):
      if see=='Live':
        matchups_df = pd.DataFrame(data={"Live":matchups_live})
      elif see=='Upcoming':
        matchups_df = pd.DataFrame(data={"Upcoming":matchups_upcoming})
      elif see=='Completed':
        matchups_df = pd.DataFrame(data={"Completed":matchups_complete})
      return matchups_df
    
    matchups_live, matchups_upcoming, matchups_complete = get_games()
    matchup_options = ['Live', 'Upcoming', 'Completed']

    see = st.radio('Today\'s Games', matchup_options)
    current_matchups = view_matchups(see)
    st.dataframe(current_matchups, hide_index=True, use_container_width = True)
  
  st.write("Results courtesy [ESPN](%s)" % "https://www.espn.com/")
  todays = datetime.now(ZoneInfo('America/New_York'))
  st.write("Last Update: ", todays.strftime("%x"), " at ", todays.strftime("%X"))
  #st.write("Last Update: ", str(datetime.now().strftime("%H:%M")), " on ", str(date.today()))
