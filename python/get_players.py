import pandas as pd
import os

directory = ' matches'

all_players_df = pd.DataFrame(columns=['player_id', 'player_name', 'player_hand', 'player_height', 'player_country'])

for year in range(2010, 2024):
    file_path = os.path.join(directory, f'matches_{year}.csv')
    if os.path.exists(file_path):
        matches_df = pd.read_csv(file_path)

        winners_df = matches_df[['winner_id', 'winner_name', 'winner_hand', 'winner_ht', 'winner_ioc']].copy()
        winners_df.columns = ['player_id', 'player_name', 'player_hand', 'player_height', 'player_country']

        losers_df = matches_df[['loser_id', 'loser_name', 'loser_hand', 'loser_ht', 'loser_ioc']].copy()
        losers_df.columns = ['player_id', 'player_name', 'player_hand', 'player_height', 'player_country']

        all_players_df = pd.concat([all_players_df, winners_df, losers_df], ignore_index=True)

all_players_df.drop_duplicates(subset=['player_id'], inplace=True)

all_players_df.to_csv(' players.csv', columns=['player_id', 'player_name', 'player_hand', 'player_height', 'player_country'], index=False)
