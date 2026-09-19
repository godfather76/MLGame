from GUI import qt_classes as qt
from GUI import utility_classes as util
from GUI import game_main
from Core import conversations
from Core import conversation_exits
from Core import helpers


class OllamaWorker(qt.QtCore.QThread):
    response_received = qt.QtCore.Signal(str)

    def __init__(self, conv_instance, user_text):
        super().__init__()
        self.conv_instance = conv_instance
        self.user_text = user_text

    def run(self):
        reply = self.conv_instance.process_turn(self.user_text)
        self.response_received.emit(reply)

class ConversationWidget(util.GroupBoxWidget):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, title='Conversation', *args, **kwargs)
        self.back_button = None
        self.curr_display = ''
        self.main_window = None
        self.button_container = None
        self.send_button = None
        self.worker = None
        # Button dictionary will be used to easily hide all the buttons we put in the button_container during a
        # given conversation
        self.button_dict = {}
        self.root = root
        self.conversations = conversations.Conversations(self.root, self)
        self.conversation_exits = conversation_exits.ConversationExits(self.root, self)
        self.main_display_layout()
        self.show()
        qt.QtCore.QTimer.singleShot(0, self.run_conversation)

    def back(self):
        if self.conversations.is_finished:
            helpers.end_conversation(self.root, self)
        else:
            self.go_to_game()

    def go_to_game(self, *args, **kwargs):
        self.goto(self.root.main_game_widget,
                  game_main.MainGameWidget)

    def run_conversation(self, *args, **kwargs):
        helpers.main_display_message = self.conversations.converse()


    def update_main(self, text, *args, **kwargs):
        self.curr_display += f'{text}\n'
        self.main_window.setText(self.curr_display)

    def main_display_layout(self, *args, **kwargs):
        self.main_window = qt.TextEdit(self.root,
                                       layout=self.gblayout)
        # Make it green with black background and readonly
        game_main.make_terminal(self.main_window)
        # self.button_container = qt.QtWidgets.QGridLayout()
        # self.gblayout.addLayout(self.button_container)
        # Layout to put the entry carat, entry bar, and enter button in
        entry_layout = qt.QtWidgets.QHBoxLayout()
        self.gblayout.addLayout(entry_layout)
        # Label for carat
        entry_label = qt.LineEdit(self.root,
                                  text='>',
                                  layout=entry_layout)
        # Make it so it stays its normal size.
        entry_label.setMinimumSize(20, 20)
        entry_label.setMaximumSize(20, 20)
        # Make it green with black background and readonly
        game_main.make_terminal(entry_label)
        # Entry box will be a line edit
        self.entry_box = qt.LineEdit(self.root,
                                     placeholderText='Enter command',
                                     layout=entry_layout)

        # Make text green for that old school feeeeeel!
        self.entry_box.setStyleSheet('background-color:black; color:green')
        # Make it so when entry_box has focus, enter sends the command.
        self.entry_box.returnPressed.connect(self.send_command)
        # self.entry_box.setFocus()
        qt.QtCore.QTimer.singleShot(0, self.entry_box.setFocus)
        # Send button
        self.send_button = qt.PushButton(self.root,
                                    text='Send Command',
                                    layout=entry_layout,
                                    func=self.send_command)
        self.back_button = qt.PushButton(self.root,
                                         text='Back',
                                         layout=self.gblayout,
                                         func=self.back)

    def send_command(self):
        ## This will update the boxes above and be the way the user interacts with the ollama prompt in the conversation
        user_text = self.entry_box.text().strip()
        if not user_text:
            return

        # Print player text to the display
        self.update_main(f'> {user_text}')
        self.entry_box.clear()

        self.entry_box.setEnabled(False)
        self.send_button.setEnabled(False)

        self.worker = OllamaWorker(self.conversations, user_text)
        self.worker.response_received.connect(self.handle_response)
        self.worker.start()

    def handle_response(self, reply_text, *args, **kwargs):
        self.update_main(f'{self.root.active_conversation_NPC}: {reply_text}\n')

        # Re-enable controls
        self.entry_box.setEnabled(True)
        self.send_button.setEnabled(True)
        self.entry_box.setFocus()

        # 4. Handle end-of-conversation criteria
        if self.conversations.is_finished:
            if self.conversations.game_state['passed']:
                exit_info =  self.root.active_conversation_data.get('exit_info')
                if exit_info:
                    getattr(self.conversation_exits, exit_info, None)()
                self.update_main(
                    self.root.active_conversation_data['end_text']
                )
                self.entry_box.setEnabled(False)
                self.send_button.setEnabled(False)
            else:
                pass

