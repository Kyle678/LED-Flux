from backend.animations.schemas import get_default_parameters
from backend.animations.animations import *
import copy

class AnimationFactory:
    def create_animation(self, animation_record_from_db):
        """
        Creates an animation instance by mergin database data with schema defaults.
        """

        anim_type = animation_record_from_db['type']

        default_params = get_default_parameters(anim_type)

        saved_params = animation_record_from_db['parameters']

        final_params = copy.deepcopy(default_params)

        for key, value_obj in saved_params.items():
            if key in final_params:
                final_params[key] = value_obj['value']

        length = animation_record_from_db['length']

        if anim_type == 'static':
            return StaticAnimation(length, final_params)
        elif anim_type == 'rotate':
            return RotateAnimation(length, final_params)
        else:
            raise ValueError(f"Unknown animation type: {anim_type}")