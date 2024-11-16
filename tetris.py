from block import Block

class Tetris:
    def __init__(self, height, width, zoom):
        self.level = 2
        self.score = 0
        self.state = "start"
        self.field = []
        self.height = height
        self.width = width
        self.x = 100
        self.y = 60 
        self.zoom = zoom
        self.block = None  

        # Cria o campo de jogo preenchido com zeros
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_block(self):
        self.block = Block(3, 0)

    def intersects(self):
        # Verifica se a figura atual colide com o campo ou com outras figuras
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.image():
                    if i + self.block.y > self.height - 1 or \
                            j + self.block.x > self.width - 1 or \
                            j + self.block.x < 0 or \
                            self.field[i + self.block.y][j + self.block.x] > 0:
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
            self.block.y += 1
        self.block.y -= 1  # Ajusta a posição
        self.freeze()  # Congela a figura no campo

    def go_down(self):
        # Move a figura para baixo
        self.block.y += 1
        if self.intersects():  # Se houver colisão
            self.block.y -= 1  # Ajusta a posição
            self.freeze()  # Congela a figura

    def freeze(self):
        # Congela a figura no campo
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.image():
                    self.field[i + self.block.y][j + self.block.x] = self.block.color
        self.break_lines()  # Verifica e quebra linhas
        self.new_block()  # Cria uma nova figura
        if self.intersects():  # Se houver colisão com a nova figura
            self.state = "gameover"  # O jogo termina

    def go_side(self, dx):
        # Move a figura para os lados
        old_x = self.block.x
        self.block.x += dx
        if self.intersects():  # Se houver colisão
            self.block.x = old_x  # Retorna à posição anterior

    def rotate(self):
        # Rotaciona a figura
        old_rotation = self.block.rotation
        self.block.rotate()
        if self.intersects():  # Se houver colisão após a rotação
            self.block.rotation = old_rotation  # Retorna à rotação anterior