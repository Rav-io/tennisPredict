import pandas as pd
import math

def elo_update(rating_a, rating_b, outcome_a, k=32):
    expected_a = 1 / (1 + 10**((rating_b - rating_a) / 400))
    expected_b = 1 / (1 + 10**((rating_a - rating_b) / 400))
    new_rating_a = rating_a + k * (outcome_a - expected_a)
    new_rating_b = rating_b + k * ((1 - outcome_a) - expected_b)
    return new_rating_a, new_rating_b

players_df = pd.read_csv(' players.csv')
matches_df = pd.concat([pd.read_csv(f' python/matches/matches_{year}.csv') for year in range(2010, 2024)])

players_df['player_elo'] = 1000
players_df['player_peak_elo'] = 0

for index, match in matches_df.iterrows():
    winner_id = match['winner_id']
    loser_id = match['loser_id']
    winner_row = players_df[players_df['player_id'] == winner_id]
    loser_row = players_df[players_df['player_id'] == loser_id]
    if not winner_row.empty and not loser_row.empty:
        winner_elo = winner_row['player_elo'].values[0]
        loser_elo = loser_row['player_elo'].values[0]
        new_winner_elo, new_loser_elo = elo_update(winner_elo, loser_elo, 1)
        players_df.loc[players_df['player_id'] == winner_id, 'player_elo'] = new_winner_elo
        players_df.loc[players_df['player_id'] == loser_id, 'player_elo'] = new_loser_elo
        players_df.loc[players_df['player_id'] == winner_id, 'player_peak_elo'] = max(new_winner_elo, 
        players_df.loc[players_df['player_id'] == winner_id, 'player_peak_elo'].values[0])
        players_df.loc[players_df['player_id'] == loser_id, 'player_peak_elo'] = max(new_loser_elo, 
        players_df.loc[players_df['player_id'] == loser_id, 'player_peak_elo'].values[0])

players_df['player_elo'] = players_df['player_elo'].round(2)
players_df['player_peak_elo'] = players_df['player_peak_elo'].round(2)

players_df.sort_values(by='player_elo', ascending=False, inplace=True)

players_df.to_csv(' xd.csv', columns=['player_id', 'player_name', 'player_elo', 'player_peak_elo'], index=False)
