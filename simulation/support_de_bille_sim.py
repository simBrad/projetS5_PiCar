import bpy

nbFrames = 200

objects = bpy.data.objects

support = objects['Cube.001']
marble = objects['Sphere.001']

support.animation_data_clear()
marble.animation_data_clear()

bpy.context.scene.frame_end = nbFrames
j = 0
for i in range(0, 100):
        if i < 50:
            support.location[1] =  1/2 * 0.68 * (i/24)**2
        else:
            support.location[1] =  support.location[1] + 0.05
        support.keyframe_insert(data_path="location", frame = i)

# for i in range (100, 200):
#         support.location[1] =  1/2 * 0.6 * (i/24)**2
#         support.location[0] =  1/2 * 0.4 * (j/24)**2
#         support.keyframe_insert(data_path="location", frame = i)
#         j += 1
bpy.ops.screen.animation_play()
