from sys import stderr
from time import time


class FrameCounter:
    """Creates a main loop and ensures that the framerate is static"""

    def __init__(self, canvas, target_fps):
        """Initialise the frame counter

        :param canvas: The canvas which to call after on
        :param target_fps: The fps to aim to achieve
        """
        self.canvas = canvas
        self.fps = target_fps
        self.frame_time = 1 / target_fps
        self.last_frame = time()

        self.current_fps = 1

    def next_frame(self, callback):
        """Calculate when the next frame should be called

        :param callback: function to call for the next frame
        """
        t = time()
        ft = t - self.last_frame

        delay = 0

        if ft > self.frame_time:
            if ft - self.frame_time > self.frame_time / 5:
                print(
                    f"Help! Running {ft - self.frame_time} seconds behind!",
                    file=stderr)
        else:
            delay = self.frame_time - ft

        self.canvas.after(int(delay*1000), callback)
        self.current_fps = 1 / (delay+ft)
        self.last_frame = t
