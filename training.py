"""
Train ML Model to Classify / Identify the person using extracted face embeddings
"""
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC
import pickle
import numpy as np
from sklearn.calibration import CalibratedClassifierCV

class Training:
    def __init__(self,embedding_path):
        self.embedding_path = embedding_path
    

    def load_embeddings_and_labels(self):
        data = pickle.loads(open(self.embedding_path, "rb").read())
        # encoding labels by names
        label = LabelEncoder()
        ids = np.array(data["face_ids"])                       
        labels = label.fit_transform(ids)

        
        # getting names
        # getting embeddings
        Embeddings = np.array(data["embeddings"])

        return [label,labels,Embeddings,ids]

    def create_svm_model(self,labels,embeddings):
        self.labels = labels
        self.embeddings = embeddings
        model_svc = LinearSVC()
        recognizer = CalibratedClassifierCV(model_svc)   
        recognizer.fit(self.embeddings,self.labels)
        return recognizer


