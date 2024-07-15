import moderngl as mgl
import numpy as np
import glm
import math


class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        self.app = app
        self.pos = pos
        self.vao_name = vao_name
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    def update(self): ...

    def get_model_matrix(self):
        m_model = glm.mat4()
        # translate
        m_model = glm.translate(m_model, self.pos)
        # rotate
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        # scale
        m_model = glm.scale(m_model, self.scale)
        return m_model

    def render(self):
        self.update()
        self.vao.render()

class ExtendedBaseModel(BaseModel):
    def __init__(self, app, vao_name, tex_id, pos, rot, scale, texture=None):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.texture = texture or self.app.mesh.texture.textures[self.tex_id]
        self.on_init()

    def update(self):
        self.texture.use(location=0)
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def update_shadow(self):
        self.shadow_program['m_model'].write(self.m_model)

    def render_shadow(self):
        self.update_shadow()
        self.shadow_vao.render()

    def on_init(self):
        self.program['m_view_light'].write(self.app.light.m_view_light)
        # resolution
        self.program['u_resolution'].write(glm.vec2(self.app.WIN_SIZE))
        # depth texture
        self.depth_texture = self.app.mesh.texture.textures['depth_texture']
        self.program['shadowMap'] = 1
        self.depth_texture.use(location=1)
        # shadow
        self.shadow_vao = self.app.mesh.vao.vaos['shadow_' + self.vao_name]
        self.shadow_program = self.shadow_vao.program
        self.shadow_program['m_proj'].write(self.camera.m_proj)
        self.shadow_program['m_view_light'].write(self.app.light.m_view_light)
        self.shadow_program['m_model'].write(self.m_model)
        # texture
        self.program['u_texture_0'] = 0
        self.texture.use(location=0)
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        # light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)


class Cube(ExtendedBaseModel):
    def __init__(self, app, vao_name='cube', tex_id=0, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

class ColoredCube(ExtendedBaseModel):
    def __init__(self, app, vao_name='cube', pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), color=(1, 0, 0)):
        # Convert color to 0-255 range and create a solid color texture
        color = tuple(int(255 * c) for c in color)
        color_tex = app.mesh.texture.get_color_texture(color)
        # Initialize with the generated color texture
        super().__init__(app, vao_name, tex_id=None, pos=pos, rot=rot, scale=scale, texture=color_tex)
        self.color_tex = color_tex
        self.color = color

    def update(self):
        self.m_model = self.get_model_matrix()
        super().update()

def ease_in_expo(t):
    return 2 ** (10 * (t - 1))

def ease_out_expo(t):
    return 1 - 2 ** (-10 * t)

def ease_in_out_expo(t):
    if t < 0.5:
        return 0.5 * 2 ** (10 * (2 * t - 1))
    else:
        return 1 - 0.5 * 2 ** (-10 * (2 * t - 1))

class MovingObj(ExtendedBaseModel):
    def __init__(self, app, vao_name='cube',pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), tex_id=0):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.keyframes = []
        self.current_keyframe_index = 0
        self.time_since_last_keyframe = 0.0  # Track time within current keyframe

    def add_keyframe(self, pos, rot, scale=(1, 1, 1), interpolation='linear', duration=1.0, easing=None):
        duration = duration * 1000
        if rot is not None:
            rot = tuple(math.radians(angle) for angle in rot)
        if scale is not None:
            self.keyframes.append({
                'pos': pos,
                'rot': rot,
                'scale': scale,
                'interpolation': interpolation,
                'duration': duration,
                'easing': easing
            })

    def update(self):
        if self.keyframes:
            # Determine current and next keyframe indices
            idx1 = self.current_keyframe_index
            idx2 = (idx1 + 1) % len(self.keyframes)

            # Total duration of current keyframe
            keyframe_duration = self.keyframes[idx1]['duration']

            # Calculate time within current keyframe
            self.time_since_last_keyframe += self.app.dtime
            t = min(self.time_since_last_keyframe / keyframe_duration, 1.0)

            # Interpolate position
            pos1 = self.keyframes[idx1]['pos']
            pos2 = self.keyframes[idx2]['pos']
            pos = self.interpolate(pos1, pos2, t, self.keyframes[idx1]['interpolation'], self.keyframes[idx1]['easing'])

            # Interpolate rotation
            rot1 = self.keyframes[idx1]['rot']
            rot2 = self.keyframes[idx2]['rot']
            rot = self.interpolate(rot1, rot2, t, self.keyframes[idx1]['interpolation'], self.keyframes[idx1]['easing'])

            # Interpolate scale
            scale1 = self.keyframes[idx1]['scale']
            scale2 = self.keyframes[idx2]['scale']
            scale = self.interpolate(scale1, scale2, t, self.keyframes[idx1]['interpolation'], self.keyframes[idx1]['easing'])

            # Update position, rotation, and scale
            self.pos = pos
            self.rot.xyz = rot
            self.scale = scale

            # Update model matrix
            self.m_model = self.get_model_matrix()

            # Check if we need to move to the next keyframe
            if t >= 1.0:
                self.current_keyframe_index = (self.current_keyframe_index + 1) % len(self.keyframes)
                self.time_since_last_keyframe = 0.0  # Reset time within current keyframe

        super().update()

    def interpolate(self, start, end, t, interpolation_type, easing=None):
        if interpolation_type == 'linear':
            return tuple((1 - t) * s + t * e for s, e in zip(start, end))
        elif interpolation_type == 'constant':
            return start  # No interpolation, hold at start keyframe
        elif interpolation_type == 'exponential':
            if easing == 'expo_in':
                return tuple((1 - ease_in_expo(t)) * s + ease_in_expo(t) * e for s, e in zip(start, end))
            elif easing == 'expo_out':
                return tuple((1 - ease_out_expo(t)) * s + ease_out_expo(t) * e for s, e in zip(start, end))
            elif easing == 'expo_in_out':
                return tuple((1 - ease_in_out_expo(t)) * s + ease_in_out_expo(t) * e for s, e in zip(start, end))
            else:
                raise ValueError(f"Unknown easing function: {easing}")
        else:
            raise ValueError(f"Unknown interpolation type: {interpolation_type}")


class Duck(ExtendedBaseModel):
    def __init__(self, app, vao_name='duck', tex_id='duck',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

class Cola(ExtendedBaseModel):
    def __init__(self, app, vao_name='cola', tex_id='cola',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)


class SkyBox(BaseModel):
    def __init__(self, app, vao_name='skybox', tex_id='skybox',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))


class AdvancedSkyBox(BaseModel):
    def __init__(self, app, vao_name='advanced_skybox', tex_id='skybox',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        m_view = glm.mat4(glm.mat3(self.camera.m_view))
        self.program['m_invProjView'].write(glm.inverse(self.camera.m_proj * m_view))

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)