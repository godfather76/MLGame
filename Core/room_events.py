from GUI import qt_classes as qt

class RoomEvents:
    def __init__(self, root, main_game, *args, **kwargs):
        self.root = root
        self.main_game = main_game

    def push(self, args_in, *args, **kwargs):
        # PUsh is crashing the code currently saying direction is nonetype
        args_in_split = args_in.split(', ')
        check = args_in_split[0]
        direction = args_in_split[1]
        msg = ''
        if check == 'not_employed':
            emp = self.root.sql.select('main',
                                       table='Characters',
                                       columns='capcorp_emp',
                                       where={'char_id': self.root.curr_char_id})[0][0]
            if emp:
                return
            else:
                msg = (f'The Security Bot 3000 pushes you {direction}, back in to the lobby.\n'
                       f'"You\'ll need to wait your turn! Please look at the sign.')
        self.root.sql.update('main',
                             table='Characters',
                             data={'capcorp_emp': 1},
                             where={'char_id': self.root.curr_char_id})
        self.main_game.commands.go(direction)
        self.main_game.update_main(msg)
