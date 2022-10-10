import pygame, random, time
# Memory Game
# Player tries to find two matching tiles by selecting tiles from a rectangular grid
# Tracks the score of the player as the time taken to complete the game where a lower score is better

# User-defined functions

def main():
    # Initialize all pygame modules
    pygame.init()

    pygame.display.set_mode((500, 400))
    pygame.display.set_caption('Memory')
    w_surface = pygame.display.get_surface() 
    game = Game(w_surface)
    
    # Start the main game loop
    game.play()
    pygame.quit()


# User-defined classes

class Game:
    # An object in this class represents a complete game.

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object

        # === objects that are part of every game
        self.surface = surface
        self.bg_color = pygame.Color('black')

        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True

        # === game specific objects
        self.create_variables()
        self.create_lists()
        self.create_images()
        self.create_board()
        self.text_font = pygame.font.SysFont('', 80)

    def create_variables(self):
        # Create the important variables of the game
        # - self is the Game
        
        self.board_size = 5
        self.score = 0
        self.increment = False
        self.matched = 0
        self.frame_counter = 0
        self.max_frames = 65        
        self.all_matched = 8
        self.two_selected = 2

    def create_lists(self):
        # Create the important lists of the game
        # - self is the Game
        
        self.board = []
        self.images = []  
        self.tiles = []
    
    def create_images(self):
        # Prepares the images that will be shown in the tiles
        # - self is the Game
        
        for index in range(1, 9):
            filename = 'image' + str(index) + '.bmp'
            image = pygame.image.load(filename)
            self.images.append(image)
        
        self.images.extend(self.images)
        self.amount = len(self.images)
        random.shuffle(self.images) 
        
    def create_board(self):
        # Creates the board for the game
        # - self is the Game
        
        width = self.surface.get_width()//5
        height = self.surface.get_height()//4
        hidden_image = pygame.image.load('image0.bmp')
        
        for row_index in range(0, self.board_size - 1):
            row = []
            for col_index in range(0, self.board_size - 1):
                left = col_index * width
                top = row_index * height

                exposed = random.randint(0, len(self.images) - 1)
                exposed_image = self.images[exposed]
                self.images.remove(self.images[exposed])

                tile = Tile(left, top, width, height, self.surface, hidden_image, exposed_image)
                self.tiles.append(tile)
                row.append(tile)

            self.board.append(row)
        
    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:
            self.handle_events()
            self.draw()
            if self.continue_game:
                self.update()
                self.decide_continue()
            self.game_Clock.tick(self.FPS)

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.handle_mousebutton_up(event)
    
    def handle_mousebutton_up(self, event):
        # Handle MOUSEBUTTONUP events
        # - self is the Game
        # - event is the MOUSEBUTTONUP event
        
        self.mouse_position = event.pos
        
        if self.increment == False:
            for row in self.board:
                for tile in row:
                    tile.expose(event.pos)      

    def draw(self):
        # Draw all game objects
        # - self is the Game to draw

        self.surface.fill(self.bg_color)
        
        for row in self.board:
            for tile in row:
                tile.draw()
            
        self.draw_score()
        pygame.display.update()

    def draw_score(self):
        # Draws the player's score
        # - self is the Tile
        
        text_string = str(self.score - 1)
        text_colour = pygame.Color('white')
        text_image = self.text_font.render(text_string, True, text_colour)
        text_pos = (self.surface.get_width() - text_image.get_width(), 0)
        self.surface.blit(text_image, text_pos)

    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update

        self.score = pygame.time.get_ticks() // 1000
        
        tile_status = []
        self.exposed_tiles = []
        
        for tile in self.tiles:
            tile_status.append(tile.check_status())
            
        if tile_status.count(True) == self.two_selected:
            for i in range(len(tile_status)):
                if tile_status[i] == True:
                    self.exposed_tiles.append(self.tiles[i])
                    
            self.check_match()
 
    def check_match(self):
        # Checks to see if the tiles match and then implement the proper behaviour
        # - self is the Tile
        
        if self.exposed_tiles[0].is_same(self.exposed_tiles[1]):
            self.matched += 1        
        else:
            self.increment = True
            if self.increment == True:
                if self.frame_counter < self.max_frames:
                    self.frame_counter += 1
                else:
                    self.increment = False
                    self.frame_counter = 0
                    
                    for tile in self.exposed_tiles:
                        tile.hide()           
    
    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check

        if self.matched == self.all_matched:
            self.continue_game = False

class Tile:
    # An object in this class represents a Tile

    def __init__(self, left, top, width, height, surface, hidden_image, exposed_image):
        # Initialize a Tile

        self.rect = pygame.Rect(left, top, width, height)
        self.surface = surface
        self.images = [hidden_image, exposed_image]
        self.present_image = self.images[0]
        self.is_exposed = False
        
    def expose(self, mouse_pos):
        # Changes the tile's state to exposed
        # - self is the Dot

        if self.rect.collidepoint(mouse_pos) and self.is_exposed == False:
            self.present_image = self.images[1]
            self.is_exposed = True

    def matched(self):
        # Set the tile's exposed status to None to declare that it has been matched
        # - self is the Tile
        
        self.is_exposed = None
    
    def check_status(self):
        # Returns the tile's current status
        # - self is the Tile
        
        return self.is_exposed

    def hide(self):
        # Set the tile back to hidden state
        # - self is the Tile
        
        self.present_image = self.images[0]
        self.is_exposed = False

    def is_same(self, other_tile):
        # Return True if the two tile images are the same; False otherwise
        # - self is the Tile
        # - other_tile is the other exposed Tile to be compared with
        
        if self.present_image == other_tile.get_image():
            self.matched()
            other_tile.matched()
            same = True
        else:
            same = False
        
        return same

    def get_image(self):
        # Return the tile's current image
        # - self is the Tile
        
        return self.present_image

    def draw(self):
        # Draw the image on the surface
        # - self is the Tile

        self.surface.blit(self.present_image, self.rect)
        color = pygame.Color('black')
        border_width = 3
        pygame.draw.rect(self.surface, color, self.rect, border_width)

main()
