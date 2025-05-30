import pygame
from hexArray import createHexArray, drawHexArray, revealTile, flagTile, countUnflagged
from hexagon import Hexagon
from button import Button
from buttonFuncs import findClosestButton
from dbFuncs import getAll, login, signUp

pygame.init()
mainSurface = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
menu = "main"
firstFrame = True
holdingLCtrl = False
holdingEsc = False
gameSize = 7
regFont = pygame.font.Font(size = 30)
bigFont = pygame.font.Font(size = 60)
buttonList = []
hexGrid = None
escCounter = 0
gameState = None

def goToHex():
    global firstFrame
    firstFrame = True
    global menu
    menu = "hex"

def goToMain():
    global firstFrame
    firstFrame = True
    global menu
    menu = "main"

def goToStats():
    global firstFrame
    firstFrame = True
    global menu
    menu = "stats"

def quit():
    global running
    running = False

while running == True:

    # Inputs work by figuring out everything that happened this frame, then resolving them dependent
    # on which menu your are currently in
    leftClick, rightClick, rClick, escClick = False, False, False, False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    
            quit()

        # Rather than checking each frame, check when the left ctrl state changes
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                holdingLCtrl = True
            elif event.key == pygame.K_r:
                rClick = True
            elif event.key == pygame.K_ESCAPE:
                holdingEsc = True
                escClick = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                holdingLCtrl = False
            elif event.key == pygame.K_ESCAPE:
                holdingEsc = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            position = (event.pos[0], event.pos[1])
            if event.button == 3 or (event.button == 1 and holdingLCtrl):
                rightClick = True
            elif event.button == 1:
                leftClick = True

    match menu:
        case "main":
            if leftClick:
                closestButton = findClosestButton(buttonList, event.pos)
                if closestButton != False:
                    function = closestButton.getClickFunction()
                    if function:
                        function()
            if holdingEsc:
                escCounter += 1
                if escCounter == 120:
                    quit()
            else:
                escCounter = 0

        case "hex":
            # When in the game, m1 reveals, ctrl + m1 flags, m2 flags and R starts a new game
            if leftClick or rightClick:
                closestButton = findClosestButton(buttonList, position)
                if closestButton != False:
                    if isinstance(closestButton, Hexagon):
                        if gameState == None:
                            if rightClick:
                                flagTile(hexGrid, closestButton.getCoords())
                            elif leftClick:
                                gameState = revealTile(hexGrid, closestButton.getCoords(), 30, True)
                    else:
                        function = closestButton.getClickFunction()
                        if function:
                            function()
            if rClick:
                goToHex()
            if escClick:
                goToMain()
    
    mainSurface.fill("purple")

    #Render Start Here
    if firstFrame:
        buttonList = []
        match menu:
            case "main":
                buttonList.append(Button((640, 440), 100, 60, False, mainSurface, (112, 142, 160), "Go to hex", regFont, False, goToHex))
                buttonList.append(Button((1200, 80), 100, 100, False, mainSurface, (200, 170, 117), "Quit (Hold Esc)", regFont, True, quit))
                buttonList.append(Button((640, 640), 100, 60, False, mainSurface, (112, 142, 160), "Go to Stats", regFont, False, goToStats))
            case "hex":
                gameState = None
                pixelSize = 30
                hexFont = pygame.font.Font(size=pixelSize)
                hexGrid = createHexArray(gameSize, mainSurface, pixelSize)
                for row in hexGrid:
                    for cell in row:
                        if isinstance(cell, Hexagon):
                            buttonList.append(cell)
                buttonList.append(Button((1140, 80), 140, 60, False, mainSurface, (160, 200, 180), "Restart (R)", regFont, False, goToHex))
                buttonList.append(Button((1140, 170), 140, 60, False, mainSurface, (160, 200, 180), "Back to Menu", regFont, False, goToMain))
            case "stats":
                pass
        firstFrame = False
    match menu:
        case "main":
            for button in buttonList:
                button.drawSelf()
        case "hex":
            mainSurface.fill((185, 226, 245))
            for button in buttonList:
                if not isinstance(button, Hexagon):
                    button.drawSelf()
            match gameState:
                case None:
                    unflaggedText = f"Mines: {countUnflagged(hexGrid)}"
                    if unflaggedText != "Mines: 0":
                        unflaggedTextSurface = bigFont.render(unflaggedText, False, 0)
                        mainSurface.blit(unflaggedTextSurface, (50, 50))
                case "Win":
                    winTextSurface = bigFont.render("You Win!", False, (50, 180, 50))
                    mainSurface.blit(winTextSurface, (50, 50))
                case "Failure":
                    failureTextSurface = bigFont.render("You Lost...", False, (180, 50, 50))
                    mainSurface.blit(failureTextSurface, (50, 50))
            drawHexArray(hexGrid, hexFont, gameState == None)
        case "stats":
            pass

    #Render End Here

    pygame.display.flip()

    clock.tick(60)

pygame.quit()