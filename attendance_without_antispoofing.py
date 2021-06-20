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
import webbrowser
import re
import shutil
from apscheduler.schedulers.background import BackgroundScheduler
import event_scheduler
import json
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import model_from_json
import tensorflow as tf
root_dir = os.getcwd()

try:
    embedding_obj = Extract_Embeddings(model_path = 'models/facenet_keras.h5')
    embedding_model = embedding_obj.load_model()
    face_cascade = cv2.CascadeClassifier("models/haarcascade_frontalface_default.xml")

    # Load Model
    json_file = open('antispoofing_models/finalyearproject_antispoofing_model_mobilenet.json','r')
    loaded_model_json = json_file.read()
    json_file.close()
    liveness_model = model_from_json(loaded_model_json)
    # load weights into new model
    liveness_model.load_weights('antispoofing_models/finalyearproject_antispoofing_model_74-0.986316.h5')
    print("Liveness Model loaded successfully from disk")

except cv2.error as e:
    print("Error: Provide correct path for face detection model.")
    sys.exit(1)
except Exception as e:
    print("{}".format(str(e)))
    sys.exit(1)
############################################ Admin Login page #############
face = Tk()
face.title("Admin Login Page")
face.geometry("1350x700+0+0")
face.iconbitmap("Photos/Aha-Soft-Free-Large-Boss-Admin.ico")
    ##  variables for login##
