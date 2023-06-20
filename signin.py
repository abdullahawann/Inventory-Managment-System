from tkinter import*
from PIL import ImageTk
from tkinter import messagebox
import pypyodbc as odbc
import os
import OTP_email
import smtplib
import time
class signin_page:
    def __init__(self,root):
        self.root=root
        #title
        self.root.title("SIGN-IN PAGE | ENTER YOUR CREDENTIALS")
        self.root.geometry("1600x950+5+5")
        self.root.config(bg="white")

        self.otp= ''

        #image insertion of signin page
        self.phone_image=PhotoImage(file="images/signin.png")
        self.lbl_Phone_image=Label(self.root, image=self.phone_image, bd=0).place(x=200,y=90)
        #sign in page main frame 
        login_frame= Frame(self.root, bd=2, relief= SUNKEN, bg="white")
        login_frame.place(x=900, y=100, width= 550, height=550)
        #title of sign in frame
        title=Label(login_frame,text="SIGN-IN CREDENTIALS", font= ("Bahnschrift Light Condensed", 50, "bold"),bg="gray60").place(x=1,y=1, relwidth=1)
        #username 
        lbl_user= Label(login_frame, text="Employee ID", font=("Bahnschrift Light Condensed",25, "bold"), bg="gray60", fg="black").place(x=50,y=110)
        self.username=StringVar()
        self.password=StringVar()
        txt_username=Entry(login_frame, textvariable=self.username, font=("Bahnschrift Light Condensed",15), bg="white").place(x=50,y=170, width=300)
        #password
        lbl_pass= Label(login_frame, text="Password:", font=("Bahnschrift Light Condensed",25, "bold"), bg="gray60", fg="black").place(x=50,y=250)
        txt_pass=Entry(login_frame, textvariable=self.password, show="*", font=("Bahnschrift Light Condensed",15), bg="white").place(x=50,y=310, width=230)
        #signin button 
        button_login= Button(login_frame, command=self.login, text="Sign In", font=("Bahnschrift Light Condensed",30), bg="black",activebackground="black", fg="gray60",activeforeground="gray60",cursor="hand2").place(x=150, y=380, width=250, height=50)
        #----if---- 
        hr=Label(login_frame, bg="lightgray").place(x=70, y=450, width=420, height=3)
        or_=Label(login_frame, text="OR", bg= "white", fg="lightgray", font=("Bahnschrift Light Condensed",15, "bold")).place(x=270, y=435)
        #forgot password
        button_forget= Button(login_frame,text="Forgot Password?",font=("Bahnschrift Light Condensed",25, "bold"),command=self.forget_win, bg="white", fg="gray60",bd=0, activebackground="white", activeforeground="gray60", cursor="hand2").place(x=170,y=460)
        #animation images for signin page
        self.im1=ImageTk.PhotoImage(file="images/signin2.png")
        self.lbl_change_image=Label(self.root, bg="white")
        self.lbl_change_image.place(x=200,y=90, width=700, height=600)
        self.animate()

    def animate(self):
        self.im=self.phone_image
        self.phone_image=self.im1
        self.im1=self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000, self.animate)

        


#-----------------------------------------login database connection----------------------------------
    def login(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            if self.username.get() == "" or self.password.get() == "":
                messagebox.showerror('Error',"All fields are required",parent = self.root)
            else:
                cur.execute("select usertype from employee where emp_id = ? AND password = ?",(self.username.get(),self.password.get()))
                user = cur.fetchone()
                if user == None:
                    messagebox.showerror('Error',"Invalid EmployeeID/Password",parent = self.root)
                else:
                    if user[0] == "Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")


        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)

