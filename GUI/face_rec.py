from GUI import main_widgets
from GUI import utility_classes as util
from GUI import qt_classes as qt


class FaceRecSetupWidget(util.GroupBoxWidget):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, title='Face Recognition Setup', *args, **kwargs)
        self.main_label = qt.Label(self.root,
                                   text='Face Recognition Setup',
                                   layout=self.gblayout)
        # self.username_entry = qt.LineEdit(self.root,
        #                                   placeholderText='Enter username here',
        #                                   layout=self.gblayout)
        # # add an entry box for password
        # self.password_entry = qt.LineEdit(self.root,
        #                                   placeholderText='Enter password here',
        #                                   layout=self.gblayout,
        #                                   echoMode=qt.LineEdit.EchoMode.Password)
        # self.face_rec_btn = qt.PushButton(self.root,
        #                                   text='Use Facial Recognition',
        #                                   layout=self.gblayout,
        #                                   func=self.use_face_rec)
        # # Button to kick off login
        # self.login_btn = qt.PushButton(self.root,
        #                                 text='Log in!',
        #                                 layout=self.gblayout,
        #                                 func=self.login)
        # # Butto nto go back to login
        # self.back_btn = qt.PushButton(self.root,
        #                               text='Back to Main Menu',
        #                               layout=self.gblayout,
        #                               func=self.back_to_main)
        self.show()

    @qt.QtCore.Slot()
    def back_to_main(self):
        if self.root.curr_user_id:
            self.root.curr_user_id = None
        self.goto(self.root.main_splash_widget,
                       main_widgets.MainSplashWidget)
