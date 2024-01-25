import pandas as pd
import math

def elo_update(rating_a, rating_b, outcome_a, k=32):
    expected_a = 1 / (1 + 10**((rating_b - rating_a) / 400))
    expected_b = 1 / (1 + 10**((rating_a - rating_b) / 400))

    new_rating_a = rating_a + k * (outcome_a - expected_a)
    new_rating_b = rating_b + k * ((1 - outcome_a) - expected_b)

    return new_rating_a, new_rating_b

players_df = pd.read_csv('players_full_elo.csv')
matches_df = pd.concat([pd.read_csv(f'matches_{year}.csv') for year in range(2010, 2024)])

for surface in ['hard', 'clay', 'grass']:
    elo_col = f'player_elo_{surface}'
    if elo_col not in players_df.columns:
        players_df[elo_col] = 1000

for index, match in matches_df.iterrows():
    winner_id = match['winner_id']
    loser_id = match['loser_id']
    surface = match['surface']
    
    if surface.lower() == 'carpet':
        continue

    winner_row = players_df[players_df['player_id'] == winner_id]
    loser_row = players_df[players_df['player_id'] == loser_id]

    if not winner_row.empty and not loser_row.empty:
        winner_elo_col = f'player_elo_{surface.lower()}'
        loser_elo_col = f'player_elo_{surface.lower()}'

        winner_elo = winner_row[winner_elo_col].values[0]
        loser_elo = loser_row[loser_elo_col].values[0]

        new_winner_elo, new_loser_elo = elo_update(winner_elo, loser_elo, 1)
        players_df.loc[players_df['player_id'] == winner_id, winner_elo_col] = new_winner_elo
        players_df.loc[players_df['player_id'] == loser_id, loser_elo_col] = new_loser_elo

for surface in ['hard', 'clay', 'grass']:
    elo_col = f'player_elo_{surface}'
    players_df[elo_col] = players_df[elo_col].round(2)

for surface in ['hard', 'clay', 'grass']:
    elo_col = f'player_elo_{surface}'
    players_df.loc[players_df[elo_col] == 1000, elo_col] = None

players_df.to_csv('players_full_elo.csv', index=False)
