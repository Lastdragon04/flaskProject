import os
path=r'..\identify\face_img\id'
imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
print(len(imagePaths))