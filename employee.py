from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import pypyodbc as odbc
from datetime import date
import datetime
class employeeclass:
    def __init__(self,root):
        self.root=root
        self.root.geometry(self.get_window_geometry())
        self.root.title("Inventory Management System")
        self.root.config(bg = "white")
        self.root.focus_force()
        #---------------------------------------------------
        #all variables to be used employee
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_empid = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_dob_year = StringVar()
        self.var_dob_year.set("1900")
        self.var_dob_month = StringVar()
        self.var_dob_month.set("1")
        self.var_dob_day = StringVar()
        self.var_dob_day.set("1")
        self.var_doj_year = StringVar()
        self.var_doj_year.set("1900")
        self.var_doj_month = StringVar()
        self.var_doj_month.set("1")
        self.var_doj_day = StringVar()
        self.var_doj_day.set("1")
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_usertype = StringVar()
        self.var_salary = StringVar()

        #search bar
        searchbar = LabelFrame(self.root, text = "Search Employee" , bg = "white", font = ("Bahnschrift Light Condensed",12,"bold"),relief = RIDGE).place(x = 300 , y = 20 , width = 600, height = 70)
           #dropdownbox
        combobox_search = ttk.Combobox(self.root,textvariable=self.var_searchby,values= ("Search By", "Email","Name" ,"emp_id" , "Contact"),state = "readonly",justify = CENTER,font = ("Bahnschrift Light Condensed",12,"bold"))
        combobox_search.place(x=310,y=46,width=180)
        combobox_search.current(0)
           #text search
        text_search = Entry(self.root,textvariable=self.var_searchtxt,font = ("Bahnschrift Light Condensed",12),bg = "white").place(x=510,y=47,width= 250)
        text_search_button = Button(self.root,command = self.search,text = "SEARCH!",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "grey",fg = "white",cursor="hand2").place(x=780,y=44,width = 85,height = 30)
        #employee title
        employee_line_title  = Label(self.root,text = "EMPLOYEE DETAILS",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "black",fg = "white").place(x=70,y=120,width=1100)
        #content in employee
            #row 1
        empid_lbl   = Label(self.root,text = "EMPLOYEE ID",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=70,y=160)
        gender_lbl  = Label(self.root,text = "GENDER",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=460,y=160)
        contact_lbl  = Label(self.root,text = "Contact INFO",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=820,y=160)
        
        empid_txt   = Entry(self.root,textvariable= self.var_empid,font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=170,y=162, width=200)
        combobox_gender = ttk.Combobox(self.root,textvariable=self.var_gender,values= ("Select", "Male","Female" ,"Other"),state = "readonly",justify = CENTER,font = ("Bahnschrift Light Condensed",10,"bold"))
        combobox_gender.place(x=540,y=162,width=200)
        combobox_gender.current(0)
        contact_txt  = Entry(self.root,textvariable= self.var_contact,font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=920,y=160,width = 250)
            #row 2
        name_lbl   = Label(self.root,text = "NAME",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=70,y=240)
        dob_lbl  = Label(self.root,text = "D.O.B(YYYY/MM/DD)",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=420,y=240)
        doj_lbl  = Label(self.root,text = "D.O.J(YYYY/MM/DD)",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=800,y=240)
        
        name_txt   = Entry(self.root,textvariable= self.var_name,font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=170,y=242,width = 200)
        dob_year_entry = Entry(self.root,textvariable= self.var_dob_year,font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=540,y=242, width=65)
        dob_month_entry = Entry(self.root,textvariable= self.var_dob_month,font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=610,y=242, width=65)
        dob_day_entry = Entry(self.root,textvariable= self.var_dob_day,font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=680,y=242, width=65)
        doj_year_entry = Entry(self.root,textvariable= self.var_doj_year,font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=920,y=242, width=65)
        doj_month_entry = Entry(self.root,textvariable= self.var_doj_month,font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=990,y=242, width=65)
        doj_day_entry = Entry(self.root,textvariable= self.var_doj_day,font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=1060,y=242, width=65)    
        #row 3
        email_lbl   = Label(self.root,text = "EMAIL",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=70,y=320)
        password_lbl  = Label(self.root,text = "PASSWORD",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=460,y=320)
        usertype_lbl  = Label(self.root,text = "USERTYPE",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=820,y=320)
        
        
        email_txt = Entry(self.root, textvariable=self.var_email, font=("Bahnschrift Light Condensed", 12, "bold"), bg="white", fg="black")
        email_txt.place(x=170, y=322, width=200)
        email_txt.bind("<KeyRelease>", self.on_email_key_release)
        

        password_txt  = Entry(self.root,textvariable= self.var_pass,font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=540,y=322, width=200)
        combobox_usertype = ttk.Combobox(self.root,textvariable=self.var_usertype,values= ("Select", "Admin","Employee" ),state = "readonly",justify = CENTER,font = ("Bahnschrift Light Condensed",10,"bold"))
        combobox_usertype.place(x=920,y=322, width=250)
        combobox_usertype.current(0)
            #row 4
        address_lbl  = Label(self.root,text = "ADDRESS",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=70,y=400)
        salary_lbl  = Label(self.root,text = "SALARY",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=820,y=400)
        
        self.address_txt   = Text(self.root,font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black")
        self.address_txt.place(x=170,y=402,width = 570, height=24)
        salary_txt  = Entry(self.root,textvariable= self.var_salary,font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=920,y=402, width=250)
        # employee functionality buttons
        employee_save_btn = Button(self.root,command=self.add,text = "SAVE",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "green",fg = "white",cursor="hand2").place(x=420,y=480,width = 85,height = 30)
        employee_update_btn = Button(self.root,command = self.update,text = "UPDATE",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "blue",fg = "white",cursor="hand2").place(x=520,y=480,width = 85,height = 30)
        employee_delete_btn = Button(self.root,command=self.delete,text = "DELETE",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "red",fg = "white",cursor="hand2").place(x=620,y=480,width = 85,height = 30)
        employee_clear_btn = Button(self.root,command=self.clear,text = "CLEAR",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "grey",fg = "white",cursor="hand2").place(x=720,y=480,width = 85,height = 30)
        #EMPLOYEE VIEWER
        emp_view_frame = Frame(self.root,bd = 3,relief=SUNKEN)
        emp_view_frame.place(x=0,y=580,relwidth=1,height = 200)
        #scrollbar in employee
        scrolly = Scrollbar(emp_view_frame,orient=VERTICAL)
        scrollx = Scrollbar(emp_view_frame,orient=HORIZONTAL)
        
        self.emptable = ttk.Treeview(emp_view_frame,columns=("emp_id","name","email","gender","contact","dob_yy_mm_dd","do_yy_mm_dd","password","usertype","address","salary"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side = BOTTOM,fill = X) 
        scrolly.pack(side = RIGHT,fill = Y)
        scrollx.config(command=self.emptable.xview) 
        scrolly.config(command=self.emptable.yview) 
        
        self.emptable.heading("emp_id",text = "EMP ID")
        self.emptable.heading("name",text = "NAME")
        self.emptable.heading("email",text = "Email")
        self.emptable.heading("gender",text = "Gender")
        self.emptable.heading("contact",text = "Contact")
        self.emptable.heading("dob_yy_mm_dd",text = "D.O.B")
        self.emptable.heading("do_yy_mm_dd",text = "D.O.J")
        self.emptable.heading("password",text = "Password")
        self.emptable.heading("usertype",text = "User Type")
        self.emptable.heading("address",text = "Address")
        self.emptable.heading("salary",text = "Salary")

        self.emptable["show"] = "headings"
        
        self.emptable.column("emp_id",width = 80)
        self.emptable.column("name",width = 160)
        self.emptable.column("email",width = 220)
        self.emptable.column("gender",width = 80)
        self.emptable.column("contact",width = 110)
        self.emptable.column("dob_yy_mm_dd",width = 100)
        self.emptable.column("do_yy_mm_dd",width = 100)
        self.emptable.column("password",width = 110)
        self.emptable.column("usertype",width = 90)
        self.emptable.column("address",width = 300)
        self.emptable.column("salary",width = 90)
        self.emptable.pack(fill = BOTH,expand=1)
        self.emptable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #SAVE BUTTON FUNCTION
    def add(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            if self.var_empid.get()=="" or self.var_name.get() == "" or self.var_pass.get() == "" or self.var_usertype.get() == "Select":
                messagebox.showerror("Error", "Employee ID/Name/Password/Usertype Can not be null",parent = self.root)
            else:
                cur.execute("select * from employee where emp_id = ?",(self.var_empid.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error","This employee ID is already assinged, Try Different",parent = self.root)
                else:
                    cur.execute("insert into employee (emp_id,name,email,gender,contact,dob_yy_mm_dd,doj_yy_mm_dd,password,usertype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                                      self.var_empid.get(),
                                      self.var_name.get(),
                                      self.var_email.get(),
                                      self.var_gender.get(),
                                      self.var_contact.get(),
                                      f"{self.var_dob_year.get()}-{self.var_dob_month.get()}-{self.var_dob_day.get()}",
                                      f"{self.var_doj_year.get()}-{self.var_doj_month.get()}-{self.var_doj_day.get()}",
                                      self.var_pass.get(),
                                      self.var_usertype.get(),
                                      self.address_txt.get('1.0',END),
                                      self.var_salary.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employee added successfully",parent = self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)
    #FUNCTION TO SHOW DATA IN THE TREE
    def show(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            cur.execute("select * from employee")
            row = cur.fetchall()
            self.emptable.delete(*self.emptable.get_children())
            for i in row:
                self.emptable.insert('',END,values=i)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)
    #FUNCTION TO CLICK ON DATA TO SHOW ON BOXES
    def get_data(self,ev):
        f=self.emptable.focus()
        content = (self.emptable.item(f))
        row = content['values']
        self.var_empid.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        dob = datetime.datetime.strptime(row[5], '%Y-%m-%d')
        self.var_dob_year.set(dob.year)
        self.var_dob_month.set(dob.month)
        self.var_dob_day.set(dob.day)
        doj = datetime.datetime.strptime(row[6], '%Y-%m-%d')
        self.var_doj_year.set(doj.year)
        self.var_doj_month.set(doj.month)
        self.var_doj_day.set(doj.day)
        self.var_pass.set(row[7])
        self.var_usertype.set(row[8])
        self.address_txt.delete('1.0',END)
        self.address_txt.insert(END,row[9]),
        self.var_salary.set(row[10])
    #UPDATE FUNCTION
    def update(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            if self.var_empid.get()=="":
                messagebox.showerror("Error", "Employee ID and Name Can not be null",parent = self.root)
            else:
                cur.execute("select * from employee where emp_id = ?",(self.var_empid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Invalid employee ID",parent = self.root)
                else:
                    cur.execute("update employee set name= ?,email= ?,gender= ?,contact= ?,dob_yy_mm_dd= ?,doj_yy_mm_dd= ?,password= ?,usertype= ?,address= ?,salary= ? where emp_id = ?",(
                                      self.var_name.get(),
                                      self.var_email.get(),
                                      self.var_gender.get(),
                                      self.var_contact.get(),
                                      f"{self.var_dob_year.get()}-{self.var_dob_month.get()}-{self.var_dob_day.get()}",
                                      f"{self.var_doj_year.get()}-{self.var_doj_month.get()}-{self.var_doj_day.get()}",
                                      self.var_pass.get(),
                                      self.var_usertype.get(),
                                      self.address_txt.get('1.0',END),
                                      self.var_salary.get(),
                                      self.var_empid.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employee updated successfully",parent = self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)
    #DELETE FUNCTION
    def delete(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            if self.var_empid.get()=="":
                messagebox.showerror("Error", "Employee ID and Name Can not be null",parent = self.root)
            else:
                cur.execute("select * from employee where emp_id = ?",(self.var_empid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Invalid employee ID",parent = self.root)
                else:
                    op = messagebox.askyesno("Confirm","Are You sure You want to delete this record ?",parent = self.root)
                    if op == True:
                        cur.execute("delete from employee where emp_id = ?",(self.var_empid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Employee record deleted successfully",parent = self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)
    #Clear Function
    def clear(self):
        self.var_empid.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob_year.set("1900")
        self.var_dob_month.set("1")
        self.var_dob_day.set("1")
        self.var_doj_year.set("1900")
        self.var_doj_month.set("1")
        self.var_doj_day.set("1")
        self.var_pass.set("")
        self.var_usertype.set("Select")
        self.address_txt.delete('1.0',END)
        self.var_salary.set("")
        self.var_searchby.set("Search By")
        self.var_searchtxt.set("")
        self.show()
    #SEARCH FUNCTION
    def search(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Search By":
                messagebox.showerror("Error","Please Select an Option",parent = self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error","Please input a value",parent = self.root)
            else:
                cur.execute("select * from employee where "+self.var_searchby.get()+" like '%"+self.var_searchtxt.get()+"%'")
                row = cur.fetchall()
                if len(row) != 0:
                   self.emptable.delete(*self.emptable.get_children())
                   for i in row:
                       self.emptable.insert('',END,values=i)
                else:
                    messagebox.showerror("Error","No record found",parent = self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)
    

    def get_window_geometry(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.86)
        window_height = int(screen_height * 0.8)
        window_x = int((screen_width - window_width) / 2)
        window_y = int((screen_height - window_height) / 2)
        return f"{window_width}x{window_height}+{window_x}+{window_y}"
    
    def on_email_key_release(self, event):
            text = self.var_email.get()
            if "@" not in text:
                index = len(text) - text[::-1].index(".")
                self.var_email.set(text[:index] + "@" + text[index:])
if __name__ == "__main__":
   root = Tk()
   obj = employeeclass(root)
   root.mainloop()