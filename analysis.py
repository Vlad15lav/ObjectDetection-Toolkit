import argparse
import os

from factory.format_read import read_xml, read_json, read_txt
from utils.tools import get_whr, analysis_target

def get_args():
    parser = argparse.ArgumentParser('Analysis boudning boxes - Vlad15lav')
    parser.add_argument('-p', '--path', type=str, help='path dataset')
    parser.add_argument('-s', '--sample', type=str, default='train', help='name sample train/val')
    parser.add_argument('-f', '--format', type=str, default='xml', help='format annotation: xml, json, txt')
    parser.add_argument('-c', '--categorys', type=int, nargs="+", default=[32, 96, 128, 256], help='categorys for bounding boxes')
    parser.add_argument('--figsize', type=int, default=16, help='figsize for plots')
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
    analysis_target(label_array, width, height, ratio, categorys=opt.categorys, opt.figsize)
