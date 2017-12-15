#!/usr/bin/python3
import member
import tkinter


class Application:
    def __init__(self):
        # Variables that hold application variables
        self.__members = []
        self.__selected_index = -1
        self.__selected_member = None

        # Window variables
        self.__window = tkinter.Tk()
        self.__window.title('People Mixer')

        # StringVar objects for entry
        self.__member_name = tkinter.StringVar()

        # Build input frames
        self.build_input_frame('Member name: ', self.__member_name)

        # Build frame and add buttons
        frame = tkinter.Frame(self.__window)
        self.__add_button = tkinter.Button(frame, text='Add Member',
                                           anchor=tkinter.W, command=self.add_member)
        self.__add_button.pack(side='left')
        self.__delete_button = tkinter.Button(frame, text='Delete Contact',
                                              anchor=tkinter.W,
                                              command=self.delete_member, state=tkinter.DISABLED)
        self.__delete_button.pack()
        frame.pack()

        # Now, we will use a Listbox widget to display our Contacts
        frame = tkinter.Frame(self.__window)
        label = tkinter.Label(frame, text='Members of the swap')
        self.__member_list = tkinter.Listbox(frame, width=120, selectmode=tkinter.SINGLE)
        # .bind is a special method that lets us connect a method in our
        # Application class definition with the user's action of clicking on
        # a row in our Listbox
        self.__member_list.bind('<<ListboxSelect>>', self.select_contact)
        label.pack()
        self.__member_list.pack()
        frame.pack()

    def build_input_frame(self, label, text_variable):
        """Build the top frames for entering names."""
        frame = tkinter.Frame(self.__window)
        label = tkinter.Label(frame, text=label, width=15, anchor=tkinter.W)
        entry = tkinter.Entry(frame, textvariable=text_variable, width=30)
        label.pack(side='left')
        entry.pack(side='right')
        frame.pack()

    def add_member(self):
        """Get the values from the bound variables and create a new Contact."""
        m = member.Member(self.__member_name.get())
        self.__members.append(m)

        # Add this Contact's __str__ output to the listbox
        self.__members.insert(tkinter.END, str(m))

    def select_contact(self, event):
        """Get the Contact at the index selected, and set the Entry fields
           with its values."""
        # Get the current selection from the Listbox. curselection() returns
        # a tuple and we want the first item
        # Get the current selection from the Listbox. curselection() returns
        # a tuple and we want the first item
        current_selection = self.__member_list.curselection()
        if current_selection:
            self.__selected_index = current_selection[0]

            # Grab the Contact object from self.__contacts at that index
            self.__selected_member = self.__members[self.__selected_index]

            # Use it's values to set the StringVars
            self.__member_name.set(self.__selected_member.get_first_name())

            # Make sure the Delete button is enabled
            self.__delete_button.config(state=tkinter.NORMAL)

    def delete_member(self):
        """Remov the Contact at the index selected then set the Entry fields
           to empty values."""
        if 0 <= self.__selected_index < len(self.__members):
            del self.__members[self.__selected_index]
            self.__members.remove(self.__selected_index)

            # Call the method to deselect the item, clear Entry fields, and
            # disable buttons.
            self.after_selected_operation()

    def save_contact(self):
        """Set the selected Contact's fields and then persist its __str__
           representation to the Listbox."""
        self.__selected_member.set_first_name(self.__member_name.get())

        # Listbox widgets don't have a way of updating an item in place. So
        # We'll delete the item at a particular index and then add it
        self.__members.remove(self.__selected_index)
        self.__members.insert(self.__selected_index, str(self.__selected_member))

        # Call the method to deselect the item, clear Entry fields, and
        # disable buttons.
        self.after_selected_operation()

    def after_selected_operation(self):
        """Clear the selected index, contact, and disable buttons."""
        self.__selected_index = -1
        self.__selected_member = None

        self.__member_name.set('')

        # Make sure the Delete button is disabled
        self.__delete_button.config(state=tkinter.DISABLED)

    @staticmethod
    def start():
        """This method starts our GUI application."""
        tkinter.mainloop()


def main():
    app = Application()
    app.start()


main()
