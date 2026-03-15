from GUI import main_widgets
from GUI import utility_classes as util
from GUI import qt_classes as qt
from SQL import db_utilities as dbutil
from GUI import game_main


class CharCreateWidget(util.GroupBoxWidget):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, title='Character Creation', *args, **kwargs)
        main_label = qt.Label(self.root,
                                   text='Character Creation',
                                   layout=self.gblayout)
        # Horizontal layout for name entry box (qlineedit) and species (qcombobox)
        name_species_layout = qt.QtWidgets.QHBoxLayout()
        # Add the layout to our original box layout
        self.gblayout.addLayout(name_species_layout)
        # Label for name
        name_label = qt.Label(self.root,
                                   text='Name:',
                                   layout=name_species_layout)
        # Qlineedit for name
        self.name_entry = qt.LineEdit(self.root,
                                      layout=name_species_layout)

        # A label to say that the combobox is for species
        species_label = qt.Label(self.root,
                                      text='Species:',
                                      layout=name_species_layout)
        # # Left align
        # self.species_label.setAlignment(qt.QtCore.Qt.AlignmentFlag.AlignLeft)
        # A dropdown menu (qcombobox) for our species
        self.species_dropdown = qt.ComboBox(self.root,
                                            layout=name_species_layout)

        # get names of species from the db and sort their names alphabetically
        species_names = sorted([x[0] for x in self.root.sql.select('main', table='Species', columns='speciesName')])
        # Add our sorted list of species to the dropdown
        self.species_dropdown.addItems(species_names)

        # Age will be a spinbox with a minimum of 13 and maximum of 500
        # Profession will be a dropdown using valus from the Professions table of the db
        # Layout for age and profession
        age_prof_layout = qt.QtWidgets.QHBoxLayout()
        self.gblayout.addLayout(age_prof_layout)
        age_label = qt.Label(self.root,
                             text='Age:',
                             layout=age_prof_layout,
                             alignment=qt.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.age_spin = qt.SpinBox(self.root,
                                   layout=age_prof_layout,
                                   minimum=13,
                                   maximum=500,
                                   value=25,
                                   alignment=qt.QtCore.Qt.AlignmentFlag.AlignLeft)

        # A label for profession
        profession_label = qt.Label(self.root,
                                    text='Profession:',
                                    layout=age_prof_layout)
        # Profession dropdown (QComboBox)
        self.profession_dropdown = qt.ComboBox(self.root,
                                               layout=age_prof_layout)
        professions = sorted([x[0] for x in self.root.sql.select('main',
                                                                 table='Professions',
                                                                 columns='professionName')])
        self.profession_dropdown.addItems(professions)

        # A label letting the player know that 20 is the highest a stat can go during character creation
        max_score_label = qt.Label(self.root,
                                   text='The highest possible score for any one stat during character creation\n'
                                        'is 20. The lowest possible score for any one stat during character\n'
                                        'creation is 8.',
                                   layout=self.gblayout,
                                   alignment=qt.QtCore.Qt.AlignmentFlag.AlignLeft)
        # Layout for a row showing how many points are remaining to be spent.
        points_remain_layout = qt.QtWidgets.QHBoxLayout()
        self.gblayout.addLayout(points_remain_layout)
        # Label for points remaining
        points_remain_label = qt.Label(self.root,
                                       text='Points Remaining:',
                                       layout=points_remain_layout,
                                       alignment=qt.QtCore.Qt.AlignmentFlag.AlignLeft)
        # This label will serve as our point tracker
        self.points_remain = qt.Label(self.root,
                                      text='20',
                                      layout=points_remain_layout,
                                      alignment=qt.QtCore.Qt.AlignmentFlag.AlignLeft)
        # We will create three separate horizontal boxes, one for each pair of attributes
        # Muscle, Speed, Toughness, Booksmarts, Streetsmarts, Appeal
        # Layout for Muscle
        mus_layout = qt.QtWidgets.QHBoxLayout()
        self.gblayout.addLayout(mus_layout)
        # Label
        self.muscle_label = qt.Label(self.root,
                                     text='Muscle:',
                                     layout=mus_layout)
        # Minus button
        self.mus_minus_btn = qt.PushButton(self.root,
                                           text='-',
                                           layout=mus_layout,
                                           func=self.mus_sub)
        # Actual number label
        self.mus_num_label = qt.Label(self.root,
                                      text='10',
                                      layout=mus_layout)
        # plus button
        self.mus_plus_btn = qt.PushButton(self.root,
                                          text='+',
                                          layout=mus_layout,
                                          func=self.mus_add)

        # Layout for Speed
        speed_layout = qt.QtWidgets.QHBoxLayout()
        self.gblayout.addLayout(speed_layout)
        # Label
        speed_label = qt.Label(self.root,
                                    text='Speed:',
                                    layout=speed_layout)
        # Minus button
        self.speed_minus_btn = qt.PushButton(self.root,
                                             text='-',
                                             layout=speed_layout,
                                             func=self.speed_sub)
        # Actual number label
        self.speed_num_label = qt.Label(self.root,
                                        text='10',
                                        layout=speed_layout)
        # plus button
        self.speed_plus_btn = qt.PushButton(self.root,
                                            text='+',
                                            layout=speed_layout,
                                            func=self.speed_add)

        # Layout for toughness
        tough_layout = qt.QtWidgets.QHBoxLayout()
        self.gblayout.addLayout(tough_layout)
        # Label
        toughness_label = qt.Label(self.root,
                                        text='Toughness:',
                                        layout=tough_layout)
        # Minus button
        self.tough_minus_btn = qt.PushButton(self.root,
                                             text='-',
                                             layout=tough_layout,
                                             func=self.tough_sub)
        # Actual number label
        self.tough_num_label = qt.Label(self.root,
                                        text='10',
                                        layout=tough_layout)
        # plus button
        self.tough_plus_btn = qt.PushButton(self.root,
                                            text='+',
                                            layout=tough_layout,
                                            func=self.tough_add)

        # Layout for Booksmarts
        book_layout = qt.QtWidgets.QHBoxLayout()
        self.gblayout.addLayout(book_layout)
        # Label
        booksmarts_label = qt.Label(self.root,
                                     text='Booksmarts:',
                                     layout=book_layout)
        # Minus button
        self.book_minus_btn = qt.PushButton(self.root,
                                           text='-',
                                           layout=book_layout,
                                           func=self.book_sub)
        # Actual number label
        self.book_num_label = qt.Label(self.root,
                                      text='10',
                                      layout=book_layout)
        # plus button
        self.book_plus_btn = qt.PushButton(self.root,
                                          text='+',
                                          layout=book_layout,
                                          func=self.book_add)

        # Layout for streetsmarts
        street_layout = qt.QtWidgets.QHBoxLayout()
        self.gblayout.addLayout(street_layout)
        # Label
        streetsmarts_label = qt.Label(self.root,
                                    text='Streetsmarts:',
                                    layout=street_layout)
        # Minus button
        self.street_minus_btn = qt.PushButton(self.root,
                                             text='-',
                                             layout=street_layout,
                                             func=self.street_sub)
        # Actual number label
        self.street_num_label = qt.Label(self.root,
                                        text='10',
                                        layout=street_layout)
        # plus button
        self.street_plus_btn = qt.PushButton(self.root,
                                            text='+',
                                            layout=street_layout,
                                            func=self.street_add)

        # Layout for Appeal
        app_layout = qt.QtWidgets.QHBoxLayout()
        self.gblayout.addLayout(app_layout)
        # Label
        appeal_label = qt.Label(self.root,
                                           text='Appeal:',
                                           layout=app_layout)
        # Minus button
        self.app_minus_btn = qt.PushButton(self.root,
                                            text='-',
                                              layout=app_layout,
                                              func=self.app_sub)
        # Actual number label
        self.app_num_label = qt.Label(self.root,
                                         text='10',
                                         layout=app_layout)
        # plus button
        self.app_plus_btn = qt.PushButton(self.root,
                                             text='+',
                                             layout=app_layout,
                                             func=self.app_add)

        # Button to kick off new user creation
        self.create_btn = qt.PushButton(self.root,
                                        text='Create!',
                                        layout=self.gblayout,
                                        func=self.create_new_char)
        # Button to go back to login
        self.back_btn = qt.PushButton(self.root,
                                      text='Back to Main Menu',
                                      layout=self.gblayout,
                                      func=self.back_to_main)
        self.show()

    @qt.QtCore.Slot()
    def back_to_main(self):
        if self.root.curr_user_id:
            self.root.curr_user_id = None
        self.goto(self.root.main_splash_widget,
                       main_widgets.MainSplashWidget)

    def go_to_game(self):
        self.goto(self.root.main_game_widget,
                  game_main.MainGameWidget)

    @qt.QtCore.Slot()
    def create_new_char(self):
        name = self.name_entry.text()
        species = self.species_dropdown.currentText()
        age = self.age_spin.value()
        points_remain = int(self.points_remain.text())
        profession = self.profession_dropdown.currentText()
        muscle = int(self.mus_num_label.text())
        speed = int(self.speed_num_label.text())
        toughness = int(self.tough_num_label.text())
        booksmarts = int(self.book_num_label.text())
        streetsmarts = int(self.street_num_label.text())
        appeal = int(self.app_num_label.text())

        # If name is empty, pop error
        if not name:
            qt.QtWidgets.QMessageBox.warning(self.root,
                                             'Error',
                                             'Name is required')
            return
        # If points_remain is 0 do nothing.
        if points_remain:
            qt.QtWidgets.QMessageBox.warning(self.root,
                                             'Error',
                                             'You still have attribute points to spend.')
            return
        # If name is used, pop error
        res = self.root.sql.select('main',
                                   table='characters',
                                   columns='charName',
                                   where=f'lower(charName)=lower("{name}")')
        if not res:
            insert = self.root.sql.insert('main',
                                 table='characters',
                                 data={'user_id': self.root.curr_user_id,
                                       'charName': name,
                                       'species': species,
                                       'age': age,
                                       'profession': profession,
                                       'muscle': muscle,
                                       'speed': speed,
                                       'toughness': toughness,
                                       'booksmarts': booksmarts,
                                       'streetsmarts': streetsmarts,
                                       'appeal': appeal})
            inv_insert = self.root.sql.insert('main',
                                              table='Inventories',
                                              data={'char_id': self.root.curr_char_id})
            # If insert returned False, there is an issue
            if not insert:
                # Pop error
                qt.QtWidgets.QMessageBox.warning(self.root,
                                                 'Database Error',
                                                 'Something went wrong with entering your new character into '
                                                 'the database. You may need to reinstall the game.')
                return
            # Otherwise, we'll get the char_id from the db, store char_id and name, and load the main game screen
            this_char = self.root.sql.select('main',
                                           table='characters',
                                           columns=['char_id', 'charName'],
                                           where=f'charName="{name}"')

            self.root.curr_char_id = this_char[0][0]
            self.root.curr_char_name = this_char[0][1]
            self.go_to_game()
        else:
            qt.QtWidgets.QMessageBox.warning(self.root,
                                             'Error',
                                             'That name is already taken. Please choose another one.')
            return



    def check_remaining(self):
        # Will just return the number, so if it's 0, if self.check_stock will be False
        return int(self.points_remain.text())

    def add(self, label):
        curr = int(label.text())
        if self.check_remaining() and curr < 20:
            label.setText(f'{str(curr + 1)}')
            self.sub_from_remaining()

    def sub(self, label):
        curr = int(label.text())
        if curr > 8:
            label.setText(f'{str(curr - 1)}')
            self.add_to_remaining()

    def add_to_remaining(self):
        self.points_remain.setText(f'{str(int(self.points_remain.text()) + 1)}')

    def sub_from_remaining(self):
        self.points_remain.setText(f'{str(int(self.points_remain.text()) - 1)}')

    @qt.QtCore.Slot()
    def mus_add(self):
        self.add(self.mus_num_label)

    @qt.QtCore.Slot()
    def mus_sub(self):
        self.sub(self.mus_num_label)

    @qt.QtCore.Slot()
    def book_add(self):
        self.add(self.book_num_label)

    @qt.QtCore.Slot()
    def book_sub(self):
        self.sub(self.book_num_label)

    @qt.QtCore.Slot()
    def speed_add(self):
        self.add(self.speed_num_label)

    @qt.QtCore.Slot()
    def speed_sub(self):
        self.sub(self.speed_num_label)

    @qt.QtCore.Slot()
    def street_add(self):
        self.add(self.street_num_label)

    @qt.QtCore.Slot()
    def street_sub(self):
        self.sub(self.street_num_label)

    @qt.QtCore.Slot()
    def tough_add(self):
        self.add(self.tough_num_label)

    @qt.QtCore.Slot()
    def tough_sub(self):
        self.sub(self.tough_num_label)

    @qt.QtCore.Slot()
    def app_add(self):
        self.add(self.app_num_label)

    @qt.QtCore.Slot()
    def app_sub(self):
        self.sub(self.app_num_label)
