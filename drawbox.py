import argparse
import os

from factory.format_read import read_xml, read_json
from utils.drawing import draw_sample, draw_batch

def get_args():
    parser = argparse.ArgumentParser('Analysis boudning boxes - Vlad15lav')
    parser.add_argument('-p', '--path', type=str, help='path dataset')
    parser.add_argument('-f', '--format', type=str, default='xml', help='format annotation: xml, json, txt')
    parser.add_argument('--xyxy', help='xyxy - format PASCAL VOC', action="store_true")
    parser.add_argument('--sample', type=int, nargs="+", default=[0, 10], help='select sample interval')
    parser.add_argument('--img_size', type=int, default=1, help='scale bounding boxes for normalized')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    opt = get_args()

    # Check arg sample
    if len(opt.sample) != 2 or opt.sample[0] > opt.sample[1]:
        raise ValueError('Incorrect selected sample')

    # Read dataset
    if opt.format == 'xml':
    	imgs, bbox, label = read_xml(opt.path)
    elif opt.format == 'json':
    	imgs, bbox, label = read_json(opt.path)
    elif opt.format == 'txt':
    	raise ValueError('format not ready')
    else:
    	raise ValueError('Undefined format')

    left, right = opt.sample

    if left < 0 or right >= len(imgs):
        raise ValueError('Incorrect selected sample')

    # Draw selected bouding boxes
    draw_batch(imgs[left:right], bbox[left:right], label[left:right])