import pygame
from tetris import Tetris
from block import colors

# Configurações gerais
zoom = 30
fieldHeight = 20
fieldWidth = 10

screenWidth = fieldWidth * zoom + 200
screenHeight = fieldHeight * zoom + 100

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Tetris")

done = False
clock = pygame.time.Clock()
fps = 25

# Paleta de cores
background_color = (30, 30, 60)
button_color = (70, 130, 180)
button_hover_color = (100, 149, 237)
text_color = (255, 255, 255)
title_color = (255, 215, 0)

# Função para desenhar botões
def draw_button(screen, text, x, y, width, height, active):
    color = button_hover_color if active else button_color
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=8)
    font = pygame.font.SysFont("Comic Sans MS", 30)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# Menu inicial
def main_menu():
    menu_running = True
    options = ["Jogar", "Sair"]
    selected = 0

    while menu_running:
        screen.fill(background_color)

        # Título
        font = pygame.font.SysFont("Comic Sans MS", 60, True)
        title_surface = font.render("TETRIS", True, title_color)
        title_rect = title_surface.get_rect(center=(screenWidth // 2, 100))
        screen.blit(title_surface, title_rect)

        # Botões do menu
        for i, option in enumerate(options):
            draw_button(screen, option, screenWidth // 2 - 100, 200 + i * 80, 200, 50, i == selected)

        # Processar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                if event.key == pygame.K_RETURN:
                    return options[selected].lower()

        pygame.display.flip()
        clock.tick(60)

# Inicializar jogo
def play_game():
    game = Tetris(fieldHeight, fieldWidth, zoom)
    counter = 0
    pressing_down = False

    while not done:
        if game.block is None:
            game.new_block()
        counter += 1
        if counter > 100000:
            counter = 0

        if counter % (fps // game.level // 2) == 0 or pressing_down:
            if game.state == "start":
                game.go_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_LEFT:
                    game.go_side(-1)
                if event.key == pygame.K_RIGHT:
                    game.go_side(1)
                if event.key == pygame.K_SPACE:
                    game.go_space()
                if event.key == pygame.K_ESCAPE:
                    game.__init__(20, 10, 30)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down = False

        screen.fill(background_color)

        # Desenho do campo e dos blocos
        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, (50, 50, 80),
                                 [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 2)
                if game.field[i][j] > 0:
                    pygame.draw.rect(screen, colors[game.field[i][j]],
                                     [game.x + game.zoom * j + 2, game.y + game.zoom * i + 2, game.zoom - 4, game.zoom - 4])

        if game.block is not None:
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in game.block.image():
                        pygame.draw.rect(screen, colors[game.block.color],
                                         [game.x + game.zoom * (j + game.block.x) + 2,
                                          game.y + game.zoom * (i + game.block.y) + 2,
                                          game.zoom - 4, game.zoom - 4])

        # Exibe a pontuação e estado do jogo
        font = pygame.font.SysFont('Comic Sans MS', 25, True, False)
        text = font.render("Pontuação: " + str(game.score), True, text_color)
        screen.blit(text, [fieldWidth * zoom + 20, 20])
        if game.state == "gameover":
            font1 = pygame.font.SysFont('Comic Sans MS', 65, True, False)
            text_game_over = font1.render("Game Over", True, (255, 50, 50))
            screen.blit(text_game_over, [screenWidth // 2 - 150, screenHeight // 2 - 50])

        pygame.display.flip()
        clock.tick(fps)

# Loop principal
while not done:
    option = main_menu()
    if option == "jogar":
        play_game()
    elif option == "sair" or option == "exit":
        done = True

pygame.quit()
