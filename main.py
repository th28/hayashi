
#Simple script to calculate covid19 cases per 100,000 for last two weeks in Japan.
#Posts result to twitter. 

import pandas as pd
import tweepy
from config import *

def main():

    auth = tweepy.OAuthHandler(
        twitter_auth_keys['api_key'],
        twitter_auth_keys['api_secret']
    )
    auth.set_access_token(
        twitter_auth_keys['access_token'],
        twitter_auth_keys['access_token_secret']
    )

    api = tweepy.API(auth)

    url = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"

    df = pd.read_csv(url)
    df = df[df.countryterritoryCode == 'JPN']
    df.rename(columns={'dateRep':'date', 'Cumulative_number_for_14_days_of_COVID-19_cases_per_100000':'COVID-19 Cases per 100000 in Japan'},inplace=True)
    df = df[['date','COVID-19 Cases per 100000 in Japan']]
    df.dropna(inplace=True)
    df['date'] = pd.to_datetime(df['date'],format='%d/%m/%Y')
    today = str(df.iloc[0].values[0].date())
    df.set_index('date',inplace=True)

    ax = df.plot()
    ax.axhline(y=25, color='r', linestyle='--')
    ax.set_title('Cases per 100,000 (past 2 weeks) as of '+ today + ': ' + str(df.iloc[0].values[0]) )
    ax.set_xlabel(" ")
    ax.set_ylabel('Cases per 100,000 (past 2 weeks)')
    fig = ax.get_figure()
    fig.savefig('jpn_covid_' + today + '.png',dpi=300)

    txt = (" COVID-19 cases per 100,000 people were recorded in Japan in the past 14 days."
    " The Finnish government permits leisure travel between Finland and Japan when this number is below 25.")

    comment = 'As of today ' + str(df.iloc[0].values[0]) + txt

    status = api.update_with_media(filename='jpn_covid_' + today + '.png', status=comment)

if __name__ == "__main__":
    main()
