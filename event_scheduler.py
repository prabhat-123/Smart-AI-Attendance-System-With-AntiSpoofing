from apscheduler.schedulers.background import BackgroundScheduler
import pymysql
from datetime import datetime
import smtplib

def getall_staffs():
    conn = pymysql.connect(host = "localhost", user = "root", password = "", database = "recognition")
    cur = conn.cursor()
    cur.execute("select eid,email_address from attendance")
    data = cur.fetchall()
    all_staffs = {}
    if len(data) != 0:
        for(id,email) in data:
            all_staffs[id] = email
    conn.close()
    return all_staffs

def registered_vs_absent_staffs(all_staffs):
    dt = datetime.now()
    dt = dt.strftime("%Y-%m-%d %I:%M:%S")
    date = str(dt).split(' ')[0]
    time = str(dt).split(' ')[1]
    time_hour = time.split(':')[0]
    time_minute = time.split(':')[1]
    start_hour = 1
    end_hour = 11
    # start_minute = 0
    # end_minute = 0
    conn = pymysql.connect(host = "localhost", user = "root", password = "", database = "recognition")
    cur = conn.cursor()
    cur.execute("select id,time from report where date=%s ",(date))
    output = cur.fetchall()
    if len(output)!= 0:
        registered_staff_ids = []
        for(x,y) in output:
            y_hour = y.split(":")[0]
            y_minute = y.split(":")[1]
            if(int(y_hour) >= start_hour and int(y_hour) <= end_hour):
                registered_staff_ids.append(int(x))
        absent_staff_ids = []
        all_staff_ids = list(all_staffs.keys())
        for x in all_staff_ids:
            if x not in registered_staff_ids:
                absent_staff_ids.append(x)
    else:
        absent_staff_ids = list(all_staffs.keys())
    conn.close()
    return absent_staff_ids

def absent_emails():
    all_staffs = getall_staffs()
    absent_staff_ids = registered_vs_absent_staffs(all_staffs)
    absent_staff_emails = []
    for item in absent_staff_ids:
        email = all_staffs[item]
        absent_staff_emails.append(email)
    return absent_staff_emails

def send_mail():
    all_staffs = getall_staffs()
    absent_staff_ids = registered_vs_absent_staffs(all_staffs)
    absent_staff_emails = absent_emails()
    dt = datetime.now()
    dt = dt.strftime("%Y-%m-%d %I:%M:%S")
    date = str(dt).split(' ')[0]
    time = str(dt).split(' ')[1]
    for id in absent_staff_ids:
        status = "Absent"
        conn = pymysql.connect(host = "localhost", user = "root", password = "", database = "recognition")
        cur1 = conn.cursor()
        cur1.execute("select fname from attendance where eid=%s ",id)
        output = cur1.fetchone()
        (name,) = output
        cur2 = conn.cursor()
        cur2.execute("insert into report(id,name,date,time,status) VALUES (%s,%s,%s,%s,%s)", (id,
                                                                                              name,
                                                                                              date,
                                                                                              time,
                                                                                              status))
        conn.commit()
        conn.close()
        print("Attendance for absent staffs has been recorded successfully")
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('srv.ale52@gmail.com','prabhat9811956469')
    for email in absent_staff_emails:
        server.sendmail('srv.ale52@gmail.com',
                    email,
                    'You are absent')
    print("Email sent successfully")



sched = BackgroundScheduler(daemon=True)
sched.add_job(send_mail,'cron',day_of_week='mon-fri', hour=12, minute=16)
sched.start()

# sched.shutdown()