import subprocess
from random import randint, choice
from library_for_glad_ai_tors import *

RED = "tier_7.py"
baseTankFile = open("baseTank.py")
BASE_TANK = baseTankFile.read()
baseTankFile.close()

place_children = {1:19, 2:19, 3:19, 4:19, 5:19}#{1:48, 2:24, 3:12, 4:6, 5:3, 6:1}
def wins(tankTest):
    result = str(subprocess.Popen('python.exe glad_ai_tors.py '+ RED + ' ' + tankTest,
                       stdout=subprocess.PIPE).stdout.read())
    return tankTest[:-3] in result

class Tank():

    def __init__(self, gen, num,
                 flee_threshold = randint(60, 95),
                 flee_timeout = randint(12, 75),
                 uses_shields = choice([True, False]),
                 charge_limit = randint(1, 100),
                 dir_change = randint(12, 75)):
        self.name = "Gen" + str(gen) + "Num" + str(num) + ".py"
        self.file = open(self.name, 'w')
        self.flee_threshold = flee_threshold
        self.flee_timeout = flee_timeout
        self.uses_shields = uses_shields
        self.charge_limit = charge_limit
        self.dir_change = dir_change

        self.header = ("FLEE_THRESHOLD = " + str(self.flee_threshold) + 
                       "\nFLEE_TIMEOUT = " + str(self.flee_timeout) + 
                       "\nUSES_SHIELDS = " + str(self.uses_shields) + 
                       "\nCHARGE_LIMIT = " + str(self.charge_limit) + 
                       "\nDIR_CHANGE = " + str(self.dir_change) + 
                       "\n")
        self.file_text = self.header + BASE_TANK
        self.file.write(self.file_text)
        self.file.close()
        self.time = 0

def create_children(tanks, gen):
    new_tanks = tanks
    tank_num = 0
    for i in range(len(tanks)):
        for j in range(place_children[i + 1]):
            new_flee_threshold = max(tanks[i].flee_threshold + randint(-9, 9), 60)
            new_flee_timeout = max(tanks[i].flee_timeout + randint(-16, 16), 12)
            new_uses_shields = choice([True, False])
            new_charge_limit = max(tanks[i].charge_limit + randint(-25, 25), 1)
            new_dir_change = max(tanks[i].dir_change + randint(-16, 16), 12)
            new_tank = Tank(gen, tank_num, new_flee_threshold, new_flee_timeout,
                            new_uses_shields, new_charge_limit, new_dir_change)
            new_tanks.append(new_tank)
            tank_num += 1

    return new_tanks

generations = 5
tanks_num = 100
        
tanks = []
winning_tanks = []
for i in range(generations):
    print("Creating generation " + str(i))
    if i == 0:
        for j in range(tanks_num):
            new_tank = Tank(i, j)
            tanks.append(new_tank)
    else:
        tanks = create_children(winning_tanks, i)

    for j in range(len(tanks)):
        print("Testing tank " + tanks[j].name)
        won = wins(tanks[j].name)
        if won:
            winning_tanks.append(tanks[j])
        print("Tank " + tanks[j].name + " " + str(won))

    print("Num Winners: " + str(len(winning_tanks)))
    if len(winning_tanks) > 5:
        new_winning_tanks = []
        for j in range(5):
            new_winning_tanks.append(winning_tanks.pop(randint(0, len(winning_tanks))))
        winning_tanks = new_winning_tanks
    elif len(winning_tanks) < 5:
        for j in range(5 - len(winning_tanks)):
            invalid = True
            while invalid:
                add_tank = tanks[randint(0, len(tanks) - 1)]
                invalid = add_tank in winning_tanks
            winning_tanks.append(add_tank)
    gen_complete = "Generation " + str(i) + " complete. Winners are:"
    for j in range(len(winning_tanks)):
        gen_complete += (" " + winning_tanks[j].name)
    input(gen_complete)
        
#wins("baseTank.py")
