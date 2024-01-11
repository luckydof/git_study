from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import re


# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
# ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory


class TextOCR:
    def __init__(self):
        self.rec_ocr = PaddleOCR(use_angle_cls=True, lang="ch",
                                 rec_model_dir='models/rec/ch/ch_PP-OCRv4_rec_infer',
                                 cls_model_dir='models/cls/ch_ppocr_mobile_v2.0_cls_infer',
                                 det_model_dir='models/det/ch/ch_PP-OCRv4_det_infer')

    def rec(self, img_path):
        # need to run only once to download and load model into memory
        result = self.rec_ocr.ocr(img_path, cls=True)
        # for idx in range(len(result)):
        #     res = result[idx]
        #     for line in res:
        #         print(line)
        # 显示结果

        result = result[0]
        image = Image.open(img_path).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        return txts
        # for t in txts:
        #     print(t)
        # print(txts)
        # temp = dict(zip([i for i in txts if txts.index(i) % 2 == 0], [i for i in txts if txts.index(i) % 2 != 0]))
        # print(temp)
        # scores = [line[1][1] for line in result]
        # im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
        # im_show = Image.fromarray(im_show)
        # im_show.save('result.jpg')


if __name__ == '__main__':
    text_ocr = TextOCR()
    res = text_ocr.rec("test_image/test_5.png")
    for i in res:
        print(i)
    print(res)