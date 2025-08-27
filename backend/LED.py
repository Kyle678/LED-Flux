from backend.api.app import run_flask_with_controller
from backend.controller.controller import Controller

import time
import threading
import signal
import sys

shutdown_event = threading.Event()

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