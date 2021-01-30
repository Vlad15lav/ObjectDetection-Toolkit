import argparse
import os
import yaml
import numpy as np

from factory.format_write import write_xml, write_json

class Params:
    def __init__(self, project_file):
        self.params = yaml.safe_load(open(project_file).read())

    def __getattr__(self, item):
        return self.params.get(item, None)

def get_args():
    parser = argparse.ArgumentParser('Analysis boudning boxes - Vlad15lav')
    parser.add_argument('-p', '--path', type=str, help='path dataset')
    parser.add_argument('-s', '--sample', type=str, default='train', help='name sample train/val')
    parser.add_argument('-f', '--format', type=str, default='xml', help='format annotation: xml, json, txt')
    parser.add_argument('--wformat', type=str, default='xml', help='write format annotation: xml, json, txt')
    parser.add_argument('--config', type=str, help='yml file with targets')
    parser.add_argument('--xyxy', help='xyxy - format PASCAL VOC', action="store_true")
    #parser.add_argument('--img_size', type=int, default=1, help='scale bounding boxes for normalized')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    opt = get_args()
    params = Params(f'config/{opt.config}.yml')

    if opt.format == 'xml':
    	imgs, bbox, label = read_xml(opt.path, opt.sample)
    elif opt.format == 'json':
    	imgs, bbox, label = read_json(opt.path, opt.sample)
    elif opt.format == 'txt':
    	raise ValueError('format not ready')
    else:
    	raise ValueError('Undefined format')

    if opt.wformat == 'xml':
    	write_xml(imgs, bbox, label, xyxy=opt.xyxy, mask=params.targets)
    elif opt.wformat == 'json':
    	write_json(imgs, bbox, label, xyxy=opt.xyxy, mask=params.targets)
    elif opt.wformat == 'txt':
    	raise ValueError('format not ready')
    else:
    	raise ValueError('Undefined format')
