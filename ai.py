def easy_ai_move(snake, food, grid):
    # Just chase the food directly (can crash into itself)
    head = snake.body[0]
    dx = food[0] - head[0]
    dy = food[1] - head[1]
    if abs(dx) > abs(dy):
        return (1 if dx > 0 else -1, 0)
    else:
        return (0, 1 if dy > 0 else -1)

hamiltonian_cache = {}

def hard_ai_move(snake, food, grid_size, player_snake_body=None, hamilton_cycle=None):
    from collections import deque

    rows, cols = grid_size
    head = snake.body[0]
    obstacles = set(snake.body[1:] + (player_snake_body or []))  # Avoid self and player

    # --- Try pathfinding (e.g., BFS) ---
    def bfs(start, goal):
        queue = deque([start])
        visited = set([start])
        parent = {}

        while queue:
            current = queue.popleft()
            if current == goal:
                # Reconstruct path
                path = []
                while current != start:
                    prev = parent[current]
                    path.insert(0, (current[0] - prev[0], current[1] - prev[1]))
                    current = prev
                return path

            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                next_cell = ((current[0] + dx) % rows, (current[1] + dy) % cols)
                if next_cell not in visited and next_cell not in obstacles:
                    visited.add(next_cell)
                    parent[next_cell] = current
                    queue.append(next_cell)
        return None

    path = bfs(head, food)
    if path:
        return path[0]

    # --- Fallback to Hamiltonian path ---
    if hamilton_cycle:
        idx = hamilton_cycle.index(head)
        next_pos = hamilton_cycle[(idx + 1) % len(hamilton_cycle)]
        dx = (next_pos[0] - head[0]) % rows
        dy = (next_pos[1] - head[1]) % cols
        # Convert to minimal delta (e.g., -1 instead of 9 if grid is 10)
        if dx > rows // 2: dx -= rows
        if dy > cols // 2: dy -= cols
        return (dx, dy)

    # If all fails, just move right
    return (0, 1)


def generate_hamiltonian_cycle(rows, cols):
    path = []
    for x in range(rows):
        if x % 2 == 0:
            for y in range(cols):
                path.append((x, y))
        else:
            for y in reversed(range(cols)):
                path.append((x, y))
    return path

