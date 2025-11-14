import pytest # pyright: ignore[reportMissingImports]
from backend.controller.controller import Controller
from backend.animations.animations import RotateAnimation
from backend.animations.animations import AnimationWrapper
from backend.animations.utils import generate_pixels

import time, threading

@pytest.mark.manual
@pytest.mark.visual
@pytest.mark.basic
def test_basic_visual_inspection():
    controller = Controller('config.ini')
    controller.fill((50, 0, 0))
    controller.show()

    input("Please visually inspect leds to ensure they are filled with color (50, 0, 0) and press Enter.")

    controller.fill((0, 50, 0))
    controller.show()

    input("Please visually inspect leds to ensure they are filled with color (0, 50, 0) and press Enter.")

    controller.fill((0, 0, 50))
    controller.show()

    input("Please visually inspect leds to ensure they are filled with color (0, 0, 50) and press Enter.")

    controller.fill((50, 50, 50))
    controller.show()

    input("Please visually inspect leds to ensure they are filled with color (50, 50, 50) and press Enter.")

    controller.fill((50, 0, 50))
    controller.show()

    input("Please visually inspect leds to ensure they are filled with color (50, 0s, 50) and press Enter.")

    controller.off()

@pytest.mark.manual
@pytest.mark.visual
def test_brightness_visual_inspection():
    print("Starting brightness visual inspection test...")
    controller = Controller('config.ini')
    controller.pixels.brightness = 1.0

    for i in range(0, 256, 5):
        controller.fill((i, 0, 0))
        controller.show()

    for i in range(255, -1, -5):
        controller.fill((i, 0, 0))
        controller.show()

    input("Please visually inspect leds to ensure they reach full brightness and then transition to off.")

    controller.off()

@pytest.mark.manual
@pytest.mark.visual
def test_neopixel_brightness_visual_inspection():
    print("Starting neopixel brightness visual inspection test...")
    controller = Controller('config.ini')

    step = 0.01
    for i in range(100):
        controller.pixels.brightness = i * step
        controller.fill((255, 0, 0))
        controller.show()

    for i in range(100, -1, -1):
        controller.pixels.brightness = i * step
        controller.fill((255, 0, 0))
        controller.show()

    input("Please visually inspect leds to ensure they reach full brightness and then transition to off.")

    controller.off()

@pytest.mark.manual
@pytest.mark.visual
@pytest.mark.current
def test_rotating_animation_visual_inspection():
    controller = Controller('config.ini')

    rotating_animation1 = RotateAnimation(length=300,
                                         parameters={'type': 'rotate',
                                                    'label': 'rotate-test',
                                                    'colors': [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    })

    rotating_animation_wrapper1 = AnimationWrapper(rotating_animation1, 300)

    rotating_animation_wrapper2 = AnimationWrapper(rotating_animation1, 0)

    controller.add_animation_wrapper(rotating_animation_wrapper1)
    controller.add_animation_wrapper(rotating_animation_wrapper2)

    while True:
        controller.update()
        controller.show()
        #print(controller.pixels[:10])  # Print first 10 pixels for debugging
        #time.sleep(0.05)

    input("Please visually inspect leds to ensure they are rotating through colors (50, 0, 0), (0, 50, 0), (0, 0, 50) and press Enter.")

    controller.stop_animation()
    controller.off()