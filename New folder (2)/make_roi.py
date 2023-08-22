from all_module import *
from image_array import roi_image
def make_roi_image(path,win,progressbar):
    org_image_path = path
    image_data = os.listdir(org_image_path)
    if not os.path.exists(org_image_path+"//"+"roi_img"):
        os.makedirs(org_image_path+"//"+"roi_img")

    n= len(os.listdir(path))
    step = 100 / n
    count = 0
    for i in image_data:
        img = cv2.imread(org_image_path+"//"+i)
        detector = MTCNN()
        faces = detector.detect_faces(img)
        c = 0
        for face in faces:
            x, y, w, h = face['box']
            roi_color = img[y:y+h, x:x+w]
            roi_color = cv2.resize(roi_color,(224, 224))
            filename = org_image_path+"//"+"roi_img" + "//" + i[:-4] + "_" + str(c) + ".jpg"
            cv2.imwrite(filename, roi_color)
            c = c+1
            win.update()
        count += step
        progressbar['value'] = count

    progressbar.stop()
    showinfo( title='Information', message='All File are Load')
    progressbar.destroy()
    roi_image(org_image_path+"//"+"roi_img",win,org_image_path)