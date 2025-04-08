import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

from RubiksCube import RubiksCube
from button import Button


# Rotation angles
x_rot = -75  # Tilt the view slightly from the top (set to -75)
z_rot = -15  # Slight rotation along the horizontal axis (set to -15)
zoom = -40  # Default zoom distance

# Mouse interaction flags
mouse_down = False
last_x, last_y = 0, 0

def draw_axes():
    """ Draw Z, X, and Y axes with labels """
    glColor3f(1, 1, 1)  # White color for all lines
    
    # Draw the Z axis line (from z = -10 to z = 10)
    glBegin(GL_LINES)
    glVertex3f(0, 0, -10)
    glVertex3f(0, 0, 10)
    glEnd()

    # Draw tick marks on the Z axis (from z = -10 to z = 10)
    tick_interval = 1  # Create ticks every 1 unit (both odd and even indices)
    for z in range(-10, 11, tick_interval):  # Including both negative and positive Z values
        glBegin(GL_LINES)
        glVertex3f(0.2, 0, z)
        glVertex3f(-0.2, 0, z)
        glEnd()


    # X-axis line (from x = -10 to x = 10)
    glBegin(GL_LINES)
    glVertex3f(-10, 0, 0)
    glVertex3f(10, 0, 0)
    glEnd()
    
    # Y-axis line (from y = -10 to y = 10)
    glBegin(GL_LINES)
    glVertex3f(0, -10, 0)
    glVertex3f(0, 10, 0)
    glEnd()
    
    """
    # Labels for Z axis (+z and -z)
    render_text(0.1, 0.0, 10, "+z")
    render_text(0.1, 0.0, -11, "-z")

    # Labels for X axis (+x and -x)
    render_text(11, 0, 0, "+x")
    render_text(-11, 0, 0, "-x")

    # Labels for Y axis (+y and -y)
    render_text(0, 11, 0, "+y")
    render_text(0, -11, 0, "-y")
    """

def render_text(x, y, z, text):
    """ Render text at a specific position """
    font = pygame.font.SysFont("Arial", 24)
    label = font.render(text, True, (255, 255, 255))
    text_texture = pygame.image.tostring(label, "RGB")
    
    glRasterPos3f(x, y, z)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(char))

def draw_grid():
    """ Draw grid lines in the XY plane at Z = 0 """
    glColor3f(1, 1, 1)  # White color for grid
    glBegin(GL_LINES)
    
    # Draw lines in the XY plane (grid)
    for i in range(-10, 11):
        # Horizontal lines
        glVertex3f(i, -10, 0)
        glVertex3f(i, 10, 0)
        # Vertical lines
        glVertex3f(-10, i, 0)
        glVertex3f(10, i, 0)
    
    glEnd()

def draw_square(x1, y1, z1, x2, y2, z2, color):
    """ Draw a filled square from (x1, y1, z1) to (x2, y2, z2) with a given color """
    glColor3f(*color)  # Set the color for the square

    # Define the four vertices of the square
    if x1 == x2: points = [(x1, y1, z1), (x1, y1, z2), (x1, y2, z2), (x1, y2, z1)]
    if y1 == y2: points = [(x1, y1, z1), (x2, y1, z1), (x2, y1, z2), (x1, y2, z2)]
    if z1 == z2: points = [(x1, y1, z1), (x2, y1, z1), (x2, y2, z2), (x1, y2, z1)]
    
    # Draw the square as a filled quad
    glBegin(GL_QUADS)
    for point in points:
        glVertex3f(*point)
    glEnd()

