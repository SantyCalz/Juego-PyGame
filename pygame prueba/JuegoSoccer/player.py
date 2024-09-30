import pygame

class Player:
    def __init__(self, x, y, color, controls, sprite_paths):
        self.rect = pygame.Rect(x, y, 80, 150)  # Tamaño y posición del jugador
        self.color = color
        self.controls = controls
        self.speed_x = 6
        self.jump_speed = 25
        self.gravity = 1
        self.speed_y = 0
        self.on_ground = True
        
        # Carga de las imágenes de los sprites a partir de las rutas
        self.sprites = [
            pygame.image.load(path).convert_alpha()
            for path in sprite_paths  # Cargar imágenes desde las rutas proporcionadas
        ]
        self.current_sprite = 0

    def move(self, keys, ground_level, ball):
        if keys[self.controls['left']]:
            self.rect.x -= self.speed_x
        if keys[self.controls['right']]:
            self.rect.x += self.speed_x
        if keys[self.controls['up']] and self.on_ground:
            self.speed_y = -self.jump_speed
            self.on_ground = False

        # Aplicar gravedad
        self.speed_y += self.gravity
        self.rect.y += self.speed_y

        # Verificar colisión con el piso
        if self.rect.bottom >= ground_level:
            self.rect.bottom = ground_level
            self.speed_y = 0
            self.on_ground = True

        # Colisión con bordes de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1920:
            self.rect.right = 1920
        if self.rect.y >= ground_level - 150:  # Ajustamos la altura
            self.rect.y = ground_level - 150
            self.on_ground = True
            self.speed_y = 0
        if self.rect.y < 0:
            self.rect.y = 0
            self.speed_y = 0

        # Colisión con la pelota
        if self.rect.colliderect(ball.rect):
            if keys[self.controls['kick']]:
                self.kick(ball)
            else:
                self.bounce(ball)

    def kick(self, ball):
        if self.color == (0, 128, 0):
            ball.kick(15, -10)
        elif self.color == (0, 0, 128):
            ball.kick(-15, -10)

    def bounce(self, ball):
        ball.kick(3 if self.color == (0, 128, 0) else -3, -3)

    def draw(self, surface):
        # Dibuja el sprite actual del jugador en la posición del rectángulo
        sprite_image = self.sprites[int(self.current_sprite)]
        
        # Dibuja el sprite alineado con la parte inferior del rectángulo
        offset = 70
        sprite_rect = sprite_image.get_rect(center=(self.rect.centerx, self.rect.bottom - offset))
        surface.blit(sprite_image, sprite_rect.topleft)

        # Actualiza el sprite actual para la animación
        self.current_sprite += 0.1  # Cambia la velocidad de animación aquí
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
