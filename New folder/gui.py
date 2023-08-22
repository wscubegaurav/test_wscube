from all_module import *
folder_path = ""
from make_roi import make_roi_image
def path():
    global folder_path, p
    folder_path = filedialog.askdirectory()
    f_path.config(text=str(folder_path))
    win.update()

    progressbar = ttk.Progressbar(
        win,
        orient='horizontal',
        mode='determinate',
        length=len(os.listdir(folder_path))
    )
    progressbar.place(x=570, y=190, width=400, height=60)
    progressbar.start()
    win.update()
    make_roi_image(folder_path, win,progressbar)

def on_closing():
    global folder_path
    folder_name = folder_path + "//" +"roi_img"
    folder_path = os.path.join(os.getcwd(), folder_name)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    win.destroy()
win = Tk()

width= win.winfo_screenwidth()

height= win.winfo_screenheight()

win.geometry("%dx%d" % (width, height))
win.config(bg="#c6c6c6")

Label(win,text="IMAGES CLASSIFICATION APP", font=("Calibri",32),bg="#a5a5a5").place(x=100,y =12,width=1335, height=70)

f_path = Label(win,text="",anchor="w",font=("Calibri",18),fg="black",bg="#c6c6c6",highlightthickness=1,relief="flat")

f_path.place(x=540,y =105,width=890, height=60)


b1 =Button(win,text="Choose Folder", font=("Calibri",24),bg="#a5a5a5",command =path)
b1.place(x=100,y =105,width=400, height=60)


win.protocol("WM_DELETE_WINDOW", on_closing)
win.mainloop()