import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Load the original image
path = input('Enter the path of the image: ')
img = cv2.imread(path)

# Convert the image to PIL format
pil_img = Image.fromarray(img)

# Define the text to be used as the watermark
watermark_text = input('Enter the text to be used as watermark: ')

# Define the font and size of the text
size = int(input('Enter the size of the text: '))
font = ImageFont.truetype('Arial.ttf', size)

# Get the size of the text
text_width, text_height = font.getsize(watermark_text)

# Create a new image with the same size as the original image
watermark_img = Image.new('RGBA', pil_img.size, (255, 255, 255, 0))

# Draw the text onto the new image
draw = ImageDraw.Draw(watermark_img)
draw.text(((pil_img.width - text_width) / 2, (pil_img.height - text_height) / 2),
          watermark_text, font=font, fill=(255, 255, 255, 128))

# Convert the watermark image back to OpenCV format
watermark = cv2.cvtColor(np.array(watermark_img), cv2.COLOR_RGBA2BGRA)

# Overlay the watermark image onto the original image
img_height, img_width, _ = img.shape
watermark_height, watermark_width, _ = watermark.shape

x_pos = int((img_width - watermark_width) / 2)
y_pos = int((img_height - watermark_height) / 2)

for c in range(0, 3):
    img[y_pos:y_pos+watermark_height, x_pos:x_pos+watermark_width, c] = \
        watermark[:,:,c] * (watermark[:,:,3]/255.0) + \
        img[y_pos:y_pos+watermark_height, x_pos:x_pos+watermark_width, c] * (1.0 - watermark[:,:,3]/255.0)

# Save the watermarked image
rename = input('Enter the name of the watermarked image: ')
cv2.imwrite(rename, img)
