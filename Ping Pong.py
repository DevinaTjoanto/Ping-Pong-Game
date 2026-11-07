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


# Subclass untuk pemain
class Player(GameSprite):

    # Player 1: W dan S
    def update_1(self):
        keys = key.get_pressed()

        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed

        if keys[K_s] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed

    # Player 2: Panah atas dan bawah
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


# Score ronde saat ini
score1 = 0
score2 = 0

# Total score semua ronde
total1 = 0
total2 = 0

# Jumlah ronde
round_number = 1
max_rounds = 3


# Status pertandingan
match_over = False
hit_racket = False


# SHIELD SKILL
shield1 = 3
shield2 = 3

active_shield1 = False
active_shield2 = False


# Status permainan
game = True
clock = time.Clock()
FPS = 60


# Objek permainan
racket1 = Player("Ping Pong Racket.png", 30, 175, 4, 50, 150)
racket2 = Player("Ping Pong Racket.png", 520, 175, 4, 50, 150)

ball = GameSprite("Ping Pong Ball.png", 270, 200, 4, 60, 60)


# Font
game_font = font.Font(None, 40)
title_font = font.Font(None, 55)
small_font = font.Font(None, 25)


# Kecepatan bola awal
ball_speed = 3
speed_x = ball_speed
speed_y = ball_speed


# MAIN GAME LOOP
while game:

    for e in event.get():

        if e.type == QUIT:
            game = False

        # Kontrol shield
        if e.type == KEYDOWN and not match_over:

            # Shield Player 1 (E)
            if e.key == K_e and shield1 > 0 and not active_shield1:
                shield1 -= 1
                active_shield1 = True

            # Shield Player 2 (C)
            if e.key == K_c and shield2 > 0 and not active_shield2:
                shield2 -= 1
                active_shield2 = True


    # GAME MASIH BERJALAN
    if not match_over:

        window.fill(back)

        # Gerakan pemain dan bola
        racket1.update_1()
        racket2.update_r()

        ball.rect.x += speed_x
        ball.rect.y += speed_y


        # Pantulan bola terhadap raket
        collision1 = sprite.collide_rect(racket1, ball)
        collision2 = sprite.collide_rect(racket2, ball)

        if collision1 and not hit_racket:
            speed_x = abs(speed_x)
            score1 += 1
            hit_racket = True

        elif collision2 and not hit_racket:
            speed_x = -abs(speed_x)
            score2 += 1
            hit_racket = True

        # Reset collision setelah bola meninggalkan raket
        if not collision1 and not collision2:
            hit_racket = False


        # Pantulan bola terhadap dinding
        if ball.rect.y <= 0:
            speed_y = abs(speed_y)

        if ball.rect.y >= win_height - ball.rect.height:
            speed_y = -abs(speed_y)


        # CEK BOLA KELUAR LAYAR
        round_finished = False

        # Bola melewati raket kiri
        if ball.rect.x < 0:

            if active_shield1:
                ball.rect.x = 0
                speed_x = abs(speed_x)
                active_shield1 = False
                hit_racket = False

            else:
                round_finished = True


        # Bola melewati raket kanan
        elif ball.rect.x > win_width - ball.rect.width:

            if active_shield2:
                ball.rect.x = win_width - ball.rect.width
                speed_x = -abs(speed_x)
                active_shield2 = False
                hit_racket = False

            else:
                round_finished = True


        # JIKA RONDE SELESAI
        if round_finished:

            # Simpan score ronde ke total
            total1 += score1
            total2 += score2

            if round_number < max_rounds:

                round_number += 1

                # Reset score ronde
                score1 = 0
                score2 = 0

                # Reset posisi bola
                ball.rect.x = 270
                ball.rect.y = 200

                # Reset posisi raket
                racket1.rect.y = 175
                racket2.rect.y = 175

                # Tambah kecepatan setiap ronde
                ball_speed += 1

                speed_x = ball_speed
                speed_y = ball_speed

                # Reset collision
                hit_racket = False

            else:
                match_over = True


        # Render objek permainan
        racket1.reset()
        racket2.reset()
        ball.reset()


        # Gambar shield aktif
        if active_shield1:
            draw.line(
                window, (0, 100, 255),
                (5, 10), (5, win_height - 10), 6
            )

        if active_shield2:
            draw.line(
                window, (0, 100, 255),
                (win_width - 5, 10),
                (win_width - 5, win_height - 10), 6
            )


        # Tampilkan ronde
        round_text = game_font.render(
            "ROUND " + str(round_number), True, (0, 0, 0)
        )
        window.blit(round_text, (240, 10))


        # Tampilkan kecepatan bola
        speed_text = game_font.render(
            "Speed: " + str(ball_speed), True, (0, 0, 0)
        )
        window.blit(speed_text, (240, 450))


        # Score ronde saat ini
        score_text1 = game_font.render(
            "Player 1: " + str(score1), True, (0, 0, 0)
        )

        score_text2 = game_font.render(
            "Player 2: " + str(score2), True, (0, 0, 0)
        )

        window.blit(score_text1, (50, 50))
        window.blit(score_text2, (350, 50))


        # Total score
        total_text1 = game_font.render(
            "Total: " + str(total1), True, (0, 0, 180)
        )

        total_text2 = game_font.render(
            "Total: " + str(total2), True, (0, 0, 180)
        )

        window.blit(total_text1, (50, 90))
        window.blit(total_text2, (350, 90))


        # Tampilkan jumlah shield
        shield_text1 = game_font.render(
            "Shield: " + str(shield1), True, (0, 100, 255)
        )

        shield_text2 = game_font.render(
            "Shield: " + str(shield2), True, (0, 100, 255)
        )

        window.blit(shield_text1, (50, 130))
        window.blit(shield_text2, (350, 130))


        # Petunjuk tombol shield
        control1 = small_font.render(
            "Press E", True, (0, 100, 255)
        )

        control2 = small_font.render(
            "Press C", True, (0, 100, 255)
        )

        window.blit(control1, (50, 165))
        window.blit(control2, (350, 165))


    # FINAL RESULT SETELAH 3 RONDE
    else:

        window.fill(back)

        # Menentukan pemenang
        if total1 > total2:

            winner_text = title_font.render(
                "PLAYER 1 WINS!", True, (0, 150, 0)
            )

        elif total2 > total1:

            winner_text = title_font.render(
                "PLAYER 2 WINS!", True, (0, 150, 0)
            )

        else:

            winner_text = title_font.render(
                "IT'S A DRAW!", True, (180, 0, 0)
            )


        # Menampilkan pemenang
        winner_rect = winner_text.get_rect(
            center=(win_width // 2, 170)
        )

        window.blit(winner_text, winner_rect)


        # Menampilkan total score
        final_score = title_font.render(
            str(total1) + " : " + str(total2),
            True, (0, 0, 0)
        )

        score_rect = final_score.get_rect(
            center=(win_width // 2, 250)
        )

        window.blit(final_score, score_rect)


        # Keterangan pertandingan selesai
        finished_text = game_font.render(
            "GAME FINISHED!", True, (0, 0, 0)
        )

        finished_rect = finished_text.get_rect(
            center=(win_width // 2, 320)
        )

        window.blit(finished_text, finished_rect)


    display.update()
    clock.tick(FPS)


quit()