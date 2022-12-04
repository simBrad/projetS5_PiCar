#!/usr/bin/env python
'''
**********************************************************************
Ce code est en construction, veuillez modifier les imports pour correspondre à l'environnement du picar ou hors picar

Le code contien 2 méthodes de contrôle de la direction:
-Smooth : changement progressif de la direction avec un minimum de perte en rapidité de réaction
-Step : le changement d'angle ce fait par incrément arbitraire.
**********************************************************************
'''
from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance
from SunFounder_Line_Follower import Line_Follower
#In Picar
from picar import front_wheels
from picar import back_wheels
import picar
import time
#Hors Picar
#import SunFounder_PiCar.picar as picar
#from SunFounder_PiCar.picar import front_wheels
#from SunFounder_PiCar.picar import back_wheels

#DO NOT MODIFY#################################
picar.setup()

REFERENCES = [200, 200, 200, 200, 200]
calibrate = False
forward_speed = 40
backward_speed = 30
max_off_track_count = 100
delay = 0.0005

distance_freinage = 10
distance_contournement = 30


fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')
lf = Line_Follower.Line_Follower()
UA = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)

UA.timeout = 0.0025
threshold = 10
lf.references = REFERENCES
fw.ready()
bw.ready()
fw.turning_max = 45
###################################################

def destroy():
    bw.stop()
    fw.turn(90)


def changement_vitesse_continu(vitesse_cible, vitesse_precedente):
    #accélération et décélération V1
    actual_speed = bw._speed
    cool = 0
    if actual_speed > vitesse_cible:
        #print("on doit ralentir")
        #applique décélération
        if vitesse_cible != actual_speed +1:
            bw.speed = vitesse_precedente - 1
            #print(bw._speed)
            time.sleep(0.05)
        #print("vitesse reduite")
    elif actual_speed < vitesse_cible:
        #print("on doit accelerer")
        #applique accélération
        if vitesse_cible != actual_speed -1:
            bw.speed = vitesse_precedente + 1
            #print(bw._speed)
            time.sleep(0.05)
        #print("vitesse augmente")
    else:
        #print("vitesse cible déjà atteinte")
        cool = 1 #juste pour pas avoir un elif vide ce qui cause une erreure
    actual_speed = bw._speed
    return actual_speed

def routine_de_contournement(moyenne_distance,mesures_precedante:list):
    bw.backward()
    bw.speed = backward_speed
    stop = 0
    while stop == 0:
        mesures_precedante,moyenne_distance = calcule_distance(mesures_precedante)
        if moyenne_distance >= 29:
            stop = 1
    bw.speed = 0
    bw.forward()
    fw.turn(45)
    time.sleep(0.5)
    bw.speed = 30
    time.sleep(3)
    fw.turn(135)
    time.sleep(4)
    fw.turn(90)
    time.sleep(4)
    fw.turn(135)
    time.sleep(3)
    print("sortie Contournement")
    return bw._speed, 135
    

#contrôle de la direction smooth
def calcule_angle_smooth(step,previous_step):
    a_step = 1
    b_step = 1.5
    c_step = 2
    d_step = 2.5
    lt_status_now = lf.read_digital()
    #print(lt_status_now)
    # Calcule de l'angle d'ajustement
    if step < -45:
        step = -45
    elif step > 45:
        step = 45
    else:
        if lt_status_now == [0, 0, 1, 0, 0]:
            step = 0
        elif lt_status_now == [0, 1, 1, 0, 0]:
            step = (step - a_step) * previous_step
            previous_step = -1
        elif lt_status_now == [0, 0, 1, 1, 0]:
            step = (step + a_step) * abs(previous_step)
            previous_step = 1
        elif lt_status_now == [0, 1, 0, 0, 0]:
            step = (step - b_step) * previous_step
            previous_step = -2
        elif lt_status_now == [0, 0, 0, 1, 0]:
            step = (step + b_step) * abs(previous_step)
            previous_step = 2
        elif lt_status_now == [1, 1, 0, 0, 0]:
            step = (step - c_step) * previous_step
            previous_step = -3
        elif lt_status_now == [0, 0, 0, 1, 1]:
            step = (step + c_step) * abs(previous_step)
            previous_step = 3
        elif lt_status_now == [1, 0, 0, 0, 0]:
            step = (step - d_step) * previous_step
            previous_step = -4
        elif lt_status_now == [0, 0, 0, 0, 1]:
            step = (step + d_step) * abs(previous_step)
            previous_step = 4
    #print("step", step)
    return lt_status_now,step,previous_step


