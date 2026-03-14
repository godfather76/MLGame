from GUI import qt_classes as qt

class CommandStructure:
    def __init__(self, root, parent):
        self.root = root
        self.parent = parent

    def test1(self, *args, **kwargs):
        self.parent.update_main('test1 complete!')

    def testify(self, *args, **kwargs):
        self.parent.update_main('testify complete!')

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
        if direction not in self.parent.exits:
            self.parent.update_main(f'There is no exit going {direction}')
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
            res = self.root.sql.update('main',
                                 table='Characters',
                                 data={'X': self.parent.X + x,
                                       'Y': self.parent.Y + y,
                                       'Z': self.parent.Z + z},
                                 where=f'char_id={self.root.curr_char_id}')

            self.parent.refresh()

    @qt.QtCore.Slot()
    def inventory(self, *args, **kwargs):
        self.parent.update_main('Opening Inventory...')

    @qt.QtCore.Slot()
    def skills(self, *args, **kwargs):
        self.parent.update_main('Showing Skills information')

    @qt.QtCore.Slot()
    def status(self, *args, **kwargs):
        self.parent.update_main('Showing Status information')

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
