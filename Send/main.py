from GUI import main_app
import sys

def main():
    # instantiate our app with sys.argv
    app = main_app.qt.QtWidgets.QApplication(sys.argv)
    # instantiate main window, passing in our app instance
    window = main_app.MainWindow(app)
    # Show the window
    window.show()
    # Execute the app
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
