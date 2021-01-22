# ############################################ Importing Tkinter modules and Libraries #####################################################################################

from tkinter import *
import cv2
import os
from tkinter.ttk import Combobox, Treeview, Scrollbar, Progressbar
from PIL import Image, ImageTk
import pymysql
import csv
from tkinter import messagebox , Message
import numpy as np
from os import listdir
from tkinter import simpledialog
import time
import random
import pandas as pd
from tkinter import filedialog
import gtts
from gtts import gTTS
from extract_embeddings import Extract_Embeddings
import pickle
from training import Training
import os
from datetime import datetime
from statistics import mode
from mark_attendance import Mark_Attendance
import sys


root_dir = os.getcwd()
try:
    embedding_obj = Extract_Embeddings(model_path = 'models/facenet_keras.h5')
    embedding_model = embedding_obj.load_model()
    staff_names = embedding_obj.get_staff_name()
    [image_ids,image_paths,image_arrays,names] = embedding_obj.get_face_pixels(categories=staff_names)
    face_pixels = embedding_obj.normalize_pixels(imagearrays = image_arrays) 
    graph_path = "models/deploy.prototxt.txt"
    weights_path = "models/res10_300x300_ssd_iter_140000.caffemodel"
    net = cv2.dnn.readNetFromCaffe(os.path.join(root_dir,graph_path),os.path.join(root_dir,weights_path))
except cv2.error as e:
    print("Error: Provide correct graph_path and weights_path.")
    sys.exit(1)
except Exception as e:
    print("{}".format(str(e)))
    sys.exit(1)
# ####################### Admin Login page #############



