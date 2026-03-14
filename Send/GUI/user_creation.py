import bcrypt
from GUI import character_creation as char_create
from GUI import main_widgets
from GUI import qt_classes as qt
from GUI import utility_classes as util


class UserCreateWidget(util.GroupBoxWidget):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, title='Create New User', *args, **kwargs)
        # Add main label
        self.main_label = qt.Label(self.root,
                                   text='Create New User\n'
                                        'Each user can have multiple characters that are related to one another,\n'
                                        'either as friends, family, or coworkers.',
                                   layout=self.gblayout)
        # Add entry box for username
        self.username_entry = qt.LineEdit(self.root,
                                          placeholderText='Enter username here',
                                          layout=self.gblayout)
        # add an entry box for password
        self.password_entry = qt.LineEdit(self.root,
                                          placeholderText='Enter password here',
                                          layout=self.gblayout,
                                          echoMode=qt.LineEdit.EchoMode.Password)
        # add an entry for password re-entry
        self.reenter_password_entry = qt.LineEdit(self.root,
                                                  placeholderText='Re-enter password',
                                                  layout=self.gblayout,
                                                  echoMode=qt.LineEdit.EchoMode.Password)
        # Button to kick off new user creation
        self.create_btn = qt.PushButton(self.root,
                                    text='Create!',
                                    layout=self.gblayout,
                                    func=self.create_new_user)
        # Butto nto go back to login
        self.back_btn = qt.PushButton(self.root,
                                      text='Back to Main Menu',
                                      layout=self.gblayout,
                                      func=self.back_to_main)
        self.show()

    @qt.QtCore.Slot()
    def create_new_user(self):
        # get username from the entry box and strip leading and trailing spaces
        username = self.username_entry.text().strip()
        # Get password1 from the entry, leave spaces as is
        password1 = self.password_entry.text()
        # get password2, also leave spaces as is
        password2 = self.reenter_password_entry.text()
        # if username is blank,
        if not username:
            # Pop up error dialog and then return
            qt.ErrorDialog(self.root,
                           title='Invalid Username',
                           text='Username cannot be blank. Please try again.')
            return

        # if either password is not entered,
        if not password1.strip() or not password2.strip():
            # pop up error dialog and then return
            qt.ErrorDialog(self.root,
                           title='Password Error',
                           text='One or more passwords was left blank.\n'
                                'Note: passwords can contain, begin with, or end with spaces, but there must be other '
                                'characters in addition to spaces. Please try again.')
            return
        # if the passwords do not match,
        if password1 != password2:
            # pop up error dialog and then return
            qt.ErrorDialog(self.root,
                           title='Password Error',
                           text='The passwords you entered do not match. Please try '
                                'again.')
            return

        # select username from Users where username=username. If this returns a result,
        if self.root.sql.select('main',
                                table='Users',
                                columns=['username'],
                                where=f'LOWER(username) = "{username.lower()}"'):
            # pop up error dialog and then return
            qt.ErrorDialog(self.root,
                           title='Username Error',
                           text='The username you entered already exists. Please try again.')
            return
        hashed = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
        sql_dict = {'username': username,
                    'password': hashed.decode('utf-8')}
        self.root.sql.insert('main',
                             table='Users',
                             data=sql_dict)
        user_id = self.root.sql.select('main',
                                       table='Users',
                                       columns=['user_id'],
                                       where=f'LOWER(username) = "{username.lower()}"')[0][0]
        self.root.curr_user_id = user_id
        self.goto(self.root.char_create_widget, char_create.CharCreateWidget)

    @qt.QtCore.Slot()
    def back_to_main(self):
        self.goto(self.root.main_splash_widget,
                  main_widgets.MainSplashWidget)
