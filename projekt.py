from tkinter import *
from tkinter import ttk
from tkinter import filedialog, colorchooser, messagebox
from pathlib import Path
import time, os, sys, shutil
from PIL import Image, ImageTk, ImageGrab, ImageDraw
#from Image import ImageTk

raam=Tk()
raam.title("Projekt")
tahvli_aken = Toplevel()
tahvli_aken.title("Pilt")
tahvel = Canvas(tahvli_aken, width=500, height=500, background="white")

#Joone omadused
paksus=IntVar()
paksus.set(2)
värv=StringVar()
värv.set("#000000")
kujundi_piir=StringVar()

#Faili tee
faili_info = StringVar()
faili_info.set("")

#PIL image ja sellele joonistamine
pilt=Image.new("P", (500,500), color=255)
joonista = ImageDraw.Draw(pilt)

#Teksti omadused
sisendtekst=StringVar()

#Hiire positsioon
#ehiir on eelmine hiire positsioon
hiir_x=0
hiir_y=0
ehiir_x=0
ehiir_y=0
hiire_info=StringVar()
hiire_info.set("")

#Kujundite joonistamiseks
algus_x=-1
algus_y=-1

def init_GUI():
    #_b- button,  _d- dropdown, _c- checkbox, _e entry, _l- label
    
    #Joonistamis ala ja algne hiire kontroll
    tahvel.grid(column=0, row=1, padx=5, pady=5, sticky=(E,N,S,W))
    tahvel.bind("<B1-Motion>", pliiats)
    tahvel.bind("<Motion>", hiire_positsioon)
    tahvli_aken.resizable(0,0)
    #tahvel.bind_all("<MouseWheel>", zoom_window)
    
    #Kõikide nuppude raam
    toolbar = ttk.Frame(height=2,relief=SUNKEN)
    toolbar.grid(column=0, row=0, padx=5, pady=5, sticky=(E,N,S,W))
    
    #Pliiatsi valimise nupp
    def pliiatsi_kasutus():
        tahvel.bind("<B1-Motion>", pliiats)
        tahvel.bind("<Button-1>", ignore)
        tahvel.bind("<ButtonRelease-1>", ignore)
    pliiats_b = ttk.Button(toolbar, text="Pliiats", command=pliiatsi_kasutus)
    pliiats_b.grid(column=0, row=0, padx=5, pady=5, sticky=(E,N,S,W))
    
    #Paksuse valik
    global paksus
    paksus_l = ttk.Label(toolbar, text="Paksus:")
    paksus_l.grid(column=1, row=0, padx=5, pady=5, sticky=(N,S,W))
    paksus_e = ttk.Entry(toolbar, textvariable=paksus)
    paksus_e.grid(column=2, row=0, padx=5, pady=5, sticky=(N,S,W))
    
    #Kujundi valimine
    def kujundi_kasutus():
        tahvel.bind("<B1-Motion>", kujund)
        tahvel.bind("<Button-1>", ignore)
        tahvel.bind("<ButtonRelease-1>", kujund_reset)
    piirid = ["Piirjoon", "Kuju", "Piiriga kuju"]
    kujund_b = ttk.Button(toolbar, text="Kujund", command=kujundi_kasutus)
    kujund_b.grid(column=3, row=0, padx=5, pady=5, sticky=(E,N,S,W))
    kujundi_piir_d = ttk.OptionMenu(toolbar, kujundi_piir , piirid, *piirid)
    kujundi_piir_d.grid(column=4, row=0, padx=5, pady=5, sticky=(E,N,S,W))
    kujundi_piir.set("Kuju")
    
    #Teksti valimise nupp
    def teksti_kasutus():
        tahvel.bind("<B1-Motion>", ignore)
        tahvel.bind("<Button-1>", tekst)
        tahvel.bind("<ButtonRelease-1>", ignore)
    tekst_b = ttk.Button(toolbar, text="Kuva see tekst:", command=teksti_kasutus)
    tekst_b.grid(column=5, row=0, padx=5, pady=5, sticky=(E,N,S,W))
    
    #Värvi valik
    värv.set("#000000")
    uus_värv_b = ttk.Button(toolbar, text="Uus värv", command=uus_värv)
    uus_värv_b.grid(column=7, row=0, padx=5, pady=5, sticky=(E,N,S,W))
    
    #Tekst mida saab kuvada
    tekst_e = ttk.Entry(toolbar, textvariable=sisendtekst)
    tekst_e.grid(column=6, row=0, padx=5, pady=5, sticky=(E,N,S,W))
    
    #Vali pilt mida kuvada
    ava_pilt_b = ttk.Button(toolbar, text="Ava pilt", command=ava_pilt)
    ava_pilt_b.grid(column=8, row=0, padx=5, pady=5, sticky=(E,N,S,W))
    
    #Pildi salvestamine
    salvesta_pilt_b = ttk.Button(toolbar, text="Salvesta pilt", command=salvesta_pilt)
    salvesta_pilt_b.grid(column=9, row=0, padx=5, pady=5, sticky=(E,N,S,W))
    
    #Pildi lõikamine
    def pildi_lõikamise_kasutus():
        tahvel.bind("<B1-Motion>", lõika_pilt)
        tahvel.bind("<Button-1>", ignore)
        tahvel.bind("<ButtonRelease-1>", lõika_pilt_reset)
    lõika_pilt_b = ttk.Button(toolbar, text="Lõika", command=pildi_lõikamise_kasutus)
    lõika_pilt_b.grid(column=10, row=0, padx=5, pady=5, sticky=(E,N,S,W))
    
    #Pildi pööramine
    pööra_pilt_b = ttk.Button(toolbar, text="Pööra", command=pildi_pööramine)
    pööra_pilt_b.grid(column=11, row=0, padx=5, pady=5, sticky=(E,N,S,W))


    #Alumine inforiba
    infobar = ttk.Frame(height=2,relief=SUNKEN)
    infobar.grid(column=0, row=2, padx=5, pady=5, sticky=(E,N,S,W))

    #Hiire positsioon
    hiire_info_l = ttk.Label(infobar, textvariable=hiire_info)
    hiire_info_l.grid(column=0, row=0, padx=5, pady=5, sticky=(N,S,W,E))

    #Värv
    global värvi_info
    värvi_info = Canvas(infobar, width=100, height=infobar.winfo_height(), background=värv.get())
    värvi_info.grid(column=1, row=0, padx=5, pady=5, sticky=(N,S))
    värvi_indikaator = värvi_info.create_rectangle(0,0,värvi_info.winfo_width(),värvi_info.winfo_height(), fill=värv.get())

    #Fail
    faili_info_l = ttk.Label(infobar, textvariable=faili_info)
    faili_info_l.grid(column=2, row=0, padx=5, pady=5, sticky=(N,S))
    
