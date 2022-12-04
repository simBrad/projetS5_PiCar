import bpy

car = bpy.data.collections['car_coll']


posInitY = {} 
posInitX = {} 

nbFrames = 2500

bpy.ops.object.select_all(action='DESELECT')


bpy.context.scene.frame_end = nbFrames


objects = bpy.data.objects
capteur_ligne_centre = objects['capteur_centrale']
circuit = objects['Circle.002']
obstacle = objects['obstacle']
obstacle2 = objects['obstacle2']
capteur_distance = objects['distance_sensor']
bpy.context.scene.gravity[2] = -9.8

v2 = circuit.data.vertices[15]
v3 = circuit.data.vertices[16]
v4 = circuit.data.vertices[12]
v5 = circuit.data.vertices[13]
v6 = circuit.data.vertices[9]

v7 = circuit.data.vertices[203]
v8 = circuit.data.vertices[202]
v9 = circuit.data.vertices[206]
v10 = circuit.data.vertices[205]
v11 = circuit.data.vertices[209]

v12 = circuit.data.vertices[241]
v13 = circuit.data.vertices[240]
v14 = circuit.data.vertices[244]
v15 = circuit.data.vertices[243]
v16 = circuit.data.vertices[247]
v17 = circuit.data.vertices[245]
v18 = circuit.data.vertices[248]

co_v2 = circuit.matrix_world @ v2.co
co_v3 = circuit.matrix_world @ v3.co
co_v4 = circuit.matrix_world @ v4.co
co_v5 = circuit.matrix_world @ v5.co
co_v6 = circuit.matrix_world @ v6.co

co_v7 = circuit.matrix_world @ v7.co
co_v8 = circuit.matrix_world @ v8.co
co_v9 = circuit.matrix_world @ v9.co
co_v10 = circuit.matrix_world @ v10.co
co_v11 = circuit.matrix_world @ v11.co

co_v12 = circuit.matrix_world @ v12.co
co_v13 = circuit.matrix_world @ v13.co
co_v14 = circuit.matrix_world @ v14.co
co_v15 = circuit.matrix_world @ v15.co
co_v16 = circuit.matrix_world @ v16.co
co_v17 = circuit.matrix_world @ v17.co
co_v18 = circuit.matrix_world @ v18.co
    
    
def tourner(i, nbrFrame, angle):
    for x in  range(nbrFrame): 
        bpy.context.scene.frame_set(i) 
        for obj in car.all_objects:
            obj.rotation_euler[2] = obj.rotation_euler[2]+angle/(nbrFrame)
            obj.keyframe_insert(data_path="rotation_euler", frame = i)
        i += 1
        
def resetPosition():
    posInitY.clear()
    posInitX.clear()
    for obj in car.all_objects:
        coupleY = {obj:obj.location.y}
        coupleX = {obj:obj.location.x}
        posInitY.update(coupleY)
        posInitX.update(coupleX)

def contourner_obstacle(i):
    resetPosition()
    k = i
    #while obstacle.location.y-car.location.y > 0:
    while obstacle.location.y - capteur_distance.location.y > 30:
        bpy.context.scene.frame_set(i)
        for obj in car.all_objects:
            if i < 45:
                    obj.location[1] =  obj.location.y + 1/2 * 0.40 * (i/24)**2
            else:
                obj.location[1] =  obj.location.y + 0.5
            obj.keyframe_insert(data_path="location", frame = i)
        i = i+1
        
    tourner(i, 50, -0.64)
    
    while capteur_ligne_centre.location.y-obstacle.location.y  < 0:
        bpy.context.scene.frame_set(i)
        for obj in car.all_objects:
            obj.location[1] =  obj.location.y + 0.33
            obj.location[0] =  obj.location.x + 0.25
            obj.keyframe_insert(data_path="location", frame = i)
        i += 1
        
    tourner(i, 50, 0.64 * 2)
    
    resetPosition()
    
    while capteur_ligne_centre.location.x-obstacle.location.x  > 0: 
        bpy.context.scene.frame_set(i)
        for obj in car.all_objects:
            obj.location[1] =  obj.location.y + 0.33
            obj.location[0] =  obj.location.x - 0.25
            obj.keyframe_insert(data_path="location", frame = i)
        i += 1
    tourner(i, 20, -0.64)
    
    return i
resetPosition()


i2 = 0           
i = 0

i = contourner_obstacle(i) 

resetPosition()

