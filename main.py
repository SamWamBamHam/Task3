import pygame
from hexArray import createHexArray, drawHexArray, revealTile, flagTile

pygame.init()
mainSurface = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
menu = "main"
firstFrame = True
holdingLCtrl = False
gameSize = 7
font = pygame.font.Font()

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
        if menu == "game":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if holdingLCtrl:
                    if event.button == 1:
                        flagTile(hexGrid, event.pos)
                else:
                    if event.button == 1:
                        revealTile(hexGrid, event.pos, 30, True)
                    elif event.button == 3:
                        flagTile(hexGrid, event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    hexGrid = createHexArray(gameSize, mainSurface, pixelSize)
    mainSurface.fill("purple")

    #Render Start Here

    if firstFrame:
        menu = "game"
        pixelSize = 30
        del font
        font = pygame.font.Font(size=pixelSize)
        hexGrid = createHexArray(gameSize, mainSurface, pixelSize)
        firstFrame = False

    drawHexArray(hexGrid, font)

    #Render End Here

    pygame.display.flip()

    clock.tick(60)

pygame.quit()