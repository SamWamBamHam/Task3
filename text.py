from pygame import font as pygameFont
from pygame import surface as pygamesurface
class Text():
    def __init__(self, pos: tuple, align: str, text: str, font, surface):
        self.pos = pos
        self.align = align
        self.text = text
        self.font = font
        self.surface = surface
    
    def getPos(self):
        return self.pos
    
    def getAlign(self):
        return self.align
    
    def getText(self):
        return self.text
    
    def getFont(self):
        return self.font
    
    def getSurface(self):
        return self.surface

    def drawSelf(self):
        pos, align, text, font, surface = self.getPos(), self.getAlign(), self.getText(), self.getFont(), self.getSurface()
        assert isinstance(font, pygameFont.Font)
        assert isinstance(surface, pygamesurface.Surface)
        sizeOf = font.size(text)
        textRender = font.render(text, False, 0)
        match align:
            case "left":
                surface.blit(textRender, pos)
            case "centre":
                surface.blit(textRender, (pos[0]-sizeOf[0]/2, pos[1]))
            case "right":
                surface.blit(textRender, (pos[0]-sizeOf[0], pos[1]))