#premiere avancement
while capteur_ligne_centre.location.y < co_v2[1]:
        bpy.context.scene.frame_set(i)
        for obj in car.all_objects:
            obj.location[1] =  obj.location.y + 0.5
            obj.keyframe_insert(data_path="location", frame = i)
        i = i+1

resetPosition()
    
j = 30

while j > 0 :
    bpy.context.scene.frame_set(i)
    for obj in car.all_objects:
        obj.location[1] =  posInitY.get(obj)+1/2 * (-10) * ((30-j)/24)**2 + 24*0.5* (30-j)/24
        obj.keyframe_insert(data_path="location", frame = i)
    j -= 1
    i = i+1
    
resetPosition()


i2=0
while capteur_ligne_centre.location.y > co_v3[1] + 5  :
            for obj in car.all_objects:
                obj.location[1] =  posInitY.get(obj)-1/2 * 10 * (i2/24)**2
                obj.keyframe_insert(data_path="location", frame = i)
            i2 = i2+1
            i = i+1

resetPosition()
    
j = 0
while j < 30 :
    bpy.context.scene.frame_set(i)
    for obj in car.all_objects:
        obj.location[1] =  posInitY.get(obj)+1/2 * (10) * ((j)/24)**2 - 10 * (j)/24
        obj.keyframe_insert(data_path="location", frame = i)
    j += 1
    i = i+1
#--------------
resetPosition()
    

tourner(i, 40, -0.52359878)
#deuxieme avancemnet
    
resetPosition()
    
i2=0
while capteur_ligne_centre.location.y < co_v4[1]:
        bpy.context.scene.frame_set(i)
        for obj in car.all_objects:
            obj.location[1] =  posInitY.get(obj)+1/2 * 3 * (i2/24)**2
            obj.location[0] =  posInitX.get(obj)+1/2 * 1.8* (i2/24)**2
            obj.keyframe_insert(data_path="location", frame = i)
        i2 = i2+1
        i = i+1

resetPosition()
    
j = 30

while j > 0 :
    bpy.context.scene.frame_set(i)
    for obj in car.all_objects:
        obj.location[1] =  posInitY.get(obj)+1/2 * (-3) * ((30-j)/24)**2 + 6 * (30-j)/24
        obj.location[0] =  posInitX.get(obj)+1/2 * (-1.8) * ((30-j)/24)**2 + 1.8*2 * (30-j)/24
        obj.keyframe_insert(data_path="location", frame = i)
    j -= 1
    i = i+1 
#reculer

i2=0
while capteur_ligne_centre.location.y > co_v5[1]+5:
        bpy.context.scene.frame_set(i)
        for obj in car.all_objects:
            obj.location[1] =  obj.location.y-1/2 * 0.5 * (i2/24)**2
            obj.location[0] =  obj.location.x-1/2 * 0.3 * (i2/24)**2
            obj.keyframe_insert(data_path="location", frame = i)
        i2 = i2+1
        i = i+1
        
resetPosition()
    
j = 0
while j < 30 :
    bpy.context.scene.frame_set(i)
    for obj in car.all_objects:
        obj.location[1] =  posInitY.get(obj)+1/2 * (5) * ((j)/24)**2 - 7.5 * (j)/24
        obj.location[0] =  posInitX.get(obj)+1/2 * (3) * ((j)/24)**2 -  4.5 * (j)/24
        obj.keyframe_insert(data_path="location", frame = i)
    j += 1
    i = i+1
     
tourner(i, 40, -0.52359878)

resetPosition()

i2=0
while capteur_ligne_centre.location.y < co_v6[1]:
        bpy.context.scene.frame_set(i)
        for obj in car.all_objects:
            obj.location[1] =  posInitY.get(obj)+1/2 * 1 * (i2/24)**2
            obj.location[0] =  posInitX.get(obj)+1/2 * 2 * (i2/24)**2
            obj.keyframe_insert(data_path="location", frame = i)
        i2 = i2+1
        i = i+1
        
        
resetPosition()
    
j = 30

while j > 0 :
    bpy.context.scene.frame_set(i)
    for obj in car.all_objects:
        obj.location[1] =  posInitY.get(obj)+1/2 * (-0.5*5) * ((30-j)/24)**2 + 1.5 * (30-j)/24
        obj.location[0] =  posInitX.get(obj)+1/2 * (-1*5) * ((30-j)/24)**2 + 3 * (30-j)/24
        obj.keyframe_insert(data_path="location", frame = i)
    j -= 1
    i = i+1 

