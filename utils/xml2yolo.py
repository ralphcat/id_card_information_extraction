import os
from xml.dom import minidom
from tqdm import tqdm


def convert_coordinates(size, box):
    dw = 1.0/size[0]
    dh = 1.0/size[1]
    x = (box[0]+box[1])/2.0
    y = (box[2]+box[3])/2.0
    w = box[1]-box[0]
    h = box[3]-box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)


def convert_xml2yolo(path):

    xmldoc = minidom.parse(path)
    itemlist = xmldoc.getElementsByTagName('object')
    size = xmldoc.getElementsByTagName('size')[0]
    width = int((size.getElementsByTagName('width')[0]).firstChild.data)
    height = int((size.getElementsByTagName('height')[0]).firstChild.data)

    save_path = path.split('.')[0] + '.txt'
    with open(save_path, 'w') as file:

        for item in itemlist:
            cls =  (item.getElementsByTagName('name')[0]).firstChild.data
            xmin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmin')[0]).firstChild.data
            ymin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymin')[0]).firstChild.data
            xmax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmax')[0]).firstChild.data
            ymax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymax')[0]).firstChild.data
            b = (float(xmin), float(xmax), float(ymin), float(ymax))
            bb = convert_coordinates((width,height), b)
            
            line = ' '.join(str(i) for i in [cls2id[cls], *bb]) + '\n'
            file.write(line)
        


cls_list = ['bottom_left', 'bottom_right', 'top_right', 'top_left', 'id_no', 'cid_no',\
    'name', 'cname', 'dob', 'cdob', 'nationality', 'cnationality', 'address', 'caddress', \
    'issued_place', 'issued_date', 'class', 'cclass', 'expires', 'cexpires', 'stamp', 'classification',\
     'seri', 'beginning_date', 'cbeginning_date', 'number', 'qrcode', 'birth']

cls2id = {}
for i, cls in enumerate(cls_list):
    cls2id[cls] = i

dir = 'data/data-text-all-voc/'

for name_file in tqdm(os.listdir(dir)):
    if name_file.split('.')[-1] == 'xml':
        path = os.path.join(dir, name_file)
        convert_xml2yolo(path)

