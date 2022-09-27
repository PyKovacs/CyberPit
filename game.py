import intro

if __name__ == '__main__':
    intro.starting_sequence()


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