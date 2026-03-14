from engine.animations.animations import RotatingAnimation

from engine.controller import Controller

import time

def main():
    controller = Controller(num_pixels=200, brightness=0.2, pin=18)
    animation = RotatingAnimation(num_pixels=10, loop_duration=2, colors=[[255, 0, 0], [0, 0, 255], [255, 0, 0]], start_index=100)
    print(animation.get_pixels())
    controller.animations.append(animation)
    for _ in range(1):
        time.sleep(0.1)
        animation.update()
        print(animation.get_pixels())
        controller[100:110] = animation.get_pixels()[:]
        controller.show()
    return
    while True:
        controller[100:110] = animation.get_pixels()[:]
        print(controller[100:110], animation.get_delta_time(), animation.pixel_to_time_ratio())
        animation.update()
        controller.show()

if __name__ == '__main__':
    main()