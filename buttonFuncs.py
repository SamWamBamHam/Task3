# With this file I can handle many, many buttons on one screen. Maybe even too many
def findClosestButton(buttonList: list, pos:tuple):
    closestButton = None
    # The highest distance possible is 1280^2+720^2 which pales in comparison to integer limit (I hope)
    closestDist = 2147483647
    if buttonList != []:
        for button in buttonList:
            centre = button.getCentre()
            dist = (centre[0]-pos[0])**2+(centre[1]-pos[1])**2
            if dist < closestDist:
                closestDist = dist
                closestButton = button
                tie = False
            elif dist == closestDist:
                tie = True
                # I don't want to leave things up to chance for the player (besides the game itself), so no equally valid clicks
        if closestButton.getIsCircle():
            maxRad = closestButton.getClickRadius()
            if closestDist > maxRad**2 or tie:
                return False
            else:
                return closestButton
        else:
            width = closestButton.getWidth()
            height = closestButton.getHeight()
            centre = closestButton.getCentre()
            if centre[0]-width/2 <= pos[0] <= centre[0] + width/2 and centre[1]-height/2 <= pos[1] <= centre[1]+height/2:
                return closestButton
            else:
                return False
    else:
        return False
    
def findIndexOfButtonByFunction(buttonList: list, function):
    for button in buttonList:
        if button.getClickFunction() == function:
            return button
    return False