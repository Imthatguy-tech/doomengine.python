import pygame, engine, math, time
from engine.display import Display
from engine.eventlistener import EventListener
from engine.linedef import LineDef
from engine.solidbspnode import SolidBSPNode

print("\n")

# Lines, each vertex connects to the next one in CW fashion
# third element is direction its facing, when CW facing 1 = left
polygons = [
    # open room
    [
        # x, y, facing
        [30,  30, 0],
        [300, 20, 0],
        [400, 300, 0],
        [30, 200, 0]
    ],
    # inner col
    [
        # x, y, facing
        [50,  50, 1],
        [100, 50, 1],
        [75,  75, 1],
        [100, 100, 1],
        [50,  100, 1]
    ],
    # inner room
    [
        [55, 55, 0],
        [70, 55, 0],
        [70, 95, 0],
        [55, 95, 0],
    ]
]

# Line Defs built Clockwise
allLineDefs = []
for i, v in enumerate(polygons):
    polygon = polygons[i]
    lineDefs = []
    for idx, val in enumerate(polygon):
        lineDef = LineDef()

        # first point, connect to second point
        if idx == 0:
            lineDef.asRoot(polygon[idx][0], polygon[idx][1], polygon[idx + 1][0], polygon[idx + 1][1], polygon[idx + 1][2])
            lineDefs.append(lineDef)
            allLineDefs.append(lineDef)

        # some point in the middle
        elif idx < len(polygon) - 1:
            lineDef.asChild(lineDefs[-1], polygon[idx + 1][0], polygon[idx + 1][1], polygon[idx + 1][2])
            lineDefs.append(lineDef)
            allLineDefs.append(lineDef)
        
        # final point, final line, connects back to first point
        elif idx == len(polygon) - 1:
            lineDef.asLeaf(lineDefs[-1], lineDefs[0], polygon[idx][2])
            lineDefs.append(lineDef)
            allLineDefs.append(lineDef)

solidBsp = SolidBSPNode(allLineDefs)
# print(solidBsp.toText())


# TESTING WALL DRAWING
wallTest = allLineDefs[4]
camPoint = [90, 150]
camDirRads = 0
camDir = engine.mathdef.toVector(camDirRads)


# testPoint = [60, 20]
# for lineDef in allLineDefs:
#     isBehind = lineDef.isPointBehind(testPoint[0], testPoint[1])
#     print(lineDef.start, lineDef.end, lineDef.facing, isBehind)
# print(solidBsp.inEmpty(testPoint))

display = Display(1280, 720)
listener = EventListener()
pygame.mouse.set_visible(False)
font = pygame.font.Font(None, 36)
    
# render mode ops
mode = 0
max_modes = 3
def mode_up():
    global mode
    mode = (mode + 1) % max_modes
listener.onKeyUp(pygame.K_UP, mode_up)
def mode_down():
    global mode
    mode = (mode - 1) % max_modes
listener.onKeyUp(pygame.K_DOWN, mode_down)
def on_left():
    global camDir, camDirRads
    camDirRads = camDirRads - 0.1
    camDir = engine.mathdef.toVector(camDirRads)
listener.onKeyHold(pygame.K_LEFT, on_left)
def on_right():
    global camDir, camDirRads
    camDirRads = camDirRads + 0.1
    camDir = engine.mathdef.toVector(camDirRads)
listener.onKeyHold(pygame.K_RIGHT, on_right)
def on_a():
    global camPoint
    camPoint[0] = camPoint[0] + math.sin(camDirRads)
    camPoint[1] = camPoint[1] - math.cos(camDirRads)
listener.onKeyHold(pygame.K_a, on_a)
def on_d():
    global camPoint
    camPoint[0] = camPoint[0] - math.sin(camDirRads)
    camPoint[1] = camPoint[1] + math.cos(camDirRads)
listener.onKeyHold(pygame.K_d, on_d)
def on_w():
    global camPoint
    camPoint[0] = camPoint[0] + math.cos(camDirRads)
    camPoint[1] = camPoint[1] + math.sin(camDirRads)
