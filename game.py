import sys

import pygame
from pygame.locals import Rect, DOUBLEBUF, QUIT, K_ESCAPE, KEYDOWN, K_DOWN, \
    K_LEFT, K_UP, K_RIGHT, KEYUP, K_LCTRL, K_RETURN, FULLSCREEN, RLEACCEL, K_a


X_MAX = 640
Y_MAX = 480

def load_sprite(sheet, surf_rect, sprite_rect):
    x0, y0, x1, y1 = sprite_rect
    img = pygame.Surface(surf_rect, pygame.SRCALPHA, 32).convert_alpha()
    img.blit(sheet, dest = (0, 0), area = sprite_rect)
    return img

class Fighter(pygame.sprite.Sprite):
    IDLING = 0
    PUNCHING = 1
    WALKING = 2
    
    
    def __init__(self, image, groups, pos, background):
        super(Fighter, self).__init__()
        self.sheet = pygame.image.load(image).convert()
        colorkey = self.sheet.get_at((0,0))
        self.sheet.set_colorkey(colorkey)
        self.image = pygame.Surface((10, 10),pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = pos
        self.load_images()
        self.state = Fighter.IDLING
        self.add(groups)
        self.background = background

        self.fighter_pos = pos
        self.push_back_to = 0


    def load_images(self):
        # Load idling images
        self.idle_images = []
        self.idle_idx = 0
        img = load_sprite(self.sheet, (166, 210), (8, 14, 8+163, 22+210))
        self.idle_images.append(img)
        img = load_sprite(self.sheet, (166, 210), (197, 14, 197+166, 26+210))
        self.idle_images.append(img)
        img = load_sprite(self.sheet, (166, 210), (382, 14, 382+164, 24+210))
        self.idle_images.append(img)
        img = load_sprite(self.sheet, (166, 210), (564, 14, 564+162, 18+210))
        self.idle_images.append(img)
        img = load_sprite(self.sheet, (166, 210), (750, 14, 750+162, 16+210))
        self.idle_images.append(img)
        img = load_sprite(self.sheet, (166, 210), (936, 14, 936+162, 16+210))
        self.idle_images.append(img)
        img = load_sprite(self.sheet, (166, 210), (1118, 14, 1118+162, 14+210))
        self.idle_images.append(img)
        self.idle_images += list(reversed(self.idle_images))


        # Load punching images
        self.punch_images = []
        self.punch_idx = 0

        img = load_sprite(self.sheet, (162, 210), (1380, 432, 1380+162, 432+210))
        self.punch_images.append(img)
        img = load_sprite(self.sheet, (222, 210), (1558, 434, 1558+222, 434+210))
        self.punch_images.append(img)
        img = load_sprite(self.sheet, (188, 210), (1796, 436, 1796+188, 436+210))
        self.punch_images.append(img)
        img = load_sprite(self.sheet, (162, 210), (1380, 432, 1380+162, 432+210))
        self.punch_images.append(img)


        # Load walking images
        self.walking_images = []
        self.walking_idx = 0
        self.walk_vel = 20
        img = load_sprite(self.sheet, (166, 213), (2, 701, 2+166, 701+213))
        self.walking_images.append(img)
        img = load_sprite(self.sheet, (168, 212), (190, 700, 190+168, 700+212))
        self.walking_images.append(img)
        img = load_sprite(self.sheet, (168, 212), (380, 694, 380+168, 694+212))
        self.walking_images.append(img)
        img = load_sprite(self.sheet, (108, 220), (562, 692, 562+108, 692+220))
        self.walking_images.append(img)
        img = load_sprite(self.sheet, (106, 220), (698, 692, 698+106, 692+220))
        self.walking_images.append(img)
        img = load_sprite(self.sheet, (106, 222), (832, 690, 832+106, 690+222))
        self.walking_images.append(img)
        img = load_sprite(self.sheet, (150, 218), (968, 694, 968+150, 694+218))
        self.walking_images.append(img)


    def idle(self):
        self.state = Fighter.IDLING

    def punch(self):
        self.state = Fighter.PUNCHING

    def walk(self):
        self.state = Fighter.WALKING

    def update(self):
        actions = {Fighter.PUNCHING : self.update_punch,
                   Fighter.IDLING : self.update_idling,
                   Fighter.WALKING: self.update_walking}
        action = actions[self.state] 
        action()

        if self.push_back_to != 0:
            self.push_back_to -= 50
            x, y = self.fighter_pos 
            x -= 150
            self.fighter_pos = x, y

        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.fighter_pos

    def update_walking(self):
        self.image = self.walking_images[int(self.walking_idx)]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.fighter_pos
        self.walking_idx += 0.5
        self.walking_idx %= len(self.walking_images)
        x, y = self.fighter_pos
        x += self.walk_vel
        self.fighter_pos = x,y
        # print ("Fighter position ", self.fighter_pos)
        # print ("Sprite position ",  self.rect.bottomleft)
        if x == X_MAX*3.0/4:
            self.background.scroll_right()
            self.push_back_to = 100
        

    def update_punch(self):
        self.image = self.punch_images[int(self.punch_idx)]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.fighter_pos
        self.punch_idx += 0.5
        self.punch_idx %= len(self.punch_images)
        if self.punch_idx == 0:
            self.state = Fighter.IDLING

    def update_idling(self):
        self.image = self.image
        self.image = self.idle_images[int(self.idle_idx)]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.fighter_pos
        self.idle_idx += 0.5
        self.idle_idx %= len(self.idle_images)



class Background(pygame.sprite.Sprite):
    def __init__(self,  bgimage, image, groups):
        super(Background, self).__init__()
        
        self.sheet = pygame.image.load(image).convert_alpha()
        colorkey = self.sheet.get_at((0,0))
        self.sheet.set_colorkey(colorkey)

        self.image = pygame.Surface((X_MAX, Y_MAX),pygame.SRCALPHA, 32).convert_alpha()
        self.background = pygame.image.load(bgimage).convert()
        self.image.blit(self.background, dest = (0,0))

        self.rect = self.image.get_rect()

        self.vertical = self.to = 0
        self.vel = 0
        self.fighter = None
        self.add(groups)
        
    def update(self):
        _, _, t, _ = self.sheet.get_rect()
        new_pos = self.vertical + self.vel

        if new_pos >= 0 and new_pos <= t - X_MAX:
            self.vertical = new_pos
        
        if abs(self.vertical - self.to) < 300:
            self.vel /= 1.5

        if abs(self.vertical - self.to) < 50:
            self.to = self.vertical
            self.vel = 0

        self.image.blit(self.background, dest = (0,0))
        self.image.blit(self.sheet, dest = (0,0), area = (self.vertical,0,640, 480))
        

    def scroll_right(self):
        self.to = self.vertical + X_MAX
        self.vel = 50

    def scroll_left(self):
        self.to = self.vertical - X_MAX
        self.vel = -50

def init_pygame(groups):
    screen = pygame.display.set_mode((X_MAX, Y_MAX), DOUBLEBUF)
    empty = pygame.Surface((X_MAX, Y_MAX))
    return screen, empty


def main():
    everything = pygame.sprite.Group()
    clock = pygame.time.Clock()

    screen, empty = init_pygame(everything)
    b = Background("sprites/bg0.png", "sprites/bg1.png", everything)
    f = Fighter("sprites/fighter-terry.png", everything, (100, 450), b)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    f.walk()
                    pass
                if event.key == K_LEFT:
                    b.scroll_left()
                    pass
                if event.key == K_a:
                    f.punch()

            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    f.idle()


        clock.tick(20)

        everything.clear(screen, empty)
        everything.update()
        everything.draw(screen)
        pygame.display.flip()
            

if __name__ == "__main__":

    main()