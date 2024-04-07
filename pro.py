import random  
import sys
import pygame
from pygame.locals import *

FPS = 32
SCREENWIDTH = 911
SCREENHEIGHT = 500

SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY = int(SCREENHEIGHT * 0.8)

GAME_SPRITES = {}
GAME_SOUNDS = {}

PLAYER = 'gallery/images/bird.png'
BACKGROUND = 'gallery/images/background.png'
BACKGROUND2 = 'gallery/images/background2.png'
PIPE = 'gallery/images/pipe.png'

def welcomeScreen():

    messagex = int(0)
    messagey = int(GAME_SPRITES['base'].get_height())
    
    basex = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            
            else :
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)



def mainGame():

    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENHEIGHT / 2)

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #list of upper pipes
    upperPipes = [
        {'x' : SCREENWIDTH, 'y' : newPipe1[0]['y']},
        {'x' : SCREENWIDTH + SCREENWIDTH/2, 'y' : newPipe2[0]['y']}
    ]

    lowerPipes = [
        {'x' : SCREENWIDTH, 'y' : newPipe1[1]['y']},
        {'x' : SCREENWIDTH + SCREENWIDTH/2, 'y' : newPipe2[1]['y']}
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8    #speed when flapped
    playerFlapped = False

    while True :
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['fly'].play()
        
        crashTest = isCollide(playerx,playery,upperPipes,lowerPipes)

        if crashTest:
            return
        
        playerMidPos = playerx + GAME_SPRITES['player'].get_width() / 2
        for pipe in upperPipes :
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos and playerMidPos < pipeMidPos + 4 :
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play() 

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        
        if playerFlapped:
            playerFlapped = False
        
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, SCREENHEIGHT - playery - playerHeight)   #don't cross the bottom

        #moving pipe to left
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX
        
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if  upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background2'],(0, 0))

        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['player'],(playerx, playery))

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        
        Xoffset = (SCREENWIDTH - width) / 2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT / 5 ))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx,playery,upperPipes,lowerPipes):
    if playery > SCREENHEIGHT - GAME_SPRITES['player'].get_height() - 1 or playery < 0:
        GAME_SOUNDS['fall'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and (abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width())):
            GAME_SOUNDS['fall'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y'] and (abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width())):
            GAME_SOUNDS['fall'].play()
            return True     

    return False        

def getRandomPipe():

    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 5     # 100
    y2 = 2.5 * offset + random.randrange(0, int(SCREENHEIGHT - 3 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = y2 - 1.5 * offset - pipeHeight
    pipe = [
            {'x' : pipeX, 'y' : y1}, #upper pipe
            {'x' : pipeX, 'y' : y2} #lower pipe
    ]

    return pipe    

if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Siddharth Singhal')

    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/images/0.png').convert_alpha(),
        pygame.image.load('gallery/images/1.png').convert_alpha(),
        pygame.image.load('gallery/images/2.png').convert_alpha(),
        pygame.image.load('gallery/images/3.png').convert_alpha(),
        pygame.image.load('gallery/images/4.png').convert_alpha(),
        pygame.image.load('gallery/images/5.png').convert_alpha(),
        pygame.image.load('gallery/images/6.png').convert_alpha(),
        pygame.image.load('gallery/images/7.png').convert_alpha(),
        pygame.image.load('gallery/images/8.png').convert_alpha(),
        pygame.image.load('gallery/images/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] = pygame.image.load('gallery/images/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/images/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
    pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
    pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['background2'] = pygame.image.load(BACKGROUND2).convert()
    GAME_SPRITES['player'] =  pygame.image.load(PLAYER).convert()

    GAME_SOUNDS['fall'] = pygame.mixer.Sound('gallery/audio/fall.wav')
    GAME_SOUNDS['fly'] = pygame.mixer.Sound('gallery/audio/fly.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')

    while True :
        welcomeScreen()
        mainGame()
        
