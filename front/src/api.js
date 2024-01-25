const API_BASE_URL = 'http://127.0.0.1:5000';

export function predictMatch(player1Id, player2Id, surface) {
  // Replace with actual POST request logic using fetch or axios
  // and the correct request payload as per your Flask backend
  return fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ player1_id: player1Id, player2_id: player2Id, surface }),
  }).then(response => response.json());
}

export function searchPlayers(query) {
  // Replace with actual GET request logic to search players
  return fetch(`${API_BASE_URL}/search_players?term=${query}`)
    .then(response => response.json());
}
