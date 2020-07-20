import cv2
import os
import numpy as np
import threading
import logging

logger = logging.getLogger(__name__)


def preprocess_img(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # smooth the image to avoid noises
    gray = cv2.medianBlur(gray, 5)

    # Apply adaptive threshold
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_TOZERO_INV)

    thresh = cv2.dilate(thresh, None, iterations=50)
    thresh = cv2.erode(thresh, None, iterations=50)
    return thresh


def find_page_area(img):
    # Find the contours
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    contours_filtered = []
    for cnt in contours:
        a = cv2.contourArea(cnt)
        if a > max_area:
            max_area = a

    for cnt in contours:
        a = cv2.contourArea(cnt)
        if a < max_area and a > 100:
            rect = cv2.minAreaRect(cnt)
            contours_filtered.append(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

    contours_all = np.concatenate(contours_filtered, axis=0)
    hull = cv2.convexHull(contours_all)
    rect = cv2.minAreaRect(hull)
    return rect


def get_crop_points(rect):

    box = cv2.boxPoints(rect)
    dist_01 = int(cv2.norm(box[0], box[1]))
    box = np.int0(box)
    w = int(rect[1][0])
    h = int(rect[1][1])

    dist_h = np.abs(dist_01 - h)
    dist_w = np.abs(dist_01 - w)

    if dist_h < dist_w: # vertical box
        return w, h, box, np.array([
                            [0, h-1],
                            [0, 0],
                            [w-1, 0],
                            [w-1, h-1]], dtype="float32")
    else: # horizontal box
        return w, h, box, np.array([
                            [w-1, h-1],
                            [0, h-1],
                            [0, 0],
                            [w-1, 0]], dtype="float32")


def process(filename, output_dir, save_intermediary=False):
    #print(f"{threading.currentThread().getName()}: Processing {filename}")
    basename = os.path.basename(filename)
    img = cv2.imread(filename)
    thresh = preprocess_img(img)
    rect = find_page_area(thresh)
    angle = rect[-1]
    rect_angle = 0
    do_rotate = False
    if angle < -45:
        angle += 90
        rect_angle = -90
        do_rotate = True
    logger.debug(f"{filename} skew: {angle}")
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    img = cv2.warpAffine(img, M, (w, h),
                         flags=cv2.INTER_CUBIC,
                         borderMode=cv2.BORDER_REPLICATE)

    width_margin = 200
    height_margin = 200
    rect = (rect[0], (rect[1][0] + width_margin,
                      rect[1][1] + height_margin), rect_angle)

    w, h, src_pts, dst_pts = get_crop_points(rect)

    # the perspective transformation matrix
    M = cv2.getPerspectiveTransform(src_pts.astype('float32'), dst_pts)

    # directly warp the rotated rectangle to get the straightened rectangle
    warped = cv2.warpPerspective(img, M, (w, h))
    img = cv2.drawContours(img, [src_pts], 0, (0, 255, 0), 2)

    if do_rotate:
        warped = np.rot90(warped)

    if save_intermediary:
        no_ext = basename[:basename.find(".tif")]
        cv2.imwrite(os.path.join(output_dir, f"{no_ext}_area.png"), img)
        cv2.imwrite(os.path.join(output_dir, f"{no_ext}_internal.png"), thresh)
    cv2.imwrite(os.path.join(output_dir, basename), warped)


if __name__ == "__main__":

    import pathlib
    filename = "mlu_001_1995_086_00048_1226.tif"
    cwd = os.getcwd()
    dst = os.path.join(cwd, "tests")
    pathlib.Path(dst).mkdir(parents=True, exist_ok=True)
    process(os.path.join(cwd, filename), dst, True)
