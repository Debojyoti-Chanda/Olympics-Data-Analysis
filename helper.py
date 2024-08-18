import pandas as pd
import numpy as np


def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0,'Overall')
    return country , years
def fetch_medal(df, year, country):
   flag = 0
   medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
   if(year == 'Overall' and country == 'Overall'):
      temp_df = medal_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
   if(year == 'Overall' and country != 'Overall'):
      flag = 1
      temp_df = medal_df[medal_df['region'] == country]
   if(year != 'Overall' and country == 'Overall'):
      temp_df = medal_df[medal_df['Year'] == int(year)]
   if(year != 'Overall' and country != 'Overall'):
      temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]
   if(flag == 1):
      x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
   else:
      x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold').reset_index()
   x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
   return x
def data_over_time(df,col):
    nations_overtime = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_overtime.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)
    return nations_overtime

def most_successful(df, sport):
   temp_df = df.dropna(subset=['Medal'])
   if sport != 'Overall':
      temp_df = temp_df[temp_df['Sport'] == sport]
   x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='Name', right_on='Name', how='left')[['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')
   x.rename(columns={'count': 'Medals'}, inplace=True)
   return x
def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    final_df = temp_df.groupby('Year').count()['Medal'].reset_index()
    return final_df