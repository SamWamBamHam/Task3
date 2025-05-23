from hexagon import Hexagon
from math import sqrt
from random import randint

# I wanted to do this as a class, but I realised that that goes against design principles since there
# is only ever one. I still never spoke from main to hex, always used the hexArray as a middle man

#Store this:   _         Like this:   [[" ", "1", " "]    In the createHexArray function
#            _/1\_                     ["6", " ", "2"]
#           /6\_/2\                    [" ", "0", " "]
#           \_/0\_/                    ["5", " ", "3"]
#           /5\_/3\                    [" ", "4", " "]]
#           \_/4\_/
#             \_/
def createHexArray(size, mainSurface, hexSize, arrayCentre = (640, 360), colour = (128, 128, 128), randomColour = False):
    grid = [["" for i in range(size*2+1)] for j in range(size*4+1)]
    for i in range(size):
        # Before recursively adding hexes, add the first one
        if i == 0:
            grid[size*2].pop(size)
            grid[size*2].insert(size, Hexagon(mainSurface, hexSize, arrayCentre, colour, (size, size*2)))
        # Add hexes recursively, adding the 6 adjacent hexes to each hex per 'generation'
        else:
            hexCoords = []
            for hex in collectHexReferences(grid):
                hexCoords.append(hex.getCoords())
            newHexCoords = []
            for hexCoord in hexCoords:
                x, y = hexCoord
                # Relative positions of all 6 adjacent neighbours
                tempNewHexCoords = ((x, y+2), (x, y-2), (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1))
                for tempNewHexCoord in tempNewHexCoords:
                    if not ((tempNewHexCoord in newHexCoords) or (tempNewHexCoord in hexCoords)):
                        newHexCoords.append(tempNewHexCoord)
            for newHexCoord in newHexCoords:
                x, y = newHexCoord
                grid[y].pop(x)
                # Calculate the coordinates for the new hexagon
                newCentre = (arrayCentre[0]+hexSize*3/2*(x-size), arrayCentre[1]+hexSize*sqrt(3)/2*(y-size*2))
                grid[y].insert(x, Hexagon(mainSurface, hexSize, newCentre, colour, newHexCoord))
    return grid

def drawHexArray(grid, font, gameActive, borderColour=(0, 0, 0), centreOnly = False):
    # Send the square root of 3 so that each hexagon does not have to make that costly calculation
    sqrt3 = sqrt(3)
    for row in grid:
        for cell in row:
            if isinstance(cell, Hexagon):
                if centreOnly:
                    cell.drawCentre(borderColour)
                else:
                    cell.drawSelf(font, borderColour, sqrt3, gameActive)    
                    # Each hexagon draws itself, but their positions are exact so they line up
                    # This does mean that every line is drawn twice, but what can you do

# I didn't like how large the distribute mines function was, so I split them
def distributeCellNumbers(grid):
    safeHexesAndCoords = []
    # Will look like [(HexagonObjectRef, (x, y)), ...]
    mineCoords = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if isinstance(grid[y][x], Hexagon):
                currentHex = grid[y][x]
                if currentHex.getMine():
                    mineCoords.append((x, y))
                else:
                    safeHexesAndCoords.append((currentHex, (x, y)))
    for safeHex in safeHexesAndCoords:
        neighbourMines = 0
        x, y = safeHex[1]
        # Check every neighbour
        if (x+1, y+1) in mineCoords:
            neighbourMines += 1
        if (x+1, y-1) in mineCoords:
            neighbourMines += 1
        if (x-1, y+1) in mineCoords:
            neighbourMines += 1
        if (x-1, y-1) in mineCoords:
            neighbourMines += 1
        if (x, y+2) in mineCoords:
            neighbourMines += 1
        if (x, y-2) in mineCoords:
            neighbourMines += 1
        safeHex[0].setMineCount(neighbourMines)