#------------------------------------------Forget password--------------------------------------------
    def forget_win(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            if self.username.get() == "":
                messagebox.showerror('Error',"Employee ID is required",parent = self.root)
            else:
                cur.execute("select email from employee where emp_id = ?",(self.username.get(),))
                email = cur.fetchone()
                if email == None:
                    messagebox.showerror('Error',"Invalid EmployeeID",parent = self.root)
                else:
                    #call otp_function
                    self.var_otp = StringVar()
                    self.var_newpass = StringVar()
                    self.var_confrimpass = StringVar()
                    #calling otp sendemail function 
                    chk=self.send_email(email[0])
                    if chk=='f':
                        messagebox.showerror("Error", "Invalid Connection, Try Again", parent=self.root)
                    else:
                        self.forget_window = Toplevel(self.root)
                        self.forget_window.title("Forget Password")
                        self.forget_window.geometry('400x350+500+100')
                        self.forget_window.focus_force()

                        title = Label(self.forget_window,text="FORGET PASSWORD",font=("Bahnschrift Light Condensed",15, "bold"),bg='black',fg='white').pack(side=TOP,fill = X)
                        lbl_reset = Label(self.forget_window,text= "Enter OTP sent on Registered Email/Spam.",font=("Bahnschrift Light Condensed",12),bg='black',fg='white').place(x=20,y=60)
                        txt_reset = Entry(self.forget_window,textvariable=self.var_otp,font=("Bahnschrift Light Condensed",14),bg='white',fg='black').place(x=20,y=100,width = 250,height = 30)
                        self.btn_reset = Button(self.forget_window,text="SUBMIT",command=self.validate_otp,font=("Bahnschrift Light Condensed",10,"bold"),bg='black',fg='white')
                        self.btn_reset.place(x=290,y=100,width = 70,height = 30)

                        newpass = Label(self.forget_window,text= "New Password",font=("Bahnschrift Light Condensed",12),bg='black',fg='white').place(x=20,y=135)
                        txt_newpass = Entry(self.forget_window,textvariable=self.var_newpass,font=("Bahnschrift Light Condensed",14),bg='white',fg='black').place(x=20,y=160,width = 250,height = 30)
                    
                        confirmpass = Label(self.forget_window,text= "Confirm Password",font=("Bahnschrift Light Condensed",12),bg='black',fg='white').place(x=20,y=195)
                        txt_confirmpass = Entry(self.forget_window,textvariable=self.var_confrimpass,font=("Bahnschrift Light Condensed",14),bg='white',fg='black').place(x=20,y=220,width = 250,height = 30)
                    
                        self.btn_passreset = Button(self.forget_window,text="RESET",command=self.update_password,state=DISABLED,font=("Bahnschrift Light Condensed",10,"bold"),bg='black',fg='white')
                        self.btn_passreset.place(x=150,y=270,width = 70,height = 30)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)

     #update password function 
    def update_password(self):
        if self.var_newpass.get()=="" or self.var_confrimpass.get()=="":
            messagebox.showerror("Error", "Password is Required to Process.", parent=self.forget_window)
        elif self.var_newpass.get()!=self.var_confrimpass.get():
             messagebox.showerror("Error", "New Password does not match with Confirm Password.", parent=self.forget_window)
        else:
            con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
            cur = con.cursor()
            try:
                cur.execute("Update employee SET password=? where emp_id=?", (self.var_newpass.get(),self.username.get()))
                con.commit()
                messagebox.showinfo("Success", "Password Updated.", parent=self.forget_window)
                self.forget_window.destroy()

            except Exception as ex:
                messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)


    #otp validate wala kaam submit krte hoye 
    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_passreset.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Error", "INVALID OTP, Try Again", parent=self.forget_window)


        #OTP EMAIL WALA KAAM
    def send_email(self, to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=OTP_email.email
        pass_=OTP_email.password
        s.login(email_,pass_)
        self.otp=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))
        subj='IMS-Reset Password OTP'
        msg= f'Dear Sir/Madam: \n\nYour OTP for reset password is {str(self.otp)}. \n\nRegards \nIMS Team'
        msg="Subject:{}\n\n{}".format(subj,msg)
        s.sendmail(email_,to_,msg)
        chk= s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'
        

root= Tk()
obj=signin_page(root)
root.mainloop()