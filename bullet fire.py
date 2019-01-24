import pygame
import random
 
BLACK = (0, 0, 0)
WHITE = (255,255,255)
BLUE = (0, 0, 255)
DEEP_PINK = (255,20,147)
CYAN =( 0,255 ,255)
PURPLE = (160, 32,240)
class Block(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface([30, 15])
        self.image.fill(color)
        self.rect = self.image.get_rect()
class Player(pygame.sprite.Sprite):
    
 
    def __init__(self):
        
        
        super().__init__()
 
        self.image = pygame.Surface([30, 20])
        self.image.fill(PURPLE)
 
        self.rect = self.image.get_rect()
 
    def update(self):
        
        pos = pygame.mouse.get_pos()
 
        
        self.rect.x = pos[0]
 
 
class Bullet(pygame.sprite.Sprite):
    
    def __init__(self):
        
        super().__init__()
        self.image = pygame.Surface([5, 12])
        self.image.fill(DEEP_PINK)
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.y -= 3
pygame.init()
screen_width = 1000
screen_height = 500
screen = pygame.display.set_mode([screen_width, screen_height])
all_sprites_list = pygame.sprite.Group()
block_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group() 
pygame.display.update()
for i in range(20):
    block = Block(CYAN)
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(400)
    block_list.add(block)
    all_sprites_list.add(block)
player = Player()
all_sprites_list.add(player)
 

done = False
clock = pygame.time.Clock()
font = pygame.font.Font(None, 46)
score = 0
player.rect.y = 475
while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            bullet = Bullet()
            
            bullet.rect.x = player.rect.x
            bullet.rect.y = player.rect.y
            
            all_sprites_list.add(bullet)
            bullet_list.add(bullet)
 
    all_sprites_list.update()
 
    
    for bullet in bullet_list:
 
        
        block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)
 
        
        for block in block_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1
            print(score)
    
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            
 
    screen.fill(BLACK)
    all_sprites_list.draw(screen)
    text = font.render("Score: "+str(score), True, WHITE)
    screen.blit(text, [10, 10])
    pygame.display.flip()
    clock.tick(60)
    if score == 20:
        import dc
pygame.quit()