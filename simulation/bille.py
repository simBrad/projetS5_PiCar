import bpy
import numpy as np

pebble_radius = 1.5/2

bpy.ops.mesh.primitive_uv_sphere_add(
    radius=pebble_radius,
    enter_editmode=False,
    align='WORLD',
    location=(0, 2.60028, 8.67546),
    scale=(1, 1, 1)
)
bpy.context.active_object.name = 'pebble'

#Appliquer RigidBody
bpy.ops.rigidbody.object_add()
bpy.context.object.rigid_body.friction = 0.5
bpy.context.object.rigid_body.mesh_source = 'FINAL'