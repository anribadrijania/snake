class Snake:
    def __init__(self, start_pos):
        self.body = [start_pos]
        self.direction = (1, 0)  # Right
        self.grow = False

    def move(self, grid_size=None):
        head = self.body[0]
        dx, dy = self.direction
        new_head = (head[0] + dx, head[1] + dy)

        # Apply grid wrapping if grid size is given
        if grid_size:
            rows, cols = grid_size
            new_head = (new_head[0] % rows, new_head[1] % cols)

        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def set_direction(self, direction):
        # Prevent 180-degree reversal
        opposite = (-self.direction[0], -self.direction[1])
        if direction != opposite:
            self.direction = direction

    def check_self_collision(self):
        return self.body[0] in self.body[1:]
