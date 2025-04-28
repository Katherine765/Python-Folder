from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from time import sleep

# don't currently have a way of seeing only some tasks
# would probably want a way to do that based on attribute and a way to do that manually but that gets complicated fast

class Task:
    attributes = ('ID','Task','Subtasks','Status','Due Date', 'Tags')

    def __init__(s, ID):
        s.fields = {'ID':str(ID), **{attribute:'' for attribute in Task.attributes[1:]}}
        s.edit('Add task')

    def edit(s, submit_text):
        root = Tk()

        entries = {}
        for field, text in list(s.fields.items())[1:]:
            ttk.Label(root, text=field).pack()
            entries[field] = ttk.Entry(root)
            entries[field].pack()
            entries[field].insert(0, text)

        def submit():
            for field, entry in list(entries.items()): # entries dict is one shorter than fields dict
                s.fields[field] = entry.get()      
            root.destroy()
            root.quit()

        ttk.Button(root, text = submit_text, command=submit).pack()
        root.mainloop()

    def get_row_tuple(s):
        return tuple(s.fields.values())



class To_do:
    def __init__(s, storage=[]):
        # storage IS the tasks list bc i'm too lazy to update separate variables
        s.storage = storage
        

        s.root = Tk()
        s.root.title('To-do')

        #menu
        menu_bar = Menu(s.root)
        menu = Menu(menu_bar, tearoff=False)
        functions = {'Add task': s.add_task, 'Edit task': s.edit_task, 'Delete tasks': s.delete_tasks, 'Clear tasks':s.clear_tasks, 'Sort tasks': s.sort_tasks}
        for label, command in functions.items():
            menu.add_command(label=label, command = command)
        menu_bar.add_cascade(label='Functions', menu = menu)
        s.root.config(menu = menu_bar)

        # table
        s.table = ttk.Treeview(s.root, columns = Task.attributes, show='headings')
        for attribute in Task.attributes:
            s.table.heading(attribute, text = attribute)
        s.table.pack(fill='both', expand=True)

        s.update_table() # in case storage was uploaded

        s.root.mainloop()


    def add_task(s):
        ID = max([int(task.fields['ID']) for task in s.storage]+[-1]) + 1
        s.storage.append(Task(ID))
        s.update_table()

    def edit_task(s):
        def submit():
            task = next((task for task in s.storage if task.fields['ID'] == entry.get()), None)
            root2.destroy()
            root2.quit()
            if task:
                task.edit('Edit task')
                s.update_table()

        root2=Tk()
        ttk.Label(root2, text='Task ID to edit').pack()
        entry = ttk.Entry(root2)
        entry.pack()
        ttk.Button(root2, text='Select', command=submit).pack()
        root2.mainloop()


    def delete_tasks(s):
        def submit():
            inputs = [item.strip() for item in entry.get().split(",")]
            root2.destroy()
            root2.quit()

            IDs = [item for item in inputs if item in [task.fields['ID'] for task in s.storage]]
            s.storage = [task for task in s.storage if not task.fields['ID'] in IDs]
            s.update_table()


        root2 = Tk()
        ttk.Label(root2, text='Task IDs to delete').pack() # separated by comma
        entry = ttk.Entry(root2)
        entry.pack()
        ttk.Button(root2, text='Delete tasks', command=submit).pack()

        root2.mainloop()


    def clear_tasks(s):
        if messagebox.askyesno('','Confirm task clearing?'):
            s.storage = []
            s.update_table()
    
    def update_table(s):
        # is this the best way of doing this?
        for row in s.table.get_children():
            s.table.delete(row)

        for task in s.storage:
            s.table.insert(parent='',index=END,values=task.get_row_tuple())


    def sort_tasks(s):
        def submit():
            attribute = entry.get()
            root2.destroy()
            root2.quit()
            if attribute in Task.attributes:
                s.storage = sorted(s.storage, key = lambda task: task.fields[attribute])
                s.update_table()

        root2 = Tk()
        ttk.Label(root2, text='Attribute to sort by').pack()
        entry = ttk.Entry(root2)
        entry.pack()
        ttk.Button(root2, text='Submit', command=submit).pack()

        root2.mainloop()
        