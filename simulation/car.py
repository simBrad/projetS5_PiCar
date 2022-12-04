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
car = bpy.data.collections.new('car_coll')
bpy.context.scene.collection.children.link(car)
layer_collection = bpy.context.view_layer.layer_collection
sub_layer_collection = recurLayerCollection(layer_collection, 'car_coll')
bpy.context.view_layer.active_layer_collection = sub_layer_collection

wheel_radius = 2
wheel_width = 0.5
car_length = 25
car_height = 2
car_width = 10

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, wheel_radius*2),
    scale=(car_width, car_length, car_height)
)

bpy.context.active_object.name = 'Body'

bpy.ops.mesh.primitive_cylinder_add(
        radius=wheel_radius+0.2,
        enter_editmode=False,
        location=(0,-car_length/4,wheel_radius-0.1),
        scale=(1,1,car_width+3),
        rotation=(0, 90*np.pi/180, 0),
)

objects = bpy.data.objects

cube = objects['Body']
cylinder1 = objects['Cylinder']

bool_one = cube.modifiers.new(type="BOOLEAN", name="bool 1")
bool_one.object = cylinder1
bool_one.operation = 'DIFFERENCE'


bpy.ops.mesh.primitive_cylinder_add(
        radius=wheel_radius+0.2,
        enter_editmode=False,
        location=(0,car_length/4,wheel_radius-0.1),
        scale=(1,1,car_width+3),
        rotation=(0, 90*np.pi/180, 0),
)

objects = bpy.data.objects
cylinder = objects['Cylinder.001']

bool_one = cube.modifiers.new(type="BOOLEAN", name="bool 1")
bool_one.object = cylinder
bool_one.operation = 'DIFFERENCE'

for i in range(0, 4):
    if (i < 2): back_wheel_distance = -car_length/4
    else: back_wheel_distance = car_length/4
    bpy.ops.mesh.primitive_cylinder_add(
        radius=wheel_radius,
        location=((-1)**i*(car_width/2), back_wheel_distance, wheel_radius),
        scale=(1, 1, wheel_width),
        rotation=(0, 90*np.pi/180, 0)
    )

for i in range (0,2):
    if i == 0:
        position = car_length/4
    elif i == 1:
        position = -car_length/4
    bpy.ops.mesh.primitive_cylinder_add(
        radius=1,
        location=(0, position, wheel_radius),
        scale=(0.3, 0.3, 6),
        rotation=(0, 90*np.pi/180, 0)
    )

# -----------------------------------------------------------------------------
pebble_cup_height = 5
pebble_cup_width = 5
pebble_cup_length = 5
pebble_radius = 1.5/2

sphere_extrusion_depth = 0.20
sphere_extrusion_radius = 14

bpy.ops.mesh.primitive_uv_sphere_add(
    radius=sphere_extrusion_radius,
    enter_editmode=False,
    align='WORLD',
    location=(0, pebble_cup_length/2, wheel_radius+car_height/2+pebble_cup_height+sphere_extrusion_radius-sphere_extrusion_depth),
    scale=(1, 1, 1)
)
bpy.context.active_object.name = 'sphere_extrusion'

bpy.ops.mesh.primitive_cube_add(
    size=1,
    enter_editmode=False,
    align='WORLD',
    location=(0, pebble_cup_length/2, wheel_radius+car_height/2+pebble_cup_height/2),
    scale=(pebble_cup_width, pebble_cup_length, pebble_cup_height)
)
bpy.context.active_object.name = 'pebble_cup'

# Make sphere_extrusion rigid
bpy.ops.rigidbody.object_add()
bpy.context.object.rigid_body.type = 'PASSIVE'
bpy.context.object.rigid_body.kinematic = True
bpy.context.object.rigid_body.collision_shape = 'MESH'
bpy.context.object.rigid_body.mesh_source = 'FINAL'
bpy.context.object.rigid_body.friction = 0.5

# Extrude the pebble_cub
bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["sphere_extrusion"]
bpy.ops.object.modifier_apply(modifier="Boolean")

# Delete the sphere_extrusion
bpy.ops.object.select_all(action='DESELECT')
bpy.data.objects['sphere_extrusion'].select_set(True)
bpy.ops.object.delete()

# -----------------------------------------------------------------------------


ultrasonic_sensor_width = 8
ultrasonic_sensor_height = 5
ultrasonic_sensor_length = 0.3
sensor_width = 0.1

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, car_length/4 + 5, wheel_radius*2 + 2.5),
    scale=(ultrasonic_sensor_width, ultrasonic_sensor_length, ultrasonic_sensor_height)
)

bpy.ops.mesh.primitive_cylinder_add(
    radius=1,
    location=(0, car_length/4 + 5.2, wheel_radius*2 + 2.5),
    scale=(1, 1, sensor_width),
    rotation=(90*np.pi/180, 0, 0)
)
bpy.context.active_object.name = 'distance_sensor'

# -----------------------------------------------------------------------------


line_sensor_height = 0.5
line_sensor_length = 5
line_sensor_width = 15

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, car_length/2, wheel_radius/2+wheel_radius),
    scale=(line_sensor_width, line_sensor_length, line_sensor_height),
)


# -----------------------------------------------------------------------------


for i in range(0, 5):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=1,
        location=((i-2)*line_sensor_width/5, car_length/2, wheel_radius/2+wheel_radius-0.3),
        scale=(1, 1, sensor_width),
        rotation=(0, 0, 0)
    )
    if i == 2:
        bpy.context.active_object.name = 'capteur_centrale'


#---------------------------------------------------------------------------------

cube.select_set(True)
bpy.ops.object.convert(target='MESH')
bpy.ops.object.select_all(action='DESELECT')
cylinder1.select_set(True)
cylinder.select_set(True)
bpy.ops.object.delete()

capteur_ligne_centre = objects['capteur_centrale']

bpy.context.scene.cursor.location = [capteur_ligne_centre.location.x, capteur_ligne_centre.location.y, capteur_ligne_centre.location.z]
for obj in car.all_objects:
    obj.select_set(True)
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
# car = bpy.data.collections['car_coll']
# bpy.context.view_layer.objects.active = bpy.data.objects["Cube"]
# for obj in car.all_objects:
#     obj.select_set(True)
# bpy.ops.object.join()