import pygame
import random
from spritesheet import Spritesheet

################################# LOAD UP A BASIC WINDOW AND CLOCK #################################
pygame.init()
DISPLAY_W, DISPLAY_H = 480, 272
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
window = pygame.display.set_mode(((DISPLAY_W,DISPLAY_H)))
running = True
clock = pygame.time.Clock()
background = pygame.image.load('background.png').convert_alpha()
font = pygame.font.Font('8-BIT WONDER.TTF', 12)
mouse = pygame.image.load("Mouse.png")
mouse_size = 16
mouse_count = -1 # -1 because the spawn also increments this counter
cat_w = 56
cat_h = 41

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.LEFT_KEY, self.RIGHT_KEY, self.UP_KEY, self.FACING_LEFT = False, False, False, False
        self.load_frames()
        self.rect = self.idle_frames_left[0].get_rect()
        self.rect.topleft = (16, 54)
        self.current_frame = 0
        self.last_updated = 0
        self.velocity = 0
        self.jump_velocity = 0
        self.state = 'idle'
        self.current_image = self.idle_frames_left[0]
    
    def draw(self, display):
        display.blit(self.current_image, self.rect)

    def update(self, empty_blocks):
        self.velocity = 0
        if self.LEFT_KEY:
            self.velocity = -2
        elif self.RIGHT_KEY:
            self.velocity = 2
        elif self.UP_KEY:
            self.jump_velocity = 14

        #display border colision
        if cat.rect.right >=  DISPLAY_W or cat.rect.left <= 0:
            self.velocity = 0
        if cat.rect.bottom >= DISPLAY_H or cat.rect.top <= 0:
            self.jump_velocity = 0

        #floor colision
        collision_tolerance = 10
        if cat.colliderect(floor_blocks):
            if abs(floor_blocks.rect.top - cat.rect.bottom) < collision_tolerance:
                self.jump_velocity = 0
            if abs(floor_blocks.rect.bottom - cat.rect.top) < collision_tolerance:
                self.jump_velocity = 0
            if abs(floor_blocks.rect.left - cat.rect.right) < collision_tolerance:
                self.velocity = 0
            if abs(floor_blocks.rect.right - cat.rect.left) < collision_tolerance:
                self.velocity = 0
        if self.velocity and self.jump_velocity == 0:
            self.set_state()
            self.animate()

    def set_state(self):
        self.state = ' idle'
        if self.velocity > 0:
            self.state = 'moving right'
        elif self.velocity < 0:
            self.state = 'moving left'

    def animate(self):
        now = pygame.time.get_ticks()
        if self.state == ' idle':
            if now - self.last_updated > 200:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames_left)
                if self.FACING_LEFT:
                    self.current_image = self.idle_frames_left[self.current_frame]
                elif not self.FACING_LEFT:
                    self.current_image = self.idle_frames_right[self.current_frame]
        else:
            if now - self.last_updated > 100:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_left)
                if self.state == 'moving left':
                    self.current_image = self.walking_frames_left[self.current_frame]
                elif self.state == 'moving right':
                    self.current_image = self.walking_frames_right[self.current_frame]

    def load_frames(self):
        my_spritesheet = Spritesheet('poppy_sheet.png')
        #pygame.image.load('MY_IMAGE_NAME.png').convert()
        self.idle_frames_left = [my_spritesheet.parse_sprite("poppy_idle1.png"),
                                 my_spritesheet.parse_sprite("poppy_idle2.png")]
        self.walking_frames_left = [my_spritesheet.parse_sprite("poppywalk1.png"), my_spritesheet.parse_sprite("poppywalk2.png"),
                           my_spritesheet.parse_sprite("poppywalk3.png"), my_spritesheet.parse_sprite("poppywalk4.png"),
                           my_spritesheet.parse_sprite("poppywalk5.png"), my_spritesheet.parse_sprite("poppywalk6.png"),
                           my_spritesheet.parse_sprite("poppywalk7.png"), my_spritesheet.parse_sprite("poppywalk8.png")]
        self.idle_frames_right = []
        for frame in self.idle_frames_left:
            self.idle_frames_right.append( pygame.transform.flip(frame,True, False) )
        self.walking_frames_right = []
        for frame in self.walking_frames_left:
            self.walking_frames_right.append(pygame.transform.flip(frame, True, False))

#check which blocks are empty
empty_space = []
hpixel = 0
wpixel = 0
empty_space_message = "Empty blocks: "
while hpixel < DISPLAY_H:
    wpixel = 0
    while wpixel < DISPLAY_W:
        if background.get_at((wpixel, hpixel))[3] == 0:
            empty_space.append([wpixel, hpixel])
            empty_space_message += str(wpixel) + ", " + str(hpixel) + "; "
        wpixel += 16
    hpixel += 16
    if not empty_space_message.endswith("\n"):
        empty_space_message += "\n"
print(empty_space_message)

#check which blocks are above the floor
floor_blocks = []
for key, value in enumerate(empty_space):
    x, y = value
    block_below = [x, y + 16]

    if block_below not in empty_space:
        floor_blocks.append(empty_space[key])

################################# LOAD PLAYER ###################################
cat = Player()
################################# GAME LOOP ##########################
while running:
    clock.tick(60)

    ################################# CHECK PLAYER INPUT #################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                cat.LEFT_KEY, cat.FACING_LEFT = True, True
            elif event.key == pygame.K_RIGHT:
                cat.RIGHT_KEY, cat.FACING_LEFT = True, False
            elif event.key == pygame.K_UP:
                cat.UP_KEY = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                cat.LEFT_KEY = False
            elif event.key == pygame.K_RIGHT:
                cat.RIGHT_KEY = False
            elif event.key == pygame.K_UP:
                cat.UP_KEY = False
    
    ################################# UPDATE/ Animate SPRITE #################################
    cat.update(empty_space)
    catx = cat.rect.x
    caty = cat.rect.y
    
    ########## MOUSE CHECK ########

    def check_mouse(mousex, mousey, catx, caty ):
        if(catx - mousex) <= mouse_size and (mousex - catx) <= cat_w:
            if(caty - mousey) <= mouse_size and (mousey - caty) <= cat_h:
                return True
        return False
    
    
    if mouse_count < 0 or check_mouse(mousex, mousey, catx, caty):
        mousex, mousey = floor_blocks[random.randrange(0, len(floor_blocks))][0], floor_blocks[random.randrange(0, (len(floor_blocks)-20))][1]
        while check_mouse(mousex, mousey, catx, caty):
            mousex, mousey = floor_blocks[random.randrange(0, len(floor_blocks))][0], floor_blocks[random.randrange(0, (len(floor_blocks)-20))][1]
        print("spawned a mouse at", mousex, mousey)
        mouse_count += 1
        print("Mouse count:", mouse_count)

    ################################# UPDATE WINDOW AND DISPLAY #################################
    canvas.fill((255,255,255))
    canvas.blit(background, (0,0))
    cat.draw(canvas)
    window.blit(canvas, (0,0))
    window.blit(mouse, (mousex, mousey))
    counter_text = font.render("Score - " + str(mouse_count), True, (0, 0, 0))
    window.blit(counter_text, (10, 10))
    pygame.display.update()


#################https://www.youtube.com/watch?v=1_H7InPMjaY##################