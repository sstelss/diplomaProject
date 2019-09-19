from tkinter import *
from tkinter.filedialog import askopenfilename
import data_formats as df
import simulated_annealing as sim
import ant_thread as ant
import gibrid_al as gb
import new_bee as nb

def button_click():
    global path
    path = askopenfilename()
    print("Выбран файл с адресом: ", path)

#
path = ""
#
root=Tk()
root.title(u'Пример приложения')
root.geometry('500x400+300+200') # ширина=500, высота=400, x=300, y=200
root.resizable(False, False)



button1=Button(root,text='Выбирите файл',width=15,height=5, font='arial 14', command=button_click)
button1.pack()


label = Label(width=25, height=2)
label['text'] = "Муравьиный алгоритм"
label.pack(side='left')

text1=Text(root,height=2,width=2,font='Arial 14',wrap=WORD)
text1.pack()


root.mainloop()