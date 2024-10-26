import math

VERSION = "0.1.0"
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        
class LinearModel:
    def __init__(self, byx: float, alfa: float, correlation: float):
        self.byx = byx
        self.alfa = alfa
        self.correlation = correlation

def TransformData(data: list[list]):
    points : list[Point] = []
    for d in data:
        if len(d) == 2:
            if d[0] is not None and d[1] is not None:
                points.append(Point(float(d[0]), float(d[1])))
    new_points = []
    skip = 0
    for i in range(0, len(points)):
        if skip > 0:
            skip -= 1
        else:
            if i < len(points) - 2:
                if points[i].x == points[i+1].x and points[i].x == points[i+2].x:
                    new_points.append(points[i+1])
                    skip = 2
                else:
                    new_points.append(points[i])
            else:
                new_points.append(points[i])
    return new_points

def PointsMean(points: list[Point]):
    if len(points) < 1:
        return Point(0, 0)
    sum_x = 0.0
    sum_y = 0.0
    for p in points:
        sum_x += p.x
        sum_y += p.y
    return Point(sum_x / len(points) * 1.0, sum_y / len(points) * 1.0)

def VarianceX(points: list[Point], mean: Point):
    sx2 = 0.0
    for p in points:
        sx2 += (p.x - mean.x) * (p.x - mean.x)
    return sx2 / (len(points) - 1.0)

def VarianceY(points: list[Point], mean: Point):
    sy2 = 0.0
    for p in points:
        sy2 += (p.y - mean.y) * (p.y - mean.y)
    return sy2 / (len(points) - 1.0)

def CoVariance(points: list[Point], mean: Point):
    sxy = 0.0
    for p in points:
        sxy += ((p.x - mean.x) * (p.y - mean.y))
    return sxy / (len(points) - 1.0)

def LinearRegression(data: list[list]):
    points = TransformData(data)
    if len(points) < 2:
        return None
    mean = PointsMean(points)
    corr = CoVariance(points, mean) / math.sqrt(VarianceX(points, mean) * VarianceY(points, mean))
    byx = CoVariance(points, mean) / VarianceX(points, mean)
    alfa = mean.y - byx * mean.x
    return LinearModel(byx, alfa, corr)