#Kui on vaja et klahv nupp midagi ei teeks
def ignore(event):
    return 0
#Paletilt uue värvi valimine
def uus_värv():
    uus_värv=str(colorchooser.askcolor(initialcolor='#ff0000'))
    uus_värv=uus_värv[uus_värv.find("#"):len(uus_värv)-2]
    värv.set(uus_värv)
    global värvi_info
    värvi_info.delete("all")
    värvi_info.create_rectangle(0,0,värvi_info.winfo_width(),värvi_info.winfo_height(), fill=värv.get())
    kuva_pilt(pilt)
#Hiire koordinaatide registreerimine
def hiire_positsioon(event):
    global hiir_x, hiir_y, ehiir_x, ehiir_y, hiire_info
    ehiir_x=hiir_x
    ehiir_y=hiir_y
    hiir_x=event.x
    hiir_y=event.y
    hiire_info.set("Hiir: " + str(hiir_x) + "x" + str(hiir_y))
#Rullikuga zoom
def zoom_window(event):
    if event.delta < 0: faktor=-0.01
    else:   faktor=0.01
    tahvel.config(width=tahvel.winfo_width()+tahvel.winfo_width()*faktor, height=tahvel.winfo_height()+tahvel.winfo_height()*faktor)
#Lõikamine
def lõika_pilt(event):
    global hiir_x, hiir_y, ehiir_x, ehiir_y, algus_x, algus_y
    hiire_positsioon(event)
    if algus_x < 0 and algus_y < 0:
        algus_x=hiir_x
        algus_y=hiir_y
    if hiir_x!=ehiir_x or hiir_y!=ehiir_y:
        tahvel.delete("ajutine")
    tahvel.create_rectangle(algus_x,algus_y,hiir_x,hiir_y,fill="",outline="gray",tag="ajutine")
def lõika_pilt_reset(event):
    global algus_x, algus_y, hiir_x, hiir_y
    if algus_x>hiir_x and algus_y>hiir_y:
        joonista.rectangle([(hiir_x,hiir_y),(algus_x,algus_y)],"#FFFFFF")
    elif algus_x>hiir_x and algus_y<hiir_y:
        joonista.rectangle([(hiir_x,algus_y),(algus_x,hiir_y)],"#FFFFFF")
    elif algus_x<hiir_x and algus_y>hiir_y:
        joonista.rectangle([(algus_x,hiir_y),(hiir_x,algus_y)],"#FFFFFF")
    else:
        joonista.rectangle([(algus_x,algus_y),(hiir_x,hiir_y)],"#FFFFFF")
    algus_x=-1
    algus_y=-1
    kuva_pilt(pilt)
#Pööramine
def pildi_pööramine():
    global pilt
    pilt=pilt.rotate(90, expand=1)
    tahvel.delete("all")
    tahvel.config(width=tahvel.winfo_x()+pilt.size[0], height=tahvel.winfo_y()+pilt.size[1])
    tahvel.update()
    kuva_pilt(pilt)
#Pliiatsiga joonistamine
def pliiats(event):
    global paksus, värv, hiir_x, hiir_y, ehiir_x, ehiir_y
    hiire_positsioon(event)
    joonista.line([ehiir_x, ehiir_y, hiir_x, hiir_y], värv.get(), paksus.get())
    kuva_pilt(pilt)
