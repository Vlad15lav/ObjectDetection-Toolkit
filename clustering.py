import argparse
import os

from factory.format_read import read_xml, read_json, read_txt
from utils.tools import get_whr, decomposit_boxes
from kmeans.base import Kmeans

def get_args():
    parser = argparse.ArgumentParser('Analysis boudning boxes - Vlad15lav')
    parser.add_argument('--c', '--clusters', type=int, default=3, help='number of clusters')
    parser.add_argument('--anchorbs', '--basescale', type=int, default=4, help='anchor base scale')
    parser.add_argument('--anchors', '--stride', type=int, default=8, help='anchor stride')
    parser.add_argument('-p', '--path', type=str, help='path dataset')
    parser.add_argument('-s', '--sample', type=str, default='train', help='name sample train/val')
    parser.add_argument('-f', '--format', type=str, default='xml', help='format annotation: xml, json, txt')
    parser.add_argument('--xyxy', help='xyxy - format PASCAL VOC', action="store_true")
    parser.add_argument('--scale', type=int, default=1, help='scale targets')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    opt = get_args()

    if opt.format == 'xml':
    	imgs, bbox, label = read_xml(opt.path, opt.sample)
    elif opt.format == 'json':
    	imgs, bbox, label = read_json(opt.path, opt.sample)
    elif opt.format == 'txt':
    	imgs, bbox, label = read_txt(opt.path, opt.sample)
    else:
    	raise ValueError('Undefined format')
	
    label_array, width, height, ratio = get_whr(bbox, label, xyxy=opt.xyxy, scale=opt.scale)

    kmeans = Kmeans(cluster_number=opt.clusters)
    bboxes = np.append([width], [height], axis=0).T
    result = kmeans.fit(bboxes)
    print("Decomposit boxes: scale - {}, ratio - {}"
        .format(*decomposit_boxes(result, anchor_base_scale=opt.anchorbs, anchor_stride=opt.anchors)))