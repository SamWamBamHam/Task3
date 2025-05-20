import pygame
class Button():
    def __init__(self, centre, menu, width, height, isCircle, surface, colour, text, clickFunction):
        self.centre = centre
        self.menu = menu
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

    def getText(self):
        return self.text

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
    
    def getMenu(self):
        return self.menu
    
    def getIsCircle(self):
        return self.isCircle
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def drawSelf(self, font):
        if self.getIsCircle():
            pygame.draw.circle(self.getSurface(), self.getColour(), self.getCentre(), self.getClickRadius())
            pygame.draw.circle(self.getSurface(), 0, self.getCentre(), self.getClickRadius(), round(self.getClickRadius()/10))
        else:
            centre = self.getCentre()
            width = self.getWidth()
            height = self.getHeight()
            corners = ((centre[0]+width/2, centre[1]+height/2), (centre[0]+width/2, centre[1]-height/2), (centre[0]-width/2, centre[1]-height/2), (centre[0]-width/2, centre[1]+height/2))
            pygame.draw.polygon(self.getSurface(), self.getColour(), corners)
            pygame.draw.polygon(self.getSurface(), 0, corners, round((width**2+height**2)/10))
        assert isinstance(font, pygame.font.Font)
        font.render(self.getText(), False, 0)