def suivie_ligne_smooth(off_track_count,step,turning_angle,lt_status_now):
    if lt_status_now == [0, 0, 1, 0, 0]:
        off_track_count = 0
        turning_angle = 90
    # Ajustement vers la droite
    elif lt_status_now in ([0, 1, 1, 0, 0], [0, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 0, 0, 0, 0]):
        off_track_count = 0
        turning_angle = int(90 - abs(step))
    # Ajustement vers la gauche
    elif lt_status_now in ([0, 0, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]):
        off_track_count = 0
        turning_angle = int(90 + step)
    # Si on sort du parcours
    if lt_status_now == [0, 0, 0, 0, 0]:
        off_track_count += 1
    else:
        off_track_count = 0
    # Last check
    if turning_angle < 45:
        turning_angle = 45
    elif turning_angle > 135:
        turning_angle = 135
    fw.turn(turning_angle)
    time.sleep(delay)
    return off_track_count,turning_angle


#contrôle de la direction step
def suivie_ligne_step(off_track_count, lt_status_now, step, turning_angle,vitesse_actuel):
    # Suivi de la trajectoire suiveur de ligne
    if lt_status_now == [0, 0, 1, 0, 0]:
        off_track_count = 0
        turning_angle = 90
        #print("centrer")
    # Ajustement vers la droite
    elif lt_status_now in ([0, 1, 1, 0, 0], [0, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 0, 0, 0, 0]):
        off_track_count = 0
        turning_angle = int(90 - step)
        #print("gauche")
    # Ajustement vers la gauche
    elif lt_status_now in ([0, 0, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]):
        off_track_count = 0
        turning_angle = int(90 + step)
        #print("Droite")
    # Si on sort du parcours
    elif lt_status_now == [0, 0, 0, 0, 0]:
        off_track_count += 1
        #print("Offtrack ++ ")
    else:
        off_track_count = 0
        #print("Offtrack reset")
    #print("turning angle: ",turning_angle)
    fw.turn(turning_angle)
    time.sleep(delay)
    return off_track_count,turning_angle


def calcule_angle_step():
    a_step = 5
    b_step = 10
    c_step = 30
    d_step = 45
    step = 0
    lt_status_now = lf.read_digital()
    #print(lt_status_now)
    # Calcule de l'angle d'ajustement
    if lt_status_now == [0, 0, 1, 0, 0]:
        step = 0
    elif lt_status_now == [0, 1, 1, 0, 0] or lt_status_now == [0, 0, 1, 1, 0]:
        step = a_step
    elif lt_status_now == [0, 1, 0, 0, 0] or lt_status_now == [0, 0, 0, 1, 0]:
        step = b_step
    elif lt_status_now == [1, 1, 0, 0, 0] or lt_status_now == [0, 0, 0, 1, 1]:
        step = c_step
    elif lt_status_now == [1, 0, 0, 0, 0] or lt_status_now == [0, 0, 0, 0, 1]:
        step = d_step
    return lt_status_now, step


def calcule_distance(mesures_precedante:list):
    UA.timeout = 0.3
    mesures_precedante.pop(0)
    ok = 0
    while ok == 0:
        mesure_actuel = UA.get_distance()
        if mesure_actuel != -1:
            mesures_precedante.append(mesure_actuel)
            ok = 1
        else:
            ok = 0
    #print(mesures_precedante)
    moyennes_mesures = int(sum(mesures_precedante)/len(mesures_precedante))
    #print("moyennes: ", moyennes_mesures)
    return mesures_precedante,moyennes_mesures


