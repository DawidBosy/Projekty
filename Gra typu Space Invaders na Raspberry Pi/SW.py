import pygame
import os
import time
import random
import serial

from pygame.locals import *
from input_arduino import ArduinoInputReader
from output_raspberry import RaspberryOutputWriter

pygame.font.init()

WIDTH,HEIGHT = 750,600
flags = DOUBLEBUF
WIN = pygame.display.set_mode((WIDTH,HEIGHT), flags, 16)
WIN.set_alpha(None)
pygame.display.set_caption("Space Shooter")

RED_SPACE_SHIP = pygame.image.load(os.path.join("assets","shipRed.png")).convert_alpha()
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets","shipGreen.png")).convert_alpha()
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets","shipBlue.png")).convert_alpha()
RED_SPACE_SHIP = pygame.transform.scale(RED_SPACE_SHIP,(RED_SPACE_SHIP.get_width()//2,RED_SPACE_SHIP.get_height()// 2))
GREEN_SPACE_SHIP = pygame.transform.scale(GREEN_SPACE_SHIP,(GREEN_SPACE_SHIP.get_width()//2,GREEN_SPACE_SHIP.get_height()//2))
BLUE_SPACE_SHIP = pygame.transform.scale(BLUE_SPACE_SHIP,(BLUE_SPACE_SHIP.get_width()//2,BLUE_SPACE_SHIP.get_height()//2))
#player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets","playerShip2_green.png")).convert_alpha()

#lasers
RED_LASER = pygame.image.load(os.path.join("assets","laserRed01.png")).convert_alpha()
GREEN_LASER = pygame.image.load(os.path.join("assets","laserGreen11.png")).convert_alpha()
BLUE_LASER = pygame.image.load(os.path.join("assets","laserBlue01.png")).convert_alpha()
YELLOW_LASER = pygame.image.load(os.path.join("assets","laserYellow01.png")).convert_alpha()
BLUE_LASER = pygame.transform.rotate(BLUE_LASER,180)
RED_LASER = pygame.transform.rotate(RED_LASER,180)
GREEN_LASER = pygame.transform.rotate(GREEN_LASER,180)
#background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets","darkPurple.png")).convert(),(WIDTH,HEIGHT))

class Laser:
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self,window):
        window.blit(self.img,(self.x,self.y))

    def move (self,vel):
        self.y += vel

    def off_screen(self,height):
        return not(self.y < height and self.y >= 0)

    def collision(self,obj):
        return collide(self,obj)

class Ship:
    def __init__(self,x,y,health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cooldown_counter = 0
        self.COOLDOWN = 5

    def draw(self,window):
        window.blit(self.ship_img,(self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self,vel,obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter = 0
        elif self.cooldown_counter>0:
            self.cooldown_counter += 1

    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x+self.get_width()/2-self.laser_img.get_width()/2,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cooldown_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self,x,y,health = 100,vel=10):
        super().__init__(x,y,health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.vel = vel
        self.score = 0

    def move_lasers(self,vel,objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        obj.health -= 50
                        if obj.health <= 0:
                            objs.remove(obj)
                            self.score += obj.max_health/5
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self,window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self,window):
        pygame.draw.rect(window,(255,0,0),(self.x,self.y+self.ship_img.get_height()+10,self.ship_img.get_width(),10))
        pygame.draw.rect(window,(0,255,0),(self.x,self.y+self.ship_img.get_height()+10,self.ship_img.get_width()*(self.health/self.max_health),10))

class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP,RED_LASER,150),
        "green": (GREEN_SPACE_SHIP,GREEN_LASER,100),
        "blue": (BLUE_SPACE_SHIP,BLUE_LASER,50)
    }
    def __init__(self,x,y,color):
        super().__init__(x,y)
        self.ship_img,self.laser_img,self.max_health = self.COLOR_MAP[color]
        self.health = self.max_health
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self,vel):
        self.y += vel

    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x +self.get_width()/2-self.laser_img.get_width()/2,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cooldown_counter = 1

    def draw(self,window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self,window):
        pygame.draw.rect(window,(255,0,0),(self.x,self.y-10,self.ship_img.get_width(),5))
        pygame.draw.rect(window,(0,255,0),(self.x,self.y-10,self.ship_img.get_width()*(self.health/self.max_health),5))



def collide(obj1,obj2):
    offset_x = int(obj2.x - obj1.x)
    offset_y = int(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y)) != None

def main():
    enemyAmount = [[5,5,0],[2,5,7],[3,10,5]]
    enemyCordsx = [
        [[WIDTH/5,WIDTH/3,WIDTH/2,WIDTH/3*2,WIDTH/5*4],
        [WIDTH/5,WIDTH/3,WIDTH/2,WIDTH/3*2,WIDTH/5*4],
        []],
                   
       [[WIDTH/3,WIDTH/3*2],
        [WIDTH/5,WIDTH/3,WIDTH/2,WIDTH/3*2,WIDTH/5*4],
        [WIDTH/7,WIDTH/5,WIDTH/3,WIDTH/2,WIDTH/3*2,WIDTH/5*4,WIDTH/7*6]],
    
        [[WIDTH/3,WIDTH/2,WIDTH/3*2],
         [WIDTH/5,WIDTH/3,WIDTH/2,WIDTH/3*2,WIDTH/5*4,WIDTH/5,WIDTH/3,WIDTH/2,WIDTH/3*2,WIDTH/5*4],
         [WIDTH/5,WIDTH/3,WIDTH/2,WIDTH/3*2,WIDTH/5*4]]]
        
    enemyCordsy = [[[-400,-400,-400,-400,-400],[-300,-200,-100,-200,-300],[]],
                   [[-200,-200],[-100,-400,-300,-400,-100],[-800,-500,-700,-600,-700,-500,-800]],
                   [[-300,-300,-300],[-500,-600,-700,-800,-900,-1000,-1100,-1200,-1300,-1400],[-400,-400,-400,-400,-400]]]
    run = True
    FPS = 30
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans",50)
    lost_font = pygame.font.SysFont("comicsans",60)

    enemies = []
    enemy_vel = 2

    lost = False
    lost_count = 0
    laser_vel = 12

    reader = ArduinoInputReader()
    writer = RaspberryOutputWriter()
    
    player = Player(300,420)

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG,(0,0))
        #score_label = main_font.render(f"Points: {int(player.score)}",1,(255,255,255))
        #level_label = main_font.render(f"Level: {level}",1,(255,255,255))
        #WIN.blit(score_label,(10,10))
        #WIN.blit(level_label,(WIDTH-level_label.get_width()-10,10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You lost!",1,(255,255,255))
            WIN.blit(lost_label,(WIDTH/2-lost_label.get_width()/2,350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        writer.write_to_screen(level=level, points=int(player.score))
        writer.set_leds_based_on_health(health=player.health)        
        
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count> FPS * 3:
                run = False
            else:
                continue
        
        if len(enemies) == 0:
            randlevel = random.randint(0,2)
            for i in range(enemyAmount[randlevel][0]):
                enemy=Enemy(enemyCordsx[randlevel][0][i],enemyCordsy[randlevel][0][i],"blue")
                enemies.append(enemy)
            for i in range(enemyAmount[randlevel][1]):
                enemy=Enemy(enemyCordsx[randlevel][1][i],enemyCordsy[randlevel][1][i],"green")
                enemies.append(enemy)
            for i in range(enemyAmount[randlevel][2]):
                enemy=Enemy(enemyCordsx[randlevel][2][i],enemyCordsy[randlevel][2][i],"red")
                enemies.append(enemy)
            level += 1
            enemy_vel+=0.25

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run= False #ustawić na quit jeśli chcemy usunąć menu

        
        x, y, z, b1, b2 = reader.get_input()
        
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_a] and player.x - player.vel > 0: #left
#             player.x -= player.vel
#         if keys[pygame.K_d] and player.x + player.vel + player.get_width() < WIDTH: #right
#             player.x += player.vel
#         if keys[pygame.K_w] and player.y-player.vel > 0: #up
#             player.y -= player.vel
#         if keys[pygame.K_s] and player.y+player.vel + player.get_height() + 20 < HEIGHT: #down
#             player.y += player.vel
#         if keys[pygame.K_SPACE]:
#             player.shoot()
#         

        if x < 400 and player.x - player.vel > 0: #left
            player.x -= player.vel
        if x > 800 and player.x + player.vel + player.get_width() < WIDTH: #right
            player.x += player.vel
        if y > 800 and player.y-player.vel > 0: #up
            player.y -= player.vel
        if y < 400 and player.y+player.vel + player.get_height() + 20 < HEIGHT: #down
            player.y += player.vel
        if b1 == 0:
            player.shoot()
        if b2 == 0:
            run = False
       
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel,player)

            if random.randrange(0,2*60) == 1:
                enemy.shoot()

            if collide(enemy,player):
                player.health -= 20
                enemies.remove(enemy)
                player.score += 5
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)


        player.move_lasers(-laser_vel,enemies)


def main_menu():
    title_font = pygame.font.SysFont("comicsans",70)
    run = True
    while run:
        WIN.blit(BG,(0,0))
#         title_label = title_font.render("Press mouse to begin!",1 ,(255,255,255))
#         WIN.blit(title_label,(WIDTH/2-title_label.get_width()/2,350))

        pygame.display.update()
        main()
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 main()
    pygame.quit()


main_menu()

