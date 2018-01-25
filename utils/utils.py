class Intersection:
    @staticmethod
    def PointInPolygon(pnt, plgn):
        """
        :param pnt: Point coordinates (x, y), type = Tuple 
        :param plgn: Poligon points set [(x, y), (x1, y1) ... (xn, yn)], type = List of Tuples
        :return: True if point inside polygon or False, type = Boolean
        """
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

    @staticmethod
    def Rectangles(first_rectangle=(0, 0, 0, 0), second_rectangle=(0, 0, 0, 0)):
        """
        :param first_rectangle: First rectangle coordinates (pnt1 x, pnt1 y, pnt2 x, pnt2 y), type = Tuple 
        :param second_rectangle: Second  rectangle coordinates (pnt1 x, pnt1 y, pnt2 x, pnt2 y), type = Tuple
        :return: True on intersect or False, type = Boolean
        """
        return first_rectangle[0] < second_rectangle[2] and first_rectangle[2] > second_rectangle[0] and \
               first_rectangle[1] < second_rectangle[3] and first_rectangle[3] > second_rectangle[1]