def manage_employee():
    try:
        conn = pymysql.connect(host = "localhost", user = "root", password = "", database = "recognition")
        cur = conn.cursor()
        first = Toplevel()
        first.iconbitmap("Photos/Bokehlicia-Captiva-System-users.ico")
        first.geometry("1350x700+0+0")
        bg_photo = PhotoImage(file = "Photos/background3.png", master = first)
        background_pic = Label(first, image = bg_photo)
        background_pic.pack()
        first.title("Manage Employee post")
        print("Hi Chhabi lal tamang")
        face = Label(first, text = "Management of Employee & post" , bg = "green" , fg = "yellow", padx = 15, pady = 15, font = ("Times New Roman", 20, "bold") ,borderwidth = 5, relief = RIDGE).place(x = 500, y = 10)
        main = Label(first, bg = "gray", borderwidth = 1).pack()
        #All Required variables for database
        eid_var = StringVar()
        post_var = StringVar()
        fname_var = StringVar()
        gender_var = StringVar()
        contact_var = StringVar()
        address_var = StringVar()
        DOJ_var = StringVar()
        search_by = StringVar()
        search_text = StringVar()

        #################################################### Functions of Employee Management form #########################



        ########################################## To Add the Employee
        def add_employee():
            conn = pymysql.connect(host = "localhost", user = "root", password = "", database = "recognition")
            cur = conn.cursor()
            if post_var.get() == "" or fname_var.get() == "" or gender_var.get() ==  "" or contact_var.get() == "" or address_var.get() == "" or DOJ_var.get() == "":
                messagebox.showerror("Error","All fields are Required", parent = first)
            else:
                cur.execute("insert into attendance VALUES (%s,%s,%s,%s,%s,%s,%s)", (eid_var.get(),
                                                                                            post_var.get(),
                                                                                            fname_var.get(),
                                                                                            gender_var.get(),
                                                                                            contact_var.get(),
                                                                                            address_var.get(),
                                                                                            DOJ_var.get()
                                                                                            ))
                conn.commit()

                display()
                clear()
                conn.close()

            ######################################################################## To Display the data of Employee

        def display():
            conn = pymysql.connect(host = "localhost", user = "root", password = "", database = "recognition")
            cur = conn.cursor()
            cur.execute("select * from attendance")
            data = cur.fetchall()
            if len(data)!= 0:
                table1.delete(*table1.get_children())
                for row in data:
                    table1.insert('', END, values = row)                                                                                                                                                                                                                                                                                                                                                                    
                conn.commit()
            conn.close()
            ########################################### To clear the data
        def clear():
            eid_var.set("")
            post_var.set("")
            fname_var.set("")
            gender_var.set("")
            contact_var.set("")
            address_var.set("")
            DOJ_var.set("")


    ####################### To display the selected items in text field area
        def focus_data(event):
            cursor = table1.focus()
            contents = table1.item(cursor)
            row = contents['values']
            eid_var.set(row[0])
            post_var.set(row[1])
            fname_var.set(row[2])
            gender_var.set(row[3])
            contact_var.set(row[4])
            address_var.set(row[5])
            DOJ_var.set(row[6])
    ############################## To update the data  
        def update():
            conn = pymysql.connect(host = "localhost", user = "root", password = "", database = "recognition")
            cur = conn.cursor()
            if post_var.get() == "" or fname_var.get() == "" or gender_var.get() ==  "" or contact_var.get() == "" or address_var.get() == "" or DOJ_var.get() == "":
                messagebox.showerror("Error","All fields are Required", parent = first)
            else:
                cur.execute("update attendance set post = %s, fname = %s, gender = %s, contact_no = %s, email_address = %s, date_of_join = %s where eid = %s", (                                                               
                                                                                post_var.get(),
                                                                                fname_var.get(),
                                                                                gender_var.get(),
                                                                                contact_var.get(),
                                                                                address_var.get(),
                                                                                DOJ_var.get(),
                                                                                eid_var.get()
                                                                                ))
                conn.commit()
                display()
                clear()
                conn.close()

    ###################### To delete the items
        def delete():
            conn = pymysql.connect(host = "localhost", user = "root", password = "", database = "recognition")
            cur = conn.cursor()
            if post_var.get() == "" or fname_var.get() == "" or gender_var.get() ==  "" or contact_var.get() == "" or address_var.get() == "" or DOJ_var.get() == "":
                messagebox.showerror("Error","All fields are Required", parent = first)
            else:
                cur.execute("delete  from attendance where eid = %s",eid_var.get())
                conn.commit()
                conn.close()
                display()
                clear()

        def search_data():
            conn = pymysql.connect(host = "localhost", user = "root", password = "", database = "recognition")
            cur = conn.cursor()
            cur.execute("select * from attendance where " + str(search_by.get()) + " like '%" + str(search_text.get()) + "%'")
            data = cur.fetchall()
            if len(data)!= 0:
                table1.delete(*table1.get_children())
                for row in data:
                    table1.insert('', END, values = row)
                conn.commit()
            conn.close()




        def show_data():
            display()


        def add_photo():
            Id = eid_var.get()
            name = fname_var.get()
            if (Id == "" or name == ""):
                messagebox.showerror("Error", "ID and Name are Required", parent = first)
            else:
                print("[INFO] loading model...")
                dataset_dir = os.path.join(root_dir,'dataset')
                input_directory = os.path.join(dataset_dir,name)
                if not os.path.exists(input_directory):
                    os.makedirs(input_directory, exist_ok = 'True')
                    count = 1
                    print("[INFO] starting video stream...")
                    video_capture = cv2.VideoCapture(0)
                    while count <= 25:
                        try:
                            # grab the frame from the threaded video stream and resize it
                            # to have a maximum width of 400 pixels
                            (ret,frame) = video_capture.read()
                            # grab the frame dimensions and convert it to a blob
                            (h,w) = frame.shape[:2]
                            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,(300, 300), (104.0, 177.0, 123.0))
                            # pass the blob through the network and obtain the detections and
                            # predictions
                            net.setInput(blob)
                            detections = net.forward()
                            # loop over the detections
                            for i in range(0, detections.shape[2]):
                                # extract the confidence (i.e., probability) associated with the
                                # prediction
                                confidence = detections[0, 0, i, 2]
                                # filter out weak detections by ensuring the `confidence` is
                                # greater than the minimum confidence
                                if confidence > 0.95:
                                    # compute the (x, y)-coordinates of the bounding box for the
                                    # object
                                    box = detections[0, 0, i, 3:7] * np.array([w,h,w,h])
                                    (startX, startY, endX, endY) = box.astype("int")
                                    # draw the bounding box of the face along with the associated
                                    # probability
                                    text = "{:.2f}%".format(confidence * 100)
                                    y = startY - 10 if startY - 10 > 10 else startY + 10
                                    face = frame[startY - 5:endY + 5,startX - 5 :endX + 5]
                                    resized_face = cv2.resize(face,(160,160))
                                    cv2.imwrite(os.path.join(input_directory,str(name) + str(count) + '.jpg'),resized_face)
                                    cv2.rectangle(frame, (startX,startY), (endX,endY),(0, 0, 255),2)
                                    cv2.putText(frame, text, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255),2)
                                    count += 1
                            # show the output frame
                            cv2.imshow("Frame",frame)
                            key = cv2.waitKey(1)
                            if key == ord('q'):
                                break
                        except Exception as e:
                            pass
                    video_capture.release()
                    cv2.destroyAllWindows()
                    messagebox.showinfo("Success", "All photos are collected", parent = first) 
                else:
                    if len(os.listdir(input_directory)) == 25:
                        messagebox.showwarning("Error","Photo already added for this user.. Click Update to update photo",parent = first)
                    else:
                        ques = messagebox.askyesnocancel("Notification","Directory already exists with incomplete samples. Do you want to delete the directory", parent = first)
                        if (ques == True):
                            os.rmdir(input_directory)
                            messagebox.showinfo("Success", "Directory Deleted..Now you can add the photo samples", parent = first) 
                                
    ################################################## Employee Management form ###############################
        f2 = Frame(first, bg = "gray",borderwidth = "3", relief = SUNKEN, height = 600, width = 420)
        titles = Label(f2, text = "Manage Employee" ,bg = "gray", font = ("Italic", 20, "bold")).place(x = 90, y = 30)
        id = Label(f2, text = "Employee ID", bg = "gray", font = ("italic",13, "bold")).place(x = 35, y = 100 )
        E1 = Entry(f2, width = 20, textvariable = eid_var,  font = ("italic",13, "bold") ).place(x = 180  , y = 100)
        post = Label(f2, text = "Post", bg = "gray",  font = ("italic",13, "bold")).place(x = 35, y = 150 )
        E2 = Entry(f2, width = 20, textvariable = post_var,  font = ("italic",13, "bold")).place(x =180, y = 150)
        name = Label(f2, text = "Full Name", bg = "gray", font = ("italic",13, "bold")).place(x =35, y = 200)
        E3 = Entry(f2, width = 20, textvariable = fname_var , font = ("italic",12, "bold")).place(x = 180, y = 200)
        gender = Label(f2, text = "Gender", bg = "gray", font = ("italic",12, "bold")).place(x = 35, y= 250)
        E7 = Combobox(f2, textvariable = gender_var , values = ["Male","Female","Others"], state = "readonly",  font = ("italic",11, "bold")).place(x = 180, y = 250)
        no = Label(f2, text = "Contact.No", bg = "gray", font = ("italic",12, "bold")  ).place(x = 35, y = 300)
        E4 = Entry(f2, width = 20, textvariable = contact_var , font = ("italic",12, "bold") ).place(x = 180, y = 300 ) 
        address = Label(f2, text = " Email Address", bg = "gray", font = ("italic",12, "bold")).place(x = 35, y = 350)
        E5 = Entry(f2, width = 20, textvariable = address_var , font = ("italic",12, "bold") ).place(x = 180, y = 350)
        date = Label(f2, text = "D.O.J(dd mm yyyy)", bg = "gray",font = ("italic",12, "bold")).place(x = 35, y = 400 )
        E6 = Entry(f2, textvariable = DOJ_var , font = ("italic",12, "bold")).place(x = 180, y = 400)
        f2.place(x = 10, y = 90)
        # b2 = Button(first, text = "Close", command = first.destroy ).place(x = 135, y = 600)
        f3 = Frame(first, bg = "white", height = 130, width = 402)
        btn1 = Button(f3, text = "Add", bg = "green", height = "1", width = "7",command = add_employee, font = ("Times new Roman", 14 , "bold")).place(x = 10, y = 10)
        btn2 = Button(f3, text = "Update", bg = "green", height = "1", width = "7", command = update, font = ("Times new Roman", 14 , "bold")).place(x = 105, y = 10)
        btn3 = Button(f3, text = "Delete", bg = "green",  height = "1", width = "7", command = delete,  font = ("Times new Roman", 14 , "bold")).place(x = 205, y = 10)
        btn4 = Button(f3, text = "Clear", bg = "green", height = "1", width = "7", command = clear, font = ("Times new Roman", 14 , "bold")).place(x = 305, y = 10)
        btn5 = Button(f3, text = "Add Photo Sample", bg = "yellow", height = "2", width = "34",command = add_photo, font = ("Times new Roman", 14 , "bold")).place(x = 10, y = 60)

        f3.place(x = 20, y = 550)
    ################################################################################### Large Frame
        f4 = Frame(first, height = 600, width = 900, bg = "gray", borderwidth = "3", relief = SUNKEN)
        f4.place(x = 440, y = 90)
        l1 = Label(first, text = "Search By:",font = ("times new roman", 18 ,"bold"),bg = "gray", fg = "white").place(x = 460, y = 100 )
        c1 = Combobox(first, textvariable = search_by, values = ["eid","fname","post"], state = "readonly", width = "25").place(x = 580, y = 109)
        E7 = Entry(first, textvariable = search_text, width = "25", font = ("times new Roman",10) ).place(x = 780, y = 109)
        btn7 = Button(first,  text = "Search ",  height = "1", width = "16", command = search_data, font = ("Times new Roman", 13 , "bold")).place(x = 960, y = 100 )
        btn8 = Button(first, text = "Show All",  height = "1", width = "16", command = show_data, font = ("Times new Roman", 13 , "bold")).place(x = 1150, y = 100)
    ################################################################################## Table frame
        f5 = Frame(f4, bg = "green", borderwidth = "2", relief = SUNKEN)
        f5.place(x = 20, y = 45, height = 550, width = 855 )
        scroll_x =Scrollbar(f5, orient = HORIZONTAL)
        scroll_y = Scrollbar(f5, orient = VERTICAL)
        table1 = Treeview(f5, columns = ("eid","post", "fname","gender","contact.no","address","DOJ"), xscrollcommand = scroll_x.set, yscrollcommand = scroll_y.set)
        scroll_x.pack(side = BOTTOM, fill = X )
        scroll_y.pack(side = RIGHT, fill = Y)
        scroll_x.config(command = table1.xview)
        scroll_y.config(command = table1.yview)
        table1.heading("eid", text ="Employee ID")
        table1.heading('post', text = "Post")
        table1.heading("fname", text= "Full Name")
        table1.heading("gender",text = "Gender")
        table1.heading("contact.no", text = "Contact_No")
        table1.heading("address", text = " Email Address")
        table1.heading("DOJ", text= "Date Of Join")
        table1['show'] = 'headings'
        table1.column("eid", width = 119)
        table1.column("post", width = 119)
        table1.column("fname", width = 119)
        table1.column("gender", width = 119)
        table1.column("contact.no", width = 119)
        table1.column("address", width = 119)
        table1.column("DOJ", width = 119)

        table1.pack(fill = BOTH, expand = 1)
        table1.bind("<ButtonRelease-1>", focus_data)
        display()
        first.mainloop()
    except pymysql.err.OperationalError as e:
        messagebox.showerror( "Error","Sql Connection Error... Open Xamp Control Panel and then start MySql Server ")
    except Exception as e:
        messagebox.showerror("Error","Close all the windows and restart your program")
