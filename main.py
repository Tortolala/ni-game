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
screen_width, screen_height = 750, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('DILEMA DEL PRISIONERO')
FPS = pygame.time.Clock()
FPS.tick(60)

# Font and background images
font = pygame.font.SysFont('Arial', 24, bold=True)
font_2 = pygame.font.SysFont('Arial', 20, bold=True)
crime_1_background = pygame.image.load('./imgs/story_crime_1.png')
crime_2_background = pygame.image.load('./imgs/story_crime_2.png')
crime_3_background = pygame.image.load('./imgs/story_crime_3.png')
crime_4_background = pygame.image.load('./imgs/story_crime_4.png')
crime_5_background = pygame.image.load('./imgs/story_crime_5.png')
welcome_background = pygame.image.load('./imgs/welcome.png')
game_background = pygame.image.load('./imgs/game.png')
end_background = pygame.image.load('./imgs/end.png')
pc_background = pygame.image.load('./imgs/pc.png')

# Game variables
current_screen = 'welcome' # Screen name
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

# 1st crime
def crime_1_screen():
    screen.blit(crime_1_background, (0, 0))
    continue_button = create_button('CONTINUAR', font_2, 500, 475, 150, 40)
    return continue_button

# 2nd crime
def crime_2_screen():
    screen.blit(crime_2_background, (0, 0))
    continue_button = create_button('CONTINUAR', font_2, 500, 475, 150, 40)
    return continue_button

# 3rd crime
def crime_3_screen():
    screen.blit(crime_3_background, (0, 0))
    continue_button = create_button('CONTINUAR', font_2, 500, 475, 150, 40)
    return continue_button

# 4th crime
def crime_4_screen():
    screen.blit(crime_4_background, (0, 0))
    continue_button = create_button('CONTINUAR', font_2, 500, 475, 150, 40)
    return continue_button

# 5th crime
def crime_5_screen():
    screen.blit(crime_5_background, (0, 0))
    continue_button = create_button('CONTINUAR', font_2, 500, 475, 150, 40)
    return continue_button

# Welcome screen
def welcome_screen():
    screen.blit(welcome_background, (0, 0))
    start_button = create_button('INICIAR', font, 326, 375, 120, 45)
    return start_button

# Game 1-3 screen
def game_1_3_screen():

    global round_count, years
    screen.blit(game_background, (0, 0))

    # Texts (counters)
    draw_text(f'Ronda: {round_count}', font, WHITE, screen, 232, 80)
    draw_text(f'Años: {years}', font, WHITE, screen, 528, 80)

    # Buttons
    confess_button = create_button('CONFESAR', font, 188, 375, 150, 45)
    lie_button = create_button('MENTIR', font, 412, 375, 150, 45)
    silent_button = create_button('CALLAR', font, 300, 450, 150, 45)
    return confess_button, lie_button, silent_button

# Game 4-5 screen
def game_4_5_screen():

    global round_count, years
    screen.blit(game_background, (0, 0))

    # Texts (counters)
    draw_text(f'Ronda: {round_count}', font, WHITE, screen, 232, 80)
    draw_text(f'Años: {years}', font, WHITE, screen, 528, 80)

    # Buttons
    confess_button = create_button('CONFESAR', font, 188, 375, 150, 45)
    lie_button = create_button('MENTIR', font, 412, 375, 150, 45)
    return confess_button, lie_button

# Continue playing screen
def continue_screen():

    global round_count, years, pc_choices, veredict
    screen.blit(pc_background, (0, 0))

    # Texts (counters)
    draw_text(f'Ronda: {round_count}', font, WHITE, screen, 232, 80)
    draw_text(f'Años: {years}', font, WHITE, screen, 528, 80)
    draw_text(f'¿Quieres seguir jugando?', font, WHITE, screen, 375, 290)

    # Buttons
    no_button = create_button('NO', font, 300, 375, 50, 45)
    yes_button = create_button('SÍ', font, 400, 375, 50, 45)
    return no_button, yes_button

