from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from pathlib import Path
import time, os, sys, shutil

raam=Tk()
raam.title("Projekt")
tahvel = Canvas(raam, width=500, height=500, background="white")

#Joone omadused
paksus=IntVar()
paksus.set(2)
värv=StringVar()
värv.set("red")

#Teksti omadused
sisend=StringVar()
#Siia tuleb veel font

#Hiire positsioon
#ehiir on hiire positsioon "delay" sekundit tagasi, selle abil saab enamvähem sujuvalt joonistada
hiir_x=0
hiir_y=0
ehiir_x=0
ehiir_y=0
delay=0.02

def init_GUI():
    #_b- button,  _l- dropdown, _c- checkbox, _e entry
    
    #Joonistamis ala
    tahvel.grid(column=0, row=1, padx=5, pady=5, sticky=(E,N,S,W))
    tahvel.bind("<B1-Motion>", pliiats)
    tahvel.bind("<Motion>", hiire_positsioon)
    #Kõikide nuppude raam
    toolbar = ttk.Frame(height=2,relief=SUNKEN)
    toolbar.grid(column=0, row=0, padx=5, pady=5, sticky=(E,N,S,W))
    #Pliiatsi valimis nupp
    def pliiatsi_kasutus():
        tahvel.bind("<B1-Motion>", pliiats)
        tahvel.bind("<Button-1>", ignore)
    pliiats_b = ttk.Button(toolbar, text="Pliiats", command=pliiatsi_kasutus)
    pliiats_b.grid(column=0, row=0, padx=5, pady=5, sticky=(E,N,S,W))
    #Pintsli valimis nupp
    def pintsli_kasutus():
        tahvel.bind("<B1-Motion>", pintsel)
        tahvel.bind("<Button-1>", ignore)
    pintsel_b = ttk.Button(toolbar, text="Pintsel", command=pintsli_kasutus)
    pintsel_b.grid(column=1, row=0, padx=5, pady=5, sticky=(E,N,S,W))
    #Teksti valimis nupp
    def teksti_kasutus():
        tahvel.bind("<B1-Motion>", ignore)
        tahvel.bind("<Button-1>", tekst)
    tekst_b = ttk.Button(toolbar, text="Tekst", command=teksti_kasutus)
    tekst_b.grid(column=2, row=0, padx=5, pady=5, sticky=(E,N,S,W))
    #Paksuse valik
    global paksus
    paksus_e = ttk.Entry(toolbar, textvariable=paksus)
    paksus_e.grid(column=3, row=0, padx=5, pady=5, sticky=(E,N,S,W))
    #Värvi valik
    global värv
    VÄRVID=[" ","yellow","black", "red", "blue", "green"]
    värv_l = ttk.OptionMenu(toolbar, värv, *VÄRVID)
    värv_l.grid(column=4, row=0, padx=5, pady=5, sticky=(E,N,S,W))
    värv.set("red")
    #Tekst mida saab kuvada
    tekst_e = ttk.Entry(toolbar, textvariable=sisend)
    tekst_e.grid(column=5, row=0, padx=5, pady=5, sticky=(E,N,S,W))
    #Vali pilt mida kuvada
    pilt_b = ttk.Button(toolbar, text="Ava pilt", command=pilt)
    pilt_b.grid(column=6, row=0, padx=5, pady=5, sticky=(E,N,S,W))
    
#Kui on vaja et klahv nupp midagi ei teeks
def ignore(event):
    return 0
#Hiire koordinaatide registreerimine
def hiire_positsioon(event):
    global hiir_x, hiir_y, ehiir_x, ehiir_y, delay
    ehiir_x=hiir_x
    ehiir_y=hiir_y
    hiir_x=event.x
    hiir_y=event.y
    time.sleep(delay)
#Pliiatsiga joonistamine
def pliiats(event):
    global paksus, värv, hiir_x, hiir_y, delay
    delay=0.001
    hiire_positsioon(event)
    tahvel.create_line(ehiir_x,ehiir_y,hiir_x,hiir_y, width=paksus.get(), fill=värv.get())
#Pintsliga joonistamine
def pintsel(event):
    global paksus, värv, hiir_x, hiir_y, delay
    delay=0.001
    hiire_positsioon(event)
    tahvel.create_oval(hiir_x,hiir_y,hiir_x+paksus.get(),hiir_y+paksus.get(),fill=värv.get(),outline=värv.get())
#Kirjutamine
def tekst(event):
    global paksus, värv, hiir_x, hiir_y, sisend
    tahvel.create_text(hiir_x,hiir_y,fill=värv.get(),text=sisend.get(),anchor=SW)
#Pilt
def pilt():
    dir=filedialog.askopenfilenames(filetypes=(("Image files", "*.gif;*.pgm;*.ppm"),("All files", "*.*") ))
    dir=str(dir)[2:len(str(dir))-3]
    img_dir=dir
    while img_dir.find("/")!=-1:
        img_dir=img_dir[img_dir.find("/")+1:len(img_dir)]
    if not Path(img_dir).is_file(): shutil.copy(dir, sys.path[0])
    print(img_dir)
    pilt = PhotoImage(file=img_dir)
    a=Label(image=pilt)
    a.image = pilt
    tahvel.create_image(100, 100, image=pilt, anchor=NW)


init_GUI()
raam.mainloop()
