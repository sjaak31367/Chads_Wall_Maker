#!/usr/bin/env python
# Written on 2018-10-24 and 2018-10-25 by sjaak31367 to make creating/editing texturemaps(?) for walls in Terraria easier, and (more) automated/automatable/faster. (Yes I am aware that this file is an ugly bodge, but it works okay?)
# Copyright: Feel free to use for personal/non-commercial/commercial/other uses, and or to copy/modify/change/redistribute/do with it as you please, as long as do not change the copyright of this file. Credit is not needed, but would be nice :)
# Warranty: I won't give any warranty for what you do or don't with script/software, I can tell you it _SHOULD_ work without shitting all over your floor, but if it does do that somehow 1) I shall not be held liable. 2) Please do tell me as I'd be interested to see how that managed to happen.
# Greetings and many time-savings wished upon you! ~Sjaak

from PIL import Image
import os



doNOToverwrite = True  # Set to `False` if you want to enable overwriting already existing image files in the "./outWalls" directory
startDir = os.getcwd().replace('\\', '/') + '/'  # Find where this file is located
inWalls = startDir + "inWalls/"  # Where are the input walls located?
outWalls = startDir + "outWalls/"  # Where to put the processed walls
minImageSize = (232, 88)  # Minimum Image size for it to be considered a wall
wallLocations = [(162,54,178,70), (180,54,196,70), (198,54,214,70)]  # Where are the "source" textures located in the image
wallPieces = ((0,0,1,2,0,0,0,1,2,0,0,0,0),
              (1,0,1,2,1,1,0,1,2,1,1,1,1),
              (2,0,1,2,2,2,0,1,2,2,2,2,2),
              (0,0,1,1,2,2,0,1,2),
              (0,0,1,1,2,2,0,1,2))  # What wall type to put where



# Check if input and output directories exist, and if not, make them
# Input
if os.path.exists(inWalls):
  if not os.path.isdir(inWalls):
    print "Input location isn't a directory, making one now..."
    os.mkdir(inWalls)
    exit(code = 1)
else:
  print "Input location doesn't exist, making one now..."
  os.mkdir(inWalls)
  exit(code = 1)
# Output
if os.path.exists(outWalls):
  if not os.path.isdir(outWalls):
    print "Input location isn't a directory, making one now..."
    os.mkdir(outWalls)
else:
  print "Input location doesn't exist, making one now..."
  os.mkdir(outWalls)



# Look for input walls
print "Input Directory:  " + inWalls
print "Output Directory: " + outWalls
print "Walls found in input directory:"
o = "   "
walls = []
for wall in os.listdir(inWalls):
  if wall.endswith(".png"):
    walls.append(wall)
    o += wall + ", "
print o[:-2] + "\n"
if len(walls) == 0:
  print "!  No walls/images found! Either add walls in \n   \"" + inWalls + "\"\n   Or check to make sure they are the correct size/format (and you have read access)!\nEXITING!"
  exit(code = 3)


# Wallify
globalPixelAccessObject = "PLACEHOLDER"
def cut(startX, startY, stopX, stopY):
  # Used to fill large rectangular areas with transparent pixels
  # This function has NO error handling! So if you pass an area smaller than 0,
  # or bigger than the image itself it will yell at you! (or loop forever)
  global globalPixelAccessObject
  distanceX = (stopX - startX) + 1
  distanceY = (stopY - startY) + 1
  for x in range(distanceX):
    for y in range(distanceY):
      globalPixelAccessObject[startX + x, startY + y] = (127, 127, 127, 0)

success = 0
overwrites = 0
notOverwrites = 0
for wall in walls:  # Iterate over found walls
  print "Wallifying wall:\t" + wall
  wallImage = Image.open(inWalls + wall, mode = 'r').convert("RGBA")  # Open image
  if not ((wallImage.height >= minImageSize[1]) & (wallImage.width >= minImageSize[0])):
    print "!  Wall \"" + wall + "\" is too small!"  # If too small, skip image
  else:
    wall_0 = wallImage.crop(wallLocations[0])  # Get different wall type "source" images
    wall_1 = wallImage.crop(wallLocations[1])
    wall_2 = wallImage.crop(wallLocations[2])
    for tileY in range(len(wallPieces)):
      for tileX in range(len(wallPieces[tileY])):
        wallType = wallPieces[tileY][tileX]  # Look what wall type goes where
        if wallType == 0:
          wallImage.paste(wall_0, (tileX*18, tileY*18))
        if wallType == 1:
          wallImage.paste(wall_1, (tileX*18, tileY*18))
        if wallType == 2:
          wallImage.paste(wall_2, (tileX*18, tileY*18))  # And put it there
    # Add transparent lines between walls
    wallPixels = wallImage.load()
    globalPixelAccessObject = wallPixels
    loopY = wallImage.height
    loopX = wallImage.width
    for y in range(loopY):  # Tile seperator lines
      for x in range(loopX):
        relativePosX = x % 18  # X/Y per tile
        relativePosY = y % 18
        if ((18 > relativePosY > 15) or (18 > relativePosX > 15)):
          wallPixels[x, y] = (127, 127, 127, 0)  # (R, G, B, A) (if you want another line colour, here is the place)
    # Removing of excess stuff / cutting off excess wall image parts
    cut(0, 12, 160, 21)
    cut(0, 30, 160, 39)
    cut(0, 66, 105, 75)
    cut(12, 0, 21, 87)
    cut(30, 0, 39, 51)
    cut(48, 0, 57, 87)
    cut(66, 0, 75, 51)
    cut(84, 54, 93, 87)
    cut(76, 48, 105, 51)

    cut(108, 22, 111, 57)
    cut(120, 22, 123, 57)
    cut(112, 48, 119, 57)
    cut(126, 22, 129, 57)
    cut(138, 22, 141, 57)
    cut(130, 48, 137, 57)
    cut(144, 22, 147, 57)
    cut(156, 22, 159, 57)
    cut(148, 48, 155, 57)

    cut(174, 0, 183, 51)
    cut(192, 4, 201, 47)
    cut(210, 0, 219, 51)
    cut(184, 0, 209, 3)
    cut(184, 12, 209, 21)
    cut(184, 30, 209, 39)
    cut(184, 48, 209, 51)

    cut(0, 0, 11, 3)
    cut(76, 0, 105, 3)
    cut(0, 48, 11, 51)
    cut(108, 72, 111, 87)
    cut(120, 72, 129, 87)
    cut(138, 72, 147, 87)

    cut(156, 72, 231, 87)
    cut(216, 54, 231, 69)
    # Saving
    if os.path.exists(outWalls + wall):
      if os.path.isfile(outWalls + wall):
        if doNOToverwrite:
          print "!  Error while saving, file already exists!"
          notOverwrites += 1
        else:
          wallImage.save(outWalls + wall, "PNG")
          success += 1
          overwrites += 1
      else:
        wallImage.save(outWalls + wall, "PNG")
        success += 1
    else:
      wallImage.save(outWalls + wall, "PNG")
      success += 1



# Final outputs / stats
print ""
print str(success) + " walls successfully converted and saved!"
if overwrites > 0:
  print str(overwrites) + " files overwritten! (if you do not want this, please see `doNOToverwrite`)"
if ((notOverwrites > 0) or (success == 0)):
  print str(notOverwrites) + " attempted overwrites, all blocked because of `doNOToverwrite = True` at the top of the file,"
  print "if you do wish to overwrite existing files in the output directory, please change this to False."
