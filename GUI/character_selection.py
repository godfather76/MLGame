from GUI import character_creation as char_create
from GUI import main_widgets
from GUI import utility_classes as util
from GUI import qt_classes as qt
from SQL import db_utilities as dbutil


class CharSelectWidget(util.GroupBoxWidget):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, title='Character Selection', *args, **kwargs)
        # Before building anything, we'll check that there are characters associated with this user. If there
        # aren't, we'll let them know they need to create a new character
        chars = self.check_for_chars()
        #If characters exist, allow character selection
        if chars:
            # Main Label
            self.main_label = qt.Label(self.root,
                                       text='Character Selection',
                                       layout=self.gblayout)

            char_select_layout = qt.QtWidgets.QHBoxLayout()
            self.gblayout.addLayout(char_select_layout)
            # A dropdown with the user's characters in it.
            self.character_dropdown =  qt.ComboBox(self.root,
                                                   layout=char_select_layout,
                                                   alignment=qt.QtCore.Qt.AlignmentFlag.AlignCenter)
            go_btn = qt.PushButton(self.root,
                                   text='Go!',
                                   layout=char_select_layout,
                                   func=self.go_to_game)
            # Get our characters list and sort it alphabetically
            characters = sorted([x[0] for x  in self.check_for_chars()])
            # Add the list to the dropdown
            self.character_dropdown.addItems(characters)

            # Create new character button
            create_new_char_btn = qt.PushButton(self.root,
                                                text='Create New Character',
                                                layout=self.gblayout,
                                                func=self.go_to_char_create)


        # If there are no characters, let them know they need to create one.
        else:
            # Label informing them
            self.no_char_label = qt.Label(self.root,
                                          text='You don\'t have any characters. Create a new one to continue.',
                                          layout=self.gblayout)
            # Button to go to character creation
            self.create_char_btn = qt.PushButton(self.root,
                                                 text='Create New Character',
                                                 layout=self.gblayout,
                                                 func=self.go_to_char_create)

        # Button to go back to main
        self.back_btn = qt.PushButton(self.root,
                                      text='Back to Main Menu',
                                      layout=self.gblayout,
                                      func=self.back_to_main)
        self.show()

    @qt.QtCore.Slot()
    def back_to_main(self):
        if self.root.curr_user_id:
            self.root.curr_user_id = None
        # Load
        self.load_page(self.root.main_splash_widget,
                       main_widgets.MainSplashWidget)

    def check_for_chars(self):
        dbutil.check_chars_table(self.root.sql)
        where_dict = {'user_id': self.root.curr_user_id}
        res = self.root.sql.select('main', table='Characters', columns='charName', where=where_dict)
        if not res:
            return None
        else:
            return res

    def go_to_char_create(self):
        self.goto(self.root.char_create_widget,
                  char_create.CharCreateWidget)

    def go_to_game(self):
        char_name = self.character_dropdown.currentText()
        self.root.curr_char = self.root.sql.select('main',
                                                   table='Characters',
                                                   columns='char_id',
                                                   where={'charName': char_name})[0][0]
        print(f"Entering game as {char_name}")
