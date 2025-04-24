import tkinter as tk
from PIL import Image, ImageTk
import pygame
import sys
import random
import time

difficulty_levels = {
    "Easy": (4, 4),
    "Medium": (7, 7),
    "Hard": (10, 10)
}

class PingPongGame:
    DEFAULT_PLAYER1_NAME = "Computer"  # Default player 1 name

    def __init__(self, root):
        self.root = root
        self.root.title("Ping Pong Game")
        self.root.geometry("1540x870")

        image_path = r"C:\Users\koushik\Downloads\ping pong.jpg"
        self.load_and_display_image(image_path)

        # Create a frame for the title
        self.title_frame = tk.Frame(root)
        self.title_frame.pack(fill="both", expand=True)

        self.start_button = tk.Button(self.title_frame, text="Start", command=self.show_player_entry, font=("Arial", 18), bg="#333", fg="white")
        self.start_button.pack(pady=20)


    def load_and_display_image(self, image_path):
        try:
            image = Image.open(image_path)
            resized_image = image.resize((1540, 500))  # Resize image to window size (800x600)
            photo = ImageTk.PhotoImage(resized_image)

            canvas = tk.Canvas(self.root, width=1540, height=500)
            canvas.pack()

            canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            canvas.image = photo
        except FileNotFoundError:
            print(f"Error: Image file not found at {image_path}")

    def show_player_entry(self):
        self.title_frame.destroy()

        entry_frame = tk.Frame(self.root, bg="#f0f0f0")
        entry_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.player1_label = tk.Label(entry_frame, text="Player 1:", font=("Arial", 18))
        self.player1_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.player1_entry = tk.Entry(entry_frame, width=30, font=("Arial", 18))
        self.player1_entry.insert(0, self.DEFAULT_PLAYER1_NAME)  # Set default value
        self.player1_entry.config(state='readonly')  # Make it read-only
        self.player1_entry.grid(row=0, column=1, padx=10, pady=10)

        self.player2_label = tk.Label(entry_frame, text="Player 2:", font=("Arial", 18))
        self.player2_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.player2_entry = tk.Entry(entry_frame, width=30, font=("Arial", 18))
        self.player2_entry.grid(row=1, column=1, padx=10, pady=10)

        self.error_message = tk.Label(entry_frame, text="", font=("Arial", 12), fg="red", bg="#f0f0f0")
        self.error_message.grid(row=2, columnspan=2)

        self.start_button = tk.Button(entry_frame, text="Start Game", command=self.start_loading, font=("Arial", 18), bg="#333", fg="white")
        self.start_button.grid(row=3, columnspan=2, pady=20)

    def start_loading(self):
        player2_name = self.player2_entry.get()
        if not player2_name:
            self.error_message.config(text="Player 2 name is required!")
            return

        loading_window = tk.Toplevel(self.root)
        loading_window.title("Loading...")
        loading_window.geometry("400x200")

        loading_label = tk.Label(loading_window, text="Loading...", font=("Arial", 24), fg="blue")
        loading_label.pack(pady=20)

        # Create a canvas for the progress bar
        progress_bar_canvas = tk.Canvas(loading_window, width=300, height=30, bg="white", bd=1, relief="solid")
        progress_bar_canvas.pack(pady=10)

        progress_rect = progress_bar_canvas.create_rectangle(5, 5, 5, 25, fill="blue")

        loading_window.update()

        for i in range(100):
            progress_bar_canvas.coords(progress_rect, 5, 5, 5 + (i * 3), 25)
            loading_window.update()
            time.sleep(0.05)

        loading_window.destroy()
        self.start_game()

    def start_game(self):
        player1_name = self.DEFAULT_PLAYER1_NAME  # Set default player 1 name
        player2_name = self.player2_entry.get()
        self.root.destroy()

        main_pygame_game(player1_name, player2_name)



