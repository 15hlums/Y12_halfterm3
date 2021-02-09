import pygame
import random

# initialise pygame
pygame.init()

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

# class that will not be in final project, keep for reference
class BouncingRectangle(pygame.sprite.Sprite):

    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()

        self.x_colour = RED

        self.image.fill(WHITE)
        pygame.draw.line(self.image, self.x_colour, self.rect.topleft, self.rect.bottomright, 10)
        pygame.draw.line(self.image, self.x_colour, self.rect.bottomleft, self.rect.topright, 10)

        self.x_speed = 5
        self.y_speed = 5

    def update(self, mos_pos):
        self.rect.left += self.x_speed
        if self.rect.right >= WINDOWWIDTH:
            self.x_speed *= -1
        if self.rect.left <= 0:
            self.x_speed *= -1

        self.rect.top += self.y_speed
        if self.rect.bottom >= WINDOWHEIGHT:
            self.y_speed *= -1
        if self.rect.top <= 0:
            self.y_speed *= -1

        if self.rect.x < mos_pos[0] < self.rect.x + self.rect.width:
            if self.rect.y < mos_pos[1] < self.rect.y + self.rect.height:
                self.x_colour = GREEN
        else:
            self.x_colour = RED

        pygame.draw.line(self.image, self.x_colour, [0, 0], [self.rect.width, self.rect.height], 10)
        pygame.draw.line(self.image, self.x_colour, [0, self.rect.height], [self.rect.width, 0], 10)

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

    def position(self):
        self.rect.y = 0
        self.rect.x = 0

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
        if pygame.sprite.spritecollide(my_character, wall_group, False):
            return(True, print('collided wall'))
        else:
            return (False, None)

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
            print('left')
        if key_input[pygame.K_UP]:
            my_character.rect.y -= 10
            print('up')
        if key_input[pygame.K_RIGHT]:
            my_character.rect.x += 10
            print('right')
        if key_input[pygame.K_DOWN]:
            my_character.rect.y += 10
            print('down')

        self.rect.left += self.move_speed
        if self.rect.right >= WINDOWWIDTH:
            self.move_speed *= -1
            self.rect.x += self.move_speed
        if self.rect.left <= 0:
            self.move_speed *= -1
            self.rect.x += self.move_speed

        self.rect.top += self.move_speed
        if self.rect.bottom >= WINDOWHEIGHT:
            self.move_speed *= -1
            self.rect.y += self.move_speed
        if self.rect.top <= 0:
            self.move_speed *= -1
            self.rect.y += self.move_speed

        if self.rect.right or self.rect.left or self.rect.top or self.rect.bottom >= wall_group:
            self.move_speed = 0

        pass

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
        if pygame.sprite.spritecollide(my_wall, wall_group, False):
            return(True, print('collided wall'))
        else:
            return (False, None)

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
        pass

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

# this is the class of the walls in the game
class Walls(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()

# this sprite group is for the hostiles
my_hostile = Hostile(15, 15)
hostile_group = pygame.sprite.Group()
hostile_group.add(my_hostile)

# this sprite group is for the walls
my_wall = Walls(5, 50)
wall_group = pygame.sprite.Group()
wall_group.add(my_wall)

# this sprite group is for the attack
my_attack = Attack()
attack_group = pygame.sprite.Group()
attack_group.add(my_attack)

# this sprite group is for the characters
my_character = MyCharacter(50, 50)
my_enemy = MyEnemy(30, 30)
my_group = pygame.sprite.Group()
my_group.add(my_character)
my_group.add(my_enemy)

# this is the mouse position
mos_pos = pygame.mouse.get_pos()

while True:

    my_character.rect.x = 10
    my_character.rect.y = 10

    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mos_pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            quit()


    # this fills the display in black
    DISPLAY.fill((BLACK))

    my_group.update(hostile_group, wall_group, 'up')

    # this draws the groups onto the display
    my_group.draw(DISPLAY)
    hostile_group.draw(DISPLAY)
    wall_group.draw(DISPLAY)
    #attack_group(DISPLAY)

    # this updates the display
    pygame.display.update()

    # this sets the clock speed
    FPS.tick(30)