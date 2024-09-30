import pygame
from juego import Game  # Importa la clase Game

# Inicialización de Pygame
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

def main():
    ground_level = 1080  # Establecer el nivel del suelo
    game = Game(screen, ground_level)  # Crear instancia del juego directamente

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        game.run()  # Ejecutar el juego

        pygame.display.flip()  # Actualizar la pantalla
        clock.tick(60)

if __name__ == "__main__":
    main()
