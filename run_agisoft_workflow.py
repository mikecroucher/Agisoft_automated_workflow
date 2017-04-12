import PhotoScan
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_directory", help="Name of directory to process")
args = parser.parse_args()

# Directory containing all photos
input_directory = args.input_directory
print("Input directory={0}".format(input_directory))
doc = PhotoScan.app.document

# Add a new chunk to the current document
chunk = PhotoScan.app.document.addChunk()
doc.save(path = "project.psz", chunks = [chunk])

# Add all photos in input_directory to current chunk
photo_files = [file.path for file in os.scandir(input_directory) if (file.path.endswith('.JPG') or file.path.endswith('.jpg'))]
print("{0} photos found".format(len(photo_files)))
chunk.addPhotos(photo_files)

# Align cameras
chunk.matchPhotos(accuracy=PhotoScan.HighAccuracy, preselection=PhotoScan.GenericPreselection)
chunk.alignCameras()

# build dense point cloud
chunk.buildDenseCloud()

chunk.buildModel(surface=PhotoScan.Arbitrary, interpolation=PhotoScan.EnabledInterpolation)

# build textures
chunk.buildUV(mapping=PhotoScan.GenericMapping)
chunk.buildTexture(blending=PhotoScan.MosaicBlending, size=4096)
doc.save(path = "project.psz", chunks = [chunk])
