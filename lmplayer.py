from tkinter import *
from tkinter import filedialog
from traceback import *
from win32com.client import Dispatch
import time,eyed3,threading

#Open file dialog and file selection
def openMusic(index = [1]):
  global total,name
  name = []
  musicfilenames = filedialog.askopenfilenames(title = "Music Player",filetypes =[("MP3 file","*.mp3"),("WMA file","*.wma"),("WAV file","*.wav")])
  if musicfilenames:
    for i in range(len(musicfilenames)):
      media = wmp.newMedia(musicfilenames[i])
      wmp.currentPlaylist.appendItem(media)

      print(musicfilenames[i])
      #读取mp3
      coco = eyed3.load(musicfilenames[i])
      total = int(coco.info.time_secs)
      minute = int(coco.info.time_secs)//60
      sec = int(coco.info.time_secs)%60
      length = int(coco.info.time_secs)

      name = musicfilenames[i].split("/")

      i =index[-1]
      list_name.insert(END,str(i)+"."+name[-1])
      list_name.insert(END," "*6)
      if sec >=10:
        list_name.insert(END,"0%d:%d" %(minute,sec)+ "\n")
      else:
        list_name.insert(END,"0%s:0%d" %(minute,sec)+ "\n")
      i = i +1
      index.append(i)

def playMusic(event = None):
  per_thread = threading.Thread(target = per)
  per_thread.daemnon = True
  wmp.controls.play()
  per_thread.start()


def per():
  global total
  while wmp.playState !=1:
    progress_scal.set(int(wmp.controls.currentPosition))
    progress_scal.config(label = wmp.controls.currentPositionString)
    progress_scal.config(to = total,tickinterval = 50)
    time.sleep(1)
    root.title("%s" % wmp.currentMedia.name)

def stop():
  wmp.controls.stop()

def pause(event = None):
  wmp.controls.pause()

def uselist():
    pass

def fullscr():
    pass

def exitit():
  root.destroy()

def Previous_it():
  wmp.controls.previous()

def Next_it():
  wmp.controls.next()

def Volume_ctr(none):
  wmp.settings.Volume = vio_scale.get()

def Volume_add(i=[0]):
  wmp.settings.Volume =wmp.settings.Volume+5
  i.append(wmp.settings.Volume)
  vio_scale.set(wmp.settings.Volume)

def Volume_minus(i=[0]):
  wmp.settings.Volume = wmp.settings.Volume -5
  i.append(wmp.settings.Volume)
  vio_scale.set(wmp.settings.Volume)

def Scale_ctr(none):
  wmp.controls.currentPosition = var_scale.get()
  print(wmp.currentMedia.duration)

def Clear_list():
  wmp.currentPlaylist.clear()
  list_name.delete(1.0,END)
  name = []
  index = []

def List_random():
  wmp.settings.setMode("shuffle",True)
  playMusic()

def List_loop():
  wmp.settings.setMode("loop",True)
  playMusic()

#tkinter object
root =Tk()
root.title('Music Player')
wmp = Dispatch("WMPlayer.OCX")


#set canvas
canvas = Canvas(root,width =210,height = 150,bg = "white")
img = PhotoImage(file = 'music.gif')
canvas.create_image((80,50),image = img)
canvas.place(x=0,y=0)
canvas.coords(img,100,50)
canvas.grid(row =0,column = 0,sticky = "nw",rowspan =2)

#Mouse bind and operation
progress_lab = LabelFrame(root,text = "Play Progress")
progress_lab.grid(row =2,column =0,sticky = "we",rowspan = 2)
var_scale = DoubleVar()
progress_scal = Scale(progress_lab,orient = HORIZONTAL,showvalue = 0,length =180,variable = var_scale)
progress_scal.bind("<Button-1>",pause)
progress_scal.bind("")
progress_scal.bind("<ButtonRelease-1>",playMusic)
progress_scal.grid(row =3,column =0)

