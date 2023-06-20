from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import pypyodbc as odbc
class supplierClass:
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
        self.var_supInvoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()

        #dropdownbox
        lbl_search = Label(self.root, text = "Search by Invoice Number", bg = "white", font = ("Bahnschrift Light Condensed",12,"bold"))
        lbl_search.place(x=620,y=80)
       
        #text search
        text_search = Entry(self.root,textvariable=self.var_searchtxt,font = ("Bahnschrift Light Condensed",12),bg = "white").place(x=790,y=83,width= 200)
        text_search_button = Button(self.root,command = self.search,text = "SEARCH!",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "grey",fg = "white",cursor="hand2").place(x=1000,y=79,width = 85,height = 30)
        
        #supplier title
        employee_line_title  = Label(self.root,text = "SUPPLIER DETAILS",font = ("Bahnschrift Light Condensed",20,"bold"),bg = "black",fg = "white").place(x=70,y=10,width=1100, height = 40)
        
        #content in supplier
            #row 1
        supInvoice_lbl   = Label(self.root,text = "INVOICE NUMBER",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=70,y=86)   
        supInvoice_txt   = Entry(self.root,textvariable= self.var_supInvoice,font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=190,y=88, width = 200)
            
            #row 2
        name_lbl   = Label(self.root,text = "NAME",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=70,y=156)
        name_txt   = Entry(self.root,textvariable= self.var_name,font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=190,y=158,width = 200)
             
             #row 3
        contact_lbl   = Label(self.root,text = "CONTACT",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=70,y=236)      
        contact_txt   = Entry(self.root,textvariable= self.var_contact,font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=190,y=238,width = 200)
   
            #row 4
        descr_lbl  = Label(self.root,text = "DESCRIPTION",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black").place(x=70,y=306)
        self.descr_txt   = Text(self.root,font = ("Bahnschrift Light Condensed",12,"bold"),bg = "white",fg = "black")
        self.descr_txt.place(x=190,y=308,width = 350,height = 60)
      
        #Supplier functionality buttons
        employee_save_btn = Button(self.root,command=self.add,text = "SAVE",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "green",fg = "white",cursor="hand2").place(x=190,y=450,width = 85,height = 30)
        employee_update_btn = Button(self.root,command = self.update,text = "UPDATE",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "blue",fg = "white",cursor="hand2").place(x=290,y=450,width = 85,height = 30)
        employee_delete_btn = Button(self.root,command=self.delete,text = "DELETE",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "red",fg = "white",cursor="hand2").place(x=390,y=450,width = 85,height = 30)
        employee_clear_btn = Button(self.root,command=self.clear,text = "CLEAR",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "grey",fg = "white",cursor="hand2").place(x=490,y=450,width = 85,height = 30)
       
        #Supplier VIEWER
        emp_view_frame = Frame(self.root,bd = 3,relief=SUNKEN)
        emp_view_frame.place(x=620,y=120,width=550,height = 400)
       
        #scrollbar in supplier
        scrolly = Scrollbar(emp_view_frame,orient=VERTICAL)
        scrollx = Scrollbar(emp_view_frame,orient=HORIZONTAL)
        
        self.suppliertable = ttk.Treeview(emp_view_frame,columns=("invoice","name","contact","descr"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side = BOTTOM,fill = X) 
        scrolly.pack(side = RIGHT,fill = Y)
        scrollx.config(command=self.suppliertable.xview) 
        scrolly.config(command=self.suppliertable.yview) 
        
        self.suppliertable.heading("invoice",text = "INVOICE")
        self.suppliertable.heading("name",text = "NAME")
        self.suppliertable.heading("contact",text = "CONTACT")
        self.suppliertable.heading("descr",text = "DESCRIPTION")
        self.suppliertable["show"] = "headings"
        
        self.suppliertable.column("invoice",width = 100)
        self.suppliertable.column("name",width = 100)
        self.suppliertable.column("contact",width = 100)
        self.suppliertable.column("descr",width = 160)
        self.suppliertable.pack(fill = BOTH,expand=1)
        self.suppliertable.bind("<ButtonRelease-1>",self.get_data)
        self.show()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   
    #SAVE BUTTON FUNCTION
    def add(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            if self.var_supInvoice.get()=="" or self.var_name.get() == "":
                messagebox.showerror("Error", "Invoice must be required",parent = self.root)
            else:
                cur.execute("select * from supplier where invoice = ?",(self.var_supInvoice.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error","Invoice Number already assigned, Try Different",parent = self.root)
                else:
                    cur.execute("insert into supplier (invoice,name,contact,descr) values(?,?,?,?)",(
                                      self.var_supInvoice.get(),
                                      self.var_name.get(),
                                      self.var_contact.get(),
                                      self.descr_txt.get('1.0',END),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier added successfully",parent = self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)
   
    #FUNCTION TO SHOW DATA IN THE TREE
    def show(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            cur.execute("select * from supplier")
            row = cur.fetchall()
            self.suppliertable.delete(*self.suppliertable.get_children())
            for i in row:
                self.suppliertable.insert('',END,values=i)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)
   
    #FUNCTION TO CLICK ON DATA TO SHOW ON BOXES
    def get_data(self,ev):
        f=self.suppliertable.focus()
        content = (self.suppliertable.item(f))
        row = content['values']
        self.var_supInvoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.descr_txt.delete('1.0',END)
        self.descr_txt.insert(END,row[3]),
   
    #UPDATE FUNCTION
    def update(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            if self.var_supInvoice.get()=="":
                messagebox.showerror("Error", "Invoice Number must be required",parent = self.root)
            else:
                cur.execute("select * from supplier where invoice = ?",(self.var_supInvoice.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Invalid Invoice Number",parent = self.root)
                else:
                    cur.execute("update supplier set name= ?, contact= ?, descr= ? where invoice = ?",(
                                      self.var_name.get(),
                                      self.var_contact.get(),
                                      self.descr_txt.get('1.0',END),
                                      self.var_supInvoice.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier updated successfully",parent = self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)
   
    #DELETE FUNCTION
    def delete(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            if self.var_supInvoice.get()=="":
                messagebox.showerror("Error", "Invoice Number must be required",parent = self.root)
            else:
                cur.execute("select * from supplier where invoice = ?",(self.var_supInvoice.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Invalid Invoice Number",parent = self.root)
                else:
                    op = messagebox.askyesno("Confirm","Are You sure You want to delete this record ?",parent = self.root)
                    if op == True:
                        cur.execute("delete from supplier where invoice = ?",(self.var_supInvoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Supplier record deleted successfully",parent = self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)
    
    #Clear Function
    def clear(self):
        self.var_supInvoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.descr_txt.delete('1.0',END)
        self.var_searchtxt.set("")
        self.show()
    
    #SEARCH FUNCTION
    def search(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror("Error","Invoice Number should be required",parent = self.root)
            else:
                cur.execute("select * from supplier where invoice =?", (self.var_searchtxt.get(),))
                row = cur.fetchone()
                if row != None:
                   self.suppliertable.delete(*self.suppliertable.get_children())
                   self.suppliertable.insert('',END,values=row)
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
if __name__ == "__main__":
   root = Tk()
   obj = supplierClass(root)
   root.mainloop()