import cv2
import os


def convert_cood(bb, img_shape):
    x, y, w, h = bb
    w, h = w/2, h/2
    xmin = x-w
    ymin = y-h
    xmax = x+w
    ymax = y+h
    xmin, ymin, xmax, ymax = int(xmin*img_shape[1]), int(ymin*img_shape[0]), int(xmax*img_shape[1]), int(ymax*img_shape[0]) 
    return ((xmin, ymin), (xmax, ymax))


cls_list = ['bottom_left', 'bottom_right', 'top_right', 'top_left', 'id_no', 'cid_no',\
    'name', 'cname', 'dob', 'cdob', 'nationality', 'cnationality', 'address', 'caddress', \
    'issued_place', 'issued_date', 'class', 'cclass', 'expires', 'cexpires', 'stamp', 'classification',\
     'seri', 'beginning_date', 'cbeginning_date', 'number', 'qrcode', 'birth']

print(len(cls_list))


if __name__ == '__main__':

    txt_path = 'data/data-text-all-voc/img_15.txt'
    path = 'data/data-text-all-voc/img_15.jpg'
    img = cv2.imread(path)
    img_shape = img.shape
    print(img_shape)

    with open(txt_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            text = line.strip()
            cls, x, y, w, h = [float(i) for i in text.split(' ')]
            (xmin, ymin), (xmax, ymax) = convert_cood((x, y, w, h), img_shape)
            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color=(0, 0 , 255), thickness=1)
            cv2.putText(img, cls_list[int(cls)], (xmin, ymin-10), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(0, 0, 255), thickness=2)

    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
