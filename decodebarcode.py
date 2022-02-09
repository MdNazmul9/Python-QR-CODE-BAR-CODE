import cv2 # Read image / camera/video input
from pyzbar.pyzbar import decode

img = cv2.imread("output_qrcode_or_barcode11.png")
print(decode(img))
