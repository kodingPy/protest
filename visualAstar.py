import pygame
import math
from heapq import heappush, heappop
from apiTask import APITask
import json 

RED = (255,0,0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.f_score = 0
        self.g_score = 0
        self.h_score = 0
        self.color = (0, 0, 0)
        self.square_path = {}
        self.value = 0


    def __lt__(self, other):
        return self.f_score < other.f_score
    
    def get_value(self, data):
        return data[self.x][self.y]
    
    def set_color(self, value):
        return WHITE if self.value == 0 else BLUE if self.value == 1 else RED if self.value < 0 else GREEN


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Node(x, y) for x in range(width)] for y in range(height)]

    def get_node(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        return self.grid[y][x]

    def is_walkable(self, x, y):
        node = self.get_node(x, y)
        if node is None:
            return False
        return node.parent is None

    def get_neighbors(self, node):
        neighbors = []
        for x in range(node.x - 1, node.x + 2):
            for y in range(node.y - 1, node.y + 2):
                neighbor = self.get_node(x, y)
                if neighbor is not None and neighbor != node and self.is_walkable(x, y):
                    neighbors.append(neighbor)
        return neighbors

class AStar:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.open_list = []
        self.closed_list = []

    def search(self):
        heappush(self.open_list, self.start)

        while self.open_list:
            node = heappop(self.open_list)
            self.closed_list.append(node)

            if node == self.goal:
                return []

            for neighbor in self.grid.get_neighbors(node):
                if neighbor not in self.closed_list:
                    g_score = node.g_score + 1
                    h_score = math.sqrt((neighbor.x - self.goal.x)**2 + (neighbor.y - self.goal.y)**2)
                    f_score = g_score + h_score

                    if neighbor not in self.open_list or f_score < neighbor.f_score:
                        neighbor.parent = node
                        neighbor.g_score = g_score
                        neighbor.h_score = h_score
                        neighbor.f_score = f_score

                        if neighbor not in self.open_list:
                            heappush(self.open_list, neighbor)

        return heappush

def visualize_astar(grid, start, goal, path):

    pygame.init()

    screen = pygame.display.set_mode((grid.width * 10, grid.height * 10))
    pygame.display.set_caption("A* Algorithm Visualization")

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fill the screen with black color
        screen.fill((0, 0, 128))

        # Draw the grid
        for x in range(grid.width):
            for y in range(grid.height):
                node = Node(jsondata["matches"][0]["board"]["structures"][x], jsondata["matches"][0]["board"]["structures"][y])

                #node = grid.get_node(x, y)
                node.color = node.set_color(jsondata["matches"][0]["board"]["structures"][x][y])
                pygame.draw.rect(screen, node.color, (11, 11, 11, 11))
        """
                if node.parent is not None:
                    pygame.draw.line(screen, (255, 255, 255), (node.x * 10, node.y * 10), (node.parent.x * 10, node.parent.y * 10), 2)
            
                if node.value == jsondata["matches"][0]["board"]["masons"][x][y]:
                    pygame.draw.rect(screen, (0, 255, 0), (grid.width, grid.height * 10, 10, 10))
                elif jsondata["matches"][0]["board"]["structures"][x][y] == 2:
                    pygame.draw.rect(screen, (255, 0, 0), (node.x * 10, node.y * 10, 10, 10))
            """

        # Draw the path
        for node in path:
                pygame.draw.rect(screen, (0, 128, 0), (node.x * 10, node.y * 10, 10, 10))

        # Update the display
        pygame.display.flip()

        # Limit the framerate to 30 FPS
        clock.tick(30)

if __name__ == "__main__":

    jsondata =  APITask.getMatches()

    # Create a grid
    grid = Grid(jsondata["matches"][0]["board"]["width"], jsondata["matches"][0]["board"]["width"])

    # Set the start and goal nodes
    start = grid.get_node(0, 0)
    goal = grid.get_node(9, 9)

    # Find a path from the start to the goal node
    astar = AStar(grid, start, goal)
    path = astar.search()

    # Visualize the path
    visualize_astar(grid, start, goal, path)