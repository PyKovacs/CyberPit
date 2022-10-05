import intro
from users import UserHandler
from db import DBHandler

if __name__ == '__main__':
    user_handler = UserHandler(DBHandler())
    user = intro.starting_sequence(user_handler)
    while True:
        action = input('If you wish to buy a new robot, type "shop".\n'
                     'Note - new robot will replace the current one.\n'
                     'If you are happy with your current robot, type "continue":\n')
        if action == 'shop':
            user.purchase_robot()
            break
        if action == 'continue':
            break


'''
print('Robot builds available:\n')
print(base.RobotBuilds.showcase())

buildname = ''
while buildname.capitalize() not in base.RobotBuilds.all_build_names:
    buildname = input('Choose your robot build:\n'+f'{base.RobotBuilds.all_build_names}\n') # TODO dorobit legendu
buildclass = base.RobotBuilds.get_buildclass_from_buildname(buildname.upper())

name = str(input('Good choice! Now name your machine:\n'))
while not name:
    name = input('Name your robot:\n')

player_robot = buildclass(name)
base.clear_console()

print('You have {} credits on your account, let\'s buy some weapons!'.format(player_robot.money))

print('Weapons available:\n')
print(base.Weapons.showcase())

print('This is your robot:\n\n' +
      '*********************\n' +
      name.upper(), '\n',
      base.RobotBuilds.showcase([buildclass]))

'''