import bpy

nbFrames = 1000

bpy.ops.object.select_all(action='DESELECT')

car = bpy.data.collections['car_coll']
bpy.context.view_layer.objects.active = bpy.data.objects["Cube"]
for obj in car.all_objects:
    obj.select_set(True)
bpy.ops.object.join()


bpy.context.scene.frame_end = nbFrames

car = bpy.data.objects["Cube"]
obstacle = bpy.data.objects['Cube.004']

posInit = {car : car.location.y} 
for i in range(0, nbFrames):
        bpy.context.scene.frame_set(i) 
        car.location[1] =  posInit.get(car)+1/2 * 0.71 * (i/24)**2
        bpy.ops.anim.keyframe_insert(type='LocRotScale')
        if obstacle.location.y-car.location.y < 60:
            k = i
            for j in range(0, 300):
                car.location[1] = car.location.y - 1/2 * 0.71 * (k/24)**2
                bpy.ops.anim.keyframe_insert(type='LocRotScale')
                i += 1
            break
    
bpy.ops.screen.animation_play()