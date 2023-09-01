from tkinter import*
from tkinter import filedialog
from tkinter import messagebox
import tkinter.ttk as ttk
import tkinter.font
import os
from ttkthemes import*
import idlelib.colorizer as ic
import idlelib.percolator as ip
import re


#creates window
root = ThemedTk()
root.geometry("860x460")
root.title("PyTXedit")
root.resizable(True, True)
root.iconbitmap(r"dat/code.ico")


cdg = ic.ColorDelegator()
cdg.prog = re.compile(r'\b(?P<MYGROUP>tkinter)\b|' + ic.make_pat().pattern, re.S)
cdg.idprog = re.compile(r'\s+(\w+)', re.S)

cdg.tagdefs['COMMENT'] = {'foreground': '#013ADF', 'background': '#FFFFFF'}
cdg.tagdefs['KEYWORD'] = {'foreground': '#7401DF', 'background': '#FFFFFF'}
cdg.tagdefs['BUILTIN'] = {'foreground': '#DF01D7', 'background': '#FFFFFF'}
cdg.tagdefs['STRING'] = {'foreground': '#DF7401', 'background': '#FFFFFF'}
cdg.tagdefs['DEFINITION'] = {'foreground': '#DF013A', 'background': '#FFFFFF'}


#define variables
global fob,tx,clib, status, listoffiles,vissible
fob = ''
tx = ''
clib = ''
vissible = True
status = StringVar()
status.set('Ln : 0 Col: 0')
listoffiles = []


#include creation
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)



Filelist = Frame(root, width = 150)
Filelist.pack(side=LEFT, fill=Y)
Closelist = Frame(root, width = 30)
Closelist.pack(side=LEFT, fill=Y)

Toolbar = Frame(root, height = 34)
Toolbar.pack(side=TOP, fill=X)

  
tabControl.add(tab1, text ='Code')
tabControl.add(tab2, text ='Detail')
tabControl.pack(expand = True,side=TOP, fill =BOTH)

scroller = ttk.Scrollbar(tab1)
scroll_hor = ttk.Scrollbar(tab1, orient='horizontal')
text_widget = Text(tab1)
detail_widget = Text(tab2)


scroller.pack(side=RIGHT, fill=Y)
scroll_hor.pack(side=BOTTOM, fill=X)
text_widget.pack(side=TOP, expand=True, fill = BOTH)
detail_widget.pack(side=TOP, expand=True, fill=BOTH)

scroller.config(command=text_widget.yview)
scroll_hor.config(command=text_widget.xview)
text_widget.config(yscrollcommand=scroller.set, wrap='none', xscrollcommand = scroll_hor.set,relief = 'flat')
detail_widget.config(relief = 'flat', state = DISABLED)
text_widget.config(undo = True)

global size
size = 10
text_widget.configure(font=("Courier New", size, "bold"))
ip.Percolator(text_widget).insertfilter(cdg)



# status bar creation
statusbar = ttk.Label(root, textvariable=status, anchor=W)
statusbar.pack(side=BOTTOM, fill = X)

#file functions
def open_file(e = False):
    global fob, tx
    if tx != text_widget.get("1.0",END)and tx != "" :
        save_file()
    fob = filedialog.askopenfilename()
    if fob == '':
        pass
    else:
        file = open(fob, "r")
        tx = file.read()
        text_widget.delete("1.0","end")
        text_widget.insert("1.0", tx)
        file.close()
        displayed_name = fob.split("/")
        global listoffiles
        listoffiles.append(fob)
        textpiece = str(displayed_name[-1:])
        textpiece = textpiece.replace("['", " ")
        textpiece = textpiece.replace("']", " ")
        filebtn = Button(Filelist,text=str(len(listoffiles)) + textpiece,relief='flat')
        filebtn.pack()
        filebtn.configure(command=lambda b=filebtn: load_file(b))
        closebtn = Button(Closelist,text="X",relief='flat')
        closebtn.pack()
        closebtn.configure(command=lambda b=filebtn, c=closebtn: close_file(b, c))
    detail_widget.config(state = NORMAL)
    detail_widget.delete("1.0","end")
    if "." in fob:
        typeof = fob.split(".")
    else:
        typeof = ("a", "unknown_file")
    detail_widget.insert(END, fob+"\n"+str(len(str(text_widget.get("1.0",END)))) + " Letters(Last Save)\n."+typeof[len(typeof)-1]+" file")
    detail_widget.config(state = DISABLED)
    
