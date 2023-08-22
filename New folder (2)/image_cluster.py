from all_module import *

def image_cluster_data(path,dataset,win,org_image_path):
    list_img = []
    for i in dataset["prd"].unique():
        name = dataset[dataset["prd"] == i]["filename"]
        list_img.append(name.iloc[0])

    folder_path = ""
    def save_path():
        global folder_path
        folder_path = filedialog.askdirectory()
        f_path2.config(text=str(folder_path))
        win.update()

    def update_button_text(index):
        global  folder_path
        current_image = list_img[index]
        if not os.path.exists(folder_path + "/" + str(index)):
            os.makedirs(folder_path + "/" + str(index))
        name1 = dataset[dataset["filename"] == current_image]["prd"]
        name2 = dataset[dataset["prd"] == name1.iloc[0]]["filename"]
        org_image_list = os.listdir(org_image_path)
        for i in name2 :
            source_folder = org_image_path
            destination_folder = folder_path + "/" + str(index)
            filtered_items = list(filter(lambda li: li.startswith(i[:-6]), org_image_list))
            source_path = os.path.join(source_folder, filtered_items[0])
            destination_path = os.path.join(destination_folder, filtered_items[0])
            shutil.copy(source_path, destination_path)

        for i in name2:
            filename = org_image_path + "/" + i[:-6] + ".JPG"
            img = cv2.imread(filename)
            img = cv2.resize(img, (600, 500))

            cv2.imshow("demo", img)
            cv2.waitKey(0)
        cv2.destroyAllWindows()

    save_adr= Button(win, text="Destination Folder", font=("Calibri", 24 ), bg="#a5a5a5", command=save_path)
    save_adr.place(x=100, y=200, width=400, height=60)

    f_path2 = Label(win, text="", anchor="w", font=("Calibri", 18), fg="black", bg="#c6c6c6", highlightthickness=1,
                   relief="flat")
    f_path2.place(x=540, y=200, width=890, height=60)

    frame_x = 100
    frame_y = 350
    frame_width = 1335
    frame_height = 420
    button_width, button_height = 100, 100
    # Calculate the number of buttons per row
    buttons_per_row = frame_width // (button_width + 20)

    x_offset, y_offset = frame_x, frame_y
    for i, image_file in enumerate(list_img):
        img = Image.open(path + "//" + list_img[i])
        img = img.resize((button_width, button_height))

        photo = ImageTk.PhotoImage(img)

        button = Button(win, image=photo, command=lambda index=i: update_button_text(index))
        button.image = photo
        button.place(x=x_offset, y=y_offset)

        x_offset += button_width + 20
        if (i + 1) % buttons_per_row == 0:
            x_offset = frame_x
            y_offset += button_height + 20

