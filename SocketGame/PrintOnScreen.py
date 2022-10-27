import pygame

WHITE = (255, 255, 255)

font_name = pygame.font.match_font('arial')

#印出分數
def write_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)    #True是代表要用反鋸齒
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)  #畫出文字