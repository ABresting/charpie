import cv2
import random
import plac

import numpy as np
from pdf2image import convert_from_path
from pathlib import Path

import pytesseract

def process_single_page(pil_img, page_no, max_text_threshold=100, area_threshold=0.8, min_height=300, min_width=300, output_dir=None):
    open_cv_img = np.array(pil_img)
    open_cv_img = open_cv_img[:, :, ::-1].copy()
    canvas = open_cv_img.copy()
    canvas2= open_cv_img.copy()
    gray_image = cv2.cvtColor(open_cv_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray_image, (11, 11), 0) 
    edged = cv2.Canny(blur, 0, 100)
    dilated = cv2.dilate(edged, np.ones((21, 21)))
    _, contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    total_text = []
    rects = [cv2.boundingRect(c) for c in contours]
    rect_c = [((x+w/2), (y+h/2)) for x, y, w, h in rects]

    def c_falls_in_rect(c, r):
        x, y, w, h = r
        x_c, y_c = c
        return (x <= x_c <= x+w) and (y <= y_c <= y+h)

    def num_of_c_in_rect(r):
        return sum([1 for c in rect_c if c_falls_in_rect(c, r)])

    cs_in_rects = [num_of_c_in_rect(r) for r in rects]

    rects = [r for r, x in zip(rects, cs_in_rects) if x <=2]

    
    def score_fn(r):
        x, y, w, h = r
        return (x+w/2)**1.5 + (y+h/2)**1.5

    for i, rect in enumerate(sorted(rects, key=score_fn)):
        print(f'{i} of {len(contours)}')
        # rect = cv2.boundingRect(contour)
        x, y, w, h = rect
        b, g = random.sample(range(0, 255), 2)
        # if w < min_width and h < min_height:
        #     continue
        # if w/h >= 2.1 or h/w>=2.5:
        #     continue
        cv2.rectangle(canvas2, (x,y), ((x+w), (y+h)), (b, g, 255), 10)
        roi = canvas[y:y+h, x:x+w]

        text_in_img = pytesseract.image_to_string(roi)
        cv2.imwrite(f'working.jpeg', canvas2)
        if len(text_in_img) >= 20:
            total_text.append(text_in_img)
        
        # text_box = pytesseract.image_to_data(roi, output_type='data.frame').dropna()
        # text_box = text_box[text_box.conf>=90] # reconsider
        # # import pdb; pdb.set_trace()
        # input_area = w * h
        # text_output_area = 0.01
        # for i, row in text_box.iterrows():
        #     if len(row.text):
        #         text_output_area += row.width * row.height

        # if text_output_area / input_area >= area_threshold:
        #     continue
        
        print("writing this one")
        # cv2.imwrite(f'{output_dir}/{page_no}_{i}_{x}_{y}.jpg', roi)

    reduced_text = ''

    total_text = [' '.join(t.split()) for t in total_text]

    for t in total_text:
        if reduced_text.find(t) == -1:
            reduced_text += t + '\n'

    # print('\n'.join(total_text))

    #print(reduced_text)
    open(f'{output_dir}/{page_no}.txt', 'w').write(reduced_text)
    
    return canvas2


def main(filename, output_dir, num_pages=None):
    Path(output_dir+'/full/').mkdir(parents=True, exist_ok=True)
    print('reading pdf into image')
    pages = convert_from_path(filename)
    for i, p in enumerate(pages):
        if num_pages is not None and int(num_pages) < i:
            break
        print(f'processing page {i}')
        deco = process_single_page(p, page_no=i, output_dir=output_dir)
        # cv2.imwrite(f'{output_dir}/full/full{i}.jpg', deco)


if __name__ == '__main__':
    plac.call(main)