def main():
    bw.speed = 0
    bw.forward()
    off_track_count = 0
    vitesse_actuel = 0
    lt_status_now = []
    step = 0
    turning_angle = 90
    previous_step = 0
    moyenne_distance = 100
    mesures_precedente = [100,100,100,100,100,100,100,100,100]
    flag_backward = 0 #signale que nous reculons
    flag_post_contournement = 0#block la routine de off track lorsque nous sortons de la routine de contournement jusqu'à ce qu'on recroise le parcours
    flag_v_max = 0
    running = 1
    while running :

        # détection d'obstacles
        if flag_post_contournement != 1 and turning_angle != 135 and turning_angle != 45:
            mesures_precedente, moyenne_distance = calcule_distance(mesures_precedente)
        #controle de vitesse situationnel
        if moyenne_distance <= 20 and moyenne_distance > 10 and flag_backward != 1 and flag_post_contournement != 1:
            #print("obstacle potentiel")
            vitesse_actuel=changement_vitesse_continu(30,vitesse_actuel)
            bw.forward()
        elif moyenne_distance <= 10 and flag_backward != 1 and flag_post_contournement != 1:
            #print("obstacle detecter")
            bw.speed = 0
            vitesse_actuel = 0
            time.sleep(2)
            #print("début routine de contournement")
            vitesse_actuel, turning_angle = routine_de_contournement(moyenne_distance,mesures_precedente)
            #postturn = 30
            off_track_count = 0
            mesures_precedente = [100,100,100,100,100,100,100,100,100]
            moyenne_distance = 100
            flag_post_contournement = 1
        
        
        elif off_track_count > max_off_track_count and flag_backward != 1 and flag_post_contournement != 1 and flag_v_max == 1:
            #start offtrack
            #print("Offtrack slowdown")
            vitesse_actuel=changement_vitesse_continu(0,vitesse_actuel)
            if vitesse_actuel == 0:
                #print("offtract")
                bw.backward()
                fw.turn(90)
                flag_backward = 1
                #invertion FW
                tmp_angle = 0
                #print("turning angle 1: ", turning_angle)
                if turning_angle < 90:
                    turning_angle = 135
                    #print("< 90",turning_angle)
                elif turning_angle > 90:
                    turning_angle = 45
                    #print(">90",turning_angle)
                #tmp_angle *= fw.turning_max
        elif off_track_count < max_off_track_count and flag_backward == 1 and flag_post_contournement != 1:
            # Stop Offtrack
            #print("offtrack correction completed")
            vitesse_actuel=changement_vitesse_continu(0,vitesse_actuel)
            if vitesse_actuel == 0:
                bw.forward()
                flag_backward = 0
                flag_v_max = 0
        else:
            #Vitesse normal
            vitesse_actuel=changement_vitesse_continu(forward_speed,vitesse_actuel)
            #print("vitesse normale")
            
        # direction smooth mode
        #lt_status_now,step,previous_step = calcule_angle_smooth(step,previous_step)
        # direction step mode
        lt_status_now,step = calcule_angle_step()
        if lt_status_now == [1,1,1,1,1]:
            bw.stop()
            #print("fin de course")
            running = 0
            destroy()
            return 0
        elif lt_status_now != [0,0,0,0,0] and flag_post_contournement == 1:
            flag_post_contournement = 0
            off_track_count = 0
            #print("fpc reset")
        else:
            off_track_count,turning_angle = suivie_ligne_step(off_track_count, lt_status_now, step, turning_angle,vitesse_actuel)
            #print("suivie normal")
            #Smooth mode
            #off_track_count,turning_angle = suivie_ligne_smooth(off_track_count,step,turning_angle,lt_status_now)
        print("off track count", off_track_count)
        if flag_v_max == 0 and vitesse_actuel >= forward_speed:
            flag_v_max = 1
            

if __name__ == '__main__':
    try:
        try:
            while True:
                main()
        except Exception as e:
            print(e)
            print('error try again in 5')
            destroy()
            time.sleep(5)
    except KeyboardInterrupt:
        destroy()