listener.onKeyHold(pygame.K_w, on_w)
def on_s():
    global camPoint
    camPoint[0] = camPoint[0] - math.cos(camDirRads)
    camPoint[1] = camPoint[1] - math.sin(camDirRads)
listener.onKeyHold(pygame.K_s, on_s)

fpvpX = 500
fpvpY = 100
fpvpW = 500
fpvpH = 300
fpvp = [
        [fpvpX, fpvpY],
        [fpvpX + fpvpW, fpvpY],
        [fpvpX + fpvpW, fpvpY + fpvpH],
        [fpvpX, fpvpY + fpvpH],
]

tdBounds = [
    [500 + 4, 40],
    [500 + 103, 40],
    [500 + 103, 149],
    [500 + 4, 149]
]

pjBounds = [
    [500 + 109, 40],
    [500 + 208, 40],
    [500 + 208, 149],
    [500 + 109, 149]
]

fpBounds = [
    [500 + 214, 40],
    [500 + 315, 40],
    [500 + 315, 149],
    [500 + 214, 149]
]


def inBoundPoint(point, bounds):
    point2 = point.copy()
    point2[0] += bounds[0][0]
    point2[1] += bounds[0][1]
    return point2

def inBoundLine(line, bounds):
    line2 = []
    line2.append(line[0].copy())
    line2.append(line[1].copy())
    line2[0][0] += bounds[0][0]
    line2[0][1] += bounds[0][1]
    line2[1][0] += bounds[0][0]
    line2[1][1] += bounds[0][1]
    return line2

def fncross(x1, y1, x2, y2):
    return x1 * y2 - y1 * x2

def intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    x = fncross(x1, y1, x2, y2)
    y = fncross(x3, y3, x4, y4)
    det = fncross(x1 - x2, y1 - y2, x3 - x4, y3 - y4)
    x = fncross(x, x1 - x2, y, x3 - x4) / det
    y = fncross(x, y1 - y2, y, y3 - y4) / det
    return [x, y]