def load_file(name):
    global listoffiles, fob, tx
    element = name.cget('text')[0]
    if tx != text_widget.get("1.0",END)and tx != "" :
          save_file()
    fob = listoffiles[int(element)-1]
    try:
        file = open(fob, "r")
        tx = file.read()
    except:
        name.pack_forget()
        del listoffiles[int(element)-1]
        return
    text_widget.delete("1.0","end")
    text_widget.insert("1.0", tx)
    file.close()
    detail_widget.config(state = NORMAL)
    detail_widget.delete("1.0","end")
    if "." in fob:
        typeof = fob.split(".")
    else:
        typeof = ("a", "unknown_file")
    detail_widget.insert(END, fob+"\n"+str(len(str(text_widget.get("1.0",END)))) + " Letters(Last Save)\n."+typeof[len(typeof)-1]+" file")
    detail_widget.config(state = DISABLED)
    
    
    print(listoffiles[int(element)-1])
def save_file(e = False):
    global fob
    if fob == '':
        save_as_file()
    else:
        file = open(fob, "w")
        file.write(text_widget.get("1.0",END+"-1c"))
        file.close()
    detail_widget.config(state = NORMAL)
    detail_widget.delete("1.0","end")
    if "." in fob:
        typeof = fob.split(".")
    else:
        typeof = ("a", "unknown_file")
    detail_widget.insert(END, fob+"\n"+str(len(str(text_widget.get("1.0",END)))) + " letters(Last Save)\n."+typeof[len(typeof)-1]+" file")
    detail_widget.config(state = DISABLED)
    
def save_as_file(e = False):
    global fob
    fob = filedialog.asksaveasfilename()
    if fob == '':
        pass
    else:
        file = open(fob, "w")
        file.write(text_widget.get("1.0",END))
        file.close()
        displayed_name = fob.split("/")
        global listoffiles
        listoffiles.append(fob)
        textpiece = str(displayed_name[-1:])
        textpiece = textpiece.replace("['", " ")
        textpiece = textpiece.replace("']", " ")
        filebtn = Button(Filelist,text=str(len(listoffiles)) + textpiece,relief='flat')
        filebtn.pack()
        filebtn.configure(command=lambda b=filebtn: load_file(b))
        closebtn = Button(Closelist,text="X",relief='flat')
        closebtn.pack()
        closebtn.configure(command=lambda b=filebtn, c=closebtn: close_file(b, c))
        detail_widget.config(state = NORMAL)
        detail_widget.delete("1.0","end")
    if "." in fob:
        typeof = fob.split(".")
    else:
        typeof = ("a", "unknown_file")
    detail_widget.insert(END, fob+"\n"+str(len(str(text_widget.get("1.0",END)))) + " Letters(Last Save)\n."+typeof[len(typeof)-1]+" file")
    detail_widget.config(state = DISABLED)

def close_file(name, xname):
    global tx, fob, listoffiles
    element = name.cget('text')[0]
    if tx != text_widget.get("1.0",END)and tx != "" :
         save_file()
    text_widget.delete("1.0","end")
    detail_widget.config(state = NORMAL)
    detail_widget.delete("1.0","end")
    name.pack_forget()
    xname.pack_forget()
    detail_widget.config(state = DISABLED)
    tx = text_widget.get("1.0",END)
    fob = ''

def new_emty(e = False):
    global tx, fob
    if tx != text_widget.get("1.0",END)and tx != "" :
         save_file()
    text_widget.delete("1.0","end")
    detail_widget.config(state = NORMAL)
    detail_widget.delete("1.0","end")
    detail_widget.config(state = DISABLED)
    tx = text_widget.get("1.0",END)
    fob = ''


# edit menu
def  cut_text(e):
    global clib
    if e:
      clib = root.clipboard_get()  
    elif text_widget.selection_get():
        clib = text_widget.selection_get()
        text_widget.delete("sel.first", "sel.last")
        root.clipboard_clear()
        root.clipboard_append(clib)
        
def copy_text(e):
    global clib
    if e:
      clib = root.clipboard_get() 
    elif text_widget.selection_get():
        clib = text_widget.selection_get()
        root.clipboard_clear()
        root.clipboard_append(clib)


