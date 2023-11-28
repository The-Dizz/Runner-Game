import pygame
from random import randint, choice
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load player animation frames
        player_walk1 = pygame.image.load('graphics\Player/alienGreen_walk1.png').convert_alpha()
        player_walk1 = pygame.transform.scale(player_walk1, (64,84))
        player_walk2 = pygame.image.load('graphics\Player/alienGreen_walk2.png').convert_alpha()
        player_walk2 = pygame.transform.scale(player_walk2, (64,84))
        self.player_walk = [player_walk1,player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics\Player/alienGreen_jump.png').convert_alpha()
        self.player_jump = pygame.transform.scale(self.player_jump, (64, 84))
        self.player_duck = pygame.image.load('graphics\Player/alienGreen_duck.png').convert_alpha()
        self.player_duck = pygame.transform.scale(self.player_duck, (64, 42))
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (200, 300))
        self.gravity = 0

    def player_input(self):
        # Jump when space pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            jump_sound.play()

    def apply_gravity(self):
        # Apply falling after jumping
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def animation_state(self):
        keys = pygame.key.get_pressed()
        # Jump animation when above ground
        if self.rect.bottom < 300:
            self.image = self.player_jump
        # Duck animation when down arrow pressed
        elif keys[pygame.K_DOWN] and self.rect.bottom >= 300:
            self.image = self.player_duck
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.rect.height = 42  # Adjust the height for ducking
        # Walk animation
        else:
            self.player_index += 0.1  # Increment animation by .1 per frame
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.rect.height = 84  # Reset the height when not ducking

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,obstacle_type):
        super().__init__()
        self.type = obstacle_type
        
        # Load animations
        if obstacle_type == 'fly':
            fly1 = pygame.image.load('graphics\Fly/fly.png').convert_alpha()
            fly1 = pygame.transform.scale_by(fly1,  0.5)
            fly2 = pygame.image.load('graphics\Fly/fly_dead.png').convert_alpha()
            fly2 = pygame.transform.scale_by(fly2, 0.5)
            self.frames = [fly1, fly2]
            y_pos = 240 # Flys fly
        elif obstacle_type == 'snail':
            snail1 = pygame.image.load('graphics\snail/snail.png').convert_alpha()
            snail1 = pygame.transform.scale_by(snail1, 0.5)
            snail2 = pygame.image.load('graphics\snail\snail_move.png').convert_alpha()
            snail2 = pygame.transform.scale_by(snail2, 0.5)
            self.frames = [snail1, snail2]
            y_pos = 300 # Snails crawl(slither?)
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))
    
    def animation_state(self):
        if self.type == 'fly':
            self.animation_index += 0.2 # Flys increment quicker than player or snails
            if self.animation_index >= len(self.frames):
                self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]
        elif self.type == 'snail':
            self.animation_index += 0.1
            if self.animation_index >= len(self.frames):
                self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]
       
    def update(self):
        self.animation_state()
        if self.type == 'fly':
            self.rect.x -=7 # Flys move faster than snails
        elif self.type == 'snail':
            self.rect.x -=5
        self.destroy() 

    def destroy(self):
        # Delete sprite once past left side of screen
        if self.rect.x <= -100: 
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    # Load score font
    score_surface = font.render(f'Time: {current_time}',False,(64,64,64))
    score_rectangle = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rectangle)
    return current_time

def collision():
    # Game over when running into obstacles
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: 
        return True
  
pygame.init()

# Set starting game state
screen = pygame.display.set_mode((800,400)) # Set size of screen
pygame.display.set_caption('Runner') # Set title of game
clock = pygame.time.Clock() # Initiate game clock
font = pygame.font.Font('font\Pixeltype.ttf', 50) # Set font
game_active = False
start_time = 0
score = 0

# Load player
player = pygame.sprite.GroupSingle()
player.add(Player())

# Load obstacles
obstacle_group = pygame.sprite.Group()

# Load sky and ground surfaces
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Load sounds
jump_sound = pygame.mixer.Sound('audio\jump.mp3')
jump_sound.set_volume(0.5)
bgm = pygame.mixer.Sound('audio\music.wav')
bgm.set_volume(0.75)
bgm.play(loops = -1)

# Intro screen
# Player image
player_stand = pygame.image.load('graphics/Player/alienGreen_front.png').convert_alpha()
#player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rectangle = player_stand.get_rect(center = (400,200))
# Game Name
game_name = font.render('Runner Game', False, (111,196,169))
game_name_rectangle = game_name.get_rect(center = (400, 80))
# Start game screen
game_message = font.render('Press space to run', False, (111,196,169))
game_message_rectangle = game_message.get_rect(center = (400,330))

# Obstacle spawn timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Quit game
            pygame.quit()
            exit()
        if game_active: 
            if event.type == obstacle_timer: # Obstacle spawning
                obstacle_group.add(Obstacle(choice(['fly', 'snail','snail'])))
        else: # Start game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        # Blit surfaces
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = display_score()

        # Player
        player.draw(screen)
        player.update()
        
        # Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collision
        game_active = collision()
    
    else: # Start up screen
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rectangle)
        screen.blit(game_name, game_name_rectangle)

        # Score screen
        score_message = font.render(f'Score: {score}', False, (111,196,169))
        score_message_rectangle = score_message.get_rect(center = (400, 330))
        if score == 0:
            screen.blit(game_message, game_message_rectangle) 
        else: 
            screen.blit(score_message, score_message_rectangle) 
    
    pygame.display.update()
    clock.tick(60) #FPS