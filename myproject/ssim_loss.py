# USAGE
# python ssim_loss.py --first images/pathA --second images/pathB

# import the necessary packages
from skimage.metrics import structural_similarity
import argparse
import imutils
import cv2
import numpy as np
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--first", required=True,
	help="first input image")
ap.add_argument("-s", "--second", required=True,
	help="second")
args = vars(ap.parse_args())

i = 0
for filename in os.listdir(args["first"]):
	filename_wo_extA = filename.split('.')[0]
	suffix_numberA = filename_wo_extA.split('_')[1]

	filename_wo_extB = os.listdir(args["second"])[0].split('.')[0]
	file_name_prefix = filename_wo_extB.split('_')[0]
	suffix_numberB = filename_wo_extB.split('_')[1]


	imageA = cv2.imread(os.path.join(args["first"],filename))
	imageB = cv2.imread(os.path.join(args["second"],file_name_prefix + '_' + suffix_numberA + '.png'))

	if imageA is None or imageB is None:
		print('Warning: one of the images with suffix id = {} is None'.format(suffix_numberA))
	else:

		#resize images
		w1 = max(imageA.shape[0], imageB.shape[0])
		w2 = max(imageA.shape[1], imageB.shape[1])

		imageA = cv2.resize(imageA, (w1, w2))
		imageB = cv2.resize(imageB, (w1, w2))



		# convert the images to grayscale
		grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
		grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

		# compute the Structural Similarity Index (SSIM) between the two
		# images, ensuring that the difference image is returned
		(score, diff) = structural_similarity(grayA, grayB, full=True)
		diff = (diff * 255).astype("uint8")
		print("SSIM: {}".format(score))

		# threshold the difference image, followed by finding contours to
		# obtain the regions of the two input images that differ
		thresh = cv2.threshold(diff, 0, 255,
			cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]
