import bcrypt
from GUI import character_creation as char_create
from GUI import character_selection as char_select
from GUI import main_widgets
from GUI import utility_classes as util
from GUI import qt_classes as qt


class LoginWidget(util.GroupBoxWidget):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, title='Login', *args, **kwargs)
        self.main_label = qt.Label(self.root,
                                   text='Login',
                                   layout=self.gblayout)
        self.username_entry = qt.LineEdit(self.root,
                                          placeholderText='Enter username here',
                                          layout=self.gblayout)
        # add an entry box for password
        self.password_entry = qt.LineEdit(self.root,
                                          placeholderText='Enter password here',
                                          layout=self.gblayout,
                                          echoMode=qt.LineEdit.EchoMode.Password)
        # Button to kick off login
        self.login_btn = qt.PushButton(self.root,
                                        text='Log in!',
                                        layout=self.gblayout,
                                        func=self.login)
        # Butto nto go back to login
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

    @qt.QtCore.Slot()
    def login(self):
        # we're not stripping for this because we're actually just going to have one error message that doesn't
        # say much more than that there was a problem. As such, we will set a flag and at the end, if the flag is true,
        # we'll pop the error
        pop_error = False
        # This is a general safety design choice even though the game is meant to be played locally
        # bring in the entered username from the entry box
        username_entered = self.username_entry.text()
        # bring in the entered password from the entry box, encode it as utf-8 so it's bytes for bcrypt
        password_entered = self.password_entry.text().encode('utf-8')
        # Our hash will be result 0, 2 (since we don't allow duplicate usernames at creation) of the following, which is
        # essentially: SELECT password FROM Users WHERE LOWER(username) = [lowercase of the entered username]
        if not username_entered or not password_entered:
            pop_error = True
        res = self.root.sql.select('main',
                                   table='Users',
                                   columns=['user_id', 'username', 'password'],
                                   where=f'LOWER(username) = "{username_entered.lower()}"')
        # if res is empty, pop_error because it means the username doesn't exist
        if not res:
            pop_error = True
        # if res is not empty hash is result 0, 2 because it is the third field in the first result.
        else:
            hash = res[0][2].encode('utf-8')
            # If bcrypt checkpw = False, pop error
            if not bcrypt.checkpw(password_entered, hash):
                pop_error = True

        # if any error changed the flag to true, pop the actual error dialog, then return
        if pop_error:
            qt.ErrorDialog(self.root,
                           title='Login Error',
                           text='There was a problem with the login information you provided.')
            return
        # If there are no errors,
        else:
            # Set current user_id in root so we can use it when needed.
            self.root.curr_user_id = res[0][0]
            # Go to character select screen
            self.go_to_char_select()

    def go_to_char_select(self):
        # Load character select widget
        self.goto(self.root.char_select_widget,
                  char_select.CharSelectWidget)
