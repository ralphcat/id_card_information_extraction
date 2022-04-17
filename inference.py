import cv2
from flask import Flask, request, jsonify
from models import Card_Detector, Text_Recognitor, TextCard_Detector, encoding_img, decoding_img


app = Flask(__name__)
card_detector = Card_Detector("./weights/card_weight.onnx")
textcard_detector= TextCard_Detector("./weights/text_card_weight_final.onnx")
text_recognitor = Text_Recognitor()


@app.route('/detect_card', methods=['POST'])
def detect_idcard():
    
    img = request.form.get('img')
    img = decoding_img(img)
    img = card_detector.predict(img)
    
    if img is not None:
        w = 640
        h = int(w*img.shape[0] / img.shape[1])
        img = cv2.resize(img, (w, h))
        img = encoding_img(img)
        return jsonify({'img': img})
    return jsonify({'img': None})


@app.route('/recognize_text', methods=['POST'])
def recognize_text():
    
    img = request.form.get('img')
    img = decoding_img(img)
    output_image, outputs = textcard_detector.predict(img.copy())
    cls2info = {}

    if outputs is not None:
        for output in outputs:
            cls = output[0]
            top_left = output[1][0]
            bottom_right = output[1][1]
            temp = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
            text = text_recognitor.predict(temp)

            if cls in cls2info.keys():
                cls2info[cls] = ', '.join([cls2info[cls], text])
            else:
                cls2info[cls] = text 

    output_image = encoding_img(output_image)               
    return jsonify({'img': output_image, 'texts': cls2info})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.2', port=8080)