def distributeMines(grid, percentageOfMines, safeSquares=(False)):
    totalHexes = len(collectHexReferences(grid))
    # The first square and those around it will never be mines, and therefore are not included in the calculation
    # Depends on the length of the tuple incase I change how many should be safe, which I did atleast once
    if safeSquares != (False):
        totalHexes -= len(safeSquares)
    totalMines = int(totalHexes*percentageOfMines/100)
    for hex in collectHexReferences(grid):
        if hex.getCoords() not in safeSquares:
            if randint(1, totalHexes) <= totalMines:
                hex.makeMine()
                totalMines -= 1
            totalHexes -= 1
    distributeCellNumbers(grid)

# Repetitive code, very happy that I made it a function
def collectHexReferences(grid):
    hexes = []
    for row in grid:
        for cell in row:
            if isinstance(cell, Hexagon):
                hexes.append(cell)
    return hexes

def revealTile(grid, coord, minePercentage=0, doSpread = False):
    returnValue = True
    hexes = collectHexReferences(grid)
    closestHex = grid[coord[1]][coord[0]]
    if isinstance(closestHex, Hexagon):
        firstClick = True
        for hex in hexes:
            if hex.getRevealed():
                firstClick = False
        if firstClick:
            # After the first click we distribute mines. Therefore the first click is always safe.
            # Common feature in minesweeper, known as Safe Start
            safeSquareCoords = [coord, (coord[0]+1, coord[1]+1), (coord[0]+1, coord[1]-1), (coord[0]-1, coord[1]+1), (coord[0]-1, coord[1]-1), (coord[0], coord[1]+2), (coord[0], coord[1]-2)]
            for sSCoord in safeSquareCoords:
                if not isinstance(grid[sSCoord[1]][sSCoord[0]], Hexagon):
                    safeSquareCoords.remove(sSCoord)
            distributeMines(grid, minePercentage, safeSquareCoords)
        if not closestHex.getFlagged():
            if closestHex.getRevealed():
                # For QOL, if you click a cell with enough flags around it to fill it if they were mines,
                # it reveals all tiles besides the flagged ones. I got the idea from cardgames.com/minesweeper
                if doSpread:
                    # If you don't make it check if it should spread, if it overlaps with something already
                    # revealed with enough flags, it makes an infinite loop, revealing back and forth
                    x, y = closestHex.getCoords()
                    neighbourCoords = ((x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1), (x, y+2), (x, y-2))
                    neighbourFlags = 0
                    for coord in neighbourCoords:
                        currentNeighbour = grid[coord[1]][coord[0]]
                        if isinstance(currentNeighbour, Hexagon):
                            if currentNeighbour.getFlagged():
                                neighbourFlags += 1
                    if neighbourFlags == closestHex.getMineCount() and closestHex.getMineCount() > 0:
                        for coord in neighbourCoords:
                            currentNeighbour = grid[coord[1]][coord[0]]
                            if isinstance(currentNeighbour, Hexagon):
                                if not currentNeighbour.getFlagged():
                                    revealTile(grid, currentNeighbour.getCoords())
            else:
                # Its Zero Spread time (common feature), where since a 0 must have all non-mine tiles around it, they are revealed.
                # Makes for some rewarding moments as a chunk of the grid is revealed
                isSpecial = closestHex.reveal()
                # When revealing a tile, it returns with true if you should keep revealing. Only triggered when zero
                if isSpecial:
                    if closestHex.getMine():
                        for hex in collectHexReferences(grid):
                            if hex.getMine():
                                hex.reveal()
                                returnValue = False
                    else:
                        revealTile(grid, (coord[0]+1, coord[1]+1))
                        revealTile(grid, (coord[0]+1, coord[1]-1))
                        revealTile(grid, (coord[0]-1, coord[1]+1))
                        revealTile(grid, (coord[0]-1, coord[1]-1))
                        revealTile(grid, (coord[0], coord[1]+2))
                        revealTile(grid, (coord[0], coord[1]-2))
    return returnValue

# Might be fun to have an essential game mechanic
def flagTile(grid, coord):
    closestHex = grid[coord[1]][coord[0]]
    if not closestHex.getRevealed():
        closestHex.flag()

def countUnflagged(grid):
    hexes = collectHexReferences(grid)
    mines, flags = (0, 0)
    for hex in hexes:
        if hex.getFlagged():
            flags += 1
        if hex.getMine():
            mines += 1
    return (mines - flags)