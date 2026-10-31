from pygame import *

init()
font.init()

# Parent class untuk sprite
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Subclass untuk raket / pemain
class Player(GameSprite):
    # Kontrol pemain kiri (W dan S)
    def update_1(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed

    # Kontrol pemain kanan (Panah Atas dan Panah Bawah)
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed

# Konfigurasi layar
back = (200, 255, 255)
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Ping-Pong")

# Status permainan
game = True
finish = False
clock = time.Clock()
FPS = 60

# Objek permainan (Pastiikan file Ping Pong Racket.png dan Ping Pong Ball.png ada di folder yang sama)
racket1 = Player("Ping Pong Racket.png", 30, 175, 4, 50, 150)
racket2 = Player("Ping Pong Racket.png", 520, 175, 4, 50, 150)
ball = GameSprite("Ping Pong Ball.png", 270, 200, 4, 60, 60)

# Teks
game_font = font.Font(None, 40)
lose1 = game_font.render("PLAYER 1 LOSE!", True, (180, 0, 0))
Lose2 = game_font.render("PLAYER 2 LOSE!", True, (180, 0, 0))

# Kecepatan bola
speed_x = 3
speed_y = 3
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.fill(back)

        # Gerakan pemain & bola
        racket1.update_1()
        racket2.update_r()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        # Pantulan bola terhadap raket (mencegah bola tersangkut di dalam raket)
        if sprite.collide_rect(racket1, ball):
            speed_x = abs(speed_x) # Pantulkan ke kanan
        elif sprite.collide_rect(racket2, ball):
            speed_x = -abs(speed_x) # Pantulkan ke kiri

        # Pantulan bola terhadap dinding atas dan bawah
        if ball.rect.y <= 0 or ball.rect.y >= win_height - ball.rect.height:
            speed_y *= -1

        # Kondisi kalah Pemain 1
        if ball.rect.x < 0:
            finish = True
            window.blit(lose1, (180, 200))

        # Kondisi kalah Pemain 2
        if ball.rect.x > win_width - ball.rect.width:
            finish = True
            window.blit(Lose2, (180, 200))

        # Render objek
        racket1.reset()
        racket2.reset()
        ball.reset()

    display.update()
    clock.tick(FPS)