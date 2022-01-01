import cv2
import time

CONFIDENCE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.1
COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

class_names = []
#with open("classes.txt", "r") as f:
with open("models/coco.names", "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]

#vc = cv2.VideoCapture('rtsp://username:password@###.###.#.##:###') # for used with IP camera through rtsp protocol
vc = cv2.VideoCapture('test.mp4')

#net = cv2.dnn.readNet("models/yolov4.weights", "models/yolov4.cfg") #for used with full sized yolov4 model (not included in models)
net = cv2.dnn.readNet("models/yolov4-tiny.weights", "models/yolov4-tiny.cfg")

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA) #must be enabled for GPU 
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
#net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16) #enable this preferable target option with enabled GPU for reduced latency at a slight cost of accuracy
#to really crank up the power, open jtop in terminal and enable jetson clocks (I have recorded 80 fps inference with it enabled)

#net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV) #must be enabled for CPU
#net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU) #must be enabled for CPU

#net.setPreferableBackend(cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE) #OpenVINO
#net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU) #must be enabled for CPU

model = cv2.dnn_DetectionModel(net)
#model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)
model.setInputParams(size=(416, 416), scale=1/float(255.0), swapRB=True) #float is important for Python version 2!!!

avg_FPS=0
count=0
total_fps=0

while cv2.waitKey(1) < 1:
    (grabbed, frame) = vc.read()
    if not grabbed:
        break
    start = time.time()
    classes, scores, boxes = model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    end = time.time()

    FPS = 1 / (end - start)
    total_fps += FPS
    count+=1
    avg_FPS = total_fps / float(count)

    start_drawing = time.time()
    for (classid, score, box) in zip(classes, scores, boxes):
        color = COLORS[int(classid) % len(COLORS)]
        label = "%s : %f" % (class_names[classid[0]], score)
        cv2.rectangle(frame, box, color, 2)
        cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    end_drawing = time.time()
    
    fps_label = "avg FPS: %.2f FPS: %.2f (excluding drawing %.2fms)" % (avg_FPS, 1 / (end - start), (end_drawing - start_drawing) * 1000)
    cv2.putText(frame, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 127), 2)
    #print(fps_label)
    cv2.imshow("detections", frame)
print(avg_FPS)
