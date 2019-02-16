import time

import anki_vector
from PIL import Image, ImageDraw
from anki_vector.screen import convert_image_to_screen_data, dimensions
from anki_vector.util import parse_command_args

width, height = dimensions()


class Robot(object):
    def __init__(self):
        args = parse_command_args()
        self.robot = anki_vector.AsyncRobot(
            args.serial,
            default_logging=False,
        )
        self.robot.connect(self.robot.behavior_activation_timeout)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.robot.disconnect()

    def display(self, text, timeout: float):
        img = Image.new('RGB', (width, height), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)
        w, h = draw.textsize(text)
        draw.text(((width - w) / 2, (height - h) / 2), text, fill=(255, 255, 0))
        screen_data = convert_image_to_screen_data(img)
        # https://www.kinvert.com/anki-vector-screen-convert_image_to_screen_data/
        # there are some bug so i have to display twice to fix it
        self.robot.screen.set_screen_with_image_data(screen_data, 0.1)
        self.robot.screen.set_screen_with_image_data(screen_data, timeout)


if __name__ == '__main__':
    robot = Robot()
    robot.display('Hello, world', 3)
    time.sleep(3)
