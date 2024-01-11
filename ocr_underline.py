from paddleocr import PaddleOCR, draw_ocr
from paddleocr.tools.infer.utility import draw_ocr_box_txt
import keyboard
from PIL import Image, ImageGrab
import time
import os

"""
    pip install paddlepaddle-gpu /  pip install paddlepaddle
    pip install shapely
    将 paddleocr-q 放到本程序同级目录下
    pip install -r requirements.txt
"""
'''
terminal调用
python tools/infer/predict_system.py --image_dir="./doc/imgs/6.jpg" --det_model_dir="./inference/ch_ppocr_mobile_v1.1_det_infer/" --rec_model_dir="./inference/ch_ppocr_mobile_v1.1_rec_infer/" --cls_model_dir="./inference/ch_ppocr_mobile_v1.1_cls_infer/" --use_angle_cls=True --use_space_char=True --use_gpu=False
'''


# 截图到识别
class ScreenShotRec:
    def __init__(self):
        # self.img_path = img_path
        # self.ocr = PaddleOCR(use_angle_cls=True, lang="ch")
        # self.ocr = PaddleOCR(use_angle_cls=True, lang="ch",
        #                      rec_model_dir=r'D:\model\rec_model',
        #                      cls_model_dir=r'D:\model\cls_model',
        #                      det_model_dir=r'D:\model\det_model')
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch",
                             rec_model_dir='models/rec/ch/ch_PP-OCRv4_rec_infer',
                             cls_model_dir='models/cls/ch_ppocr_mobile_v2.0_cls_infer',
                             det_model_dir='models/det/ch/ch_PP-OCRv4_det_infer')
        # need to run only once to download and load model into memory

    # 截图
    # def screenshot(self):
    #     if not keyboard.wait(hotkey='f1'):
    #         if not keyboard.wait(hotkey='ctrl+c'):
    #             time.sleep(0.1)
    #             image = ImageGrab.grabclipboard()
    #             image.save(self.img_path)

    # 识别
    def rec(self, img_path):
        # print("=============================")
        # result = self.ocr.ocr(img_path, cls=True)
        # # for idx in range(len(result)):
        # #     res = result[idx]
        # #     for line in res:
        # #         print(line)
        # image = Image.open(img_path).convert('RGB')
        # boxes = [line[0] for line in result]
        # txts = [line[1][0] for line in result]
        # scores = [line[1][1] for line in result]
        # im_show = draw_ocr(image, boxes, txts, scores, font_path='doc/fonts/simfang.ttf')
        #
        # # 第二种可视化 使用这段需要注释掉第43行的im_show = draw_ocr()
        # # for polygon in boxes:
        # #     for i in range(len(polygon)):
        # #         # 将每个顶点的坐标从列表改为元组
        # #         polygon[i] = tuple(polygon[i])
        # # im_show = draw_ocr_box_txt(image, boxes, txts, scores, font_path='doc/fonts/simfang.ttf')
        #
        # save, _ = os.path.splitext(img_path)
        # save = save + '_result.jpg'
        # im_show = Image.fromarray(im_show)
        # im_show.save(save)

        result = self.ocr.ocr(img_path, cls=True)
        result = result[0]
        image = Image.open(img_path).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        # 识别结果
        # for t in txts:
        #     print(t)
        scores = [line[1][1] for line in result]
        im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
        im_show = Image.fromarray(im_show)
        im_show.save('result.jpg')
        return txts


if __name__ == '__main__':
    scr = ScreenShotRec()
    # scr.screenshot()
    img_path = 'zhengce.png'
    txt = scr.rec(img_path)
    print(txt)
