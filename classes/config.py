
#basic config for the game(colors and chambercount)
COLORS = {

    'LEVEL1': {
        'offMap': '#817b69',
        'onMap': '#beb99c',
        'obstacle': '#dad3c5',
        'shadow': '#989898'
    },
    
    'LEVEL2':{
        'offMap': '#817b69',
        'onMap': '#329599',
        'obstacle': '#80d1e4',
        'shadow': '#2490A8'
    },

    'LEVEL3':{
        'offMap': '#817b69',
        'onMap': '#c57862',
        'obstacle': '#f79b80',
        'shadow': '#C0360C'
    },

    'lightpurple': '#C6B2E6',
    'lightorange': '#FFDD99',
    'purple': '#3e236e',
    'orange': '#ffa90a',
    'green': '#98fb98',
    'red': '#ff6961',
    'lightgray': '#e4e6eb',
    'mediumgray': '#a8a8a8',
    'darkgray': '#444444',
    'brightpurple': '#6e44ff',

    'enemyA': '#3a3b3c',
    'enemyB': '#242526',

    
    #repeated from lv1, but they are tech default colors so repetition whatever
    'offMap': '#817b69',
    'onMap': '#beb99c',
    'obstacle': '#dad3c5',
    

}

LEVEL_BY_CHAMBER_COUNT = {
    # # 0-6 chambers through lv 1
    # # 6-12 chambers through lv 2
    # # 12-21 chambers through lv 3
    # #21 total chambers
    1:0,
    2:6,
    3:12,
    'totalChambers': 21

}

