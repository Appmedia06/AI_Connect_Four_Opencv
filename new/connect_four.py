import random
import cv2
import opencv_function as cv_f
import time

class Connect_Four():
    def __init__(self, log):
        self.log = log
        self.cv_object = cv_f.Opencv_Function()

    def new_board(self, board_width, board_height):
        return tuple(tuple(0 for _ in range(board_height)) for _ in range(board_width))

    def apply_move(self, board_state, move_x, side):
        move_y = 0
        for x in board_state[move_x]:
            if x == 0:
                break
            else:
                move_y += 1

        def get_tuples():
            for i in range(len(board_state)):
                if move_x == i:
                    temp = list(board_state[i])
                    temp[move_y] = side
                    yield tuple(temp)
                else:
                    yield board_state[i]

        return tuple(get_tuples())

    def available_moves(self, board_state):
        for x in range(len(board_state)):
            if any(y == 0 for y in board_state[x]):
                yield x

    def has_winning_line(self, line, winning_length):
        count = 0
        last_side = 0
        for x in line:
            if x == last_side:
                count += 1
                if count == winning_length:
                    return last_side
            else:
                count = 1
                last_side = x
        return 0

    def has_winner(self, board_state, winning_length):
        board_width = len(board_state)
        board_height = len(board_state[0])

        # Rows
        for x in range(board_width):
            winner = self.has_winning_line(board_state[x], winning_length)
            if winner != 0:
                return winner
        # Columns
        for y in range(board_height):
            winner = self.has_winning_line((i[y] for i in board_state), winning_length)
            if winner != 0:
                return winner

        # Diagonals
        diagonals_start = -(board_width - winning_length)
        diagonals_end = (board_width - winning_length)
        for d in range(diagonals_start, diagonals_end):
            winner = self.has_winning_line(
                (board_state[i][i + d] for i in range(max(-d, 0), min(board_width, board_height - d))),
                winning_length)
            if winner != 0:
                return winner
        for d in range(diagonals_start, diagonals_end):
            winner = self.has_winning_line(
                (board_state[i][board_height - i - d - 1] for i in range(max(-d, 0), min(board_width, board_height - d))),
                winning_length)
            if winner != 0:
                return winner

        return 0 

    def play_game(self, plus_player_function, minus_player_function, board_width=7, board_height=6, winning_length=4, log = True):
        board_state = self.new_board(board_width, board_height)
        player_turn = 1
        flag_var = -1

        p_bottom, cap = self.cv_object.prepare()
        if p_bottom == 1:
            while True:
                success, img = cap.read()
                contourimg = img.copy()
                if success:
                    cv2.imshow("Video", img)

                    pos = self.cv_object.find_Chess(img, contourimg)

                    cv2.rectangle(contourimg, (70, 40), (570, 450), (0, 255, 0), 2)
                    cv2.imshow("Final", contourimg)

                    if pos == -2:
                        pass
                    else:
                        # 當玩家了下棋
                        if pos != flag_var:
                            count = 0
                            flag_var = pos
                            time.sleep(0.01)
                            # 讓玩家下一次，電腦也下一次
                            while count < 2:
                                
                                _avialable_moves = list(self.available_moves(board_state))
                                if len(_avialable_moves) == 0:
                                    if self.log:
                                        print("no moves left, game ended a draw")
                                    return 0.
                                if player_turn > 0:
                                    move = plus_player_function(board_state, 1, pos)
                                    print("Your move : " + str(move))
                                    count += 1
                                else:
                                    move = minus_player_function(board_state, -1)
                                    count += 1

                                if move not in _avialable_moves:
                                    # 下到不能下的地方
                                    if self.log:
                                        print("illegal move ", move)
                                    continue

                                board_state = self.apply_move(board_state, move, player_turn)
                                if self.log:
                                    self.printboard(board_state)

                                winner = self.has_winner(board_state, winning_length)
                                if winner != 0:
                                    if self.log:
                                        if player_turn == 1:
                                            # 玩家
                                            print("We have a winner, side : O")
                                        else:
                                            # 電腦
                                            print("We have a winner, side : X")

                                    return winner
                                player_turn = -player_turn


                else:
                    break
                if cv2.waitKey(1) == ord('q'):
                    break
        else:
            pass

        cap.release()
        cv2.destroyAllWindows()

    def printboard(self, board_state):
        R_Max = 7
        C_Max = 6

        board = list(board_state)
        for i in range(R_Max):
            board[i] = list(board_state[i])
        
        for i in range(R_Max):
            for j in range(C_Max):
                if board[i][j] == 1:
                    board[i][j] = 'O'
                elif board[i][j] == -1:
                    board[i][j] = 'X'

        # 換行條件
        key1 = ''
        key2 = ''
        key3 = ''
        # 印出board
        for x in range(0, R_Max):
            if x == R_Max - 1:
                key1 = "\n"
            print(" ---", end='{}'.format(str(key1)))
        for x in range(0, C_Max):
            key2 = ''
            key3 = ''
            print("|", end='')
            for y in range(0, R_Max):
                if board[y][C_Max - 1 - x] == 0:
                    print("  ", end = '')
                else:
                    print(" " + str(board[y][C_Max - 1 - x]), end='')
                if y == R_Max - 1:
                    key2 = "\n"
                print(" |", end='{}'.format(str(key2)))

            if x < R_Max:
                for y in range(0, R_Max):
                    if y == R_Max - 1:
                        key3 = "\n"
                    print(" ---", end='{}'.format(str(key3)))

    # 玩家
    def real_player_opencv(self, board_state, _, pos):
        moves = list(self.available_moves(board_state))
        print("Can move position coordinate [O] : ", end = '')
        print(moves)
        return pos

    def random_player(self, board_state, _):
        moves = list(self.available_moves(board_state))
        return random.choice(moves)