
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