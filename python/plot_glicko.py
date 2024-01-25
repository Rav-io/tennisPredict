import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import seaborn as sns
import io
import base64

sns.set(style="whitegrid")

def preprocess_data(file_path):
    df = pd.read_csv(file_path)
    df['tourney_date'] = pd.to_datetime(df['tourney_date'], format='%Y%m%d')
    df1 = df[['player1_id', 'tourney_date', 'player_1_glicko']].rename(columns={'player1_id': 'player_id', 'player_1_glicko': 'glicko'})
    df2 = df[['player2_id', 'tourney_date', 'player_2_glicko']].rename(columns={'player2_id': 'player_id', 'player_2_glicko': 'glicko'})
    combined_df = pd.concat([df1, df2])
    combined_df = combined_df.sort_values(by=['player_id', 'tourney_date', 'glicko']).groupby(['player_id', 'tourney_date']).last().reset_index()
    return combined_df

def plot_glicko_history(player_id, player_name):
    all_data = pd.DataFrame()
    for year in range(2010, 2024):
        file_path = f' python/matches_containing_glicko/balanced_matches_{year}.csv'
        yearly_data = preprocess_data(file_path)
        all_data = pd.concat([all_data, yearly_data])
    
    player_data = all_data[all_data['player_id'] == player_id].sort_values(by='tourney_date')
    plt.figure(figsize=(12, 6))
    if len(player_data) > 1:
        sns.lineplot(x=player_data['tourney_date'], y=player_data['glicko'], color='b')
    elif len(player_data) == 1:
        plt.scatter(player_data['tourney_date'], player_data['glicko'], color='b')
    else:
        plt.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
        plt.gca().set_xticks([])
        plt.gca().set_yticks([])
        return None

    plt.title(f'Glicko History for {player_name}', fontsize=14)
    plt.xlabel('Tournament Date', fontsize=12)
    plt.ylabel('Glicko Rating', fontsize=12)

    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return image_base64

