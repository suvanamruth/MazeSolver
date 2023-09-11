import pygame
import random
from queue import PriorityQueue

class Pixel:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size = 20
        self.visited = False
        self.walls = {"left":True, "right":True,"bottom":True,"top":True}

    def hasRight(self):
        if(self.x + 20 <= 300):
            return True
        return False

    def hasLeft(self):
        if(self.x - 20 >= 20):
            return True
        return False

    def hasTop(self):
        if(self.y - 20 >= 20):
            return True
        return False

    def hasBottom(self):
        if(self.y + 20 <= 300):
            return True
        return False


    
    def drawPixel(self):
        if self.walls.get("left"):
            pygame.draw.line(screen, (255,0,0), [self.x,self.y], [self.x, self.y+self.size], 1)
            pygame.display.flip()
        else:
            pygame.draw.line(screen, (0,0,0), [self.x,self.y], [self.x, self.y+self.size], 1)
            pygame.display.flip()
        if self.walls.get("top"):
            pygame.draw.line(screen, (255,0,0), [self.x,self.y], [self.x + self.size, self.y], 1)
            pygame.display.flip()
        else:
            pygame.draw.line(screen, (0,0,0), [self.x,self.y], [self.x + self.size, self.y], 1)
            pygame.display.flip()
        if self.walls.get("bottom"):
            pygame.draw.line(screen, (255,0,0), [self.x, self.y + self.size], [self.x + self.size, self.y + self.size], 1)
            pygame.display.flip()
        else:
            pygame.draw.line(screen, (0,0,0), [self.x, self.y + self.size], [self.x + self.size, self.y + self.size], 1)
            pygame.display.flip()
        if self.walls.get("right"):
            pygame.draw.line(screen, (255,0,0), [self.x + self.size,self.y], [self.x + self.size, self.y + self.size], 1)
            pygame.display.flip()
        else:
            pygame.draw.line(screen, (0,0,0), [self.x + self.size,self.y], [self.x + self.size, self.y + self.size], 1)
            pygame.display.flip()


def depthFirstSearch(index, gridArray, pixelStack):
    p = gridArray[index]
    #print(index, p.x, p.y)
    options = []
    p.visited = True
    if(p.hasTop()):
        if(gridArray[index - 15].visited == False):
            options.append("top")
    if(p.hasBottom()):
        if(gridArray[index + 15].visited == False):
            options.append("bottom")
    if(p.hasLeft()):
        if(gridArray[(index) - 1].visited == False):
            options.append("left")
    if(p.hasRight()):
        if(gridArray[(index) + 1].visited == False):
            options.append("right")

    if(len(options) == 0):
        if(index == 0):
            return
        else:
            #print("went here")
            nextPixel = pixelStack.pop()
            depthFirstSearch(gridArray.index(nextPixel), gridArray, pixelStack)
    else:
        randomIndex = random.randrange(0, len(options))
        nextChoice = options[randomIndex]
        nextPixel = "hi"
        if(nextChoice == "left"):
            p.walls["left"] = False 
            nextPixel = gridArray[(index) - 1]
            nextPixel.walls["right"] = False
            p.drawPixel()
            nextPixel.drawPixel()
        elif(nextChoice == "right"):
            p.walls["right"] = False
            nextPixel = gridArray[(index) + 1]
            nextPixel.walls["left"] = False
            p.drawPixel()
            nextPixel.drawPixel()
        elif(nextChoice == "bottom"):
            p.walls["bottom"] = False
            nextPixel = gridArray[index + 15]
            nextPixel.walls["top"] = False
            p.drawPixel()
            nextPixel.drawPixel()
        elif(nextChoice == "top"):
            p.walls["top"] = False
            nextPixel = gridArray[index - 15]
            nextPixel.walls["bottom"] = False
            p.drawPixel()
            nextPixel.drawPixel()
        pixelStack.append(p)
        depthFirstSearch(gridArray.index(nextPixel), gridArray, pixelStack)


def solve(startIndex):
    print("working")
    reversePath = {}
    score = {}
    for p in gridArray:
        score[p] = float("inf")

    options = PriorityQueue()
    visited = []
    visited.append(0)
    options.put((560, 560, 0, startIndex))    # total score, endScore, startScore, pixel
    while not options.empty():
        currentIndex = options.get()
        if(gridArray[currentIndex[3]].x == 300 and gridArray[currentIndex[3]].y == 300):
            break
        for direction in ("left", "right", "top", "bottom"):
            if(gridArray[currentIndex[3]].walls[direction] == False):
                if(direction == "left" and (currentIndex[3] - 1) not in visited):
                    nextPixel = currentIndex[3] - 1
                elif(direction == "right" and (currentIndex[3] + 1) not in visited):
                    nextPixel = currentIndex[3] + 1
                elif(direction == "top" and (currentIndex[3] - 15) not in visited):
                    nextPixel = currentIndex[3] - 15
                elif(direction == "bottom" and (currentIndex[3] + 15) not in visited):
                    nextPixel = currentIndex[3] + 15
                else:
                    continue

                sDist =  currentIndex[2] + 20
                eDist = abs(300 - gridArray[nextPixel].x) + abs(300 - gridArray[nextPixel].y)
                totalScore = sDist + eDist

                if(totalScore < score[gridArray[nextPixel]]):
                    visited.append(nextPixel)
                    score[gridArray[nextPixel]] = totalScore
                    options.put((totalScore, eDist, sDist, nextPixel))
                    reversePath[nextPixel] = currentIndex[3]
    
    correctPath = {}
    endIndex = 224
    while endIndex != startIndex:
        correctPath[reversePath[endIndex]] = endIndex
        endIndex = reversePath[endIndex]
    
    i = 0
    while i != 224:
        stepIndex = correctPath[i]
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(gridArray[stepIndex].x + 5, gridArray[stepIndex].y + 5, 10, 10))
        pygame.display.flip()
        i = stepIndex
        

      






if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((340,420))
    pygame.display.set_caption("Maze")
    gridArray = []
    pixelStack = []
    for i in range(20,301,20):
        for j in range(20,301,20):
            #print(i,j)
            pixel = Pixel(j,i)          #create grid using instances of pixel object
            gridArray.append(pixel)
            pixel.drawPixel()           #draw walls for each pixel
    
    depthFirstSearch(0, gridArray, pixelStack)
    pygame.draw.rect(screen, (0,255,0), pygame.Rect(301, 301, 19, 19))
    pygame.draw.rect(screen, (0,255,0), pygame.Rect(21, 21, 19, 19))
    gridArray[0].walls["right"] = False
    gridArray[0].walls["bottom"] = False
    gridArray[0].drawPixel()

    button = pygame.Rect(20, 360, 300, 40)
    font = pygame.font.SysFont(None, 24)
    img = font.render('Solve', True, (0,0,0))
    
    pygame.display.flip() 
    

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    solve(0)
                    print("finished solving")
        x,y = pygame.mouse.get_pos()
        if(button.x <= x <= button.x + 300 and button.y <= y <= button.y + 40):
            pygame.draw.rect(screen, (200,200,200), button)
            screen.blit(img, (150, 375))
        else:
            pygame.draw.rect(screen, (100,100,100), button)
            screen.blit(img, (150, 375))
        
        pygame.display.flip()
        

