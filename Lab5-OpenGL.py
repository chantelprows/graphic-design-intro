import sys
import math

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GL import glOrtho
    from OpenGL.GLU import gluPerspective
    from OpenGL.GL import glRotated
    from OpenGL.GL import glTranslated
    from OpenGL.GL import glLoadIdentity
    from OpenGL.GL import glMatrixMode
    from OpenGL.GL import GL_MODELVIEW
    from OpenGL.GL import GL_PROJECTION
except:
    print("ERROR: PyOpenGL not installed properly. ")

DISPLAY_WIDTH = 500.0
DISPLAY_HEIGHT = 500.0

def init():
    glClearColor (0.0, 0.0, 0.0, 0.0)
    glShadeModel (GL_FLAT)

def drawHouse ():
    glLineWidth(2.5)
    glColor3f(1.0, 0.0, 0.0)
    #Floor
    glBegin(GL_LINES)
    glVertex3f(-5.0, 0.0, -5.0)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 0, 5)
    glVertex3f(5, 0, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 0, -5)
    #Ceiling
    glVertex3f(-5, 5, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 5, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(-5, 5, 5)
    glVertex3f(-5, 5, 5)
    glVertex3f(-5, 5, -5)
    #Walls
    glVertex3f(-5, 0, -5)
    glVertex3f(-5, 5, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 0, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 5, 5)
    #Door
    glVertex3f(-1, 0, 5)
    glVertex3f(-1, 3, 5)
    glVertex3f(-1, 3, 5)
    glVertex3f(1, 3, 5)
    glVertex3f(1, 3, 5)
    glVertex3f(1, 0, 5)
    #Roof
    glVertex3f(-5, 5, -5)
    glVertex3f(0, 8, -5)
    glVertex3f(0, 8, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(-5, 5, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(0, 8, -5)
    glEnd()

x_ = 0 #Global Variables
y_ = 0
z_ = -34
p = 1
r = 0

def display():
    glClear (GL_COLOR_BUFFER_BIT)
    glColor3f (1.0, 1.0, 1.0)
    # viewing transformation

    glMatrixMode(GL_PROJECTION) #Set Projection matrix according to Projection setting
    glLoadIdentity()

    if p == 1:
        gluPerspective(90, 1, 1, 100) #These numbers found by experimentation
    else:
        glOrtho(-30, 30, -20, 20, 1, 100)


    glMatrixMode(GL_MODELVIEW) #Set Camera Matrix
    glLoadIdentity()

    glRotated(r, 0, 1, 0)
    glTranslated(x_, y_, z_)



    drawHouse()


    glFlush()


def keyboard(key, x, y):
    global x_ #you have to do this with global variables so python doesnt get confused
    global y_
    global z_
    global p
    global r

    if key == chr(27):
        import sys
        sys.exit(0)

    if key == b'w':
        z_ = z_ + math.sin(math.radians(r + 90)) #matrix relative to where camera is rotated
        x_ = x_ + math.cos(math.radians(r + 90))

    if key == b'a':
        z_ = z_ - math.sin(math.radians(r + 180))
        x_ = x_ - math.cos(math.radians(r + 180))

    if key == b'd':
        z_ = z_ + math.sin(math.radians(r + 180))
        x_ = x_ + math.cos(math.radians(r + 180))

    if key == b's':
        z_ = z_ - math.sin(math.radians(r + 90))
        x_ = x_ - math.cos(math.radians(r + 90))

    if key == b'q':
        r = r + 1

    if key == b'e':
        r = r - 1

    if key == b'r':
        y_ = y_ - 1

    if key == b'f':
        y_ = y_ + 1

    if key == b'h':
        x_ = 0
        y_ = 0
        z_ = -34
        p = 1
        r = 0

    if key == b'o':
        p = 0

    if key == b'p':
        p = 1

    glutPostRedisplay()


glutInit(sys.argv)
glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize (int(DISPLAY_WIDTH), int(DISPLAY_HEIGHT))
glutInitWindowPosition (100, 100)
glutCreateWindow (b'OpenGL Lab')
init ()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMainLoop()
