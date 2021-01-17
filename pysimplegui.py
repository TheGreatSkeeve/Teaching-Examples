import PySimpleGUI as sg

'''
PySimpleGUI is a pretty decent GUI library for Python.

Using the statement above, we import it as "sg", and can use "sg" to call / initialize various objects

I prefer to assign them to variables, and then call the variables when needed.  Up to you.

Good reference - https://pysimplegui.readthedocs.io/en/latest/call%20reference/
'''

#   Generate a text label
#   Testing, probably ignore me
def TextLabel(text):
    return sg.Text(text + ':', justification='r', size=(15, 1))

# Create a top bar menu
menu_def = [
            ['&File', ['&Open     Ctrl-O', '&Save       Ctrl-S', '&Properties', 'E&xit']],
            ['&Edit', ['&Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['&Toolbar', ['---', 'Command &1', 'Command &2',
                          '---', 'Command &3', 'Command &4']],
            ['&Help', '&About...'], ]

# Create a right click menu
right_click_menu = ['Unused', ['Right', '!&Click', '&Menu', 'E&xit', 'Properties']]



# Set the Theme
sg.theme('SystemDefault1')

# Create a button
#   "key" assigns a unique key to the button, so the program can tell if it is clicked
#   "bind_rettaskmgrurn_key" enables pressing enter to click the button
test_button = sg.Button("Button Text", key='-test_button-', button_color=('green', 'black'), bind_return_key=True)

# Create a text label
#   Edit text size with "size"
test_text = sg.Text("This is a test.", size=(30, 1),key='-test_text-')

# Get input from the user
test_input = sg.InputText(password_char="*",key='-test_input-')

# Create a checkbox
checkbox_name = sg.CBox('Do you like Python?', size=(10, 15), key="-checkbox_name-")

# You can create a Column to organize these elements if you want
# With the few that we have, it's not really worth it.
'''
column_new = sg.Col([
    [text_name], [input_name],
    [checkbox_name],
], justification="top")
'''

# Create a dropdown box
values = ["Jeffery","Donny","Walter","Brandt","Bunny"]
test_listbox = sg.Listbox(values=values,
                            size=(30, 15),
                            select_mode=sg.SELECT_MODE_EXTENDED,
                            key='-test_listbox-',
                            change_submits=True
                            )

# Create an output box
# This is a cool element, it will show you any output like from print, or from errors.
output = sg.Output(size=(175, 15), font='Helvetica 10', key='-output-', visible=True)

# Define the GUI's layout
layout = [
    [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
    [test_text, test_input, test_button],
    [checkbox_name],
    [test_listbox],
    [output]
]


# Create the GUI
window = sg.Window(
    'GUI Title', layout,
    default_element_size=(30, 2), resizable=True,
    font=('Helvetica', ' 13'),
    icon='icon.ico',
    default_button_element_size=(4, 1),
    return_keyboard_events=True,
    right_click_menu = right_click_menu

)


# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':     # if user closes window or clicks cancel
        break
    elif event == '-test_button-':
        print("\nButton Pressed!")
        print("Here's the test input:  " + values['-test_input-'])
        if values['-checkbox_name-'] == True:
            print("Checkbox is checked!")
        else:
            print("Checkbox is not checked!")
        print("You selected " + str(values['-test_listbox-'][0]))