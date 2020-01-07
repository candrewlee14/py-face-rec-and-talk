import json
import os
from slugify import slugify
import cv2
import face_recognition
import numpy as np
from numpy.core.defchararray import rsplit
from watsontalker import sayWords
from PIL import Image, ImageDraw
from speechListener import *

import yaml
#try to read the config data from config.yaml
config = []
with open("config.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

#import mxnet as mx

#read json file
#with open('data.txt') as json_file:
#   data = json.load(json_file)

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

#known_pictures_dir = os.listdir('known_pictures')
unknown_pictures_dir = os.listdir('unknown_pictures')
known_face_encodings_dir = os.listdir('known_face_encodings')

known_face_encodings = []
known_face_names = []

#remove all overlapping filenames and be left with unknown pictures to process
pictures_to_process = set(map(lambda x: x.rsplit('.', 1)[0], unknown_pictures_dir))
for knownEncodingItem in known_face_encodings:
    try:
        pictures_to_process.remove(knownEncodingItem.rsplit('.', 1)[0])
    except ValueError:
        pass  # do nothing!

#for every picture to process, recognize faces and dump encoding into json file
for picture in pictures_to_process:
    pic_image = face_recognition.load_image_file("unknown_pictures/"+picture+".jpg")
    face_encoding = face_recognition.face_encodings(pic_image)[0]
    with open('known_face_encodings/'+picture+'.json', 'w') as outfile:
        json.dump(face_encoding.tolist(), outfile)
    #move pic to known_pictures
    os.rename("unknown_pictures/"+picture+".jpg", "known_pictures/"+picture+".jpg")


#load every json encoding file into known_face_encodings
for dirItem in known_face_encodings_dir:
    with open('known_face_encodings/' + dirItem) as json_file:
        known_face_encodings.append(np.array(json.load(json_file)))
    #add to known_face_names
    known_face_names.append(dirItem.rsplit('.', 1)[0])


# Load a sample picture and learn how to recognize it.
# obama_image = face_recognition.load_image_file("known_pictures/obama.jpg")
#obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

#dump image encoding to json file
#with open('known_face_encodings/obama.json', 'w') as outfile:
#   json.dump(obama_face_encoding.tolist(), outfile)

#read face encoding from json file

#with open('known_face_encodings/obama.json') as json_file:
#  obama_face_encoding = np.array(json.load(json_file))



# Initialize some variables
def lookForFace():
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    foundFace = False

    while not foundFace:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_landmarks_list = face_recognition.face_landmarks(frame)

            if len(face_locations) > 0:
                foundFace = True
        process_this_frame = not process_this_frame

            
    # Release handle to the webcam
    video_capture.release()
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index].replace('_', ' ').replace('-',' ')

        face_names.append(name)

        #write image to file, and write Andrew encoding to dump
    if "Unknown" in face_names:
        face_names.remove("Unknown")
        if "Unknown" not in face_names:
            name = askName(True)
            print(name)
            name = slugify(name)
            #
            #This is where we are going to ask for their name, and set the filename to be their name
            #
            #
            #cv2.imwrite('unknown_pictures/Image.jpg', frame)
            with open('known_face_encodings/'+ name+ '.json', 'w') as outfile:
                json.dump(face_encoding.tolist(), outfile)
    else:
        if len(face_names) == 1:
            sayWords("Good to see you",config, True)
            sayWords(face_names[0].rsplit(' ', 1)[0], config, True)

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        #face_image = frame[top:bottom, left:right]
        face_image = frame
        pil_image = Image.fromarray(face_image)
        #
        d = ImageDraw.Draw(pil_image)


        for face_landmarks in face_landmarks_list:

            # Let's trace out each facial feature in the image with a line!
            for facial_feature in face_landmarks.keys():
                d.line(face_landmarks[facial_feature], width=5)

        pil_image.show()

    # Display the resulting image
    #while True:
    #    cv2.imshow('image', face_image)

    # Hit 'q' on the keyboard to quit!
    #   if cv2.waitKey(1) & 0xFF == ord('q'):
    #       break
        
    cv2.destroyAllWindows()

lookForFace()
