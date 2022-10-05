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
