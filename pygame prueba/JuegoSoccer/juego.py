import os
import pygame
import sys
from player import Player
from pelota import Ball

# Configuración de las dimensiones de la pantalla
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

class Game:
    def __init__(self, screen, ground_level):
        # Configuración inicial del juego
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.ground_level = ground_level
        self.ball = Ball(960, ground_level - 30, 30)  # Crea la pelota en el centro del suelo

        # Controles de los jugadores
        player1_controls = {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s, 'kick': pygame.K_SPACE}
        player2_controls = {'left': pygame.K_j, 'right': pygame.K_l, 'up': pygame.K_i, 'down': pygame.K_k, 'kick': pygame.K_RETURN}

        # Cargar sprites de jugadores desde la carpeta de assets
        script_dir = os.path.dirname(os.path.abspath(__file__))
        player1_sprites = [os.path.join(script_dir, "assets/sprites messi", f"{i}.png") for i in range(1, 7)]
        player2_sprites = [os.path.join(script_dir, "assets/sprite ronaldo", f"{i}.png") for i in range(1, 7)]

        # Crear jugadores con sus posiciones y colores
        self.player1 = Player(100, ground_level - 50, (0, 128, 0), player1_controls, player1_sprites)
        self.player2 = Player(1800, ground_level - 50, (0, 0, 128), player2_controls, player2_sprites)

        # Variables de puntuación y portería
        self.score1 = 0
        self.score2 = 0
        self.goal_width = 100
        self.goal_height = 200
        self.goal1 = pygame.Rect(0, self.ground_level - self.goal_height, self.goal_width, self.goal_height)
        self.goal2 = pygame.Rect(SCREEN_WIDTH - self.goal_width, self.ground_level - self.goal_height, self.goal_width, self.goal_height)

        # Cargar imágenes de fondo y porterías
        self.background = pygame.image.load(os.path.join(script_dir, "assets/Fondo.png")).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.goal1_image = pygame.image.load(os.path.join(script_dir, "assets/arco izq.png")).convert_alpha()
        self.goal2_image = pygame.image.load(os.path.join(script_dir, "assets/arco der.png")).convert_alpha()
        self.goal1_image = pygame.transform.scale(self.goal1_image, (self.goal_width, self.goal_height))
        self.goal2_image = pygame.transform.scale(self.goal2_image, (self.goal_width, self.goal_height))

        # Configuración de tiempo límite y estado de juego
        self.time_limit = 60
        self.start_time = pygame.time.get_ticks()
        self.game_over = False
        self.winner = None

    # Verifica si hay gol y actualiza puntaje
    def check_goal(self):
        if self.ball.rect.colliderect(self.goal1):
            if self.ball.rect.bottom >= self.goal1.top:
                self.score2 += 1
                self.ball.reset_position()  # Reinicia la posición de la pelota

        if self.ball.rect.colliderect(self.goal2):
            if self.ball.rect.bottom >= self.goal2.top:
                self.score1 += 1
                self.ball.reset_position()

    # Maneja colisiones entre la pelota y los jugadores
    def handle_collision(self, keys):
        if keys[self.player1.controls['kick']] and self.ball.rect.colliderect(self.player1.rect):
            self.ball.kick(10, -15)
        if keys[self.player2.controls['kick']] and self.ball.rect.colliderect(self.player2.rect):
            self.ball.kick(-10, -15)

    # Muestra el ganador o si es un empate
    def display_winner(self):
        font = pygame.font.SysFont('Arial', 50)
        winner_text = font.render(f'El ganador es: {self.winner}' if self.winner else 'Empate!', True, (0, 0, 0))
        self.screen.fill((255, 255, 255))
        self.screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)

    # Reinicia el juego a los valores iniciales
    def reset_game(self):
        self.score1 = 0
        self.score2 = 0
        self.ball.reset_position()
        self.game_over = False
        self.winner = None

    # Muestra el menú inicial con opciones de comenzar o salir
    def show_menu(self):
        font = pygame.font.SysFont('Arial', 50)
        self.screen.fill((255, 255, 255))
        title_text = font.render('Bienvenido al juego de Futbol!', True, (0, 0, 0))
        start_text = font.render('Presiona ENTER para empezar', True, (0, 0, 0))
        exit_text = font.render('Presiona ESC para salir', True, (0, 0, 0))
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 150))
        pygame.display.flip()

        # Espera hasta que se presione ENTER o ESC
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.start_time = pygame.time.get_ticks()
                        waiting = False
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    # Ejecución principal del juego
    def run(self):
        self.show_menu()  # Mostrar el menú inicial
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if not self.game_over:
                keys = pygame.key.get_pressed()
                self.player1.move(keys, self.ground_level, self.ball)
                self.player2.move(keys, self.ground_level, self.ball)
                self.ball.move(self.ground_level)

                # Control de colisión con el suelo
                if self.ball.rect.bottom >= self.ground_level:
                    self.ball.rect.bottom = self.ground_level
                    self.ball.velocity_y = 0

                self.handle_collision(keys)  # Manejo de colisiones con jugadores
                self.check_goal()  # Verifica si se marcó gol

                # Actualización del temporizador
                elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
                time_left = self.time_limit - elapsed_time
                if time_left <= 0:
                    # Determina el ganador cuando se acaba el tiempo
                    if self.score1 > self.score2:
                        self.winner = "Player 1"
                    elif self.score2 > self.score1:
                        self.winner = "Player 2"
                    else:
                        self.winner = None  # Empate
                    self.game_over = True

                # Dibujar fondo, arcos, jugadores y puntaje
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.goal1_image, (self.goal1.x, self.goal1.y))
                self.screen.blit(self.goal2_image, (self.goal2.x, self.goal2.y))
                self.player1.draw(self.screen)
                self.player2.draw(self.screen)
                self.ball.draw(self.screen)

                # Mostrar tiempo restante y puntaje
                font = pygame.font.SysFont('Arial', 30)
                timer_text = font.render(f'Tiempo: {int(time_left)}s', True, (0, 0, 0))
                self.screen.blit(timer_text, (800, 60))
                score_text = font.render(f'Puntuación: {self.score1} - {self.score2}', True, (0, 0, 0))
                self.screen.blit(score_text, (800, 20))

                pygame.display.flip()
                self.clock.tick(60)
            else:
                self.display_winner()  # Muestra el resultado
                self.reset_game()  # Reinicia para el próximo juego
                self.show_menu()  # Volver al menú principal
