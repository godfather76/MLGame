from GUI import qt_classes as qt

class Conversations:
    def __init__(self, root, conversation_window, *args, **kwargs):
        self.root = root
        self.conversation_window = conversation_window

    def assessment(self, *args ,**kwargs):
        self.conversation_window.main_window.clear()
        self.conversation_window.update_main('The CapitalCorp Assessment Specialist looks at your file with a frown '
                                             'that is hard to read. She could be interested or disgusted (with no real '
                                             'in-between. After a time she puts the file down and asks you,'
                                             f'"5 years ago, if I had asked you where you saw yourself in 7 years, '
                                             f'would you now, to your knowledge, be within 3 years of that vision?"')

        self.button = qt.PushButton(self.root,
                      text='Hide',
                      layout=self.conversation_window.button_container,
                      func=self.hide,
                                    loc=(0,0))
        self.button2 = qt.PushButton(self.root,
                                     text='Unhide',
                                     layout=self.conversation_window.button_container,
                                     loc=(0,1),
                                     func=self.unhide)

    def hide(self, *args ,**kwargs):
        self.button.hide()

    def unhide(self, *args ,**kwargs):
        self.button.show()

