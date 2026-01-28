import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from ultralytics import YOLO

#load model
model = YOLO("first_model.pt")

# export model 

#model.export(format="ncnn")

#model.export(format="mnn",imgsz=640,int8=True)

#model.export(format="openvino" ,int8=True ,fraction = 1, data ="IA_dataSet/data.yaml");

