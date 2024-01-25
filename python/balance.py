import pandas as pd
import random

file_path = 'matches_2010_w.csv'
df = pd.read_csv(file_path)

columns_to_exchange = ['player1_id', 'player2_id', 'player1_rank', 'player2_rank',
                        'player1_rank_points', 'player2_rank_points', 'player1_elo', 'player2_elo']

def exchange_columns(row):
    if random.random() > 0.5:
        row['player1_id'], row['player2_id'] = row['player2_id'], row['player1_id']
        row['player1_rank'], row['player2_rank'] = row['player2_rank'], row['player1_rank']
        row['player1_rank_points'], row['player2_rank_points'] = \
        row['player2_rank_points'], row['player1_rank_points']
        row['player1_elo'], row['player2_elo'] = row['player2_elo'], row['player1_elo']
        row['winner'] = 'player2' if row['winner'] == 'player1' else 'player1'
    return row

df_exchanged = df.apply(exchange_columns, axis=1)


output_file_path = 'asd.csv'
df_exchanged.to_csv(output_file_path, index=False)

print(f'Columns exchanged successfully. Output saved to {output_file_path}')
