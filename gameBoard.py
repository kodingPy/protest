import sys, pygame



RED = (255,0,0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Game():

    def __init__(self, jsonData):
        self.value = 0

        if jsonData["matches"] != None :
            self.board =  jsonData["matches"][0]["board"]
            self.id = jsonData["matches"][0]["id"]
            self.turn = jsonData["matches"][0]["turns"]
            self.turnSecobds =jsonData["matches"][0]["turnSeconds"]
            
        else:
            self.board = jsonData["board"]
            self.id = jsonData["id"]
        
        self.castle = None
        self.isCastle= False
        self.lake = (0, 0)
        self.mason_id = (0, 0, 0)
        self.img = pygame.image.load("asset/hexagon.png")
        self.structures = self.board["structures"]
        self.masons = self.board["masons"]
        self.width = self.board["width"]
        self.height = self.board["height"]

        
    def set_castle(self, x, y):
       
        if self.structures[x][y] == 2:
            self.castle = (x, y)
            self.isCastle = True
        
        return self.castle
    
    def set_mason(self, x, y):
        if self.masons[x][y] == 1:
            self.mason_id = (x, y, 1)

    def icon(self, x, y):
        self.img = pygame.image.load('asset/hexagon.png')
        self.value = self.structures[x][y]
        if self.value == 1:
            self.img = pygame.image.load('asset/lake.png')
        elif self.value == 2:
            self.img = pygame.image.load('asset/castle.png')
        
        self.value = self.masons[x][y]
        if self.value > 0:
            self.img = pygame.image.load('asset/masons.png')
        elif self.value < 0:
            self.img = pygame.image.load('asset/enemy.png')

        return self.img

    def draw_grid(self, screen, grid):
        for y in range(self.height):
            for x in range(self.width):
                cell = grid.get_cell(x, y)
                color = (0, 0, 0) if cell.get_state() == 0 else (255, 0, 0)
                pygame.draw.rect(screen, color, (x * 10, y * 10, 10, 10))


    def draw_label(self, screen, text, position):
        font = pygame.font.SysFont(None, 20)
        text_surface = font.render(text, True, (0, 0, 0))
        screen.blit(text_surface, position)
        
    def draw_square_path(self, screen, start_x, start_y, distance):
        """Draws a square path from a cell at (start_x, start_y) in an 11*11 grid with distance = distance.

        Args:
        start_x: The x-coordinate of the start cell.
        start_y: The y-coordinate of the start cell.
        distance: The distance of the square path.

        Returns:
        A list of (x, y) coordinates of the square path.
        """
        distance = distance * 2

       
            # Create a list to store the square path.
        square_path = []
        start_x = start_x - distance // 2
        start_y = start_y - distance // 2
        if 0 > start_x : start_x == 0
        if 11 < start_x: start_x == 10
        if 0 > start_y : start_y == 0
        if 11 < start_y : start_y == 10
        # Add the start top left cell to the square path.
       

        # Move right by distance.
        for i in range(distance ):
            square_path.append((start_x + i + 1, start_y))


        # Move down by distance.
        for i in range(distance ):
            square_path.append((start_x + distance, start_y + i + 1))

        # Move left by distance.
        for i in range(distance):
            square_path.append((start_x + distance - i - 1, start_y + distance))

        # Move up by distance.
        for i in range(distance):
            square_path.append((start_x, start_y + distance - i - 1))

        # Close the square path by adding the start cell again.
        square_path.append((start_x, start_y))


        # Return the square path.
        return square_path

    def get_neighbor_cells_with_distance_2(self, dist, center_cell_x, center_cell_y, grid):
        """Returns a list of all neighbor cells with distance = 2 from the center cell.

        Args:
            center_cell_x: The x-coordinate of the center cell.
            center_cell_y: The y-coordinate of the center cell.
            grid: A 2D list representing the grid.

        Returns:
            A list of all neighbor cells with distance = 2 from the center cell.
        """

        neighbor_cells = []
        # Check all 8 cells around the center cell.
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
            # Make sure that the neighbor cell is within the bounds of the grid.
                if 0 <= center_cell_x + dx < grid.width and 0 <= center_cell_y + dy < grid.height:
                # Make sure that the neighbor cell is not the center cell itself.
                    if dx != 0 or dy != 0:
                        neighbor_cells.append((center_cell_x + dx, center_cell_y + dy))

        return neighbor_cells

