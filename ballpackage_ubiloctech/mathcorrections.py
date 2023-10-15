import math

# Convert degrees to radians
def convertDegtoRad(deg:float) -> float:
    return (deg * math.pi / 180)

# Convert radians to degrees
def convertRadtoDeg(rad:float) -> float:
    return(rad * 180 / math.pi)

# Convert angle to between 0 and 360
def correctedAngle(angle) -> int:
    lAngle = angle
    while lAngle < 0:
        lAngle += 360
    
    while lAngle > 360:
        lAngle -= 360

    return round(lAngle)

# Quad Solutions
# Returns only real solutions
def QuadSolution(a, b, c) -> ():
    discriminant = b ** 2 - 4 * a * c

    if discriminant < 0:
        return(0, 0)
    else:
        r1 = (-b + math.sqrt(discriminant)) / (2 * a)
        r2 = -(b + math.sqrt(discriminant)) / (2 * a)
    return (r1, r2)