from GUI import qt_classes as qt


class RoomEvents:
    def __init__(self, root, parent, *args, **kwargs):
        self.root = root
        self.parent = parent

    def push(self, args_in, *args, **kwargs):
        print('here')
        # PUsh is crashing the code currently saying direction is nonetype
        args_in_split = args_in.split(', ')
        check = args_in_split[0]
        direction = args_in_split[1]
        # Check if employed
        # THis part is broken, makes the screen clear
        # self.parent.commands.go(direction)
        self.parent.update_main('An office worker pushes you to the south because you are not employed by CapitalCorp.')