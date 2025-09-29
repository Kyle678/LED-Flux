import copy

BASE_PARAMETERS = {
    "label": {
        "label": "Animation Name",
        "type": "text",
        "value": "New Animation"
    },
    "colors": {
        "label": "Colors",
        "type": "color-list",
        "value": [(30, 0, 0), (0, 30, 0), (0, 0, 30)]
    },
    "gradient": {
        "label": "Gradient",
        "type": "boolean",
        "value": True
    },
    "wrap": {
        "label": "Wrap",
        "type": "boolean",
        "value": True
    },
    "step": {
        "label": "Step",
        "type": "integer",
        "value": 0,
        "min": 0,
        "max": -1,
        "step": 1
    },
    "brightness": {
        "label": "Brightness",
        "type": "float",
        "value": 1.0,
        "min": 0.0,
        "max": 1.0,
        "step": 0.01,
    }
}

BASE_MOVEMENT_PARAMETERS = {
    "speed": {
        "label": "Speed",
        "type": "integer",
        "value": 1000,
        "min": 0,
        "max": 5000,
        "step": 10
    },
    "syncronous": {
        "label": "Syncronous",
        "type": "boolean",
        "value": False
    },
    "repeat_interval": {
        "label": "Repeat Interval (Seconds)",
        "type": "integer",
        "value": 10,
        "min": 1,
        "max": 3600,
        "step": 1
    }
}

ANIMATION_SCHEMAS = {
    "static": {
        "name": "Static",
        "parameters": {**BASE_PARAMETERS}
    },
    "rotate": {
        "name": "Rotate",
        "parameters": {**BASE_PARAMETERS,
                       **BASE_MOVEMENT_PARAMETERS
        }
    }
}

def get_default_parameters(animation_type):
    schema = ANIMATION_SCHEMAS.get(animation_type)
    if not schema:
        return None
    return copy.deepcopy(schema["parameters"])