'''Author : Howard Leung
   
   Date: May, 4th, 2017
   
   Description: A file containing all the sprites for my Break-Out game.
'''
import pygame, random



class EndZone(pygame.sprite.Sprite):
    '''This class defines the sprite for our Platform.'''
    def __init__(self, screen, position, picture):
        '''This initializer takes a screen surface as a parameter, initializes
        the image and rect attributes of the Platform.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Set the image and rect attributes for the endzone
        self.image = pygame.image.load(picture)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = position
        


class Player(pygame.sprite.Sprite):
    '''This class defines the sprite for our player.'''
    def __init__(self, screen, picture,position):
        '''This initializer takes a screen surface as a parameter, initializes
        the image and rect attributes, and direction of the player.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Set the image and rect attributes for the player
        self.image = pygame.image.load(picture)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.__screen = screen
        self.rect.center = position
 
        # Instance variables to keep track of the screen surface
        # and set the initial x and y vector for the ball.
        self.__screen = screen
        self.__dx = 0
        self.__gravity = 8
        self.__jump = 0
        self.__rightcount = 0
        self.__leftcount = 0
        self.__attackcount=  0
        self.__right = False
        self.__left = False
        self.__attack = False
        self.__attackdelay = 20
        self.__hit = 20

    def givepos(self):
        return self.rect.center
    def attack(self):
        self.__attack = True
        
    def jump(self,jump1):
        if jump1 < 2:
            self.__jump = -26
    
    def gethit(self,timetodie):
        self.__hit = 0
        if timetodie:
            self.__dx = 100
    def grounded(self):
        self.__gravity = 0
    def notgrounded(self):
        self.__gravity = 8
    def moveright(self,rightcount):
        '''This method moves the player right'''
        self.__dx = 10
        self.__right = True
        self.__left = False
        
        
    def moveleft(self):
        '''This method moves the player left'''
        self.__dx = -10
        self.__left = True
        self.__right = False
        
    def stop(self):
        '''This method stops the player from moving'''
        self.__dx = 0
        self.image = pygame.image.load('playeridle.png').convert_alpha()  
        self.__right = False
        self.__left = False
    def checkdie(self):
        if (self.rect.top> self.__screen.get_height()) or (self.rect.right < 0) \
           or (self.rect.left > self.__screen.get_width()):
            return True
        else:
            return False
            
    def reset(self,position):
        self.rect.center = position
        self.__dx = 0
        
        
    def update(self,position):
        '''This method will be called automatically to reposition the
        player sprite on the screen.'''
        if self.__hit < 20 :
            self.image = pygame.image.load('hurt.png').convert_alpha()
        if self.__hit > 20 :
            self.image = pygame.image.load('playeridle.png').convert_alpha()
        
        if self.__attack and self.__attackdelay > 19 and self.__dx >= 0 :
            self.__attackcount += 1
            self.image = pygame.image.load('attack'+str(self.__attackcount)+'.png').convert_alpha()
            if self.__attackcount == 13:
                self.__attackcount = 1
                self.__attack = False
                self.__attackdelay = 0
        if self.__attack and self.__attackdelay > 19 and self.__dx < 0:
            self.__attackcount += 1
            self.image = pygame.image.load('attackleft'+str(self.__attackcount)+'.png').convert_alpha()
            if self.__attackcount == 13:
                self.__attackcount = 1
                self.__attack = False
                self.__attackdelay = 0   
        self.__hit+= 2
        self.__attackdelay += 1
        if self.__right and not self.__attack :
            self.__rightcount += 1

            if self.__rightcount > 24:
                self.__rightcount = 1
        
            self.image = pygame.image.load('run'+str(self.__rightcount)+'.png').convert_alpha()
            
        if self.__left and not self.__attack :
            self.__leftcount += 1

            if self.__leftcount > 24:
                self.__leftcount = 1
        
            self.image = pygame.image.load('runleft'+str(self.__leftcount)+'.png').convert_alpha()
            
        self.rect.left += self.__dx
        self.rect.top += self.__gravity + self.__jump
        if self.__jump < 0:
            self.__jump += 1
      #  print self.rect.left
      #  print self.rect.right

            
class ScoreKeeper(pygame.sprite.Sprite):
    '''This class defines a label sprite to display the score.'''
    def __init__(self,position):
        '''This initializer loads the system font "Arial", and
        sets the starting score to 0:0'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Load our custom font, and initialize the starting score.
        self.__font = pygame.font.SysFont("Rockwell Extra Bold", 100)
        self.__font.set_italic(1)
        self.__percent = 0
        self.__position=position

        self.__colour = (255, 255, 255)
                         
         
    def damage(self):
        self.__percent += random.randrange(1,3)
    def died(self):
        self.__percent = 0
        self.__colour = (255,255,255)
        
    def health(self):
        return self.__percent

    def checkalive(self):
        '''This method checks if the ball is still alive and returns True if it is
        or false if it isn't'''
        if self.__lives <= 0:
            return True
        else: 
            return False
 
    def update(self,position):
        '''This method will be called automatically to display 
        the current score and lives at the top of the game window.'''
        if self.__percent >= 100:
            self.__colour = (255, 0, 0)
        message = str(self.__percent)
        self.image = self.__font.render(message, 1, self.__colour)
        self.rect = self.image.get_rect()
        self.rect.center = self.__position
class Lives(pygame.sprite.Sprite):
    '''This class defines a label sprite to display the score.'''
    def __init__(self,position):
        '''This initializer loads the system font "Arial", and
        sets the starting score to 0:0'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Load our custom font, and initialize the starting score.
        self.__font = pygame.font.SysFont("Rockwell Extra Bold", 50)
        self.__font.set_italic(1)
        self.__position=position
        self.__lives = 3
        self.__colour = (255, 255, 255)
                         
        
    def died(self):
        '''This method deletes a life value'''
        self.__lives -= 1
        
    def life(self):

        
        return self.__lives
 
    def update(self,position):
        '''This method will be called automatically to display 
        the current score and lives at the top of the game window.'''
        message = str(self.__lives)
        self.image = self.__font.render('Lives: '+message, 1, self.__colour)
        self.rect = self.image.get_rect()
        self.rect.center = self.__position
        
class Stars(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('stars.png')
        self.image = self.image.convert_alpha()
        self.__screen = screen
        self.rect = self.image.get_rect()
        self.rect.right = self.__screen.get_width()
        self.rect.top = self.__screen.get_height()/6
    def update(self,position):
        if self.rect.left < 0:
            self.rect.right += 4
        else:
            self.rect.right = (self.__screen.get_width())
class Platform(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('platline.png')
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = (161,460)
class PlayerBar(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (position)

class Arrow(pygame.sprite.Sprite):
    def __init__(self,  position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('p1.png')
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (position)
    def update(self,position):
        
        self.rect.center = ((position[0],position[1]-100))
