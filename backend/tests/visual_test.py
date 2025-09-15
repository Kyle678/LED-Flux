import pytest # pyright: ignore[reportMissingImports]
from backend.controller.controller import Controller
from backend.animations.animations import RotateAnimation, LightningAnimation
from backend.animations.animations import AnimationWrapper
from backend.animations.utils import generate_pixels

import time, threading

@pytest.mark.manual
@pytest.mark.visual
#@pytest.mark.basic
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

    input("Please visually inspect leds to ensure they are filled with color (50, 50, 50) and press Enter.")

    controller.off()

@pytest.mark.manual
@pytest.mark.visual
@pytest.mark.basic
def test_rainbow_visual_inspection():
    controller = Controller('config.ini')

    rainbow_animation = RotateAnimation(length=300,
                                       type_='rainbow',
                                       params={'step': 1,
                                               'colors': [(50, 0, 0), (0, 50, 0), (0, 0, 50)],
                                               'gradient': True,
                                               'wrap': True,
                                               'speed': 50
    })

    ra1 = AnimationWrapper(rainbow_animation, 0)
    ra2 = AnimationWrapper(rainbow_animation, 300)
    ra3 = AnimationWrapper(rainbow_animation, 600)
    ra4 = AnimationWrapper(rainbow_animation, 900)
    ra5 = AnimationWrapper(rainbow_animation, 1200)

    controller.add_animation_wrappers([ra1, ra2, ra3, ra4, ra5])

    controller.loop()

    input("Please visually inspect leds to ensure they are showing a rainbow effect and press Enter.")

@pytest.mark.manual
@pytest.mark.visual
def test_lightning_visual_inspection():
    controller = Controller('config.ini')

    lightning_animation = LightningAnimation(length=300)

    lightning_animation_wrapper = AnimationWrapper(lightning_animation, 0)

    controller.add_animation_wrapper(lightning_animation_wrapper)

    while True:
        controller.update()
        controller.show()

    input("Please visually inspect leds to ensure they are showing a lightning effect and press Enter.")

@pytest.mark.manual
@pytest.mark.visual
def test_color_setup_visual_inspection():
    controller = Controller('config.ini')

    pixels = generate_pixels(300, colors=[(50, 0, 0), (0, 50, 0), (0, 0, 50)], gradient=True, loop=False)
    controller[:300] = pixels
    controller.show()

    input("Please visually inspect leds to ensure they show a gradient from (50, 0, 0) to (0, 50, 0) to (0, 0, 50) and press Enter.")

    controller.off()

@pytest.mark.manual
@pytest.mark.visual
def test_brightness_visual_inspection():
    print("Starting brightness visual inspection test...")
    controller = Controller('config.ini')
    controller.pixels.brightness = 1.0

    for i in range(256):
        print(i)
        controller.fill((i, 0, 0))
        controller.show()

    for i in range(255, -1, -1):
        print(i)
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
        print(i)
        controller.pixels.brightness = i * step
        controller.fill((255, 0, 0))
        controller.show()

    for i in range(100, -1, -1):
        print(i)
        controller.pixels.brightness = i * step
        controller.fill((255, 0, 0))
        controller.show()

    input("Please visually inspect leds to ensure they reach full brightness and then transition to off.")

    controller.off()

@pytest.mark.manual
@pytest.mark.visual
def test_rotating_animation_visual_inspection():
    controller = Controller('config.ini')

    rotating_animation1 = RotateAnimation(length=300,
                                         type_='rotate',
                                         params={'colors': [(50, 0, 0), (0, 50, 0), (0, 0, 50)],
                                                'gradient': True,
                                                'loop': True
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