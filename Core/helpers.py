from GUI import qt_classes as qt


def db_write_string_maker(item_data, *args, **kwargs):
    # If item_data is a dictionary, we will append its contents to a list
    if isinstance(item_data, dict):
        item_list = []
        # Loop through the itemnames that are keys
        for item in item_data.keys():
            # For each qty, make an entry
            for qty in item_data[item]:
                if qty == 1:
                    item_list.append(f'{item}')
                else:
                    item_list.append(f'{qty} {item}')
        # make it so item_data is now our list that we made
        item_data = item_list.copy()
        # Now delete the temporary list
        del item_list

    return '; '.join(item_data)


@qt.QtCore.Slot()
def change_reputation(root, conv_window, conversation, amount, text):
    for btn in conversation.response_dict[conversation.reputation]['buttons']:
        btn.hide()
    try:
        conversation.reputation += amount
    except TypeError:
        end_conversation(root, conv_window, conversation)
        return
    # self.conv_window.main_window.clear()
    conv_window.update_main(text)
    conv_window.update_main(conversation.response_dict[conversation.reputation]['text'])
    conversation_button_builder(root, conv_window, conversation)

def conversation_had_check(root, conv_window, conversation, *args, **kwargs):
    res = root.sql.select('main',
                          table='ConversationsHad',
                          where={'char_id': root.curr_char_id,
                                 'convName': conversation.current_conversation},
                          where_and=True)
    if res:
        conv_window.update_main('You have already spoken with this person.')
        return True
    return False

def conversation_button_builder(root, conv_window, conversation, *args, **kwargs):
    for btn_info in conversation.response_dict[conversation.reputation]['button_info']:
        text, rep = btn_info
        btn = qt.PushButton(root,
                            text=text,
                            layout=conv_window.button_container,
                            func=lambda event, r=root, w=conv_window,
                                        c=conversation, x=rep, y=text: change_reputation(r, w, c, x, y))
        conversation.response_dict[conversation.reputation]['buttons'].append(btn)

def create_response_dict(root, conversation, *args, **kwargs):
    # Get info for this conversation from the db.
    res = root.sql.select('main',
                          table='Conversations',
                          where={'conversationName': conversation.current_conversation})
    # Get the column names from the db
    col_names= root.sql.column_names('main',
                                     table='Conversations')

    res_dict_list = [{x: y for x, y in zip(col_names, res[i])} for i in range(len(res))]
    response_dict = {response['keyNumber']: {'text': response['text'],
                                            'button_info': [(response[f'button{i}_text'],
                                                             response[f'button{i}_value']) for i in range(1, 5)
                                                            if response[f'button{i}_text']],
                                            'buttons': []} for response in res_dict_list}
    return response_dict

def display_string_maker(root, item_data, *args, **kwargs):
    # If item_data is a dictionary, we will append its contents to a list
    if isinstance(item_data, dict):
        item_list = []
        # Loop through the itemnames that are keys
        for item in item_data.keys():
            # For each qty, make an entry
            qty = sum(item_data[item])
            if qty == 1:
                item_list.append(f'{get_name(root, item, qty)}')
            else:
                item_list.append(f'{qty} {get_name(root, item, qty)}')
        # make it so item_data is now our list that we made
        item_data = item_list.copy()
        # Now delete the temporary list
        del item_list


    # This means no result, so return None
    if not item_data or item_data == ['']:
        return 'None'
    if len(item_data) == 1:
        return item_data[0]
    elif len(item_data) == 2:
        return f'{item_data[0]} and {item_data[1]}'
    else:
        return f'{', '.join(item_data[:-1])}, and {item_data[-1]}'

def end_conversation(root, conv_window, conversation, *args, **kwargs):
    root.sql.insert('main',
                    table='ConversationsHad',
                    data={'convName': conversation.current_conversation,
                          'char_id': root.curr_char_id})
    conv_window.go_to_game()


def get_bag_contents(root, *args, **kwargs):
    res = root.sql.select('main',
                               table='Inventories',
                               columns=['bagContents', 'bagType'],
                               where={'char_id': root.curr_char_id})[0]
    return res[1], item_dict_maker(root, res[0])


def get_indef_article(item, *args, **kwargs):
    # If I'm spending a bunch of time putting plurals in (which I was), I'm dealing with indefinite articles too
    # Blame the English language. Or just the English. That works too.
    if item[0].lower() in ['a', 'e', 'i', 'o', 'u']:
        return 'an'
    else:
        return 'a'


def get_bag_size(root, *args, **kwargs):
    return root.sql.select('main',
                               table='Inventories',
                               columns='bagMax',
                               where={'char_id': root.curr_char_id})[0][0]


