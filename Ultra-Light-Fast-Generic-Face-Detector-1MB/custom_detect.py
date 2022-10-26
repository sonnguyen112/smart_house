import imp
import os
import sys

import cv2

import time;

from vision.ssd.config.fd_config import define_img_size
def detect(net_type = "RFB", input_size = 640, threshold = 0.6, candidate_size = 1500, img_path = "", test_device = "cpu"):
    start_time = time.perf_counter()
    define_img_size(input_size)
    from vision.ssd.mb_tiny_fd import create_mb_tiny_fd, create_mb_tiny_fd_predictor
    from vision.ssd.mb_tiny_RFB_fd import create_Mb_Tiny_RFB_fd, create_Mb_Tiny_RFB_fd_predictor

    result_path = "./detect_imgs_results"
    label_path = "./models/voc-model-labels.txt"
    test_device = test_device

    class_names = [name.strip() for name in open(label_path).readlines()]

    if net_type == 'slim':
        model_path = "models/pretrained/version-slim-320.pth"
        # model_path = "models/pretrained/version-slim-640.pth"
        net = create_mb_tiny_fd(len(class_names), is_test=True, device=test_device)
        predictor = create_mb_tiny_fd_predictor(net, candidate_size=candidate_size, device=test_device)
    elif net_type == 'RFB':
        model_path = "models/pretrained/version-RFB-320.pth"
        # model_path = "models/pretrained/version-RFB-640.pth"
        net = create_Mb_Tiny_RFB_fd(len(class_names), is_test=True, device=test_device)
        predictor = create_Mb_Tiny_RFB_fd_predictor(net, candidate_size=candidate_size, device=test_device)
    else:
        print("The net type is wrong!")
        sys.exit(1)
    net.load(model_path)

    sum = 0
    orig_image = cv2.imread(img_path)
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
    boxes, labels, probs = predictor.predict(image, candidate_size / 2, threshold)
    end_time = time.perf_counter()
    print(end_time - start_time)
    print(boxes)
    sum += boxes.size(0)
    for i in range(boxes.size(0)):
        box = boxes[i, :]
        print(box)
        cv2.rectangle(orig_image, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 0, 255), 2)
        # label = f"""{voc_dataset.class_names[labels[i]]}: {probs[i]:.2f}"""
        label = f"{probs[i]:.2f}"
        # cv2.putText(orig_image, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(orig_image, str(boxes.size(0)), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imwrite(r"result_test/test.jpg", orig_image)
    cv2.waitKey(0) 
    print(sum)

detect(img_path=r"/home/pi/data/smart_house/src/speed_compare/test.jpg", net_type='slim')