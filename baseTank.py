from random import randint
#FLEE_THRESHOLD = 90 #determines at what damage tank flees
#FLEE_TIMEOUT = 25 #determines when the tank starts searching again
#USES_SHIELDS = False#determines if the tank will use its shields when moving
#CHARGE_LIMIT = 50#determines how much the tank will charge its weapon
#DIR_CHANGE = 25#determines how long until the tank changes direction

from library_for_glad_ai_tors import *
import math

def get_rotate_angle(currentAngle, destAngle):
    resultAngle = destAngle - currentAngle
    if abs(resultAngle) > 180:
        resultAngle = abs(resultAngle) - 360
    return resultAngle

def start(arg):
    return ("search", {'A': FLEE_THRESHOLD,
                       'B': FLEE_TIMEOUT,
                       'C': 0, # Curr flee timeout
                       'D': USES_SHIELDS,
                       'E': CHARGE_LIMIT,
                       'F': 0, # Direction, N-0, E-1, S-2, W-3
                       'G': DIR_CHANGE,
                       'H': 0, # Curr dir change
                       'CHARGE': True})

def search(arg):
    
    if get_damage_level(arg) > get_saved_data(arg, 'A') and (get_saved_data(arg, 'C') == 0):
        new_dir = randint(0, 3)
        return("flee", {'SHIELD': False, 'F': new_dir})

    weapon_ang = get_weapon_angle(arg)
    shield = get_saved_data(arg, 'D')
    n_wall = get_n_border(arg)
    s_wall = get_s_border(arg)
    e_wall = get_e_border(arg)
    w_wall = get_w_border(arg)
    pos = get_position(arg)
    vel = get_velocity(arg)
    direc = get_saved_data(arg, 'F')
    new_dir = direc
    r_cc = 0
    r_cw = 1
    
    for i in range(0, 360):
        (detected, distance) = get_radar_data(arg, i)

        if detected == "opponent":
            angle = get_rotate_angle(weapon_ang, i)
            if abs(angle) < 30 and distance < 400:
                if angle > 0:
                    return ("attack", {'CHARGE': False,
                                       'ROT_CC':1, 'H':0})
                elif angle < 0:
                    return ("attack", {'CHARGE': False,
                                       'ROT_CW':1, 'H':0})
                else:
                    return ("attack", {'CHARGE': False,
                                       'H':0})
            else:
                if angle > 0:
                    r_cc = 1
                    r_cw = 0
                    #return ("search", {'ROT_CC':1, 'H':0})
                elif angle < 0:
                    r_cc = 0
                    r_cw = 1
                    #return ("search", {'ROT_CW':1, 'H':0})
                
        elif detected == "obstacle":
            if distance < 100:
                y_acc = -1 * (math.sin(i) / abs(math.sin(i)))
                x_acc = -1 * (math.cos(i) / abs(math.cos(i)))
                return("search", {'ACLT_X': x_acc, 'ACLT_Y': y_acc,
                                  'SHIELD': shield,
                                  'CHARGE': False,
                                  'H': (get_saved_data(arg, 'H') + 1)})
#python.exe glad_ai_tors.py tier_7.py baseTank.py
    
    if get_saved_data(arg, 'H') == get_saved_data(arg, 'G'):
        new_dir = randint(0, 3)
        print(new_dir)
        return("search", {'H': 0, 'F': new_dir})
    
    dx = 0
    dy = 0
    if direc == 1:
        d_e = abs(e_wall - pos[0])
        if d_e < 200: #vel[0]:
            dx = -1
            new_dir = 3
        else:
            dx = 1
    elif direc == 3:
        d_w = abs(w_wall - pos[0])
        if d_w < 200: #vel[0]:
            dx = 1
            new_dir = 1
        else:
            dx = -1
    if direc == 0:
        d_n = abs(n_wall - pos[1])
        if d_n < 200: #vel[1]:
            print('north')
            dy = 1
            new_dir = 2
        else:
            dy = -1
    elif direc == 2:
        d_s = abs(s_wall - pos[1])
        if d_s < 200: #vel[1]:
            dy = -1
            new_dir = 0
        else:
            dy = 1

    return("search", {'ACLT_X': dx, 'ACLT_Y': dy,
                      'H': (get_saved_data(arg, 'H') + 1),
                      'CHARGE': False, 'F': new_dir, 'SHIELD': shield,
                      'ROT_CC':r_cc, 'ROT_CW':r_cw, 'D_TEXT': 'searching'})

