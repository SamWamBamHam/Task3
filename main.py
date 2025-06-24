import pygame
from time import monotonic
from hexArray import createHexArray, drawHexArray, revealTile, flagTile, countUnflagged, collectHexReferences
from hexagon import Hexagon
from button import Button
from buttonFuncs import findClosestButton, findIndexOfButtonByFunction
from dbFuncs import getAll, login, signUp, addToVars
from text import Text

pygame.init()
mainSurface = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
menu = "login"
firstFrame = True
holdingLCtrl = False
holdingEsc = False
holdingBackspace = False
backspaceFrames = 0
gameSize = 7
regFont = pygame.font.Font(size = 30)
bigFont = pygame.font.Font(size = 60)
buttonList = []
textList = []
hexGrid = None
escCounter = 0
gameState = None
focusedTextbox = None
typedText = ""
usernameText = ""
passwordText = ""
usernameButtonPos = (570, 360)
passwordButtonPos = (570, 460)
bannedCharacters = ["'", '"']
loginLeftMargin = usernameButtonPos[0]-50
loginAlertText = ""
loginButtonsWidth = 100
loginColumGap = 20
username = None
startTime = 0
addedToDb = True
update = True

def goToHex():
    global firstFrame, menu, startTime, addedToDb
    firstFrame = True
    menu = "hex"
    if not addedToDb:
        addToDb()
    startTime = monotonic()
    addedToDb = False

def goToMain():
    global firstFrame, menu
    firstFrame = True
    if menu == "hex":
        addToDb()
    menu = "main"

def addToDb():
    global hexGrid, startTime, addedToDb
    revealed, flagged = 0, 0
    success = True
    for hex in collectHexReferences(hexGrid):
        assert isinstance(hex, Hexagon)
        if hex.getFlagged():
            flagged += 1
        elif hex.getRevealed() and not hex.getMine():
            revealed += 1
        if (not hex.getRevealed() and not hex.getMine()) or (hex.getMine() and hex.getRevealed()):
            success = False
    totalTime = int((monotonic() - startTime)*1000)
    addToVars(username, 1 if success else 0, 1, totalTime, flagged, revealed)
    addedToDb = True

def goToStats():
    global firstFrame, menu
    firstFrame = True
    menu = "stats"

def quit():
    global running, menu
    if menu == "hex":
        addToDb()
    running = False

def doSignup():
    global usernameText, passwordText, username, loginAlertText
    success = signUp(usernameText, passwordText)
    if success:
        username = usernameText
        goToMain()
    else:
        loginAlertText = "Username already exists"

def doLogin():
    global usernameText, passwordText, username, loginAlertText
    success = login(usernameText, passwordText)
    if success:
        username = usernameText
        goToMain()
    else:
        loginAlertText = "Invalid credentials"

def unfocus():
    global focusedTextbox, typedText, usernameText, passwordText
    focusedTextbox = None
    typedText = ""
    pygame.key.stop_text_input()
    button = findIndexOfButtonByFunction(buttonList, focusPassword)
    buttonList.remove(button)
    if passwordText == "":
        buttonList.append(Button(passwordButtonPos, 100, 60, False, mainSurface, (150, 180, 210), "Password", regFont, True, focusPassword))
    else:
        buttonList.append(Button(passwordButtonPos, 100, 60, False, mainSurface, (150, 180, 210), passwordText, regFont, True, focusPassword))
    button = findIndexOfButtonByFunction(buttonList, focusUsername)
    buttonList.remove(button)
    if usernameText == "":
        buttonList.append(Button(usernameButtonPos, 100, 60, False, mainSurface, (150, 180, 210), "Username", regFont, True, focusUsername))
    else:
        buttonList.append(Button(usernameButtonPos, 100, 60, False, mainSurface, (150, 180, 210), usernameText, regFont, True, focusUsername))

def focusUsername():
    global focusedTextbox, usernameText, typedText, buttonList
    focusedTextbox = "username"
    typedText = usernameText
    pygame.key.start_text_input()
    button = findIndexOfButtonByFunction(buttonList, focusUsername)
    buttonList.remove(button)
    buttonList.append(Button(usernameButtonPos, 100, 60, False, mainSurface, (170, 200, 230), usernameText, regFont, True, focusUsername))

