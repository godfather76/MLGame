from GUI import main_widgets
from GUI import utility_classes as util
from GUI import qt_classes as qt


class AboutWidget(util.GroupBoxWidget):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, title='About CorpoPunk', *args, **kwargs)
        self.test_label = qt.Label(self.root,
                                   text='CorpoPunk is a machine learning and hobby project written by Isaac Godsey.\n'
                                        'The code is open source and is meant to be a way I can practice, showcase\n'
                                        'my skills, and relax in between further learning endeavors. I sincerely\n'
                                        'hope this game brings you joy and gives you some insight into my eclectic\n'
                                        'mind. If you\'d like to thank or reward me for my work, tell a friend about\n'
                                        'it. Bonus points if that friend is looking for an ML Engineer and also likes\n'
                                        'my work ;-{D}',
                                   layout=self.gblayout,
                                   alignment=qt.QtCore.Qt.AlignLeft)
        self.nav_btn_layout = qt.QtWidgets.QVBoxLayout()
        # Add our nav button layout to the gblayout
        self.gblayout.addLayout(self.nav_btn_layout)
        # Add a back button
        self.back_btn = qt.PushButton(self.root,
                                      text='Back',
                                      layout=self.nav_btn_layout,
                                      func=self.go_back)
        self.show()

    @qt.QtCore.Slot()
    def go_back(self):
        self.goto(self.root.main_splash_widget, main_widgets.MainSplashWidget)