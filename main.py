import pygame # pygame

pygame.init()

WINDOWWIDTH = 800
WINDOWHEIGHT = 600

DISPLAY = pygame.display.set_mode([WINDOWWIDTH, WINDOWHEIGHT])

FPS = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
left = 50
top = 50
width = 40
height = 40
x_speed = 5
y_speed = 5
x_colour = RED

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


class MyCharacter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.max_health = 3
        self.attack_damage = 2
        self.move_speed = 10
        self.name = MyCharacter
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
        :param hostile_group:
        :return:
        '''
        return (False, [])
    # TODO collide health check function

    def collide_wall_check(self, wall_group, direction):
        '''
        Takes input of a sprite group categorized as walls
        Returns (True, collided wall) if a collision has occurred
        Returns (False, None) if a collision has not occurred
        :param wall_group:
        :param direction:
        :return:
        '''

        return (False, None)
    # TODO collide wall check

    def damage_or_healing(self, amount):
        '''
        Takes input of damage (negative) or healing (positive)
        Calculates  if you are dead
        Changes your current health by the amount input
        returns False if current health <=0 (dead)
        returns True if current health > 0
        :param amount:
        :return:
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
        :param hostile_group:
        :param wall_group:
        :param direction:
        :return:
        '''
        pass
    # TODO update (cant finish unless hostile and wall check are complete)

class MyEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = None
        self.move_speed = None

    def collide_wall_check(self, wall_group, direction):
        return (False, None)

    def collide_hostile_check(self, hostile_group):
        return (False, [])

    def update(self, wall_group, hostile_group, direction):
        pass

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


my_rectangle = BouncingRectangle(80, 80)
my_group = pygame.sprite.Group()
my_group.add(my_rectangle)

mos_pos = pygame.mouse.get_pos()

while True:

    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mos_pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            quit()


    DISPLAY.fill((BLACK))

    my_group.update(mos_pos)
    my_group.draw(DISPLAY)

    pygame.display.update()

    FPS.tick(30)