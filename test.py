import cv2
import face_recognition
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import system

cap = cv2.VideoCapture(0)
cap.set(3, 2560)
cap.set(4, 1600)

name_image = face_recognition.load_image_file("image.jpg")
# load all images(faces)

name_encoding = face_recognition.face_encodings(name_image)[0]
# encode all faces

known_face_encodings = [
    name_encoding
]

# setup a known database of encodings

known_face_names = [
    "NAME"
]

fromEmail = 'emailid@gmail.com'
fromEmailPassword = 'Password'
toEmail = 'emailid@gmail.com'
save = open("log.txt", "a")


def say(tts):
    system(f'say {tts}')
    
    
def send_email(subj, tex):
     msgroot = MIMEMultipart('related')
     msgroot['Subject'] = f'Security Update-{subj}'
     msgroot['From'] = fromEmail
     msgroot['To'] = toEmail
     msgroot.preamble = 'problem'
     msgalternative = MIMEMultipart('alternative')
     msgroot.attach(msgalternative)
     msgtext = MIMEText(f'security cam found object{tex}')
     msgalternative.attach(msgtext)
     smtp = smtplib.SMTP('smtp.gmail.com', 587)
     smtp.starttls()
     smtp.login(fromEmail, fromEmailPassword)
     smtp.sendmail(fromEmail, toEmail, msgroot.as_string())
     smtp.quit()
     save.write('mail sent\n')
     print("Mail sent!")


def log_data(time):
    save.write('unknown at ' + time + '\n')
    print("Data logged!")


def photo():
    camera = cv2.VideoCapture(0)
    for i in range(1):
        return_value, image = camera.read()
        cv2.imwrite(str(time.asctime(time.localtime(time.time()))) + '.jpg', image)
        camera.release()
    print("picture taken")
    # save = open("log.txt", "a")
    save.write('picture taken\n')


# setup a known database of names
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    abcd = time.asctime(time.localtime(time.time()))
    rgb_small_frame = small_frame[:, :, ::-1]
    ret, frame = cap.read()
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if process_this_frame:

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            if True in matches:
                index = matches.index(True)
                name = known_face_names[index]
            face_names.append(name)
            print(name, abcd)
            if name == "Unknown":
                say("intruder alert")
                log_data(abcd)
                say("data logged")
                photo()
                say("photo taken")
                send_email(subj=abcd, tex=f'at{abcd}')
                say("mail sent")
                

    process_this_frame = not process_this_frame
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 255), 2)
        # Draw a label with a name below the face 
        cv2.rectangle(frame, (left, bottom), (right, bottom), (255, 255, 255))
        cv2.putText(frame, name, (left + 6, top - 6), cv2.FONT_HERSHEY_DUPLEX, 1.3, (2, 2, 255), 1)
        # Display the resulting image
    cv2.imshow('FACE RECOGNITION', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
