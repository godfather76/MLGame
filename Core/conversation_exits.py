from Core import helpers, conversations


class ConversationExits:

    def __init__(self, root, conv_window, *args, **kwargs):
        self.root = root
        self.conv_window = conv_window

    def make_employee(self, *args, **kwargs):
        self.root.sql.update('main',
                             table='Characters',
                             data={'capcorp_emp': 1},
                             where={'char_id': self.root.curr_char_id})
