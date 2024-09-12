import pygame, sys, random


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
pc_background = pygame.image.load('./imgs/pc.png')
end_background = pygame.image.load('./imgs/end.png')

# Game variables
current_screen = 'welcome' # 'welcome', 'game_1_3', 'game_4_5', 'pc_turn', or 'end'
round_count = 1
years = 3 # Prison years counter
user_choices = [] # User's choices
pc_choices = [] # PC's choices
veredict = 0


'''
***** ITEM UTILS ***** 
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


'''
***** SCREENS ***** 
'''

# Welcome screen
def welcome_screen():
    screen.blit(welcome_background, (0, 0))
    start_button = create_button('INICIAR', font, 435, 500, 160, 60)
    return start_button

# Game 1-3 screen
def game_1_3_screen():

    global round_count, years
    screen.blit(game_background, (0, 0))

    # Texts (counters)
    draw_text(f'Ronda: {round_count}', font, WHITE, screen, 310, 106)
    draw_text(f'Años: {years}', font, WHITE, screen, 704, 106)

    # Buttons
    confess_button = create_button('CONFESAR', font, 250, 500, 200, 60)
    lie_button = create_button('MENTIR', font, 550, 500, 200, 60)
    silent_button = create_button('CALLAR', font, 400, 600, 200, 60)
    return confess_button, lie_button, silent_button

# Game 4-5 screen
def game_4_5_screen():

    global round_count, years
    screen.blit(game_background, (0, 0))

    # Texts (counters)
    draw_text(f'Ronda: {round_count}', font, WHITE, screen, 310, 106)
    draw_text(f'Años: {years}', font, WHITE, screen, 704, 106)

    # Buttons
    confess_button = create_button('CONFESAR', font, 250, 500, 200, 60)
    lie_button = create_button('MENTIR', font, 550, 500, 200, 60)
    return confess_button, lie_button

# PC turn screen
def pc_screen():

    global round_count, years, pc_choices, veredict
    screen.blit(pc_background, (0, 0))

    # Texts (counters)
    draw_text(f'Ronda: {round_count}', font, WHITE, screen, 310, 106)
    draw_text(f'Años: {years}', font, WHITE, screen, 704, 106)
    draw_text(f'La PC ha decidido: {pc_choices[-1]}', font, WHITE, screen, 500, 354)
    draw_text(f'Sentencia: {veredict} años', font, WHITE, screen, 500, 410)

# Game over screen
def end_screen():

    global years
    screen.blit(end_background, (0, 0))
    draw_text('GAME OVER...', font, WHITE, screen, 500, 560)
    draw_text(f'Años de condena: {years}', font, WHITE, screen, 500, 630)
    draw_text(f'Recibes: {get_exit_results()} ', font, WHITE, screen, 500, 710)


'''
***** GAME LOGIC UTILS ***** 
'''

# PC random choice
def pc_random_choice():

    choice = random.randint(1,3)

    if choice == 1:
        return 'CONFESAR'
    elif choice == 2:
        return 'MENTIR'
    else: 
        return 'CALLAR'

# Calculate veredict
def get_veredict():

    global user_choices, pc_choices, years

    user = user_choices[-1]
    pc = pc_choices[-1]

    if user == 'CONFESAR':
        if pc == 'CONFESAR':
            return -2
        elif pc == 'MENTIR':
            return -1
        elif pc == 'CALLAR':
            return -2

    if user == 'MENTIR':
        if pc == 'CONFESAR':
            return 5
        elif pc == 'MENTIR':
            return years * -1
        elif pc == 'CALLAR':
            return -1

    if user == 'CALLAR':
        if pc == 'CONFESAR':
            return 3
        elif pc == 'MENTIR':
            return -2
        elif pc == 'CALLAR':
            return 0

# Calculate exit
def get_exit_results():

    global years

    if years <= 0: 
        return 'Apuesta + Bono'
    if years in (1, 2): 
        return 'Apuesta'
    if years in (3, 4):
        return '75% de Apuesta'  
    if years in (5, 6):
        return '50% de Apuesta'  
    if years > 6:
        return '0% de Apuesta'  

def update_globals():

    global current_screen, pc_choices, veredict, years

    pygame.time.delay(200)
    pc_choices.append(pc_random_choice())
    veredict = get_veredict()
    years = years + veredict
    current_screen = 'pc_turn'


'''
***** GAME FLOW ***** 
'''

def game_loop():

    global current_screen, round_count, years, user_choices, pc_choices, veredict

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
                    user_choices.append('CONFESAR')
                    update_globals()
                elif lie_button.collidepoint(event.pos):
                    user_choices.append('MENTIR')
                    update_globals()
                elif silent_button.collidepoint(event.pos):
                    user_choices.append('CALLAR')
                    update_globals()

            # Game rounds 4-5
            elif current_screen == 'game_4_5' and event.type == pygame.MOUSEBUTTONDOWN:
                if confess_button.collidepoint(event.pos):
                    user_choices.append('CONFESAR')
                    update_globals()
                elif lie_button.collidepoint(event.pos):
                    user_choices.append('MENTIR')
                    update_globals()
                    
            # PC turn
            elif current_screen == 'pc_turn' and event.type == pygame.MOUSEBUTTONDOWN:
                
                pygame.time.delay(200)

                if round_count in (1, 2):
                    current_screen = 'game_1_3'
                    years += 3
                elif round_count in (3, 4):
                    current_screen = 'game_4_5'
                    years += 3
                else:
                    current_screen = 'end'

                round_count += 1
                
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
        elif current_screen == 'pc_turn':
            pc_screen()
        elif current_screen == 'end':
            end_screen()

        pygame.display.flip()


# Invoke game loop
game_loop()