def get_name(root, item, qty,  *args, **kwargs):
    # If qty is 1, get the indefinite article and return "a/an [item name]"
    # If qty is not 1, return the plural
    return f'{get_indef_article(item)} {item}' if qty == 1 else get_plural(root, item)

def get_plural(root, item, *args, **kwargs):
    # This try except just says if we don't find what we're looking for, it's already plural
    # We're essentially plugging the plural into the where clause so it's false.
    # We just return item back
    # This is just so we can easily say "find me the plural" and if it already is, it won't break
    try:
        return root.sql.select('main',
                               table='Items',
                               columns='itemNamePlural',
                               where={'itemName': item})[0][0]
    except IndexError:
        return item


def get_singular(root, item, *args, **kwargs):
    # Same as for get_plural, we'll try except block so if we ask for the singular and it's already
    # singular, it will just return the singular back and not break down.
    try:
        return root.sql.select('main',
                                   table='Items',
                                   columns='itemName',
                                   where={'itemNamePlural': item})[0][0]
    except IndexError:
        return item


def get_stack_size(root, item, *args, **kwargs):
    stack_size = root.sql.select('main',
                                 table='Items',
                                 columns='stackSize',
                                 where={'itemName': item})[0][0]
    return stack_size


def item_dict_entry_maker(stack_size, full_stacks_needed, overflow, *args, **kwargs):
    # We set the bag_contents_dict[item] to a list that is full_stacks_needed number of stack_size
    # So if we need 3 full stacks and the stack size is 20, it will be [20, 20, 20]
    this_list = [stack_size for x in range(full_stacks_needed)]
    # Then if there is overflow, we add it to the end of the list of qtys
    if overflow:
        this_list.append(overflow)
    return this_list


def item_dict_maker(root, item_str, *args, **kwargs):
    item_dict = {}
    # Loop through each of the items in the list
    for item in item_str.split('; '):
        # Split the word by space so we get a list of the words/quantities
        this_split = item.split(' ')
        # if index 0 is a number, we make it the quantity, otherwise we make the quantity 1
        qty = 1
        if this_split[0].isdigit():
            qty = int(this_split[0])
            del this_split[0]
            item = ' '.join(this_split)
        # Get the item's plural name from the db
        item_plural = get_plural(root, item)
        # If item_plural is the same as item, it was already plural, so we need to get the singular
        if item_plural == item:
            item = get_singular(root, item_plural)
        if item in item_dict.keys():
            item_dict[item].append(qty)
        else:
            item_dict[item] = [qty]
    return item_dict


def possible_from_userin(main_game, user_in, full_list, suppress_update=False, source='this room'):
    qty, user_in = user_in
    if isinstance(full_list, dict):
        full_list = list(full_list.keys())
    possible = [x for x in full_list if x.lower().strip().startswith(user_in)]
    # If nothing startswith user in
    if len(possible) == 0:
        # Split each into its separate words
        split_list = [x.split(' ') for x in full_list]
        # Loop through with enumerate
        for i, l in enumerate(split_list):
            # Make everything lowercase
            this_list = [x.lower() for x in l]
            # If user in is one of the words, add it the full_list version to our possible matches
            if user_in in this_list:
                possible.append(full_list[i])
            # otherwise, we'll see if any of the words start with user_in
            else:
                for word in this_list:
                    if word.lower().startswith(user_in):
                        possible.append(full_list[i])
    if len(possible) == 0:
        if not suppress_update:
            main_game.update_main(f'I\'m sorry, I don\'t see a {user_in} in {source}.')
        return None
    elif len(possible) == 1:
        return possible[0]
    else:
        if not suppress_update:
            main_game.update_main(f'{user_in} could refer to:')
            for item in possible:
                main_game.update_main(f'{item}')
        return possible


def stacker(new_total, stack_size):
    # Full stacks needed is new total integer divided by stack size
    full_stacks_needed = (new_total // stack_size)
    # Overflow is whatever is left over after those full stacks
    overflow = new_total - (full_stacks_needed * stack_size)

    return full_stacks_needed, overflow


def update_bag_items(root, bag_contents_dict, *args, **kwargs):
    write_str = db_write_string_maker(bag_contents_dict)
    # Write to db
    root.sql.update('main',
                         table='Inventories',
                         data={'bagContents': write_str},
                         where={'char_id': root.curr_char_id})


def update_room_items(root, main_game, item, new_total, stack_size, *args, **kwargs):
    full_stacks_room, overflow_room = stacker(new_total, stack_size)
    main_game.room_items[item] = item_dict_entry_maker(stack_size, full_stacks_room, overflow_room)
    write_str_room = db_write_string_maker(main_game.room_items)
    # Write to db
    root.sql.update('main',
                         table='Locations',
                         data={'items': write_str_room},
                         where={'X': main_game.X,
                                'Y': main_game.Y,
                                'Z': main_game.Z})
