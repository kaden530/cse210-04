from game.casting.actor import Actor
import random
from game.shared.point import Point

class Artifact(Actor):
    """
    Rocks and Gems that fall 

    Attributes:
       _points
    """
    def __init__(self):
        super().__init__()
        self.artifact = ""
        self.select = 0
        self.worth = 0
        self._position = 0
        self.speed = 1
    
    def artifact_type(self):
        self.select = random.randint(1,2)
        if self.select == 1:
            self.artifact = "rock"
        else:
            self.artifact = "gem"
        return self.artifact

    def point_gen(self):
        if self.artifact == "gem":
            self.worth = random.randint(1,50)
        else:
            self.worth = random.randint(-50,-1)
        return self.worth
        
    def placement(self):
        self._position = random.randint(1,600)



    def get_points(self):
        """Gets the artifact's message.
        
        Returns:
            string: The message.
        """
        return self.worth
    
    def set_total(self, message):
        """Updates the message to the given one.
        
        Args:
            message (string): The given message.
        """
        self._points = self.worth + message
        super().points = self._points
        return message

    def get_velocity(self):
        """Gets the artifacts speed and direction.
        
        Returns:
            Point: The artifacts speed and direction.
        """
        return self._velocity
    
    def move_next(self, max_y):
        """Moves the actor to its next position according to its velocity. Will wrap the position 
        from one side of the screen to the other when it reaches the given maximum x and y values.
        
        Args:
            max_x (int): The maximum x value.
            max_y (int): The maximum y value.
        """
        x = self._position
        y = (self._velocity.get_y()) + self.speed
        self._position = Point(x, y)