username_var = StringVar()
password_var = StringVar()
oldpass_var = StringVar()
user_var = StringVar()
newpass_var = StringVar()
def login():
    if username_var.get() == "" or password_var.get() == "":
        messagebox.showerror('Error','All the fields are required', parent = face)
    else:
        try:
            conn = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'recognition')
            curr = conn.cursor()
            curr.execute('select * from login where username = %s and password = %s',(username_var.get(), password_var.get()))
            row = curr.fetchone()
            if row == None:
                messagebox.showerror('Error','Invalid Data')

            else:
                face.destroy()
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
                        face = Label(first, text = "Management of Employee" , bg = "green" , fg = "yellow", padx = 15, pady = 15, font = ("Times New Roman", 20, "bold") ,borderwidth = 5, relief = RIDGE).place(x = 500, y = 10)
                        main = Label(first, bg = "gray", borderwidth = 1).pack()
                        def back():
                            first.destroy() 
                        backbtn = Button(first, text = 'Back', font = ('Times new Roman', 15), fg = 'black', bg = 'white', height = 1, width = 7, command = back).place(x = 1250, y = 10)  
                        #All Required variables for database
                        eid_var = StringVar()
                        post_var = StringVar()
                        fname_var = StringVar()
                        gender_var = StringVar()
                        contact_var = StringVar()
                        address_var = StringVar()
                        dt = datetime.now()
                        DOJ_var = str(dt).split(' ')[0]
                        search_by = StringVar()
                        search_text = StringVar()
                        search_from = StringVar()
                        search_result = StringVar()
                        mydata = []
                        dataset_dir = os.path.join(root_dir,'dataset')

                        #################################################### Functions of Employee Management form #########################
                        ########################################## To Add the Employee
                        def add_employee():
                            conn = pymysql.connect(host = "localhost", user = "root", password = "", database = "recognition")
                            
                            if post_var.get() == "" or fname_var.get() == "" or gender_var.get() ==  "" or contact_var.get() == "" or address_var.get() == "":
                                messagebox.showerror("Error","All fields are Required", parent = first)
                            else:
                                if (re.search('[a-zA-Z]+', fname_var.get())):
                                    if len(contact_var.get()) != 10:
                                        messagebox.showerror('Error', 'Contact Number must be 10 digits', parent = first)
                                    else:
                                        if (re.search('^[9]\d{9}$', contact_var.get())):
                                            regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
                                            if(re.search(regex, address_var.get())):
                                                name =fname_var.get()
                                                input_directory = os.path.join(dataset_dir,name)
                                                if not os.path.exists(input_directory):
                                                    os.makedirs(input_directory, exist_ok = 'True')
                                                    count = 1
                                                    print("[INFO] starting video stream...")
                                                    video_capture = cv2.VideoCapture(0)
                                                    while count <= 50:
                                                        try:
                                                            check, frame = video_capture.read()
                                                            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                                                            faces = face_cascade.detectMultiScale(gray,1.3,5)
                                                            for (x,y,w,h) in faces:  
                                                                face = frame[y-5:y+h+5,x-5:x+w+5]
                                                                resized_face = cv2.resize(face,(160,160))
                                                                cv2.imwrite(os.path.join(input_directory,name + str(count) + '.jpg'),resized_face)
                                                                cv2.rectangle(frame, (x,y), (x+w, y+h),(0,0,255), 2)
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
                                                    cur1 = conn.cursor()
                                                    cur1.execute("insert into attendance(department,fname,gender,contact_no,email_address,date_of_join) VALUES (%s,%s,%s,%s,%s,%s)", (
                                                                                                                                                                                post_var.get(),
                                                                                                                                                                                fname_var.get(),
                                                                                                                                                                                gender_var.get(),
                                                                                                                                                                                contact_var.get(),
                                                                                                                                                                                address_var.get(),
                                                                                                                                                                                DOJ_var
                                                                                                                                                                                ))

                                                    conn.commit()
                                                    cur2 = conn.cursor()
                                                    cur2.execute("select eid from attendance where fname=%s ",(name))
                                                    output = cur2.fetchone()
                                                    (id,) = output
                                                    os.rename(os.path.join(dataset_dir,name),os.path.join(dataset_dir,name + "_" + str(id)))
                                                    display()
                                                    clear()
                                                    conn.close()
                                                    messagebox.showinfo("Success", "All photos are collected", parent = first) 
                                                else:
                                                    if len(os.listdir(input_directory)) == 50:
                                                        messagebox.showwarning("Error","Photo already added for this user.. Click Update to update photo",parent = first)
                                                    else:
                                                        ques = messagebox.askyesnocancel("Notification","Directory already exists with incomplete samples. Do you want to delete the directory", parent = first)
                                                        if (ques == True):
                                                            shutil.rmtree(input_directory)
                                                            messagebox.showinfo("Success", "Directory Deleted..Now you can add the photo samples", parent = first) 
                                            else:
                                                messagebox.showerror('Error','Please Enter the Valid Email Address', parent = first)
                                        else:
                                            messagebox.showerror('Error','Invalid Phone number', parent = first)
                                else:
                                    messagebox.showerror('Error', 'Full Name must be String Character', parent = first)
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


                    ####################### To display the selected items in text field area
                        def focus_data(event):
                            cursor = table1.focus()
                            contents = table1.item(cursor)
                            row = contents['values']
                            if(len(row) != 0):
                                eid_var.set(row[0])
                                post_var.set(row[1])
                                fname_var.set(row[2])
                                gender_var.set(row[3])
                                contact_var.set(row[4])
                                address_var.set(row[5])
                    ############################## To update the data  
                        def update():
                            conn = pymysql.connect(host = "localhost", user = "root", password = "", database = "recognition")
                            cur = conn.cursor()
                            if post_var.get() == "" or fname_var.get() == "" or gender_var.get() ==  "" or contact_var.get() == "" or address_var.get() == "":
                                messagebox.showerror("Error","All fields are Required", parent = first)
                            else:
                                if (re.search('[a-zA-Z]+', fname_var.get())):
                                    if len(contact_var.get()) != 10:
                                        messagebox.showerror('Error', 'Contact Number must be 10 digits', parent = first)
                                    else:
                                        if(re.search('^[9]\d{9}$', contact_var.get())):
                                            regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
                                            if(re.search(regex, address_var.get())):
                                                id = eid_var.get()
                                                name = fname_var.get()
                                                staff_names = os.listdir(dataset_dir)
                                                staff_ids = [x.split('_')[1] for x in staff_names]
                                                if id in staff_ids:
                                                    index = staff_ids.index(id)
                                                    staff_name = staff_names[index]
                                                    q = messagebox.askyesno("Notification","Do you want to update the photo samples too", parent = attendance)
                                                    if (q == True):
                                                        input_directory = os.path.join(dataset_dir,staff_name)
                                                        shutil.rmtree(input_directory) 
                                                        output_directory = os.path.join(dataset_dir,name + "_" + id)
                                                        os.mkdir(output_directory)
                                                        count = 1
                                                        print("[INFO] starting video stream...")
                                                        video_capture = cv2.VideoCapture(0)
                                                        while count <= 50:
                                                            try:
                                                                check, frame = video_capture.read()
                                                                gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                                                                faces = face_cascade.detectMultiScale(gray,1.3,5)
                                                                for (x,y,w,h) in faces:  
                                                                    face = frame[y-5:y+h+5,x-5:x+w+5]
                                                                    resized_face = cv2.resize(face,(160,160))
                                                                    cv2.imwrite(os.path.join(output_directory,name + str(count) + '.jpg'),resized_face)
                                                                    cv2.rectangle(frame, (x,y), (x+w, y+h),(0,0,255), 2)
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
                                                        cur.execute("update attendance set department = %s, fname = %s, gender = %s, contact_no = %s, email_address = %s where eid = %s", (                                                               
                                                                                                    post_var.get(),
                                                                                                    fname_var.get(),
                                                                                                    gender_var.get(),
                                                                                                    contact_var.get(),
                                                                                                    address_var.get(),
                                                                                                    eid_var.get()
                                                                                                    ))
                                                        conn.commit()
                                                        display()
                                                        clear()
                                                        conn.close()
                                                        messagebox.showinfo("Success", "Photos and database updated successfully", parent = first) 
                                                    
                                                    else:
                                                        os.rename(os.path.join(dataset_dir,staff_name),os.path.join(dataset_dir,name + "_" + id))
                                                        cur.execute("update attendance set department = %s, fname = %s, gender = %s, contact_no = %s, email_address = %s where eid = %s", (                                                               
                                                                                                                        post_var.get(),
                                                                                                                        fname_var.get(),
                                                                                                                        gender_var.get(),
                                                                                                                        contact_var.get(),
                                                                                                                        address_var.get(),
                                                                                                                        eid_var.get()
                                                                                                                        ))
                                                        conn.commit()
                                                        display()
                                                        clear()
                                                        conn.close() 
                                                        messagebox.showinfo("Success", "Database updated successfully", parent = first) 
                                                else:
                                                    ques = messagebox.askyesno("Notification","Photo samples for this staff didnot exist in local directory. Please delete the entry from the database", parent = attendance)
                                                    if (ques == True):
                                                        delete()
                                                        messagebox.showinfo("Success","Database Updated successfully")
                                                    else:
                                                        delete()
                                                        messagebox.showinfo("Success","Database Updated successfully")
                                            else:
                                                messagebox.showerror('Error','Please Enter the Valid Email Address', parent = first)
                                        else:
                                            messagebox.showerror('Error','Invalid Contact number', parent = first)
                                else:
                                    messagebox.showerror('Error', 'Full Name must be String Character', parent = first)
                                            
                                

                    ###################### To delete the items #########################
                        def delete():
                            conn = pymysql.connect(host = "localhost", user = "root", password = "", database = "recognition")
                            cur = conn.cursor()
                            if post_var.get() == "" or fname_var.get() == "" or gender_var.get() ==  "" or contact_var.get() == "" or address_var.get() == "":
                                messagebox.showerror("Error","All fields are Required", parent = first)
                            else:
                                try:
                                    input_name = fname_var.get() + "_" + eid_var.get()
                                    staff_input = os.path.join(dataset_dir,input_name)
                                    if not os.path.exists(staff_input):
                                        cur.execute("delete from attendance where eid = %s",eid_var.get())
                                    else:
                                        cur.execute("delete from attendance where eid = %s",eid_var.get())
                                        shutil.rmtree(staff_input)
                                    conn.commit()
                                    conn.close()
                                    display()
                                    clear()
                                except Exception as e:
                                    messagebox.showerror("Error",e)
                                

                        def search_data():
                            conn = pymysql.connect(host = "localhost", user = "root", password = "", database = "recognition")
                            cur = conn.cursor()
                            cur.execute("select * from attendance where " + str(search_from.get()) + " LIKE '%" + str(search_result.get()) + "%'")
                            data = cur.fetchall()
                            if len(data)!= 0:
                                table1.delete(*table1.get_children())
                                for row in data:
                                    table1.insert('', END, values = row)
                                conn.commit()
                            else:
                                messagebox.showinfo('Sorry', 'No Data Found', parent = first)
                            conn.close()

                        def show_data():
                            display()
                                                
                    ################################################## Employee Management form ###############################
                        f2 = Frame(first, bg = "gray",borderwidth = "3", relief = SUNKEN, height = 600, width = 420)
                        titles = Label(f2, text = "Manage Employee" ,bg = "gray", font = ("Italic", 20, "bold")).place(x = 90, y = 30)
                        id = Label(f2, text = "Employee ID", bg = "gray", font = ("italic",13, "bold")).place(x = 35, y = 100 )
                        E1 = Entry(f2,state="disabled", width = 20, textvariable = eid_var,  font = ("italic",13, "bold") ).place(x = 180  , y = 100)
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
                        # date = Label(f2, text = "D.O.J(dd mm yyyy)", bg = "gray",font = ("italic",12, "bold")).place(x = 35, y = 400 )
                        # E6 = Entry(f2, textvariable = DOJ_var , font = ("italic",12, "bold")).place(x = 180, y = 400)
                        f2.place(x = 10, y = 90)
                        # b2 = Button(first, text = "Close", command = first.destroy ).place(x = 135, y = 600)
                        f3 = Frame(first, bg = "white", height = 130, width = 402)
                        btn1 = Button(f3, text = "Add", bg = "green", height = "1", width = "7",command = add_employee, font = ("Times new Roman", 14 , "bold")).place(x = 10, y = 10)
                        btn2 = Button(f3, text = "Update", bg = "green", height = "1", width = "7", command = update, font = ("Times new Roman", 14 , "bold")).place(x = 105, y = 10)
                        btn3 = Button(f3, text = "Delete", bg = "green",  height = "1", width = "7", command = delete,  font = ("Times new Roman", 14 , "bold")).place(x = 205, y = 10)
                        btn4 = Button(f3, text = "Clear", bg = "green", height = "1", width = "7", command = clear, font = ("Times new Roman", 14 , "bold")).place(x = 305, y = 10)
                        # btn5 = Button(f3, text = "Add Photo Sample", bg = "yellow", height = "2", width = "34",command = add_photo, font = ("Times new Roman", 14 , "bold")).place(x = 10, y = 60)
                        f3.place(x = 20, y = 550)
                    ################################################################################### Large Frame
                        f4 = Frame(first, height = 600, width = 900, bg = "gray", borderwidth = "3", relief = SUNKEN)
                        f4.place(x = 440, y = 90)
                        l1 = Label(first, text = "Search By:",font = ("times new roman", 18 ,"bold"),bg = "gray", fg = "white").place(x = 460, y = 100 )
                        c1 = Combobox(first, textvariable = search_from, values = ["eid","fname","post"], state = "readonly", width = "25").place(x = 580, y = 109)
                        E7 = Entry(first, textvariable = search_result, width = "25", font = ("times new Roman",10) ).place(x = 780, y = 109)
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
                        print(e)
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
                        train_title = Label(second, text = "Train the System", fg = 'white', font = ("times new roman", 20, "bold"), bg = "brown")
                        train_title.place(x = 0,y = 0, relwidth = 1)
                        img4 = PhotoImage(file = "Photos/samples.png")
                        train_img2 = Label(second, image = img4)
                        train_img2.place(x = 420, y = 150)
                        def back():
                            second.destroy()   
                        backbtn = Button(second, text = 'Back', fg = 'black', bg = 'white', font = ('Times new roman', 15), height = 1, width = 7, command = back).place(x = 1260, y = 3)
                        
                        def progress():
                            progress_bar.start(5)
                            try:
                                training_obj = Training(embedding_path='models/embeddings.pickle')
                                [label,labels,Embeddings,ids] = training_obj.load_embeddings_and_labels()
                                recognizer = training_obj.create_svm_model(labels=labels,embeddings=Embeddings)
                                f1 = open('models/recognizer.pickle', "wb")
                                f1.write(pickle.dumps(recognizer))
                                f1.close()
                                messagebox.showinfo("Success", "Training Done Successfully.. New pickle file created to store Face Recognition Model", parent = attendance)
                                second.after(1000,second.destroy)
                            except FileNotFoundError as e:
                                second.after(1000,second.destroy)
                                messagebox.showerror("Error","Pickle file for embeddings is missing. {} not found.First Extract Embeddings and then try again".format(str(e).split(':')[-1]))
                            except ValueError as e:
                                second.after(1000,second.destroy)
                                messagebox.showerror("Error",e)
                            except Exception as e:
                                second.after(1000,second.destroy)
                                messagebox.showerror("Error","{} not found.".format(e))

                        progress_bar = Progressbar(second, orient = HORIZONTAL, length = 500, mode = 'determinate')
                        progress_bar.place(x = 430, y = 520) 
                        btn = Button(second, text = "Start Training", fg = 'white',font = ("Times new roman", 20, "bold"), command = progress, bg = "green" )
                        btn.place(x = 600, y = 450) 
                        second.mainloop()
                    except Exception as e:
                        second.after(1000,second.destroy)
                        messagebox.showerror("Error","{} not found.".format(e))

    ######################################### Function to recognize the face
                def distance(emb1, emb2):
                    return np.sqrt(np.square(emb1 - emb2))

                
                def getkey(val,dict):
                    for key, value in dict.items():
                        if val == value:
                            return key

                def face_recognize():
                    embeddings_model_file = os.path.join(root_dir,"models/embeddings.pickle")
                    recognizer_model_file = os.path.join(root_dir,"models/recognizer.pickle")
                    predictions = []
                    liveness_predictor = []
                    if os.path.exists(embeddings_model_file and recognizer_model_file): 
                        training_obj = Training(embedding_path='models/embeddings.pickle')
                        [label,labels,Embeddings,ids] = training_obj.load_embeddings_and_labels()
                        staff_details = embedding_obj.get_staff_details()
                        recognizer = pickle.loads(open('models/recognizer.pickle', "rb").read())
                        vs = cv2.VideoCapture(0)
                        print("[INFO] starting video stream...")
                        while len(predictions) <= 10:
                            try:
                                (ret,frame) = vs.read()
                                gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                                faces = face_cascade.detectMultiScale(gray,1.3,5)
                                for (x,y,w,h) in faces:  
                                    face = frame[y-5:y+h+5,x-5:x+w+5]
                                    resized_face = cv2.resize(face,(160,160))
                                    face_pixel = embedding_obj.normalize_pixels(imagearrays=resized_face)
                                    sample = np.expand_dims(face_pixel,axis=0)
                                    embedding = embedding_model.predict(sample)
                                    embedding = embedding.reshape(1,-1)   
                                    COLORS = np.random.randint(0, 255, size=(len(label.classes_), 3), dtype="uint8")
                                    # perform classification to recognize the face
                                    preds = recognizer.predict_proba(embedding)[0]
                                    p = np.argmax(preds)
                                    proba = preds[p]
                                    id = label.classes_[p]
                                    name = getkey(id,staff_details)
                                    if proba >= 0.6:
                                        color = [int(c) for c in COLORS[p]]
                                        cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
                                        text = "{} {}".format(name,id)
                                        cv2.putText(frame,text,(x,y - 5),cv2.FONT_HERSHEY_SIMPLEX,0.5,color,2)
                                        predictions.append(id)
                                    else:
                                        name = "NONE"
                                        id = "NONE"
                                        color = (255,255,0)
                                        text = "{} {}".format(name,id)
                                        cv2.putText(frame,text,(x,y - 5),cv2.FONT_HERSHEY_SIMPLEX,0.5,color,2)
                                        cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
                                cv2.imshow("Capture",frame)
                                key = cv2.waitKey(1)
                                if key == ord('q'):
                                    break
                            except Exception as e:
                                messagebox.showerror("Error",e)
                                break
                        vs.release()
                        cv2.destroyAllWindows()
                        final_id = mode(predictions)
                        final_name = getkey(final_id,staff_details)
                        print(final_name)
                        print(final_id)
                        dt = datetime.now()
                        dt = dt.strftime("%Y-%m-%d %I:%M:%S")
                        date = str(dt).split(' ')[0]
                        time = str(dt).split(' ')[1]
                        time_hour = time.split(':')[0]
                        time_minute = time.split(':')[1]
                        start_hour = 0
                        end_hour = 24
                        status = "Present"
                        cur1 = conn.cursor()
                        cur1.execute("select name,date from report where name = %s and date = %s",(final_name,date))
                        data = cur1.fetchall()
                        if len(data)!= 0:
                            messagebox.showwarning("Warning","Sorry {}.Your attendance has already been recorded".format(final_name))     
                        else:
                            if(int(time_hour) >= start_hour and int(time_hour) <= end_hour):
                                cur2 = conn.cursor()
                                cur2.execute("insert into report(id,name,date,time,status) VALUES (%s,%s,%s,%s,%s)", (final_id,
                                                                                                                    final_name,
                                                                                                                    date,
                                                                                                                    time,
                                                                                                                    status))

                                conn.commit()
                                messagebox.showinfo("Success","Hello {}.Your attendance has been recorded successfully".format(final_name))
                    else:
                        messagebox.showerror("Error","Model file not found. Embeddings.pickle file and Recognizer.pickle file must exist within models directory.")

                ############### Function to recognize the face
                    


                ######################################## To change the user data
                ######################## User Admin
                

                def change():
                    account = Toplevel()
                    account.geometry('500x450+200+200')
                    account.title('Admin Account')
                    account.iconbitmap('Photos/Aha-Soft-Free-Large-Boss-Admin.ico')
                    account.focus_force()
                    account.grab_set()
                    account_frame = Frame(account, bg = 'white', height = 480, width = 500)
                    account_frame.pack()
                
                    title = Label(account_frame, text = "Admin Account", font = ('times new roman', 20, 'bold') , fg = 'green', bd = 3, relief = SUNKEN)    
                    title.place(x = 3, y = 3, relwidth = 1)     
                    def back():
                        account.destroy()
                    oldpass_var = StringVar()
                    newuser_var = StringVar()
                    newpass_var = StringVar()
                    backbtn = Button(account, text = 'Back' , bg = "gray" , fg = "white",font = ("Times New Roman", 13, "bold") ,borderwidth = 1, relief = RIDGE, command = back).place(x = 445, y = 7)
                    logo_icon = PhotoImage(file = 'Photos/logo.png',master = account)
                    admin_logo = Label(account_frame, image= logo_icon, bg = 'white').place( y = 70, relwidth = 1)
                    pass_icon = PhotoImage(file = 'Photos/password.png', master = account)
                    pass_logo = Label(account_frame, image = pass_icon).place(x = 7, y = 200)
                    pass_label = Label(account_frame, text = 'Old Password', font = ('times new roman', 14, 'bold')).place(x = 55, y = 215)
                    pass_entry = Entry(account_frame, show  = '*', font = ('times new roman', 14, 'bold'), textvariable = oldpass_var).place(x = 210, y = 215)
                    user_icon = PhotoImage(file = 'Photos/user.png', master = account)
                    user_logo = Label(account_frame, image = user_icon).place(x = 7, y = 265)
                    user_label = Label(account_frame, text = 'New Username', font = ('times new roman', 14, 'bold')).place(x = 55, y = 275)
                    user_entry = Entry(account_frame, font = ('times new roman', 14, 'bold'), textvariable = newuser_var).place(x = 210, y = 275)
                    newpass_logo = Label(account_frame, image = pass_icon).place(x = 7, y = 325)
                    newpass_label = Label(account_frame, text = 'New Password', font = ('times new roman', 14, 'bold')).place(x = 55, y = 335)
                    newpass_entry = Entry(account_frame, show = '*', font = ('times new roman', 14, 'bold'), textvariable = newpass_var).place(x = 210, y = 325)


                    def user_change():

                        if oldpass_var.get() == "" or newuser_var.get() == "" or newpass_var.get() == "" :
                            messagebox.showerror('Error',' All fields are Required', parent = account)
                        else:
                            conn = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'recognition')
                            cur = conn.cursor()
                            cur.execute('select * from login where password = %s',(oldpass_var.get()))
                            row = cur.fetchone()
                            if row == None:

                                messagebox.showerror('Error', 'Invalid Old Password', parent = account)
                            else:
                                cur.execute('update login set password = %s , username = %s',(newpass_var.get(), newuser_var.get()))
                                conn.commit()
                                conn.close()
                                messagebox.showinfo('Success', 'Datas Reset Successfully', parent = account)
                                account.destroy()
                        
                    btn = Button(account_frame, text = 'Reset', font = ('times new roman', 14, 'bold'), width = 10 , bg = 'green', command = user_change, relief = GROOVE).place(x = 240, y = 380 )
                    account.mainloop()   
                    
                ######################################## To display the attendance register report 
                def report():
                    report = Toplevel()
                    report.geometry("1400x700+0+0")
                    report.title("Attendance Report")
                    report.iconbitmap("Photos/Aha-Soft-Large-Seo-SEO.ico")
                    report.config(bg = "green")
                    title = Frame(report, bg = "cyan", bd = "3", relief = SUNKEN )
                    title.pack(fill = BOTH)
                    title_label = Label(title, text = "Attendance Report", font = ("times new roman", 30, "bold"), fg = "white", bg = "maroon")
                    title_label.pack()
                    def back():
                        report.destroy()
                    backbtn = Button(title, text = 'Back' , bg = "blue" , fg = "white", font = ("Times New Roman", 20 ,"bold"), relief = RIDGE, command = back).place(x = 1250, y = 0)
                
                    ################### Functions of all buttons that are used in this report window #####################################################################################
                    ###################################################################### To fetch the data from the database and display it into the app table #############################
                
                    ############################## To update the data  ##########################################################


                    def update(rows):
                        global mydata
                        mydata = rows
                        report_table.delete(*report_table.get_children())
                        for i in rows:
                            report_table.insert('', 'end', values = i)

                    def clear():
                        return True


                    ##################################################### To show all the datas from the database #######################################################################
                    def show_data():
                        conn = pymysql.connect(host = "localhost", user = "root", password = "", database = "recognition")
                        cur = conn.cursor()
                        cur.execute("select * from report")
                        data = cur.fetchall()
                        if len(data)!= 0:
                            report_table.delete(*report_table.get_children())
                            for row in data:
                                report_table.insert('', END, values = row)                                                                                                                                                                                                                                                                                                                                                                    
                            conn.commit()
                        conn.close()

                    ############################################ To save the csv data into mysql database ################################################################


                    def delete_data():
                        conn = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'recognition')
                        cur = conn.cursor()
                        selected_item = report_table.selection()[0]
                        uid = report_table.item(selected_item)['values'][0]
                        print("UID is ",uid)
                        cur.execute('delete from report where id = %s',(uid))
                        conn.commit()
                        report_table.delete(selected_item)
                        messagebox.showinfo('Success', ' Data Deleted Successfully', parent = report) 
                        conn.close()
                    
                    
                    def search_data():
                        conn = pymysql.connect(host = "localhost", user = "root", password = "", database = "recognition")
                        cur = conn.cursor()
                    
                        cur.execute("select * from report where " + str(search_by.get()) + " LIKE '%" + str(search_text.get()) + "%'")
                        rows = cur.fetchall()
                        if len(rows)!= 0:
                            report_table.delete(*report_table.get_children())
                            for row in rows:
                                report_table.insert('', END, values = row)
                            conn.commit()
                        else:
                            messagebox.showinfo('Sorry', 'No Data Found', parent = report)
                        conn.close()

                
                    

                    search_by = StringVar()
                    search_text = StringVar()
                    ####################################### Textfill Frame 
                    text_fill = Frame(report, height = 620, width = 1350, bg= "yellow", borderwidth = "3", relief = SUNKEN)
                    text_fill.place(x = 10, y = 75)
                    search_label = Label(text_fill, text = "Search By:", font = ("times new roman", 15, "bold"), bg = "yellow")
                    search_label.place(x = 10, y = 13)
                    search_combo = Combobox(text_fill, textvariable = search_by, values = ['date', 'name'], state = 'readonly', font = ("times new roman", 15),width = 15)
                    search_combo.place(x = 110, y = 13)
                    search_entry = Entry(text_fill, textvariable = search_text,  font = ("times new roman", 15 ), width = 15)
                    search_entry.place(x = 330 , y = 13)
                    search_btn = Button(text_fill, text = "Search", font = ("times new roman", 15, "bold"), command = search_data, width = 15)
                    search_btn.place(x = 540, y = 10)
                    search_today = Button(text_fill, text = "Delete", font = ("times new roman", 15, "bold"), command = delete_data, width = 15)
                    search_today.place(x = 840, y = 10 )
                    show_btn = Button(text_fill,  height = "1", text = "Show All", font = ("times new roman", 15, "bold"), command = show_data, width = 15)
                    show_btn.place(x = 1144, y = 10)
                    ###################################### Table frame

                    table_frame = Frame(text_fill, borderwidth = "3", relief = GROOVE, bg = "white")
                    table_frame.place(x= 10, y= 55, height = 560, width = 1325)
                    scroll_x = Scrollbar(table_frame, orient = HORIZONTAL)
                    scroll_y = Scrollbar(table_frame, orient = VERTICAL)
                    report_table = Treeview(table_frame, columns = ("ID","Date", "Name", "Time", "Status"), xscrollcommand = scroll_x.set, yscrollcommand = scroll_y.set)
                    scroll_x.pack(side = BOTTOM, fill = X )
                    scroll_y.pack(side = RIGHT, fill = Y)
                    scroll_x.config( command = report_table.xview)
                    scroll_y.config( command = report_table.yview) 
                    report_table.heading('ID', text = "ID") 
                    report_table.heading('Date', text ="Date")
                    report_table.heading('Name', text = "Name")
                    report_table.heading("Time", text= "Time")
                    report_table.heading("Status", text = "Status")
                    report_table['show'] = 'headings'
                    report_table.column("ID",  width = 140)
                    report_table.column("Date", width = 140)
                    report_table.column("Name", width = 140)
                    report_table.column("Time", width = 140)
                    report_table.column('Status', width = 140)
                    report_table.pack(fill = BOTH, expand = 1)

                    show_data()
                    # save_data()  
                    report.mainloop()

                    

                ################################## Function to exit the attendance management form ####################################
                def exit(): 
                    ques = messagebox.askyesnocancel("Notification","Do you Really want to exit?", parent = attendance)
                    if (ques == True):
                        attendance.destroy()
                    

                

                #################################### Function to display the all Images ###########################################################
                def photo_samples():
                    global my_image
                    attendance.photo_paths = filedialog.askopenfilename(initialdir ='./dataset', title = "Select Photo", filetypes = (("jpg files", "*.jpg"), ("all files", "*.*")), master = attendance)
                    my_label = Label(attendance, text = attendance.photo_paths).pack()
                    my_image = ImageTk.PhotoImage(Image.open(attendance.photo_paths))
                    my_image_label = Label(attendance, image = my_image).pack()


                #################################### Function for the face Embedding ##############################################################
                def face_embedding():
                    fe = Toplevel()
                    fe.title("Extract Embeddings")
                    fe.geometry("1400x700+0+0")
                    fe.iconbitmap("Photos/Hopstarter-Soft-Scraps-User-Group.ico")
                    img1= PhotoImage(file = "Photos/background1.png", master = fe)
                    backgrd = Label(fe, image = img1)
                    backgrd.pack()
                    embed_title = Label(fe, text = "Extract And Save Embeddings",font = ("times new roman", 30, "bold"), bg = "brown")
                    embed_title.place(x = 0,y = 0, relwidth = 1)
                    img2 = PhotoImage(file = "Photos/samples.png")
                    embed_img2 = Label(fe, image = img2)
                    embed_img2.place(x = 420, y =150)
                    staff_details = embedding_obj.get_staff_details()
                    embeddings_model_file = os.path.join(root_dir,"models/embeddings.pickle")
                    if not os.path.exists(embeddings_model_file):
                        [image_ids,image_paths,image_arrays,names,face_ids] = embedding_obj.get_all_face_pixels(staff_details)
                        face_pixels = embedding_obj.normalize_pixels(imagearrays = image_arrays)
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
                                data = {"paths":image_paths, "names":names,"face_ids":face_ids, "imageIDs":image_ids,"embeddings":embeddings}
                            f = open('models/embeddings.pickle' , "wb")
                            f.write(pickle.dumps(data))
                            f.close()
                            fe.after(1000,fe.destroy)
                            messagebox.showinfo("Success", "Embedding extracted successfully.. New pickle file created to store embeddings", parent = attendance)
                        def back():
                            fe.destroy()
                        backbtn = Button(fe, text = 'Back', fg = 'White', bg = 'green', font = ('times new roman', 18 , 'bold'), command = back).place(x = 1250, y = 1)
                        l = len(face_pixels)
                        percent = StringVar()
                        text = StringVar()  
                        pgbar = Progressbar(fe,length=500,mode='determinate',maximum=l,value=0,orient=HORIZONTAL)
                        pgbar.place(x=400,y = 450) 
                        percentlabel = Label(fe,textvariable=percent,font=("Times new roman", 16, "bold"))
                        percentlabel.place(x=475,y=475)
                        textlabel = Label(fe,textvariable=text,font=("Times new roman", 16, "bold")) 
                        textlabel.place(x=475,y=500)  
                        btn = Button(fe,text="Start Extracting Embeddings",fg = 'white', font = ("Times new roman", 20, "bold"),command=lambda: start_extracting_embedding(pixels=face_pixels),bg="green")
                        btn.place(x = 450, y = 550)
                        fe.mainloop()

                    else:
                        [old_data,unique_names] = embedding_obj.check_pretrained_file(embeddings_model_file)
                        remaining_names = embedding_obj.get_remaining_names(staff_details,unique_names)
                        data = embedding_obj.get_remaining_face_pixels(staff_details,remaining_names)
                        if data != None:
                            [image_ids,image_paths,image_arrays,names,face_ids] = data
                            face_pixels = embedding_obj.normalize_pixels(imagearrays = image_arrays)
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
                                new_data = {"paths":image_paths, "names":names,"face_ids":face_ids, "imageIDs":image_ids,"embeddings":embeddings}
                                combined_data = {"paths":[],"names":[],"face_ids":[],"imageIDs":[],"embeddings":[]}
                                combined_data["paths"] = old_data["paths"] + new_data["paths"]
                                combined_data["names"] = old_data["names"] + new_data["names"]
                                combined_data["face_ids"] = old_data["face_ids"] + new_data["face_ids"]
                                combined_data["imageIDs"] = old_data["imageIDs"] + new_data["imageIDs"]
                                combined_data["embeddings"] = old_data["embeddings"] + new_data["embeddings"]

                                f = open('models/embeddings.pickle' , "wb")
                                f.write(pickle.dumps(combined_data))
                                f.close()
                                fe.after(1000,fe.destroy)
                                messagebox.showinfo("Success", "Embedding extracted successfully.. New pickle file created to store embeddings", parent = attendance)
                            def back():
                                fe.destroy()
                            backbtn = Button(fe, text = 'Back', fg = 'White', bg = 'green', font = ('times new roman', 18 , 'bold'), command = back).place(x = 1250, y = 1)
                            l = len(face_pixels)
                            percent = StringVar()
                            text = StringVar()  
                            pgbar = Progressbar(fe,length=500,mode='determinate',maximum=l,value=0,orient=HORIZONTAL)
                            pgbar.place(x=400,y = 450) 
                            percentlabel = Label(fe,textvariable=percent,font=("Times new roman", 16, "bold"))
                            percentlabel.place(x=475,y=475)
                            textlabel = Label(fe,textvariable=text,font=("Times new roman", 16, "bold")) 
                            textlabel.place(x=475,y=500)  
                            btn = Button(fe,text="Start Extracting Embeddings",fg = 'white', font = ("Times new roman", 20, "bold"),command=lambda: start_extracting_embedding(pixels=face_pixels),bg="green")
                            btn.place(x = 450, y = 550)
                            fe.mainloop()
                        else:
                            messagebox.showinfo("Warning","No new staffs found. Embeddings already existed for these staffs")
                            fe.after(1000,fe.destroy)
  
                ########################################## Facial Based Attendance system page ########################

                attendance = Tk()
                attendance.title("Facial based Attendance system")
                attendance.iconbitmap("Photos/Aha-Soft-Free-Large-Boss-Admin.ico")
                attendance.geometry("1350x700+0+0")
                bg_image = PhotoImage(file = "Photos/background2.png", master = attendance)
                background_photo = Label(attendance, image = bg_image)
                background_photo.pack()
                manage_text = 'Face Based Attendance Management System'
                ######################################## Face Based Attendance Management Slider ##############################
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
                ########################################## Slider Colors
                colors = ['red','green','pink','gold2','blue','black','yellow','purple']
                def faceslidercolor():
                    fg = random.choice(colors)
                    topic.config(fg = fg)
                    topic.after(30,faceslidercolor)
                manage = 'Smart Attendance Management System'
                topic = Label(attendance, text = manage , bg = "blue" , fg = "yellow", padx = 15, pady = 15, font = ("Times New Roman", 20, "bold") ,borderwidth = 5, relief = RIDGE)
                topic.place (x = 0, y = 0,relwidth = 1)
                # faceslider()
                # faceslidercolor()

                photo1 = PhotoImage(file = "Photos/management.png", master = attendance)
                B1 = Button(attendance, image = photo1, text = "Employee Management",font = ("Times New Roman" , 15), fg = "green", height =230, width = 265, command = manage_employee, compound = BOTTOM )
                B1.place(x = 20, y = 100)

                photo2 = PhotoImage(file = "Photos/face_recognizer.png",  master = attendance)
                B2 = Button(attendance, image = photo2 , text = "Face Recognizer", font = ("Times new roman", 15), fg = "green", height = 230, width= 265, command = face_recognize, compound = BOTTOM )
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
                B7 = Button(attendance, text="Admin Account" ,fg = "green",font =("Times new roman",15), image = photo7, height = 230, width = 265, command = change, compound = BOTTOM )
                B7.place(x = 700, y = 400)
                photo8 = PhotoImage(file = "Photos/embeddings.png", master = attendance)
                B8 = Button(attendance, text = "Extract Embeddings", fg = "green", font = ("Times new Roman", 15), image = photo8, height = 230, width = 265,command= face_embedding, compound = BOTTOM)
                B8.place(x = 1040, y =100)
                attendance.mainloop()
        except pymysql.err.OperationalError as e:
            messagebox.showerror( "Error","Sql Connection Error... Open Xamp Control Panel and then start MySql Server ")
        except Exception as e:
            print(e)
            messagebox.showerror("Error","Close all the windows and restart your program")
