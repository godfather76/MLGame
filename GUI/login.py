import bcrypt
from GUI import character_creation as char_create
from GUI import character_selection as char_select
from GUI import face_rec
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
        self.face_rec_btn = qt.PushButton(self.root,
                                          text='Use Facial Recognition',
                                          layout=self.gblayout,
                                          func=self.use_face_rec)
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

    @qt.QtCore.Slot()
    def use_face_rec(self):
        # if there's nothing in username, pop error dialog and return
        if not self.username_entry.text():
            qt.ErrorDialog(self.root,
                           title='Enter Username',
                           text='In order to use facial recognition, you must first enter a username.',)
            return
        else:
            # Make a dictionary {'username': {'user_id': user_id, 'face_rec_pic"; face_rec_pic}
            # We use name as the key because that's what they typed in. We make it lower and strip it to ignore case
            users = {y.lower().strip(): {'user_id': x, 'face_rec_pic': z} for x, y, z in self.root.sql.select('main',
                                                                        table='Users',
                                                                        columns=['user_id',
                                                                                 'username',
                                                                                 'face_rec_pic'])}
            # If the lowered and stripped text from the entry box is in the usernames (keys in our dictionary)
            if self.username_entry.text().lower().strip() in users.keys():
                # Set pic path to
                face_rec_pic_path = users[self.username_entry.text().lower().strip()]['face_rec_pic']
                print(repr(face_rec_pic_path))
                if not face_rec_pic_path:
                    self.go_to_face_rec_setup()
                    return
                user_id = users[self.username_entry.text().lower().strip()]['user_id']
            else:
                qt.ErrorDialog(self.root,
                               title='Incorrect Username',
                               text='Please enter a valid username. If you have not created a user for yourself, do that'
                                    'first. You can set up facial recognition at a later time.',)
                return
        # We only get here if the above doesn't return due to error, so we know that face_rec_pic_path is set
        if self.check_device():
            from deepface import DeepFace
            DeepFace.stream(face_rec_pic_path)


    @qt.QtCore.Slot()
    def go_to_char_select(self):
        # Load character select widget
        self.goto(self.root.char_select_widget,
                  char_select.CharSelectWidget)

    @qt.QtCore.Slot()
    def go_to_face_rec_setup(self):
        # Load face recognition setup widget
        self.goto(self.root.face_rec_setup_widget,
                  face_rec.FaceRecSetupWidget)

    def check_device(self):
        import os

        # Suppress core OpenCV warnings and info logs
        os.environ['OPENCV_LOG_LEVEL'] = 'OFF'

        # Suppress companion FFmpeg backend warnings
        os.environ['OPENCV_FFMPEG_LOGLEVEL'] = '-8'
        import cv2
        cap = cv2.VideoCapture(0)
        dev_found = False
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                dev_found = True
        if not dev_found:
            qt.ErrorDialog(self.root,
                           title='No Video Device Detected',
                           text='No Video Device Detected. Make sure your device is plugged in and then try again.')
            return False
        else:
            return True