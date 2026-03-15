
def get_bag_contents(root, main_game, *args, **kwargs):
    raw_contents = root.sql.select('main',
                                   table='Inventories',
                                   columns='bagContents',
                                   where={'char_id': root.curr_char_id})[0][0]
    if not raw_contents:
        return None
    else:
        # Items are separated by '; ' so we split
        contents_list = raw_contents.split('; ')
        # FOr each string in the split, we split by ' ' so any items with more than 1 will give us [[#], [item]]
        contents_list = [x.split(' ') for x in contents_list]
        # Loop through and enumerate
        for i, item in enumerate(contents_list):
            # If index 0 is not a digit, insert 1 at index 0
            if not item[0].isdigit():
                contents_list[i].insert(0, 1)
            else:
                # Otherwise make the digit an int
                contents_list[i][0] = int(item[0])
            # Join the rest of the list back togwther as index 1 and delete what's after that
            contents_list[i][1] = ' '.join(item[1:])
            del contents_list[i][2:]
        # Return our new list
        return contents_list

def inventory_entry_maker(bag_contents, *args, **kwargs):
    # Loop through bag contents
    for i, item in enumerate(bag_contents):
        # if the first element is 1, delete it
        if item[0] == 1:
            del item[0]
        # Otherwise join index 0 and index 1
        else:
            ' '.join(item)


def possible_from_userin(main_game, user_in, full_list):
    possible = [x for x in full_list if x.lower().strip().startswith(user_in) or user_in in x.lower().strip()]
    # If nothing startswith user in
    if len(possible) == 0:
        # Split each into its separate words
        split_list = [x.split(' ') for x in full_list]
        # Loop through with enumerate
        for i, list in enumerate(split_list):
            # Make everything lowercase
            this_list = [x.lower() for x in list]
            # If user in is one of the words, add it the full_list version to our possible matches
            if user_in in this_list:
                possible.append(full_list[i])
            # otherwise, we'll see if any of the words start with user_in
            else:
                for word in this_list:
                    if word.lower().startswith(user_in):
                        possible.append(full_list[i])

    if len(possible) == 0:
        main_game.update_main(f'I\'m sorry, I don\'t see a {user_in} in this room.')
        return None
    elif len(possible) == 1:
        return possible[0]
    else:
        main_game.update_main(f'{user_in} could refer to:')
        for item in possible:
            main_game.update_main(f'{item}')
        return None