i2=0
while capteur_ligne_centre.location.y >= co_v7[1]+2:
        bpy.context.scene.frame_set(i)
        for obj in car.all_objects:
            obj.location[1] =  obj.location.y-1/2 * 0.8 * (i2/24)**2
            obj.location[0] =  obj.location.x-1/2 * 2 * (i2/24)**2
            obj.keyframe_insert(data_path="location", frame = i)
        i2 = i2+1
        i = i+1
        
resetPosition()
    
j = 0
while j < 30 :
    bpy.context.scene.frame_set(i)
    for obj in car.all_objects:
        obj.location[1] =  posInitY.get(obj)+1/2 * (2) * ((j)/24)**2 - 2 * (j)/24
        obj.location[0] =  posInitX.get(obj)+1/2 * (5) * ((j)/24)**2 - 5 * (j)/24
        obj.keyframe_insert(data_path="location", frame = i)
    j += 1
    i = i+1
    
tourner(i, 40, -0.52359878)
#----------------------------------------------------------------------------
i2 = 0

resetPosition()

while capteur_ligne_centre.location.x < co_v7[0]:
        bpy.context.scene.frame_set(i)
        for obj in car.all_objects:
            if i2 < 45:
                obj.location[0] =  obj.location.x + 1/2 * 0.40 * (i2/24)**2
            else:
                obj.location[0] =  obj.location.x + 0.5
            obj.keyframe_insert(data_path="location", frame = i)
        i2 += 1
        i = i+1

resetPosition()

j = 30

while j > 0 :
    bpy.context.scene.frame_set(i)
    for obj in car.all_objects:
        obj.location[0] =  posInitX.get(obj)+1/2 * (-10) * ((30-j)/24)**2 + 24*0.5* (30-j)/24
        obj.keyframe_insert(data_path="location", frame = i)
    j -= 1
    i = i+1
    
resetPosition()
    
    
i2=0
while capteur_ligne_centre.location.x > co_v8[0]+5:
            for obj in car.all_objects:
                obj.location[0] =  posInitX.get(obj)-1/2 * 10 * (i2/24)**2
                obj.keyframe_insert(data_path="location", frame = i)
            i2 = i2+1
            i = i+1
            
resetPosition()
    
j = 0
while j < 30 :
    bpy.context.scene.frame_set(i)
    for obj in car.all_objects:
        obj.location[0] =  posInitX.get(obj)+1/2 * (10) * ((j)/24)**2 - 10 * (j)/24
        obj.keyframe_insert(data_path="location", frame = i)
    j += 1
    i = i+1

resetPosition()

tourner(i, 40, 0.52359878)


i2=0
while capteur_ligne_centre.location.x < co_v9[0]:
        bpy.context.scene.frame_set(i)
        for obj in car.all_objects:
            obj.location[1] =  posInitY.get(obj)+1/2 * 1.8 * (i2/24)**2
            obj.location[0] =  posInitX.get(obj)+1/2 * 3 * (i2/24)**2
            obj.keyframe_insert(data_path="location", frame = i)
        i2 = i2+1
        i = i+1

resetPosition()
    
j = 30

while j > 0 :
    bpy.context.scene.frame_set(i)
    for obj in car.all_objects:
        obj.location[1] =  posInitY.get(obj)+1/2 * (-1.8) * ((30-j)/24)**2 + 1.8*2 * (30-j)/24
        obj.location[0] =  posInitX.get(obj)+1/2 * (-3) * ((30-j)/24)**2 + 6 * (30-j)/24
        obj.keyframe_insert(data_path="location", frame = i)
    j -= 1
    i = i+1 
    
i2=0
while capteur_ligne_centre.location.x > co_v10[0]+5:
        bpy.context.scene.frame_set(i)
        for obj in car.all_objects:
            obj.location[1] =  obj.location.y-1/2 * 0.3 * (i2/24)**2
            obj.location[0] =  obj.location.x-1/2 * 0.5 * (i2/24)**2
            obj.keyframe_insert(data_path="location", frame = i)
        i2 = i2+1
        i = i+1
        
resetPosition()
    
j = 0
while j < 30 :
    bpy.context.scene.frame_set(i)
    for obj in car.all_objects:
        obj.location[1] =  posInitY.get(obj)+1/2 * (3) * ((j)/24)**2 - 4.5 * (j)/24
        obj.location[0] =  posInitX.get(obj)+1/2 * (5) * ((j)/24)**2 - 7.5 * (j)/24
        obj.keyframe_insert(data_path="location", frame = i)
    j += 1
    i = i+1
    
tourner(i, 40, 0.52359878)

resetPosition()

