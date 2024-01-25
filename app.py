from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import pandas as pd
import python.test_rank_hyper
import python.test_rank
import python.test_elo
import python.test_elo_hyper
import python.glicko_counter
import python.test_glicko
import python.test_glicko_hyper
import python.plot_glicko
import python.plot_elo
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


app = Flask(__name__)
CORS(app)
engine = create_engine('mssql+pyodbc://localhost/tennis?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes')

players_df = pd.read_sql('SELECT * FROM players', engine)
player_elos_df = pd.read_sql('SELECT * FROM player_elos', engine)

player_data = list(zip(player_elos_df['player_id'], players_df['player_name'], players_df['player_country']))

@app.route('/predict', methods=['POST'])
def predict():
        if request.method == 'POST':
            data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        player1_id = data['player1_id']
        player2_id = data['player2_id']
        surface = data['surface']
        model = data['model']
        elo_calculated_using_surface = True

        query_player1 = f"SELECT player_elo_{surface.lower()} as player_elo FROM player_elos WHERE player_id = {player1_id}"
        query_player2 = f"SELECT player_elo_{surface.lower()} as player_elo FROM player_elos WHERE player_id = {player2_id}"

        player1_elo_df = pd.read_sql(query_player1, engine)
        player2_elo_df = pd.read_sql(query_player2, engine)

        if player1_elo_df.empty or player2_elo_df.empty:
            return jsonify({'error': 'Player ELO rating not found'}), 404

        player1_elo = player1_elo_df['player_elo'].values[0]
        player2_elo = player2_elo_df['player_elo'].values[0]
        
        if player1_elo is None or player2_elo is None:
            elo_calculated_using_surface = False
            query_player1 = f"SELECT player_elo FROM player_elos WHERE player_id = {player1_id}"
            query_player2 = f"SELECT player_elo FROM player_elos WHERE player_id = {player2_id}"
            player1_elo_df = pd.read_sql(query_player1, engine)
            player2_elo_df = pd.read_sql(query_player2, engine)
            player1_elo = player1_elo_df['player_elo'].values[0]
            player2_elo = player2_elo_df['player_elo'].values[0]

        prob_player1_wins = 1 / (1 + 10**((player2_elo - player1_elo) / 400))
        prob_player2_wins = 1 / (1 + 10**((player1_elo - player2_elo) / 400))

        total_prob = prob_player1_wins + prob_player2_wins
        normalized_prob_player1 = round((prob_player1_wins / total_prob) * 100, 2)
        normalized_prob_player2 = round((prob_player2_wins / total_prob) * 100, 2)
        
        player1_name = players_df.loc[players_df['player_id'] == player1_id, 'player_name'].values[0]
        player2_name = players_df.loc[players_df['player_id'] == player2_id, 'player_name'].values[0]
        
        query_player1_rank = f"SELECT rank_points FROM player_ranks WHERE player_id = {player1_id}"
        query_player2_rank = f"SELECT rank_points FROM player_ranks WHERE player_id = {player2_id}"
        
        player1_rank_df = pd.read_sql(query_player1_rank, engine)
        player2_rank_df = pd.read_sql(query_player2_rank, engine)
        
        if not player1_rank_df.empty:
            player1_rank = player1_rank_df['rank_points'].values[0]
        else:
            player1_rank = 0

        if not player2_rank_df.empty:
            player2_rank = player2_rank_df['rank_points'].values[0]
        else:
            player2_rank = 0
        
        query_player1_glicko = f"SELECT player_glicko FROM players_glicko WHERE player_id = {player1_id}"
        query_player2_glicko = f"SELECT player_glicko FROM players_glicko WHERE player_id = {player2_id}"
        
        player1_glicko_df = pd.read_sql(query_player1_glicko, engine)
        player2_glicko_df = pd.read_sql(query_player2_glicko, engine)
        
        player1_glicko = player1_glicko_df['player_glicko'].values[0]
        player2_glicko = player2_glicko_df['player_glicko'].values[0]
        
        if model == "GradientBoosting":
            winning_chance_player1_by_rank, winning_chance_player2_by_rank = python.test_rank.predict_by_rank_gb(player1_id, player2_id, player1_rank, player2_rank, surface)
            winning_chance_player1_by_rank_hyper, winning_chance_player2_by_rank_hyper = python.test_rank_hyper.predict_by_rank_gb(player1_id, player2_id, player1_rank, player2_rank, surface)
            winning_chance_player1_by_elo, winning_chance_player2_by_elo = python.test_elo.predict_by_elo_gb(player1_id, player2_id, player1_elo, player2_elo, surface)
            winning_chance_player1_by_elo_hyper, winning_chance_player2_by_elo_hyper = python.test_elo_hyper.predict_by_elo_gb(player1_id, player2_id, player1_elo, player2_elo, surface)
            winning_chance_player1_by_glicko_normal, winning_chance_player2_by_glicko_normal = python.test_glicko.predict_by_glicko_gb(player1_id, player2_id, player1_glicko, player2_glicko, surface)
            winning_chance_player1_by_glicko_hyper, winning_chance_player2_by_glicko_hyper = python.test_glicko_hyper.predict_by_glicko_hyper_gb(player1_id, player2_id, player1_glicko, player2_glicko, surface)
        else:
            winning_chance_player1_by_rank, winning_chance_player2_by_rank = python.test_rank.predict_by_rank(player1_id, player2_id, player1_rank, player2_rank, surface)
            winning_chance_player1_by_rank_hyper, winning_chance_player2_by_rank_hyper = python.test_rank_hyper.predict_by_rank(player1_id, player2_id, player1_rank, player2_rank, surface)
            winning_chance_player1_by_elo, winning_chance_player2_by_elo = python.test_elo.predict_by_elo(player1_id, player2_id, player1_elo, player2_elo, surface)
            winning_chance_player1_by_elo_hyper, winning_chance_player2_by_elo_hyper = python.test_elo_hyper.predict_by_elo(player1_id, player2_id, player1_elo, player2_elo, surface)
            winning_chance_player1_by_glicko_normal, winning_chance_player2_by_glicko_normal = python.test_glicko.predict_by_glicko(player1_id, player2_id, player1_glicko, player2_glicko, surface)
            winning_chance_player1_by_glicko_hyper, winning_chance_player2_by_glicko_hyper = python.test_glicko_hyper.predict_by_glicko_hyper(player1_id, player2_id, player1_glicko, player2_glicko, surface)
            
        result = {
            'player1_name': player1_name,
            'player2_name': player2_name,
            'elo_calculated_using_surface': elo_calculated_using_surface,
            'winning_chance_player1': normalized_prob_player1,
            'winning_chance_player2': normalized_prob_player2,
            'winning_chance_player1_by_rank': winning_chance_player1_by_rank,
            'winning_chance_player2_by_rank': winning_chance_player2_by_rank,
            'winning_chance_player1_by_rank_hyper': winning_chance_player1_by_rank_hyper,
            'winning_chance_player2_by_rank_hyper': winning_chance_player2_by_rank_hyper,
            'winning_chance_player1_by_elo': winning_chance_player1_by_elo,
            'winning_chance_player2_by_elo': winning_chance_player2_by_elo,
            'winning_chance_player1_by_elo_hyper': winning_chance_player1_by_elo_hyper,
            'winning_chance_player2_by_elo_hyper': winning_chance_player2_by_elo_hyper,
            'winning_chance_player1_by_glicko_normal': winning_chance_player1_by_glicko_normal,
            'winning_chance_player2_by_glicko_normal': winning_chance_player2_by_glicko_normal,
            'winning_chance_player1_by_glicko_hyper': winning_chance_player1_by_glicko_hyper,
            'winning_chance_player2_by_glicko_hyper': winning_chance_player2_by_glicko_hyper,
        }
        return jsonify(result)
    
