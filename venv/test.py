CHESS_TYPE_NUM=10
chess_len=15

pos_score = [[(7 - max(abs(x - 7), abs(y - 7))) for x in range(chess_len)] for y in range(chess_len)]

count = [[0 for x in range(CHESS_TYPE_NUM)] for i in range(2)]
print(pos_score)
print(pos_score[6])
print(pos_score[6][5])