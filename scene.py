from model import *

class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()

    def add_object(self, obj):
        self.objects.append(obj)

    def get_scene(self, scene_name):
        file_path = f'scenes/{scene_name}.txt'
        try:
            with open(file_path, 'r') as file:
                scene_code = file.read()
            # Define a local context with necessary variables
            local_context = {
                'self': self,
                'app': self.app,
                'add': self.add_object,
                'Cube': Cube,
                'ColoredCube': ColoredCube,
                'Duck': Duck,
                'MovingObj': MovingObj
            }
            # Execute the scene code in the given context
            exec(scene_code, globals(), local_context)
        except FileNotFoundError:
            print(f"The specified scene file '{file_path}' was not found.")
        except Exception as e:
            print(f"An error occurred while loading the scene: {e}")

        # Check if music_name is defined in the local context
        if 'music_name' in local_context:
            music_name = local_context['music_name']
            music_path = f'music/{music_name}.wav'
            self.app.play_music(music_path)
        else:
            # Use default music if no music_name defined in the scene file
            self.app.play_default_music()

    def load(self):
        app = self.app
        add = self.add_object
        # skybox
        self.skybox = AdvancedSkyBox(app)

        self.get_scene('scene_1')  # scene name

    def update(self):
        pass
