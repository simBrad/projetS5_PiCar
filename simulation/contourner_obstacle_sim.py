import bpy
import numpy as np

bpy.ops.object.select_all(action='DESELECT')

car = bpy.data.collections['car_coll']
bpy.context.view_layer.objects.active = bpy.data.objects["Cube"]
for obj in car.all_objects:
    obj.select_set(True)
bpy.ops.object.join()

nbFrames = 600
bpy.context.scene.frame_end = nbFrames
car = bpy.data.objects["Cube"]
obstacle = bpy.data.objects['Cube.004']

posInit = {car : car.location.y} 

def avancer():
    i = 0
    j = 0
    while obstacle.location.y-car.location.y  > 60:
        bpy.context.scene.frame_set(i) 
        car.location[1] =  posInit.get(car)+1/2 * 0.71 * (i/24)**2
        bpy.ops.anim.keyframe_insert(type='LocRotScale')
        i += 1
    tourner(i, 50, -0.3490658504)
    k = i
    #while obstacle.location.y-car.location.y > 0:
    for x in range(k, k+125):
        bpy.context.scene.frame_set(i) 
        car.location[1] =  posInit.get(car)+1/2 * 0.71 * (i/24)**2
        car.location[0] =  posInit.get(car)+1/2 * 1 * (j/24)**2
        bpy.ops.anim.keyframe_insert(type='LocRotScale')
        j  += 1
        i += 1
    tourner(i, 50, 0.3490658504 * 2)
    posX = car.location.x
    j = 0
    while car.location.x-obstacle.location.x  > 0: 
        bpy.context.scene.frame_set(i) 
        car.location[1] =  posInit.get(car)+1/2 * 0.71 * (i/24)**2
        car.location[0] =  posX-1/2 * 1 * (j/24)**2
        bpy.ops.anim.keyframe_insert(type='LocRotScale')
        j += 1
        i += 1
    tourner(i, 20, -0.3490658504)

def tourner(i, nbrFrame, angle):
    for x in  range(nbrFrame): 
        bpy.context.scene.frame_set(i) 
        car.rotation_euler[2] = car.rotation_euler[2]+angle/(nbrFrame)
        bpy.ops.anim.keyframe_insert(type='LocRotScale')
        i += 1


avancer()


bpy.ops.screen.animation_play()
