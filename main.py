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
regFont = pygame.font.Font(size = 30)
bigFont = pygame.font.Font(size = 60)
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
        match menu:
            case "main":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        closestButton = findClosestButton(buttonList, event.pos)
                        if closestButton != False:
                            function = closestButton.getClickFunction()
                            if function:
                                function()
                            if button.getTitle() == "goToHex":
                                firstFrame = True
                                menu = "hex"
            case "hex":
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
        buttonList = []
        match menu:
            case "main":
                buttonList.append(Button((640, 440), 100, 60, False, mainSurface, (112, 142, 160), "Go to hex", regFont, "goToHex"))
                pass
            case "hex":
                pixelSize = 30
                hexFont = pygame.font.Font(size=pixelSize)
                hexGrid = createHexArray(gameSize, mainSurface, pixelSize)
                for row in hexGrid:
                    for cell in row:
                        if isinstance(cell, Hexagon):
                            buttonList.append(cell)
        firstFrame = False
    else:
        match menu:
            case "main":
                for button in buttonList:
                    button.drawSelf()
            case "hex":
                mainSurface.fill((185, 226, 245))
                drawHexArray(hexGrid, hexFont)

    #Render End Here

    pygame.display.flip()

    clock.tick(60)

pygame.quit()