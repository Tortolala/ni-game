import pygame, sys


'''
***** SET UP ***** 
'''

# Game initialization
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Setup screen
screen_width, screen_height = 1000, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('DILEMA DEL PRISIONERO')
FPS = pygame.time.Clock()
FPS.tick(60)

# Font and background images
font = pygame.font.SysFont('Arial', 32, bold=True)
welcome_background = pygame.image.load('./imgs/welcome.png')
game_background = pygame.image.load('./imgs/game.png')
end_background = pygame.image.load('./imgs/end.png')

# Game variables
current_screen = 'welcome' # 'welcome', 'game_1_3', 'game_4_5', or 'end'
round_count = 1
base_years = 3
choices = [] # User's choices


'''
***** UTILS ***** 
'''

# Utility functions
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def create_button(text, font, x, y, width, height):
    border_rect = pygame.Rect(x - 3, y - 3, width + 3 * 2, height + 3 * 2)
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, WHITE, border_rect)
    pygame.draw.rect(screen, BLACK, button_rect)
    draw_text(text, font, WHITE, screen, x + width // 2, y + height // 2)
    return button_rect

# Welcome screen
def welcome_screen():
    screen.blit(welcome_background, (0, 0))
    start_button = create_button('INICIAR', font, 435, 500, 160, 60)
    return start_button

# Game 1-3 screen
def game_1_3_screen():

    global round_count, base_years

    screen.blit(game_background, (0, 0))

    # Texts (counters)
    draw_text(f'Ronda: {round_count}', font, WHITE, screen, 310, 106)
    draw_text(f'Años: {base_years}', font, WHITE, screen, 704, 106)

    # Buttons
    confess_button = create_button('CONFESAR', font, 250, 500, 200, 60)
    lie_button = create_button('MENTIR', font, 550, 500, 200, 60)
    silent_button = create_button('CALLAR', font, 400, 600, 200, 60)
    return confess_button, lie_button, silent_button

# Game 4-5 screen
def game_4_5_screen():

    global round_count, base_years

    screen.blit(game_background, (0, 0))

    # Texts (counters)
    draw_text(f'Ronda: {round_count}', font, WHITE, screen, 310, 106)
    draw_text(f'Años: {base_years}', font, WHITE, screen, 704, 106)

    # Buttons
    confess_button = create_button('CONFESAR', font, 250, 500, 200, 60)
    lie_button = create_button('MENTIR', font, 550, 500, 200, 60)
    return confess_button, lie_button

# Game over screen
def end_screen():
    screen.blit(end_background, (0, 0))
    draw_text('GAME OVER...', font, WHITE, screen, 510, 560)


'''
***** GAME FLOW ***** 
'''

def game_loop():

    global current_screen, round_count, base_years, choices

    while True:
        
        for event in pygame.event.get():

            # Window exit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Start game
            if current_screen == 'welcome' and event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    current_screen = 'game_1_3'
                    pygame.time.delay(200)

            # Game rounds 1-3
            elif current_screen == 'game_1_3' and event.type == pygame.MOUSEBUTTONDOWN:
                if confess_button.collidepoint(event.pos):
                    choices.append('CONFESAR')
                elif lie_button.collidepoint(event.pos):
                    choices.append('MENTIR')
                elif silent_button.collidepoint(event.pos):
                    choices.append('CALLAR')
                    
                round_count += 1
                pygame.time.delay(200)

                # Check round 3 limit
                if round_count > 3:
                    current_screen = 'game_4_5'

            # Game rounds 4-5
            elif current_screen == 'game_4_5' and event.type == pygame.MOUSEBUTTONDOWN:
                if confess_button.collidepoint(event.pos):
                    choices.append('CONFESAR')
                elif lie_button.collidepoint(event.pos):
                    choices.append('MENTIR')
                elif silent_button.collidepoint(event.pos):
                    choices.append('CALLAR')
                    
                round_count += 1
                pygame.time.delay(200)

                # Check round 5 limit
                if round_count > 5:
                    current_screen = 'end'

            # End of game
            elif current_screen == 'end' and event.type == pygame.MOUSEBUTTONDOWN:
                pygame.time.delay(500)
                pygame.quit()
                sys.exit()

        # Render screens
        if current_screen == 'welcome':
            start_button = welcome_screen()
        elif current_screen == 'game_1_3':
            confess_button, lie_button, silent_button = game_1_3_screen()
        elif current_screen == 'game_4_5':
            confess_button, lie_button = game_4_5_screen()
        elif current_screen == 'end':
            end_screen()

        pygame.display.flip()


# Invoke game loop
game_loop()
