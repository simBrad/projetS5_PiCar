import bpy;
from bpy import context as C; 
from bpy import data as D; 

print("Hello Blender")

bpy.ops.mesh.primitive_cube_add()
#bpy.ops.mesh.primitive_monkey_add() 
ob = bpy.context.active_object 
bpy.ops.object.shade_smooth() 


rotations = [0, 6.28319] # En radian = 360 degrees
frames = [1, 250] 
moveX = [0, 5] 
moveY = [0, 2] 
moveZ = [0, 5]

for i in range(len(rotations)): 
	rotation = rotations[i] 
	frame = frames[i]
	mvX = moveX[i]
	mvY = moveY[i]
	bpy.context.scene.frame_set(frame) 
	ob.rotation_euler[2] = rotation 
	ob.location[0] = mvX
	ob.location[1] = mvY

	bpy.ops.anim.keyframe_insert(type='LocRotScale') 
	
bpy.ops.screen.animation_play()
