import pygame
import random

# initialise pygame
pygame.init()

pygame.display.set_caption('King Gizzard and the Lizard Wizard')

# this is the width and height of the window the project will appear in
WINDOWWIDTH = 800
WINDOWHEIGHT = 600

# this displays the window
DISPLAY = pygame.display.set_mode([WINDOWWIDTH, WINDOWHEIGHT])

# this sets the clock
FPS = pygame.time.Clock()

# these are some variables of colour
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)
PURPLE = (148, 0, 211)

# this is the class of the player's character
class MyCharacter(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.max_health = 25
        self.attack_damage = 1
        self.move_speed = 10
        self.name = 'MyCharacter'
        self.current_health = 20

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
        if pygame.sprite.groupcollide(my_group, hostile_group, False, False):
             self.current_health -= 1
             print('Green Health = ', self.current_health)
             return True, self.current_health
        if pygame.sprite.groupcollide(my_group, enemy_group, False, False):
            self.current_health = 0
            print('Green and Red Collided!')
            return True, self.current_health
        else:
            return False

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

    def damage_or_healing(self):
        '''
        Takes input of damage (negative) or healing (positive)
        Calculates  if you are dead
        Changes your current health by the amount input
        returns False if current health <=0 (dead)
        returns True if current health > 0
        '''

        if self.current_health > 0:
            return True
        elif self.current_health <= 0:
            return False

    def attack(self, hostile_group):
        if hostile_group == None:
            return True

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
    def __init__(self, width, height, x, y):
        super().__init__()
        self.health = 20
        self.move_speed = 10

        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def collide_wall_check(self, wall_group):
        for my_wall in wall_group:
            if self.rect.bottom > 230:
                if self.rect.right < 211:
                    if pygame.sprite.collide_rect(my_enemy, my_wall):
                        self.rect.x = 145
                        return True, 'collided wall'
                if self.rect.right > 229:
                    if pygame.sprite.collide_rect(my_wall, my_enemy):
                        self.rect.x = 230
                        return True, 'collided wall'
                else:
                    if pygame.sprite.collide_rect(my_enemy, my_wall):
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
        if pygame.sprite.spritecollide(my_enemy, hostile_group, False):
            self.health -= 1
            print('Red Health = ', self.health)
            return True, self.health
        else:
            return False

    def damage_or_healing(self):
        '''
        Takes input of damage (negative) or healing (positive)
        Calculates  if you are dead
        Changes your current health by the amount input
        returns False if current health <=0 (dead)
        returns True if current health > 0
        '''

        if self.health > 0:
            return True
        elif self.health <= 0:
            return False

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
    def __init__(self, width, height):
        super().__init__()
        self.damage = 2
        self.mode = 'range'
        self.count = 40
        self.move_speed = 50
        self.direction = 'right'

        self.image = pygame.Surface([width, height])
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()

    def collide_hostile_check(self, hostile_group):
        '''
        Takes input of a sprite group categorized as hostile
        Compares own rectangle to sprite rectangle and checks for collisions
        Deletes both sprites if a collision has occured
        '''
        for hostile in hostile_group:
            if hostile == my_hostile1:
                if pygame.sprite.collide_rect(my_attack, my_hostile1):
                    my_hostile1.kill()
            if hostile == my_hostile2:
                if pygame.sprite.collide_rect(my_attack, my_hostile2):
                    my_hostile2.kill()
            if hostile == my_hostile3:
                if pygame.sprite.collide_rect(my_attack, my_hostile3):
                    my_hostile3.kill()
            if hostile == my_hostile4:
                if pygame.sprite.collide_rect(my_attack, my_hostile4):
                    my_hostile4.kill()
            if hostile == my_hostile5:
                if pygame.sprite.collide_rect(my_attack, my_hostile5):
                    my_hostile5.kill()

            if hostile == my_hostile1:
                if pygame.sprite.collide_rect(other_attack, my_hostile1):
                    my_hostile1.kill()
            if hostile == my_hostile2:
                if pygame.sprite.collide_rect(other_attack, my_hostile2):
                    my_hostile2.kill()
            if hostile == my_hostile3:
                if pygame.sprite.collide_rect(other_attack, my_hostile3):
                    my_hostile3.kill()
            if hostile == my_hostile4:
                if pygame.sprite.collide_rect(other_attack, my_hostile4):
                    my_hostile4.kill()
            if hostile == my_hostile5:
                if pygame.sprite.collide_rect(other_attack, my_hostile5):
                    my_hostile5.kill()

    def position(self):
        my_attack.rect.center = my_character.rect.center
        my_attack.rect.left = my_character.rect.right

        other_attack.rect.center = my_enemy.rect.center
        other_attack.rect.right = my_enemy.rect.left

    def update(self):
        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_SPACE]: # for my_character
            my_attack.rect.x += 10
            my_attack.rect.x += self.move_speed
        if key_input[pygame.K_RETURN]: # for my_enemy
            other_attack.rect.x -= 10
            other_attack.rect.x -= self.move_speed

