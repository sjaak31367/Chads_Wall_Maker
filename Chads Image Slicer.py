#!/usr/bin/env python

from PIL import Image
import os
from math import ceil



doNOToverwrite = True
sectionSize = 16
spacerSize = 2
gridColour = (0,0,0,0)              # RGBA (transparent)
#gridColour = (0,0,0,255)           # RGBA (black)
#gridColour = (247, 119, 249, 255)  # RGBA (pink)
startDir = os.getcwd().replace('\\', '/') + '/'  # Find where this file is located
inImages = startDir + "inSlice/"                  # Where are the input images located?
outImages = startDir + "outSlice/"



# Check if input and output directories exist, and if not, make them
# Input
if os.path.exists(inImages):
  if not os.path.isdir(inImages):
    print("Input location isn't a directory, making one now...")
    os.mkdir(inImages)
    exit(code = 1)
else:
  print("Input location doesn't exist, making one now...")
  os.mkdir(inImages)
  exit(code = 1)
# Output
if os.path.exists(outImages):
  if not os.path.isdir(outImages):
    print("Input location isn't a directory, making one now...")
    os.mkdir(outImages)
else:
  print("Input location doesn't exist, making one now...")
  os.mkdir(outImages)

# Look for input images
print("Input Directory:  " + inImages)
print("Output Directory: " + outImages)
print("Walls found in input directory:")
o = "   "
images = []
for image in os.listdir(inImages):
  if image.endswith(".png"):
    images.append(image)
    o += image + ", "
print(o[:-2] + "\n")
if len(images) == 0:
  print("!  No input images found! Either add images in")
  print("   \"" + inImages + "\"")
  print("   Or check to make sure they are the correct size/format")
  print("   (and you have read access)!")
  print("EXITING!")
  exit(code = 3)

# Slice
# These are here so they can be accessed outside of the slicing functions
inImg = None
inPix = None
outImg = None
outPix = None
tmpImg = None

# Add seams
def slice(inFilepath, outFilepath):
  global inImg, inPix, outImg, outPix, tmpImg
  inImg = Image.open(inFilepath, 'r').convert("RGBA")
  inPix = inImg.load()
  width = ceil(inImg.width / (sectionSize))*(sectionSize+spacerSize)
  height = ceil(inImg.height / (sectionSize))*(sectionSize+spacerSize)
  outImg = Image.new("RGBA", (width, height), gridColour)

  for ySec in range(ceil(inImg.height / sectionSize)):
    for xSec in range(ceil(inImg.width / sectionSize)):
      tmpImg = inImg.crop((xSec*sectionSize, \
                           ySec*sectionSize, \
                           (xSec+1)*sectionSize, \
                           (ySec+1)*sectionSize))
      outImg.paste(tmpImg, (xSec*(sectionSize+spacerSize), \
                            ySec*(sectionSize+spacerSize)))

  outImg.save(outFilepath)

# Stitch away the seams
def unslice(inFilepath, outFilepath):
  global inImg, inPix, outImg, outPix, tmpImg
  # Load input image, and create output image
  inImg = Image.open(inFilepath, 'r').convert("RGBA")
  inPix = inImg.load()
  width = ceil(inImg.width / (sectionSize+spacerSize))*sectionSize
  height = ceil(inImg.height / (sectionSize+spacerSize))*sectionSize
  outImg = Image.new("RGBA", (width, height), gridColour)
  outPix = outImg.load()

  # get a crop of every little tile, and copy-paste the from input to output image
  for ySec in range(ceil(inImg.height / (sectionSize+spacerSize))):
    for xSec in range(ceil(inImg.width / (sectionSize+spacerSize))):
      tmpImg = inImg.crop((xSec*(sectionSize+spacerSize), \
                           ySec*(sectionSize+spacerSize), \
                           (xSec+1)*(sectionSize+spacerSize)-spacerSize, \
                           (ySec+1)*(sectionSize+spacerSize)-spacerSize))
      outImg.paste(tmpImg, (xSec*sectionSize, ySec*sectionSize))
  # Check there's no pixels left on the bottom of the input image that might still be in need of copying
  usefulPixelsOOB = 0
  for y in range(inImg.height-spacerSize, inImg.height):
    for x in range(inImg.width):
      if not (inPix[x,y] == gridColour or inPix[x,y] == (127,127,127,0) or inPix[x,y] == (0,0,0,0)):
        usefulPixelsOOB += 1
  if (usefulPixelsOOB != 0):
    print("!  Error, useful pixels out of bounds, Not Yet Implemented!")

  # Save output image
  outImg.save(outFilepath)

if __name__ == "__main__":
  for image in images:
    print(f"Slicing   \t" + image)
    outFilepathSlice = outImages + image.split(".")[0] + "_sliced." + image.split(".")[1]  # "example.png" -> "example_sliced.png"
    slice(inImages + image, outFilepathSlice)

    print(f"Stitching   \t" + image)
    outFilepathUnslice = outImages + image.split(".")[0] + "_stitched." + image.split(".")[1]  # "example.png" -> "example_stitched.png"
    unslice(inImages + image, outFilepathUnslice)
