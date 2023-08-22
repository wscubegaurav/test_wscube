from all_module import *
from image_cluster import image_cluster_data

def roi_image(roi_list,win,org_image_path):
    images_folder = roi_list
    img_width, img_height = 224, 224
    batch_size = 32
    epochs = 10

    def create_cnn_model():
        model = Sequential()
        model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(img_width, img_height, 3)))
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(128, (3, 3), activation='relu'))
        model.add(MaxPooling2D((2, 2)))
        model.add(Flatten())
        model.add(Dense(512, activation='relu'))
        model.add(Dense(256, activation='relu'))
        model.add(Dense(128, activation='relu'))
        return model

    image_files = []
    for root, dirs, files in os.walk(images_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_files.append(os.path.join(root, file))

    num_images = len(image_files)

    if num_images == 0:
        pass
        return

    image_data = np.zeros((num_images, img_width, img_height, 3))

    for i, image_path in enumerate(image_files):
        img = load_img(image_path, target_size=(img_width, img_height))
        img = img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = imagenet_utils.preprocess_input(img)
        image_data[i] = img

    cnn_model = create_cnn_model()

    image_features = cnn_model.predict(image_data, batch_size=batch_size)

    # Calculate the maximum number of components based on the number of samples and features
    max_components = min(image_features.shape[0], image_features.shape[1])

    pca = PCA(n_components=max_components)  # Set n_components to the maximum possible value
    image_features_pca = pca.fit_transform(image_features.reshape(len(image_features), -1))


    image_path1 = images_folder
    image_data1 = os.listdir(image_path1)

    d1 = pd.DataFrame(image_features_pca)
    d2 = pd.DataFrame(image_data1, columns=["filename"])
    dataset = pd.concat((d1, d2), axis=1)
    er = []

    max_cluster = len(image_data1)

    for i in range(2,max_cluster+1):
        k = KMeans(n_clusters=i)
        k.fit(d1)
        er.append(k.inertia_)
    cluster = [i for i in range(2,max_cluster+1)]
    plt.figure(figsize=(10,10))
    plt.plot(cluster,er,marker="o")
    canvas = FigureCanvasTkAgg(plt.gcf(), master=win)

    canvas.get_tk_widget().place(x=700, y=310, width=735, height=450)

    noc =Label(win, text="Number of CLusters", font=("Calibri", 24), bg="#a5a5a5")
    noc.place(x=100, y=310, width=400, height=60)

    e = Entry(win, font=("Calibri", 24), bg="#c6c6c6", highlightthickness=1)
    e.place(x=545, y=310, width=110, height=60)

    b=Button(win, text="Done", font=("Calibri", 24), bg="#a5a5a5",command=lambda : cluster_make(d1,dataset))
    b.place(x=100, y=420, width=400, height=60)

    def cluster_make(d1,dataset):
        no_cluster = e.get()
        e.destroy()
        b.destroy()
        canvas.get_tk_widget().destroy()
        noc.destroy()
        k1 = KMeans(n_clusters=int(no_cluster))
        k1.fit(d1)
        pr = k1.fit_predict(d1)
        d3 = pd.DataFrame(pr, columns=["prd"])
        final_out = pd.concat((dataset["filename"],d3),axis=1)
        image_cluster_data(roi_list,final_out,win,org_image_path)
