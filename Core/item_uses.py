from GUI import qt_classes as qt

class ItemUses:
    def __init__(self, root, main_game, *args, **kwargs):
        self.root = root
        self.main_game = main_game

    def go_cap_intake(self, *args, **kwargs):
        self.root.sql.update('main',
                             table='Characters',
                             data={'capcorp_emp': 1},
                             where={'char_id': self.root.curr_char_id})
        self.main_game.commands.goto(51, 53, 1)
        self.main_game.update_main('You take a number and go sit down')
        self.main_game.update_main('After what seems like 83 years, a tired-looking Wolfperson employee comes out and '
                              'calls your number.')
        self.main_game.update_main('"Please follow me right this way to the aptitude test," they say in a gravelly '
                                   'voice. You follow them some way and up some stairs into a small office.')