#!/usr/bin/python3
import member
import os
import tkinter
import tkinter.filedialog as filedialog

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

        frame = tkinter.Frame(self.__window)
        self.__load_button = tkinter.Button(frame, text='Load Member File', anchor=tkinter.W, command=self.load_members)
        self.__load_button.pack(side='left')
        self.__save_button = tkinter.Button(frame, text='Save Member File', anchor=tkinter.W, command=self.save_members)
        self.__save_button.pack(side='left')
        frame.pack()

        # Build a Frame consisting of a Label and Entry widget for each field
        self.build_input_frame('Name: ', self.__name)

        # Build a new Frame and add three Buttons
        frame = tkinter.Frame(self.__window)
        self.__add_button = tkinter.Button(frame, text='Add Member', anchor=tkinter.W, command=self.add_member)
        self.__add_button.pack(side='left')
        self.__delete_button = tkinter.Button(frame, text='Delete Member', anchor=tkinter.W, command=self.delete_member,
                                              state=tkinter.DISABLED)
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
        self.__match_button = tkinter.Button(frame, text='Match Members', anchor=tkinter.W, command=self.match)
        self.__match_button.pack(side='left')
        frame.pack()

        frame = tkinter.Frame(self.__window)
        label = tkinter.Label(frame, text='Matched Members')
        self.__matched_members_list = tkinter.Listbox(frame, width=120)
        label.pack()
        self.__matched_members_list.pack()
        frame.pack()

    def build_input_frame(self, label, text_variable):
        """Build the top frames of the window for being able to enter data."""
        frame = tkinter.Frame(self.__window)
        label = tkinter.Label(frame, text=label, width=15, anchor=tkinter.W)
        entry = tkinter.Entry(frame, textvariable=text_variable, width=30)
        label.pack(side='left')
        entry.pack(side='right')
        frame.pack()

    def load_members(self):
        members_file = filedialog.askopenfile(initialdir=os.getcwd(), title="Open file",
                                              filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        try:
            for person in members_file:
                c = member.Member(person[:-1])
                self.__members.append(c)
                self.__members_list.insert(tkinter.END, str(c))
        except TypeError:
            pass

        try:
            members_file.close()
        except AttributeError:
            pass

        self.after_selected_operation()

    def save_members(self):
        members_file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save file",
                                                    filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        output_file = open(members_file, 'w')
        for person in self.__members:
            output_file.write('{}\n'.format(person.get_name()))

        try:
            output_file.close()
        except AttributeError and FileNotFoundError:
            pass

        self.after_selected_operation()

    def add_member(self):
        """Get the values from the bound variables and create a new Member."""
        if self.__name.get() != '':
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
        matched_members = []

        for person in self.__members:
            local_members.append(str(person))

        # Shuffle members three times
        shuffle(local_members)
        shuffle(local_members)
        shuffle(local_members)

        print()
        for i in range(len(local_members)):
            c = (local_members[i - 1], local_members[i])
            matched_members.append(c)
            print('{} - {}'.format(c[0], c[1]))
            # TODO: get matched members to display in a listbox
            try:
                self.__matched_members_list.insert(tkinter.END, str('{} - {}'.format(c[0], c[1])))
            except TypeError as e:
                # print(e)
                pass

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
