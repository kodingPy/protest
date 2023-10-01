
import pygame, sys
import math
from heapq import heappush, heappop
from apiTask import APITask
from gameBoard import Game

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
        self.color = WHITE
        self.square_path = {}
        self.value = 0


    def __lt__(self, other):
        return self.f_score < other.f_score
    
    def get_value(self, data):
        return data[self.x][self.y]
    
    def set_color(self, value):
        if value == 0: return  WHITE 
        if value == 2: return  BLUE
        if value == 1: return RED
        if value < 0: return  GREEN
        else:
            return WHITE

    
    
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
    squarePaths = []
    screen = pygame.display.set_mode((grid.width * 64, grid.height * 64))
    pygame.display.set_caption("A* Algorithm Visualization")
    size = 48
    clock = pygame.time.Clock()
    castle_list =  []
    masons = grid.set_mason(0,0)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    print(x // 48, y // 48)

                    cell = grid.set_castle(x // size, y //size)
                    squarePaths = grid.draw_square_path(screen, cell[0], cell[1], 1)
                #draw square path on screen
            for square in squarePaths:
                pygame.draw.rect(screen, GREEN, (square[0] * size, square[1] * size, size, size),width= 2, border_radius= 2)        
                pygame.display.flip()
        # Fill the screen with black color
        screen.fill((255, 255, 255))
        
        
        # Draw the grid
        for x in range(grid.width):
            for y in range(grid.height):
                surface = pygame.Surface((size, size))
                surface.fill(WHITE)
                node = grid
                #node.color = node.set_color(jsondata["matches"][0]["board"]["structures"][x][y])
                
                #pygame.draw.rect(screen, BLACK, (node.x , node.y , 20, 20),width= 2, border_radius= 0)
                nodeIcon = grid.icon(x, y)
                imageIcon = pygame.transform.scale(nodeIcon, (size, size))
                surface.blit(imageIcon, (0,0))
                screen.blit(surface, (x * size,y * size))
                
                
                """ castle_list = grid.set_castle(8, 8)
                if castle_list:
                    squarePaths = grid.draw_square_path(screen, castle_list[0], castle_list[1], 1)
                #draw square path on screen
                    for square in squarePaths:
                        pygame.draw.rect(screen, GREEN, (square[0] * size, square[1] * size, size, size),width= 2, border_radius= 2)
                 """
                #
        '''
        
                if node.parent is not None:
                #    pygame.draw.line(screen, (255, 255, 0), (node.x * 10, node.y * 10), (node.parent.x * 10, node.parent.y * 10), 2)
            
                if node.value == jsondata["matches"][0]["board"]["masons"][x][y]:
                    pygame.draw.rect(screen, (0, 255, 0), (node.x , node.y, 10, 10))
                elif node.value == jsondata["matches"][0]["board"]["masons"][x][y]:
                    pygame.draw.rect(screen, BLACK, (node.x , node.y , 20, 20),width= 1, border_radius= 45) 
'''
       
                
                

        # Draw the path
       # for node in path:
          #     pygame.draw.rect(screen, (255, 0, 0), (node.x * 10, node.y * 10, 10, 10))


        

        
        

        enemyImg = pygame.transform.scale(pygame.image.load("asset/enemy.png"), (size, size))
        masonImg = pygame.transform.scale(pygame.image.load("asset/masons.png") , (size, size))
        screen.blit(enemyImg, (64, 555))
        grid.draw_label(screen, "Enemy:", (10, 580))
        screen.blit(masonImg, (320, 555))
        grid.draw_label(screen, "Jibun:", (260, 580))

        # Update the display
        pygame.display.flip()

        # Limit the framerate to 30 FPS
        clock.tick(3)

if __name__ == "__main__":

    apiRequest = APITask("")
    jsondata =  apiRequest.jsonReturn

    if jsondata:
        print(apiRequest.structures)
        # Create a grid
        board = Game(jsondata)
        grid = Grid(board.width, board.height)
        

    # Set the start and goal nodes
        start = grid.get_node(0, 0)
        goal = grid.get_node(9, 9)

    # Find a path from the start to the goal node
        astar = AStar(grid, start, goal)
        path = astar.search()

    # Visualize the path
        visualize_astar(board, start, goal, path)