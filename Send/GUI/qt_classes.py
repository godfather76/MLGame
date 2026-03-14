from PySide6 import QtCore, QtWidgets, QtGui
import sys
from tkinter import messagebox

from PySide6.QtWidgets import QPushButton


@QtCore.Slot()
def default_func():
    print("Enter a function")


class Dialog(QtWidgets.QDialog):
    def __init__(self, root, parent=None, title='Dialog', *args, **kwargs):
        self.root = root
        super().__init__(parent, *args, **kwargs)
        self.setWindowTitle(title)
        self.show()


class ErrorDialog(QtWidgets.QMessageBox):
    def __init__(self, root, parent=None, title='Error', *args, **kwargs):
        self.root = root
        super().__init__(parent, *args, **kwargs)
        self.setWindowTitle(title)
        self.exec()


class OKCancelDialog(QtWidgets.QMessageBox):
    def __init__(self, root, parent=None, title='Ok or Cancel?', *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setWindowTitle(title)
        self.exec()

class GroupBox(QtWidgets.QGroupBox):
    def __init__(self, root, parent=None, title='Enter Title', layout=None, loc=None, alignment=None, *args, **kwargs):
        self.root = root
        if not alignment:
            alignment = QtCore.Qt.AlignCenter
        super().__init__(parent, alignment=alignment, *args, **kwargs)
        self.setTitle(title)
        if not layout:
            self.show()
        else:
            if loc:
                layout.addWidget(self, loc[0], loc[1])
            else:
                layout.addWidget(self)


class Widget(QtWidgets.QWidget):
    def __init__(self, root, parent=None, layout=None, loc=None, *args, **kwargs):
        self.root = root
        super().__init__(parent, *args, **kwargs)
        if not layout:
            self.show()
        else:
            if loc:
                layout.addWidget(self, loc[0], loc[1])
            else:
                layout.addWidget(self)


class ComboBox(QtWidgets.QComboBox):
    def __init__(self, root, parent=None, layout=None, alignment=QtCore.Qt.AlignmentFlag.AlignLeft , *args, **kwargs):
        self.root = root
        super().__init__(parent, *args, **kwargs)
        if not layout:
            self.show()
        else:
            layout.addWidget(self,
                             alignment=alignment)


class DateEdit(QtWidgets.QDateEdit):
    def __init__(self, root, parent=None, layout=None, loc=None, *args, **kwargs):
        self.root = root
        super().__init__(parent, *args, **kwargs)
        if not layout:
            self.show()
        else:
            if loc:
                layout.addWidget(self, loc[0], loc[1])
            else:
                layout.addWidget(self)


class Label(QtWidgets.QLabel):
    def __init__(self, root, parent=None, text='Enter Text', layout=None, loc=None, alignment=None, *args, **kwargs):
        self.root = root
        if not alignment:
            alignment = QtCore.Qt.AlignCenter
        super().__init__(parent, text=text, alignment=alignment, *args, **kwargs)
        if not layout:
            self.show()
        else:
            if loc:
                layout.addWidget(self, loc[0], loc[1])
            else:
                layout.addWidget(self)


class LineEdit(QtWidgets.QLineEdit):
    def __init__(self, root, parent=None, text=None, placeholderText='Enter Text Here', layout=None, loc=None, *args, **kwargs):
        self.root = root
        super().__init__(text=text, placeholderText=placeholderText, *args, **kwargs)
        if not layout:
            self.show()
        else:
            if loc:
                layout.addWidget(self, loc[0], loc[1])
            else:
                layout.addWidget(self)


class PushButton(QtWidgets.QPushButton):
    def __init__(self, root, parent=None, text='Enter Text', layout=None, loc=None, func=default_func, *args, **kwargs):
        self.root = root
        super().__init__(parent, text=text, *args, **kwargs)
        # func must be @QtCore.Slot()
        self.clicked.connect(func)
        if not layout:
            self.show()
        else:
            if loc:
                layout.addWidget(self, loc[0], loc[1])
            else:
                layout.addWidget(self)


class RadioButton(QtWidgets.QRadioButton):
    def __init__(self, root, parent=None, text='Enter Text', layout=None, loc=None, *args, **kwargs):
        self.root = root
        super().__init__(parent, text=text, *args, **kwargs)
        if not layout:
            self.show()
        else:
            if loc:
                layout.addWidget(self, loc[0], loc[1])
            else:
                layout.addWidget(self)

class SpinBox(QtWidgets.QSpinBox):
    def __init__(self, root, parent=None, layout=None, loc=None, alignment=QtCore.Qt.AlignmentFlag.AlignCenter, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        if not layout:
            self.show()
        else:
            layout.addWidget(self,
                             alignment=alignment)


class TextEdit(QtWidgets.QTextEdit):
    def __init__(self, root, parent=None, placeholderText='Enter Text', layout=None, loc=None, *args, **kwargs):
        self.root = root
        super().__init__(parent, placeholderText=placeholderText, *args, **kwargs)
        if not layout:
            self.show()
        else:
            if loc:
                layout.addWidget(self, loc[0], loc[1])
            else:
                layout.addWidget(self)


class TimeEdit(QtWidgets.QTimeEdit):
    def __init__(self, root, parent=None, layout=None, loc=None, *args, **kwargs):
        self.root = root
        super().__init__(parent, *args, **kwargs)
        if not layout:
            self.show()
        else:
            if loc:
                layout.addWidget(self, loc[0], loc[1])
            else:
                layout.addWidget(self)

class ToolButton(QtWidgets.QToolButton):
    def __init__(self, root, parent=None, text='Tool Button', func=default_func, layout=None, loc=None, *args, **kwargs):
        self.root = root
        super().__init__(parent, *args, **kwargs)
        self.clicked.connect(func)
        if not layout:
            self.show()
        else:
            if loc:
                layout.addWidget(self, loc[0], loc[1])
            else:
                layout.addWidget(self)


class TestWindow(QtWidgets.QMainWindow):
    def __init__(self, main_app, *args, **kwargs):
        self.main_app = main_app
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Simple Pic Sorter')
        self.resize(400, 200)
        main_widget = TestWidget(self)
        self.setCentralWidget(main_widget)
        file = QtCore.QFile('Darkeum_teal.qss')
        if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            return

        qss = QtCore.QTextStream(file)
        self.setStyleSheet(qss.readAll())
        # self.setWindowFlags(qt.QtCore.Qt.WindowType.FramelessWindowHint)
        # self.title_bar = qt.CustomTitleBar(self)
        self.show()
        sys.exit(self.main_app.exec())


class TestWidget(QtWidgets.QWidget):
    text_box = None
    go_button = None

    def __init__(self, root, *args, **kwargs):
        self.root = root
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QGridLayout(self)
        gb = GroupBox(self.root, title='GroupBox', layout=self.layout)
        # top_layout = qt.QtWidgets.QGridLayout(gb)
        gblayout = QtWidgets.QVBoxLayout(gb)
        cb = ComboBox(self.root,
                      layout=gblayout)
        cb.addItems(['ComboBox', 'Items'])
        DateEdit(self.root,
                 layout=gblayout)
        Dialog(self.root,
               parent=self,
               )
        Label(self.root,
              text='Label',
              layout=gblayout)
        LineEdit(self.root,
                 placeholderText='LineEdit',
                 layout=gblayout)
        PushButton(self.root,
                   text='PushButton',
                   layout=gblayout,
                   func=default_func)
        RadioButton(self.root,
                    text='RadioButton',
                    layout=gblayout)
        TextEdit(self.root,
                 placeholderText='TextEdit',
                 layout=gblayout)
        TimeEdit(self.root,
                 layout=gblayout)
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = TestWindow(app)
    window.show()
    app.exec()
