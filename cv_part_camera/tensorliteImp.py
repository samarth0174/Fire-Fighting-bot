import tflite_runtime.interpreter as tflite

import numpy as np  
import cv2
import time


def maskfun(frame):
    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    
    # lower = [0,102,149]
    # lower1 = [0,0,231]
    
    # lower = [115,0,145]
    lower = [0,102,149]
    upper = [25,255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    mask = cv2.inRange(hsv, lower, upper)
 
    output1 = cv2.bitwise_and(frame, hsv, mask=mask)
    no_red = cv2.countNonZero(mask)
    countours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(frame,countours,-1,(0,255,0),3)
    
    # cv2.imshow("frame",frame)
    cv2.imshow("output", output1)
    # cv2.imshow("mask",mask)


# loading the stored model from file
# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="converted_model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()





cap = cv2.VideoCapture(1)
#cap = cv2.VideoCapture(r'VIDEO_FILE_NAME')
time.sleep(2)

if cap.isOpened(): # try to get the first frame
    rval, frame = cap.read()
else:
    rval = False


IMG_SIZE = 64
# IMG_SIZE = 224


#for i in range(2500):
#    cap.read()



while(1):

    rval, image = cap.read()
    if rval==True:
        orig = image.copy()
        
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        IMG_SIZE = 64
        # image = cv2.imread("/content/fire.jpeg")
        input_shape = input_details[0]['shape']
        image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))  
        image = image.astype("float") / 255.0
        image = np.float32(np.array(image))
        image = np.expand_dims(image, axis=0)

        
        tic = time.time()
        
        # Test model
        interpreter.set_tensor(input_details[0]['index'], image)
        interpreter.invoke()

        output_data = interpreter.get_tensor(output_details[0]['index'])

        fire_prob = output_data[0][0] * 100
        toc = time.time()
        print("Time taken = ", toc - tic)
        print("FPS: ", 1 / np.float64(toc - tic))
        print("Fire Probability: ", fire_prob)
        print("Predictions: ", output_data)
        print(image.shape)
        
        label = "Fire Probability: " + str(fire_prob)
        cv2.putText(orig, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,0.7, (0, 255, 0), 2)
        if(fire_prob>50):
            maskfun(orig)
        cv2.imshow("Output", orig)
        
        key = cv2.waitKey(10)
        if key == 27: # exit on ESC
            break
    elif rval==False:
            break
end = time.time()

cap.release()
cv2.destroyAllWindows()