def train(): 
    try:
        second = Toplevel()
        second.title("Train The System")
        second.geometry("1400x700+0+0")
        second.iconbitmap("Photos/Hopstarter-Soft-Scraps-User-Group.ico")
        img3= PhotoImage(file = "Photos/background2.png", master = second)
        backgrd = Label(second, image = img3)
        backgrd.pack()
        train_title = Label(second, text = "Train the System", font = ("times new roman", 20, "bold"), bg = "brown")
        train_title.place(x = 0,y = 0, relwidth = 1)
        img4 = PhotoImage(file = "Photos/samples.png")
        train_img2 = Label(second, image = img4)
        train_img2.place(x = 420, y =150)
        
        def progress():
            progress_bar.start(5)
            try:
                training_obj = Training(embedding_path='models/facenet_embeddings.pickle')
                [label,Embeddings,labels,names] = training_obj.load_embeddings_and_labels()
                recognizer = training_obj.create_svm_model(labels=labels,embeddings=Embeddings)
                f1 = open('models/recognizer.pickle', "wb")
                f1.write(pickle.dumps(recognizer))
                f1.close()
                
                messagebox.showinfo("Success", "Training Done Successfully.. New pickle file created to store Face Recognition Model", parent = attendance)
            except FileNotFoundError as e:
                second.after(1000,second.destroy)
                print(e)
                messagebox.showerror("Error","Pickle file for embeddings is missing. {} not found.First Extract Embeddings and then try again".format(str(e).split(':')[-1]))
            except ValueError as e:
                second.after(1000,second.destroy)
                messagebox.showerror("Error","You need atleast 2 classes to train a SVM classifier,but the dataset contains less than two class")
            except Exception as e:
                second.after(1000,second.destroy)
                messagebox.showerror("Error","{} not found.".format(e))
                
                

        progress_bar = Progressbar(second, orient = HORIZONTAL, length = 500, mode = 'indeterminate')
        progress_bar.place(x = 430, y = 520) 
        btn = Button(second, text = "Start Training", font = ("Times new roman", 20, "bold"), command = progress, bg = "green" )
        btn.place(x = 600, y = 450) 
        second.mainloop()
    except Exception as e:
        second.after(1000,second.destroy)
        messagebox.showerror("Error","{} not found.".format(e))

