'''Author : Howard Leung
   
   Date: May, 4th, 2017
   
   Description: A reincarnation of the video game Smash Bros! Win by
   defeating the other player.
'''
# I - IMPORT AND INITIALIZE
import pygame, BreakSprites, time
pygame.init()     

def main():
    '''This function defines the 'mainline logic' for our pySmash game.'''
      
    # DISPLAY
    
    screen = pygame.display.set_mode((1280, 720))    
    pygame.display.set_caption("Super Smash Bros Py!")
     
    # ENTITIES
    background = pygame.image.load('back.jpg')
    background = background.convert()

    screen.blit(background, (0, 0))

    
    #Music and sound effects
    pygame.mixer.music.load("fdmusic.mp3")
    pygame.mixer.music.set_volume(0.7)
  #  pygame.mixer.music.play(-1)
    boing = pygame.mixer.Sound("bounce.wav")
    boing.set_volume(0.5)   
    # Sprites for: Players

    font = pygame.font.SysFont("Rockwell Extra Bold", 300)
    end = font.render('Mr.Rao Wins!',1,(0,255,0))
    player1 = BreakSprites.Player(screen, 'playeridle.png', (440,360))
    p1arrow = BreakSprites.Arrow(player1.givepos())
    player2 = BreakSprites.Player(screen, 'playeridle.png', (840,360))
    life1  =BreakSprites.Lives((300,690))
    life2  =BreakSprites.Lives((590,690))
    stars = BreakSprites.Stars(screen)
    platform = BreakSprites.EndZone(screen,(640,630),"platform.png")
    platline = BreakSprites.Platform()
    health1= BreakSprites.ScoreKeeper((350,625))
    health2= BreakSprites.ScoreKeeper((620,625))
    player1bar = BreakSprites.PlayerBar('playerbar.png', (120,570))
    player2bar = BreakSprites.PlayerBar('player2bar.png', (400,570))
    player1group = pygame.sprite.Group(player1)
    player2group = pygame.sprite.Group(player2)
    ground = pygame.sprite.Group(platline)
    allSprites = pygame.sprite.OrderedUpdates( stars,  platline ,\
                                      platform, player1,player2, health1, health2, \
                                      player1bar, player2bar, life1, life2, p1arrow)

    # ASSIGN 
    clock = pygame.time.Clock()
    keepGoing = True
    gameover = False
    keys1 = 0
    jump1 = 0
    left1 = True
    right1 = True
    keys2 = 0
    jump2 = 0
    left2 = True
    right2 = True
    jumping1 = 0
    jumping2 = 0
    rightcount1 = 0
    rightcount2 = 0
    attacklength1= 14
    attacklength2= 14
    player1attacking = False
    player2attacking = False
    timetodie1 = False
    timetodie2 = False

    
 
    # Hide the mouse pointer
    #pygame.mouse.set_visible(False)
    
    # LOOP
    while keepGoing:
     
        # TIME
        clock.tick(30)
     
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print "mouse down:", pygame.mouse.get_pos()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player1.moveleft()
                    left1 = True
                    keys1 += 1
                
                if event.key == pygame.K_RIGHT:
                    rightcount1 += 1

                    if rightcount1 > 8:
                        rightcount1 = 1
                    player1.moveright(rightcount1)
                    keys1 += 1
                    right1 = True

                if event.key == pygame.K_UP:
                    jumping1 = 1
                    jump1 += 1
                    player1.jump(jump1)
                    
                if event.key == pygame.K_COMMA:
                    if not player1attacking:
                        player1.attack() 
                        player1attacking = True
                        attacklength1 = 0
                
                if event.key == pygame.K_g:
                    player2.attack()   
                    player2attacking = True
                    attacklength2 = 0
                    
                if event.key == pygame.K_a:
                    player2.moveleft()
                    left2 = True
                    keys2 += 1
                
                if event.key == pygame.K_d:
                    rightcount2 += 1
                    if rightcount2 > 8:
                        rightcount1 = 1                    
                    player2.moveright(rightcount2)

                    keys2 += 1
                    right2 = True

                if event.key == pygame.K_w:
                    jumping2 = 1
                    jump2 += 1
                    player2.jump(jump2)
                    
 
                    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    jumping1 = 0

                if event.key == pygame.K_RIGHT:
                    right1 = False
                    keys1 -= 1
                    if keys1 == 0:
                        player1.stop()
                    elif keys1 == 1:
                        player1.moveleft()
                if event.key == pygame.K_LEFT:
                    left1 = False
                    keys1 -= 1
                    if keys1 == 0:
                        player1.stop()
                    elif keys1 == 1:
                        player1.moveright(rightcount1)
                
                
                if event.key == pygame.K_w:
                    jumping2 = 0

                if event.key == pygame.K_d:
                    right2 = False
                    keys2 -= 1
                    if keys2 == 0:
                        player2.stop()
                    elif keys2 == 1:
                        player2.moveleft()
                if event.key == pygame.K_a:
                    left2 = False
                    keys2 -= 1
                    if keys2 == 0:
                        player2.stop()
                    elif keys2 == 1:
                        player2.moveright(rightcount2)
        attacklength1 += 2
        if attacklength1 > 13:
            player1attacking = False
        attacklength2 += 2
        if attacklength2 > 13:
            player2attacking = False
        if health1.health() >= 100:
            timetodie1 = True
        if health2.health() >= 100:
            timetodie2 = True

        if pygame.sprite.spritecollide(player1, player2group, False) and \
           player1attacking:
            player2.gethit(timetodie2)
            health2.damage()
            
     
        if pygame.sprite.spritecollide(player2, player1group, False) and \
           player2attacking:
            player1.gethit(timetodie1)
            health1.damage()
            
        if pygame.sprite.spritecollide(player1, ground, False):
            player1.grounded()
            if jumping1 == 1 and jump1 != 0:
                player1.notgrounded()
            jump1 = 0
        elif not pygame.sprite.spritecollide(player1, ground, False):
            player1.notgrounded()
            
        if player1.checkdie():
            player1.reset((440,360))
            health1.died()
            life1.died()
            timetodie1 = False
            
        
        if pygame.sprite.spritecollide(player2, ground, False):
            player2.grounded()
            if jumping2 == 1 and jump2 != 0:
                player2.notgrounded()
            jump2 = 0
        elif not pygame.sprite.spritecollide(player2, ground, False):
            player2.notgrounded()
        if player2.checkdie():
            player2.reset((840,360))
            health2.died()
            life2.died()
            timetodie2 = False
            

        
            



        # REFRESH SCREEN


        allSprites.clear(screen, background)
        allSprites.update(player1.givepos())
        allSprites.draw(screen) 
  
        if not life1.life()  or not life2.life() :
            screen.blit(end,(20,200))
            keepGoing = False

        pygame.display.flip()
       
         
    # Unhide the mouse pointer
    pygame.mouse.set_visible(True)
 
    # Close the game window

    time.sleep(2)    
    pygame.quit()     
     
# Call the main function
main()    