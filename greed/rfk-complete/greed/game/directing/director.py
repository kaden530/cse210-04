from ..casting.artifact import Artifact
from game.shared.point import Point
from game.shared.color import Color
import random
import __main__


class Director:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
    """

    def __init__(self, keyboard_service, video_service):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        self._total_points = 0
        self._current_score = 0

    def start_game(self, cast):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.open_window()
        while self._video_service.is_window_open():
            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)
        self._video_service.close_window()

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the robot.
        
        Args:
            cast (Cast): The cast of actors.
        """
        robot = cast.get_first_actor("robots")
        velocity = self._keyboard_service.get_direction()
        robot.set_velocity(velocity)

    def _do_updates(self, cast):
        """Updates the robot's position and resolves any collisions with artifacts.  Also recreates artifacts when the
        robot collides with one
        
        Args:
            cast (Cast): The cast of actors.
        """
        banner = cast.get_first_actor("banners")
        robot = cast.get_first_actor("robots")
        artifacts = cast.get_actors("artifacts")

        banner.set_text(f"Total: {self._total_points} Last: {self._current_score}   ")
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        robot.move_next(max_x, max_y)

        artifacts_removed = 0
        # loop through artifacts to display on screen and show the score
        for artifact in artifacts:
            artifact.move_next(max_y)
            if robot.get_position().equals(artifact.get_position()):
                self._current_score = artifact.get_points()
                self._total_points = robot.set_total(self._current_score)
                banner.set_text(f"Total: {self._total_points} last: {self._current_score}")
                cast.remove_actor("artifacts", artifact)
                artifacts_removed +=1
        # recreate the artifacts for the amount that was removed
        for i in range(artifacts_removed):
            artifact = Artifact()
            COLS = 60
            ROWS = 40
            CELL_SIZE = 15
            FONT_SIZE = 15
            symbol = artifact.artifact_type()
            if symbol in "rock":
                text = "o"
            else:
                text = "*"

            x = random.randint(1, COLS - 1)
            y = random.randint(1, ROWS - 1)
            position = Point(x, y)
            position = position.scale(CELL_SIZE)

            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            color = Color(r, g, b)

            artifact.set_text(text)
            artifact.set_font_size(FONT_SIZE)
            artifact.set_color(color)
            artifact.set_position(position)
            artifact.point_gen()
            cast.add_actor("artifacts", artifact)

    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()
