import sqlite3
from tkinter import *
from tkinter.ttk import Combobox
from datetime import datetime
import time
from tkinter import messagebox,filedialog
import random
import gmail
from tkinter.ttk import Style,Treeview,Scrollbar
from PIL import Image,ImageTk
import shutil
import os

try:
    con=sqlite3.connect(database='banking.sqlite')
    cur=con.cursor()
    cur.execute("create a table account(acn integer primary key autoincrement,name text,password text,email text,mob text,bal float,type text,opendate text)")
    cur.execute("create table txn_history(acn int,txn_amt float,txn_type text,txn_date text,update_bal float)")


    con.commit()
    print("tables created")
except:
    print("something went wrong, might be tables already exits")
con.close()




win=Tk()
win.state("zoomed")
win.resizable(width=False,height=True)
win.configure(bg='powder blue')
lbl_title=Label(win,text="Banking Automation",bg='powder blue',fg='blue',font=('arial',60,'bold','underline'))
lbl_title.pack()

lbl_date=Label(win,text=f"{datetime.now().date()}",bg='powder blue',font=('arial',15,'bold'))
lbl_date.place(relx=.9,rely=.1)

def main_screen():
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)
    
    def forgot_pass():
        frm.destroy()
        forgotpass_screen()
        
    def open_account():
        frm.destroy()
        openaccount_screen()

    def login_account():
        global name,acn                                              # global karne se hum direct kisi agle screen pe ja skte hai.
        acn=entry_acn.get()                                          #ye code kisi bhi tarah se kuch nhi likha jaye to screen pe ye problem ("Login","ACN/PASS cna't be empty") hogi.
        pwd=entry_pass.get()
        if(acn=="" or pwd==""):
            messagebox.showerror("Login","ACN/PASS cna't be empty")           #"Login","ACN/PASS cna't be empty" empty hone par
            return
        
        con=sqlite3.connect(database="banking.sqlite")
        cur=con.cursor()
        cur.execute("select name from account  where acn=? and password=?",(acn,pwd))
        row=cur.fetchone()
        con.close()
        if(row==None):
            messagebox.showerror("Login","Invalid ACN/PASS")                  #"Login","Invalid ACn/PASS" empty na hone par
        else:
            name=row[0]
            frm.destroy()
            loginaccount_screen()
        
    def reset():                                                              #ydi cursor ko starting point pe le jana hai to reset karna parta hai.to ye function help karta hai.
        entry_acn.delete(0,"end")
        entry_pass.delete(0,"end")
        entry_acn.focus()
    
    lbl_acn=Label(frm,text="A/C NO. :",bg='pink',font=('arial',20,'bold'))
    lbl_acn.place(relx=.3,rely=.1)
    
    entry_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    entry_acn.place(relx=.4,rely=.1)
    entry_acn.focus()
    
    lbl_pass=Label(frm,text="PASS     :",bg='pink',font=('arial',20,'bold'))
    lbl_pass.place(relx=.3,rely=.2)
    
    entry_pass=Entry(frm,font=('arial',20,'bold'),bd=5,show='*')
    entry_pass.place(relx=.4,rely=.2)
    
    btn_login=Button(frm,command=login_account,text='login',font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_login.place(relx=.41,rely=.3)
    
    btn_reset=Button(frm,command=reset,text='reset',font=('arial',20,'bold'),bd=5,bg='powderblue')                          #command=reset se sb clear ho jata hai.
    btn_reset.place(relx=.53,rely=.3)
    
    btn_open=Button(frm,command=open_account,text='open account',width=16,font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_open.place(relx=.41,rely=.44)
    
    btn_forgotpass=Button(frm,command=forgot_pass,text='forgot password',width=18,font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_forgotpass.place(relx=.40,rely=.58)
    
def forgotpass_screen():
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)
    
    def back():
        frm.destroy()
        main_screen()
        
    def otp_send():
        acn=entry_acn.get()
        email=entry_email.get()
        
        con=sqlite3.connect(database="banking.sqlite")     #for database insert. mysql=%s,and sqlite=?.
        cur=con.cursor()
        cur.execute("select email,password from account where acn=?",(acn,))
        row=cur.fetchone()
        if(row==None):                                     #ye karne se ydi a/c no. aur password wrong dalege to acn does not exist ho jayega.
            messagebox.showerror("Password Recovery","ACN does not exist")
        else:
            if(row[0]==email):
                otp=random.randint(1000,9999)
                print(otp)                                                #print karne se hume, jise hum otp bhej rhe hai wo print ho jayega
                try: 
                    con=gmail.GMail("kppappu666@gmail.com","")            #email ka use kar ke otp received karne ke liye
                    msg=gmail.Message(to=email,subject="OTP verification",text=f"You OTP is:{otp}")
                    con.send(msg)
                    messagebox.showingo("Password Recovery","OTP sent,check your email")  #ydi otp sahi hai to message me otp sent aayega.
                    
                except:
                    messagebox.showerror("Password Recovery","Somethig went wrong")       #ydi otp wrong hai to message me something went wrong aayega.
                
                lbl_otp=Label(frm,text="otp",bg='pink',font=('arial',20,'bold'))          #otp genrate karne ke liye otp ka label banane ke liye
                lbl_otp.place(relx=.4,rely=.45)
    
                entry_otp=Entry(frm,font=('arial',20,'bold'),bd=5)                        #otp likhne ke liye
                entry_otp.place(relx=.4,rely=.5)
                entry_otp.focus()
                
                def getpass():                                                            #otp genrate hoga aur hume message box me bataya jayega by message.
                    verify_otp=int(entry_otp.get())
                    if(otp==verify_otp):
                        messagebox.showinfo("Password Recovery","Your Pass:{row[1]}")
                    else:
                        messagebox.showerror("Password Recovery","Incorrect OTP")
                
                btn_verify=Button(frm,command=getpass,text='verify',font=('arial',20,'bold'),bd=5,bg='powderblue')  #send otp karne ke bad otp ko put kar ke verify kare.(getpass)
                btn_verify.place(relx=.54,rely=.6)
                
            else:                                          #ye karne se ydi a/c no. sahi diya aur password wrong dalege to Email is not correct ho jayega.
                messagebox.showerror("Password Recovery","Email is not correct")
        con.close()
        
    btn_back=Button(frm,command=back,text='Back',font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_back.place(relx=0,rely=0)
    
    lbl_frmtitle=Label(frm,text="This is Forgot Password Screen",bg='pink',font=('arial',20,'bold'))
    lbl_frmtitle.pack()
    
    lbl_acn=Label(frm,text="A/C NO. :",bg='pink',font=('arial',20,'bold'))     #text field
    lbl_acn.place(relx=.3,rely=.1)
    
    entry_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    entry_acn.place(relx=.4,rely=.1)
    entry_acn.focus()
    
    lbl_email=Label(frm,text="Email     :",bg='pink',font=('arial',20,'bold'))
    lbl_email.place(relx=.3,rely=.2)
    
    entry_email=Entry(frm,font=('arial',20,'bold'),bd=5)                                                 #
    entry_email.place(relx=.4,rely=.2)
    
    btn_otp=Button(frm,command=otp_send,text='otp send',font=('arial',20,'bold'),bd=5,bg='powderblue')   #Otp button banane ke liye.
    btn_otp.place(relx=.51,rely=.30)
    
    
def openaccount_screen():
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)
    
    def back():
        frm.destroy()
        main_screen()
    
    def open_acn():
        name=entry_name.get()                              #for data get
        pwd=entry_pass.get()
        email=entry_email.get()
        mob=entry_mob.get()
        acn_type=combo_type.get()
        opendate=time.ctime()
        bal=1000
        
        con=sqlite3.connect(database="banking.sqlite")     #for database insert. mysql=%s,and sqlite=?.
        cur=con.cursor()
        cur.execute("insert into account(name,password,email,mob,bal,type,opendate) values(?,?,?,?,?,?,?)",(name,pwd,email,mob,bal,acn_type,opendate))
        con.commit()
        con.close()
        
        con=sqlite3.connect(database="banking.sqlite")     #for maximum record jo ki accounts me aaya hoga, use hum ek lbl pe dikha rhe hai.
        cur=con.cursor()
        cur.execute("select max(acn) from account")
        row=cur.fetchone()
        
        lbl_acn_open=Label(frm,text=f"Account opened with ACN:{row[0]}",bg='pink',font=('arial',20,'bold'),fg='green')
        lbl_acn_open.place(relx=.4,rely=.75)
        con.close()
        
        entry_name.delete(0,"end")                         #reset karne ke liye hai ye. yadi koi dusra accout open karna chahte hai to uske liye phle hume reset karna padega.
        entry_mob.delete(0,"end")
        entry_pass.delete(0,"end")
        entry_email.delete(0,"end")
        entry_name.focus()                                 #focus function se hum cursor ko starting point pe la sakte hai.
        
        
    btn_back=Button(frm,command=back,text='Back',font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_back.place(relx=0,rely=0)
    
    lbl_frmtitle=Label(frm,text="This is Open Account Screen",bg='pink',font=('arial',20,'bold'))
    lbl_frmtitle.pack()
    
    lbl_name=Label(frm,text="Name:",bg='pink',font=('arial',20,'bold'))
    lbl_name.place(relx=.3,rely=.1)
    
    entry_name=Entry(frm,font=('arial',20,'bold'),bd=5)
    entry_name.place(relx=.4,rely=.1)
    entry_name.focus()
    
    lbl_pass=Label(frm,text="Password:",bg='pink',font=('arial',20,'bold'))
    lbl_pass.place(relx=.3,rely=.2)
    
    entry_pass=Entry(frm,font=('arial',20,'bold'),bd=5,show='*')
    entry_pass.place(relx=.4,rely=.2)
    
    lbl_email=Label(frm,text="Email:",bg='pink',font=('arial',20,'bold'))
    lbl_email.place(relx=.3,rely=.3)
    
    entry_email=Entry(frm,font=('arial',20,'bold'),bd=5)
    entry_email.place(relx=.4,rely=.3)
    
    lbl_mob=Label(frm,text="Mobile:",bg='pink',font=('arial',20,'bold'))
    lbl_mob.place(relx=.3,rely=.4)
    
    entry_mob=Entry(frm,font=('arial',20,'bold'),bd=5)
    entry_mob.place(relx=.4,rely=.4)
    
    lbl_type=Label(frm,text='Type:',bg='pink',font=('arial',20,'bold'))
    lbl_type.place(relx=.3,rely=.5)
    
    
    combo_type=Combobox(frm,font=('arial',20,'bold'),values=['Saving','Current'])
    combo_type.current(0)
    combo_type.place(relx=.40,rely=.5)
    
    btn_open=Button(frm,command=open_acn,text='open',font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_open.place(relx=.40,rely=.6)
    
    btn_reset=Button(frm,text='reset',font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_reset.place(relx=.55,rely=.6) 
    
def loginaccount_screen():
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)
    
    def logout():
        frm.destroy()
        main_screen()
    
    def details():
        ifrm=Frame(frm,highlightthickness=1,highlightbackground='brown')
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.1,relwidth=.5,relheight=.5)
        lbl_frmtitle.configure(text="This is Check Details Screen")
        
        con=sqlite3.connect(database="banking.sqlite")
        cur=con.cursor()
        cur.execute("select acn,bal,opendate,type from account  where acn=?",(acn,))
        row=cur.fetchone()
        con.close()
        
        Label(ifrm,text=f"Account No.\t{row[0]}",font=('',15),bg='white',fg='purple').place(relx=.3,rely=.1)   #is se hume check details me account holder ki basic details milegi.
        Label(ifrm,text=f"Account Bal\t{row[1]}",font=('',15),bg='white',fg='purple').place(relx=.3,rely=.2)
        Label(ifrm,text=f"Account Opendate\t{row[2]}",font=('',15),bg='white',fg='purple').place(relx=.3,rely=.3)
        Label(ifrm,text=f"Account Type\t{row[3]}",font=('',15),bg='white',fg='purple').place(relx=.3,rely=.4) 
        
    def update_profile():
        ifrm=Frame(frm,highlightthickness=1,highlightbackground='brown')
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.1,relwidth=.5,relheight=.5)
        lbl_frmtitle.configure(text="This is Update Profile Screen")
        def update_profile_afterlogin():
            name=entry_name.get()
            pwd=entry_pass.get()
            email=entry_email.get()
            mob=entry_mob.get()
        
            con=sqlite3.connect(database='banking.sqlite')
            cur=con.cursor()
            cur.execute("update account set name=?,password=?,email=?,mob=? where acn=?",(name,pwd,email,mob,acn))
            con.commit()
            con.close()
            
            messagebox.showinfo("Update Profile","Profile Updated")
            lbl_wel.configure(text=f"Welcome,{name}")              #on same time pe update ke time jb hum name change karte to ye karne par name update ho jata hai.                                            
                              
        lbl_name=Label(ifrm,text="Name",bg='white',font=('arial',12,'bold'))                      #ifrm me adding
        lbl_name.place(relx=.1,rely=.1)
        
        entry_name=Entry(ifrm,font=('arial',15,'bold'),bd=5)                                      #ifrm me adding
        entry_name.place(relx=.1,rely=.2)
        entry_name.focus()
        
        lbl_pass=Label(ifrm,text="Pass",bg='white',font=('arial',12,'bold'))                      #ifrm me adding
        lbl_pass.place(relx=.52,rely=.1)
        
        entry_pass=Entry(ifrm,font=('arial',15,'bold'),bd=5)                                      #ifrm me adding
        entry_pass.place(relx=.52,rely=.2)
        entry_pass.focus()
        
        lbl_email=Label(ifrm,text="Email",bg='white',font=('arial',12,'bold'))                      #ifrm me adding
        lbl_email.place(relx=.1,rely=.4)
        
        entry_email=Entry(ifrm,font=('arial',15,'bold'),bd=5)                                      #ifrm me adding
        entry_email.place(relx=.1,rely=.5)
        entry_email.focus()
        
        lbl_mob=Label(ifrm,text="Mob",bg='white',font=('arial',12,'bold'))                      #ifrm me adding
        lbl_mob.place(relx=.52,rely=.4)
        
        entry_mob=Entry(ifrm,font=('arial',15,'bold'),bd=5)                                      #ifrm me adding
        entry_mob.place(relx=.52,rely=.5)
        entry_mob.focus()
        
        btn_update=Button(frm,command=update_profile_afterlogin,text='Update',font=('arial',20,'bold'),bd=5,bg='powderblue')              #update_profile_afterlogin after login
        btn_update.place(relx=.44,rely=.45)
        
        con=sqlite3.connect(database='banking.sqlite')                                           #for update
        cur=con.cursor()
        cur.execute("select name,password,email,mob from account where acn=?",(acn,))
        row=cur.fetchone()
        con.close()
        
        entry_name.insert(0,row[0])                                                              #for update
        entry_pass.insert(0,row[1])                                                              #for update
        entry_email.insert(0,row[2])                                                             #for update
        entry_mob.insert(0,row[3])                                                               #for update
        
        
        
        
    def deposit():
        ifrm=Frame(frm,highlightthickness=1,highlightbackground='brown')
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.1,relwidth=.5,relheight=.5)
        lbl_frmtitle.configure(text="This is Deposit Screen")
        
        def deposit_acn():
            amt=float(entry_amt.get())
            con=sqlite3.connect(database="banking.sqlite")
            cur=con.cursor()
            cur.execute("select bal from account where acn=?",(acn,))
            bal=cur.fetchone()[0]
            cur.close()
            
            cur=con.cursor()
            cur.execute("update account set bal=bal+? where acn=?",(amt,acn))
            cur.execute("insert into txn_history values(?,?,?,?,?)",(acn,amt,"Cr",time.ctime(),bal+amt))
            con.commit()
            con.close()
        
            messagebox.showinfo("Deposit",f"Amount{amt} credited to ACN:{acn}")
        
        lbl_amt=Label(ifrm,text="Amount",bg='white',font=('arial',20,'bold')) 
        lbl_amt.place(relx=.1,rely=.1)
        
        entry_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        entry_amt.place(relx=.4,rely=.1)
        entry_amt.focus()
        
        
        btn_dept=Button(frm,command=deposit_acn,text='deposit',font=('arial',20,'bold'),bd=5,bg='powderblue')
        btn_dept.place(relx=.5,rely=.25)

        
        
    def withdraw():
        ifrm=Frame(frm,highlightthickness=1,highlightbackground='brown')
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.1,relwidth=.5,relheight=.5)
        lbl_frmtitle.configure(text="This is Withdraw Screen")
        
        def withdraw_acn():
            amt=float(entry_amt.get())
            con=sqlite3.connect(database="banking.sqlite")
            cur=con.cursor()
            cur.execute("select bal from account where acn=?",(acn,))
            bal=cur.fetchone()[0]
            cur.close()
            
            if(bal>amt):
                cur=con.cursor()
                cur.execute("update account set bal=bal-? where acn=?",(amt,acn))
                cur.execute("insert into txn_history values(?,?,?,?,?)",(acn,amt,"Dr",time.ctime(),bal-amt))
                con.commit()
                con.close()
        
                messagebox.showinfo("Withdraw",f"Amount{amt} withdraw from to ACN:{acn}")
            else:
                messagebox.showerror("Withdraw",f"Insufficient Bal:{bal}")
        
        
        lbl_amt=Label(ifrm,text="Amount",bg='white',font=('arial',20,'bold')) 
        lbl_amt.place(relx=.1,rely=.1)
        
        entry_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        entry_amt.place(relx=.4,rely=.1)
        entry_amt.focus()
        
        btn_widrw=Button(ifrm,command=withdraw_acn,text='withdraw',font=('arial',20,'bold'),bd=5,bg='powderblue')
        btn_widrw.place(relx=.5,rely=.3)
        
    def tranfer():
        ifrm=Frame(frm,highlightthickness=1,highlightbackground='brown')
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.1,relwidth=.5,relheight=.5)
        lbl_frmtitle.configure(text="This is Tranfer Screen")
        
        def tranfer_acn():
            to_acn=entry_to.get()
            frm_amt=float(entry_amt.get())
            
            con=sqlite3.connect(database="banking.sqlite")
            cur=con.cursor()
            cur.execute("select acn,bal from account where acn=?",(to_acn,))
            to_row=cur.fetchone()
            cur.close()
            if(to_row==None):
                messagebox.showerror("Tranfer","To Account does not exist")
            else:
                cur=con.cursor()
                cur.execute("select bal from account where acn=?",(acn,))
                bal=cur.fetchone()[0]
                cur.close()
                if(bal>frm_amt):
                    cur=con.cursor()
                    cur.execute("update account set bal=bal+? where acn=?",(frm_amt,to_acn))
                    cur.execute("update account set bal=bal-? where acn=?",(frm_amt,acn))
                    cur.execute("insert into txn_history values(?,?,?,?,?)",(acn,frm_amt,"Db",time.ctime(),bal-frm_amt))
                    cur.execute("insert into txn_history values(?,?,?,?,?)",(to_acn,frm_amt,"Cr",time.ctime(),to_row[1]+frm_amt))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Transfer","Txn Done")
                else:
                    messagebox.showerror("Transfer",f"Insufficient Bal:{bal}")                                #Insufficient Balance
                    
                
            
        lbl_to=Label(ifrm,text="To",bg='white',font=('arial',20,'bold')) 
        lbl_to.place(relx=.1,rely=.2)
        
        entry_to=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        entry_to.place(relx=.4,rely=.2)
        entry_to.focus()
        
        lbl_amt=Label(ifrm,text="Amount",bg='white',font=('arial',20,'bold')) 
        lbl_amt.place(relx=.1,rely=.4)
        
        entry_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        entry_amt.place(relx=.4,rely=.4)
        entry_amt.focus()
        
        btn_trans=Button(ifrm,command=tranfer_acn,text='tranfer',font=('arial',20,'bold'),bd=5,bg='powderblue')
        btn_trans.place(relx=.5,rely=.6)
        
        
        
        
        
    def txn_history():
        ifrm=Frame(frm,highlightthickness=1,highlightbackground='brown')
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.1,relwidth=.5,relheight=.5)
        lbl_frmtitle.configure(text="This is Transaction History Screen")
        
        tv=Treeview(ifrm)
        tv.place(x=0,y=0,height=100,width=610)
        
        style=Style()
        style.configure("Treeview.Heading",font=('Arial',15,'bold'),foreground='black')

        sb=Scrollbar(ifrm,orient='vertical',command=tv.yview)
        sb.place(x=600,y=0,height=100)
        tv.configure(yscrollcommand=sb.set)
        
        tv['columns']=('col1','col2','col3','col4')

        tv.column('col1',width=150,anchor='c')
        tv.column('col2',width=100,anchor='c')
        tv.column('col3',width=80,anchor='c')
        tv.column('col4',width=100,anchor='c')

        tv.heading('col1',text='Date')
        tv.heading('col2',text='Amount')
        tv.heading('col3',text='Type')
        tv.heading('col4',text='Updated Bal')

        tv['show']='headings'
        
        con=sqlite3.connect(database='banking.sqlite')
        cur=con.cursor()
        cur.execute("select * from txn_history where acn=?",(acn,))

        for row in cur:
            tv.insert("","end",values=(row[3],row[1],row[2],row[4]))
        
    def updatepic():                                               
        img=filedialog.askopenfilename()                           #jaha user ne path bataya tha wo read kr liya 
        shutil.copy(img,f"{acn}.png")                              #YE line kah rhi hai isne current directory me pest kar liya hai
        img=Image.open(f"{acn}.png").resize((140,150))             #ye line kah rhi hai ki us image ko open kar liya hai
        imgtk=ImageTk.PhotoImage(img,master=win)                   #tkinter competable bana diya hai
        lbl_img.image=imgtk                                        #jo pahle image lagi thi use hata ke jo change ki gai hai wo laga di gai hai
        lbl_img['image']=imgtk                                     #jo pahle image lagi thi use hata ke jo change ki gai hai wo laga di gai hai
    
    btn_back=Button(frm,command=logout,text='logout',font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_back.place(relx=.93,rely=0)
    
    lbl_frmtitle=Label(frm,text="This is Login Account Screen",bg='pink',font=('arial',20,'bold'))
    lbl_frmtitle.pack() 
    
    global lbl_wel
    lbl_wel=Label(frm,text=f"Welcome,{name}",bg='pink',font=('arial',20,'bold')) 
    lbl_wel.place(relx=0,rely=0)                                             #global karne se hum direct kisi agle screen pe ja skte hai.aur hum welcome ke aage name pa skte hai.
    
    global img,imgtk,lbl_img                                                      #for image adding
    if(os.path.exists(f"{acn}.png")):                                             #ye code picture ko fixed kar deta hai aur use badanle nhi deta
        img=Image.open(f"{acn}.png").resize((140,150))
        imgtk=ImageTk.PhotoImage(img,master=win)
    else:                                                                         #for image adding
        img=Image.open("default.jpg").resize((140,150))
        imgtk=ImageTk.PhotoImage(img,master=win)                                  #for image adding
    
    lbl_img=Label(frm,image=imgtk)
    lbl_img.place(relx=.01,rely=.05)                                              #for image adding
    
    btn_propic=Button(frm,command=updatepic,text="update pic",bd=5,bg='powderblue')         #profile picture change karne ke ye buttom.
    btn_propic.place(relx=.10,rely=.25)
    
    btn_details=Button(frm,command=details,text='check details',width=12,font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_details.place(relx=0,rely=.3)
    
    btn_update_profile=Button(frm,command=update_profile,text='update profile',width=12,font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_update_profile.place(relx=0,rely=.4)
    
    btn_deposit=Button(frm,command=deposit,text='deposit',width=12,font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_deposit.place(relx=0,rely=.5)
    
    btn_withdraw=Button(frm,command=withdraw,text='withdraw',width=12,font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_withdraw.place(relx=0,rely=.6)
    
    btn_tranfer=Button(frm,command=tranfer,text='tranfer',width=12,font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_tranfer.place(relx=0,rely=.7)
    
    btn_txn_history=Button(frm,command=txn_history,text='txn history',width=12,font=('arial',20,'bold'),bd=5,bg='powderblue')
    btn_txn_history.place(relx=0,rely=.8)
main_screen()    
win.mainloop()


from tkinter.ttk import Style,Treeview,Scrollbar

root=Tk()
tv=Treeview(root)
tv.place(x=100,height=100,width=600)

style=Style()
style.configure("Treeview.Heading",font=('Arial',15,'bold'),foreground='black')

sb=Scrollbar(root,orient='vertical',command=tv.yview)
sb.place(x=600+100,y=0,height=100)
tv.configure(yscrollcommand=sb.set)

tv['columns']=('col1','col2','col3')

tv.column('col1',width=150,anchor='c')
tv.column('col2',width=150,anchor='c')
tv.column('col3',width=150,anchor='c')

tv.heading('col1',text='date')
tv.heading('col2',text='amount')
tv.heading('col3',text='type')

tv['show']='headings'


con=sqlite3.connect(database='banking.sqlite')
cur=con.cursor()
cur.execute("select * from txn_history where acn=1")

for row in cur:
    tv.insert("","end",values=(row[3],row[1],row[2]))
    
root.state('zoomed')
root.mainloop()


from tkinter import messagebox,filedialog


filedialog.askopenfilename()




