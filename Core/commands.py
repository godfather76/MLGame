from tarfile import fully_trusted_filter

from GUI import qt_classes as qt
from Core import helpers


def arg_cruncher(args):
    if args == ('',):
        return False
    elif ', ' in args:
        this_split = args.split(', ')
        if this_split[0].isdigit():
            qty = int(this_split[0])
            del this_split[0]
        elif this_split[0] == 'all':
            qty = this_split[0]
            del this_split[0]
        else:
            qty = 1
        return qty, ' '.join(this_split)
    else:
        return 1, args


class CommandStructure:
    def __init__(self, root, main_game, *args, **kwargs):
        self.root = root
        self.main_game = main_game

    def test1(self, *args, **kwargs):
        self.main_game.update_main('test1 complete!')

    def testify(self, *args, **kwargs):
        self.main_game.update_main('testify complete!')

    def drop(self, *args, **kwargs):
        # parse user_in args
        qty, user_in = arg_cruncher(args[0])
        # if they didn't specify an item
        if not user_in:
            self.main_game.update_main('Drop what? You have to specify what item you would like to drop.')
            return
        # Get the bag type and contents of the bag (as a dictionary where {itemname: [qtys]
        bag_type, bag_contents_dict = helpers.get_bag_contents(self.root)
        item = helpers.possible_from_userin(self.main_game,
                                            qty,
                                            user_in,
                                            list(bag_contents_dict.keys()),
                                            source=bag_type)
        # If the item matches and isn't a list
        if item and not isinstance(item, list):
            # We need to check the number in the bag against quantity they asked to drop
            total_in_bag = sum(bag_contents_dict[item])
            # If qty is 'all'
            if qty == 'all':
                # Set qty to total_in bag
                qty = total_in_bag
            # If they aren't carrying as many as they asked to drop
            if total_in_bag < qty:
                # Tell them no and return
                self.main_game.update_main(f'You can\'t drop {str(qty)} {item}. There are only {str(total_in_bag)} '
                                           f'{item} in your {bag_type}.')
                return
            # Otherwise, we continue on by subtracting qty from the total in the bag.
            new_total_in_bag = total_in_bag - qty
            # Get stack size to pass into our new quantity parsing functions:
            stack_size = helpers.get_stack_size(self.root, item)
            # Now, we need to figure out new stacking.
            full_stacks_needed, overflow = helpers.stacker(new_total_in_bag, stack_size)
            # We set the bag_contents_dict[item] to a list that is full_stacks_needed number of stack_size
            # So if we need 3 full stacks and the stack size is 20, it will be [20, 20, 20]
            bag_contents_dict[item] = helpers.item_dict_entry_maker(stack_size, full_stacks_needed, overflow)
            helpers.update_bag_items(self.root, bag_contents_dict)

            # Now we need to add it to the room's items
            if item in self.main_game.room_items.keys():
                qty_in_rm = sum(self.main_game.room_items[item])
            else:
                qty_in_rm = 0
            new_total_in_rm = qty_in_rm + qty
            full_stacks_needed, overflow = helpers.stacker(new_total_in_rm, stack_size)
            self.main_game.room_items[item] = helpers.item_dict_entry_maker(stack_size, full_stacks_needed, overflow)
            helpers.update_room_items(self.root, self.main_game, item, new_total_in_rm, stack_size)
            self.main_game.refresh()
            self.main_game.update_main(f'You get {qty} {item} from your {bag_type} and drop it on the floor.')

    def get(self, *args, **kwargs):
        # Parse user_in
        qty, user_in = arg_cruncher(args[0])
        if not user_in:
            self.main_game.update_main('Get what? Type "get [item name]" to get something.')
            return
        # room contents are in self.main_game.room_items, and the item names are the keys
        item = helpers.possible_from_userin(self.main_game,
                                            qty,
                                            user_in,
                                            list(self.main_game.room_items.keys()),
                                            suppress_update=True)
        person = helpers.possible_from_userin(self.main_game,
                                              qty,
                                              user_in,
                                              self.main_game.people,
                                              suppress_update=True)
        # If it is an item, we ignore whether it might be a person, so we start with that
        if item and not isinstance(item, list):
            # We can just skip this tree, all we're doing is preventing the others and moving on
            pass
        # If it's neither an item nor a person, it's not there
        elif not person and not isinstance(item, list):
            # We'll tell the player it's not there
            self.main_game.update_main(f'Sorry, I don\'t see a {user_in} in this room.')
            return
        # If it's a person and not an item, tell the player how rude they're being. Sheesh.
        elif person and not isinstance(person, list):
            self.main_game.update_main(f'{person} is a whole ass person. You can\'t just go around picking people up, '
                                       f'it\'s terribly rude and is actually assault. That\'s illegal.')
            return
        elif isinstance(item, list):
            self.main_game.update_main(f'{user_in} could refer to multiple items in this room:')
            for i in item:
                self.main_game.update_main(f'{i}')
            return

        # See if the item is able to be picked up
        pickup = self.root.sql.select('main',
                                table='Items',
                                columns=['pickup', 'nopickup_reason'],
                                where={'itemName': item})[0]
        # pickup is either 0 (no) or 1 (yes). If it's zero:
        if not pickup[0]:
            # update nopickup_reason to the main screen then return
            self.main_game.update_main(f'{pickup[1]}')
            return
        # Now we'll check if the number requested exist in the room
        qty_in_room = sum(self.main_game.room_items[item])
        # Check if qty == 'all'
        if qty == 'all':
            # Set all to the number in the room
            qty = qty_in_room
        # If the qty is more than what's in the room
        if qty > qty_in_room:
            self.main_game.update_main(f'You can\'t pick up '
                                       f'{str(qty)} {helpers.get_name(self.root, item, qty)}. '
                                       f'There are only {str(qty_in_room)} {helpers.get_name(self.root, item, qty)} '
                                       f'in this room.')
            return
        # Since we know there are enough to be picked up, we need to check if there's room in the bag
        # get bag contents
        bag_type, bag_contents_dict = helpers.get_bag_contents(self.root)
        # Get the bag's max size from the DB
        bag_max = helpers.get_bag_size(self.root)
        # Get stack size from the DB
        stack_size = helpers.get_stack_size(self.root, item)
        # If the item is in the bag, we need to check stack size and see if the number being picked up will fit
        if item in bag_contents_dict.keys():
            new_total = sum(bag_contents_dict[item]) + qty
        else:
            bag_contents_dict[item] = []
            new_total = qty

        ## WORKING HERE ADDING CREDITS
        # Now, we need to figure out new stacking.
        if item == 'Credit' or item == 'Credits':
            helpers.add_credits(self.root, self.main_game, qty)
            return

        full_stacks_needed, overflow = helpers.stacker(new_total, stack_size)
        # We set the bag_contents_dict[item] to a list that is full_stacks_needed number of stack_size
        # So if we need 3 full stacks and the stack size is 20, it will be [20, 20, 20]
        bag_contents_dict[item] = helpers.item_dict_entry_maker(stack_size, full_stacks_needed, overflow)
        # Need to get total of slots taken now to check against bag_max
        total_slots_taken = 0
        for qty_list in bag_contents_dict.values():
            total_slots_taken += len(qty_list)

        if total_slots_taken > bag_max:
            self.main_game.update_main(f'You can\'t fit {qty} more {helpers.get_name(self.root, item, qty)}')
            return
        helpers.update_bag_items(self.root, bag_contents_dict)

        # Now we remove it from the room as well (We already know it's there and that there are enough of it)
        new_total_room = qty_in_room - qty
        helpers.update_room_items(self.root, self.main_game, item, new_total_room, stack_size)
        self.main_game.refresh()
        self.main_game.update_main(f'You pick up {str(qty)} {helpers.get_name(self.root, item, qty)} and put '
                                   f'{'it' if qty == 1 else 'them'} in your {bag_type}')



    @qt.QtCore.Slot()
    def inventory(self, *args, **kwargs):
        bag_type, bag_contents_dict = helpers.get_bag_contents(self.root)
        bag_size = helpers.get_bag_size(self.root)
        self.main_game.update_main(f'You open your {bag_type} and peer inside. You have:')
        i = 1
        for item, qty_list in bag_contents_dict.items():
            for qty in qty_list:
                stack_size = helpers.get_stack_size(self.root, item)
                self.main_game.update_main(f'{i}. {qty}/{stack_size} {helpers.get_name(self.root, item, qty)}')
                i += 1
        for x in range(i, bag_size+1):
            self.main_game.update_main(f'{x}. Empty')


    def look(self, *args, **kwargs):
        qty, user_in = arg_cruncher(args[0])
        if not user_in:
            self.main_game.update_main('Look at what? Type "look [item or person name]" to look at something.')
            return
        # First we'll try the contents of room, then if it's not there, we'll look in character's bag.
        # We suppress updates because we'll check the bag if there's nothing in the room that fits
        lookable = helpers.possible_from_userin(self.main_game,
                                                qty,
                                                user_in,
                                                self.main_game.lookables,
                                                suppress_update=True)
        # If lookable is a string, it is the one possible "lookable" user_in could refer to, so we get the desc
        if not lookable or isinstance(lookable, list):
            # Get bag type and the contents from db
            bag_type, bag_contents_dict = helpers.get_bag_contents(self.root)
            # Check if user_in could refer to anything in the bag.
            # This time we don't suppress updates, so it will let user know if there's nothing
            bag_lookable = helpers.possible_from_userin(self.main_game,
                                                        qty,
                                                        user_in,
                                                        list(bag_contents_dict.keys()),
                                                        suppress_update=True)
            # If there's something in the bag user_in could refer to:
            if bag_lookable and not isinstance(bag_lookable, list):
                desc = self.root.sql.select('main',
                                            table='Items',
                                            columns='itemDesc',
                                            where={'itemName': bag_lookable})[0][0]
                self.main_game.update_main(f'{desc}')
            elif isinstance(bag_lookable, list):
                if lookable:
                    all_possible = set(lookable + bag_lookable)
                    self.main_game.update_main(f'{user_in} could refer to multiple items between the room and your '
                                               f'{bag_type}.')
                    for item in all_possible:
                        self.main_game.update_main(f'{item}')
            else:
                self.main_game.update_main(f'There is no {user_in} in this room or in your {bag_type}')

        else:
            # If it's less that length of the room_items -1, that means it was in room_items
            if self.main_game.lookables.index(lookable) <= len(self.main_game.room_items) - 1:
                desc = self.root.sql.select('main',
                                     table='Items',
                                     columns='itemDesc',
                                     where={'itemName': lookable})[0][0]
            # more than that means it was in people
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
        qty, user_in = arg_cruncher(args[0])
        # If there are no args, they only typed "speak"
        if not user_in:
            # Let the user know
            self.main_game.update_main('Speak to whom? Currently you\'re just talking to yourself.')
        # person will either be the name of the only possibility from user_in or it will be False/None.
        person = helpers.possible_from_userin(self.main_game, qty, user_in, self.main_game.people)
        # If not False/None,
        if person and not isinstance(person, list):
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
        item = helpers.possible_from_userin(self.main_game, None, user_in, self.main_game.room_items)
        if not item or isinstance(item, list):
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
