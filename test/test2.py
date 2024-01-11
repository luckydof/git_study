from paddleocr import PaddleOCR
from PIL import Image

ocr = PaddleOCR(lang="ch", show_log=False)
img = Image.open('test.png')
import numpy as np

result = ocr.ocr(np.array(img))
print(result)


def sort_paddle_result(result, val=10):
    '''
    对paddle返回的结果排序，默认纵坐标不超过10的为一行
    Args:
        result:paddle返回原始结果
val ：
    Returns:

    '''
    result.sort(key=lambda x: x[0][0][1])  # y排序
    first_dot = result[0][0][0]
    other_dots = [x[0][0] for x in result[1:]]
    sort_dots = [[first_dot]]  # 第一个点  在第一行
    index = 0
    for dot in other_dots:
        if sort_dots[index] == [] or abs(dot[1] - np.mean([x[1] for x in sort_dots[index]])) < val:  # 同一行
            sort_dots[index].append(dot)
        else:  # 第二行
            index += 1
            sort_dots.append([dot])
    print('共有%s行' % len(sort_dots))
    sort_result = []
    for dot in sort_dots:  # [item for sublist in sort_dots for item in sublist]:
        # ocr_result = [x for x in result if x[0][0] == dot]
        ocr_result = [x for x in result if x[0][0] in dot]
        sort_result.append(ocr_result)

    for sublist in sort_result:
        sublist.sort()

    sort_result = [item for sublist in sort_result for item in sublist]  # 返回原始格式
    print(sort_result)
    return sort_result