i2=0
while capteur_ligne_centre.location.x < co_v11[0]:
        bpy.context.scene.frame_set(i)
        for obj in car.all_objects:
            obj.location[1] =  posInitY.get(obj)+1/2 * 2 * (i2/24)**2
            obj.location[0] =  posInitX.get(obj)+1/2 * 1 * (i2/24)**2
            obj.keyframe_insert(data_path="location", frame = i)
        i2 = i2+1
        i = i+1

resetPosition()
    
j = 30

while j > 0 :
    bpy.context.scene.frame_set(i)
    for obj in car.all_objects:
        obj.location[1] =  posInitY.get(obj)+1/2 * (-1*5) * ((30-j)/24)**2 + 3 * (30-j)/24
        obj.location[0] =  posInitX.get(obj)+1/2 * (-0.5*5) * ((30-j)/24)**2 + 1.5 * (30-j)/24
        obj.keyframe_insert(data_path="location", frame = i)
    j -= 1
    i = i+1 

    
i2=0
while capteur_ligne_centre.location.x >= co_v12[0]+2:
        bpy.context.scene.frame_set(i)
        for obj in car.all_objects:
            obj.location[1] =  obj.location.y-1/2 * 2 * (i2/24)**2
            obj.location[0] =  obj.location.x-1/2 * 0.8 * (i2/24)**2
            obj.keyframe_insert(data_path="location", frame = i)
        i2 = i2+1
        i = i+1

resetPosition()
    
j = 0
while j < 30 :
    bpy.context.scene.frame_set(i)
    for obj in car.all_objects:
        obj.location[1] =  posInitY.get(obj)+1/2 * (5) * ((j)/24)**2 - 5 * (j)/24
        obj.location[0] =  posInitX.get(obj)+1/2 * (2) * ((j)/24)**2 - 2 * (j)/24
        obj.keyframe_insert(data_path="location", frame = i)
    j += 1
    i = i+1
    
tourner(i, 40, 0.52359878)
#----------------------------------------------------------------------------

i2 = 0
while capteur_ligne_centre.location.y < co_v12[1]:
        bpy.context.scene.frame_set(i)
        for obj in car.all_objects:
            if i2 < 45:
                obj.location[1] =  obj.location.y+1/2 * 0.40 * (i2/24)**2
            else:
                obj.location[1] =  obj.location.y + 0.5
            obj.keyframe_insert(data_path="location", frame = i)
        i2 += 1
        i = i+1

resetPosition()
    
j = 30

while j > 0 :
    bpy.context.scene.frame_set(i)
    for obj in car.all_objects:
        obj.location[1] =  posInitY.get(obj)+1/2 * (-10) * ((30-j)/24)**2 + 24*0.5 * (30-j)/24
        obj.keyframe_insert(data_path="location", frame = i)
    j -= 1
    i = i+1
    
resetPosition()
    
i2=0
while capteur_ligne_centre.location.y > co_v13[1]+5:
            for obj in car.all_objects:
                obj.location[1] =  posInitY.get(obj)-1/2 * 10 * (i2/24)**2
                obj.keyframe_insert(data_path="location", frame = i)
            i2 = i2+1
            i = i+1

resetPosition()
    
j = 0
while j < 30 :
    bpy.context.scene.frame_set(i)
    for obj in car.all_objects:
        obj.location[1] =  posInitY.get(obj)+1/2 * (10) * ((j)/24)**2 - 10 * (j)/24
        obj.keyframe_insert(data_path="location", frame = i)
    j += 1
    i = i+1

resetPosition()
    
tourner(i, 40, 0.52359878)

resetPosition()

i2=0
while capteur_ligne_centre.location.y < co_v14[1]:
        bpy.context.scene.frame_set(i)
        for obj in car.all_objects:
            obj.location[1] =  posInitY.get(obj)+1/2 * 3 * (i2/24)**2
            obj.location[0] =  posInitX.get(obj)-1/2 * 1.8 * (i2/24)**2
            obj.keyframe_insert(data_path="location", frame = i)
        i2 = i2+1
        i = i+1

resetPosition()

j = 30

while j > 0 :
    bpy.context.scene.frame_set(i)
    for obj in car.all_objects:
        obj.location[1] =  posInitY.get(obj)+1/2 * (-3) * ((30-j)/24)**2 + 6 * (30-j)/24
        obj.location[0] =  posInitX.get(obj)-1/2 * (-1.8) * ((30-j)/24)**2 - 1.8*2 * (30-j)/24
        obj.keyframe_insert(data_path="location", frame = i)
    j -= 1
    i = i+1 
    
