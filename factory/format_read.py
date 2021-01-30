import os
import glob
import xml.etree.ElementTree as ET
import json

from pycocotools.coco import COCO

# PASCAL VOC annotation
def read_xml(path, sample='train'):
    imgs_path, bboxs, labels = [], [], []
    path_ann = os.path.join(path, "annotations")
    path_img = os.path.join(path, "JPEGImages")
    paths = [os.path.join(path_ann, l.strip().split(None, 1)[0] + '.xml')
                 for l in open(os.path.join(path, 'ImageSets', 'Main', sample + '.txt')).readlines()]
    
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
    path_img = os.path.join(path, sample)

    coco = COCO(os.path.join(path, 'annotations', 'instances_' + sample + '.json'))
    image_ids = coco.getImgIds()

    for i in range(len(image_ids)):
        image_info = coco.loadImgs(image_ids[i])[0]
        imgs_path.append(os.path.join(path_img, image_info['file_name']))

        annotations_ids = coco.getAnnIds(imgIds=image_ids[i], iscrowd=False)
        coco_annotations = coco.loadAnns(annotations_ids)

        bbox_list, label_list = [], []
        for idx, a in enumerate(coco_annotations):
            bbox_list.append(a['bbox'])
            label_list.append(a['category_id'])

        bboxs.append(bbox_list)
        labels.append(label_list)
    
    return imgs_path, bboxs, labels
