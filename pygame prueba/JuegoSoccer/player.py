import pygame

class Player:
    def __init__(self, x, y, color, controls, sprite_paths):
        # Inicialización de posición y tamaño del jugador
        self.rect = pygame.Rect(x, y, 80, 150)
        self.color = color  # Color del jugador para identificarlo
        self.controls = controls  # Diccionario de controles para moverse y patear
        self.speed_x = 6  # Velocidad de movimiento horizontal
        self.jump_speed = 25  # Velocidad de salto
        self.gravity = 1  # Gravedad aplicada en cada fotograma
        self.speed_y = 0  # Velocidad vertical inicial
        self.on_ground = True  # Indica si el jugador está en el suelo o en el aire
        
        # Carga de los sprites del jugador a partir de las rutas de imagen proporcionadas
        self.sprites = [
            pygame.image.load(path).convert_alpha()
            for path in sprite_paths  # Convierte cada imagen con transparencia
        ]
        self.current_sprite = 0  # Índice para animación del sprite actual

    def move(self, keys, ground_level, ball):
        # Movimiento horizontal del jugador según los controles
        if keys[self.controls['left']]:
            self.rect.x -= self.speed_x
        if keys[self.controls['right']]:
            self.rect.x += self.speed_x

        # Salto del jugador si está en el suelo
        if keys[self.controls['up']] and self.on_ground:
            self.speed_y = -self.jump_speed  # Iniciar el salto con velocidad negativa
            self.on_ground = False  # Indica que ya no está en el suelo

        # Aplicar la gravedad al movimiento vertical
        self.speed_y += self.gravity
        self.rect.y += self.speed_y

        # Verificar colisión con el suelo y ajustar posición
        if self.rect.bottom >= ground_level:
            self.rect.bottom = ground_level  # Ajusta la posición al nivel del suelo
            self.speed_y = 0  # Reinicia la velocidad vertical
            self.on_ground = True  # Indica que está en el suelo

        # Restricciones para mantener al jugador dentro de los límites de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1920:
            self.rect.right = 1920
        if self.rect.y >= ground_level - 150:
            self.rect.y = ground_level - 150  # Ajusta la posición si cae demasiado bajo
            self.on_ground = True
            self.speed_y = 0
        if self.rect.y < 0:
            self.rect.y = 0  # Evita que el jugador se salga por la parte superior
            self.speed_y = 0

        # Colisión con la pelota
        if self.rect.colliderect(ball.rect):
            # Si el control de patear está activo, aplica un golpe
            if keys[self.controls['kick']]:
                self.kick(ball)
            else:
                # De lo contrario, solo rebota la pelota
                self.bounce(ball)

    def kick(self, ball):
        # Aplica un impulso a la pelota dependiendo del color del jugador (lado)
        if self.color == (0, 128, 0):  # Jugador verde
            ball.kick(15, -10)
        elif self.color == (0, 0, 128):  # Jugador azul
            ball.kick(-15, -10)

    def bounce(self, ball):
        # Rebota la pelota con una pequeña fuerza, dependiendo del lado del jugador
        ball.kick(3 if self.color == (0, 128, 0) else -3, -3)

    def draw(self, surface):
        # Dibuja el sprite actual del jugador en la posición del rectángulo
        sprite_image = self.sprites[int(self.current_sprite)]
        
        # Ajusta el sprite para alinearlo con la parte inferior del rectángulo
        offset = 70  # Ajuste para centrar el sprite en la posición correcta
        sprite_rect = sprite_image.get_rect(center=(self.rect.centerx, self.rect.bottom - offset))
        surface.blit(sprite_image, sprite_rect.topleft)

        # Actualiza el sprite actual para la animación
        self.current_sprite += 0.1  # Controla la velocidad de animación
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0  # Reinicia el ciclo de sprites
