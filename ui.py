# Code by Adrien TIMBERT @ github.com/aleolux
import pygame


# Image class
class Image:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return


# button class
# Credits: Russs123 @ https://github.com/russs123
class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


# checkbox class
# https://stackoverflow.com/questions/38551168/radio-button-in-pygame
class Checkbox:
    def __init__(self, surface, x, y, id_num, color=(230, 230, 230),
                 caption="", outline_color=(0, 0, 0), check_color=(0, 0, 0),
                 font_size=22, font_color=(0, 0, 0),
                 text_offset=(28, 1), font='Ariel Black'):
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = font_size
        self.fc = font_color
        self.to = text_offset
        self.ft = font

        # identification for removal and reorganization
        self.id_num = id_num

        # checkbox object
        self.checkbox_obj = pygame.Rect(self.x, self.y, 12, 12)
        self.checkbox_outline = self.checkbox_obj.copy()

        # variables to test the different states of the checkbox
        self.checked = False

    def _draw_button_text(self):
        self.font = pygame.font.SysFont(self.ft, self.fs)
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + self.to[0], self.y + 12 / 2 - h / 2 +
                         self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render_checkbox(self):
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
            pygame.draw.circle(self.surface, self.cc, (self.x + 6, self.y + 6), 4)

        elif not self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
        self._draw_button_text()

    def _update(self, event_object):
        x, y = pygame.mouse.get_pos()
        px, py, w, h = self.checkbox_obj
        if px < x < px + w and py < y < py + w:
            if self.checked:
                self.checked = False
            else:
                self.checked = True

    def update_checkbox(self, event_object):
        if event_object.type == pygame.MOUSEBUTTONDOWN:
            self.click = True
            self._update(event_object)
