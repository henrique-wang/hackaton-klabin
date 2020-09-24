import cv2
import os

def newUser(id):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    user_dir = os.path.join(BASE_DIR, 'users.csv')
    print(user_dir)

    with open(user_dir,'r+') as f:
        DataList=f.readlines()
        idList=[]
        for line in DataList:
            entry=line.split(',')
            idList.append(entry[0])
        if id not in idList:
            print("\n [INFO] Creating a new User ...")
            username=input('\n enter username and press <return> ==>  ')
            f.writelines(f'\n{id},{username},0,0')

def TakePicture():

    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video width
    cam.set(4, 480)  # set video height
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    cascade_dir = os.path.join(BASE_DIR,'cascades/haarcascade_frontalface_default.xml')
    print(cascade_dir)
    face_detector = cv2.CascadeClassifier(cascade_dir)

    # For each person, enter one numeric face id
    face_id = input('\n enter user id and press <return> ==>  ')
    newUser(face_id)
    print("\n [INFO] Initializing face capture. Look the camera and wait ...")
    # Initialize individual sampling face count
    count = 0

    # Let's create a directory to store the pictures if the ID does not exists
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    dirName = str(face_id)
    NEW_DIR = os.path.join(BASE_DIR, 'dataset', dirName)
    if not os.path.exists(NEW_DIR):
        print("Cretaing new directory")
        os.mkdir(NEW_DIR)

    # Let's take pictures to store on the directory
    while True:
        ret, img = cam.read()
        print(count)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
            count += 1
            # Save the captured image into the datasets folder
            save_path = os.path.join(BASE_DIR, ("dataset/" + str(face_id) +
                                                "/" + "User." + str(face_id) + '.' +
                                                str(count) + ".jpg"))
            newPath = save_path.replace(os.sep, '/')
            print(newPath)
            cv2.imwrite(newPath, gray[y:y + h, x:x + w])
            cv2.imshow('image', img)
        k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break
        elif count >= 30:  # Take 30 face sample and stop video
            break

    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
    return (NEW_DIR)

