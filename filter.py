import json
import tkinter as tk
from tkinter import ttk


data=None
#create ui for filtering
root = tk.Tk()
root.title('Filter')
#display height and width
root.geometry("1500x1500")


var1 = tk.IntVar()
var2 = tk.IntVar()
var3 = tk.IntVar()
var4 = tk.IntVar()

c1 = tk.Checkbutton(root, text="Daten mit keinem TER entfernen", variable=var1)
c2 = tk.Checkbutton(root, text="Ausschüttend", variable=var2)
c3 = tk.Checkbutton(root, text="keine Sparkosten", variable=var3)
c4 = tk.Checkbutton(root, text="Thesaurierend", variable=var4)

c1.pack()
c2.pack()
c3.pack()
c4.pack()

def filter():
    #remove table if it exists
    for widget in root.winfo_children():
        if widget.winfo_class() == 'Treeview':
            widget.destroy()
    #remove scrollbar if it exists
    for widget in root.winfo_children():
        if widget.winfo_class() == 'Scrollbar':
            widget.destroy()

    with open('everything_sparkosten.json') as data_file:  
        global data
        data = json.load(data_file)
        if var1.get() == 1:
            data = [x for x in data if x['ter'] >= 0]
        if var2.get() == 1:
            data = [x for x in data if x['isDistributing'] == True]
        if var3.get() == 1:
            data = [x for x in data if x['sparkosten'] != 'ja']
        if var4.get() == 1:
            data = [x for x in data if x['isDistributing'] == False]
    visualize()

#visualize filtered data as a table
def visualize():
    # Table with max height and width
    table = ttk.Treeview(root, columns=(1,2,3,4), show="headings",  height="30", selectmode="browse")
    table.column(1, width=600, minwidth=500)
    table.column(2, width=200, minwidth=200)
    table.column(3, width=200, minwidth=200)
    table.column(4, width=300, minwidth=200)
    table.pack()

    table.heading(1, text="Name")
    table.heading(2, text="Sparkosten")
    table.heading(3, text="TER")
    table.heading(4, text="ISIN")

    for x in data:
        table.insert("", tk.END, values=(x['name'], x['sparkosten'], x['ter'], x['number']))

    # Scrollbar
    vsb = ttk.Scrollbar(root, orient="vertical", command=table.yview)
    vsb.pack(side=tk.RIGHT, fill='y')
    table.configure(yscrollcommand=vsb.set)

    #make table sortable by clicking on the header, ter is sorted by number
    table.heading(1, text="Name", command=lambda: sortby(table, 1, False))
    table.heading(2, text="Sparkosten", command=lambda: sortby(table, 2, False))
    table.heading(3, text="TER", command=lambda: sortby(table, 3, False))
    table.heading(4, text="ISIN", command=lambda: sortby(table, 4, False))



def sortby(tree, col, descending):#
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) for child in tree.get_children('')]
    # reorder data
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so that it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, int(not descending)))


b1 = tk.Button(root, text='Suchen', command=filter)
b1.pack()

root.mainloop()


