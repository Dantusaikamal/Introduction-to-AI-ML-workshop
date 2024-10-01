# Simplified Wumpus World problem

import random

# Grid size
GRID_SIZE = 4

# Directions
DIRECTIONS = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1)
}

# Initialize the world with pits, wumpus, and gold
class WumpusWorld:
    def __init__(self, grid_size=GRID_SIZE):
        self.grid_size = grid_size
        self.grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]
        self.agent_position = (0, 0)
        self.has_gold = False

        # Randomly place the Wumpus, pits, and gold
        self.place_element("W", 1)  # Wumpus
        self.place_element("P", 3)  # Pits (3 pits)
        self.place_element("G", 1)  # Gold

    def place_element(self, element, count):
        """ Randomly place an element on the grid """
        while count > 0:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if (x, y) != (0, 0) and self.grid[x][y] == '':
                self.grid[x][y] = element
                count -= 1

    def get_percepts(self, x, y):
        """ Return percepts based on the agent's current position """
        percepts = []
        if self.grid[x][y] == "G":
            percepts.append("Glitter")

        for dx, dy in DIRECTIONS.values():
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                if self.grid[nx][ny] == "W":
                    percepts.append("Stench")
                if self.grid[nx][ny] == "P":
                    percepts.append("Breeze")
        return percepts

    def move_agent(self, direction):
        """ Move the agent in the specified direction """
        x, y = self.agent_position
        dx, dy = DIRECTIONS[direction]
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
            self.agent_position = (new_x, new_y)
            percepts = self.get_percepts(new_x, new_y)
            return percepts
        else:
            return None

    def display_grid(self):
        """ Display the grid for debugging purposes """
        for row in self.grid:
            print(row)

# Simple agent that moves and perceives
# Simple agent that moves and perceives with modified logic
class Agent:
    def __init__(self, world):
        self.world = world
        self.current_position = (0, 0)
        self.has_gold = False
        self.visited = set()
        self.visited.add(self.current_position)

    def make_move(self):
        """ Simple logic for agent to make a move """
        x, y = self.current_position
        percepts = self.world.get_percepts(x, y)
        print(f"Agent at position {self.current_position}, Percepts: {percepts}")
        
        if "Glitter" in percepts:
            print("Gold found! Agent grabs the gold.")
            self.has_gold = True
            return
        
        # Check if it's safe to move in one of the directions
        for direction in DIRECTIONS:
            new_x, new_y = x + DIRECTIONS[direction][0], y + DIRECTIONS[direction][1]
            if (0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE) and (new_x, new_y) not in self.visited:
                percepts = self.world.get_percepts(new_x, new_y)
                if "Breeze" not in percepts and "Stench" not in percepts:
                    print(f"Moving {direction} to {new_x, new_y}")
                    self.world.move_agent(direction)
                    self.current_position = (new_x, new_y)
                    self.visited.add(self.current_position)
                    return

        # If no safe move, take a risk and move randomly to an unvisited square
        print("No obvious safe moves, taking a calculated risk...")
        for direction in DIRECTIONS:
            new_x, new_y = x + DIRECTIONS[direction][0], y + DIRECTIONS[direction][1]
            if (0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE) and (new_x, new_y) not in self.visited:
                print(f"Moving {direction} to {new_x, new_y}")
                self.world.move_agent(direction)
                self.current_position = (new_x, new_y)
                self.visited.add(self.current_position)
                return

# Create the Wumpus World
world = WumpusWorld()

# Display the grid (for debugging, not part of the actual agent)
print("Initial Wumpus World Grid:")
world.display_grid()

# Create an agent
agent = Agent(world)

# Run the agent in the world
print("\nAgent starts exploring...")
for _ in range(10):
    if agent.has_gold:
        break
    agent.make_move()

# Create the Wumpus World
world = WumpusWorld()

# Display the grid (for debugging, not part of the actual agent)
print("Initial Wumpus World Grid:")
world.display_grid()

# Create an agent
agent = Agent(world)

# Run the agent in the world
print("\nAgent starts exploring...")
for _ in range(10):
    if agent.has_gold:
        break
    agent.make_move()
