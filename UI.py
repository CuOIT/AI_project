import pygame
import sys

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft=(x,y)
        self.clicked= False       
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
        pygame.display.update()
        pos = pygame.mouse.get_pos()
        action = False
        if self.rect.collidepoint(pos):
            print("hover")
            if pygame.mouse.get_pressed()[0] ==1 and self.clicked == False:
                print("clicked")
                self.clicked ==True
                action = True 
        
        return action
 


 