def focusPassword():
    global focusedTextbox, typedText, passwordText, buttonList
    focusedTextbox = "password"
    typedText = passwordText
    pygame.key.start_text_input()
    button = findIndexOfButtonByFunction(buttonList, focusPassword)
    buttonList.remove(button)
    buttonList.append(Button(passwordButtonPos, 100, 60, False, mainSurface, (170, 200, 230), passwordText, regFont, True, focusPassword))

while running == True:

    # Inputs work by figuring out everything that happened this frame, then resolving them dependent
    # on which menu your are currently in
    leftClick, rightClick, rClick, escClick, tabClick = False, False, False, False, False
    typedButton = None
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                quit()

        # Rather than checking each frame, check when the left ctrl state changes
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_LCTRL:
                        holdingLCtrl = True
                    case pygame.K_r:
                        rClick = True
                    case pygame.K_ESCAPE:
                        holdingEsc = True
                        escClick = True
                    case pygame.K_BACKSPACE:
                        holdingBackspace = True
                    case pygame.K_TAB:
                        tabClick = True

            case pygame.KEYUP:
                match event.key:
                    case pygame.K_LCTRL:
                        holdingLCtrl = False
                    case pygame.K_ESCAPE:
                        holdingEsc = False
                    case pygame.K_BACKSPACE:
                        holdingBackspace = False
                        backspaceFrames = 0

            case pygame.MOUSEBUTTONDOWN:
                position = (event.pos[0], event.pos[1])
                if event.button == 3 or (event.button == 1 and holdingLCtrl):
                    rightClick = True
                elif event.button == 1:
                    leftClick = True

            case pygame.TEXTINPUT:
                typedButton = event.text
                if typedButton in bannedCharacters:
                    typedButton = None

    match menu:
        case "main":
            if leftClick:
                closestButton = findClosestButton(buttonList, position)
                if closestButton != False:
                    function = closestButton.getClickFunction()
                    if function:
                        function()
            if holdingEsc:
                escCounter += 1
                if escCounter == 90:
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
        
        case "login":
            if leftClick:
                closestButton = findClosestButton(buttonList, position)
                if closestButton:
                    unfocus()
                    clickFunction = closestButton.getClickFunction()
                    clickFunction()
                else:
                    unfocus()
            oldTypedText = typedText
            if holdingBackspace:
                backspaceFrames += 1
                if typedText != "" and (backspaceFrames == 1 or (backspaceFrames > 30 and backspaceFrames%5 ==1)):
                    typedText = typedText[0:-1]
            if typedButton != None:
                if len(typedText) < 20:
                    typedText += typedButton
            if len(typedText) == 20:
                loginAlertText = "You have reached the maximum character limit"
            elif loginAlertText == "You have reached the maximum character limit":
                loginAlertText = ""
            if oldTypedText != typedText:
                if focusedTextbox == "username":
                    usernameText = typedText
                    button = findIndexOfButtonByFunction(buttonList, focusUsername)
                    buttonList.remove(button)
                    del button
                    buttonList.append(Button(usernameButtonPos, 100, 60, False, mainSurface, (170, 200, 230), typedText, regFont, True, focusUsername))
                elif focusedTextbox == "password":
                    passwordText = typedText
                    button = findIndexOfButtonByFunction(buttonList, focusPassword)
                    buttonList.remove(button)
                    del button
                    buttonList.append(Button(passwordButtonPos, 100, 60, False, mainSurface, (170, 200, 230), typedText, regFont, True, focusPassword))
            if tabClick:
                match focusedTextbox:
                    case "username":
                        unfocus()
                        focusPassword()
                    case "password":
                        unfocus()
                        focusUsername()

    mainSurface.fill("purple")

    #Render Start Here
    if firstFrame:
        textToggle = False
        pygame.key.stop_text_input()
        update = True
        buttonList = []
        textList = []
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
                for hex in collectHexReferences(hexGrid):
                    buttonList.append(hex)
                buttonList.append(Button((1140, 80), 140, 60, False, mainSurface, (160, 200, 180), "Restart (R)", regFont, False, goToHex))
                buttonList.append(Button((1140, 170), 140, 60, False, mainSurface, (160, 200, 180), "Back to Menu", regFont, False, goToMain))
            case "stats":
                null1, null2, games, wins, time, flags, revealed = getAll(username)
                statsPos = (640, 160)
                textList.append(Text(statsPos, "right", "Wins: ", regFont, mainSurface))
                textList.append(Text((statsPos[0], statsPos[1]+70), "right", "Losses: ", regFont, mainSurface))
                textList.append(Text((statsPos[0], statsPos[1]+140), "right", "Win Rate: ", regFont, mainSurface))
                textList.append(Text((statsPos[0], statsPos[1]+210), "right", "Avg Game Time: ", regFont, mainSurface))
                textList.append(Text((statsPos[0], statsPos[1]+280), "right", "Total Flags: ", regFont, mainSurface))
                textList.append(Text((statsPos[0], statsPos[1]+350), "right", "Total Revealed: ", regFont, mainSurface))

                textList.append(Text(statsPos, "left", str(wins), regFont, mainSurface))
                textList.append(Text((statsPos[0], statsPos[1]+70), "left", str(games-wins), regFont, mainSurface))
                textList.append(Text((statsPos[0], statsPos[1]+140), "left", f"{round((1-wins/games)*100)}%", regFont, mainSurface))
                textList.append(Text((statsPos[0], statsPos[1]+210), "left", f"{round(time/1000/games)} seconds", regFont, mainSurface))
                textList.append(Text((statsPos[0], statsPos[1]+280), "left", str(flags), regFont, mainSurface))
                textList.append(Text((statsPos[0], statsPos[1]+350), "left", str(revealed), regFont, mainSurface))


                # CHANGE TEMP DO SOMETHING
                
            case "login":
                buttonList.append(Button(usernameButtonPos, 100, 60, False, mainSurface, (150, 180, 210), "Username", regFont, True, focusUsername))
                buttonList.append(Button(passwordButtonPos, 100, 60, False, mainSurface, (150, 180, 210), "Password", regFont, True, focusPassword))
                buttonList.append(Button((loginLeftMargin-loginColumGap-int(loginButtonsWidth/2), passwordButtonPos[1]+100), loginButtonsWidth, 40, False, mainSurface, (200, 200, 200), "Login", regFont, False, doLogin))
                buttonList.append(Button((loginLeftMargin+int(loginButtonsWidth/2), passwordButtonPos[1]+100), loginButtonsWidth, 40, False, mainSurface, (200, 200, 200), "Signup", regFont, False, doSignup))
        firstFrame = False
    match menu:
        case "main":
            for button in buttonList:
                button.drawSelf()
            textRender = bigFont.render(f"User: {username}", False, 0)
            size = bigFont.size(f"User: {username}")
            mainSurface.blit(textRender, (100, 100+size[1]))
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
            for text in textList:
                text.drawSelf()
        case "login":
            for button in buttonList:
                if button.getClickFunction() in (focusPassword, focusUsername):
                    button.drawSelf(loginLeftMargin)
                else:
                    button.drawSelf()
            size = regFont.size("Username:")
            textRender = regFont.render("Username:", False, 0)
            mainSurface.blit(textRender, (loginLeftMargin-loginColumGap-size[0], usernameButtonPos[1]-size[1]/2))
            textRender = regFont.render("Password: ", False, 0)
            mainSurface.blit(textRender, (loginLeftMargin-loginColumGap-size[0], passwordButtonPos[1]-size[1]/2))
            if loginAlertText != "":
                size = regFont.size(loginAlertText)
                textRender = regFont.render(loginAlertText, False, (230, 20, 20))
                mainSurface.blit(textRender, (640-size[0]/2, 120-size[1]/2))
    #Render End Here

    if update:
        pygame.display.flip()
        if menu == "stats":
            update = False
    else:
        if menu != "stats":
            update = True

    clock.tick(60)

pygame.quit()