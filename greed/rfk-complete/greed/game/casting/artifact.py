from game.casting.actor import Actor
import random

class Artifact(Actor):
    """
    Rocks and Gems that fall 

    Attributes:
       _points
    """
    def __init__(self):
        super().__init__()
        self._points = 0
        self.artifact = ""
        self.select = 0
        self.worth = 0
    
    def artifact_type(self):
        self.select = random.int(1,2)
        if self.select == 1:
            self.artifact = "rock"
        else:
            self.artifact = "gem"

    def point_gen(self):
        if self.artifact == "rock":
            self.worth = random.int(1,50)
        else:
            self.worth = random.int(-1,-50)

    def get_message(self):
        """Gets the artifact's message.
        
        Returns:
            string: The message.
        """
        return self._points
    
    def set_message(self, points):
        """Updates the message to the given one.
        
        Args:
            message (string): The given message.
        """
        self._points = points