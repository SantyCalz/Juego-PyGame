import os
import pygame

class Ball:
    def __init__(self, x, y, radius):
        # Inicialización de los parámetros de la pelota
        self.radius = radius
        self.rect = pygame.Rect(x, y, radius * 2, radius * 2)  # Crear un rectángulo para la pelota
        self.velocity_x = 0  # Velocidad inicial en el eje X
        self.velocity_y = 0  # Velocidad inicial en el eje Y
        self.gravity = 0.2  # Fuerza de gravedad
        self.rebound_factor = 0.9  # Factor de rebote (entre 0 y 1)

        # Obtener el directorio del script actual
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Cargar los sprites de la pelota desde la carpeta 'assets/pelota'
        self.original_sprites = [
            pygame.image.load(os.path.join(script_dir, "assets/pelota", f"{i}.png")).convert_alpha()
            for i in range(1, 7)
        ]
        
        # Escalar los sprites a un tamaño adecuado para la pelota
        self.sprites = [pygame.transform.scale(sprite, (radius * 2, radius * 2)) for sprite in self.original_sprites]
        
        self.current_sprite_index = 0  # Índice del sprite actual
        self.sprite_animation_speed = 0.1  # Velocidad de animación
        self.sprite_timer = 0  # Temporizador para controlar el cambio de sprite

    def move(self, ground_level):
        # Aplicar la gravedad a la pelota
        self.velocity_y += self.gravity

        # Mover la pelota según las velocidades en X y Y
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Verificar si la pelota ha llegado al piso
        if self.rect.y >= ground_level - self.radius:
            self.rect.y = ground_level - self.radius  # Ajustar la posición para que no se hunda
            self.velocity_y = -self.velocity_y * self.rebound_factor  # Rebotar la pelota en el piso

        # Rebote en los bordes laterales de la pantalla
        if self.rect.x < 0 or self.rect.x > 1920 - self.radius * 2:
            self.velocity_x = -self.velocity_x * 0.9  # Rebote con una pequeña amortiguacion
            self.rect.x = max(0, min(self.rect.x, 1920 - self.radius * 2))  # Mantener dentro de los límites de la pantalla

        # Rebote en el techo
        if self.rect.y < 0:
            self.rect.y = 0  # Ajustar la posición para que no se salga de la pantalla
            self.velocity_y = -self.velocity_y * self.rebound_factor  # Rebote en el techo con una pequeña amortiguacion

    def kick(self, impulse_x, impulse_y):
        # Aplicar un impulso a la pelota cuando es golpeada
        self.velocity_x += impulse_x
        self.velocity_y += impulse_y

    def draw(self, screen):
        # Dibujar el sprite actual de la pelota en la pantalla
        current_sprite = self.sprites[self.current_sprite_index]
        screen.blit(current_sprite, (self.rect.x, self.rect.y))
        
        # Actualizar el índice del sprite para la animación
        self.sprite_timer += self.sprite_animation_speed
        if self.sprite_timer >= 1:
            self.sprite_timer = 0
            self.current_sprite_index = (self.current_sprite_index + 1) % len(self.sprites)  # Ciclo de sprites

    def reset_position(self):
        # Resetear la posición de la pelota al centro de la pantalla
        self.rect.x = 960  # Posición X centrada
        self.rect.y = 540  # Posición Y centrada
        self.velocity_x = 0  # Resetear la velocidad X
        self.velocity_y = 0  # Resetear la velocidad Y