def main_pygame_game(player1_name, player2_name):
    pygame.init()

    clock = pygame.time.Clock()

    screen_width = 1550
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Pong')

    ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
    player = pygame.Rect(screen_width - 30, screen_height / 2 - 70, 10, 140)
    opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

    bg_color = pygame.Color('grey12')
    light_grey = (200, 200, 200)
    player_color = pygame.Color('dodgerblue')
    opponent_color = pygame.Color('orangered')
    ball_color = pygame.Color('white')
    player_speed = 0
    opponent_speed = 7

    player_score = 0
    opponent_score = 0

    font = pygame.font.Font(None, 50)
    name_font = pygame.font.Font(None, 36)

    start_time = time.time()  # Store the start time

    def ball_animation():
        nonlocal ball_speed_x, ball_speed_y, player_score, opponent_score
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= screen_height:
            ball_speed_y *= -1

        if ball.colliderect(player):
            ball_speed_x = -abs(ball_speed_x)
            player_score += 1
        if ball.colliderect(opponent):
            ball_speed_x = abs(ball_speed_x)
            opponent_score += 1

        # Ball hitting the sides (game over condition)
        if ball.left <= 0:
            game_over(f"{player2_name} wins!")
            return False
        if ball.right >= screen_width:
            game_over(f"{player1_name} wins!")
            return False

        # Draw the ball
        pygame.draw.ellipse(screen, ball_color, ball)

    def game_over(winner):
        # Display winner directly on the game screen
        game_over_text = font.render(winner, True, light_grey)
        screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2 - 50))

        # Draw buttons for Quit and Restart
        quit_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 20, 100, 50)
        pygame.draw.rect(screen, light_grey, quit_button)
        quit_text = font.render("Quit", True, bg_color)
        screen.blit(quit_text, (
        quit_button.centerx - quit_text.get_width() // 2, quit_button.centery - quit_text.get_height() // 2))

        restart_button = pygame.Rect(screen_width // 2 + 20, screen_height // 2 + 20, 150, 50)
        pygame.draw.rect(screen, light_grey, restart_button)
        restart_text = font.render("Restart", True, bg_color)
        screen.blit(restart_text, (restart_button.centerx - restart_text.get_width() // 2,
                                   restart_button.centery - restart_text.get_height() // 2))

        pygame.display.flip()

        # Handle button clicks
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if quit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    elif restart_button.collidepoint(mouse_pos):
                        main_pygame_game(player1_name, player2_name)

    def player_animation():
        nonlocal player_speed
        player.y += player_speed
        if player.top <= 0:
            player.top = 0
        if player.bottom >= screen_height:
            player.bottom = screen_height

    def opponent_ai():
        if opponent.top < ball.y:
            opponent.top += opponent_speed
        if opponent.bottom > ball.y:
            opponent.bottom -= opponent_speed
        if opponent.top <= 0:
            opponent.top = 0
        if opponent.bottom >= screen_height:
            opponent.bottom = screen_height

    def ball_restart():
        nonlocal ball_speed_x, ball_speed_y
        ball.center = (screen_width / 2, screen_height / 2)
        ball_speed_y = initial_ball_speed_y * random.choice((1, -1))
        ball_speed_x = initial_ball_speed_x * random.choice((1, -1))

    def display_scores():
        player_text = font.render(str(player_score), True, light_grey)
        opponent_text = font.render(str(opponent_score), True, light_grey)

        player_name_text = name_font.render(player1_name, True, light_grey)
        opponent_name_text = name_font.render(player2_name, True, light_grey)

        player_name_width = player_name_text.get_width()
        opponent_name_width = opponent_name_text.get_width()

        screen.blit(player_name_text, (20, 20))
        screen.blit(player_text, (20 + player_name_width + 10, 20))

        screen.blit(opponent_name_text, (screen_width - opponent_name_width - 20, 20))
        screen.blit(opponent_text, (screen_width - opponent_name_width - 60, 20))

    def game_over(winner):
        # Display winner directly on the game screen
        game_over_text = font.render(winner, True, light_grey)
        screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2 - 50))

        # Draw buttons for Quit and Restart
        quit_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 20, 100, 50)
        pygame.draw.rect(screen, light_grey, quit_button)
        quit_text = font.render("Quit", True, bg_color)
        screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2, quit_button.centery - quit_text.get_height() // 2))

        restart_button = pygame.Rect(screen_width // 2 + 20, screen_height // 2 + 20, 150, 50)
        pygame.draw.rect(screen, light_grey, restart_button)
        restart_text = font.render("Restart", True, bg_color)
        screen.blit(restart_text, (restart_button.centerx - restart_text.get_width() // 2, restart_button.centery - restart_text.get_height() // 2))

        pygame.display.flip()

        # Handle button clicks
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if quit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    elif restart_button.collidepoint(mouse_pos):
                        main_pygame_game(player1_name, player2_name)

    def quit_game():
        pygame.quit()
        sys.exit()

    def show_menu():
        screen.fill(bg_color)
        title = font.render("Pong Game", True, light_grey)
        easy_text = font.render("1. Easy", True, light_grey)
        medium_text = font.render("2. Medium", True, light_grey)
        hard_text = font.render("3. Hard", True, light_grey)

        screen.blit(title, (screen_width // 2 - 130, 50))
        screen.blit(easy_text, (screen_width // 2 - 100, 150))
        screen.blit(medium_text, (screen_width // 2 - 120, 200))
        screen.blit(hard_text, (screen_width // 2 - 90, 250))

        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return "Easy"
                    if event.key == pygame.K_2:
                        return "Medium"
                    if event.key == pygame.K_3:
                        return "Hard"

    chosen_difficulty = show_menu()
    ball_speed_x, ball_speed_y = difficulty_levels[chosen_difficulty]
    initial_ball_speed_x, initial_ball_speed_y = ball_speed_x, ball_speed_y

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player_speed += 7
                if event.key == pygame.K_UP:
                    player_speed -= 7
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player_speed -= 7
                if event.key == pygame.K_UP:
                    player_speed += 7

        ball_animation()
        player_animation()
        opponent_ai()

        screen.fill(bg_color)
        draw_racket(screen, player, player_color)
        draw_racket(screen, opponent, opponent_color)
        pygame.draw.ellipse(screen, ball_color, ball)
        pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

        display_scores()

        pygame.display.flip()
        clock.tick(60)

def draw_racket(screen, racket, color):
    handle_width = 10
    handle_height = 60
    handle_x = racket.centerx - handle_width // 2
    handle_y = racket.bottom - handle_height
    pygame.draw.rect(screen, color, (handle_x, handle_y, handle_width, handle_height))

    head_radius = 30
    head_center = (racket.centerx, handle_y)
    pygame.draw.circle(screen, color, head_center, head_radius)

if __name__ == "__main__":
    root = tk.Tk()
    game = PingPongGame(root)
    root.mainloop()
