# backend/animations/animation_factory.py
import copy
import json

from .schemas import get_default_parameters
from .animations import StaticAnimation, RotateAnimation # Add other classes as you create them

class AnimationFactory:
    @staticmethod
    def create_animation(animation_record_from_db):
        """
        Creates an animation instance by merging database data with schema defaults.
        """
        anim_type = animation_record_from_db.get('type')
        length = animation_record_from_db.get('length')

        saved_parameters_raw = animation_record_from_db.get('parameters')
        
        saved_parameters = {}
        if isinstance(saved_parameters_raw, str):
            saved_parameters = json.loads(saved_parameters_raw)
        elif isinstance(saved_parameters_raw, dict):
            saved_parameters = saved_parameters_raw

        default_parameters = get_default_parameters(anim_type)
        if not default_parameters:
            raise ValueError(f"Unknown animation type: {anim_type}")

        final_parameters = copy.deepcopy(default_parameters)
        for key, value_obj in saved_parameters.items():
            if key in final_parameters:
                final_parameters[key]['value'] = value_obj.get('value')

        if anim_type == 'static':
            return StaticAnimation(length, final_parameters)
        elif anim_type == 'rotate':
            return RotateAnimation(length, final_parameters)
        else:
            raise ValueError(f"No class found for animation type: {anim_type}")