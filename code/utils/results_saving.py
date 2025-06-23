# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 21:17:11 2020

@author: Ali Hamdi; ali.ali@rmit.edu.au
"""

import utils.bbox_helper as bbox_helper
import utils.config_helper as config
from scipy.spatial import distance
import pandas as pd
import os
import cv2

def save_tracking_results(title, class_dir, file, bbox, gt_box, s, extime, full_filepath):
    center   = bbox_helper.get_bbox_center(bbox)
    gtcenter = bbox_helper.get_bbox_center(gt_box)
    img = cv2.imread(full_filepath, 0)
    iou = bbox_helper.intersection_over_union(bbox_helper.get_bbox_points(gt_box),
                                                              tuple(i * s for i in bbox_helper.get_bbox_points(bbox)))
    
    results = [title, class_dir, file, bbox[0]*s, bbox[1]*s, bbox[2]*s, bbox[3]*s, 
                                   center[0]*s, center[1]*s, 
                                   iou,
                                   distance.euclidean((gtcenter[0], gtcenter[1]), (center[0]*s, center[1]*s)),
                                   extime]

    # Define your bounding box: (x1, y1, x2, y2)
    bbox = (bbox[0]*s, bbox[1]*s, bbox[0]*s + bbox[2]*s, bbox[1]*s + bbox[3]*s)  # example values

    # Draw the bounding box
    cv2.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color=(0, 255, 0), thickness=2)

    # Prepare the IOU text
    iou_text = f"IOU: {iou:.2f}"

    # Get text size to place it **below** the box
    (font_width, font_height), baseline = cv2.getTextSize(iou_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

    # Define position: just below the box (x1, y2 + some padding)
    text_x = int(bbox[0])
    text_y = int(bbox[3] + font_height + 5)

    # Draw the text
    cv2.putText(img, iou_text, (text_x, text_y),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5,
                color=(0, 255, 0),
                thickness=1,
                lineType=cv2.LINE_AA)

    # Root path where you want to save images
    save_root = "/code/results"

    # Full path to save the image
    save_path = os.path.join(save_root, title, class_dir)

    # Ensure the directory exists
    os.makedirs(save_path, exist_ok=True)

    # Final full file path
    full_filename = os.path.join(save_path, file)

    # Save the image
    cv2.imwrite(full_filename, img)

    dataframe = pd.DataFrame([results], columns=None)
    print(dataframe)
    with open('/code/results/DroTrack_results_evaluation.csv', 'a') as f:
        dataframe.to_csv(f, index = False, header=None)