import PhotoScan
import os

# Directory containing all photos
input_directory = './'

# Add a new chunk to the current document
chunk = PhotoScan.app.document.addChunk()

# Add all photos in input_directory to current chunk
photo_files = [file.path for file in os.scandir(input_directory) if file.path.endswith('.jpg')]
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
