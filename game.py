import pygame
from tetris import Tetris
from block import colors

pygame.mixer.init()

# Carregar a música de fundo
pygame.mixer.music.load("tetris-theme-classical.mp3")  # Substitua pelo caminho correto
pygame.mixer.music.set_volume(0.5)  # Ajusta o volume (0.0 a 1.0)
pygame.mixer.music.play(-1)  # Reproduz em loop

# Configurações gerais
zoom = 35
fieldHeight = 20
fieldWidth = 10
highscore = 0

screenWidth = fieldWidth * zoom + 300
screenHeight = fieldHeight * zoom + 100

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Tetris")

done = False
clock = pygame.time.Clock()
fps = 20

# Paleta de cores
background_color = (30, 30, 60)
button_color = (70, 130, 180)
button_hover_color = (100, 149, 237)
text_color = (255, 255, 255)
title_color = (255, 215, 0)


font = "Comic Sans MS"
def drawText(size, text, blit, functionColor=None):
    sysFont = pygame.font.SysFont(font, size, True, False)
    
    if functionColor is None:
        renderedText = sysFont.render(text, True, text_color)
    else:
        renderedText = sysFont.render(text, True, functionColor)

    screen.blit(renderedText, blit)

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
    options = ["Jogar", "Controles", "Sair"]
    selected = 0

    while menu_running:
        screen.fill(background_color)

        # Título
        drawText(60, "TETRIS", [screenWidth // 2 - 115, 90], title_color)

        drawText(30, 'BLNV Games Team', [screenWidth // 2 - 130, 450])
        drawText(20, 'Vitor Barroso Rodrigues', [screenWidth // 2 - 280, 550])
        drawText(20, 'Bruno Gabriel Rodrigues', [screenWidth // 2 + 30, 550])
        drawText(20, 'Leonardo Martelli', [screenWidth // 2 - 280, 650])
        drawText(20, 'Nathan Golçalves Lopes', [screenWidth // 2 + 30, 650])

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
    global highscore
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
                    game.__init__(fieldHeight, fieldWidth, zoom)
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
        
        if game.next_block is not None:
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in game.next_block.image():
                        pygame.draw.rect(screen, colors[game.next_block.color],
                            [fieldWidth * zoom + 150 + zoom * j, 150 + zoom * i, zoom - 4, zoom - 4]) 

        # Exibir na tela
        
        drawText(25, ("Highscore: " + str(highscore)), [fieldWidth * zoom + 125, 50])
        drawText(25, ("Pontuação: " + str(game.score)), [fieldWidth * zoom + 125, 90])

        # Desenhar o título da próxima peça
        drawText(25, "Próxima peça", [fieldWidth * zoom + 130, 300]) 
        
        # Game-over
        if game.state == "gameover":
            drawText(65, "Game Over", [screenWidth // 2 - 150, screenHeight // 2 - 50])
            drawText(30, "ESC para reiniciar", [screenWidth // 2 - 100, screenHeight // 2 + 20])

        if game.score > highscore:
                highscore = game.score

        pygame.display.flip()
        clock.tick(fps)

        # Tela de controles
def show_controls():
    controls_running = True

    while controls_running:
        screen.fill(background_color)

        # Título
        drawText(60, "Controles", [screenWidth // 2 - 150, 50], title_color)

        # Texto dos controles
        font_text = pygame.font.SysFont("Comic Sans MS", 25)
        controls = [
            "Setas Esquerda/Direita: Mover peça",
            "Seta Cima: Girar peça",
            "Seta Baixo: Acelerar queda",
            "Espaço: Queda rápida",
            "ESC: Reiniciar jogo",
        ]
        for i, line in enumerate(controls):
            text_surface = font_text.render(line, True, text_color)
            text_rect = text_surface.get_rect(center=(screenWidth // 2, 150 + i * 40))
            screen.blit(text_surface, text_rect)

        # Mensagem para voltar
        back_message = font_text.render("Pressione ESC para voltar", True, text_color)
        back_rect = back_message.get_rect(center=(screenWidth // 2, screenHeight - 50))
        screen.blit(back_message, back_rect)

        # Processar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    controls_running = False

        pygame.display.flip()
        clock.tick(60)


# Loop principal
while not done:
    
    option = main_menu()
    
    if option == "jogar":
        play_game()
    elif option == "controles":
        show_controls()
    elif option == "sair" or option == "exit":
        done = True


pygame.quit()
