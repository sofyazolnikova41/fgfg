from pygame import *
from random import *
from time import time as timer
window = display.set_mode((700,500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700,500))

mixer.init()
fire_sound = mixer.Sound('fire.ogg')

clock = time.Clock()
FPS = 60
speed = 10
lost = 0

font.init()
font2 = font.SysFont('Arial', 70)

font1 = font.SysFont('Arial', 36)
win = font1.render('you win', True, (255, 255, 255))
lose = font1.render('you lose', True, (100, 0, 0))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 625:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost = lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
win_height = 500
win_width = 700
score = 0

max_lost = 10
player = Player('rocket.png', 330, 400, 80, 100, 4)
asteroids = sprite.Group()
monsters = sprite.Group()
for i in range(1, 5):
    monster = Enemy('ufo.png', randint(80, 620), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
for i in range(1, 5):
    asteroid = Asteroid('asteroid.png', randint(80, 620), -40, 80, 50, randint(1, 5))
    asteroids.add(asteroid)
bullets = sprite.Group()
finish = False
game = True
life = 5
num_fire = 0
rel_time = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 6 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    player.fire()               
                if num_fire >= 6 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if finish != True:
        window.blit(background,(0, 0))
        player.update()
        player.reset()
        bullets.update()
        monsters.update()
        asteroids.update()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render("Wait, reload...", 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, 620), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
            #если спрайт коснулся врага, уменьшает жизнь
        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)
            life = life -1
         #проигрыш
        if life == 0 or lost >= max_lost:
            finish = True #проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))
        if score >= 10:          
            finish = True
            window.blit(win, (200, 200))        
        text = font2.render("Cчёт: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        lifes = font2.render(str(life), 1, (150, 0, 0))
        window.blit(lifes, (10, 100))
        display.update()     
    if finish == True:
        finish = False
        score = 0
        lost = 0
        life = 5
        num_fire = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
       
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy('ufo.png', randint(80, 620), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        for i in range(1, 5):
            asteroid = Asteroid('asteroid.png', randint(80, 620), -40, 80, 50, randint(1, 5))
            asteroids.add(asteroid)     
    clock.tick(FPS)
