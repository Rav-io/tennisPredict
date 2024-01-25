

def simplified_glicko_update(player_rating, opponent_rating, player_score, k_factor=30):
    expected_score = 1 / (1 + 10 ** ((opponent_rating - player_rating) / 400))
    new_rating = player_rating + k_factor * (player_score - expected_score)
    return new_rating

def update_ratings_for_matches(dataframe, player_ratings, initial_rating=1500):
    for index, row in dataframe.iterrows():
        player1_id = row['player1_id']
        player2_id = row['player2_id']
        winner = row['winner']
        player1_rating = player_ratings.get(player1_id, initial_rating)
        player2_rating = player_ratings.get(player2_id, initial_rating)
        player1_score = 1 if winner == 'player1' else 0
        player2_score = 1 - player1_score
        updated_player1_rating = simplified_glicko_update(player1_rating, player2_rating, player1_score)
        updated_player2_rating = simplified_glicko_update(player2_rating, player1_rating, player2_score)
        dataframe.at[index, 'player_1_glicko'] = updated_player1_rating
        dataframe.at[index, 'player_2_glicko'] = updated_player2_rating
        player_ratings[player1_id] = updated_player1_rating
        player_ratings[player2_id] = updated_player2_rating
    return dataframe

player_ratings_dict = {}

for df in dataframes:
    df = update_ratings_for_matches(df, player_ratings_dict)

dataframes[0].head()
