import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_HELVETICA_18
from OpenGL.GL import glWindowPos2f


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 24)  # Font for button text


    def draw(self, screen):
        """ Draw the button and its text """
        # First, draw the button shape using OpenGL
        self.draw_button()

        # Then draw the text on top of it using Pygame
        self.draw_text(screen)

    def draw_button(self):
        """ Draw the button shape using OpenGL """
        glPushMatrix()
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 800, 600, 0)  # 2D projection matrix for text rendering

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Change color based on hover state
        glColor3f(*([c / 255 for c in (self.hover_color if self.is_hovered else self.color)]))

        # Draw button rectangle using OpenGL
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x, self.y + self.height)
        glEnd()

        # Restore OpenGL settings
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def draw_text(self, screen):
        """ Render the button text using OpenGL bitmap fonts using glWindowPos2f (safer) """
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 800, 600, 0)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glColor3f(1.0, 1.0, 1.0)

        char_width = 9
        char_height = 18
        text_width = len(self.text) * char_width

        text_x = self.x + (self.width - text_width) / 2
        text_y = 600 - self.y - (self.height + char_height) / 2 # Adjust for baseline


        # print(f"[DEBUG] glWindowPos2f text at ({text_x}, {text_y})")

        # Use glWindowPos instead of glRasterPos
        glWindowPos2f(text_x, text_y)

        for char in self.text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        

    def is_clicked(self, mouse_x, mouse_y):
        """ Check if the button is clicked """
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height

    def check_hover(self, mouse_x, mouse_y):
        """ Check if the mouse is hovering over the button """
        self.is_hovered = self.is_clicked(mouse_x, mouse_y)
