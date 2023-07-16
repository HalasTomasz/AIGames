import random
import copy
# class Player2AI:
#     def get_move(self, game):
#         legal_moves = game.get_legal_moves()
#         print("P1",legal_moves)
#         #return(('D',))
#         return random.choice(legal_moves)

from collections import deque

PlAYERS_HEADING_DIRECTION={
    'P1':0,
    'P2':4
}


class Player2AI:

    init = True

    def init_game(self, game):
        self.init= False
        self.board_size = game.board_size
        self.number_of_wals = 4

    def get_move(self, game):

        if self.init:
            self.init_game(game)

        keys = list(game.player_positions.keys())
        values = list(game.player_positions.values())
        
        enemy_position_AI = values[0]        
        user_position_AI = values[1]


        distance_enemy, _ = self.find_shortest_path(
            game.board,
            enemy_position_AI, 
            PlAYERS_HEADING_DIRECTION[keys[0]]
        )

        distance_user, path_user = self.find_shortest_path(
            game.board,
            user_position_AI,
            PlAYERS_HEADING_DIRECTION[keys[1]]
        )

        print("PLAYER DIST:", distance_user)
        print("ENEMY DIST:", distance_enemy)

        path_user = list(path_user)
        next_user_step = path_user[0]
        
        dist_enemy, answer =  self.add_for_enemy_wall(
            game,
            enemy_position_AI,
            PlAYERS_HEADING_DIRECTION[keys[0]]
        )

        # print(answer)
        # print("WALL INCREASE:", dist_enemy)

        user_command = self.decoder(user_position_AI, next_user_step)
        
        if distance_enemy <= distance_user and self.number_of_wals >= 0:
            print("WALL HIM")
            self.number_of_wals -= 1
            return answer
        else:
            return user_command

    def is_valid(self, x, y, board_size):
        return 0 <= x < board_size and 0 <= y < board_size

    def find_shortest_path(self, array_2d, player_position, pawn_heading):

        visited = [[False for _ in range(self.board_size)] for _ in range(self.board_size)]
        start_x, start_y = player_position[0], player_position[1]

        # print("ARRAY")
        # for i in range(self.board_size):
        #     for j in range(self.board_size):
        #         print(array_2d[i][j] , end="\t")
        #     print()

        queue = deque([(start_x, start_y, 0, [])])
        visited[start_x][start_y] = True

        while queue:
            curr_x, curr_y, distance, path = queue.popleft()

            if curr_x == pawn_heading:
                return distance, path

            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for dx, dy in directions:
                new_x, new_y = curr_x + dx, curr_y + dy

                if self.is_valid(new_x, new_y, self.board_size) and not visited[new_x][new_y] and self.checker(array_2d, curr_x, dx, curr_y, dy ):
                    visited[new_x][new_y] = True
                    queue.append((new_x, new_y, distance + 1, path + [(new_x, new_y)]))
    
    def checker(self, array_2d, curr_x, dx, curr_y, dy):
        new_x, new_y = curr_x + dx, curr_y + dy
        result_array = []
        if  array_2d[curr_x][curr_y] == False and array_2d[new_x][new_y] == False :
            return True
        else:

            if isinstance(array_2d[curr_x][curr_y], str) and 'H' in array_2d[curr_x][curr_y]:
                if dx == 1:
                    result_array.append(False)
                else:
                    result_array.append(True)
            if isinstance(array_2d[new_x][new_y], str) and 'H' in array_2d[new_x][new_y]:
                if dx == -1:
                    result_array.append(False)
                else:
                    result_array.append(True) 
                
            if isinstance(array_2d[curr_x][curr_y], str) and 'V' in array_2d[curr_x][curr_y]:
                if dy == 1:
                    result_array.append(False)
                else:
                    result_array.append(True)
            if isinstance(array_2d[new_x][new_y], str) and 'V' in array_2d[new_x][new_y]:
                if dy == -1:
                    result_array.append(False)
                else:
                    result_array.append(True)

            return all(result_array)
        
    def decoder(self, player_position, new_direction):
        # print("PLAYER POSITION ", player_position)
        # print("NEW POSITION ", new_direction)

        if player_position[0] < new_direction[0]:
            return ('D',)
        elif player_position[0] > new_direction[0]:
            return ('U',) 
        elif player_position[1] < new_direction[1]:
            return ('R',)
        elif player_position[1] > new_direction[1]:
            return ('L',)
        else: 
            return None
        
    def add_for_enemy_wall(self, game_object, player_position, pawn_heading):

        self.previous_state = copy.deepcopy(game_object.board)
        legal_moves = game_object.get_legal_moves()
        filtered_list = [tpl for tpl in legal_moves if 'H' in tpl or 'V' in tpl]
        
        worst_solution_distance = -1
        solution = None

        for move in filtered_list:

            array_2d = [row[:] for row in self.previous_state]
            board = self.update_board_wall(array_2d, move)

            distance, _ = self.find_shortest_path(board, player_position, pawn_heading)
            if distance > worst_solution_distance:
                worst_solution_distance = distance
                solution = move

        self.previous_state = None

        return worst_solution_distance, solution
    
    def update_board_wall(self, board, move):
        wall_type, center_row, center_col = move
        
        if wall_type == 'H':
            
            if board[center_row][center_col] == False:
                board[center_row][center_col] = 'HH'
            elif board[center_row][center_col] == "V":
                board[center_row][center_col] = 'HV'
            elif board[center_row][center_col] == "VV":
                board[center_row][center_col] = 'HV'
                
            if board[center_row][center_col + 1] == False:
                board[center_row][center_col + 1] = 'H'
            elif board[center_row][center_col + 1] == "V":
                board[center_row][center_col + 1] = 'HV'
            elif board[center_row][center_col + 1] == "VV":
                board[center_row][center_col + 1] = 'HV'
                
        elif wall_type == 'V':
            
            if board[center_row][center_col] == False:
                board[center_row][center_col] = 'VV'
            elif board[center_row][center_col] == "H":
                board[center_row][center_col] = 'HV'
            elif board[center_row][center_col] == "HH":
                board[center_row][center_col] = 'HV'
                
            if board[center_row + 1][center_col] == False:
                board[center_row + 1][center_col] = 'V'
            elif board[center_row + 1][center_col] == "H":
                board[center_row + 1][center_col] = 'HV'
            elif board[center_row + 1][center_col] == "HH":
                board[center_row + 1][center_col] = 'HV'

        return board