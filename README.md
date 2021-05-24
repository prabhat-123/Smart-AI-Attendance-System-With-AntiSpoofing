# Smart-AI-Attendance-System-With-AntiSpoofing

## HOW TO RUN THIS PROJECT

### 1.  Download the repository on your local computer.

https://github.com/prabhat-123/Attendance_System_Using_Face_Recognition.git


### 2. After downloading, you have to open Command prompt/Anaconda prompt/Visual studio terminal to run this project.


### 3. Before running any files, you have to set up  virtual environment in the directory where the project is located and 
install all the dependenices required for this project.


Creating virtual environment enable us to install the dependencies virtually for this project only without affecting the python dependencies on  your computer.


A virtual environment is a tool that helps to keep dependencies required by different projects separate by creating isolated python virtual environments for them.


For installing virtual environment on command prompt and visual studio terminal:


##### i) First of all you have to install virtual environment tool to create one.


 For installation:
   
   
### On Windows:
   
   
      python -m pip install --user virtualenv
      
##### Recommended
For installing virtual environment on Anaconda Prompt(Windows):


       conda install -c anaconda virtualenv
   
   
### On MacOS or Linux:
  
  
      py -m pip install --user virtualenv
     
     
##### ii) After installing virtual environment, you have to install all the dependencies required to run this project in your virtual environment. For doing so you have to follow the following steps:
  
  
  First of all, you have to change your working directory to the location of this repository in your computer by using the following command:
  
  
        cd /*location to the repository */
        e.g cd E:/Attendance_system_using_face_recognition/ (location to the repository in local computer)
  
  
 ##### iii) After changing the working directory to the current repository/project create a virtual environment by using the following commands:
 
 ### On Windows:
    For Visual Studio Code Users
     
     python -m venv venv 
     
     
   Here venv is the name of the environment you like to choose.
     
 
 #### Recommended
     On Anaconda Prompt (Windows)
     
     conda create -n "your virtual environment name" python=3.6 (The code is tested and implemented in 3.6 so install python 3.6)
     e.g.
     
     conda create -n facialrecognition python=3.6
     
     
     
 ### On Linux or Mac:
     python3 -m venv venv
    
     
##### iv) After creating a virtual environment in a working directory, you need to activate the virtual environment:

 ### On Windows:
   
    On Visual Studio Code:
 
       venv\Scripts\activate
       
 
 #### Recommended
   On Anaconda Prompt (Windows):
  
     conda activate "your virtual environment name"
   
     e.g 
   
     conda activate facialrecognition
   

#### v) Now you need to install all the requirements and dependencies for running this project.


  ###### Install the dependencies by seeing the install_requirements.txt file.
  
### Note: The project will not work if the version of python is different. And try installing all the dependencies by following the above instructions if it does not work.

#### vi) After installation change the working directory to models/retinaface by using the following command:
          
           cd models/retinaface
           
           Then run the following commands to execute each script in the following                  order:
           
           python box_utils.py
           
           python config.py
           
           python mobilev1.py
           
           python prior_box.py
           
           python py_cpu_nms.py
           
           python retinaface.py
           
           And finally run the face detection model by running:
           
           python detect.py
           
###### After running detect.py, the script will open the web camera and load the retinaface detector pretrained weights. The user is asked to input their name... Input your name and the script will capture your 100 images and store the images in dataset/name folder.

## The output will look like this:
[![Video](face_detector.gif)](https://www.youtube.com/watch?v=0AnN6nQ6QMg)
           

#### vii) Then again goto the main directory by using the command:
           
           cd .. 
           (two times)
           
 #### viii) Now after the face has been detected and the output has been stored in dataset/input_name folder now extract the embeddings for the face by running the following command:
 
              python extractEmbeddings.py
              
###### Note: This will take some time to extract the embeddings of your dataset..

#### ix) Train the model(after extracting embeddings) by running the following command:

              python trainModel.py
  
 #### x) After training the model, finally use the trained models to recognize the face (who you are?) by running the command:
 
              python recognize.py
              
              
#### Output Demo: 
[![Video](face_recognition_video.gif)](https://www.youtube.com/watch?v=RWLD1y1FTbw)
