from collections import deque

def is_valid(x, y, rows, cols):
    return 0 <= x < rows and 0 <= y < cols

def find_shortest_path(array_2d, board_size, player_position, pawn_heading):

    visited = [[False for _ in range(board_size)] for _ in range(board_size)]

    start_x, start_y = player_position[0], player_position[1]

    queue = deque([(start_x, start_y, 0, [])])
    visited[start_x][start_y] = True

    while queue:
        curr_x, curr_y, distance, path = queue.popleft()

        if curr_x == pawn_heading:
            return distance, path, visited

        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        for dx, dy in directions:
            new_x, new_y = curr_x + dx, curr_y + dy

            if is_valid(new_x, new_y, board_size, board_size) and not visited[new_x][new_y] and not isinstance(array_2d[new_x][new_y] , str):
                visited[new_x][new_y] = True
                queue.append((new_x, new_y, distance + 1, path + [(new_x, new_y)]))


# Example usage:
array_2d = [[False, False, False, False, False, False, False, False, False, False], 
            [False, False, False, False, False, False, False, False, False, False], 
            [False, False, False, False, False, False, False, False, False, False], 
            [False, False, False, False, False, False, False, False, False, False], 
            [False, False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False, False], 
            [False, False, False, False, False, False, False, False, False, False], 
            [False, False, False, False, False, False, False, False, False, False], 
            [False, False, False, False, False, False, False, False, False, False]
            [False, False, False, False, False, False, False, False, False, False]]
(4, 2)


distance, path, visited = find_shortest_path(array_2d, 5, (0, 2*2), 4*2)

print(path)
print(distance)
print(visited)