def draw_cube(cube):
    """ Draw a cube centered at (0, 0, 0) with faces of size 12 """
    
    colors = {"Y": (1, 1, 0),
              "B": (0, 0, 1),
              "R": (1, 0, 0),
              "G": (0, 1, 0),
              "O": (1, 0.5, 0),
              "W": (1, 1, 1)}

    draw_square(-6, -6, 6, 6, 6, 6, (0, 0, 0)) # U
    for x in range(3):
        for y in range(3):
            x1, y1, x2, y2 = -5.8 + x * 4, 5.8 - y * 4, -2.2 + x * 4, 2.2 - y * 4
            draw_square(x1, y1, 6.01, x2, y2, 6.01, colors[cube.U[y][x]])
            
    draw_square(-6, -6, -6, 6, -6, 6, (0, 0, 0)) # F
    for x in range(3):
        for y in range(3):
            x1, y1, x2, y2 = -5.8 + x * 4, 5.8 - y * 4, -2.2 + x * 4, 2.2 - y * 4
            draw_square(x1, -6.01, y1, x2, -6.01, y2, colors[cube.F[y][x]])
            
    draw_square(6, -6, -6, 6, 6, 6, (0, 0, 0)) # R
    for x in range(3):
        for y in range(3):
            x1, y1, x2, y2 = -5.8 + x * 4, 5.8 - y * 4, -2.2 + x * 4, 2.2 - y * 4
            draw_square(6.01, x1, y1, 6.01, x2, y2, colors[cube.R[y][x]])
            
    draw_square(-6, 6, -6, 6, 6, 6, (0, 0, 0)) # B
    for x in range(3):
        for y in range(3):
            x1, y1, x2, y2 = 5.8 - x * 4, 5.8 - y * 4, 2.2 - x * 4, 2.2 - y * 4
            draw_square(x1, 6.01, y1, x2, 6.01, y2, colors[cube.B[y][x]])
            
    draw_square(-6, -6, -6, -6, 6, 6, (0, 0, 0)) # L
    for x in range(3):
        for y in range(3):
            x1, y1, x2, y2 = 5.8 - x * 4, 5.8 - y * 4, 2.2 - x * 4, 2.2 - y * 4
            draw_square(-6.01, x1, y1, -6.01, x2, y2, colors[cube.L[y][x]])
    
    draw_square(-6, -6, -6, 6, 6, -6, (0, 0, 0)) # D
    for x in range(3):
        for y in range(3):
            x1, y1, x2, y2 = -5.8 + x * 4, -5.8 + y * 4, -2.2 + x * 4, -2.2 + y * 4
            draw_square(x1, y1, -6.01, x2, y2, -6.01, colors[cube.D[y][x]])

    glColor3f(1, 1, 1)
    render_text(-0.2, 0, 8, "U")
    render_text(-0.2, -8, 0, "F")
    render_text(8, 0, 0, "R")
    render_text(-0.2, 8, 0, "B")
    render_text(-8.2, 0, 0, "L")
    render_text(-0.2, 0, -8, "D")

def handle_mouse_motion(x, y):
    """ Handle mouse dragging to rotate the view """
    global x_rot, z_rot, last_x, last_y, mouse_down

    if mouse_down:
        dx = x - last_x
        dy = y - last_y
        
        # Use z_rot for horizontal dragging (rotate around the Z-axis)
        z_rot += dx

        # For vertical dragging, adjust x_rot (rotate around the X-axis)
        x_rot += dy

    last_x, last_y = x, y

def handle_mouse_scroll(scroll):
    """ Handle zoom in and out with the scroll wheel """
    global zoom
    zoom += scroll * 2  # Zoom in or out by 2 units

def setup_view():
    """ Set up perspective and camera view """
    glClearColor(0, 0, 0, 1)  # Black background
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear both color and depth buffers
    glLoadIdentity()

    # Adjust aspect ratio to keep grid lines square
    width, height = pygame.display.get_surface().get_size()
    gluPerspective(45, width / height, 0.1, 50.0)  # Aspect ratio based on window size

    glTranslatef(0.0, 0.0, zoom)  # Move the scene backward by zoom distance

    # Rotate based on mouse movement
    glRotatef(x_rot, 1, 0, 0)  # Rotate around X-axis
    glRotatef(z_rot, 0, 0, 1)  # Rotate around Z-axis

