import cv2
import numpy as np


def convert_to_grayscale(img):
    try:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    finally:
        return img


def show(img):
    value = np.max(img)
    img = img * (255 / value)
    img = img.astype(np.uint8)
    return img


def hist_equal(img):
    newImg = convert_to_grayscale(img)
    newImg = cv2.equalizeHist(newImg)
    return [newImg]


def thresholding(img, thresh=127, maxVal=255):
    newImg = convert_to_grayscale(img)
    newImg = cv2.threshold(newImg, thresh, maxVal, cv2.THRESH_BINARY)[1]
    return [show(newImg)]


def negative(img):
    newImg = convert_to_grayscale(img)
    newImg = 255 - newImg
    return [show(newImg)]


def logarith(img):
    newImg = convert_to_grayscale(img)
    c = 255 / np.log(1 + np.max(newImg))
    newImg = c * (np.log(newImg + 1))
    return [show(newImg)]


def normalize(img, alpha=0, beta=255):
    newImg = convert_to_grayscale(img)
    newImg = cv2.normalize(newImg, None, alpha, beta, cv2.NORM_MINMAX)
    return [show(newImg)]
