import cv2
import os
import numpy as np
from tensorflow.keras.models import load_model
import pickle


rootdir = os.getcwd()

class Extract_Embeddings():

	def __init__(self,model_path):
		self.model_path = model_path		
		self.dataset_dir = os.path.join(rootdir,'dataset')


	def load_model(self):
		model = load_model(self.model_path)
		return model

	def check_pretrained_file(self,embeddings_model):
		self.embeddings_model = embeddings_model
		data = pickle.loads(open(embeddings_model, "rb").read())
		names = np.array(data["names"])
		unique_names = np.unique(names).tolist()
		return [data,unique_names]

	def get_staff_details(self):
		details = os.listdir(self.dataset_dir)
		staff_details = {}
		for item in details:
			name = item.split("_")[0]
			id = item.split("_")[1]
			staff_details[name] = id
		return staff_details

	def get_remaining_names(self,dictionaries,unique_names):
		self.dictionaries = dictionaries
		self.unique_names = unique_names
		remaining_names = np.setdiff1d(list(dictionaries.keys()),unique_names).tolist()
		return remaining_names

	def get_all_face_pixels(self,dictionaries):
		image_ids = []
		image_paths = []
		image_arrays = []
		names = []
		face_ids = []
		for category in list(dictionaries.keys()):
			path = os.path.join(self.dataset_dir,category + "_" + dictionaries[category])
			for img in os.listdir(path):
				img_array = cv2.imread(os.path.join(path,img))
				image_paths.append(os.path.join(path,img))
				image_ids.append(img)
				image_arrays.append(img_array)
				names.append(category)
				face_ids.append(dictionaries[category])
		return [image_ids,image_paths,image_arrays,names,face_ids]


	def get_remaining_face_pixels(self,dictionaries,remaining_names):
		self.dictionaries = dictionaries
		self.remaining_names = remaining_names
		image_ids = []
		image_paths = []
		image_arrays = []
		names = []
		face_ids = []
		if len(remaining_names) != 0:	
			for category in list(remaining_names):
				path = os.path.join(self.dataset_dir,category + "_" + dictionaries[category])
				for img in os.listdir(path):
					img_array = cv2.imread(os.path.join(path,img))
					image_paths.append(os.path.join(path,img))
					image_ids.append(img)
					image_arrays.append(img_array)
					names.append(category)
					face_ids.append(dictionaries[category])
			return [image_ids,image_paths,image_arrays,names,face_ids]
		else:
			return None

	def normalize_pixels(self,imagearrays):
		self.imagearrays = imagearrays
		face_pixels = np.array(self.imagearrays)
		# scale pixel values
		face_pixels = face_pixels.astype('float32')
		# standardize pixel values across channels (global)
		mean, std = face_pixels.mean(), face_pixels.std()
		face_pixels = (face_pixels - mean) / std
		return face_pixels






				
