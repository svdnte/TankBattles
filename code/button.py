import pygame.font
from mixer import play_button_sound


class Button:
    def __init__(self,
                 screen: pygame.Surface,
                 x,
                 y,
                 text,
                 text_size,
                 link,
                 bgcolor=None,
                 linecolor=None,
                 textcolor='white',
                 point_bg_color=None,
                 point_line_color=None,
                 point_text_color=None,
                 font='../data/fonts/ft40.ttf',
                 group=False) -> None:

        self.font = pygame.font.Font(font, int(text_size))
        self.offset = 35

        self.screen = screen
        self.cords = [x, y]
        self.text = text
        self.link = link
        self.bgcolor = pygame.Color(bgcolor)
        self.linecolor = pygame.Color(linecolor) if linecolor else self.bgcolor
        self.textcolor = pygame.Color(textcolor)
        self.point_bg_color = pygame.Color(point_bg_color) if point_bg_color else self.bgcolor
        self.point_line_color = pygame.Color(point_line_color) if point_line_color else self.point_bg_color
        self.point_text_color = pygame.Color(point_text_color) if point_text_color else self.textcolor

        self.st_rendered = self.font.render(text, 1, self.textcolor)
        self.st_rext = self.st_rendered.get_rect()
        self.st_rext.y = y

        self.button_surface = pygame.Surface((self.st_rext.w + self.offset * 2, self.st_rext.h + self.offset))

        if x == "c":
            self.cords[0] = screen.get_width() // 2 - self.button_surface.get_width() // 2
        elif group:
            self.cords[0] = x - self.button_surface.get_width() // 2

        self.st_rext.x = self.cords[0]
        self.rect = pygame.rect.Rect(self.cords[0], self.cords[1], self.st_rext.w + self.offset * 2,
                                     self.st_rext.h + self.offset)

        self.set_default()

    def pressed(self):
        play_button_sound()
        self.link()

    def set_default(self):
        self.button_surface.fill(self.bgcolor)
        pygame.draw.rect(self.button_surface, self.linecolor,
                         (0, 0, self.st_rext.w + self.offset * 2, self.st_rext.h + self.offset), 5)

        self.button_surface.blit(self.st_rendered,
                                 (self.offset - 0.1 * self.offset, self.offset // 2 + 0.1 * self.offset))

        self.st_rendered = self.font.render(self.text, 1, self.textcolor)

        self.screen.blit(self.button_surface, (self.cords[0], self.cords[1]))

    def pointed(self):
        if self.point_bg_color:
            self.button_surface.fill(self.point_bg_color)
        if self.point_text_color:
            self.st_rendered = self.font.render(self.text, 1, self.point_text_color)
        if self.point_line_color:
            pygame.draw.rect(self.button_surface, self.point_line_color,
                             (0, 0, self.st_rext.w + self.offset * 2, self.st_rext.h + self.offset), 5)
        self.button_surface.blit(self.st_rendered,
                                 (self.offset - 0.1 * self.offset, self.offset // 2 + 0.1 * self.offset))

        self.screen.blit(self.button_surface, (self.cords[0], self.cords[1]))
