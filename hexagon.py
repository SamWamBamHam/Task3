import pygame
from button import Button
class Hexagon(Button):
    def __init__(self, surface, size: int, centre: tuple, revealedColour: tuple, coords: tuple):
        self.surface = surface
        self.centre = centre
        self.size = size
        self.colour = (int(revealedColour[0]*0.8), int(revealedColour[1]*0.8), int(revealedColour[2]*0.8))
        # Is darker
        self.revealedColour = revealedColour
        self.mine = False
        self.revealed = False
        self.mineCount = -1
        self.flagged = False
        self.coords = coords
        self.clickRadius = size
        self.title = "hex"
        self.isCircle = True

    def setMineCount(self, count: int):
        self.mineCount = count

    def getCoords(self):
        return self.coords

    def getMineCount(self):
        return self.mineCount

    def makeMine(self):
        self.mine = True

    def getMine(self):
        return self.mine

    def getSize(self):
        return self.size

    def getColour(self):
        return self.colour

    def getRevealedColour(self):
        return self.revealedColour

    def setRevealed(self, revealed: bool):
        self.revealed = revealed

    def getRevealed(self):
        return self.revealed

    def getFlagged(self):
        return self.flagged

    def setFlagged(self, flagged: bool):
        self.flagged = flagged
    
    def flag(self):
        self.setFlagged(not self.getFlagged())

    # For testing purposes
    def drawCentre(self, borderColour):
        surface = self.getSurface()
        pygame.draw.circle(surface, borderColour, self.getCentre(), int(self.getSize()/3))

    # When left-clicked for the first time
    def reveal(self):
        self.setRevealed(True)
        if self.getMineCount() <= 0:
            return True
        else:
            return False
        # Returns whether or not 0, therefore whether or not to reveal adjacent tiles

    def drawFlag(self, sqrt3: float):
        # Draws 3 different things, the flag base, the red flag and the flag pole
        # Flag pole last because I want it to be visible over the red flag
        centre = self.getCentre()
        size = self.getSize()
        baseCorners = ((round(centre[0]-size*2/10*sqrt3), round(centre[1]+size/2)), (round(centre[0]+size*2/10*sqrt3), round(centre[1]+size/2)), (round(centre[0]), round(centre[1]+size*3/10)))
        pygame.draw.polygon(self.getSurface(), (0, 0, 0), baseCorners)
        redCorners = ((round(centre[0]), round(centre[1])), (round(centre[0]), round(centre[1]-size/2)), (round(centre[0]-size*2/10*sqrt3), round(centre[1]-size/4)))
        pygame.draw.polygon(self.getSurface(), (230, 20, 20), redCorners)
        pygame.draw.line(self.getSurface(), (0, 0, 0), (round(centre[0]), round(centre[1]+size*3/10)), (round(centre[0]), round(centre[1]-size/2)), 2)

    def drawBomb(self, surface, centre: tuple, size: int, sqrt3: float):
        pygame.draw.circle(surface, 0, centre, round(size/4))
        pygame.draw.line(surface, 0, (round(centre[0]+size*sqrt3/3), round(centre[1]+size/3)), (round(centre[0]-size*sqrt3/3), round(centre[1]-size/3)), round(size/10))
        pygame.draw.line(surface, 0, (round(centre[0]-size*sqrt3/3), round(centre[1]+size/3)), (round(centre[0]+size*sqrt3/3), round(centre[1]-size/3)), round(size/10))
        pygame.draw.line(surface, 0, (centre[0], round(centre[1]+size*2/3)), (centre[0], round(centre[1]-size*2/3)), round(size/10))

    def drawCross(self, surface, centre: tuple, size: int):
        pygame.draw.line(surface, (240, 110, 110), ((round(centre[0]+size/2)), round(centre[1]+size/2)), ((round(centre[0]-size/2)), round(centre[1]-size/2)), round(size/10))
        pygame.draw.line(surface, (240, 110, 110), ((round(centre[0]-size/2)), round(centre[1]+size/2)), ((round(centre[0]+size/2)), round(centre[1]-size/2)), round(size/10))

    def drawSelf(self, font, borderColour, sqrt3: float, gameActive: bool):
        # To save CPU, calculate sqrt3 once and send to all things
        # Classic computing problem, where space and speed can be traded. I chose speed over space bc I don't trust pygame
        size = self.getSize()
        centre = self.getCentre()
        x = centre[0]-size/2
        y = centre[1]-size*sqrt3/2
        # Kinda just trace the hexagon, then save those points
        corners = []
        x += size
        corners.append((x, y))
        x += size/2
        y += size/2*sqrt3
        corners.append((x, y))
        x -= size/2
        y += size/2*sqrt3
        corners.append((x, y))
        x -= size
        corners.append((x, y))
        x -= size/2
        y -= size/2*sqrt3
        corners.append((x, y))
        x += size/2
        y -= size/2*sqrt3
        corners.append((x, y))
        for i in range(6):
            x, y = corners[i]
            corners.pop(i)
            corners.insert(i, (round(x), round(y)))
        surface = self.getSurface()
        if not self.getRevealed() or (not gameActive and self.getMine() and not self.getFlagged()) or self.getFlagged():
            pygame.draw.polygon(surface, self.getColour(), corners, 0)
        else:
            pygame.draw.polygon(surface, self.getRevealedColour(), corners, 0)
        # Border last so that its on top
        pygame.draw.polygon(surface, borderColour, corners, int(size/10))
        if self.getRevealed() and not self.getFlagged():
            text = str(self.getMineCount())
            assert isinstance(font, pygame.font.Font)
            # Testing out some new syntax. Its pretty sweet
            # Different colours per number so that a glance tells you the number, rather than a read
            match text:
                case "-1":
                    self.drawBomb(surface, centre, size, sqrt3)
                case "0":
                    pass
                case "1":
                    textSurface = font.render(text, True, (20, 20, 250))
                case "2":
                    textSurface = font.render(text, True, (20, 180, 50))
                case "3":
                    textSurface = font.render(text, True, (200, 200, 20))
                case "4":
                    textSurface = font.render(text, True, (240, 100, 20))
                case "5":
                    textSurface = font.render(text, True, (230, 20, 20))
                case "6":
                    textSurface = font.render(text, True, (200, 30, 200))
            if int(text) > 0:
                sizeOf = font.size(text)
                # Rendering text makes its own image 'Surface', which must be added, or 'blit'ed to the main surface
                self.getSurface().blit(textSurface, (centre[0]-sizeOf[0]/2, centre[1]-sizeOf[1]/2))
        elif self.getFlagged():
            if gameActive or self.getMine():
                self.drawFlag(sqrt3)
            else:
                self.drawCross(surface, centre, size)
