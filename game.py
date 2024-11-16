import pygame
from tetris import Tetris
from block import colors

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
game = Tetris(fieldHeight, fieldWidth, zoom) 
counter = 0
pressing_down = False

while not done:
    if game.block is None:  # Se não houver figura atual
        game.new_block()  # Cria uma nova figura
    counter += 1
    if counter > 100000:
        counter = 0  # Reseta o contador se for muito alto

    # Se o tempo passar, move a figura para baixo
    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()  # Move a figura para baixo

    # Processa eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True  # Sai do jogo
        if event.type == pygame.KEYDOWN:  # Se uma tecla for pressionada
            if event.key == pygame.K_UP:
                game.rotate()  # Rotaciona a figura
            if event.key == pygame.K_DOWN:
                pressing_down = True  # Ativa a movimentação para baixo
            if event.key == pygame.K_LEFT:
                game.go_side(-1)  # Move para a esquerda
            if event.key == pygame.K_RIGHT:
                game.go_side(1)  # Move para a direita
            if event.key == pygame.K_SPACE:
                game.go_space()  # Muda para o modo de queda rápida
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10, 30)  # Reinicia o jogo
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_DOWN:
            pressing_down = False  # Desativa a movimentação para baixo

    screen.fill((255, 255, 255))  # Limpa a tela

    # Desenha o campo e as figuras
    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, (128, 128, 128),
                             [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.block is not None:
        for i in range(4):
            for j in range(4):
                if i * 4 + j in game.block.image():
                    pygame.draw.rect(screen, colors[game.block.color],
                                     [game.x + game.zoom * (j + game.block.x) + 1,
                                      game.y + game.zoom * (i + game.block.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    # Exibe a pontuação e estado do jogo
    font = pygame.font.SysFont('Calibri', 25, True, False)
    text = font.render("Pontuação: " + str(game.score), True, (0, 0, 0))
    screen.blit(text, [0, 0])
    if game.state == "gameover":
        font1 = pygame.font.SysFont('Calibri', 65, True, False)
        text_game_over = font1.render("Game Over", True, (255, 125, 0))
        screen.blit(text_game_over, [20, 200])

    pygame.display.flip()
    clock.tick(fps)  # Atualiza a tela

pygame.quit()