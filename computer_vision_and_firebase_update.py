import cv2
import dlib

from os.path import join

from jinja2 import ModuleLoader


def load_model(model_path, caffemodel, prototxt):
    caffemodel_path = join(model_path, caffemodel)
    prototxt_path = join(model_path, prototxt)
    model = cv2.dnn.readNet(prototxt_path, caffemodel_path)

    return model


def predict(model, img, height, width):
    face_blob = cv2.dnn.blobFromImage(
        img, 1.0, (height, width), (0.485, 0.456, 0.406))
    model.setInput(face_blob)
    predictions = model.forward()
    class_num = predictions[0].argmax()
    confidence = predictions[0][class_num]

    return class_num, confidence


detector = dlib.get_frontal_face_detector()

font, fontScale, fontColor, lineType = cv2.FONT_HERSHEY_SIMPLEX, 1, (
    0, 255, 0), 2

input_height = 224
input_width = 224

# load gender model
gender_model_path = 'models/gender'
gender_caffemodel = 'gender.caffemodel'
gender_prototxt = 'gender.prototxt'
gender_model = load_model(
    gender_model_path, gender_caffemodel, gender_prototxt)

# gender_model.set_mode_gpu()
# load age model
age_model_path = 'models/age'
age_caffemodel = 'dex_chalearn_iccv2015.caffemodel'
age_prototxt = 'age.prototxt'
age_model = load_model(age_model_path, age_caffemodel, age_prototxt)


cap = cv2.VideoCapture(-1)
x = 0

totalGender = 0
totalMen = 0
totalWomen = 0
total_age=0

mold=0
madult=0
myoung=0
mkid=0

fold=0
fadult=0
fyoung=0
fkid=0






while cap.isOpened():

    try:
        _, frame_bgr = cap.read()
       # frame_bgr=cv2.resize(frame_bgr,(224,224))
        x = x+1
        # frame_bgr=cv2.imread("4.jpg")
        # if x > 5:
        #     x = 0
        #     continue

        
        if frame_bgr is not None:
            
            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            faces = detector(frame_rgb, 1)
            print('u')
            print(len(faces))
            print('u')
            if len(faces) > 0:
                for d in faces:
                    
                    left = int(0.6 * d.left())     # + 40% margin
                    top = int(0.6 * d.top())       # + 40% margin
                    right = int(1.4 * d.right())   # + 40% margin
                    bottom = int(1.4 * d.bottom())  # + 40% margin
                    face_segm = frame_rgb[top:bottom, left:right]
                    gender, gender_confidence = predict(
                        gender_model, face_segm, input_height, input_width)
                    
                    age, age_confidence = predict(
                        age_model, face_segm, input_height, input_width)

                    


                    
                    # gender = 'man' if gender == 1 else 'woman'
                    if gender == 1:
                        totalMen = totalMen+gender_confidence
                        gender = 'men'
                        fontColor = (0, 0, 255)
                        if 0<= age <=15:
                            mkid=mkid+age_confidence
                            total_age=total_age+age_confidence
                        if 16<= age <=30:
                            myoung=myoung+age_confidence
                            total_age=total_age+age_confidence
                        if 31<= age <=60:
                            madult=madult+age_confidence
                            total_age=total_age+age_confidence
                        if 61<= age <=100:
                            mold=mold+age_confidence
                            total_age=total_age+age_confidence
                        
                    else:
                        totalWomen = totalWomen+gender_confidence
                        gender = 'women'
                        fontColor = (0, 255, 0)
                        if 0<= age <=15:
                            fkid=fkid+age_confidence
                            total_age=total_age+age_confidence
                        if 16<= age <=30:
                            fyoung=fyoung+age_confidence
                            total_age=total_age+age_confidence
                        if 31<= age <=60:
                            fadult=fadult+age_confidence
                            total_age=total_age+age_confidence
                        if 61<= age <=100:
                            fold=fold+age_confidence
                            total_age=total_age+age_confidence



                    totalGender = totalMen+totalWomen

                    xc = 0
                    if gender_confidence * 100 < 88:
                        # gender='!!!'
                        xc = xc+155
                        fontColor = (xc, 0, 0)
                    if age_confidence * 100 < 10:
                        # age='!!!'
                        xc = xc+100
                        fontColor = (xc, 0, 0)
                    if age<40:
                        age=age-3
                    else:
                        age+=6
                    text = '{}  age {} ({:.2f}%)'.format(
                        gender, age, age_confidence*100)
                    cv2.putText(frame_bgr, text, (d.left(), d.top() - 20),
                                font, fontScale, fontColor, lineType)
                    cv2.rectangle(frame_bgr, (d.left(), d.top()),
                                  (d.right(), d.bottom()), fontColor, 2)
            
        
        if(totalGender):
            print("Men per = ", 100*totalMen/totalGender,
                  "%   Women per = ", 100*totalWomen/totalGender, "%")
            myoung_per=myoung*100/total_age
            fyoung_per=fyoung*100/total_age

            madult_per=madult*100/total_age
            fadult_per=fadult*100/total_age

            mkid_per=mkid*100/total_age
            fkid_per=fkid*100/total_age

            mold_per=mold*100/total_age
            fold_per=fold*100/total_age

            percentage={

                "myoung":myoung_per,
                "fyoung":fyoung_per,
                "madult":madult_per,
                "fadult":fadult_per,
                "mkid":mkid_per,
                "fkid":fkid_per,
                "mold":mold_per,
                "fold":fold_per

            }
        import json

        with open("jdid.json", "w") as jsonFile:
            json.dump(percentage, jsonFile)

        
        cv2.imshow('frame', frame_bgr)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except:
        print('Got a bad image, skipping the frame')

cap.release()
cv2.destroyAllWindows()
