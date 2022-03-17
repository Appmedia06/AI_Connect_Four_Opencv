import connect_four as cf
import sys

class Connect_four_algorithm():
    def __init__(self):
        self.cf_object = cf.Connect_Four(log=True)

    def score_line(self, line):
        minus_count = line.count(-1)
        plus_count = line.count(1)
        if minus_count + plus_count < 4:
            if minus_count == 3:
                return -1
            elif plus_count == 3:
                return 1
        return 0

    def evaluate(self, board_state):
        score = 0
        # Rows
        for x in range(7):
            score += self.score_line(board_state[x])
        # Columns
        for y in range(6):
            score += self.score_line([i[y] for i in board_state])
        # Diagonals
        # \ 
        for i in range(4):
            tempList = []
            tempList.append(board_state[i][3 - i])
            score += self.score_line(tempList)
        
        for i in range(5):
            tempList = []
            tempList.append(board_state[i][4 - i])
            score += self.score_line(tempList)

        for i in range(6):
            tempList = []
            tempList.append(board_state[i][5 - i])
            score += self.score_line(tempList)

        for i in range(1, 7):
            tempList = []
            tempList.append(board_state[i][6 - i])
            score += self.score_line(tempList)

        for i in range(2, 7):
            tempList = []
            tempList.append(board_state[i][7 - i])
            score += self.score_line(tempList)

        for i in range(3, 7):
            tempList = []
            tempList.append(board_state[i][8 - i])
            score += self.score_line(tempList)

        # / 
        for i in range(4):
            tempList = []
            tempList.append(board_state[i][i + 2])
            score += self.score_line(tempList)

        for i in range(5):
            tempList = []
            tempList.append(board_state[i][i + 1])
            score += self.score_line(tempList)
        
        for i in range(6):
            tempList = []
            tempList.append(board_state[i][i])
            score += self.score_line(tempList)

        for i in range(1, 7):
            tempList = []
            tempList.append(board_state[i][i - 1])
            score += self.score_line(tempList)

        for i in range(2, 7):
            tempList = []
            tempList.append(board_state[i][i - 2])
            score += self.score_line(tempList)

        for i in range(3, 7):
            tempList = []
            tempList.append(board_state[i][i - 3])
            score += self.score_line(tempList)

        return score

    def min_max_alpha_beta(self, board_state, side, max_depth, alpha=-sys.float_info.max,
                        beta=sys.float_info.max):
        best_score_move = None
        moves = list(self.cf_object.available_moves(board_state))

        if not moves:
            return 0, None

        for move in moves:
            new_board_state = self.cf_object.apply_move(board_state, move, side)
            winner = self.cf_object.has_winner(new_board_state, winning_length = 4)
            if winner != 0:
                return winner * 10000, move
            else:
                if max_depth <= 1:
                    score = self.evaluate(new_board_state)
                else:
                    score, _ = self.min_max_alpha_beta(new_board_state, -side, max_depth - 1, alpha, beta)
            if side > 0:
                if score > alpha:
                    alpha = score
                    best_score_move = move
            else:
                if score < beta:
                    beta = score
                    best_score_move = move

            if alpha >= beta:
                break
        return alpha if side > 0 else beta, best_score_move

    def min_max_alpha_beta_player(self, board_state, side):
        move = self.min_max_alpha_beta(board_state, side, 5)[1]
        return move


