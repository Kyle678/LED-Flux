from backend.api.app import run_flask_with_controller
from backend.controller.controller import Controller

import time
import threading
import signal
import sys

shutdown_event = threading.Event()

def getGradientColors(start_color, end_color, steps):
    gradient_colors = []
    for i in range(steps):
        ratio = i / (steps - 1)
        r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        gradient_colors.append((r, g, b))
    return gradient_colors

def getGradient(colorList, steps):
    gradient_colors = []
    num_colors = len(colorList)
    if num_colors < 2:
        return gradient_colors

    steps_per_segment = steps // (num_colors - 1)
    for i in range(num_colors - 1):
        start_color = colorList[i]
        end_color = colorList[i + 1]
        segment_colors = getGradientColors(start_color, end_color, steps_per_segment)
        gradient_colors.extend(segment_colors)

    while len(gradient_colors) < steps:
        gradient_colors.append(colorList[-1])

    return gradient_colors[:steps]

def rotate_list(lst, n):
    n = n % len(lst)
    return lst[-n:] + lst[:-n]

def main():
    print("Starting LED-Flux...")
    controller = Controller('config.ini')

    led_thread = threading.Thread(target= controller.loop, daemon=True)
    flask_thread = threading.Thread(target=run_flask_with_controller,
                                    args=(controller, "ledflux.db", controller.getFlaskHost(), controller.getFlaskPort()), 
                                    daemon=True)

    led_thread.start()
    flask_thread.start()

    # Handle CTRL+C nicely
    def handle_sigint(sig, frame):
        print("\nShutting down...")
        shutdown_event.set()
        # tell controller to stop if it supports it
        if hasattr(controller, "stop"):
            controller.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_sigint)

    while True:
        choice = input("Press 'q' to quit: ")
        if choice.lower() == 'q':
            controller.off()
            handle_sigint(None, None)
            break
        elif choice.lower() == 'on':
            controller.fill((50, 50, 50))
            controller.show()
        elif choice.lower() == 'off':
            controller.off()

    led_thread.join()
    flask_thread.join()

if __name__ == "__main__":
    main()