# PC turn screen
def pc_screen():

    global round_count, years, pc_choices, veredict
    screen.blit(pc_background, (0, 0))

    # Texts (counters)
    draw_text(f'Ronda: {round_count}', font, WHITE, screen, 232, 80)
    draw_text(f'Años: {years}', font, WHITE, screen, 528, 80)
    draw_text(f'La PC ha decidido: {pc_choices[-1]}', font, WHITE, screen, 375, 266)
    draw_text(f'Sentencia: {veredict} años', font, WHITE, screen, 375, 308)

# Game over screen
def end_screen():

    global years, round_count
    screen.blit(end_background, (0, 0))
    draw_text('GAME OVER...', font, WHITE, screen, 375, 420)
    if years == 0:
        draw_text('¡Quedaste libre!', font, WHITE, screen, 375, 472)
        draw_text(f'Recibes: {get_exit_results()} (Round {round_count})', font, WHITE, screen, 375, 532)
    else:
        draw_text(f'Condena final: {years} años', font, WHITE, screen, 375, 472)
        draw_text(f'Recibes: {get_exit_results()} ', font, WHITE, screen, 375, 532)


'''
***** GAME LOGIC UTILS ***** 
'''

# PC random choice
def pc_random_choice():

    w_1 = random.randint(1,100)
    w_2 = random.randint(-20, 20)
    odds = w_1 + w_2

    if odds < 1:
        odds = 1
    elif odds > 100:
        odds = 100

    if (odds >= 1) and (odds < 61):
        return 'CONFESAR'
    elif odds < 75:
        return 'CALLAR'
    else: 
        return 'MENTIR'

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
                    current_screen = 'crime_1'
                    pygame.time.delay(200)

            # Crime 1
            elif current_screen == 'crime_1' and event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    current_screen = 'game_1_3'
                    pygame.time.delay(200)
            
            # Crime 2
            elif current_screen == 'crime_2' and event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    current_screen = 'game_1_3'
                    pygame.time.delay(200)
            
            # Crime 3
            elif current_screen == 'crime_3' and event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    current_screen = 'game_1_3'
                    pygame.time.delay(200)
            
            # Crime 4
            elif current_screen == 'crime_4' and event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    current_screen = 'game_4_5'
                    pygame.time.delay(200)
            
            # Crime 5
            elif current_screen == 'crime_5' and event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    current_screen = 'game_4_5'
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

                if round_count in (1, 2, 3, 4):
                    current_screen = 'continue'
                else:
                    current_screen = 'end'

            # Continue playing
            elif current_screen == 'continue' and event.type == pygame.MOUSEBUTTONDOWN:
                
                pygame.time.delay(200)

                if no_button.collidepoint(event.pos):
                    current_screen = 'end'

                elif yes_button.collidepoint(event.pos):

                    round_count += 1
                    years += 3

                    if round_count == 2:
                        current_screen = 'crime_2'
                    elif round_count == 3:
                        current_screen = 'crime_3'
                    elif round_count == 4:
                        current_screen = 'crime_4'
                    elif round_count == 5:
                        current_screen = 'crime_5'

            # End of game
            elif current_screen == 'end' and event.type == pygame.MOUSEBUTTONDOWN:
                pygame.time.delay(800)
                pygame.quit()
                sys.exit()

        # Render screens
        if current_screen == 'welcome':
            start_button = welcome_screen()
        elif current_screen == 'crime_1':
            continue_button = crime_1_screen()
        elif current_screen == 'crime_2':
            continue_button = crime_2_screen()
        elif current_screen == 'crime_3':
            continue_button = crime_3_screen()
        elif current_screen == 'crime_4':
            continue_button = crime_4_screen()
        elif current_screen == 'crime_5':
            continue_button = crime_5_screen()
        elif current_screen == 'game_1_3':
            confess_button, lie_button, silent_button = game_1_3_screen()
        elif current_screen == 'game_4_5':
            confess_button, lie_button = game_4_5_screen()
        elif current_screen == 'continue':
            no_button, yes_button = continue_screen()
        elif current_screen == 'pc_turn':
            pc_screen()
        elif current_screen == 'end':
            end_screen()

        pygame.display.flip()


# Invoke game loop
game_loop()
