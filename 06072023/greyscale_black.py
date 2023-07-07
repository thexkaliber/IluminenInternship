from PIL import Image, ImageEnhance
import numpy as np

img = Image.open("manga.png") #Fetch the image
print('Filename: ',img.filename, end="\n") #Display File Information
print('Size (Height x Width): ',img.size, end="\n")
print('Format: ',img.format, end="\n")
print('Mode: ',img.mode, end="\n")


print('\nConverting ' + img.filename + ' into a matrix', end="\n") #Convert image into a Numpy Array
img = img.convert('L')
img_matrix = np.array(img)
print('\nOriginal image data:\n',img_matrix)

img_matrix = np.where((img_matrix==0) | (img_matrix==255),img_matrix, 0) #Replace all pixels which aren't Black or White to Black
print('\nModified image data (Blacken):\n',img_matrix)

print('\nSaving as a 1bit BMP file...') #Save the image as a Black and White BMP File
img_blacked = Image.fromarray(img_matrix).convert('1')
img_blacked.save('Greyscale_black.bmp')
print('Saved file.')
