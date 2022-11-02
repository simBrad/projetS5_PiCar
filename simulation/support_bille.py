from pickle import TRUE
import bpy
import numpy as np

def recurLayerCollection(layer_collection, collection_name):
    found = None
    if (layer_collection.name == collection_name):
        return layer_collection
    for layer in layer_collection.children:
        found = recurLayerCollection(layer, collection_name)
        if found:
            return found


# -----------------------------------------------------------------------------
support = bpy.data.collections.new('support')
bpy.context.scene.collection.children.link(support)
layer_collection = bpy.context.view_layer.layer_collection
sub_layer_collection = recurLayerCollection(layer_collection, 'support')
bpy.context.view_layer.active_layer_collection = sub_layer_collection

support_length = 0.05 * 5
support_width = 0.05 * 5
support_height = 0.005 * 5

sphere_radius = 140

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, support_height/2),
    scale=(support_width, support_length, support_height)
)

bpy.ops.mesh.primitive_uv_sphere_add(
    radius=1,
    location=(0, 0, sphere_radius + support_height-0.0015 * 5),
    scale=(sphere_radius, sphere_radius, sphere_radius)
)

bpy.ops.object.mode_set(mode = 'OBJECT')
obj = bpy.context.active_object
bpy.ops.object.mode_set(mode = 'EDIT') 
bpy.ops.mesh.select_mode(type="VERT")
bpy.ops.mesh.select_all(action = 'DESELECT')
bpy.ops.object.mode_set(mode = 'OBJECT')
obj.data.vertices[80].select = True
obj.data.vertices[65].select = True
obj.data.vertices[50].select = True
obj.data.vertices[35].select = True
obj.data.vertices[20].select = True
obj.data.vertices[481].select = True
obj.data.vertices[472].select = True
obj.data.vertices[457].select = True
obj.data.vertices[442].select = True
obj.data.vertices[427].select = True
obj.data.vertices[412].select = True
obj.data.vertices[397].select = True
obj.data.vertices[382].select = True
obj.data.vertices[367].select = True
obj.data.vertices[352].select = True
obj.data.vertices[337].select = True
obj.data.vertices[322].select = True
obj.data.vertices[306].select = True
obj.data.vertices[291].select = True
obj.data.vertices[276].select = True
obj.data.vertices[261].select = True
obj.data.vertices[246].select = True
obj.data.vertices[231].select = True
obj.data.vertices[216].select = True
obj.data.vertices[201].select = True
obj.data.vertices[186].select = True
obj.data.vertices[171].select = True
obj.data.vertices[156].select = True
obj.data.vertices[141].select = True
obj.data.vertices[126].select = True
obj.data.vertices[111].select = True
obj.data.vertices[96].select = True
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.transform.translate(value=(-0, -0, -0.561707 + -0.0817881), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False)
bpy.ops.object.mode_set(mode = 'OBJECT')

objects = bpy.data.objects

cube = objects['Cube.001']
sphere = objects['Sphere']

bool_one = cube.modifiers.new(type="BOOLEAN", name="bool 1")
bool_one.object = sphere
bool_one.operation = 'DIFFERENCE'



#------------------------------------------------------------------------------------------
bille = bpy.data.collections.new('bille')
layer_collection = bpy.context.view_layer.layer_collection
bpy.context.view_layer.active_layer_collection = layer_collection

marble_radius = 0.008 * 5

bpy.ops.mesh.primitive_uv_sphere_add(
    radius=1,
    location=(0, 0, support_height + marble_radius-0.0015 * 5 +0.01),
    scale=(marble_radius, marble_radius, marble_radius)
)

bpy.ops.rigidbody.object_add() 
bpy.context.object.rigid_body.collision_shape = 'SPHERE'
bpy.context.object.rigid_body.friction = 0
#------------------------------------------------------------------------------------------------
cube.select_set(True)
bpy.ops.object.convert(target='MESH')
bpy.ops.object.select_all(action='DESELECT')
sphere.select_set(True)
bpy.ops.object.delete()

bpy.context.view_layer.objects.active = cube
bpy.ops.rigidbody.object_add()
bpy.context.object.rigid_body.type = 'PASSIVE'
bpy.context.object.rigid_body.kinematic = True
bpy.context.object.rigid_body.collision_shape = 'MESH'
bpy.context.object.rigid_body.mesh_source = 'FINAL'
bpy.context.object.rigid_body.friction = 0
#-------------------------------------------------------------------------------------------------

