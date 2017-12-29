#!/usr/bin/python3
import member
import tkinter

from random import shuffle


class Application:
    def __init__(self):
        # Build a list that will hold Member objects, an int to used when
        # we want to select a particular Member, and a variable that will
        # point to our selected Member once chosen.
        self.__members = []
        self.__selected_index = -1
        self.__selected_member = None

        self.__window = tkinter.Tk()
        self.__window.title('Member Matcher')

        # Create four StringVar objects to be bound to the Entry widgets
        self.__name = tkinter.StringVar()

        # TODO: add buttons for load/save list from/to a file

        # Build a Frame consisting of a Label and Entry widget for each field
        self.build_input_frame('First Name: ', self.__name)

        # Build a new Frame and add three Buttons
        frame = tkinter.Frame(self.__window)
        self.__add_button = tkinter.Button(frame, text='Add Member', anchor=tkinter.W, command=self.add_member)
        self.__add_button.pack(side='left')
        self.__delete_button = tkinter.Button(frame, text='Delete Member', anchor=tkinter.W, command=self.delete_member, state=tkinter.DISABLED)
        self.__delete_button.pack(side='left')
        frame.pack()

        # Now, we will use a Listbox widget to display our Members
        frame = tkinter.Frame(self.__window)
        label = tkinter.Label(frame, text='Your Members')
        self.__members_list = tkinter.Listbox(frame, width=120, selectmode=tkinter.SINGLE)
        # .bind is a special method that lets us connect a method in our
        # Application class definition with the user's action of clicking on
        # a row in our Listbox
        self.__members_list.bind('<<ListboxSelect>>', self.select_member)
        label.pack()
        self.__members_list.pack()
        frame.pack()

        frame = tkinter.Frame(self.__window)
        self.__match_button = tkinter.Button(frame, text='Save Member', anchor=tkinter.W, command=self.match)
        self.__match_button.pack(side='left')
        frame.pack()

        # frame = tkinter.Frame(self.__window)
        # label = tkinter.Label(frame, text='Matched Members')
        # self.__matched_members_list = tkinter.Listbox(frame, width=120, selectmode=tkinter.NONE)
        # label.pack()
        # self.__matched_members_list.pack()
        # frame.pack()

    def build_input_frame(self, label, text_variable):
        """Build the top frames of the window for being able to enter data."""
        frame = tkinter.Frame(self.__window)
        label = tkinter.Label(frame, text=label, width=15, anchor=tkinter.W)
        entry = tkinter.Entry(frame, textvariable=text_variable, width=30)
        label.pack(side='left')
        entry.pack(side='right')
        frame.pack()

    def add_member(self):
        """Get the values from the bound variables and create a new Member."""
        c = member.Member(self.__name.get())
        self.__members.append(c)

        # Add this Member's __str__ output to the listbox
        self.__members_list.insert(tkinter.END, str(c))

        self.after_selected_operation()

    def select_member(self, event):
        """Get the Member at the index selected, and set the Entry fields
           with its values."""
        # Get the current selection from the Listbox. curselection() returns
        # a tuple and we want the first item
        # Get the current selection from the Listbox. curselection() returns
        # a tuple and we want the first item
        current_selection = self.__members_list.curselection()
        if current_selection:
            self.__selected_index = current_selection[0]

            # Grab the Member object from self.__members at that index
            self.__selected_member = self.__members[self.__selected_index]

            # Use it's values to set the StringVars
            self.__name.set(self.__selected_member.get_name())

            # Make sure the Save button is enabled
            self.__match_button.config(state=tkinter.NORMAL)
            self.__delete_button.config(state=tkinter.NORMAL)

    def delete_member(self):
        """Remove the Member at the index selected then set the Entry fields
           to empty values."""
        if 0 <= self.__selected_index < len(self.__members):
            del self.__members[self.__selected_index]
            self.__members_list.delete(self.__selected_index)

            # Call the method to deselect the item, clear Entry fields, and
            # disable buttons.
            self.after_selected_operation()

    def match(self):
        self.__matched_members_list = []
        local_members = []
        for person in self.__members:
            local_members.append(str(person))

        shuffle(local_members)

        for i in range(len(local_members)):
            pair = '{} - {}'.format(local_members[i - 1], local_members[i])
            print(pair)
            # self.__matched_members_list.insert(tkinter.END, str(pair))

        self.after_selected_operation()

    def after_selected_operation(self):
        """Clear the selected index, member, and disable buttons."""
        self.__selected_index = -1
        self.__selected_member = None

        self.__name.set('')

        # Make sure the Save and Delete buttons are disabled
        self.__delete_button.config(state=tkinter.DISABLED)

    @staticmethod
    def start():
        """This method starts our GUI application."""
        tkinter.mainloop()


def main():
    app = Application()
    app.start()


main()