def main():
    """ Main function to run the OpenGL window """
    glutInit()  # Initialize GLUT (required for text rendering)
    pygame.init()
    WIDTH = 800
    HEIGHT = 600
    display = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    RButton = Button(20, 20, 40, 40, "R", (100, 200, 255), (50, 150, 255))
    LButton = Button(80, 20, 40, 40, "L", (100, 200, 255), (50, 150, 255))
    UButton = Button(140, 20, 40, 40, "U", (100, 200, 255), (50, 150, 255))
    DButton = Button(200, 20, 40, 40, "D", (100, 200, 255), (50, 150, 255))
    FButton = Button(260, 20, 40, 40, "F", (100, 200, 255), (50, 150, 255))
    BButton = Button(320, 20, 40, 40, "B", (100, 200, 255), (50, 150, 255))
    RpButton = Button(20, 80, 40, 40, "R'", (100, 200, 255), (50, 150, 255))
    LpButton = Button(80, 80, 40, 40, "L'", (100, 200, 255), (50, 150, 255))
    UpButton = Button(140, 80, 40, 40, "U'", (100, 200, 255), (50, 150, 255))
    DpButton = Button(200, 80, 40, 40, "D'", (100, 200, 255), (50, 150, 255))
    FpButton = Button(260, 80, 40, 40, "F'", (100, 200, 255), (50, 150, 255))
    BpButton = Button(320, 80, 40, 40, "B'", (100, 200, 255), (50, 150, 255))
    xButton = Button(620, 20, 40, 40, "x", (100, 200, 255), (50, 150, 255))
    yButton = Button(680, 20, 40, 40, "y", (100, 200, 255), (50, 150, 255))
    zButton = Button(740, 20, 40, 40, "z", (100, 200, 255), (50, 150, 255))
    xpButton = Button(620, 80, 40, 40, "x'", (100, 200, 255), (50, 150, 255))
    ypButton = Button(680, 80, 40, 40, "y'", (100, 200, 255), (50, 150, 255))
    zpButton = Button(740, 80, 40, 40, "z'", (100, 200, 255), (50, 150, 255))
    
    buttons = {RButton: "R", LButton: "L", UButton: "U", DButton: "D", FButton: "F", BButton: "B",
               RpButton: "R'", LpButton: "L'", UpButton: "U'", DpButton: "D'", FpButton: "F'", BpButton: "B'",
               xButton: "x", yButton: "y", zButton: "z", xpButton: "x'", ypButton: "y'", zpButton: "z'"}
               
    scrambleButton = Button(280, 540, 100, 40, "Scramble", (100, 200, 255), (50, 150, 255))
    resetButton = Button(420, 540, 100, 40, "Reset", (100, 200, 255), (50, 150, 255))
    
    glEnable(GL_DEPTH_TEST)  # Enable depth testing
    
    cube = RubiksCube() # Create an instance of a cube
    # cube.alg("R U R' U R U R' F' R U R' U' R' F R2 U' R' U2 R U' R'") # Perform an N perm
    
    global mouse_down, last_x, last_y
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return  # Use return to exit the main function gracefully
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_down = True
                    last_x, last_y = event.pos
                    for move_button in buttons:
                        if move_button.is_clicked(*event.pos):
                            cube.move(buttons[move_button])
                            draw_cube(cube)
                    if scrambleButton.is_clicked(*event.pos):
                        cube.scramble()
                        draw_cube(cube)
                    if resetButton.is_clicked(*event.pos):
                        cube.reset()
                        draw_cube(cube)
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down = False
            if event.type == MOUSEMOTION:
                for move_button in list(buttons) + [scrambleButton, resetButton]:
                    move_button.check_hover(*event.pos)
                handle_mouse_motion(*event.pos)
            if event.type == MOUSEWHEEL:
                handle_mouse_scroll(event.y)  # Use event.y for scroll direction

        setup_view()  # Set up the view with rotation and zoom
        # draw_grid()  # Draw the grid in the XY plane
        # draw_axes()  # Draw the axes with labels
        
        
        # Draw the cube
        draw_cube(cube)
        for move_button in buttons:
            move_button.draw(screen)
        
        scrambleButton.draw(screen)
        resetButton.draw(screen)

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()

