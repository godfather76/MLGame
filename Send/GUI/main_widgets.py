from GUI import about
from GUI import character_selection as char_select
from GUI import login
from GUI import user_creation as user_create
from GUI import utility_classes as util
from GUI import qt_classes as qt


class MainSplashWidget(util.GroupBoxWidget):
    def __init__(self, root, *args, **kwargs):
        # Initialize the super class
        super().__init__(root, title='CorpoPunk', *args, **kwargs)
        # Add a label that is essentially the splash screen message. May eventually have this change on each boot
        self.path_label = qt.Label(self.root,
                                   text='The streets are slick with rain. There is a river of red running in the\n'
                                        'gutter. You\'re not sure if it\'s blood, a fruity drink, or radiator fluid.\n'
                                        'Here in Corpo City, it could be anything... but it\'s probably blood.',
                                   layout=self.gblayout)
        # Add a layout for just the nav buttons. Make it a vertical box layout
        self.nav_btn_layout = qt.QtWidgets.QVBoxLayout()
        # Add our nav button layout to the gblayout
        self.gblayout.addLayout(self.nav_btn_layout)
        # add a login button
        self.login_btn = qt.PushButton(self.root,
                                          text='Login',
                                          layout=self.nav_btn_layout,
                                          func=self.go_login)

        # We are going to check that Users table exists (the first time the game is booted, it will not exist yet)
        if 'Users' not in self.root.sql.table_names('main'):
            # Make list of column names for Users table
            column_data = ['username', 'password']
            # Create the Users table with a primary key called user_id
            self.root.sql.create_table('main', table='Users', primary_key='user_id', column_data=column_data)
        # Now that the Users table for sure exists, we'll check to see if there are any entries in it
        # Basically, we want to see if there are Users so we can disable the login button if there aren't
        # This way, if it gets booted once and no Users are created, we can catch that
        if not self.root.sql.select('main', 'Users'):
            self.login_btn.setDisabled(True)
        self.create_new_user_btn = qt.PushButton(self.root,
                                                 text='Create New User',
                                                 layout=self.nav_btn_layout,
                                                 func=self.go_user_create)
        self.about_btn = qt.PushButton(self.root,
                                       text='About',
                                       layout=self.nav_btn_layout,
                                       func=self.go_about)
        self.show()

    @qt.QtCore.Slot()
    def go_login(self, *args, **kwargs):
        # If we are in dev mode
        if self.root.dev_mode:
            # Make the current user id the dev user id we selected
            self.root.curr_user_id = self.root.dev_user_id
            # Load character select widget
            self.goto(self.root.char_select_widget,
                      char_select.CharSelectWidget)
        else:
            self.goto(self.root.login_widget,
                      login.LoginWidget)

    @qt.QtCore.Slot()
    def go_user_create(self, *args, **kwargs):
        self.goto(self.root.user_create_widget,
                  user_create.UserCreateWidget)

    @qt.QtCore.Slot()
    def go_about(self, *args, **kwargs):
        self.goto(self.root.about_widget,
                  about.AboutWidget)
