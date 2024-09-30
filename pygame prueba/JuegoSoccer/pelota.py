import os
import pygame

class Ball:
    def __init__(self, x, y, radius):
        self.radius = radius
        self.rect = pygame.Rect(x, y, radius * 2, radius * 2)
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 0.2  # Fuerza de gravedad
        self.rebound_factor = 0.9  # Factor de rebote (0 < factor < 1)

        # Obtener el directorio del script actual
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construir la ruta a los sprites de la pelota
        self.original_sprites = [
            pygame.image.load(os.path.join(script_dir, "assets/pelota", f"{i}.png")).convert_alpha()
            for i in range(1, 7)
        ]
        
        # Escalar los sprites a un tamaño adecuado
        self.sprites = [pygame.transform.scale(sprite, (radius * 2, radius * 2)) for sprite in self.original_sprites]
        
        self.current_sprite_index = 0
        self.sprite_animation_speed = 0.1  # Controla la velocidad de la animación
        self.sprite_timer = 0

    def move(self, ground_level):
        # Aplicar gravedad
        self.velocity_y += self.gravity

        # Mover la pelota
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Colisión con el suelo
        if self.rect.y >= ground_level - self.radius:
            self.rect.y = ground_level - self.radius  # Ajustar la posición para que no se hunda
            self.velocity_y = -self.velocity_y * self.rebound_factor  # Rebotar en el suelo

        # Rebote en los bordes laterales
        if self.rect.x < 0 or self.rect.x > 1920 - self.radius * 2:
            self.velocity_x = -self.velocity_x * 0.9  # Rebote en los bordes laterales (con un pequeño damping)
            self.rect.x = max(0, min(self.rect.x, 1920 - self.radius * 2))  # Mantener dentro de la pantalla

        # Rebote en el techo
        if self.rect.y < 0:
            self.rect.y = 0
            self.velocity_y = -self.velocity_y * self.rebound_factor  # Rebote en el techo (con un pequeño damping)

    def kick(self, impulse_x, impulse_y):
        self.velocity_x += impulse_x
        self.velocity_y += impulse_y

    def draw(self, screen):
        # Dibujar el sprite actual de la pelota
        current_sprite = self.sprites[self.current_sprite_index]
        screen.blit(current_sprite, (self.rect.x, self.rect.y))
        
        # Actualizar el índice del sprite para animación
        self.sprite_timer += self.sprite_animation_speed
        if self.sprite_timer >= 1:
            self.sprite_timer = 0
            self.current_sprite_index = (self.current_sprite_index + 1) % len(self.sprites)

    def reset_position(self):
        self.rect.x = 960  # Reajustar la posición inicial en el centro
        self.rect.y = 540
        self.velocity_x = 0
        self.velocity_y = 0
