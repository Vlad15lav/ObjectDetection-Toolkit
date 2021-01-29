import argparse
import os

from factory.format_read import read_xml, read_json
from utils.tools import get_whr, analysis_target

def get_args():
    parser = argparse.ArgumentParser('Analysis boudning boxes - Vlad15lav')
    parser.add_argument('-p', '--path', type=str, help='path dataset')
    parser.add_argument('-f', '--format', type=str, default='xml', help='format annotation: xml, json, txt')
    parser.add_argument('-c', '--categorys', type=int, nargs="+", default=[32, 96, 128, 256], help='categorys for bounding boxes')
    parser.add_argument('--figsize', type=int, default=16, help='figsize for plots')
    parser.add_argument('--xyxy', help='xyxy - format PASCAL VOC', action="store_true")
    parser.add_argument('--img_size', type=int, default=1, help='scale bounding boxes for normalized')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    opt = get_args()

    if opt.format == 'xml':
    	imgs, bbox, label = read_xml(opt.path)
    elif opt.format == 'json':
    	imgs, bbox, label = read_json(opt.path)
    elif opt.format == 'txt':
    	raise ValueError('format not ready')
    else:
    	raise ValueError('Undefined format')

    label_array, width, height, ratio = get_whr(bbox, label, xyxy=opt.xyxy)
	analysis_target(label_array, width, height, ratio, categorys=opt.categorys)