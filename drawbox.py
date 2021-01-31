import argparse
import os

from factory.format_read import read_xml, read_json, read_txt
from utils.drawing import draw_sample, draw_batch

def get_args():
    parser = argparse.ArgumentParser('Analysis boudning boxes - Vlad15lav')
    parser.add_argument('-p', '--path', type=str, help='path dataset')
    parser.add_argument('-s', '--sample', type=str, default='train', help='name sample train/val')
    parser.add_argument('-f', '--format', type=str, default='xml', help='format annotation: xml, json, txt')
    parser.add_argument('--xyxy', help='xyxy - format PASCAL VOC', action="store_true")
    parser.add_argument('--batch', type=int, nargs="+", default=[0, 0], help='select batch interval')
    parser.add_argument('--scale', type=int, default=1, help='scale targets')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    opt = get_args()

    # Check arg batch
    left, right = opt.batch
    if len(opt.batch) != 2 or left > right or left < 0:
        raise ValueError('Incorrect selected sample')

    # Read dataset
    if opt.format == 'xml':
    	imgs, bbox, label = read_xml(opt.path, opt.sample)
    elif opt.format == 'json':
    	imgs, bbox, label = read_json(opt.path, opt.sample)
    elif opt.format == 'txt':
    	imgs, bbox, label = read_txt(opt.path, opt.sample)
    else:
    	raise ValueError('Undefined format')
    
    if right >= len(imgs):
        raise ValueError('Incorrect selected sample')

    # Draw selected bouding boxes
    draw_batch(imgs[left:right], bbox[left:right], label[left:right], scale=opt.scale, xyxy=opt.xyxy)
