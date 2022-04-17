from os import times_result
import streamlit as st
from PIL import Image
import requests
import cv2
import time
from models import encoding_img, decoding_img


if __name__=='__main__':

    url1 = ' http://127.0.0.2:8080/detect_card'
    url2 = ' http://127.0.0.2:8080/recognize_text'

    file = st.file_uploader(label='')
    if file != None:
        
        img = Image.open(file)
        st.image(img, caption='QUERY', width=233)

        path = f'./imgs/{time.time()}.jpg'
        img.save(path)
        img = cv2.imread(path)
        img = encoding_img(img)

        reponse = requests.post(url1, data={'img': img}).json()
        card = reponse['img']
        if card is not None:
            reponse = requests.post(url2, data={'img': card}).json()
            output_image = decoding_img(reponse['img'])
            texts = reponse['texts']
            st.image(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB))
            st.write(texts)
        else:
            st.write('Non-detected ID CARD')