@app.route('/search_players', methods=['GET'])
@cross_origin()
def search_players():
        all_players = [{'id': player_id, 'text': f"{player_name} ({country})"} 
                       for player_id, player_name, country in player_data]
        return jsonify(all_players)


@app.route('/get_glicko_history', methods=['POST'])
def get_glicko_history():
    data = request.get_json()
    if not data or 'player_id' not in data:
        return jsonify({'error': 'No player ID provided'}), 400
    player_id = data['player_id']
    query_player = f"SELECT player_name FROM players WHERE player_id = {player_id}"
    player_df = pd.read_sql(query_player, engine)
    player_name = player_df['player_name'].values[0]
    image = python.plot_glicko.plot_glicko_history(player_id, player_name)
    return jsonify({'image': image})

@app.route('/get_elo_history', methods=['POST'])
def get_elo_history():
    data = request.get_json()
    if not data or 'player_id' not in data:
        return jsonify({'error': 'No player ID provided'}), 400
    player_id = data['player_id']
    query_player = f"SELECT player_name FROM players WHERE player_id = {player_id}"
    player_df = pd.read_sql(query_player, engine)
    player_name = player_df['player_name'].values[0]
    image = python.plot_elo.plot_elo_history(player_id, player_name)
    return jsonify({'image': image})

if __name__ == '__main__':
    app.run(debug=True)
