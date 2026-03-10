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
        self.char_data = self.get_char_data()
        # Main panel will consist of location bar, room desc, main window, and entry bar
        self.location_bar = qt.LineEdit(self.root,
                                     text=f'{self.X}, {self.Y}, {self.Z} - {location_name}',
                                     layout=main_panel)
        # Make it green with black background and readonly for that old school feeeeel
        self.make_terminal(self.location_bar)
        # A text edit window set to readonly will act as our main window.
        self.main_window = qt.TextEdit(self.root,
                                    text=f'{location_desc}',
                                    layout=main_panel)
        # Make it green with black background and readonly
        self.make_terminal(self.main_window)
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
        # Make it green with black background and readonly
        self.make_terminal(entry_label)
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
        self.name_box = qt.LineEdit(self.root,
                               text=f'{self.root.curr_char_name}',
                               layout=name_layout)
        self.name_box.setMinimumSize(300,20)
        # Make it green with black background and readonly
        self.make_terminal(self.name_box)

        # Horizontal layout for level and its label, experience and its label
        level_layout = qt.QtWidgets.QHBoxLayout()
        right_panel.addLayout(level_layout)
        # Label
        level_label = qt.Label(self.root,
                               text='Level:',
                               layout=level_layout)
        # LineEdit Box for the level to be displayed in
        self.level_box = qt.LineEdit(self.root,
                                text=f'{self.char_data["level"]}',
                                layout=level_layout)
        # Make it green with black background and readonly
        self.make_terminal(self.level_box)

        # Label for XP
        xp_label = qt.Label(self.root,
                            text='Experience:',
                            layout=level_layout)
        # LineEdit to show XP
        self.xp_box = qt.LineEdit(self.root,
                                  text=f'{self.char_data["xp"]}',
                                  layout=level_layout)
        # Make it green with black background and readonly
        self.make_terminal(self.xp_box)

        # Layout for faction and its label
        faction_layout = qt.QtWidgets.QHBoxLayout()
        right_panel.addLayout(faction_layout)
        # Label
        faction_label = qt.Label(self.root,
                                 text='Faction:',
                                 layout=faction_layout)
        # Readonly lineedit to display faction
        self.faction_box = qt.LineEdit(self.root,
                                  text=f'{self.char_data["faction"]}',
                                  layout=faction_layout)
        # make it green with black background
        self.make_terminal(self.faction_box)

        # Button that displays contents of character's inventory
        inventory = qt.PushButton(self.root,
                                  text='Inventory',
                                  layout=right_panel,
                                  func=self.open_inventory)

        # Layout for Money display and its label
        moneys_layout = qt.QtWidgets.QHBoxLayout()
        right_panel.addLayout(moneys_layout)
        # Label
        moneys_label = qt.Label(self.root,
                               text='GB$',
                               layout=moneys_layout)
        # Lineedit for displaying current moneys
        self.moneys_box = qt.LineEdit(self.root,
                                     text=f'{self.char_data["moneys"]}',
                                     layout=moneys_layout)
        # Make it green with black background
        self.make_terminal(self.moneys_box)

        # Layout for hp and its label
        hp_layout = qt.QtWidgets.QHBoxLayout()
        right_panel.addLayout(hp_layout)
        # Label
        hp_label = qt.Label(self.root,
                            text='Hit Points:',
                            layout=hp_layout)
        # hp box
        self.hp_box = qt.LineEdit(self.root,
                                  text=f'{self.char_data["hp"]}',
                                  layout=hp_layout)
        # Make it green on black background
        self.make_terminal(self.hp_box)

        # Label for worn on
        worn_label = qt.Label(self.root,
                              text='Worn on:',
                              layout=right_panel)
        worn_label.setMaximumSize(300,20)

        # layout for head
        head_layout = qt.QtWidgets.QHBoxLayout()
        right_panel.addLayout(head_layout)
        # label for head
        head_label = qt.Label(self.root,
                              text='Head:',
                              layout=head_layout)
        # lineedit for head
        self.head_box = qt.LineEdit(self.root,
                                    text=f'{self.char_data["head"]}',
                                    layout=head_layout)
        # Make it green with black background
        self.make_terminal(self.head_box)

        # layout for chest
        chest_layout = qt.QtWidgets.QHBoxLayout()
        right_panel.addLayout(chest_layout)
        # label for chest
        chest_label = qt.Label(self.root,
                              text='Chest:',
                              layout=chest_layout)
        # lineedit for chest
        self.chest_box = qt.LineEdit(self.root,
                                    text=f'{self.char_data["chest"]}',
                                    layout=chest_layout)
        # Make it green with black background
        self.make_terminal(self.chest_box)

        # Layout for hands
        hands_layout = qt.QtWidgets.QHBoxLayout()
        right_panel.addLayout(hands_layout)
        # label for hands
        hands_label = qt.Label(self.root,
                              text='Hands:',
                              layout=hands_layout)
        # lineedit for hands
        self.hands_box = qt.LineEdit(self.root,
                                    text=f'{self.char_data["hands"]}',
                                    layout=hands_layout)
        # Make it green with black background
        self.make_terminal(self.hands_box)

        # layout for legs
        legs_layout = qt.QtWidgets.QHBoxLayout()
        right_panel.addLayout(legs_layout)
        # label for legs
        legs_label = qt.Label(self.root,
                              text='Legs:',
                              layout=legs_layout)
        # lineedit for legs
        self.legs_box = qt.LineEdit(self.root,
                                text=f'{self.char_data["legs"]}',
                                layout=legs_layout)
        # Make it green with black background
        self.make_terminal(self.legs_box)

        # layout for feet
        feet_layout = qt.QtWidgets.QHBoxLayout()
        right_panel.addLayout(feet_layout)
        # label for feet
        feet_label = qt.Label(self.root,
                              text='Feet:',
                              layout=feet_layout)
        # lineedit for feet
        self.feet_box = qt.LineEdit(self.root,
                                text=f'{self.char_data["feet"]}',
                                layout=feet_layout)
        # Make it green with black background
        self.make_terminal(self.feet_box)


        self.show()
        self.entry_box.setFocus()

    def get_char_data(self):
        raw_data =  self.root.sql.select('main',
                                    table='Characters',
                                    where={'char_id': self.root.curr_char_id})[0]

        data_dict = {'level': raw_data[3],
                     'xp': raw_data[4],
                     'hp': raw_data[5],
                     'species': raw_data[6],
                     'age': raw_data[7],
                     'profession': raw_data[8],
                     'faction': raw_data[9],
                     'moneys': raw_data[10],
                     'muscle': raw_data[11],
                     'speed': raw_data[12],
                     'toughness': raw_data[13],
                     'booksmarts': raw_data[14],
                     'streetsmarts': raw_data[15],
                     'appeal': raw_data[16],
                     'head': raw_data[20],
                     'chest': raw_data[21],
                     'hands': raw_data[22],
                     'legs': raw_data[23],
                     'feet': raw_data[24]}

        return data_dict

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

    def make_terminal(self, widget):
        widget.setStyleSheet('background-color:black; color:green')
        widget.setReadOnly(True)
