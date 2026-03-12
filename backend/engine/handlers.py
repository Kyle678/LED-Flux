from engine.animations.animation_registry import ANIMATION_CLASSES

def handle_brightness(controller, data):
    value = data.get('value', 0) 
    controller.set_brightness(value)

def handle_clear(controller, data):
    controller.clear()

def handle_animation(controller, data):
    anim_name = data.get('name')
    anim_class = ANIMATION_CLASSES.get(anim_name)
    
    if not anim_class:
        print(f"Unknown animation requested: {anim_name}")
        return
    
    animation = anim_class(**data)
    controller.add_animation(animation)

def handle_config(controller, data):
    # Placeholder for future configuration handling
    pass

def handle_get_status(controller):
    current_state = {
        "active": controller.is_active(),
        "power": controller.is_power(),
        "brightness": controller.brightness,
        "num_pixels": controller.num_pixels,
        "animations": [type(anim).__name__ for anim in controller.animations],
        "pixels": controller[:]
    }
    return current_state

def handle_power(controller, data):
    state = data.get('state', 'off')
    if state == 'on':
        controller.set_power(True)
    else:
        controller.set_power(False)
        controller.clear()

COMMAND_HANDLERS = {
    "brightness": handle_brightness,
    "clear": handle_clear,
    "animation": handle_animation,
    "config": handle_config,
    "power": handle_power,
    "get_status": handle_get_status
}