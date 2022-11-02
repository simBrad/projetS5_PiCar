import imp
import bpy
import numpy as np

#---------------------------------
obstacle_coll = bpy.data.collections.new('obstacle_coll')
layer_collection = bpy.context.view_layer.layer_collection
bpy.context.view_layer.active_layer_collection = layer_collection

obstacle_height = 15
obstacle_width = 10
obstacle_lenght = 10

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 100, obstacle_height/2),
    scale=(obstacle_width, obstacle_lenght, obstacle_height)
)

