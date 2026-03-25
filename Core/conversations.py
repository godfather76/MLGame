from GUI import qt_classes as qt
from Core import helpers

def clear_buttons(btn_dict):
    for i in range(len(btn_dict.keys())):
        btn_dict[i].hide()
        del btn_dict[i]


class Conversations:
    def __init__(self, root, conversation_window, *args, **kwargs):
        self.root = root
        self.conv_window = conversation_window
        self.current_conversation = None
        self.response_dict = {}
        self.reputation = 0
        self.threshold = 0
        self.conv_window.setMinimumSize(750, 500)

    def assessment(self, *args ,**kwargs):
        # Set the current_conversation name to this one
        self.current_conversation = 'assessment'
        # Check if this character has finished this conversation
        if not helpers.conversation_had_check(self.root, self.conv_window, self):
            # Create a response_dictionary
            self.response_dict = helpers.create_response_dict(self.root, self)
            # Begin conversation by starting the 0-rep branch
            helpers.change_reputation(self.root, self.conv_window, self, 0, '')