count = 0 
text = ""
                 
def tick():
    time_string = time.strftime("%H:%M:%S")
    date_string = time.strftime("%d:%m:%Y")
    # print(time_string , date_string)
    clock.config (text = "Time :" + time_string  + "\n" + "Date :" + date_string)
    clock.after(200,tick)

########################### Admin login page form ####################################
bg_icon = PhotoImage(file = "Photos/background.png", master = face)
background_image = Label(face, image = bg_icon)
background_image.pack()

title = Label(face, text = "Admin Login Page" , font = ("times new roman", 30, "bold"), bg = "green", fg = "yellow", bd = 7, relief = GROOVE) 
title.place(x = 0, y = 0, relwidth = 1)

clock = Label(face , font = ("times",20,"bold"), bg = "green", relief = GROOVE)
clock.place(x = 1000, y= 600)
tick()
login_frame= Frame(face, bg = "white" )
login_frame.place(x = 400, y = 200)
logo_icon = PhotoImage(file = "Photos/logo.png", master= login_frame)
logo_image = Label(login_frame, image = logo_icon, bd = 0 ).grid( row = 0, columnspan = 3 , pady = 40, padx= 40)
user_icon = PhotoImage(file = "Photos/user.png", master = login_frame)
password_icon = PhotoImage(file = "Photos/password.png", master = login_frame)
user_label = Label(login_frame , text = "Username", image = user_icon, bg= "white", compound = LEFT, font = ("times new roman", 15, "bold")).grid( row  = 1 , column = 0, padx = 30, pady = 5)
user_entry = Entry(login_frame, font = ("times new roman", 15, "bold"), relief = GROOVE, textvariable = username_var, bg = "lightgray").grid(row = 1, column= 1, padx= 10, pady = 5)
password_label = Label(login_frame, text = "Password", image = password_icon, bg ="white", compound = LEFT, font = ("times new roman", 15, "bold")).grid(row = 2, column = 0, padx = 30, pady = 5)
password_entry = Entry(login_frame, show = "*", font = ("times new roman", 15,"bold"), relief = GROOVE, textvariable = password_var, bg = "lightgray").grid(row = 2, column = 1, padx = 20, pady = 5)
submit_btn = Button(login_frame, text = "Log In",width = 10, activebackground = "blue", activeforeground = "white", command = login , font = ("times new roman", 20, "bold"),relief = GROOVE, bg = "green").grid(row = 3, column = 1, pady =25, padx = 25) 
face.mainloop()            