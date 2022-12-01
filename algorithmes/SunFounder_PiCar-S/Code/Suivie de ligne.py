#!/usr/bin/env python
'''
**********************************************************************
Ce code est en construction, veuillez modifier les imports pour correspondre à l'environnement du picar ou hors picar

Le code contien 2 méthodes de contrôle de la direction:
-Smooth : changement progressif de la direction avec un minimum de perte en rapidité de réaction
-Step : le changement d'angle ce fait par incrément arbitraire.
**********************************************************************
'''

from SunFounder_Line_Follower import Line_Follower
# In Picar
from picar import front_wheels
from picar import back_wheels
import picar
import time

# Hors Picar
# import SunFounder_PiCar.picar as picar
# from SunFounder_PiCar.picar import front_wheels
# from SunFounder_PiCar.picar import back_wheels

# DO NOT MODIFY#################################
picar.setup()

REFERENCES = [200, 200, 200, 200, 200]
calibrate = False
forward_speed = 70
backward_speed = 30
turning_angle = 40
max_off_track_count = 40
delay = 0.0005

fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')
lf = Line_Follower.Line_Follower()

lf.references = REFERENCES
fw.ready()
bw.ready()
fw.turning_max = 45


###################################################

def destroy():
    bw.stop()
    fw.turn(90)


def changement_vitesse_continu(vitesse_cible, vitesse_precedente):
    # accélération et décélération V1
    actual_speed = bw._speed
    cool = 0
    if actual_speed > vitesse_cible:
        # print("on doit ralentir")
        # applique décélération
        if vitesse_cible != actual_speed + 1:
            bw.speed = vitesse_precedente - 1
            # print(bw._speed)
            time.sleep(0.05)
        # print("vitesse reduite")
    elif actual_speed < vitesse_cible:
        # print("on doit accelerer")
        # applique accélération
        if vitesse_cible != actual_speed - 1:
            bw.speed = vitesse_precedente + 1
            # print(bw._speed)
            time.sleep(0.05)
        # print("vitesse augmente")
    else:
        # print("vitesse cible déjà atteinte")
        cool = 1  # juste pour pas avoir un elif vide ce qui cause une erreure
    actual_speed = bw._speed
    return actual_speed


# contrôle de la direction smooth
def calcule_angle_smooth(step, previous_step):
    a_step = 1
    b_step = 1.5
    c_step = 2
    d_step = 2.5
    lt_status_now = lf.read_digital()
    # print(lt_status_now)
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
    # print("step", step)
    return lt_status_now, step, previous_step


def suivie_ligne_smooth(off_track_count, step, turning_angle, lt_status_now):
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
    return off_track_count, turning_angle


# contrôle de la direction step
def suivie_ligne_step(off_track_count, lt_status_now, step):
    global turning_angle
    # Suivi de la trajectoire suiveur de ligne
    if lt_status_now == [0, 0, 1, 0, 0]:
        off_track_count = 0
        turning_angle = 90
    # Ajustement vers la droite
    elif lt_status_now in ([0, 1, 1, 0, 0], [0, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 0, 0, 0, 0]):
        off_track_count = 0
        turning_angle = int(90 - step)
    # Ajustement vers la gauche
    elif lt_status_now in ([0, 0, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]):
        off_track_count = 0
        turning_angle = int(90 + step)
    # Si on sort du parcours
    elif lt_status_now == [0, 0, 0, 0, 0]:
        off_track_count += 1
    else:
        off_track_count = 0
    # print("turning angle: ",turning_angle)
    fw.turn(turning_angle)
    time.sleep(delay)
    return off_track_count


def calcule_angle_step():
    a_step = 3
    b_step = 10
    c_step = 30
    d_step = 45
    step = 0
    lt_status_now = lf.read_digital()
    # print(lt_status_now)
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


def main():
    off_track_count = 0
    vitesse_actuel = 0
    lt_status_now = []
    step = 0
    turning_angle = 90
    previous_step = 0
    while True:
        if off_track_count > max_off_track_count:
            vitesse_actuel = changement_vitesse_continu(forward_speed / 2, vitesse_actuel)
        else:
            vitesse_actuel = changement_vitesse_continu(forward_speed, vitesse_actuel)
        # direction smooth mode
        # lt_status_now,step,previous_step = calcule_angle(step,previous_step)
        # off_track_count,turning_angle = suivie_ligne(off_track_count,step,turning_angle,lt_status_now)

        # direction step mode
        lt_status_now, step = calcule_angle_step()
        off_track_count = suivie_ligne_step(off_track_count, lt_status_now, step)


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