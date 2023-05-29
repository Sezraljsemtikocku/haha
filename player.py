import pygame
from spritesheet import Spritesheet

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
        
        leftFloor = [self.rect.bottomleft[0]-self.rect.bottomleft[0]%16, self.rect.bottomleft[1]-self.rect.bottomleft[1]%16]
        rightFloor = [self.rect.bottomright[0]-self.rect.bottomright[0]%16, self.rect.bottomright[1]-self.rect.bottomright[1]%16]
        midFloor = [self.rect.midbottom[0]-self.rect.midbottom[0]%16, self.rect.midbottom[1]-self.rect.midbottom[1]%16]
        #falling/jumping logic
        if leftFloor in empty_blocks and rightFloor in empty_blocks and midFloor in empty_blocks:
            #fix so the cat doesn't sink into the floor
            leftFloor = [self.rect.bottomleft[0]-self.rect.bottomleft[0]%16, self.rect.bottomleft[1]+2-self.jump_velocity-(self.rect.bottomleft[1]+2-self.jump_velocity)%16]
            rightFloor = [self.rect.bottomright[0]-self.rect.bottomright[0]%16, self.rect.bottomright[1]+2-self.jump_velocity-(self.rect.bottomright[1]+2-self.jump_velocity)%16]
            midFloor = [self.rect.midbottom[0]-self.rect.midbottom[0]%16, self.rect.midbottom[1]+2-self.jump_velocity-(self.rect.midbottom[1]+2-self.jump_velocity)%16]
            if leftFloor not in empty_blocks or rightFloor not in empty_blocks or midFloor not in empty_blocks:
                self.rect.y += 1
                print("Fell only one block!")
            else:
                self.rect.y += 2
            if self.jump_velocity != 0:
                self.jump_velocity -= 2
        elif self.UP_KEY:
            self.jump_velocity = 14
        self.rect.y -= (self.jump_velocity)

        #walking logic
        leftWall = [self.rect.bottomleft[0]+self.velocity-(self.rect.bottomleft[0]+self.velocity)%16, self.rect.bottomleft[1]-1-(self.rect.bottomleft[1]-1)%16]
        rightWall = [self.rect.bottomright[0]-(self.rect.bottomright[0])%16, self.rect.bottomright[1]-1-(self.rect.bottomright[1]-1)%16]
        if (self.FACING_LEFT and (leftWall in empty_blocks)) or ((not self.FACING_LEFT) and (rightWall in empty_blocks)):
            self.rect.x += self.velocity
        if (leftWall not in empty_blocks or rightWall not in empty_blocks) and self.velocity != 0:
            print("Stuck on a wall!")
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