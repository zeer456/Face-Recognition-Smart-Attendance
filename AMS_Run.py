import tkinter as tk
from tkinter import *
import cv2
import csv
import os
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time

#####Window is our Main frame of system
window = tk.Tk()
window.title("SMART ATTENDANCE SYSTEM")


window.geometry('1280x720')
photo=PhotoImage(file="C:\\Users\Hp\Desktop\\Attendace_management_system-master\\Time-Attendance.png")
l=Label(window,image=photo)
l.image=photo       #just keeping a reference
l.grid()
#window.configure(backgroung='snow')


####GUI for manually fill attendance

def manual_att():
    global bs
    bs = tk.Tk()
    bs.iconbitmap('ppl.ico')
    bs.title("Enter Module Code...")
    bs.geometry('580x320')
    bs.configure(background='light steel blue')

    def sub_err():

        def er_sc_delete():
            er.destroy()

        global er
        er = tk.Tk()
        er.geometry('300x100')
        er.iconbitmap('ppl.ico')
        er.title('Warning!!')
        er.configure(background='black')
        Label(er, text='Please enter your module code!!!', fg='red', bg='black', font=('times', 16, ' bold ')).pack()
        Button(er, text='OK', command=er_sc_delete, fg="yellow", bg="green", width=9, height=1, activebackground="blue",
               font=('times', 15, ' bold ')).place(x=90, y=50)

    def fill_attendance():
        ts = time.time()
        Date = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStamp.split(":")
        ####Creatting csv of attendance

        ##Create table for Attendance
        DB_date = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
        global mod
        mod = Mod_Write.get()
        Database_table = str(mod + "_" + Date)

        import pymysql.connections

        ###Connect to the database
        try:
            global cursor
            connection = pymysql.connect(host='localhost', user='root', password='root', db='manual_attendance')
            cursor = connection.cursor()
        except Exception as e:
            print(e)

        sql = "CREATE TABLE IF NOT EXISTs " + Database_table + """
                                                 (ID INT NOT NULL AUTO_INCREMENT,
                                                  ENROLLMENT varchar(100) NOT NULL,
                                                  NAME VARCHAR(50) NOT NULL,
                                                  DATE VARCHAR(20) NOT NULL,
                                                  TIME VARCHAR(20) NOT NULL,
                                                      PRIMARY KEY (ID)
                                                      );
                                                 """
        try:
            cursor.execute(sql)  ##for create a table
        except Exception as ex:
            print(ex)  #

        if mod == '':
            sub_err()
        else:
            bs.destroy()
            MA = tk.Tk()
            MA.iconbitmap('ppl.ico')
            MA.title("Manual attendance of " + str(mod))
            MA.geometry('880x470')
            MA.configure(background='light steel blue')

            def delete_sc_err1():
                scerr1.destroy()

            def err_sc1():
                global scerr1
                scerr1 = tk.Tk()
                scerr1.geometry('330x100')
                scerr1.iconbitmap('ppl.ico')
                scerr1.title('ERROR!!')
                scerr1.configure(background='black')
                Label(scerr1, text='Please enter NAME & ENROL!!!', fg='red', bg='black',
                      font=('times', 16, ' bold ')).pack()
                Button(scerr1, text='OK', command=delete_sc_err1, fg="yellow", bg="green", width=9, height=1,
                       activebackground="blue", font=('times', 15, ' bold ')).place(x=90, y=50)

            def Value(Letter, type):
                if type == '1':  # insert
                    if not Letter.isdigit():
                        return False
                return True

            Eroll = tk.Label(MA, text="Enrollment Number", width=15, height=2, fg="tomato", bg="light steel blue",
                           font=('times', 18, ' bold '))
            Eroll.place(x=30, y=100)

            Name = tk.Label(MA, text="Student Name", width=15, height=2, fg="tomato", bg="light steel blue",
                                font=('times', 18, ' bold '))
            Name.place(x=30, y=200)

            global Enroll_Write
            Enroll_Write = tk.Entry(MA, width=20, validate='key', bg="gainsboro", fg="indian red", font=('times', 23, ' bold '))
            Enroll_Write['validatecommand'] = (Enroll_Write.register(Value), '%P', '%d')
            Enroll_Write.place(x=290, y=105)

            def rmv_enroll():
                Enroll_Write.delete(first=0, last=22)

            Name_Write = tk.Entry(MA, width=20, bg="gainsboro", fg="indian red", font=('times', 23, ' bold '))
            Name_Write.place(x=290, y=205)

            def rmv_name_stu():
                Name_Write.delete(first=0, last=22)

            ####get important variable
            def DB_data():
                ENROLL = Enroll_Write.get()
                STU = Name_Write.get()
                if ENROLL == '':
                    scr2_error()
                elif STU == '':
                    scr2_error()
                else:
                    time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    Hour, Minute, Second = time.split(":")
                    Insert_data = "INSERT INTO " + Database_table + " (ID,ENROLLMENT,NAME,DATE,TIME) VALUES (0, %s, %s, %s,%s)"
                    VALUES = (str(ENROLL), str(STU), str(Date), str(time))
                    try:
                        cursor.execute(Insert_data, VALUES)
                        connection.commit()
                    except Exception as e:
                        print(e)
                    Enroll_Write.delete(first=0, last=22)
                    Name_Write.delete(first=0, last=22)

            def csv_doc():
                import csv
                cursor.execute("select * from " + Database_table + ";")
                doc_name = "Attendance\Manually Attendance/" + Database_table + '.csv'
                with open(doc_name, "w") as csv_file:
                    doc_input = csv.writer(csv_file)
                    doc_input.writerow([i[0] for i in cursor.description])  # write headers
                    doc_input.writerows(cursor)
                    Notice = "csv file made"
                    Inform.configure(text=Notice, bg="tan", fg="salmon", width=33, font=('times', 19, 'bold'))
                    Inform.place(x=180, y=380)
                import csv
                import tkinter
                slot = tkinter.Tk()
                slot.title("Attendance of " + mod)
                slot.configure(background='light slate gray')
                with open(doc_name, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(slot, width=13, height=1, fg="Salmon", font=('times', 13, ' bold '),
                                                  bg="light slate gray", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                slot.mainloop()

            Inform = tk.Label(MA, text="CSV File Made", bg="light steel blue", fg="brown", width=33,
                              height=2, font=('times', 19, 'bold'))

            c1r_txt_enroll = tk.Button(MA, text="Delete", command=rmv_enroll, fg="black", bg="rosy brown", width=10,
                                     height=1,
                                     activebackground="khaki", font=('times', 15, ' bold '))
            c1r_txt_enroll.place(x=690, y=100)

            c1r_txt_student = tk.Button(MA, text="Delete", command=rmv_name_stu, fg="black", bg="rosy brown", width=10,
                                      height=1,
                                      activebackground="khaki", font=('times', 15, ' bold '))
            c1r_txt_student.place(x=690, y=200)

            Data_Enter = tk.Button(MA, text="Data Save", command=DB_data, fg="black", bg="plum", width=20,
                                 height=2,
                                 activebackground="wheat", font=('times', 15, ' bold '))
            Data_Enter.place(x=170, y=400)

            Csv_cr = tk.Button(MA, text="Make CSV File", command=csv_doc, fg="black", bg="plum", width=20,
                                 height=2,
                                 activebackground="wheat", font=('times', 15, ' bold '))
            Csv_cr.place(x=570, y=400)

            def Att_File():
                import subprocess
                subprocess.Popen(
                    r'explorer /select,"C:\Users\Hp\Desktop\Attendace_management_system-master\Attendance\Manually Attendance\-------Check atttendance-------"')

            Att_File = tk.Button(MA, text="Attendance sheet", command=Att_File, fg="black", bg="light green", width=12, height=1,
                             activebackground="dark sea green", font=('times', 14, ' bold '))
            Att_File.place(x=730, y=510)

            MA.mainloop()

    MODULE = tk.Label(bs, text="Enter Subject", width=15, height=2, fg="tomato", bg="light steel blue", font=('times', 18, ' bold '))
    MODULE.place(x=30, y=100)

    global Mod_Write

    Mod_Write = tk.Entry(bs, width=20, bg="gainsboro", fg="indian red", font=('times', 23, ' bold '))
    Mod_Write.place(x=250, y=105)

    fill_manual_attendance = tk.Button(bs, text="Fill Attendance", command=fill_attendance, fg="black", bg="plum",
                                       width=20, height=2,
                                       activebackground="wheat", font=('times', 15, ' bold '))
    fill_manual_attendance.place(x=250, y=160)
    bs.mainloop()


##For clear textbox
def dlt():
    enro_tx.delete(first=0, last=22)


def dlt1():
    nm_tx.delete(first=0, last=22)


def scr1_des():
    scr1.destroy()


def scr1_error():
    global scr1
    scr1 = tk.Tk()
    scr1.geometry('300x100')
    scr1.iconbitmap('ppl.ico')
    scr1.title('ERROR!!')
    scr1.configure(background='black')
    Label(scr1, text='FILL ALL FIELDS!!!', fg='red', bg='black', font=('times', 16, ' bold ')).pack()
    Button(scr1, text='OK', command=scr1_des, fg="yellow", bg="green", width=9, height=1, activebackground="blue",
           font=('times', 15, ' bold ')).place(x=90, y=50)



##Error screen2
def scr2_des():
    scr2.destroy()


def scr2_error():
    global scr2
    scr2 = tk.Tk()
    scr2.geometry('300x100')
    scr2.iconbitmap('ppl.ico')
    scr2.title('ERROR!!')
    scr2.configure(background='black')
    Label(scr2, text='Enter Module Code!!!', fg='red', bg='black', font=('times', 16, ' bold ')).pack()
    Button(scr2, text='OK', command=scr1_des, fg="yellow", bg="green", width=9, height=1, activebackground="blue",
           font=('times', 15, ' bold ')).place(x=90, y=50)

##Error screen3
def scr3_des():
    scr3.destroy()


def scr3_error():
    global scr3
    scr3 = tk.Tk()
    scr3.geometry('300x100')
    scr3.iconbitmap('ppl.ico')
    scr3.title('ERROR!!')
    scr3.configure(background='black')
    Label(scr3, text='NOT STARTED!!!', fg='red', bg='black', font=('times', 16, ' bold ')).pack()


##Error screen4
def scr4_des():
    scr4.destroy()


def scr4_error():
    global scr4
    scr4 = tk.Tk()
    scr4.geometry('300x100')
    scr4.iconbitmap('ppl.ico')
    scr4.title('ERROR!!')
    scr4.configure(background='black')
    Label(scr4, text='TIME UP!!!', fg='red', bg='black', font=('times', 16, ' bold ')).pack()

##Error screen5
def scr5_des():
    scr5.destroy()


def scr5_error():
    global scr5
    scr5 = tk.Tk()
    scr5.geometry('300x100')
    scr5.iconbitmap('ppl.ico')
    scr5.title('ERROR!!')
    scr5.configure(background='black')
    Label(scr5, text='ENTER CORRECT MODULE CODE', fg='red', bg='black', font=('times', 16, ' bold ')).pack()

###For take images for datasets
def face_image():
    import errno
    enr = enro_tx.get()
    nme = nm_tx.get()
    if enr == '':
        scr1_error()
    elif nme == '':
        scr1_error()
    else:
        try:
            cam = cv2.VideoCapture(0)
            dect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            ENR = enro_tx.get()
            NME = nm_tx.get()
            TrainNum = 0
            while (True):
                ret, img = cam.read()
                grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                face = dect.detectMultiScale(grey, 1.3, 5)
                for (x, y, w, h) in face:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # incrementing sample number
                    TrainNum = TrainNum + 1
                    # saving the captured face in the dataset folder
                    cv2.imwrite("TrainingImage/ " + NME + "." + ENR + '.' + str(TrainNum) + ".jpg",
                                grey[y:y + h, x:x + w])
                    cv2.imshow('Frame', img)
                # wait for 100 miliseconds
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif TrainNum > 70:
                    break
            cam.release()
            cv2.destroyAllWindows()
            ##Create table for Attendance
            import time
            Tr = time.time()
            Date = datetime.datetime.fromtimestamp(Tr).strftime('%Y-%m-%d')
            Time = datetime.datetime.fromtimestamp(Tr).strftime('%H:%M:%S')
            DB_date = datetime.datetime.fromtimestamp(Tr).strftime('%Y_%m_%d')

            Database_table = str("Students")

            import pymysql.connections
            try:
                global cursor
                connection = pymysql.connect(host='localhost', user='root', password='root', db='students_registered')
                cursor = connection.cursor()
            except Exception as e:
                print(e)

            sql = "CREATE TABLE IF NOT EXISTs " + Database_table + """
                                                     (ID INT NOT NULL AUTO_INCREMENT,
                                                      ENROLLMENT varchar(100) NOT NULL,
                                                      NAME VARCHAR(50) NOT NULL,
                                                      DATE VARCHAR(20) NOT NULL,
                                                      TIME VARCHAR(20) NOT NULL,
                                                          PRIMARY KEY (ID)
                                                          );
                                                     """
            try:
                cursor.execute(sql)  ##for create a table
            except Exception as ex:
                print(ex)  #
            time = datetime.datetime.fromtimestamp(Tr).strftime('%H:%M:%S')
            Hour, Minute, Second = time.split(":")
            Insert_data = "INSERT INTO " + Database_table + " (ID,ENROLLMENT,NAME,DATE,TIME) VALUES (0, %s, %s, %s,%s)"
            VALUES = (str(ENR), str(NME), str(Date), str(time))
            try:
               cursor.execute(Insert_data, VALUES)
               connection.commit()
            except Exception as e:
               print(e)
            row = [ENR, NME, Date, Time]
            with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
                write = csv.writer(csvFile, delimiter=',')
                write.writerow(row)
                csvFile.close()
            save = "Data Saved For Training: " + ENR + " Name : " + NME
            INFORM.configure(text=save, bg="lavender", width=50, font=('times', 18, 'bold'))
            INFORM.place(x=250, y=400)
        except OSError as e:
            if e.errno == errno.EEXIST:
               e = 'Student Data already exists'
               INFORM.configure(text=e, bg="lavender", width=21)
               INFORM.place(x=450, y=400)


###for choose subject and fill attendance
import time
def select_module():
    def Fillattendances():
        ti = time.strftime("%H%M")
        start1 = "1450"
        end1 = "1745"
        start2 = "2345"
        end2 = "0130"
        sub = tex.get()
        vid = time.time()  ###For calculate seconds of video
        future = vid + 20
        if time.time() < future:
            if sub == '':
                scr2_error()
            elif sub == 'cst3511':
                if int(str(ti)) < int(start1):
                   scr3_error()
                elif int(str(ti)) > int(end1):
                    scr4_error()
                else:
                    reco = cv2.face.LBPHFaceRecognizer_create()  # cv2.createlbphfacerecognizer()
                    try:
                        reco.read("TrainingImageLabel\Trainner.yml")
                    except:
                        e = 'Model not found,Please train model'
                        notify.configure(text=e, bg=" light slate gray", fg="black", width=33, font=('times', 15, 'bold'))
                        notify.place(x=20, y=250)

                    HRCpath = "haarcascade_frontalface_default.xml"
                    FaceCsc = cv2.CascadeClassifier(HRCpath)
                    SD = pd.read_csv("StudentDetails\StudentDetails.csv")
                    cam = cv2.VideoCapture(0)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    column_names = ['Enrollment', 'Name', 'Date', 'Time']
                    atten = pd.DataFrame(columns=column_names)
                    while True:
                        ret, im = cam.read()
                        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                        faces = FaceCsc.detectMultiScale(gray, 1.2, 5)
                        for (x, y, w, h) in faces:
                            global DT

                            DT, conf = reco.predict(gray[y:y + h, x:x + w])
                            if (conf < 70):
                                print(conf)
                                global MOD
                                global E_N
                                global date
                                global TiSt
                                MOD = tex.get()
                                ts = time.time()
                                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                                TiSt = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                                E_N = SD.loc[SD['Enrollment'] == DT]['Name'].values
                                global fg
                                fg = str(DT) + "-" + E_N
                                Ne = '15624031' + str(DT)
                                atten.loc[len(atten)] = [DT, E_N, date, TiSt]
                                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                                cv2.putText(im, str(fg), (x + h, y), font, 1, (255, 255, 0,), 4)

                            else:
                                DT = 'Unknown'
                                fg = str(DT)
                                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                                cv2.putText(im, str(fg), (x + h, y), font, 1, (0, 25, 255), 4)
                        if time.time() > future:
                            break

                        atten = atten.drop_duplicates(['Enrollment'], keep='first')
                        cv2.imshow('Filling attedance..', im)
                        key = cv2.waitKey(30) & 0xff
                        if key == 27:
                            break

                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    TiSt = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    Hour, Minute, Second = TiSt.split(":")
                    fileName = "Attendance/" + MOD + "_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
                    atten = atten.drop_duplicates(['Enrollment'], keep='first')
                    print(atten)
                    atten.to_csv(fileName, index=False)

                    ##Create table for Attendance
                    DB_Date = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
                    Database_table = str(MOD + "_" + DB_Date)
                    import pymysql.connections

                    ###Connect to the database
                    try:
                        global cursor
                        connection = pymysql.connect(host='localhost', user='root', password='root',
                                                     db='auto_attendance')
                        cursor = connection.cursor()
                    except Exception as e:
                        print(e)

                    sql = "CREATE TABLE IF NOT EXISTS " + Database_table + """
                                                        (ID INT NOT NULL AUTO_INCREMENT,
                                                         ENROLLMENT varchar(100) NOT NULL,
                                                         NAME VARCHAR(50) NOT NULL,
                                                         DATE VARCHAR(20) NOT NULL,
                                                         TIME VARCHAR(20) NOT NULL,
                                                             PRIMARY KEY (ID)
                                                             );
                                                        """
                    ####Now enter attendance in Database
                    insert_data = "INSERT INTO " + Database_table + " (ID,ENROLLMENT,NAME,DATE,TIME) VALUES (0, %s, %s, %s,%s)"
                    VALUES = (str(DT), str(E_N), str(date), str(TiSt))
                    try:
                        cursor.execute(sql)  ##for create a table
                        cursor.execute(insert_data, VALUES)  ##For insert data into table
                        connection.commit()
                    except Exception as ex:
                        print(ex)  #

                    F = 'Filled Attendance'
                    notify.configure(text=F, bg="light steel blue", fg="brown", width=33, font=('times', 15, 'bold'))
                    notify.place(x=20, y=250)

                    cam.release()
                    cv2.destroyAllWindows()

                    import csv
                    import tkinter
                    slot = tkinter.Tk()
                    slot.title("Attendance of " + MOD)
                    slot.configure(background='light steel blue')
                    doc = '' + fileName
                    with open(doc, newline="") as file:
                        read = csv.reader(file)
                        r = 0

                        for col in read:
                            c = 0
                            for row in col:
                                # i've added some styling
                                label = tkinter.Label(slot, width=8, height=1, fg="salmon", font=('times', 15, 'bold'),
                                                      bg="light slate gray", text=row, relief=tkinter.RIDGE)
                                label.grid(row=r, column=c)
                                c += 1
                            r += 1
                    slot.mainloop()
                    print(atten)

            elif sub == 'cst3515':
                 if int(str(ti)) < int(start2):
                    scr3_error()
                 elif int(str(ti)) > int(end2):
                      scr4_error()
                 else:
                     reco = cv2.face.LBPHFaceRecognizer_create()  # cv2.createlbphfacerecognizer()
                     try:
                         reco.read("TrainingImageLabel\Trainner.yml")
                     except:
                         e = 'Model not found,Please train model'
                         notify.configure(text=e, bg=" light slate gray", fg="black", width=33,
                                          font=('times', 15, 'bold'))
                         notify.place(x=20, y=250)

                     HRCpath = "haarcascade_frontalface_default.xml"
                     FaceCsc = cv2.CascadeClassifier(HRCpath)
                     SD = pd.read_csv("StudentDetails\StudentDetails.csv")
                     cam = cv2.VideoCapture(0)
                     font = cv2.FONT_HERSHEY_SIMPLEX
                     column_names = ['Enrollment', 'Name', 'Date', 'Time']
                     atten = pd.DataFrame(columns=column_names)
                     while True:
                         ret, im = cam.read()
                         gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                         faces = FaceCsc.detectMultiScale(gray, 1.2, 5)
                         for (x, y, w, h) in faces:

                             DT, conf = reco.predict(gray[y:y + h, x:x + w])
                             if (conf < 70):
                                 print(conf)
                                 #global MOD
                                 #global E_N
                                 #global date
                                 #global TiSt
                                 MOD = tex.get()
                                 ts = time.time()
                                 date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                                 TiSt = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                                 E_N = SD.loc[SD['Enrollment'] == DT]['Name'].values
                                 #global fg
                                 fg = str(DT) + "-" + E_N
                                 Ne = '15624031' + str(DT)
                                 atten.loc[len(atten)] = [DT, E_N, date, TiSt]
                                 cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                                 cv2.putText(im, str(fg), (x + h, y), font, 1, (255, 255, 0,), 4)

                             else:
                                 DT = 'Unknown'
                                 fg = str(DT)
                                 cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                                 cv2.putText(im, str(fg), (x + h, y), font, 1, (0, 25, 255), 4)
                         if time.time() > future:
                             break

                         atten = atten.drop_duplicates(['Enrollment'], keep='first')
                         cv2.imshow('Filling attedance..', im)
                         key = cv2.waitKey(30) & 0xff
                         if key == 27:
                             break

                     ts = time.time()
                     date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                     TiSt = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                     Hour, Minute, Second = TiSt.split(":")
                     fileName = "Attendance/" + MOD + "_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
                     atten = atten.drop_duplicates(['Enrollment'], keep='first')
                     print(atten)
                     atten.to_csv(fileName, index=False)

                     ##Create table for Attendance
                     DB_Date = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
                     Database_table = str(MOD + "_" + DB_Date)
                     import pymysql.connections

                     ###Connect to the database
                     try:
                         #global cursor
                         connection = pymysql.connect(host='localhost', user='root', password='root',
                                                      db='auto_attendance')
                         cursor = connection.cursor()
                     except Exception as e:
                         print(e)

                     sql = "CREATE TABLE IF NOT EXISTS " + Database_table + """
                                                                            (ID INT NOT NULL AUTO_INCREMENT,
                                                                             ENROLLMENT varchar(100) NOT NULL,
                                                                             NAME VARCHAR(50) NOT NULL,
                                                                             DATE VARCHAR(20) NOT NULL,
                                                                             TIME VARCHAR(20) NOT NULL,
                                                                                 PRIMARY KEY (ID)
                                                                                 );
                                                                            """
                     ####Now enter attendance in Database
                     insert_data = "INSERT INTO " + Database_table + " (ID,ENROLLMENT,NAME,DATE,TIME) VALUES (0, %s, %s, %s,%s)"
                     VALUES = (str(DT), str(E_N), str(date), str(TiSt))
                     try:
                         cursor.execute(sql)  ##for create a table
                         cursor.execute(insert_data, VALUES)  ##For insert data into table
                         connection.commit()
                     except Exception as ex:
                         print(ex)  #

                     F = 'Filled Attendance'
                     notify.configure(text=F, bg="light steel blue", fg="brown", width=33, font=('times', 15, 'bold'))
                     notify.place(x=20, y=250)

                     cam.release()
                     cv2.destroyAllWindows()

                     import csv
                     import tkinter
                     slot = tkinter.Tk()
                     slot.title("Attendance of " + MOD)
                     slot.configure(background='light steel blue')
                     doc = '' + fileName
                     with open(doc, newline="") as file:
                         read = csv.reader(file)
                         r = 0

                         for col in read:
                             c = 0
                             for row in col:
                                 # i've added some styling
                                 label = tkinter.Label(slot, width=8, height=1, fg="salmon", font=('times', 15, 'bold'),
                                                       bg="light slate gray", text=row, relief=tkinter.RIDGE)
                                 label.grid(row=r, column=c)
                                 c += 1
                             r += 1
                     slot.mainloop()
                     print(atten)
            else:
                scr5_error()

    ###windo is frame for subject chooser
    Wio = tk.Tk()
    Wio.iconbitmap('ppl.ico')
    Wio.title("Enter Module Code")
    Wio.geometry('580x320')
    Wio.configure(background='light steel blue')
    notify= tk.Label(Wio, text="Filled Attendance", bg="light steel blue", fg="brown", width=33,
                        height=2, font=('times', 15, 'bold'))

    def AutoAtt():
        import subprocess
        subprocess.Popen(
            r'explorer /select,"C:\Users\Hp\Desktop\Attendace_management_system-master\Attendance\-------Check atttendance-------"')

    AutoAtt = tk.Button(Wio, text="Check Sheet", command=AutoAtt, fg="black", bg="light green", width=12, height=1,
                     activebackground="dark sea green", font=('times', 14, ' bold '))
    AutoAtt.place(x=430, y=255)

    mod = tk.Label(Wio, text="Enter Module", width=15, height=2, fg="tomato", bg="light steel blue",
                   font=('times', 15, ' bold '))
    mod.place(x=30, y=100)

    tex = tk.Entry(Wio, width=20, bg="gainsboro", fg="indian red", font=('times', 23, ' bold '))
    tex.place(x=250, y=105)

    give_att = tk.Button(Wio, text="Fill Attendance", fg="black", command=Fillattendances, bg="plum", width=20,
                       height=2,
                       activebackground="wheat", font=('times', 15, ' bold '))
    give_att.place(x=250, y=160)
    Wio.mainloop()


def Adm_pnl():
    wid = tk.Tk()
    wid.iconbitmap('ppl.ico')
    wid.title("LogIn")
    wid.geometry('880x420')
    wid.configure(background='light steel blue')

    def sign_in():
        username = user_write.get()
        password = pas_write.get()

        if username == 'zahabiya':
            if password == 'zahabiya12':
                wid.destroy()
                import csv
                import tkinter
                slot = tkinter.Tk()
                slot.title("Student Details")
                slot.configure(background='light steel blue')

                doc = 'StudentDetails/StudentDetails.csv'
                with open(doc, newline="") as file:
                    read = csv.reader(file)
                    r = 0

                    for col in read:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(slot, width=8, height=1, fg="salmon", font=('times', 15, ' bold '),
                                                  bg="light slate gray", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                slot.mainloop()
            else:
                valid = 'Incorrect ID or Password'
                In.configure(text=valid, bg="red", fg="black", width=38, font=('times', 19, 'bold'))
                In.place(x=120, y=350)

        else:
            valid = 'Incorrect ID or Password'
            In.configure(text=valid, bg="light steel blue", fg="brown", width=38, font=('times', 19, 'bold'))
            In.place(x=120, y=350)

    In = tk.Label(wid, text="Attendance filled Successfully", bg="light steel blue", fg="brown", width=40,
                  height=2, font=('times', 19, 'bold'))
    # Nt.place(x=120, y=350)

    user = tk.Label(wid, text="Enter username", width=15, height=2, fg="tomato", bg="light steel blue",
                  font=('times', 15, ' bold '))
    user.place(x=30, y=50)

    pas = tk.Label(wid, text="Enter password", width=15, height=2, fg="tomato", bg="light steel blue",
                  font=('times', 15, ' bold '))
    pas.place(x=30, y=150)

    def us():
        user_write.delete(first=0, last=22)

    user_write = tk.Entry(wid, width=20, bg="gainsboro", fg="indian red", font=('times', 23, ' bold '))
    user_write.place(x=290, y=55)

    def ps():
        pas_write.delete(first=0, last=22)

    pas_write = tk.Entry(wid, width=20, show="*", bg="gainsboro", fg="indian red", font=('times', 23, ' bold '))
    pas_write.place(x=290, y=155)

    dele = tk.Button(wid, text="Delete", command=us, fg="black", bg="rosy brown", width=10, height=1,
                   activebackground="khaki", font=('times', 15, ' bold '))
    dele.place(x=690, y=55)

    dele1 = tk.Button(wid, text="Delete", command=ps, fg="black", bg="rosy brown", width=10, height=1,
                   activebackground="khaki", font=('times', 15, ' bold '))
    dele1.place(x=690, y=155)

    Login = tk.Button(wid, text="LogIn", fg="black", bg="plum", width=20,
                      height=2,
                      activebackground="wheat", command=sign_in, font=('times', 15, ' bold '))
    Login.place(x=290, y=250)
    wid.mainloop()


###For train the model
def Image_train():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    global detec
    detec = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    try:
        global face, Id
        face, Id = getImagesAndLabels("TrainingImage")
    except Exception as e:
        Err = 'Make "TrainingImage" folder first and save Data'
        INFORM.configure(text=Err, bg="lavender", width=50, font=('times', 18, 'bold'))
        INFORM.place(x=350, y=400)

    recognizer.train(face, np.array(Id))
    try:
       recognizer.save("TrainingImageLabel\Trainner.yml")
    except Exception as e:
        Err1 = 'Make "TrainingImageLabel" folder first'
        INFORM.configure(text=Err1, bg="lavender", width=50, font=('times', 18, 'bold'))
        INFORM.place(x=350, y=400)

    inf = "Data Trained"  # +",".join(str(f) for f in Id)
    INFORM.configure(text=inf, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
    INFORM.place(x=250, y=400)


def getImagesAndLabels(path):
    Img_Path = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faceSamples = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imgPth in Img_Path:
        # loading the image and converting it to gray scale
        conimg = Image.open(imgPth).convert('L')
        # Now we are converting the PIL image into numpy array
        npimg = np.array(conimg, 'uint8')
        # getting the Id from the image

        Id = int(os.path.split(imgPth)[-1].split(".")[1])
        # extract the face from the training image sample
        face = detec.detectMultiScale(npimg)
        # If a face is the
        # re then append that in the list as well as Id of it
        for (x, y, w, h) in face:
            faceSamples.append(npimg[y:y + h, x:x + w])
            Ids.append(Id)
    return faceSamples, Ids


window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.iconbitmap('ppl.ico')


def exiting():
    from tkinter import messagebox
    if messagebox.askokcancel("Exit", "Do you want to exit?"):
        window.destroy()


window.protocol("WM_DELETE_WINDOW", exiting)

message = tk.Label(window, text="Face-Recognition-Based-Attendance-Management-System", bg="lavender", fg="black", width=45,
                   height=2, font=('times', 25, 'italic bold '))

message.place(x=200, y=20)

INFORM = tk.Label(window, text="All Correct", bg="lavender", fg="brown", width=15,
                        height=3, font=('times', 17, 'bold'))

enro = tk.Label(window, text="Enter Enrollment", width=20, height=2, fg="firebrick", bg="silver",
               font=('times', 18, ' bold '))
enro.place(x=200, y=200)


def Value(Letter, type):
    if type == '1':  # insert
        if not Letter.isdigit():
            return False
    return True


enro_tx = tk.Entry(window, validate="key", width=20, bg="light gray", fg="crimson", font=('times', 25, ' bold '))
enro_tx['validatecommand'] = (enro_tx.register(Value), '%P', '%d')
enro_tx.place(x=550, y=210)

nm = tk.Label(window, text="Enter Name", width=20, fg="firebrick", bg="silver", height=2, font=('times', 18, ' bold '))
nm.place(x=200, y=300)

nm_tx = tk.Entry(window, width=20, bg="light gray", fg="crimson", font=('times', 25, ' bold '))
nm_tx.place(x=550, y=310)

Dlt_bt = tk.Button(window, text="Clear", command=dlt, fg="black", bg="pale violet red", width=10, height=1,
                        activebackground="medium violet red", font=('times', 15, ' bold '))
Dlt_bt.place(x=950, y=210)

Dly_bt1 = tk.Button(window, text="Clear", command=dlt1, fg="black", bg="pale violet red", width=10, height=1,
                         activebackground="medium violet red", font=('times', 15, ' bold '))
Dly_bt1.place(x=950, y=310)

Ad_Pl = tk.Button(window, text="Student Register", command=Adm_pnl, fg="black", bg="rosy brown", width=19, height=1,
               activebackground="tan", font=('times', 15, ' bold '))
Ad_Pl.place(x=990, y=510)

Img_Take = tk.Button(window, text="Take Face Images", command=face_image, fg="white", bg="light sea green", width=20, height=3,
                    activebackground="teal", font=('times', 15, ' bold '))
Img_Take.place(x=90, y=600)

Img_Train = tk.Button(window, text="Train Images", fg="black", command=Image_train, bg="medium sea green", width=20, height=3,
                     activebackground="sea green", font=('times', 15, ' bold '))
Img_Train.place(x=390, y=600)

SM = tk.Button(window, text="Automatic Attendace", fg="white", command=select_module, bg="light sea green", width=20, height=3,
               activebackground="teal", font=('times', 15, ' bold '))
SM.place(x=690, y=600)

MA = tk.Button(window, text="Manually Fill Attendance", command=manual_att, fg="black", bg="medium sea green",
                       width=20, height=3, activebackground="sea green", font=('times', 15, ' bold '))
MA.place(x=990, y=600)

window.mainloop()
