from GUI import qt_classes as qt
from GUI import utility_classes as util
from GUI import game_main
from Core import conversations

class ConversationWidget(util.GroupBoxWidget):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.back_button = None
        self.curr_display = ''
        self.main_window = None
        self.button_container = None
        # Button dictionary will be used to easily hide all the buttons we put in the button_container during a
        # given conversation
        self.button_dict = {}
        self.root = root
        self.conversations = conversations.Conversations(self.root, self)
        self.main_display_layout()
        self.show()
        qt.QtCore.QTimer.singleShot(0, self.run_conversation)

    def go_to_game(self, *args, **kwargs):
        self.goto(self.root.main_game_widget,
                  game_main.MainGameWidget)

    def run_conversation(self, *args, **kwargs):
        getattr(self.conversations, self.root.active_conversation, None)()

    def update_main(self, text, *args, **kwargs):
        self.curr_display += f'\n{text}'
        self.main_window.setText(self.curr_display)

    def main_display_layout(self, *args, **kwargs):
        self.main_window = qt.TextEdit(self.root,
                                       layout=self.gblayout)
        # Make it green with black background and readonly
        game_main.make_terminal(self.main_window)
        self.button_container = qt.QtWidgets.QGridLayout()
        self.gblayout.addLayout(self.button_container)
        self.back_button = qt.PushButton(self.root,
                                         text='Back',
                                         layout=self.gblayout,
                                         func=self.go_to_game)