def paste_text(e):
    global clib
    if e:
      clib = root.clipboard_get()
    elif clib != '':
        position = text_widget.index(INSERT)
        text_widget.insert(position, clib)

def run_file(e = False):
    global fob, tx
    if tx != text_widget.get("1.0",END)and tx != "" :
        save_file()
    if fob != '':
        os.startfile(fob)
def do_popup(event):
    try:
        mrc.tk_popup(event.x_root, event.y_root)
    finally:
        mrc.grab_release()
def select_all():
    text_widget.tag_add(SEL, "1.0", END)
    text_widget.mark_set(INSERT, "1.0")
    text_widget.see(INSERT)
    return 'break'
def zoom_in(e = False):
    global size
    if size < 30:
        size += 2
        text_widget.configure(font=("Courier New", size, "bold"))
def zoom_out(e = False):
    global size
    if size > 2:
        size -= 2
        text_widget.configure(font=("Courier New", size, "bold"))
def zoom_reset(e = False):
    global size
    size = 10
    text_widget.configure(font=("Courier New", size, "bold"))
def about_pop():
    messagebox.showinfo(title="About", message="PyTXedit is a simple Texeditor for Python\n ©Copyright 2023 Berend Schilcher\n MIT License found in programm folder")

#tobbar creation
menubar = Menu(root)
mrc = Menu(root, tearoff = False)
file_menu = Menu(menubar, tearoff = False)
edit_menu = Menu(menubar, tearoff = False)
run_menu = Menu(menubar, tearoff = False)
view_menu = Menu(menubar, tearoff = False)
help_menu = Menu(menubar, tearoff = False)
menubar.add_cascade(label="File", menu=file_menu)
menubar.add_cascade(label="Edit", menu=edit_menu)
menubar.add_cascade(label="Run", menu=run_menu)
menubar.add_cascade(label="View", menu=view_menu)
menubar.add_cascade(label="Help", menu=help_menu)

file_menu.add_command(label="Open",accelerator='Ctrl-O', command=open_file)
file_menu.add_command(label="Save",accelerator='Ctrl-S', command=save_file)
file_menu.add_command(label="Save as",accelerator='Ctrl-Alt-S', command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="New File",accelerator='Ctrl-N', command=new_emty)

edit_menu.add_command(label="Cut",accelerator='Ctrl-X', command=lambda: cut_text(False))
edit_menu.add_command(label="Copy",accelerator='Ctrl-C', command=lambda: copy_text(False))
edit_menu.add_command(label="Paste",accelerator='Ctrl-V', command=lambda: paste_text(False))
edit_menu.add_separator()
edit_menu.add_command(label="Undo", command=text_widget.edit_undo,accelerator='Ctrl-Z')
edit_menu.add_command(label="Redo", command=text_widget.edit_redo,accelerator='Ctrl-Y')

mrc.add_command(label="Cut",accelerator='Ctrl-X', command=lambda: cut_text(False))
mrc.add_command(label="Copy",accelerator='Ctrl-C', command=lambda: copy_text(False))
mrc.add_command(label="Paste",accelerator='Ctrl-V', command=lambda: paste_text(False))
mrc.add_separator()
mrc.add_command(label="Select All", command=select_all,accelerator='Ctrl-A')


run_menu.add_command(label="Run",accelerator='F5', command=run_file)

view_menu.add_command(label="Zoom In",accelerator='Ctrl+', command=lambda: zoom_in(False))
view_menu.add_command(label="Zoom Out",accelerator='Ctrl-', command=lambda: zoom_out(False))
view_menu.add_command(label="Reset Zoom",accelerator='Ctrl-R', command=lambda: zoom_reset(False))

help_menu.add_command(label="About", command=about_pop)


#toolbar and addbutton creation
undo_icon = PhotoImage(file='./dat/backward.png')
undo_icon = undo_icon.subsample(2, 2)

redo_icon = PhotoImage(file='./dat/forward.png')
redo_icon = redo_icon.subsample(2, 2)

zoom_in_icon = PhotoImage(file='./dat/zoom_in.png')
zoom_in_icon = zoom_in_icon.subsample(2, 2)

zoom_reset_icon = PhotoImage(file='./dat/reload.png')
zoom_reset_icon = zoom_reset_icon.subsample(2, 2)