#Pintsliga joonistamine
def kujund(event):
    global paksus, värv, hiir_x, hiir_y, ehiir_x, ehiir_y, algus_x, algus_y
    hiire_positsioon(event)
    if algus_x < 0 and algus_y < 0:
        algus_x=hiir_x
        algus_y=hiir_y
    if hiir_x!=ehiir_x or hiir_y!=ehiir_y:
        tahvel.delete("ajutine")
    if kujundi_piir.get() == "Piirjoon":    tahvel.create_rectangle(algus_x,algus_y,hiir_x,hiir_y,fill="",outline=värv.get(),tag="ajutine")
    if kujundi_piir.get() == "Kuju":    tahvel.create_rectangle(algus_x,algus_y,hiir_x,hiir_y,fill=värv.get(),tag="ajutine")
def kujund_reset(event):
    global algus_x, algus_y, hiir_x, hiir_y
    if algus_x>hiir_x and algus_y>hiir_y:
        if kujundi_piir.get() == "Piirjoon":    joonista.rectangle([(hiir_x,hiir_y),(algus_x,algus_y)],None,värv.get())
        if kujundi_piir.get() == "Kuju":    joonista.rectangle([(hiir_x,hiir_y),(algus_x,algus_y)],värv.get())
        if kujundi_piir.get() == "Piiriga kuju":    joonista.rectangle([(hiir_x,hiir_y),(algus_x,algus_y)],värv.get(),värv.get())
    elif algus_x>hiir_x and algus_y<hiir_y:
        if kujundi_piir.get() == "Piirjoon":    joonista.rectangle([(hiir_x,algus_y),(algus_x,hiir_y)],None,värv.get())
        if kujundi_piir.get() == "Kuju":    joonista.rectangle([(hiir_x,hiir_y),(algus_x,algus_y)],värv.get())
        if kujundi_piir.get() == "Piirjoon":    joonista.rectangle([(hiir_x,hiir_y),(algus_x,algus_y)],None,värv.get())
    elif algus_x<hiir_x and algus_y>hiir_y:
        if kujundi_piir.get() == "Piirjoon":    joonista.rectangle([(algus_x,hiir_y),(hiir_x,algus_y)],None,värv.get())
        if kujundi_piir.get() == "Kuju":    joonista.rectangle([(hiir_x,hiir_y),(algus_x,algus_y)],värv.get())
        if kujundi_piir.get() == "Piirjoon":    joonista.rectangle([(hiir_x,hiir_y),(algus_x,algus_y)],None,värv.get())
    else:
        if kujundi_piir.get() == "Piirjoon":    joonista.rectangle([(algus_x,algus_y),(hiir_x,hiir_y)],None,värv.get())
        if kujundi_piir.get() == "Kuju":    joonista.rectangle([(hiir_x,hiir_y),(algus_x,algus_y)],värv.get())
        if kujundi_piir.get() == "Piirjoon":    joonista.rectangle([(hiir_x,hiir_y),(algus_x,algus_y)],None,värv.get())
    algus_x=-1
    algus_y=-1
    kuva_pilt(pilt)
#Kirjutamine
def tekst(event):
    global paksus, värv, hiir_x, hiir_y, sisend
    joonista.text((hiir_x,hiir_y), sisendtekst.get(), värv.get(), font=None, anchor=None)
    kuva_pilt(pilt)
#Pildi avamine
def ava_pilt():
    global pilt, joonista, faili_info
    dir=filedialog.askopenfilenames(filetypes=[("Image files", "*.gif;*.pgm;*.ppm;*.PNG;*.jpg"),("All files", "*.*")])
    if dir is None: return
    dir=str(dir)[2:len(str(dir))-3]
    img_dir=dir
    faili_info.set(img_dir)
    while img_dir.find("/")!=-1:
        img_dir=img_dir[img_dir.find("/")+1:len(img_dir)]
    if not Path(img_dir).is_file(): shutil.copy(dir, sys.path[0])
    pilt = Image.open(img_dir)
    tahvel.config(width=tahvel.winfo_x()+pilt.size[0], height=tahvel.winfo_y()+pilt.size[1])
    joonista = ImageDraw.Draw(pilt)
    tahvel.delete("all")
    tahvel.update()
    kuva_pilt(pilt)
#Teeb PIL image TK photoimage-ks ja kuvab selle tahvlile
def kuva_pilt(p):
    img = ImageTk.PhotoImage(p, p.size)
    a=Label(image=img)
    a.image = img
    tahvel.create_image(tahvel.winfo_width()/2-img.width()/2, tahvel.winfo_height()/2-img.height()/2, image=img, anchor=NW)
#Pildi salvestamine
def salvesta_pilt():
    dir=filedialog.asksaveasfile(defaultextension=".gif", filetypes=[("GIF image", "*.gif"), ("PNG image","*.png")])
    dir=dir.name
    print(dir)
    if dir is None: return
    pilt.save(dir)
    
init_GUI()
raam.mainloop()
