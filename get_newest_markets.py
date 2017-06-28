from __future__ import print_function
import requests
import pandas as pd

def get_all_summaries():
    res = requests.get('https://bittrex.com/api/v1.1/public/getmarketsummaries')
    if res.json()['success']:
        summary = res.json()['result']
        df = pd.io.json.json_normalize(summary)
        df['TimeStamp'] = pd.to_datetime(df['TimeStamp'])
        df['Created'] = pd.to_datetime(df['Created'])
        df['24hr_chg'] = df['Last'] - df['PrevDay']
        df['24hr_chg_pct'] = df['24hr_chg'] / df['PrevDay'] * 100
        return df
    else:
        print('error! ', res.json()['message'])
        return None


def show_newest(df, top=10):
    newest = df.sort_values(by='Created', ascending=False).head(10)[['MarketName', 'Created', '24hr_chg_pct']]
    print('newest coins:')
    print(newest)


if __name__=="__main__":
    df = get_all_summaries()
    show_newest(df)
