import pytest # pyright: ignore[reportMissingImports]
from backend.controller.controller import Controller

@pytest.mark.manual
@pytest.mark.visual
def test_visual_inspection():
    controller = Controller('config.ini')
    controller.fill((50, 50, 50))
    controller.show()

    input("Please visually inspect leds to ensure they are filled with color (50, 50, 50) and press Enter.")

    controller.off()