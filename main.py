from GUI import main_app
import sys
import tomllib

def main():
    with open('config.toml', 'rb') as f:
        config = tomllib.load(f)
    f.close()
    # instantiate our app with sys.argv
    app = main_app.qt.QtWidgets.QApplication(sys.argv)
    # instantiate main window, passing in our app instance
    window = main_app.MainWindow(app, config)
    # Show the window
    window.show()
    # Execute the app
    sys.exit(app.exec())


if __name__ == '__main__':
    main()