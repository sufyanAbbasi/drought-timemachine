from PIL import Image
from os import listdir
from os.path import isfile

size = (256, 256)
halfbox1 = (128,0,256,256)
halfbox2 = (0,0,128,256)

def createintermediarytiles(foldername, rows, columns, fileextension):
	images_urls = [foldername + "/" + f for f in listdir(foldername) if (fileextension in f)]
	images = map(Image.open, images_urls)
	print "r: {0}, c: {1}".format(rows, columns)
	currentColumn = -1
	currentRow = 1
	for i in range(rows*columns - rows):
		currentRow += 1
		if not i % rows:
			currentColumn += 1
			currentRow  = 1
		#print str(currentRow) + "," + str(currentColumn)
		createintermediatetile(images[i], images[i + rows], images_urls[currentColumn*rows+rows-1][:-(len(str(fileextension))+len(str(rows+1)))] + str(currentRow) + fileextension)

	return (columns << 1) - 1

def createintermediatetile(firstimage, secondimage, savePath):
	
	try:
		region1 = firstimage.crop(halfbox1)
		region2 = secondimage.crop(halfbox2)

		newimage = Image.new('RGBA', size)

		newimage.paste(region1, (0,0))
		newimage.paste(region2, (128, 0))

		img_info = newimage.info
		
		newimage.save(savePath, **img_info)
 	except IOError:
 		print "bad: {0}".format(savePath)
 	except KeyError:
 		newimage.save(savePath + ".png", "PNG")


