import random

def draw_maze(maze):
    for row in maze:
        print(''.join(row))
        
def generate_maze(width, height):
    # Create a grid with walls
    maze = [['#'] * (2 * width + 1) for _ in range(2 * height + 1)]

    def carve(x, y):
        maze[y][x] = ' '  # Carve a path

        # Shuffle the directions
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + 2 * dx, y + 2 * dy
            if 0 <= nx < 2 * width + 1 and 0 <= ny < 2 * height + 1 and maze[ny][nx] == '#':
                maze[y + dy][x + dx] = ' '  # Remove the wall
                carve(nx, ny)
    
    maze = generate_maze()  # あなたの迷路生成関数
    draw_maze(maze)

