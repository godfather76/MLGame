from GUI import qt_classes as qt
from Core import command_helpers as helpers


def arg_cruncher(args):
    if args == ('',):
        return False
    elif ', ' in args:
        return ' '.join(args.split(', '))
    else:
        return args


class CommandStructure:
    def __init__(self, root, main_game, *args, **kwargs):
        self.root = root
        self.main_game = main_game

    def test1(self, *args, **kwargs):
        self.main_game.update_main('test1 complete!')

    def testify(self, *args, **kwargs):
        self.main_game.update_main('testify complete!')

    @qt.QtCore.Slot()
    def inventory(self, *args, **kwargs):
        self.main_game.update_main('Opening Inventory...')

    def look(self, *args, **kwargs):
        user_in = arg_cruncher(args[0])
        if not user_in:
            self.main_game.update_main('Look at what? Type "look [item or person name]" to look at something.')
            return
        lookable = helpers.possible_from_userin(self.main_game, user_in, self.main_game.lookables)
        # If lookable is a string, it is the one possible "lookable" user_in could refer to, so we get the desc
        if not lookable:
            return
        else:
            # Easiest way to deal with this is to try except and do the other table because lookables comes from two
            # tables
            if self.main_game.lookables.index(lookable) <= len(self.main_game.items) - 1:
                desc = self.root.sql.select('main',
                                     table='Items',
                                     columns='itemDesc',
                                     where={'itemName': lookable})[0][0]
            else:
                desc = self.root.sql.select('main',
                                            table='NPCs',
                                            columns='npcDesc',
                                            where={'npcName': lookable})[0][0]
            self.main_game.update_main(f'{desc}')


    @qt.QtCore.Slot()
    def skills(self, *args, **kwargs):
        self.main_game.update_main('Showing Skills information')

    def speak(self, *args, **kwargs):
        # crunch the args into a single string
        user_in = arg_cruncher(args[0])
        # If there are no args, they only typed "speak"
        if not user_in:
            # Let the user know
            self.main_game.update_main('Speak to whom? Currently you\'re just talking to yourself.')
        # person will either be the name of the only possibility from user_in or it will be False/None.
        person = helpers.possible_from_userin(self.main_game, user_in, self.main_game.people)
        # If not False/None,
        if person:
            # Select the conversation column from db where npcName is the person in the room indicated by user_in
            conversation = self.root.sql.select('main',
                                                table='NPCs',
                                                columns='conversation',
                                                where={'npcName': person})[0][0]
            # If this is empty, there is no conversation associated with this NPC.
            if not conversation:
                self.main_game.update_main('They don\'t seem to want to speak to you.')
            else:
                # Otherwise, we now have the name of our conversation in self.root.conversations class
                # Set the root var to the conversation from the db
                self.root.active_conversation = conversation
                # LOad the conversation widget
                self.main_game.goto_conversation()

    @qt.QtCore.Slot()
    def status(self, *args, **kwargs):
        self.main_game.update_main('Showing Status information')

    def use(self, *args, **kwargs):
        user_in = arg_cruncher(args[0])
        if not user_in:
            self.main_game.update_main('Use what? You must specify what item you want to use by '
                                       'typing "use [item name]"')
        item = helpers.possible_from_userin(self.main_game, user_in, self.main_game.items)
        if not item:
            return
        item_use = self.root.sql.select('main',
                                        table='Items',
                                        columns='itemUse',
                                        where={'itemName': item})[0][0]
        getattr(self.main_game.item_uses, item_use, None)()

    # Direction commands all at the bottom to be grouped together for ease.
    def go(self, direction, *args, **kwargs):
        aliases = {'nw': 'northwest',
                   'n': 'north',
                   'ne': 'northeast',
                   'w': 'west',
                   'e': 'east',
                   'sw': 'southwest',
                   's': 'south',
                   'se': 'southeast',
                   'u': 'up',
                   'd': 'down',}
        # If the direction is an alias, make the direction the actual direction
        if direction in aliases.keys():
            direction = aliases[direction]
        if direction not in self.main_game.exits:
            self.main_game.update_main(f'There is no exit going {direction}')
        else:
            x = 0
            y = 0
            z = 0
            if direction == 'northwest':
                x = -1
                y = 1
            elif direction == 'north':
                y = 1
            elif direction == 'northeast':
                x = 1
                y = 1
            elif direction == 'west':
                x = -1
            elif direction == 'east':
                 x = 1
            elif direction == 'southwest':
                x = -1
                y = -1
            elif direction == 'south':
                y = -1
            elif direction == 'southeast':
                x = 1
                y = -1
            elif direction == 'up':
                z = 1
            elif direction == 'down':
                z = -1

            self.goto(self.main_game.X + x, self.main_game.Y + y, self.main_game.Z + z)

        qt.QtCore.QTimer.singleShot(0, self.main_game.entry_box.setFocus)

    def goto(self, X, Y, Z, *args, **kwargs):
        res = self.root.sql.update('main',
                                   table='Characters',
                                   data={'X': X,
                                         'Y': Y,
                                         'Z': Z},
                                   where=f'char_id={self.root.curr_char_id}')
        self.main_game.refresh()

    def northeast(self, *args, **kwargs):
        self.go('northeast')

    def ne(self, *args, **kwargs):
        self.go('northeast')

    def north(self, *args, **kwargs):
        self.go('north')

    def n(self, *args, **kwargs):
        self.go('north')

    def northwest(self, *args, **kwargs):
        self.go('northwest')

    def nw(self, *args, **kwargs):
        self.go('northwest')

    def west(self, *args, **kwargs):
        self.go('west')

    def w(self, *args, **kwargs):
        self.go('west')

    def east(self, *args, **kwargs):
        self.go('east')

    def e(self, *args, **kwargs):
        self.go('east')

    def southwest(self, *args, **kwargs):
        self.go('southwest')

    def sw(self, *args, **kwargs):
        self.go('southwest')

    def south(self, *args, **kwargs):
        self.go('south')

    def s(self, *args, **kwargs):
        self.go('south')

    def southeast(self, *args, **kwargs):
        self.go('southeast')

    def se(self, *args, **kwargs):
        self.go('southeast')

    def up(self, *args, **kwargs):
        self.go('up')

    def u(self, *args, **kwargs):
        self.go('up')

    def down(self, *args, **kwargs):
        self.go('down')

    def d(self, *args, **kwargs):
        self.go('down')
