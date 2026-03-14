from SQL import db_utilities as dbutil
from GUI import main_widgets
from GUI import utility_classes as util
from GUI import qt_classes as qt
from Core import commands
from Core import room_events


def make_terminal(widget):
    widget.setStyleSheet('background-color:black; color:green')
    widget.setReadOnly(True)


class MainGameWidget(util.GroupBoxWidget):
    X = None
    Y = None
    Z = None
    curr_display = None
    def __init__(self, root, *args, **kwargs):
        super().__init__(root,title='CorpoPunk',*args, **kwargs)
        # Container to hold the two panels (main and right)
        self.se_btn = None
        self.s_btn = None
        self.sw_btn = None
        self.e_btn = None
        self.down_btn = None
        self.up_btn = None
        self.w_btn = None
        self.ne_btn = None
        self.n_btn = None
        self.skills_btn = None
        self.status_btn = None
        self.hands_box = None
        self.chest_box = None
        self.faction_box = None
        self.name_box = None
        self.xp_box = None
        self.level_box = None
        self.moneys_box = None
        self.hp_box = None
        self.head_box = None
        self.legs_box = None
        self.feet_box = None
        self.entry_box = None
        self.main_window = None
        self.location_bar = None
        self.nw_btn = None
        self.update_list = []
        self.commands = commands.CommandStructure(self.root, self)
        self.room_events = room_events.RoomEvents(self.root, self)
        self.location_name, self.location_desc, self.event = self.get_room_info()
        self.char_data = self.get_char_data()
        self.check_for_event()
        if not self.curr_display:
            self.curr_display = self.location_desc
        self.commands_list = [x for x in dir(self.commands) if not x.startswith('__')]
        self.container = qt.QtWidgets.QHBoxLayout()
        # Add the container to our GroupBox
        self.gblayout.addLayout(self.container)
        # A vertical main panel
        self.main_panel = qt.QtWidgets.QVBoxLayout()
        # Add main panel to container
        self.container.addLayout(self.main_panel)

        # Left panel is main display and command entry bar
        self.left_panel()

        # Right panel for various displays and buttons
        self.right_panel()
        self.show()

    def check_for_event(self, *args, **kwargs):
        if self.event:
            print(self.event)
            event_split = self.event.split('; ')
            evt = event_split[0]
            arg_str = ', '.join(event_split[1:])
            getattr(self.room_events, evt, None)(arg_str)

    def get_char_data(self):
        raw_data =  self.root.sql.select('main',
                                    table='Characters',
                                    where={'char_id': self.root.curr_char_id})[0]

        columns = self.root.sql.column_names('main', table='Characters')
        data_dict = {x: y for x, y in zip(columns, raw_data)}


        return data_dict

    def get_room_info(self):
        self.X, self.Y, self.Z = self.root.sql.select('main',
                                      table='Characters',
                                      columns=['X', 'Y', 'Z'],
                                      where={'char_id': self.root.curr_char_id})[0]

        res = self.root.sql.select('main',
                                    table='Locations',
                                    where={'X': self.X,
                                           'Y': self.Y,
                                           'Z': self.Z},
                                    )[0]

        data_dict = {x: y for x, y in zip(self.root.sql.column_names('main', table='Locations'), res)}
        del(data_dict['locationID'])
        self.exits = [x for x, y in data_dict.items() if y == 1]
        display_exits = [x.title() for x in self.exits]
        data_dict['locationDesc'] += f'\nExits: {', '.join(display_exits)}'

        return data_dict['locationName'], data_dict['locationDesc'], data_dict['event']

    def refresh(self):
        self.char_data = self.get_char_data()
        self.location_name, self.location_desc, event = self.get_room_info()
        self.location_bar.setText(f'{self.X}, {self.Y}, {self.Z} - {self.location_name}')
        # NEED TO CHANGE HOW MAIN DISPLAY IS POPULATED HERE AND IN INIT
        self.curr_display = self.location_desc
        self.main_window.setText(self.curr_display)
        self.name_box.setText(self.root.curr_char_name)
        self.level_box.setText(str(self.char_data["level"]))
        self.xp_box.setText(str(self.char_data["xp"]))
        self.faction_box.setText(self.char_data["faction"])
        self.moneys_box.setText(str(self.char_data["moneys"]))
        self.hp_box.setText(f'{self.char_data["curr_hp"]}/{self.char_data["hp"]}')
        self.head_box.setText(self.char_data["head"])
        self.chest_box.setText(self.char_data["chest"])
        self.hands_box.setText(self.char_data["hands"])
        self.legs_box.setText(self.char_data["legs"])
        self.feet_box.setText(self.char_data["feet"])
        self.check_for_event()


    def send_command(self):
        # split user input by spaces
        user_in_split = self.entry_box.text().strip().lower().split(' ')
        # First word is command
        user_in = user_in_split[0]
        # Second through the end are arguments
        args = ', '.join(user_in_split[1:])
        self.update_main(f'{user_in}')
        self.entry_box.clear()
        if user_in:
            if user_in in self.commands_list:
                getattr(self.commands, user_in, None)(args)
            else:
                possible_commands = [x for x in self.commands_list if x.startswith(user_in)]
                if len(possible_commands) == 1:
                    getattr(self.commands, possible_commands[0], None)(args)
                elif len(possible_commands) > 1:
                    self.update_main(f'{user_in} could refer to multiple commands:')
                    for poss_cmd in possible_commands:
                        self.update_main(f'{poss_cmd}')

    def update_main(self, text):
        self.curr_display += f'\n{text}'
        self.main_window.setText(self.curr_display)

    def left_panel(self):
        # Main panel will consist of location bar, room desc, main window, and entry bar
        self.location_bar = qt.LineEdit(self.root,
                                        text=f'{self.X}, {self.Y}, {self.Z} - {self.location_name}',
                                        layout=self.main_panel)
        # Make it green with black background and readonly for that old school feeeeel
        make_terminal(self.location_bar)

        # A text edit window set to readonly will act as our main window.
        self.main_window = qt.TextEdit(self.root,
                                       text=f'{self.curr_display}',
                                       layout=self.main_panel)
        self.update_list.append((self.main_window, f'{self.curr_display}'))
        # Make it green with black background and readonly
        make_terminal(self.main_window)
        # Set the minimum size of the main window
        self.main_window.setMinimumSize(1000, 750)

        # Layout to put the entry carat, entry bar, and enter button in
        entry_layout = qt.QtWidgets.QHBoxLayout()
        self.main_panel.addLayout(entry_layout)
        # Label for carat
        entry_label = qt.LineEdit(self.root,
                                  text='>',
                                  layout=entry_layout)
        # Make it so it stays its normal size.
        entry_label.setMinimumSize(20, 20)
        entry_label.setMaximumSize(20, 20)
        # Make it green with black background and readonly
        make_terminal(entry_label)
        # Entry box will be a line edit
        self.entry_box = qt.LineEdit(self.root,
                                     placeholderText='Enter command',
                                     layout=entry_layout)

        # Make text green for that old school feeeeeel!
        self.entry_box.setStyleSheet('background-color:black; color:green')
        # Make it so when entry_box has focus, enter sends the command.
        self.entry_box.returnPressed.connect(self.send_command)
        self.entry_box.setFocus()
        # Send button
        send_button = qt.PushButton(self.root,
                                    text='Send Command',
                                    layout=entry_layout,
                                    func=self.send_command)

    def right_panel(self):
        # Right panel for things like inventory
        right_panel = qt.QtWidgets.QVBoxLayout()
        self.container.addLayout(right_panel)
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
        self.name_box.setMinimumSize(300, 20)

        # Make it green with black background and readonly
        make_terminal(self.name_box)

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
        make_terminal(self.level_box)

        # Label for XP
        xp_label = qt.Label(self.root,
                            text='Experience:',
                            layout=level_layout)
        # LineEdit to show XP
        self.xp_box = qt.LineEdit(self.root,
                                  text=f'{self.char_data["xp"]}',
                                  layout=level_layout)
        # Make it green with black background and readonly
        make_terminal(self.xp_box)

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
        make_terminal(self.faction_box)

        # Layout for Status and Skills buttons
        status_skills_layout = qt.QtWidgets.QHBoxLayout()
        right_panel.addLayout(status_skills_layout)

        # Status Button
        self.status_btn = qt.PushButton(self.root,
                                        text='Status',
                                        layout=status_skills_layout,
                                        func=self.commands.status)

        self.skills_btn = qt.PushButton(self.root,
                                        text='Skills',
                                        layout=status_skills_layout,
                                        func=self.commands.skills)

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
        make_terminal(self.moneys_box)

        # Button that displays contents of character's inventory
        inventory = qt.PushButton(self.root,
                                  text='Inventory',
                                  layout=moneys_layout,
                                  func=self.commands.inventory)

        # Layout for hp and its label
        hp_layout = qt.QtWidgets.QHBoxLayout()
        right_panel.addLayout(hp_layout)
        # Label
        hp_label = qt.Label(self.root,
                            text='Hit Points:',
                            layout=hp_layout)
        # hp box
        self.hp_box = qt.LineEdit(self.root,
                                  text=f'{self.char_data["curr_hp"]}/{self.char_data["hp"]}',
                                  layout=hp_layout)

        # Make it green on black background
        # Eventually want to add if statement here to change text color based on
        make_terminal(self.hp_box)

        # Label for worn on
        worn_label = qt.Label(self.root,
                              text='Worn on:',
                              layout=right_panel)
        worn_label.setMaximumSize(300, 20)

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
        make_terminal(self.head_box)

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
        make_terminal(self.chest_box)

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
        make_terminal(self.hands_box)

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
        make_terminal(self.legs_box)

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
        make_terminal(self.feet_box)

        spacer_label = qt.Label(self.root,
                                text='',
                                layout=right_panel)

        right_panel.addStretch()
        # Now we'll add directional buttons
        # We'll start with a container for all of it
        button_container = qt.QtWidgets.QGridLayout()
        right_panel.addLayout(button_container)

        button_container.setRowStretch(0, 1)
        button_container.setColumnStretch(0, 1)
        # Now our top row of buttons X=0, y=1-3
        self.nw_btn = qt.PushButton(self.root,
                                    text='NW',
                                    layout=button_container,
                                    loc=(1,1),
                                    func=lambda: self.commands.go('northwest'))
        self.nw_btn.setMinimumSize(55, 55)
        self.nw_btn.setMaximumSize(55, 55)
        self.n_btn = qt.PushButton(self.root,
                                    text='N',
                                    layout=button_container,
                                    loc=(1,2),
                                   func=lambda: self.commands.go('north'))
        self.n_btn.setMinimumSize(55, 55)
        self.n_btn.setMaximumSize(55, 55)
        self.ne_btn = qt.PushButton(self.root,
                                    text='NE',
                                    layout=button_container,
                                    loc=(1,3),
                                    func=lambda: self.commands.go('northeast'))
        self.ne_btn.setMinimumSize(55, 55)
        self.ne_btn.setMaximumSize(55, 55)
        button_container.setColumnStretch(4, 1)
        # Second row of buttons. The middle "button" will be a vertical layout with up and down buttons in it
        self.w_btn = qt.PushButton(self.root,
                                   text='W',
                                   layout=button_container,
                                   loc=(2,1),
                                   func=lambda: self.commands.go('west'))
        self.w_btn.setMinimumSize(55, 55)
        self.w_btn.setMaximumSize(55, 55)
        # A vertical layout for our up and down buttons
        up_dn_layout = qt.QtWidgets.QVBoxLayout()
        button_container.addLayout(up_dn_layout, 2, 2, alignment=qt.QtCore.Qt.AlignmentFlag.AlignCenter)
        # up button
        self.up_btn = qt.ToolButton(self.root,
                                    layout=up_dn_layout,
                                    func=lambda: self.commands.go('up'))

        self.up_btn.setArrowType(qt.QtCore.Qt.ArrowType.UpArrow)
        self.up_btn.setMinimumSize(50, 27)
        self.up_btn.setMaximumSize(50, 27)

        # Down button
        self.down_btn = qt.ToolButton(self.root,
                                      layout=up_dn_layout,
                                      func=lambda: self.commands.go('down'))

        self.down_btn.setArrowType(qt.QtCore.Qt.ArrowType.DownArrow)
        self.down_btn.setMinimumSize(50, 27)
        self.down_btn.setMaximumSize(50, 27)
        # East button
        self.e_btn = qt.PushButton(self.root,
                                   text='E',
                                   layout=button_container,
                                   loc=(2,3),
                                   func=lambda: self.commands.go('east'))
        self.e_btn.setMinimumSize(55, 55)
        self.e_btn.setMaximumSize(55, 55)
        self.sw_btn = qt.PushButton(self.root,
                                    text='SW',
                                    layout=button_container,
                                    loc=(3,1),
                                    func=lambda: self.commands.go('southwest'))
        self.sw_btn.setMinimumSize(55, 55)
        self.sw_btn.setMaximumSize(55, 55)
        self.s_btn = qt.PushButton(self.root,
                                   text='S',
                                   layout=button_container,
                                   loc=(3,2),
                                   func=lambda: self.commands.go('south'))
        self.s_btn.setMinimumSize(55, 55)
        self.s_btn.setMaximumSize(55, 55)
        self.se_btn = qt.PushButton(self.root,
                                    text='SE',
                                    layout=button_container,
                                    loc=(3,3),
                                    func=lambda: self.commands.go('southeast'))
        self.se_btn.setMinimumSize(55, 55)
        self.se_btn.setMaximumSize(55, 55)
        button_container.setRowStretch(4, 1)
        button_container.setContentsMargins(0, 0, 0, 0)
        up_dn_layout.setContentsMargins(0, 0, 0, 0)

