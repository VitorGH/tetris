import random

# Lista de cores para os blocos
colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]

class Block:
    x = 0
    y = 0 

    # Lista de figuras possíveis e suas rotações
    blocks = [
        [
            [1, 5, 9, 13], [4, 5, 6, 7]
        ],

        [
            [4, 5, 9, 10], 
            [2, 6, 5, 9]
        ],

        [
            [6, 7, 9, 10], 
            [1, 5, 6, 10]
        ],

        [
            [1, 2, 5, 9], 
            [0, 4, 5, 6], 
            [1, 5, 9, 8], 
            [4, 5, 6, 10]
        ],

        [
            [1, 2, 6, 10], 
            [5, 6, 7, 9], 
            [2, 6, 10, 11], 
            [3, 5, 6, 7]
        ],

        [
            [1, 4, 5, 6], 
            [1, 4, 5, 9], 
            [4, 5, 6, 9], 
            [1, 5, 6, 9]
        ],

        [
            [1, 2, 5, 6]
        ]
    ]

    def __init__(self, x, y):
        # Inicializa a posição x e y do bloco
        self.x = x 
        self.y = y
        # Escolhe aleatoriamente um tipo e cor do bloco
        self.type = random.randint(0, len(self.blocks) - 1)  
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0  # Inicializa a rotação da figura

    def image(self):
        # Retorna a imagem da figura com base no tipo e na rotação
        return self.blocks[self.type][self.rotation]

    def rotate(self):
        # Altera a rotação da figura
        self.rotation = (self.rotation + 1) % len(self.blocks[self.type])