import os
import json
import xml.etree.ElementTree as ET

from xml.etree import ElementTree

def write_xml(imgs_path, bboxs, labels, xyxy=True, mask=None):
    if not os.path.exists('annotation'):
        os.makedirs('annotation')
    
    ds_name = imgs_path[0].split('\\')[0]
    
    for i_img in range(len(imgs_path)):
        ann_xml = ET.Element('annotation')

        folder = ET.Element('folder')
        folder.text = ds_name
        ann_xml.append(fold)

        filename = ET.Element('filename')
        filename.text = imgs_path[i_img].split('\\')[-1]
        ann_xml.append(filename)

        source = ET.Element('source')
        database = ET.Element('database')
        database.text = 'The {} database'.format(ds_name)
        source.append(database)
        ann_xml.append(source)
        
        for (bbox, label) in zip(bboxs[i_img], labels[i_img]):  
            obj = ET.Element('object')

            name = ET.Element('name')
            name.text = mask[int(label) - 1]
            obj.append(name)

            bndbox = ET.Element('bndbox')
            xmin, ymin = ET.Element('xmin'), ET.Element('ymin')
            xmax, ymax = ET.Element('xmax'), ET.Element('ymax')
            
            if xyxy:
                xmin.text, ymin.text, xmax.text, ymax.text = list(map(str, bbox))
            else:
                bbox[2] += bbox[0] # xywh2xyxy
                bbox[3] += bbox[1]
                xmin.text, ymin.text, xmax.text, ymax.text = list(map(str, bbox))
            
            bndbox.append(xmin)
            bndbox.append(ymin)
            bndbox.append(xmax)
            bndbox.append(ymax)
            obj.append(bndbox)

            ann_xml.append(obj)
        
        tree = ElementTree.ElementTree()
        tree._setroot(ann_xml)
        tree.write('annotation/{}.xml'.format(filename.text.split('.')[0]))

def write_json(imgs_path, bboxs, labels, xyxy=True, mask=None):
    if not os.path.exists('annotation'):
        os.makedirs('annotation')
    
    ds_name = imgs_path[0].split('\\')[0]
    ann_json = {'info': ds_name, 'images': [], 'annotations': []}
    ann_json['images'] = [{'id': i, 
                           'file_name': imgs_path[i].split('\\')[-1]}
                          for i in range(len(imgs_path))]
    
    mask_arr = {mask[i]:i + 1 for i in range(len(mask))}
    ann_idx = 0
    for i_img in range(len(imgs_path)):
        for i, (bbox, label) in enumerate(zip(bboxs[i_img], labels[i_img])):
            if xyxy:
                xmin, ymin, xmax, ymax = bbox
                w, h = xmax - xmin, ymax - ymin
            else:
                xmin, ymin, w, h = bbox
            
            ann_tag = {'id': ann_idx, 'image_id': i_img,
                   'category_id': mask_arr[label], 'area': w * h,
                  'bbox': [xmin, ymin, w, h]}
            ann_idx += 1
            ann_json['annotations'].append(ann_tag)
    
    with open('annotation/instances_.json', 'w') as f:
        json.dump(ann_json, f)

def write_txt(imgs_path, bboxs, labels, scale=1, sample='train', mask=None):
    labels_path = 'labels/{}'.format(sample)
    if not os.path.exists(labels_path):
        os.makedirs(labels_path)
    
    txt_names = [imgs_path[i].split('\\')[-1].split('.')[0] for i in range(len(imgs_path))]
    
    for i_img in range(len(imgs_path)):
        out_txt = ''
        for i, (bbox, label) in enumerate(zip(bboxs[i_img], labels[i_img])):
            box = np.array(bbox) * scale
            
            out_txt += "{} {} {} {} {}\n".format(label, *box.tolist())
            
        with open("{}/{}.txt".format(labels_path, txt_names[i_img]), "w") as outfile:
            outfile.write(out_txt)
