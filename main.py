import pygame
import random

# initialise pygame
pygame.init()

pygame.display.set_caption('The Game...')

# this is the width and height of the window the project will appear in
WINDOWWIDTH = 800
WINDOWHEIGHT = 600

# this displays the window
DISPLAY = pygame.display.set_mode([WINDOWWIDTH, WINDOWHEIGHT])

# this sets the clock
FPS = pygame.time.Clock()

# these are some variables
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)

# this is the class of the player's character
class MyCharacter(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.max_health = 3
        self.attack_damage = 2
        self.move_speed = 10
        self.name = 'MyCharacter'
        self.current_health = 2

        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

    def collide_hostile_check(self, hostile_group):
        '''
        Takes input of a sprite group categorized as hostile
        Compares own rectangle to sprite rectangle and checks for collisions
        Returns (True, [list of collided sprites]) if collisions have occurred
        Returns (False, []) if no collisions have occurred
        '''
        if pygame.sprite.spritecollide(my_character, hostile_group, False):
            return(True, [hostile_group])
        else:
            return(False, [])

    def collide_wall_check(self, wall_group):
        '''
        Takes input of a sprite group categorized as walls
        Returns (True, collided wall) if a collision has occurred
        Returns (False, None) if a collision has not occurred
        '''
        for my_wall in wall_group:
            if self.rect.bottom > 230:
                if self.rect.right < 211:
                    if pygame.sprite.collide_rect(my_character, my_wall):
                        self.rect.x = 145
                        return True, 'collided wall'
                if self.rect.right > 229:
                    if pygame.sprite.collide_rect(my_wall, my_character):
                        self.rect.x = 230
                        return True, 'collided wall'
                else:
                    if pygame.sprite.collide_rect(my_character, my_wall):
                        self.rect.y = 220
                        return True, 'collided wall'
            else:
                return False, None

    def damage_or_healing(self, amount):
        '''
        Takes input of damage (negative) or healing (positive)
        Calculates  if you are dead
        Changes your current health by the amount input
        returns False if current health <=0 (dead)
        returns True if current health > 0
        '''
        self.current_health += amount

        if self.current_health > 0:
            return True
        elif self.current_health <= 0:
            return False

    def update(self, hostile_group, wall_group, direction):
        '''
        takes input of hostile_group, wall_group, direction
        updates rectangle position by move_speed in that direction.
        checks if there is a wall and does not move if one is detected
        does not return anything
        '''

        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_LEFT]:
            my_character.rect.x -= 10
        if key_input[pygame.K_UP]:
            my_character.rect.y -= 10
        if key_input[pygame.K_RIGHT]:
            my_character.rect.x += 10
        if key_input[pygame.K_DOWN]:
            my_character.rect.y += 10

# this is the class of the enemy character
class MyEnemy(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.health = 5
        self.move_speed = 10

        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

    def collide_wall_check(self, wall_group):
        for my_wall in wall_group:
            if self.rect.bottom > 230:
                if self.rect.right < 211:
                    if pygame.sprite.collide_rect(my_character, my_wall):
                        self.rect.x = 145
                        return True, 'collided wall'
                if self.rect.right > 229:
                    if pygame.sprite.collide_rect(my_wall, my_character):
                        self.rect.x = 230
                        return True, 'collided wall'
                else:
                    if pygame.sprite.collide_rect(my_character, my_wall):
                        self.rect.y = 220
                        return True, 'collided wall'
            else:
                return False, None

    def collide_hostile_check(self, hostile_group):
        '''
        Takes input of a sprite group categorized as hostile
        Compares own rectangle to sprite rectangle and checks for collisions
        Returns (True, [list of collided sprites]) if collisions have occurred
        Returns (False, []) if no collisions have occurred
        '''
        if pygame.sprite.spritecollide(my_wall, hostile_group, False):
            return(True, [hostile_group])
        else:
            return(False, [])

    def update(self, wall_group, hostile_group, direction):

        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_a]:
            my_enemy.rect.x -= 10
        if key_input[pygame.K_w]:
            my_enemy.rect.y -= 10
        if key_input[pygame.K_d]:
            my_enemy.rect.x += 10
        if key_input[pygame.K_s]:
            my_enemy.rect.y += 10

