import pygame as pg
import moderngl as mgl

class Texture:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path='textures/face textures/texture_0.png')
        self.textures[1] = self.get_texture(path='textures/face textures/texture_1.jpg')
        self.textures[2] = self.get_texture(path='textures/face textures/texture_2.png')
        self.textures[3] = self.get_texture(path='textures/face textures/texture_3.png')
        self.textures[4] = self.get_texture(path='textures/face textures/texture_4.png')
        self.textures[5] = self.get_texture(path='textures/face textures/texture_5.jpg')
        self.textures[6] = self.get_texture(path='textures/face textures/dirt.png')
        # holy shit its a duck
        self.textures['duck'] = self.get_texture(path='objects/duck/bird.jpg')
        # snort coke, it'll give you ligma
        self.textures['cola'] = self.get_texture(path='objects/cola/Can.png')
        # gah, too bright
        self.textures['skybox'] = self.get_texture_cube(dir_path='textures/skybox_2/', ext='png')
        self.textures['depth_texture'] = self.get_depth_texture()

    def get_depth_texture(self):
        depth_texture = self.ctx.depth_texture(self.app.WIN_SIZE)
        depth_texture.repeat_x = False
        depth_texture.repeat_y = False
        return depth_texture

    def get_texture_cube(self, dir_path, ext='png'):
        faces = ['right', 'left', 'top', 'bottom'] + ['front', 'back'][::-1]
        textures = []
        for face in faces:
            texture = pg.image.load(dir_path + f'{face}.{ext}').convert()
            if face in ['right', 'left', 'front', 'back']:
                texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
            else:
                texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            textures.append(texture)

        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_data = pg.image.tostring(textures[i], 'RGB')
            texture_cube.write(face=i, data=texture_data)

        return texture_cube

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        texture.anisotropy = 32.0
        texture.filter = (mgl.TRIANGLES, mgl.TRIANGLES)
        return texture
    
    def get_color_texture(self, color=(255, 0, 0), size=(1, 1)):
        surface = pg.Surface(size)
        surface.fill(color)
        texture = self.ctx.texture(size=size, components=3, data=pg.image.tostring(surface, 'RGB'))
        texture.filter = (mgl.NEAREST, mgl.NEAREST)
        return texture

    def destroy(self):
        [tex.release() for tex in self.textures.values()]