#Play mode
#Music selection
modee_lab = LabelFrame(root,text = "Play Mode")
modee_lab.grid(row =4,column =0,rowspan =2,sticky = "ws")
var_mode = IntVar()
randomradio = Radiobutton(modee_lab,variable = var_mode,value = 1,text ="Random",command =List_random )
randomradio.grid(row =4,column =2)
inturnradio = Radiobutton(modee_lab,variable = var_mode,value =2,text= "Inorder",command = playMusic)
inturnradio.grid(row=4,column =3)
alloop = Radiobutton(modee_lab,variable = var_mode,value =2,text = "All Loop",command = List_loop)
alloop.grid(row =5,column = 2)
sinloop = Radiobutton(modee_lab,variable = var_mode,value =3,text = "Single Loop")
sinloop.grid(row =5,column =3)
previous_play = Button(modee_lab,text = "Prev<<",command = Previous_it)
previous_play.grid(row =6,column =2,rowspan =2,pady =10)
next_play = Button(modee_lab,text = "Next>>",command = Next_it)
next_play.grid(row =6,column =3,rowspan =2,pady =10)

#Volume control
var_volume = IntVar()
vioce_lab = LabelFrame(root,text = "Volume Control")
vioce_lab.grid(row =8,column =0,sticky = "wes")
vio_scale = Scale(vioce_lab,orient = HORIZONTAL,length =170,variable = var_volume,command =Volume_ctr)
vio_scale.set(60)
vio_scale.grid(row =8,column =0)
vio_plus = Button(vioce_lab,width =8,text = "Add++",command =Volume_add)
vio_plus.grid(row =9,column =0,sticky = "w")
vio_minus = Button(vioce_lab,width =8,text ="Sub--",command = Volume_minus)
vio_minus.grid(row =9,column =0,sticky ="e")

#Play control
ctr_lab = LabelFrame(root,text = "Play Control",height =130)
ctr_lab.grid(row =0,column =1,rowspan =12,sticky = "ns")
btn_open = Button(ctr_lab,text ="Open...",width =10,command = openMusic)
btn_open.grid(row=0,column =1)
btn_play = Button(ctr_lab,text ="Play",width =10,command = playMusic)
btn_play.grid(row =1,column =1,pady =5)
btn_stop = Button(ctr_lab,text ="Stop",width =10,command = stop)
btn_stop.grid(row =2,column =1,pady =5)
btn_pause = Button(ctr_lab,text ="Pause",width =10,command = pause)
btn_pause.grid(row =3,column =1,pady =5)

#Playlist
#List related dealing
btn_playlist = Button(ctr_lab,text ="New List",width =10,command = uselist)
btn_playlist.grid(row =4,column =1,pady =5)
listimport = Button(ctr_lab,width =10,text = "Import List")
listimport.grid(row =6,column =1,sticky ="nw",pady =5)
listexport = Button(ctr_lab,width =10,text = "Export List")
listexport.grid(row =7,column =1,sticky = "nw",pady =5)
listdel_all = Button(ctr_lab,width =10,text = "Clear List",command = Clear_list)
listdel_all.grid(row =8,column =1,sticky ="nw",pady =5)
listdel_sel= Button(ctr_lab,width =10,text = "Del Music")
listdel_sel.grid(row =12,column =1,sticky = "nw",pady =5)
savelist_btn = Button(ctr_lab,text = "Save as List")
savelist_btn.grid(row=9,column =1)
min_btn = Button(ctr_lab,text = "Minimize",command = root.iconify)
min_btn.grid(row =13,column =1,pady=5)

time_text= Text(root,width =30,height =3,foreground ="green")
time_text.grid(row =10,column =0,sticky = "nw",pady =5)

list_name = Text(root,height =18,width =50)
list_name.grid(row =0,column =2,sticky = "n",rowspan =6)

#Main event loop
root.mainloop()
