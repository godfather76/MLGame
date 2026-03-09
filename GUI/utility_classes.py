from GUI import qt_classes as qt

# This has a layout structure all of our widgets will inherit. This will make things easier on me,
# who would really rather minimize UI coding time (I'm here for the data) XD
class GroupBoxWidget(qt.QtWidgets.QWidget):
    def __init__(self, root, title='Add a title', *args, **kwargs):
        self.root = root
        super().__init__(*args, **kwargs)
        # Set up a grid layout to put our group box in.
        self.layout = qt.QtWidgets.QGridLayout(self)
        # create our group box, adding it to our layout.
        self.gb = qt.GroupBox(self.root, title=title, layout=self.layout)
        # Add a vertical box layout to our group box
        self.gblayout = qt.QtWidgets.QVBoxLayout(self.gb)

    def end(self, var):
        self.close()
        self.deleteLater()
        var = None

    @qt.QtCore.Slot()
    def goto(self, var, widget):
        self.end(var)
        self.load_page(var, widget)

    @qt.QtCore.Slot()
    def load_page(self, var, widget):
        var = widget(self.root)
        self.root.setCentralWidget(var)


