def point_in_polygon(pnt, plgn):
    # pnt - tuple of x, y point coordinates
    # plgn - list of tuples with x, y polygon coordinates 
    # return - True of False
    x = pnt[0]
    y = pnt[1]
    c = 0
    xp = []
    yp = []
    for ppnt in plgn:
        xp.append(ppnt[0])
        yp.append(ppnt[1])
    for i in range(len(xp)):
        if (((yp[i] <= y < yp[i - 1]) or (yp[i - 1] <= y < yp[i])) and
                (x > (xp[i - 1] - xp[i]) * (y - yp[i]) / (yp[i - 1] - yp[i]) + xp[i])):
            c = 1 - c
    return True if c == 1 else False

polygon = [(0, 0), (100, 0), (100, 100), (50, 50), (0, 50)]
print(point_in_polygon((51, 50), polygon))
