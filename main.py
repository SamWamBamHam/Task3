import pygame
from hexArray import createHexArray, drawHexArray, revealTile, flagTile
from hexagon import Hexagon
from button import Button
from buttonFuncs import findClosestButton

pygame.init()
mainSurface = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
menu = "main"
firstFrame = True
holdingLCtrl = False
gameSize = 7
font = pygame.font.Font()
buttonList = []
hexGrid = None

while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    
            running = False
        # Rather than checking each frame, check when the left ctrl state changes
        if event.type == pygame.KEYDOWN:
            if event.key == 1073742048:
                holdingLCtrl = True
        if event.type == pygame.KEYUP:
            if event.key == 1073742048:
                holdingLCtrl = False
        # When in the game, m1 reveals, ctrl + m1 flags, m2 flags and R starts a new game
        if menu == "hex":
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                button = findClosestButton(buttonList, position)
                if button != False:
                    if isinstance(button, Hexagon):
                        if holdingLCtrl:
                            if event.button == 1:
                                flagTile(hexGrid, button.getCoords())
                        else:
                            if event.button == 1:
                                revealTile(hexGrid, button.getCoords(), 30, True)
                            elif event.button == 3:
                                flagTile(hexGrid, button.getCoords())
                    else:
                        pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    newButtonList = []
                    for button in buttonList:
                        if not isinstance(button, Hexagon):
                            newButtonList.append(button)
                    buttonList = newButtonList
                    del newButtonList
                    hexGrid = createHexArray(gameSize, mainSurface, pixelSize)
                    for row in hexGrid:
                        for cell in row:
                            if isinstance(cell, Button):
                                buttonList.append(cell)
    
    mainSurface.fill("purple")

    #Render Start Here
    if firstFrame:
        match menu:
            case "main":
                #buttonList.append(Button())
                # CHANGE TEMP DO SOMETHING
                pass
            case "hex":
                pixelSize = 30
                del font
                font = pygame.font.Font(size=pixelSize)
                hexGrid = createHexArray(gameSize, mainSurface, pixelSize)
                for row in hexGrid:
                    for cell in row:
                        if isinstance(cell, Hexagon):
                            buttonList.append(cell)
        firstFrame = False
    else:
        match menu:
            case "main":
                menu = "hex"
                firstFrame = True
            case "hex":
                mainSurface.fill((185, 226, 245))
                drawHexArray(hexGrid, font)

    #Render End Here

    pygame.display.flip()

    clock.tick(60)

pygame.quit()