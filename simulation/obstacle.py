import bpy

obstacle_height = 15
obstacle_width = 10
obstacle_lenght = 10

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 115, obstacle_height/2),
    scale=(obstacle_width, obstacle_lenght, obstacle_height)
)

bpy.context.active_object.name = 'obstacle'

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(57.2724, 364.79, obstacle_height/2),
    scale=(obstacle_width, obstacle_lenght, obstacle_height)
)

bpy.context.active_object.name = 'obstacle2'