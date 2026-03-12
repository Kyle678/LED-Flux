

class LEDConfig:
    def __init__(self, name):
        self.name = name
        self.animations = []

    def add_animation(self, animation):
        self.animations.append(animation)

    def get_animations(self):
        return self.animations
    
    def clear_animations(self):
        self.animations = []

    def update_animation(self, animation):
        for c_animation in self.animations:
            if animation == c_animation:
                c_animation.update()

    def update(self):
        for animation in self.animations:
            animation.update()
