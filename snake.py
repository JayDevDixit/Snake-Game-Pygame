import pygame
import random
import time
pygame.init()
pygame.mixer.init()
screen_width = 800
screen_height = 500
info = pygame.display.Info()
full_screen_width = info.current_w
full_screen_height = info.current_h
rate = 5






# game_window = pygame.display.set_mode((screen_width, screen_height),pygame.SCALED | pygame.FULLSCREEN)
game_window = pygame.display.set_mode((screen_width, screen_height),pygame.NOFRAME)
full_screen = False






pygame.display.set_caption('Snake Game')
font = pygame.font.SysFont(None, 40)
exit_game = False
# Colors
white = (255, 255, 255)
red = (255, 0, 0)
green = [0, 255, 0]
blue = (0, 0, 255)
black = (0, 0, 0)
yellow = (255,255,0)



# To display Text on Game Window


def print_text(text, color, x, y):
    text = font.render(text, True, color)
    game_window.blit(text, [x, y])


global play


def welcome_screen():
    global rate
    global game_window
    global screen_width
    global screen_height
    global full_screen
    snake_img = pygame.image.load('pic1.jpg')
    snake_img = pygame.transform.scale(snake_img,(screen_width,screen_height)).convert_alpha()
    game_window.blit(snake_img,(0,0))
    global play
    play = False
    print_text('Snake Game Press Enter to Play..',
               green, screen_width/6, screen_height/3)
    print_text('Press F to Full Screen..',
               green, screen_width/4, screen_height/2)
    

    call_welcome_screen = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    play = True
                    return
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_f:
                    full_screen = not full_screen
                    if full_screen:
                        screen_width = full_screen_width
                        screen_height = full_screen_height
                        game_window = pygame.display.set_mode((screen_width, screen_height),pygame.SCALED | pygame.FULLSCREEN)
                        rate = 10
                        call_welcome_screen = True
                    else:
                        screen_width = 800
                        screen_height = 500
                        game_window = pygame.display.set_mode((screen_width, screen_height),pygame.NOFRAME)
                        rate = 5
                        call_welcome_screen = True
        if call_welcome_screen:
            break
        pygame.display.update()
    if call_welcome_screen:
        welcome_screen()



def play_game():
    # Snake
    snk_head_x = random.randint(50, screen_width-50)
    snk_head_y = random.randint(50, screen_height-50)
    vel_x = rate
    vel_y = 0
    snk = []
    snk_length = 5
    snk_width = 15
    score = 0
    game_over = False

    # Food
    food_x = random.randint(50, screen_width-50)
    food_y = random.randint(50, screen_height-50)
    food_size = 20

    fps = 20
    clock = pygame.time.Clock()
    global high_score
    try:
        with open('highscore.txt','r') as f:
           high_score = int(f.read())
    except:
        with open('highscore.txt','w') as f:
            f.write('0')
            high_score = 0
    global snake_img
    snake_img = pygame.image.load('pic2.jpg')
    snake_img = pygame.transform.scale(snake_img,(screen_width,screen_height)).convert_alpha()

    while not game_over:
       
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.load('hiss.mp3')
            pygame.mixer.music.play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    vel_x = rate
                    vel_y = 0
                if event.key == pygame.K_LEFT:
                    vel_x = -rate
                    vel_y = 0
                if event.key == pygame.K_UP:
                    vel_y = -rate
                    vel_x = 0
                if event.key == pygame.K_DOWN:
                    vel_y = rate
                    vel_x = 0
                if event.key == pygame.K_f:
                    fps+=5
                if event.key == pygame.K_s:
                    if fps>20:
                        fps-=5
                if event.key == pygame.K_SPACE:
                    game_over = True
                    pygame.mixer.music.pause()

                if event.key == pygame.K_q:
                    score+=10
                if event.key == pygame.K_w:
                    score-=10
                if event.key == pygame.K_l:
                    snk_length+=25

        snk_head_x += vel_x
        snk_head_y += vel_y

        if snk_head_x >= screen_width:
            snk_head_x = 0
        if snk_head_x < 0:
            snk_head_x = screen_width
        if snk_head_y >= screen_height:
            snk_head_y = 0
        if snk_head_y < 0:
            snk_head_y = screen_height

        snk.append([snk_head_x, snk_head_y])
        if len(snk) > snk_length:
            del snk[0]

        draw_snake(snk, green, snk_width)
        draw_food(food_x, food_y, food_size, red)
        if (abs(food_x-snk_head_x) < 14 and abs(food_y-snk_head_y) < 14):
            pygame.mixer.music.load('swallow.mp3')
            pygame.mixer.music.play()
            score += 10
            if score>high_score:
                high_score = score
            fps+=5
            snk_length += 10
            food_x = random.randint(50, screen_width-50)
            food_y = random.randint(50, screen_height-50)
        print_text(f"Score : {score} and High Score : {high_score}", red, 0, 0)
        clock.tick(fps)
        pygame.display.update()
        # print(snk_head_x,snk_head_y,snk[:-1])

        if [snk_head_x, snk_head_y] in snk[:-1]:
            # print(snk_head_x,snk_head_y,snk[:-1])
            pygame.mixer.music.load('crash.mp3')
            pygame.mixer.music.play()
            game_over = True
            time.sleep(2)

    if game_over:
        game_over_screen(score,high_score)


def draw_snake(snk, color, snk_width):
    game_window.fill(black)
    game_window.blit(snake_img,(0,0))
    snake_color = color.copy()
    subtractor = 1
    
    for x, y in snk:
        if snake_color[1] > 80:
            snake_color[1]-=subtractor
       
        pygame.draw.rect(game_window, snake_color, (x, y, snk_width, snk_width))


def draw_food(food_x, food_y, food_size, color):
    pygame.draw.rect(game_window, color,
                     (food_x, food_y, food_size, food_size))


def game_over_screen(score,high_score):
    snake_img = pygame.image.load('pic4.png')
    snake_img = pygame.transform.scale(snake_img,(screen_width,screen_height)).convert_alpha()
    game_window.blit(snake_img,(0,0))
    print_text(f'Game Over Your Score is {score}',yellow, screen_width/2, screen_height/6)
    print_text('Press Enter To Play Again',yellow, screen_width/2, screen_height/4)
    print_text(f'High Score : {high_score}',yellow, screen_width/2, screen_height/3)

    with open('highscore.txt','w') as f:
        f.write(str(high_score))

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    play_game()
                if event.key == pygame.K_SPACE:
                    return


welcome_screen()
if play:
    play_game()

pygame.quit()
quit()