# this is the class of the attack
class Attack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.damage = None
        self.mode = None
        self.count = None
        self.move_speed = None
        self.direction = None
    def update(self):
        pass

# this is the class of the hostiles in the game
class Hostile(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.speed = [random.randrange(5, 15), random.randrange(5, 15)]

    def collide_wall_check(self, wall_group):
        '''
        Takes input of a sprite group categorized as walls
        Returns (True, collided wall) if a collision has occurred
        Returns (False, None) if a collision has not occurred
        '''
        for my_wall in wall_group:
                if pygame.sprite.collide_rect(my_hostile1, my_wall):
                    self.speed[0] *= -1

    def update(self):
        self.rect.x = self.rect.x + self.speed[0]
        if self.rect.right > WINDOWWIDTH or self.rect.left < 0:
            self.speed[0] *= -1

        self.rect.y = self.rect.y + self.speed[1]
        if self.rect.bottom > WINDOWHEIGHT or self.rect.top < 0:
            self.speed[1] *= -1

# this is the class of the walls in the game
class Walls(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(200, 280))

    # this sprite group is for the hostiles

# this sprite class is for the hostiles
my_hostile1 = Hostile(25, 25)
my_hostile2 = Hostile(25, 25)
my_hostile3 = Hostile(25, 25)
my_hostile4 = Hostile(25, 25)
my_hostile5 = Hostile(25, 25)
hostile_group = pygame.sprite.Group()
hostile_group.add(my_hostile1)
hostile_group.add(my_hostile2)
hostile_group.add(my_hostile3)
hostile_group.add(my_hostile4)
hostile_group.add(my_hostile5)

# this sprite group is for the walls
my_wall = Walls(25, 200)
wall_group = pygame.sprite.Group()
wall_group.add(my_wall)

# this sprite group is for the attack
my_attack = Attack()
attack_group = pygame.sprite.Group()
attack_group.add(my_attack)

# this sprite group is for the characters
my_character = MyCharacter(50, 50)
my_enemy = MyEnemy(50, 50)
my_group = pygame.sprite.Group()
my_group.add(my_character)
my_group.add(my_enemy)

# this is the mouse position
mos_pos = pygame.mouse.get_pos()

while True:

    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mos_pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            quit()

    # this lets the main character respawn back into window if exceeds boundary
    if my_character.rect.bottom > WINDOWHEIGHT:
        my_character.rect.top = 0
    if my_character.rect.top < 0:
        my_character.rect.bottom = WINDOWHEIGHT
    if my_character.rect.right > WINDOWWIDTH:
        my_character.rect.left = 0
    if my_character.rect.left < 0:
        my_character.rect.right = WINDOWWIDTH

    # this lets the enemy character respawn back into window if exceeds boundary
    if my_enemy.rect.bottom > WINDOWHEIGHT:
        my_enemy.rect.top = 0
    if my_enemy.rect.top < 0:
        my_enemy.rect.bottom = WINDOWHEIGHT
    if my_enemy.rect.right > WINDOWWIDTH:
        my_enemy.rect.left = 0
    if my_enemy.rect.left < 0:
        my_enemy.rect.right = WINDOWWIDTH


    my_character.collide_wall_check(wall_group)

    my_hostile1.collide_wall_check(wall_group)
    my_hostile2.collide_wall_check(wall_group)
    my_hostile3.collide_wall_check(wall_group)
    my_hostile4.collide_wall_check(wall_group)
    my_hostile5.collide_wall_check(wall_group)

    # this fills the display in black
    DISPLAY.fill((BLACK))

    my_group.update(hostile_group, wall_group, 'up')

    hostile_group.update()

    # this draws the groups onto the display
    my_group.draw(DISPLAY)
    hostile_group.draw(DISPLAY)
    wall_group.draw(DISPLAY)
    #attack_group(DISPLAY)

    # this updates the display
    pygame.display.update()

    # this sets the clock speed
    FPS.tick(30)

# TODO make enemy
# TODO make sure the collisions with the enemy give a warning too
# TODO get the attack to work
# TODO make sure collisions cost lives (read up on health and stuff)
# TODO maybe make characters more interesting (better colours?)