zoom_out_icon = PhotoImage(file='./dat/zoom_out.png')
zoom_out_icon = zoom_out_icon.subsample(2, 2)

run_icon = PhotoImage(file='./dat/arrow.png')
run_icon = run_icon.subsample(2, 2)



undo_btn = Button(Toolbar,height=32,width=32, image=undo_icon, command=text_widget.edit_undo, relief="flat")
redo_btn = Button(Toolbar,height=32,width=32, image=redo_icon, command=text_widget.edit_redo, relief="flat")
zoom_in_btn = Button(Toolbar,height=32,width=32, image=zoom_in_icon, command= lambda: zoom_in(False), relief="flat")
zoom_reset_btn = Button(Toolbar,height=32,width=32, image=zoom_reset_icon, command= lambda: zoom_reset(False), relief="flat")
zoom_out_btn = Button(Toolbar,height=32,width=32, image=zoom_out_icon, command= lambda: zoom_out(False), relief="flat")
run_btn = Button(Toolbar,height=32,width=32, image=run_icon, command=run_file, relief="flat")


undo_btn.pack(side=LEFT)
redo_btn.pack(side=LEFT)

spacer = Label(Toolbar,text="")
spacer.pack(expand=True,side=LEFT,fill=X)
run_btn.pack(side=LEFT)
spacer_t = Label(Toolbar,text="")
spacer_t.pack(expand=True,side=LEFT,fill=X)

zoom_in_btn.pack(side=RIGHT)
zoom_reset_btn.pack(side=RIGHT)
zoom_out_btn.pack(side=RIGHT)




#bindings
root.bind('<Control-Key-n>', new_emty)
root.bind('<Control-Alt-n>', new_emty)
root.bind('<Control-Key-o>', open_file)
root.bind('<Control-Key-s>', save_file)
root.bind('<Control-Alt-s>', save_as_file)


root.bind('<Control-Key-x>', cut_text)
root.bind('<Control-Key-c>', copy_text)
root.bind('<Control-Key-v>', paste_text)

root.bind('<Key-F5>', run_file)
root.bind("<Button-3>", do_popup)

root.bind("<Control-plus>", zoom_in)
root.bind("<Control-minus>", zoom_out)
root.bind("<Control-Key-r>", zoom_reset)



#initializing
root.config(menu=menubar)
text_widget.focus_set()

def newline_add(event):
    full = text_widget.get("1.0",END)
    tcoord = text_widget.index(INSERT)
    po_duble = text_widget.get(tcoord+"-2c", tcoord+ " +1c")
    po_break = text_widget.get(tcoord+"-6c", tcoord+ " +1c")
    tcom_pos= int(tcoord.index("."))
    tcoord_x =tcoord[tcom_pos + 1:]
    breakable = 4
    if text_widget.get(tcoord+"-1line linestart", tcoord+ " -1line linestart+1c") ==' ':
        point = ' '
        string = text_widget.get(tcoord+"-1line linestart", tcoord+ " -1line lineend")
        for i in string:
            point = i
            if point != ' ':
                break
            if 'break' in  po_break and breakable > 0:
                breakable -= 1
            else:
                text_widget.insert(tcoord, i)
    if ':'in po_duble :
        text_widget.insert(INSERT, " " * 4)
def tab_add(arg):
    text_widget.insert(INSERT, "    ")
    return 'break'
def tab_del(e = False):
    full = text_widget.get("1.0",END)
    tcoord = text_widget.index(INSERT)
    text_widget.delete(tcoord+"-4c", tcoord)
def exit_all():
    if tx != text_widget.get("1.0",END):
        save_file()
    root.destroy()
    os._exit(0)
root.bind('<Return>', newline_add)
root.bind('<Control-Key-y>', tab_del)
text_widget.bind('<Tab>', tab_add)
root.protocol('WM_DELETE_WINDOW', exit_all)
        
while True:

    coord = text_widget.index(INSERT)
    com_pos= int(coord.index("."))
    coord_x =coord[com_pos + 1:]
    coord_old = com_pos - 1
    #print(text_widget.get(coord+"-1line linestart", coord+ " -1line linestart+1c"))
    #if coord_x == '0':
    #   text_widget.insert(text_widget.index(INSERT), 'a')
    coord_y =coord[:com_pos]
    status.set('Ln: ' + coord_y + '  Col: ' + coord_x)
    root.update()
