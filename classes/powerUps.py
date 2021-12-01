
import random


#apply to player powers only


# powerUps = [
#     ('ON_DEFEAT_RECOVER_HP', f"After defeating an enemy, there's a chance to recover a set amount of HP"),
    
#     ('BULLET_SPEED', "When pressing Mouse right-click, your bullets fly out at a faster speed"),
#     ("BULLET_POWER_UP", "Shoot with Mouse right-click. Inflict greater damage on enemies with your bullets."),

#     ('DASH_DISTANCE',"Press SPACE to dash. Your dash distance can travel one space further"),
#     ('DASH_COOLDOWN', "After dashing with SPACE, it takes less time before you can dash again."),
#     ('DASH_RECOVER_HP', f"After dashing with SPACE, there's a chance to recover a set amount of HP"),
    
#     ('SECOND_CHANCE', "Revive after dying. Can only happen once."),
    
#     ('RECOVER_HP', "Recover HP"),
#     ('INCREASE_MAX_HP', 'Increase MAX HP'),
    
#     ('ABSORB_ORANGE', "Orange bullets are absorbed. No damage is dealt when hit by them anymore."),
#     ('ABSORB_PURPLE', "Purple bullets are absorbed. No damage is dealt when hit by them anymore."),

#     #press f to turn enemies blue and freeze their movement for 3 seconds
#     #press e to fire powerful red bullets that can phase through obstacles every 8 seconds

# ]


#for the sake of attaining MVP quicker lool
easyPowerUps = [
    
    ('BULLET_COOLDOWN', "When pressing Mouse left-click, it takes less time to shoot between fired bullets", '%'),
    ("BULLET_POWER_UP", "Shoot with Mouse left-click. Inflict greater damage on enemies with your bullets.", '%'),

    ('DASH_DISTANCE',"Press SPACE to dash. Your dash distance can travel one space further", 'num'),
    ('DASH_COOLDOWN', "After dashing with SPACE, it takes less time before you can dash again.", '%'),
    
    
    ('HP_RECOVER', "Recover HP", 'num'),
    ('HP_INCREASE', 'Increase MAX HP', 'num'),
    
]

def pickThree(powerUpList):
    numAbilities = len(powerUpList)
    picked = []
    for iteration in range(3):
        rand = random.randint(0, numAbilities-1)
        picked.append(powerUpList[rand])
    return picked

    


def getAbilitiesAndParameters():
    abilities = pickThree(easyPowerUps)

    result = []
    for ability in abilities:
        newAbilityList = []
        
        type = ability[0]
        description = ability[1]
        parameter = None
        incType = ability[2]

        if(type == ('BULLET_COOLDOWN')):
            parameter = -random.randint(3, 5)
        
        elif(type == ('BULLET_POWER_UP')):
            parameter = random.randint(2, 3)

        elif(type == ('DASH_DISTANCE')):
            parameter = 1
        
        elif(type == ('DASH_COOLDOWN')):
            parameter = -random.randint(5, 10)
        
        elif(type == ('HP_INCREASE')):
            parameter = 10
        else:
            #hp recovery
            parameter = random.randint(10, 35)
        
        newAbilityList.append(type)
        newAbilityList.append(description)
        newAbilityList.append(parameter)
        newAbilityList.append(incType)

        result.append(newAbilityList)

    return result






    


