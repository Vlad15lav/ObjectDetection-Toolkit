import os
import glob
import xml.etree.ElementTree as ET
import json

# PASCAL VOC annotation
def read_xml(path):
    imgs_path, bboxs, labels = [], [], []
    path_ann = os.path.join(path, "annotations")
    path_img = os.path.join(path, "JPEGImages")
    paths = [p.replace("\\", '/') for p in glob.glob("{}/*.xml".format(path_ann))]
    
    for xml_file in paths:
        tree = ET.parse(xml_file)
        imgs_path.append(os.path.join(path_img, tree.findtext("filename")))
        
        bbox_list, label_list = [], []
        for i, obj in enumerate(tree.iter("object")):
            # Xmin, Ymin, Xmax, Ymax format
            xmin = int(obj.findtext("bndbox/xmin"))
            ymin = int(obj.findtext("bndbox/ymin"))
            xmax = int(obj.findtext("bndbox/xmax"))
            ymax = int(obj.findtext("bndbox/ymax"))
            bbox_list.append([xmin, ymin, xmax, ymax])
            label_list.append(obj.findtext("name"))
        
        bboxs.append(bbox_list)
        labels.append(label_list)
    
    return imgs_path, bboxs, labels

# COCO annotation
def read_json(path, sample='train'):
    imgs_path, bboxs, labels = [], [], []
    path_ann = os.path.join(path, "annotations")
    path_img = os.path.join(path, sample)
    
    f = open(os.path.join(path_ann, "instances_{}.json".format(sample)), 'r')
    obj = json.load(f)
    f.close()
    
    imgs, gt = obj['images'], obj['annotations']
    num_img, num_gt = len(obj['images']), len(obj['annotations'])
    imgs_path, bboxs, labels = [], [], []
    cur_gt = 0
    for i in range(num_img):        
        imgs_path.append(os.path.join(path_img, imgs[i]['file_name']))
        
        bbox_list, label_list = [], []
        while gt[cur_gt]['image_id'] == i:
            # xc, yc, width, height
            bbox_list.append(gt[cur_gt]['bbox'])
            label_list.append(gt[cur_gt]['category_id'])
            cur_gt += 1
            
            if cur_gt == num_gt:
                break
        
        bboxs.append(bbox_list)
        labels.append(label_list)

    return imgs_path, bboxs, labels