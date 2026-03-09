from GUI import main_widgets
from GUI import utility_classes as util
from GUI import qt_classes as qt
from SQL import builder
from SQL import db_utilities as db_util
import sys

# Main window will remain here and the centralWidget will change
class MainWindow(qt.QtWidgets.QMainWindow):
    # dev_mode will log me directly in so I don't go crazy retyping my username and password
    # dev_mode = False
    dev_mode = True
    # This allows me to easily select a different user for dev mode
    dev_user_id = 1
    # Create variables we want to use later, so that they're considered declared in the init
    about_widget = None
    char_create_widget = None
    char_select_widget = None
    login_widget = None
    user_create_widget = None
    # these variables are specifically for screen position:
    wd = 400
    ht = 200
    x = 0
    y = 0
    # user/character data variables
    curr_user_id = None
    curr_char = None

    def __init__(self, main_app, *args, **kwargs):
        # This is root
        # instantiate the super class
        super().__init__(*args, **kwargs)
        self.main_app = main_app
        # set up our sql builder and sql database
        # Key is database path, value is the database's alias.
        db_info = {'SQL/main_db.db': 'main'}
        # instantiate our builder, pass in db_info, create the db if it doesn't exist.
        self.sql = builder.Build(db_info=db_info, create=True)
        # Set window's title
        self.setWindowTitle('CorpoPunk: Capitalist Hellscape')
        # resize the window to 400x200
        self.setGeometry(self.x, self.y, self.wd, self.ht)
        # instantiate our main widget, then set it as the Central widget
        self.set_center()
        self.setGeometry(self.geometry().x(), self.geometry().y() - 100, self.wd, self.ht)
        self.main_splash_widget = main_widgets.MainSplashWidget(self)
        self.setCentralWidget(self.main_splash_widget)
        # Load our color theme
        file = qt.QtCore.QFile('Darkeum_teal.qss')
        if not file.open(qt.QtCore.QFile.ReadOnly | qt.QtCore.QFile.Text):
            return
        qss = qt.QtCore.QTextStream(file)
        self.setStyleSheet(qss.readAll())
        # show our window
        self.show()
        # Needed so the x will exit the program
        sys.exit(self.main_app.exec())

    def set_center(self):
        center = qt.QtGui.QScreen.availableGeometry(qt.QtWidgets.QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())
