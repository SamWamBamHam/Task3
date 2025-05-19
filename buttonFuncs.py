from button import Button

# With this class I can have many, many buttons on one screen. Maybe even too many
def findClosestButton(buttonList, pos):
    closestButton = None
    # The highest distance possible is 1280^2+720^2 which pales in comparison to integer limit (I hope)
    closestDist = 2147483647
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
    maxRad = button.getClickRadius()
    if closestDist > maxRad**2 or tie:
        return False
    else:
        return closestButton