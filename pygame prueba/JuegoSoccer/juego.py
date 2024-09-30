import os
import pygame
import sys
from player import Player
from pelota import Ball

# Definir dimensiones de la pantalla
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

class Game:
    def __init__(self, screen, ground_level):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.ground_level = ground_level
        self.ball = Ball(960, ground_level - 30, 30)

        player1_controls = {
            'left': pygame.K_a,
            'right': pygame.K_d,
            'up': pygame.K_w,
            'down': pygame.K_s,
            'kick': pygame.K_SPACE
        }

        player2_controls = {
            'left': pygame.K_j,
            'right': pygame.K_l,
            'up': pygame.K_i,
            'down': pygame.K_k,
            'kick': pygame.K_RETURN
        }

        # Obtener el directorio del script actual
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Rutas de los sprites para los jugadores usando rutas relativas
        player1_sprites = [
            os.path.join(script_dir, "assets/sprites messi", f"{i}.png") for i in range(1, 7)
        ]

        player2_sprites = [
            os.path.join(script_dir, "assets/sprite ronaldo", f"{i}.png") for i in range(1, 7)
        ]

        self.player1 = Player(100, ground_level - 50, (0, 128, 0), player1_controls, player1_sprites)
        self.player2 = Player(1800, ground_level - 50, (0, 0, 128), player2_controls, player2_sprites)

        self.score1 = 0
        self.score2 = 0
        self.goal_width = 100
        self.goal_height = 200
        self.goal1 = pygame.Rect(0, self.ground_level - self.goal_height, self.goal_width, self.goal_height)
        self.goal2 = pygame.Rect(SCREEN_WIDTH - self.goal_width, self.ground_level - self.goal_height, self.goal_width, self.goal_height)

        # Cargar la imagen de fondo
        self.background = pygame.image.load(os.path.join(script_dir, "assets/Fondo.png")).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Escalar a las dimensiones de la pantalla

        # Cargar las imágenes de los arcos
        self.goal1_image = pygame.image.load(os.path.join(script_dir, "assets/arco izq.png")).convert_alpha()
        self.goal2_image = pygame.image.load(os.path.join(script_dir, "assets/arco der.png")).convert_alpha()

        # Escalar las imágenes si es necesario (opcional)
        self.goal1_image = pygame.transform.scale(self.goal1_image, (self.goal_width, self.goal_height))
        self.goal2_image = pygame.transform.scale(self.goal2_image, (self.goal_width, self.goal_height))

        # Temporizador
        self.time_limit = 60  # 60 segundos
        self.start_time = pygame.time.get_ticks()  # Tiempo de inicio
        self.game_over = False  # Estado del juego
        self.winner = None  # Almacena el ganador

    # Resto de la clase permanece igual...

    def check_goal(self):
        if self.ball.rect.colliderect(self.goal1):
            if self.ball.rect.right > self.goal1.left and self.ball.rect.left < self.goal1.right:
                if self.ball.rect.bottom < self.goal1.top:
                    self.ball.velocity_y = -self.ball.velocity_y * 0.9
                else:
                    self.score2 += 1
                    self.ball.reset_position()

        if self.ball.rect.colliderect(self.goal2):
            if self.ball.rect.right > self.goal2.left and self.ball.rect.left < self.goal2.right:
                if self.ball.rect.bottom < self.goal2.top:
                    self.ball.velocity_y = -self.ball.velocity_y * 0.9
                else:
                    self.score1 += 1
                    self.ball.reset_position()

    def handle_collision(self, keys):
        if keys[self.player1.controls['kick']] and self.ball.rect.colliderect(self.player1.rect):
            self.ball.kick(10, -15)

        if keys[self.player2.controls['kick']] and self.ball.rect.colliderect(self.player2.rect):
            self.ball.kick(-10, -15)

    def display_winner(self):
        font = pygame.font.SysFont('Arial', 50)
        if self.winner:
            winner_text = font.render(f'The winner is: {self.winner}', True, (0, 0, 0))
        else:
            winner_text = font.render(f'It\'s a draw!', True, (0, 0, 0))

        self.screen.fill((255, 255, 255))  # Limpiar la pantalla
        self.screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)  # Esperar 3 segundos antes de regresar al menú

    def reset_game(self):
        self.score1 = 0
        self.score2 = 0
        self.ball.reset_position()
        self.game_over = False
        self.winner = None

    def show_menu(self):
        font = pygame.font.SysFont('Arial', 50)
        self.screen.fill((255, 255, 255))  # Limpiar pantalla
        title_text = font.render('Welcome to the Football Game!', True, (0, 0, 0))
        start_text = font.render('Press ENTER to start', True, (0, 0, 0))
        exit_text = font.render('Press ESC to exit', True, (0, 0, 0))
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 150))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Iniciar el juego
                        self.start_time = pygame.time.get_ticks()  # Reiniciar el tiempo aquí
                        waiting = False
                    if event.key == pygame.K_ESCAPE:  # Salir del juego
                        pygame.quit()
                        sys.exit()

    def run(self):
        self.show_menu()  # Mostrar el menú al iniciar el juego
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

                if self.ball.rect.bottom >= self.ground_level:
                    self.ball.rect.bottom = self.ground_level
                    self.ball.velocity_y = 0

                self.handle_collision(keys)
                self.check_goal()

                # Lógica del temporizador
                elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000  # Tiempo transcurrido en segundos
                time_left = self.time_limit - elapsed_time

                if time_left <= 0:
                    # Si el tiempo se acabó, determina el ganador
                    if self.score1 > self.score2:
                        self.winner = "Player 1"
                    elif self.score2 > self.score1:
                        self.winner = "Player 2"
                    else:
                        self.winner = None  # Es un empate
                    self.game_over = True  # Termina el juego

                # Dibuja la imagen de fondo
                self.screen.blit(self.background, (0, 0))

                # Dibuja las imágenes de los arcos en las posiciones de goal1 y goal2
                self.screen.blit(self.goal1_image, (self.goal1.x, self.goal1.y))
                self.screen.blit(self.goal2_image, (self.goal2.x, self.goal2.y))

                self.player1.draw(self.screen)  # Dibuja el jugador 1
                self.player2.draw(self.screen)  # Dibuja el jugador 2
                self.ball.draw(self.screen)  # Dibuja la pelota

                # Mostrar el tiempo restante
                font = pygame.font.SysFont('Arial', 30)
                timer_text = font.render(f'Time Left: {int(time_left)}s', True, (0, 0, 0))
                self.screen.blit(timer_text, (800, 60))

                # Mostrar puntaje
                score_text = font.render(f'Score: {self.score1} - {self.score2}', True, (0, 0, 0))
                self.screen.blit(score_text, (800, 20))

                pygame.display.flip()
                self.clock.tick(60)
            else:
                self.display_winner()  # Mostrar ganador o empate
                self.reset_game()  # Reiniciar el juego después de mostrar el ganador o empate
                self.show_menu()  # Volver al menú
