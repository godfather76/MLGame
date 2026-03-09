from GUI import main_widgets
from GUI import utility_classes as util
from GUI import qt_classes as qt


class MainGameWidget(util.GroupBoxWidget):
    X = None
    Y = None
    Z = None
    def __init__(self, root, *args, **kwargs):
        super().__init__(root,title='CorpoPunk',*args, **kwargs)
        # Container to hold the two panels (main and right)
        container = qt.QtWidgets.QHBoxLayout()
        # Add the container to our GroupBox
        self.gblayout.addLayout(container)
        # A vertical main panel
        main_panel = qt.QtWidgets.QVBoxLayout()
        # Add main panel to container
        container.addLayout(main_panel)
        location_name, location_desc = self.get_room_info()
        # Main panel will consist of location bar, room desc, main window, and entry bar
        self.location_bar = qt.LineEdit(self.root,
                                     text=f'{self.X}, {self.Y}, {self.Z} - {location_name}',
                                     layout=main_panel)
        # Make text green for that old school feeeeeel!
        self.location_bar.setStyleSheet('background-color:black; color:green')
        # Make the line edit read only
        self.location_bar.setReadOnly(True)
        # A text edit window set to readonly will act as our main window.
        self.main_window = qt.TextEdit(self.root,
                                    text=f'{location_desc}',
                                    layout=main_panel)
        self.main_window.setReadOnly(True)
        # Make text green for that old school feeeeeel!
        self.main_window.setStyleSheet('background-color:black; color:green')
        # Set the minimum size of the main window
        self.main_window.setMinimumSize(1000, 750)

        # Layout to put the entry carat, entry bar, and enter button in
        entry_layout = qt.QtWidgets.QHBoxLayout()
        main_panel.addLayout(entry_layout)
        # Label for carat
        entry_label = qt.LineEdit(self.root,
                               text='>',
                               layout=entry_layout)
        # Make it so it stays its normal size.
        entry_label.setMinimumSize(20, 20)
        entry_label.setMaximumSize(20, 20)
        # Make text green for that old school feeeeeel!
        entry_label.setStyleSheet('background-color:black; color:green')
        entry_label.setReadOnly(True)
        # Entry box will be a line edit
        self.entry_box = qt.LineEdit(self.root,
                                     placeholderText='Enter command',
                                     layout=entry_layout)
        # Make text green for that old school feeeeeel!
        self.entry_box.setStyleSheet('background-color:black; color:green')
        # Make it so when entry_box has focus, enter sends the command.
        self.entry_box.returnPressed.connect(self.send_command)
        # Send button
        send_button = qt.PushButton(self.root,
                                    text='Send Command',
                                    layout=entry_layout,
                                    func=self.send_command)


        # Right panel for things like inventory
        right_panel = qt.QtWidgets.QVBoxLayout()
        container.addLayout(right_panel)
        # Create a layout for name and its label
        name_layout = qt.QtWidgets.QHBoxLayout()
        right_panel.addLayout(name_layout)
        # A label for name
        name_label = qt.Label(self.root,
                              text='Name:',
                              layout=name_layout)
        name_box = qt.LineEdit(self.root,
                               text=f'{self.root.curr_char_name}',
                               layout=name_layout)
        # Make it green text on black background
        name_box.setStyleSheet('background-color:black; color:green')
        # Set it to readonly
        name_box.setReadOnly(True)

        inventory = qt.PushButton(self.root,
                                  text='Inventory',
                                  layout=right_panel,
                                  func=self.open_inventory)
        for x in range(15):
            qt.PushButton(self.root,
                          text=f'{x}',
                          layout=right_panel)



        self.show()
        self.entry_box.setFocus()

    def get_room_info(self):
        self.X, self.Y, self.Z = self.root.sql.select('main',
                                      table='Characters',
                                      columns=['X', 'Y', 'Z'],
                                      where={'user_id': self.root.curr_user_id})[0]
        return self.root.sql.select('main',
                                    table='Locations',
                                    columns=['locationName', 'locationDesc'],
                                    where={'X': self.X,
                                           'Y': self.Y,
                                           'Z': self.Z},
                                    )[0]

    def send_command(self):
        print('Doing command:', self.entry_box.text())
        self.entry_box.clear()

    def open_inventory(self):
        print('Opening inventory')
