import pygame
import random
import math

class star:
    def __init__(self):
        self.color = (255,255,255)
        self.x = 0
        self.y = random.randrange(0,screenHeight-150)
        self.dx = 10

    def update(self):
        size = random.randrange(1,3)
        self.x = self.x + self.dx
        self.starObj = pygame.draw.rect(screen,(255,255,255),[self.x,self.y,size,size])

class word:
    def __init__(self):
        self.word = random.choice(wordList)
        self.x = screenWidth
        self.y = random.randrange(0,screenHeight-150)
        self.dx = 0.6
        self.font = pygame.font.Font("Adobe_Dia.ttf",34)
        
    def update(self,color):
        text_surface = self.font.render(self.word, True, color)
        self.x = self.x - self.dx
        screen.blit(text_surface, (int(self.x),int(self.y)))

def updateText(text,x,y):
    font = pygame.font.Font("Adobe_Dia.ttf",32).render(text, True, (0,0,0))
    screen.blit(font,(x,y))

def drawInputText(text,y):
    font = pygame.font.Font("Adobe_Dia.ttf",34).render(text, True, (0,0,0))
    text_width = font.get_width()
    screen.blit(font,(int(screenWidth/2-(text_width/2)),y))

def checkWPM(liste):
    characters = 0
    for item in liste:
        characters += len(item)
    return (characters/(seconds/60))/5
def checkCurrentWPM(liste):
    characters = 0
    for item in liste:
        characters += len(item)
    return characters/5/0.06

def checkInput(word,liste):
    for x in liste:
        if x.word == word:
            del liste[liste.index(x)]
            return True

with open("words.txt") as f:
    wordList = f.read().splitlines()
        
wordScreenList = []
starScreenList = []
screenWidth = 800
screenHeight = 600
userInput = ""
correctWords = []
recentCorrectWords = []
missedWords = 0
inputWidth = None
i= 0

pygame.init()
screen = pygame.display.set_mode([screenWidth,screenHeight])
running = True
word1 = word()
while running:
    seconds = pygame.time.get_ticks()/1000
    screen.fill((0,0,0))
    pygame.draw.rect(screen,(0,0,255),[0,screenHeight-100,screenWidth,150])
    drawInputText(userInput, screenHeight-40)
    for item in starScreenList:
        item.update()
        if item.x >= screenWidth:
            del starScreenList[starScreenList.index(item)]
    
    for item in wordScreenList:
        if screenWidth/4 < item.x <= screenWidth/2:
            item.update((0,255,0))
        elif item.x <= screenWidth/4:
            item.update((255,0,0))
        else:
            item.update((255,255,255))
        for subItem in wordScreenList:
            if item != subItem:
                if item.x - subItem.x < 70 and -15 < (item.y - subItem.y) < 15:
                    del wordScreenList[wordScreenList.index(subItem)]
        if item.x <= 0:
            del wordScreenList[wordScreenList.index(item)]
            missedWords += 1
    
    
    if random.randrange(1,100) == 2:
        wordScreenList.append(word())
    
    if i == 50:
        starScreenList.append(star())
        i = 0
    i+=1

    for item in recentCorrectWords:
        if item[1] <= seconds - 10:
            del recentCorrectWords[recentCorrectWords.index(item)]

    updateText("Average WPM: " + str(round((checkWPM(correctWords)))),5,screenHeight-75)
    updateText("Current WPM: " + str(round(checkCurrentWPM(recentCorrectWords))),5,screenHeight-25)
    updateText("Elapsed Time: " + str(round(divmod(seconds,60)[0]))+":"+str(round(divmod(seconds,60)[1],1)),550,screenHeight-75)
    updateText("Missed Words: " + str(missedWords),550,screenHeight-25)
    pygame.time.Clock().tick(144)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if checkInput(userInput,wordScreenList) == True:
                    correctWords.append(userInput)
                    recentCorrectWords.append((userInput,seconds))
                userInput = "" 
            elif event.key == pygame.K_BACKSPACE:
                userInput= userInput[:-1]
            elif event.unicode.isalpha():
             userInput += event.unicode
            elif event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False
        
    


