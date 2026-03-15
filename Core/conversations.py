from GUI import qt_classes as qt

def clear_buttons(btn_dict):
    for i in range(len(btn_dict.keys())):
        btn_dict[i].hide()
        del btn_dict[i]


class Conversations:
    def __init__(self, root, conversation_window, *args, **kwargs):
        self.root = root
        self.conv_window = conversation_window
        self.reputation = 0
        self.threshold = 0

    def assessment(self, *args ,**kwargs):
        def yes_totally():
            pass

        def confusion():
            pass

        # Set threshold for "winning" this conversation
        self.threshold = 20
        self.conv_window.main_window.clear()
        self.conv_window.update_main('The CapitalCorp Assessment Specialist looks at your file with a frown '
                                             'that is hard to read. She could be interested or disgusted (with no real '
                                             'in-between. After a time she puts the file down and asks you,'
                                             f'"5 years ago, if I had asked you where you saw yourself in 7 years, '
                                             f'would you now, to your knowledge, be within 3 years of that vision?"')

        self.conv_window.button_dict[0] = qt.PushButton(self.root,
                              text='Yes, totally, I actually have dreamed of working at CapitalCorp my whole life!',
                              layout=self.conv_window.button_container,
                              func=lambda: self.change_reputation(10),
                              loc=(0,0))

        self.conv_window.button_dict[1] = qt.PushButton(self.root,
                                     text='Ok, wait... 5 years, and then 7 years from there is... and then... uhhh...',
                                     layout=self.conv_window.button_container,
                                     loc=(1,0),
                                     func=lambda: self.change_reputation(-10))

    def change_reputation(self, amount):
        self.reputation += amount
        if self.reputation >= self.threshold:
            pass

