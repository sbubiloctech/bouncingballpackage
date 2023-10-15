
# Random Factor bouncing ball exception class to ensure that random bounces are not too high
class RandomFactorException (Exception):
    statusCode = None
    message = None

    def __init__(self, *args: object) -> None:
        self.statusCode = 1
        self.message = "Random Factor should be between 0 and 1 only"
        super().__init__(self.message)

# Random Theta exception to ensure that all angles in degrees are between 0 and 360 only
class ThetaException (Exception):
    statusCode = None
    message = None
    angle = None

    def __init__(self, *args: object) -> None:
        super().__init__(f'Angle is not between 0 and 360. Please either handle this exception or correct the angle')
        self.statusCode = 2
        self.angle = args[0]
        self.message = f'Angle is not between 0 and 360. Please either handle this exception or correct the angle'

# Random Velocity Exception to ensure that velocity is never too high (10% or less that total screen size)
class VelocityException (Exception):
    statusCode = None
    message = None
    velocity = None

    def __init__(self, *args: object) -> None:
        self.velocity = args[0]
        if self.velocity <= 1:
            self.message = f'Velocity cannot less than 1 or negative'
        else:
            self.message = f'Velocity is too high for current grid size'
        super().__init__(self.message)

# Resolution Exception to ensure that resolution is not too high for given screen resolution
class ResolutionException (Exception):
    def __init__(self, *args: object) -> None:
        message = 'Required resolutions (number of x or y partitions) is too high. Please reduce these.'
        super().__init__(message)