def attack(arg):
    if (get_damage_level(arg) > get_saved_data(arg, 'A')) and (get_saved_data(arg, 'C') == 0):
        new_dir = randint(0, 3)
        return("flee", {'SHIELD': False, 'F': new_dir})     
    
    weapon_ang = get_weapon_angle(arg)
    weapon_charge = get_weapon_power(arg)
    charge_max = get_saved_data(arg, 'E')
    
    for i in range(0, 360):
        (detected, distance) = get_radar_data(arg, i)
        if detected == "opponent":
            angle = get_rotate_angle(weapon_ang, i)
            if abs(angle) < 30:
                if angle > 0:
                    if charge_max > weapon_charge:
                        return("attack", {'CHARGE': True, 'ROT_CC':1})
                    else:
                        return ("attack", {'LAUNCH': True, 'CHARGE': False,
                                           'ROT_CC':1})
                elif angle < 0:
                    if charge_max > weapon_charge:
                        return("attack", {'CHARGE': True, 'ROT_CW':1})
                    else:
                        return ("attack", {'LAUNCH': True,  'CHARGE': False,
                                           'ROT_CW':1})
                else:
                    if charge_max > weapon_charge:
                        return("attack", {'CHARGE': True})
                    else:
                        return ("attack", {'LAUNCH': True, 'CHARGE': False})
            else:
                if angle > 0:
                    return ("search", {'ROT_CC':1, 'H':0})
                elif angle < 0:
                    return ("search", {'ROT_CW':1, 'H':0})

def flee(arg):
    shield = get_saved_data(arg, 'D')
    n_wall = get_n_border(arg)
    s_wall = get_s_border(arg)
    e_wall = get_e_border(arg)
    w_wall = get_w_border(arg)
    pos = get_position(arg)
    vel = get_velocity(arg)
    direc = get_saved_data(arg, 'F')
    new_dir = direc

    if get_saved_data(arg, 'C') > get_saved_data(arg, 'B'):
        return("search", {"SHIELD": shield})
    
    for i in range(0, 360):
        (detected, distance) = get_radar_data(arg, i)
        if detected == "obstacle":
            if distance < 100:
                y_acc = -1 * (math.sin(i) / abs(math.sin(i)))
                x_acc = -1 * (math.cos(i) / abs(math.cos(i)))
                shield = get_saved_data(arg, 'E')
                return("flee", {'ACLT_X': x_acc, 'ACLT_Y': y_acc,
                                  'C': (get_saved_data(arg, 'C') + 1)})
    
    if get_saved_data(arg, 'C') == get_saved_data(arg, 'G'):
        new_dir = randint(0, 3)
        print(new_dir)
        return("search", {'F': new_dir})
    
    dx = 0
    dy = 0
    if direc == 1:
        d_e = abs(e_wall - pos[0])
        if d_e < 200: #vel[0]:
            dx = -1
            new_dir = 3
        else:
            dx = 1
    elif direc == 3:
        d_w = abs(w_wall - pos[0])
        if d_w < 200: #vel[0]:
            dx = 1
            new_dir = 1
        else:
            dx = -1
    if direc == 0:
        d_n = abs(n_wall - pos[1])
        if d_n < 200: #vel[1]:
            print('north')
            dy = 1
            new_dir = 2
        else:
            dy = -1
    elif direc == 2:
        d_s = abs(s_wall - pos[1])
        if d_s < 200: #vel[1]:
            dy = -1
            new_dir = 0
        else:
            dy = 1

    return("flee", {'ACLT_X': dx, 'ACLT_Y': dy,
                      'C': (get_saved_data(arg, 'C') + 1),
                      'CHARGE': False, 'F': new_dir})
