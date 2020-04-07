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
        self.font = pygame.font.Font(fontName,34)
        self.color = (255,255,255)
        text_surface = self.font.render(self.word, True, self.color)
        self.width = text_surface.get_width()
        
    def update(self):
        text_surface = self.font.render(self.word, True, self.color)
        self.x = self.x - self.dx
        screen.blit(text_surface, (int(self.x),int(self.y)))

def updateText(text,x,y):
    font = pygame.font.Font(fontName,32).render(text, True, (0,0,0))
    screen.blit(font,(x,y))

def drawInputText(text,y):
    font = pygame.font.Font(fontName,34).render(text, True, (0,0,0))
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
            checkScore(x)
            del liste[liste.index(x)]
            return x.color
def checkScore(x):
        score = 0
        if x == (255,255,255):
            score = 1
        elif x == (0,255,0):
            score = 2
        elif x ==(255,0,0):
            score = 3
        return score


with open("words.txt") as f:
    wordList = f.read().splitlines()

fontName = "Adobe_Dia.ttf"       
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

score = 0
Name = ""

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
            item.color = (0,255,0)
            item.update()
        elif item.x <= screenWidth/4:
            item.color = (255,0,0)
            item.update()
        else:
            item.update()
        for subItem in wordScreenList:
            if item != subItem:
                if item.x - subItem.x < 70 and -15 < (item.y - subItem.y) < 15:
                    del wordScreenList[wordScreenList.index(subItem)]

        if item.x <= -item.width:
            del wordScreenList[wordScreenList.index(item)]
            score = score - 1
            missedWords += 1
            print(score)
    
    
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
                inputVarColor = checkInput(userInput,wordScreenList)
                if inputVarColor == (255,255,255) or (0,255,0) or (255,0,0):
                    correctWords.append(userInput)
                    recentCorrectWords.append((userInput,seconds))
                    score += checkScore(inputVarColor)
                    print(score)
                userInput = "" 
            elif event.key == pygame.K_BACKSPACE:
                userInput= userInput[:-1]
            elif event.unicode.isalpha():
             userInput += event.unicode
            elif event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False
        
    