# this is the class of the hostiles in the game
class Hostile(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.speed = [random.randrange(2, 15), random.randrange(2, 15)]
        self.rect.x = x
        self.rect.y = y

    def collide_wall_check(self, wall_group):
        '''
        Takes input of a sprite group categorized as walls
        Returns (True, collided wall) if a collision has occurred
        Returns (False, None) if a collision has not occurred
        '''
        for my_wall in wall_group:
                if pygame.sprite.collide_rect(my_hostile1, my_wall):
                    self.speed[0] *= -1
                if pygame.sprite.collide_rect(my_hostile2, my_wall):
                    self.speed[0] *= -1
                if pygame.sprite.collide_rect(my_hostile3, my_wall):
                    self.speed[0] *= -1
                if pygame.sprite.collide_rect(my_hostile4, my_wall):
                    self.speed[0] *= -1
                if pygame.sprite.collide_rect(my_hostile5, my_wall):
                    self.speed[0] *= -1

    def update(self):
        self.rect.x += self.speed[0]
        if self.rect.right > WINDOWWIDTH or self.rect.left < 0:
            self.speed[0] *= -1

        self.rect.y += self.speed[1]
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
my_hostile1 = Hostile(25, 25, 0, 100)
my_hostile2 = Hostile(25, 25, 0, 300)
my_hostile3 = Hostile(25, 25, 0, 500)
my_hostile4 = Hostile(25, 25, 750, 200)
my_hostile5 = Hostile(25, 25, 750, 400)
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
my_attack = Attack(25, 5)
other_attack = Attack(25, 5)
attack_group = pygame.sprite.Group()
attack_group.add(my_attack)
attack_group.add(other_attack)

# this sprite group is for the character
my_character = MyCharacter(50, 50)
my_group = pygame.sprite.Group()
my_group.add(my_character)

# this sprite group is for the enemy
my_enemy = MyEnemy(50, 50, 750, 550)
enemy_group = pygame.sprite.Group()
enemy_group.add(my_enemy)

# this is the mouse position
mos_pos = pygame.mouse.get_pos()

while True:

    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mos_pos = pygame.mouse.get_pos()
        if my_character.damage_or_healing() == False:
            print('GAME OVER')
            quit()
        if my_enemy.damage_or_healing() == False:
            print('GAME OVER')
            quit()
        if len(hostile_group) == 0:
            print('WIN!')
            quit()
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

    # this respawns attack if it goes outside of the boundaries
    if my_attack.rect.right > WINDOWWIDTH:
        my_attack.kill()
        my_attack = Attack(25, 5)
        attack_group.add(my_attack)
    if my_attack.rect.left < 0:
        my_attack.kill()
        my_attack = Attack(25, 5)
        attack_group.add(my_attack)
    if my_attack.rect.bottom > WINDOWWIDTH:
        my_attack.kill()
        my_attack = Attack(25, 5)
        attack_group.add(my_attack)
    if my_attack.rect.top < 0:
        my_attack.kill()
        my_attack = Attack(25, 5)
        attack_group.add(my_attack)

    # this respawns attack if it goes outside of the boundaries
    if other_attack.rect.right > WINDOWWIDTH:
        other_attack.kill()
        other_attack = Attack(25, 5)
        attack_group.add(other_attack)
    if other_attack.rect.left < 0:
        other_attack.kill()
        other_attack = Attack(25, 5)
        attack_group.add(other_attack)
    if other_attack.rect.bottom > WINDOWWIDTH:
        other_attack.kill()
        other_attack = Attack(25, 5)
        attack_group.add(other_attack)
    if other_attack.rect.top < 0:
        other_attack.kill()
        other_attack = Attack(25, 5)
        attack_group.add(other_attack)


    # attack position
    my_attack.position()

    # this checks if anything has collided with the hostiles
    my_character.collide_hostile_check(hostile_group)
    my_enemy.collide_hostile_check(hostile_group)

    # this checks if anything has collided with the wall
    my_character.collide_wall_check(wall_group)
    my_enemy.collide_wall_check(wall_group)
    my_hostile1.collide_wall_check(wall_group)
    my_hostile2.collide_wall_check(wall_group)
    my_hostile3.collide_wall_check(wall_group)
    my_hostile4.collide_wall_check(wall_group)
    my_hostile5.collide_wall_check(wall_group)

    # checks if anything has collided with the attack
    my_attack.collide_hostile_check(hostile_group)

    # this fills the display in black
    DISPLAY.fill((BLACK))

    # this updates things
    my_group.update(hostile_group, wall_group, 'up')
    enemy_group.update(hostile_group, wall_group, 'up')
    hostile_group.update()
    attack_group.update()

    # this draws the groups onto the display
    my_group.draw(DISPLAY)
    enemy_group.draw(DISPLAY)
    hostile_group.draw(DISPLAY)
    wall_group.draw(DISPLAY)
    attack_group.draw(DISPLAY)


    # this updates the display
    pygame.display.update()

    # this sets the clock speed
    FPS.tick(30)