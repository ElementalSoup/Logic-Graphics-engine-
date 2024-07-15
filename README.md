# Logic-Graphics-engine-
its a graphics engine with customizable scenes

# Dependencies
•moderngl
•pygame
•glm
•numpy
•pywavefront

# scene building & framework
to quickly add a model without animation, you would use this:

add(Cube(app, pos=(0, 0, 0), scale=(1, 1, 1), rot=(0, 0, 0), tex_id=1))

pos is the position, scale is the scaling, rot is the rotation (degrees), and tex_id is the texture, which is usually a number or the name of the texture, here is a list of the textures:

0 = black and white checker tile
1 = wooden crate
2 = beij metal crate
3 = metal crate
4 = grey pixel edge block
5 = uh... meat
6 = dirt

named textures must have quotation marks around them in the code line, these textures are pretty much only for the models i personally added, and don't look very good when put on anything else
here is a list of those:

•duck = duck texture (for the duck)
•cola = cola texture (for the cola can)

i have added two models: duck and cola, these names can be in place of "cube" when making an object

ex:
add(Cola(app, pos=(0, 0, 0), scale=(1, 1, 1), rot=(0, 0, 0)))

# Animated Objects
to add an animated object, first you must define what it is (be sure to add "self." at the beginning):

self.moving_obj = MovingOBJ(app, tex_id, vao_name='cube')

vao_name is just defining which model to use, and "moving_obj" is just a name i chose for this example, you can use whatever name as long as you reference it exactly when adding keyframes
after defining it, you add keyframes, this is what that would look like:

self.moving_obj.add_keyframe(pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), interpolation='linear', easing='expo_in_out', duration=1)
self.moving_obj.add_keyframe(pos=(0, 10, 0), rot=(0, 0, 0), scale=(1, 1, 1), interpolation='linear', easing='expo_in_out', duration=1)

# object movement types
the orientation is the same, but as you can see there are some new unfamiliar parts to address,
interpolation is the way the object moves, the three types are:
•constant, the object changing instantly
•linear, the object changing at a consistent pace 
•exponential, the object changing with easing, which i personally find alot smoother

# easing types
only exponential uses the easy types, the easing types are:
•Expo_in, easing into the keyframe
•expo_out, easing out of the previous keyframe
•expo_in_out, easing out of the previous keyframe, and easing into the current one

the duration just defines how long it should take to reach that keyframe

# add the instance to the scene
the last thing to do is add it to the scene with the name you chose to define the animated object:

add(self.moving_obj)

# Example Scene

//Create a MovingCube instance
self.moving_cube = MovingObj(app, tex_id=1, vao_name='cube')
//Add multiple keyframes with different interpolation types
self.moving_cube.add_keyframe(pos=(0, 0, -10), rot=(0, 0, 0), scale=(1, 1, 1), interpolation='exponential', easing='expo_out', duration=1)
self.moving_cube.add_keyframe(pos=(0, 2, -10), rot=(0, 360, 0), scale=(1, 3, 1), interpolation='exponential', easing='expo_in_out', duration=1)
self.moving_cube.add_keyframe(pos=(0, 2, -10), rot=(0, 0, 0), scale=(3, 3, 3), interpolation='exponential', easing='expo_in_out', duration=1)
self.moving_cube.add_keyframe(pos=(0, 4, -10), rot=(0, 0, 0), scale=(1, 1, 1), interpolation='exponential', easing='expo_in_out', duration=1)
//Add the MovingCube instance to the scene
add(self.moving_cube)


# model types

•Cube
•Colored cube (be sure to add color when setting the orientation, instead of texture, use 0-1 rgb)
•MovingOBJ (for animation only, vao_name is the model type, remember that)
•Duck
•Cola

# Background Music
last but not least, if you want to add custom audio to your scene, that isn't the boss jazz i have set it to by default, add your audio file to the "music folder" (wav only), and add this line to your scene at the top:

music_name = "audio file name"
