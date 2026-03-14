from engine.animations.animations import RotatingAnimation

from engine.controller import Controller

import time

def main():
    controller = Controller(num_pixels=1500, brightness=0.2, pin=18)
    animation = RotatingAnimation(num_pixels=1500, loop_duration=10, colors=[[255, 0, 0], [0, 0, 255], [255, 0, 0]], start_index=100)

    while True:
        if animation.ready_to_update():
            animation.update()
            controller[:] = animation.render_frame()
            controller.show()

if __name__ == '__main__':
    main()