i2=0
while capteur_ligne_centre.location.y > co_v15[1]+5:
        bpy.context.scene.frame_set(i)
        for obj in car.all_objects:
            obj.location[1] =  obj.location.y-1/2 * 0.5 * (i2/24)**2
            obj.location[0] =  obj.location.x+1/2 * 0.3 * (i2/24)**2
            obj.keyframe_insert(data_path="location", frame = i)
        i2 = i2+1
        i = i+1
        
resetPosition()

j = 0
while j < 30 :
    bpy.context.scene.frame_set(i)
    for obj in car.all_objects:
        obj.location[1] =  posInitY.get(obj)+1/2 * (5) * ((j)/24)**2 - 7.5 * (j)/24
        obj.location[0] =  posInitX.get(obj)-1/2 * (3) * ((j)/24)**2 + 4.5 * (j)/24
        obj.keyframe_insert(data_path="location", frame = i)
    j += 1
    i = i+1
    
tourner(i, 40, 0.52359878)

resetPosition()
    
i2=0
while capteur_ligne_centre.location.y < co_v16[1]:
        bpy.context.scene.frame_set(i)
        for obj in car.all_objects:
            obj.location[1] =  posInitY.get(obj)+1/2 * 1 * (i2/24)**2
            obj.location[0] =  posInitX.get(obj)-1/2 * 2 * (i2/24)**2
            obj.keyframe_insert(data_path="location", frame = i)
        i2 = i2+1
        i = i+1

resetPosition()
    
j = 30

while j > 0 :
    bpy.context.scene.frame_set(i)
    for obj in car.all_objects:
        obj.location[1] =  posInitY.get(obj)+1/2 * (-0.5*5) * ((30-j)/24)**2 + 1.5 * (30-j)/24
        obj.location[0] =  posInitX.get(obj)-1/2 * (-1*5) * ((30-j)/24)**2 - 3 * (30-j)/24
        obj.keyframe_insert(data_path="location", frame = i)
    j -= 1
    i = i+1 
    
#recule

i2=0
while capteur_ligne_centre.location.y >= co_v17[1]+2:
        bpy.context.scene.frame_set(i)
        for obj in car.all_objects:
            obj.location[1] =  obj.location.y-1/2 * 0.8 * (i2/24)**2
            obj.location[0] =  obj.location.x+1/2 * 2 * (i2/24)**2
            obj.keyframe_insert(data_path="location", frame = i)
        i2 = i2+1
        i = i+1

resetPosition()
    
j = 0
while j < 30 :
    bpy.context.scene.frame_set(i)
    for obj in car.all_objects:
        obj.location[1] =  posInitY.get(obj)+1/2 * (2) * ((j)/24)**2 - 2 * (j)/24
        obj.location[0] =  posInitX.get(obj)-1/2 * (5) * ((j)/24)**2 + 5 * (j)/24
        obj.keyframe_insert(data_path="location", frame = i)
    j += 1
    i = i+1
    
tourner(i, 40, 0.52359878)

i2 = 0
while capteur_ligne_centre.location.x > co_v18[0]:
    bpy.context.scene.frame_set(i)
    for obj in car.all_objects:
        if i2 < 45:
            obj.location[0] =  obj.location.x-1/2 * 0.40 * (i2/24)**2
        else:
            obj.location[0] =  obj.location.x - 0.5
        obj.keyframe_insert(data_path="location", frame = i)
    if capteur_ligne_centre.location.x - obstacle2.location.x < 40:
        break
    i2 += 1
    i = i+1
        
resetPosition()
j = 30
while j > 0 :
    bpy.context.scene.frame_set(i)
    for obj in car.all_objects:
        obj.location[0] =  posInitX.get(obj)+1/2 * (10) * ((30-j)/24)**2 - 24*0.5 * (30-j)/24
        obj.keyframe_insert(data_path="location", frame = i)
    j -= 1
    i = i+1

bpy.ops.screen.animation_play()

# #collision = check_Collision(get_BoundBox('Cube1'), get_BoundBox('Cube2'))

# objects = bpy.data.objects

# bpy.context.view_layer.objects.active = circuit

# bpy.context.view_layer.objects.active = circuit
# v = circuit.data.vertices[233]

# co_final = circuit.matrix_world @ v.co

# # now we can view the location by applying it to an object
# obj_empty = bpy.data.objects.new("Test", None)
# bpy.context.collection.objects.link(obj_empty)
# obj_empty.location = co_final