# str(e).split(':')[-1])
######################################### Function to recognize the face
def distance(emb1, emb2):
    return np.sqrt(np.square(emb1 - emb2))

def face_recognize():
    print("[INFO] starting video stream...")
    training_obj = Training(embedding_path='models/facenet_embeddings.pickle')
    [label,Embeddings,labels,names] = training_obj.load_embeddings_and_labels()
    vs = cv2.VideoCapture(0)
    predictions = []
    while len(predictions) <= 10:
        try:
            # grab the frame from the threaded video stream and resize it
            # to have a maximum width of 400 pixels
            (ret,frame) = vs.read()
            # grab the frame dimensions and convert it to a blob
            (h,w) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,(300, 300), (104.0, 177.0, 123.0))
            # pass the blob through the network and obtain the detections and
            # predictions
            net.setInput(blob)
            detections = net.forward()
            # loop over the detections
            for i in range(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with the
                # prediction
                confidence = detections[0, 0, i, 2]
                # filter out weak detections by ensuring the `confidence` is
                # greater than the minimum confidence
                if confidence > 0.95:
                    # compute the (x, y)-coordinates of the bounding box for the
                    # object
                    box = detections[0, 0, i, 3:7] * np.array([w,h,w,h])
                    (startX, startY, endX, endY) = box.astype("int")
                    # draw the bounding box of the face along with the associated
                    # probability
                    text = "{:.2f}%".format(confidence * 100)
                    y = startY - 10 if startY - 10 > 10 else startY + 10
                    face = frame[startY - 5:endY + 5,startX - 5 :endX + 5]
                    resized_face = cv2.resize(face,(160,160))
                    face_pixel = embedding_obj.normalize_pixels(imagearrays=resized_face)
                    sample = np.expand_dims(face_pixel,axis=0)
                    embedding = embedding_model.predict(sample)
                    new_embedding = embedding.reshape(1,-1)   
                    COLORS = np.random.randint(0, 255, size=(len(label.classes_), 3), dtype="uint8")
                    recognizer = pickle.loads(open('models/recognizer.pickle', "rb").read())
                    # perform classification to recognize the face
                    preds = recognizer.predict_proba(new_embedding)[0]
                    p = np.argmax(preds)
                    proba = preds[p]
                    name = label.classes_[p]
                    print(proba)
                    print(name)
                    result = np.where(names == name)
                    resultEmbeddings = Embeddings[result]
                    print(name)
                    print(proba)
                    dists = []
                    for emb in resultEmbeddings:
                        d = distance(emb,new_embedding)
                        dists.append(d)
                    distarray = np.array(dists)
                    min_dist = np.min(distarray)
                    max_dist = np.max(distarray)    
                    print(distarray)
                    print(min_dist)
                    print(max_dist)     
                    if proba >= 0.50:
                        if (min_dist < 0.75 and max_dist < 1.4) or (min_dist < 0.5) or (proba ==1 and min_dist <= 0.5):
                            # print("dist name ", name)
                            print("min dist :",min_dist)
                            print("max dist :",max_dist)
                            color = [int(c) for c in COLORS[p]]
                            cv2.rectangle(frame,(startX,startY),(endX,endY),color,2)
                            predictions.append(name)
                            text = "{}: {:.2f}".format(name,proba)
                            cv2.putText(frame,text,(startX,startY - 5),cv2.FONT_HERSHEY_SIMPLEX,0.5,color,2)
                        else:

                            name = "NONE"

                            color = (255,255,0)

                            cv2.rectangle(frame,(startX,startY),(endX,endY),color,2)

                            text = "{}".format(name)
                            cv2.putText(frame,text,(startX,startY - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5,color,2)

                    else:
                        name = "NONE"

                        color = (255,255,0)
                        
                        cv2.rectangle(frame,(startX,startY),(endX,endY),color,2)

                        text = "{}".format(name)
                        cv2.putText(frame,text,(startX,startY - 5),cv2.FONT_HERSHEY_SIMPLEX,0.5,color,2)
            cv2.imshow("Capture",frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        except Exception as e:
            pass       
    vs.release()
    cv2.destroyAllWindows()
    
    csv_name = 'Attendance_Details/attendance.csv'
    mark_attendance_obj = Mark_Attendance(csv_filename=csv_name)
    if not os.path.exists(os.path.join(root_dir,csv_name)):
        mark_attendance_obj.write_csv_header(date='Date',staff_name='Staff_Name',time='Time',status='Status')
    final_name = mode(predictions)
    dt = datetime.now()
    date = str(dt).split(' ')[0]
    time = str(dt).split(' ')[1]
    status = "Present"
    df = pd.read_csv(csv_name)
    if date in str(df['Date']) and final_name in str(df['Staff_Name']):
        messagebox.showwarning("Sorry {}.Your attendance has already been recorded".format(final_name))
    else:   
        attendance_record = [date,final_name,time,status]
        mark_attendance_obj.append_csv_rows(records=attendance_record)
        messagebox.showinfo("Hello {}.Your attendance has been recorded successfully".format(final_name))



######################################## To change the user data
######################## User Admin
    
def change():
    import change
    
######################################## To display the attendance register report 
def report():
   import report 

################################## Function to exit the attendance management form ####################################
def exit():
    
    ques = messagebox.askyesnocancel("Notification","Do you Really want to exit?", parent = attendance)
    if (ques == True):
        attendance.destroy()
    

#             ############################## Face Based Attendance Management Slider ##############################
def faceslider():
    global count, text

    if (count>= len(manage)):
        count = -1
        text = ''
        topic.config(text = text)
    else:
        text = text + manage[count]
        topic.config(text = text)
        count += 1
    topic.after(200, faceslider)





#             ############################### Slider Colors

colors = ['red','green','pink','gold2','blue','black','yellow','purple']
def faceslidercolor():
    fg = random.choice(colors)
    topic.config(fg = fg)
    topic.after(30,faceslidercolor)

#################################### Function to display the all Images
def photo_samples():
    global my_image
    attendance.photo_path = filedialog.askopenfilename(initialdir ='./dataset', title = "Select Photo", filetypes = (("jpg files", "*.jpg"), ("all files", "*.*")), master = attendance)
    my_label = Label(attendance, text = attendance.photo_path).pack()
    my_image = ImageTk.PhotoImage(Image.open(attendance.photo_path))
    my_image_label = Label(attendance, image = my_image).pack()


#################################### Function for the face alignment
def face_embedding():
    fe = Toplevel()
    fe.title("Extract Embeddings")
    fe.geometry("1400x700+0+0")
    fe.iconbitmap("Photos/Hopstarter-Soft-Scraps-User-Group.ico")
    img1= PhotoImage(file = "Photos/background1.png", master = fe)
    backgrd = Label(fe, image = img1)
    backgrd.pack()
    embed_title = Label(fe, text = "Extract And Save Embeddings", font = ("times new roman", 20, "bold"), bg = "brown")
    embed_title.place(x = 0,y = 0, relwidth = 1)
    img2 = PhotoImage(file = "Photos/facial_clusters.png")
    embed_img2 = Label(fe, image = img2)
    embed_img2.place(x = 420, y =150)
    
    def start_extracting_embedding(pixels):
        embeddings = []
        for (i,face_pixel) in enumerate(face_pixels):
            j = i+1
            percent.set(str(int((j/l)*100))+"%")
            text.set(str(j)+"/"+str(l)+"tasks completed")
            pgbar["value"] = j
            fe.update()
            sample = np.expand_dims(face_pixel,axis=0)
            embedding = embedding_model.predict(sample)
            new_embedding = embedding.reshape(-1)
            embeddings.append(new_embedding)
        data = {"paths":image_paths, "names":names, "imageIDs":image_ids,"embeddings":embeddings}
        f = open('models/facenet_embeddings.pickle' , "wb")
        f.write(pickle.dumps(data))
        f.close()
        fe.after(1000,fe.destroy)
        messagebox.showinfo("Success", "Embedding extracted successfully.. New pickle file created to store embeddings", parent = attendance)
    
    l = len(face_pixels)
    percent = StringVar()
    text = StringVar()  
    pgbar = Progressbar(fe,length=500,mode='determinate',maximum=l,value=0,orient=HORIZONTAL)
    pgbar.place(x=400,y = 450) 
    percentlabel = Label(fe,textvariable=percent,font=("Times new roman", 16, "bold"))
    percentlabel.place(x=475,y=475)
    textlabel = Label(fe,textvariable=text,font=("Times new roman", 16, "bold")) 
    textlabel.place(x=475,y=500)  
    btn = Button(fe,text="Start Extracting Embeddings",font = ("Times new roman", 20, "bold"),command=lambda: start_extracting_embedding(pixels=face_pixels),bg="green")
    btn.place(x = 450, y = 550)
    fe.mainloop()



    
########################################## Facial Based Attendance system page ########################

attendance = Tk()
attendance.title("Facial based Attendance system")
attendance.iconbitmap("Photos/Aha-Soft-Free-Large-Boss-Admin.ico")
attendance.geometry("1350x700+0+0")
bg_image = PhotoImage(file = "Photos/background2.png", master = attendance)
background_photo = Label(attendance, image = bg_image)
background_photo.pack()

topic = Label(attendance, text = 'Face Based Attendance Management System' , bg = "blue" , fg = "yellow", padx = 15, pady = 15, font = ("Times New Roman", 20, "bold") ,borderwidth = 5, relief = RIDGE)
topic.place (x = 0, y = 0,relwidth = 1)
# faceslider()
# faceslidercolor()

photo1 = PhotoImage(file = "Photos/management.png", master = attendance)
B1 = Button(attendance, image = photo1, text = "Employee Management",font = ("Times New Roman" , 15), fg = "green", height =230, width = 265, command = manage_employee, compound = BOTTOM )
B1.place(x = 20, y = 100)

photo2 = PhotoImage(file = "Photos/face_recognizer.png",  master = attendance)
B2 = Button(attendance, image = photo2 , text = "Face Rocognizer", font = ("Times new roman", 15), fg = "green", height = 230, width= 265, command = face_recognize, compound = BOTTOM )
B2.place(x = 20, y = 400)
photo3 = PhotoImage(file = "Photos/train.png",  master = attendance)
B3 =  Button(attendance , image = photo3 , text = "Train the Data" , font = ("Times new roman", 15), fg = "green" , height = 230, width= 265, command = train , compound = BOTTOM )
B3.place(x = 360, y = 100)
photo4 = PhotoImage(file = "Photos/exit1.png",  master = attendance )
B4 = Button(attendance, text="Exit",image = photo4, fg = "green",font = ("Times new Roman", 15), height = 230, width = 265 , command = exit, compound = BOTTOM)
B4.place(x =1040, y = 400)
photo5 = PhotoImage(file = "Photos/report.png" ,  master = attendance)
B5 = Button(attendance, text = "Attendance Report", fg = "green", font = ("Times new roman", 15), image = photo5, height = 230, width = 265, command = report, compound = BOTTOM)
B5.place(x = 360, y = 400)
photo6 = PhotoImage(file = "Photos/photosample.png",  master = attendance)
B6 = Button(attendance, text = "Photo Samples" ,fg = "green", font =("Times new roman",15), image = photo6, height = 230, width = 265, command = photo_samples, compound = BOTTOM )
B6.place(x = 700, y= 100) 
photo7 = PhotoImage(file = "Photos/passwordchange.png", master = attendance)
B7 = Button(attendance, text="Change Password" ,fg = "green",font =("Times new roman",15), image = photo7, height = 230, width = 265, command = change, compound = BOTTOM )
B7.place(x = 700, y = 400)
photo8 = PhotoImage(file = "Photos/embeddings.png", master = attendance)
B8 = Button(attendance, text = "Extract Embeddings", fg = "green", font = ("Times new Roman", 15), image = photo8, height = 230, width = 265,command= face_embedding, compound = BOTTOM)
B8.place(x = 1040, y =100)



attendance.mainloop()

            