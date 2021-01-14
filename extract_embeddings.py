import cv2
import os
import numpy as np
from tensorflow.keras.models import load_model


rootdir = os.getcwd()

class Extract_Embeddings():

	def __init__(self,model_path):
		self.model_path = model_path		
		self.dataset_dir = os.path.join(rootdir,'dataset')


	def load_model(self):
		model = load_model(self.model_path)
		return model


	def get_staff_name(self):
		staff_names = os.listdir(self.dataset_dir)
		return staff_names


	def get_face_pixels(self,categories):
		self.categories = categories
		image_ids = []
		image_paths = []
		image_arrays = []
		names = []
		for category in categories:
			path = os.path.join(self.dataset_dir,category)
			for img in os.listdir(path):
				img_array = cv2.imread(os.path.join(path,img))
				image_paths.append(os.path.join(path,img))
				image_ids.append(img)
				image_arrays.append(img_array)
				names.append(category)
		return [image_ids,image_paths,image_arrays,names]


	def normalize_pixels(self,imagearrays):
		self.imagearrays = imagearrays
		face_pixels = np.array(self.imagearrays)
		# scale pixel values
		face_pixels = face_pixels.astype('float32')
		# standardize pixel values across channels (global)
		mean, std = face_pixels.mean(), face_pixels.std()
		face_pixels = (face_pixels - mean) / std
		return face_pixels






				
