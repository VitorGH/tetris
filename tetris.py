import pygame
import random

# Lista de cores para os blocos
colors = [
    (0, 0, 0),  # Cor para o fundo
    (120, 37, 179),  # Cor para um tipo de bloco
    (100, 179, 179),  # Cor para outro tipo de bloco
    (80, 34, 22),  # Cor para outro tipo de bloco
    (80, 134, 22),  # Cor para outro tipo de bloco
    (180, 34, 22),  # Cor para outro tipo de bloco
    (180, 34, 122),  # Cor para outro tipo de bloco
]

# Classe que representa uma figura (bloco) do Tetris
class Figure:
    x = 0  # Posição x da figura
    y = 0  # Posição y da figura

    # Lista de figuras possíveis e suas rotações
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],  # Figura 1
        [[4, 5, 9, 10], [2, 6, 5, 9]],  # Figura 2
        [[6, 7, 9, 10], [1, 5, 6, 10]],  # Figura 3
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # Figura 4
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # Figura 5
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # Figura 6
        [[1, 2, 5, 6]],  # Figura 7
    ]

    def __init__(self, x, y):
        self.x = x  # Inicializa a posição x da figura
        self.y = y  # Inicializa a posição y da figura
        self.type = random.randint(0, len(self.figures) - 1)  # Escolhe aleatoriamente um tipo de figura
        self.color = random.randint(1, len(colors) - 1)  # Escolhe uma cor aleatoriamente
        self.rotation = 0  # Inicializa a rotação da figura

    def image(self):
        # Retorna a imagem da figura com base no tipo e na rotação
        return self.figures[self.type][self.rotation]

    def rotate(self):
        # Altera a rotação da figura
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


# Classe que representa o jogo Tetris
class Tetris:
    def __init__(self, height, width, zoom):
        self.level = 2  # Nível do jogo
        self.score = 0  # Pontuação do jogador
        self.state = "start"  # Estado do jogo (início)
        self.field = []  # Campo do jogo
        self.height = height  # Altura do campo
        self.width = width  # Largura do campo
        self.x = 100  # Posição x do campo na tela
        self.y = 60  # Posição y do campo na tela
        self.zoom = zoom  # Tamanho de cada bloco (aumentado para melhorar a visibilidade)
        self.figure = None  # Figura atual do jogo

        # Cria o campo de jogo preenchido com zeros
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        # Cria uma nova figura
        self.figure = Figure(3, 0)

    def intersects(self):
        # Verifica se a figura atual colide com o campo ou com outras figuras
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        # Verifica e remove linhas completas do campo
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                # Move as linhas acima da linha removida para baixo
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2  # Aumenta a pontuação

    def go_space(self):
        # Move a figura para baixo até o final do campo
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1  # Ajusta a posição
        self.freeze()  # Congela a figura no campo

    def go_down(self):
        # Move a figura para baixo
        self.figure.y += 1
        if self.intersects():  # Se houver colisão
            self.figure.y -= 1  # Ajusta a posição
            self.freeze()  # Congela a figura

    def freeze(self):
        # Congela a figura no campo
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()  # Verifica e quebra linhas
        self.new_figure()  # Cria uma nova figura
        if self.intersects():  # Se houver colisão com a nova figura
            self.state = "gameover"  # O jogo termina

    def go_side(self, dx):
        # Move a figura para os lados
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():  # Se houver colisão
            self.figure.x = old_x  # Retorna à posição anterior

    def rotate(self):
        # Rotaciona a figura
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():  # Se houver colisão após a rotação
            self.figure.rotation = old_rotation  # Retorna à rotação anterior


# Configuração dinâmica do tamanho da tela com base no zoom e nas dimensões do campo
zoom = 30
campo_altura = 20
campo_largura = 10

# Calcula o tamanho da tela baseado nas dimensões do campo e no zoom
tela_largura = campo_largura * zoom + 200  # 200 pixels extras para pontuação e margem
tela_altura = campo_altura * zoom + 100    # 100 pixels extras para margem superior e inferior

# Inicializa o motor do jogo
pygame.init()
screen = pygame.display.set_mode((tela_largura, tela_altura))  # Cria a tela do jogo com o tamanho dinâmico
pygame.display.set_caption("Tetris")  # Define o título da janela

# Variáveis de controle do jogo
done = False
clock = pygame.time.Clock()  # Controla o tempo do jogo
fps = 25  # Frames por segundo
game = Tetris(campo_altura, campo_largura, zoom)  # Cria uma instância do jogo Tetris
counter = 0  # Contador para o tempo
pressing_down = False  # Flag para verificar se o botão de baixo está pressionado

while not done:
    if game.figure is None:  # Se não houver figura atual
        game.new_figure()  # Cria uma nova figura
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

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                if i * 4 + j in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
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