while True:
    listener.update()

    display.start()

    # render the polygons directly
    if mode == 0:
        for lineDef in allLineDefs:
            display.drawLine([lineDef.start, lineDef.end], (0, 0, 255), 1)
            ln = 7
            mx = lineDef.mid[0]
            my = lineDef.mid[1]
            nx = lineDef.normals[lineDef.facing][0] * ln
            ny = lineDef.normals[lineDef.facing][1] * ln
            if lineDef.facing == 1:
                display.drawLine([ [mx, my] , [mx + nx, my + ny] ], (0, 255, 255), 1)
            else:
                display.drawLine([ [mx, my] , [mx + nx, my + ny] ], (255, 0, 255), 1)

    mx, my = pygame.mouse.get_pos()

    # render the tree
    if mode == 1:
        solidBsp.drawSegs(display)
    if mode == 2:
        solidBsp.drawFaces(display, mx, my)




    # BISQWIT
    
    wall = [ [wallTest.start[0], wallTest.start[1]], [wallTest.end[0], wallTest.end[1]] ]
    px = camPoint[0]
    py = camPoint[1]
    angle = camDirRads
    angleLength = 10

    # TOP DOWN
    
    # Render frame
    display.drawLines(tdBounds, (150, 0, 150), 2, True)

    # Render wall
    tdWall = inBoundLine(wall, tdBounds)
    display.drawLine(tdWall, (255, 50, 255), 2)

    # Render player angle
    dir = [[px, py], [px + math.cos(angle) * angleLength, py + math.sin(angle) * angleLength]]
    tdDir = inBoundLine(dir, tdBounds)
    display.drawLine(tdDir, (255, 100, 255), 1)

    # Render player pos
    tdCamPoint = inBoundPoint(camPoint, tdBounds)
    display.drawPoint(tdCamPoint, (255, 255, 255), 2)


    # PROJECTED

    # Render frame
    display.drawLines(pjBounds, (150, 150, 0), 2, True)

    # Transform vertices relative to player
    tx1 = wall[0][0] - px
    ty1 = wall[0][1] - py
    tx2 = wall[1][0] - px
    ty2 = wall[1][1] - py

    # Rotate them around the players view
    tz1 = tx1 * math.cos(angle) + ty1 * math.sin(angle)
    tz2 = tx2 * math.cos(angle) + ty2 * math.sin(angle)
    tx1 = tx1 * math.sin(angle) - ty1 * math.cos(angle)
    tx2 = tx2 * math.sin(angle) - ty2 * math.cos(angle)

    # Render wall
    pjWall = [[50 - tx1, 50 - tz1], [50 - tx2, 50 - tz2]]
    pjWall = inBoundLine(pjWall, pjBounds)
    display.drawLine(pjWall, (255, 255, 50), 2)

    # Render player angle
    pjDir = [[50, 50], [50, 50 - angleLength]]
    pjDir = inBoundLine(pjDir, pjBounds)
    display.drawLine(pjDir, (255, 255, 100), 1)

    # Render player pos
    pjCamPoint = [50, 50]
    pjCamPoint = inBoundPoint(pjCamPoint, pjBounds)
    display.drawPoint(pjCamPoint, (255, 255, 255), 2)


    # PERSPECTIVE TRANSFORMED

    # Clip
    # determine clipping, if both z's < 0 its totally behind
	# if only 1 is negative it can be clipped
    if tz1 > 0 or tz2 > 0:
        # if line crosses the players view plane clip it
        # i think the last two are set by refs
        i1 = intersect(tx1, tz1, tx2, tz2, -0.0001, 0.0001, -20, 5)
        ix1 = i1[0]
        iz1 = i1[1]
        i2 = intersect(tx1, tz1, tx2, tz2, 0.0001, 0.0001, 20, 5)
        ix2 = i2[0]
        iz2 = i2[1]
        if tz1 <= 0:
            if iz1 > 0:
                tx1 = ix1
                tz1 = iz1
            else:
                tx1 = ix2
                tz1 = iz2
        if tz2 <= 0:
            if iz1 > 0:
                tx2 = ix1
                tz2 = iz1
            else:
                tx2 = ix2
                tz2 = iz2

    # Render frame
    display.drawLines(fpBounds, (0, 150, 150), 2, True)

    if (tz1 > 0 and tz2 > 0):

        # Transform
        x1 = -tx1 * 16 / tz1
        y1a = -50 / tz1
        y1b = 50 / tz1
        x2 = -tx2 * 16 / tz2
        y2a = -50 / tz2
        y2b = 50 / tz2

        # Render
        topLine = [[50 + x1, 50 + y1a], [50 + x2, 50 + y2a]]
        bottomLine = [[50 + x1, 50 + y1b], [50 + x2, 50 + y2b]]
        leftLine = [[50 + x1, 50 + y1a], [50 + x1, 50 + y1b]]
        rightLine = [[50 + x2, 50 + y2a], [50 + x2, 50 + y2b]]
        
        fpTopLine = inBoundLine(topLine, fpBounds)
        fpBottomLine = inBoundLine(bottomLine, fpBounds)
        fpLeftLine = inBoundLine(leftLine, fpBounds)
        fpRightLine = inBoundLine(rightLine, fpBounds)
        display.drawLine(fpTopLine, (0, 255, 255), 2)
        display.drawLine(fpBottomLine, (0, 255, 255), 2)
        display.drawLine(fpLeftLine, (0, 255, 255), 2)
        display.drawLine(fpRightLine, (0, 255, 255), 2)






    # draw our position information
    text = font.render("{}, {}".format(mx, my), 1, (50, 50, 50))
    textpos = text.get_rect(centerx = display.width / 2, centery = display.height/2)
    display.drawText(text, textpos)

    # test our BSP tree
    inEmpty = solidBsp.inEmpty([mx, my])
    display.drawPoint([mx, my], (0,255,255) if inEmpty else (255, 0, 0), 4)

    display.end()

    time.sleep(1 / 60)