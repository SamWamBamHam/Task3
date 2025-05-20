import pygame
class Button():
    def __init__(self, centre, width, height, isCircle, surface, colour, text, font, uniqueTitle, clickFunction = None):
        self.centre = centre
        if isCircle:
            self.isCircle = True
            self.clickRadius = width/2
        else:
            self.isCircle = False
            self.width = width
            self.height = height
        self.surface = surface
        self.colour = colour
        self.text = text
        self.clickFunction = clickFunction
        self.font = font
        self.title = uniqueTitle

    def getTitle(self):
        return self.title

    def getText(self):
        return self.text
    
    def getFont(self):
        return self.font

    def getClickFunction(self):
        return self.clickFunction

    def getCentre(self):
        return self.centre
    
    def getColour(self):
        return self.colour
    
    def getSurface(self):
        return self.surface
    
    def getClickRadius(self):
        return self.clickRadius
    
    def getIsCircle(self):
        return self.isCircle
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def drawSelf(self):
        centre = self.getCentre()
        if self.getIsCircle():
            pygame.draw.circle(self.getSurface(), self.getColour(), centre, self.getClickRadius())
            pygame.draw.circle(self.getSurface(), 0, centre, self.getClickRadius(), round(self.getClickRadius()/10))
        else:
            width = self.getWidth()
            height = self.getHeight()
            corners = ((centre[0]+width/2, centre[1]+height/2), (centre[0]+width/2, centre[1]-height/2), (centre[0]-width/2, centre[1]-height/2), (centre[0]-width/2, centre[1]+height/2))
            pygame.draw.polygon(self.getSurface(), self.getColour(), corners)
            pygame.draw.polygon(self.getSurface(), 0, corners, round((width+height)/35))
        font = self.getFont()
        text = self.getText()
        assert isinstance(font, pygame.font.Font)
        textSurface = font.render(text, False, 0)
        sizeOf = font.size(text)
        self.getSurface().blit(textSurface, (centre[0]-sizeOf[0]/2, centre[1]-sizeOf[1]/2))