def predict_by_glicko(player1_glicko, player2_glicko):
    exponent = (player1_glicko - player2_glicko) / 400
    probability2 = round(1 / (1 + 10 ** exponent)*100,2)
    probability1 = round(abs(100-probability2),2)
    return probability1, probability2

print(predict_by_glicko(2100,1800))

    