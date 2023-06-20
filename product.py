from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import pypyodbc as odbc
class productclass:
    def __init__(self,root):
        self.root=root
        self.root.geometry(self.get_window_geometry())
        self.root.title("Inventory Management System")
        self.root.config(bg = "white")
        self.root.focus_force()
        #---------------------------------------------------
        #VARIABLES DEF

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        
        self.var_pid=StringVar()
        self.var_category=StringVar()
        self.var_supplier=StringVar()
        self.category_list=[]
        self.supplier_list=[]
        self.fetch_category_supplier()
        
        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_quantity=StringVar()
        self.var_status=StringVar()


        #PRODFRAME
        product_Frame=Frame(self.root,bd=5,relief=RIDGE,bg="white")
        product_Frame.place(x=10,y=30,width=500,height=550)
        
        #product title
        product_line_title  = Label(product_Frame,text = "MANAGE PRODUCT DETAILS",font = ("Bahnschrift Light Condensed",15,"bold"),bg = "black",fg = "white").pack(side=TOP,fill=X)
        #category
        label_category  = Label(product_Frame,text = "CATEGORY",font = ("Bahnschrift Light Condensed",14),fg="black").place(x=30,y=60)
        #supplier
        label_supplier  = Label(product_Frame,text = "SUPLIER",font = ("Bahnschrift Light Condensed",14),fg="black").place(x=30,y=110)
        #prodname
        label_prodname  = Label(product_Frame,text = "NAME",font = ("Bahnschrift Light Condensed",14,),fg="black").place(x=30,y=160)
        #price
        label_price  = Label(product_Frame,text = "PRICE",font = ("Bahnschrift Light Condensed",14),fg="black").place(x=30,y=210)
        #quantity
        label_quantity  = Label(product_Frame,text = "QUANTITY",font = ("Bahnschrift Light Condensed",14),fg="black").place(x=30,y=260)
        #status
        label_status  = Label(product_Frame,text = "STATUS",font = ("Bahnschrift Light Condensed",14),fg="black").place(x=30,y=310)

        #Searches
        #category
        combobox_category = ttk.Combobox(product_Frame,textvariable=self.var_category,values= self.category_list,state = "readonly",justify = CENTER,font = ("Bahnschrift Light Condensed",12,"bold"))
        combobox_category.place(x=150,y=60,width=200)
        combobox_category.current(0)
        #supplier
        combobox_supplier = ttk.Combobox(product_Frame,textvariable=self.var_supplier,values=self.supplier_list,state = "readonly",justify = CENTER,font = ("Bahnschrift Light Condensed",12,"bold"))
        combobox_supplier.place(x=150,y=110,width=200)
        combobox_supplier.current(0)
        #prodname
        txt_name = Entry(product_Frame,textvariable=self.var_name,font=("Bahnschrift Light Condensed",12,"bold"),bg ='white').place(x=150,y=160,width=200)
        #price
        txt_price = Entry(product_Frame,textvariable=self.var_price,font=("Bahnschrift Light Condensed",12,"bold"),bg ='white').place(x=150,y=210,width=200)
        #quantity
        txt_quantity= Entry(product_Frame,textvariable=self.var_quantity,font=("Bahnschrift Light Condensed",12,"bold"),bg ='white').place(x=150,y=260,width=200)
        #status
        combobox_status = ttk.Combobox(product_Frame,textvariable=self.var_status,values= ("Active", "Inactive"),state = "readonly",justify = CENTER,font = ("Bahnschrift Light Condensed",12,"bold"))
        combobox_status.place(x=150,y=310,width=200)
        combobox_status.current(0)

        #buttons
        btn_save=Button(product_Frame,command=self.add,text = "SAVE",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "green",fg = "white",cursor="hand2").place(x=125,y=400,width = 85,height = 30)
        btn_update=Button(product_Frame,command = self.update,text = "UPDATE",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "blue",fg = "white",cursor="hand2").place(x=125,y=470,width = 85,height = 30)
        btn_delete=Button(product_Frame,command=self.delete,text = "DELETE",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "red",fg = "white",cursor="hand2").place(x=275,y=400,width = 85,height = 30)
        btn_clear=Button(product_Frame,command=self.clear,text = "CLEAR",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "grey",fg = "white",cursor="hand2").place(x=275,y=470,width = 85,height = 30)

        #search bar
        searchbar = LabelFrame(self.root, text = "Search Employee" , bg = "white", font = ("Bahnschrift Light Condensed",12,"bold"),relief = RIDGE).place(x = 650 , y = 20, width = 600, height = 80)
        #dropdownbox
        combobox_search = ttk.Combobox(self.root,textvariable=self.var_searchby,values= ("Search By", "Category","Supplier","Name"),state = "readonly",justify = CENTER,font = ("Bahnschrift Light Condensed",12,"bold"))
        combobox_search.place(x=680,y=46,width=180)
        combobox_search.current(0)
        #text search
        text_search = Entry(self.root,textvariable=self.var_searchtxt,font = ("Bahnschrift Light Condensed",12),bg = "white").place(x=875,y=47,width= 250)
        text_search_button = Button(self.root,command = self.search,text = "SEARCH!",font = ("Bahnschrift Light Condensed",12,"bold"),bg = "grey",fg = "white",cursor="hand2").place(x=1150,y=44,width = 85,height = 30)
       
       #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #Product VIEWER

        prod_viewframe = Frame(self.root,bd = 3,relief=SUNKEN)
        prod_viewframe.place(x=650,y=150,width=600,height = 430)

        #scrollbar in product
        scrolly = Scrollbar(prod_viewframe,orient=VERTICAL)
        scrollx = Scrollbar(prod_viewframe,orient=HORIZONTAL)
        
        self.prodtable = ttk.Treeview(prod_viewframe,columns=("PRODUCT ID","SUPPLIER","CATEGORY","NAME","PRICE","QUANTITY","STATUS"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side = BOTTOM,fill = X) 
        scrolly.pack(side = RIGHT,fill = Y)
        scrollx.config(command=self.prodtable.xview) 
        scrolly.config(command=self.prodtable.yview) 
        
        self.prodtable.heading("PRODUCT ID",text = "PRODUCT ID")
        self.prodtable.heading("CATEGORY",text = "CATEGORY")
        self.prodtable.heading("SUPPLIER",text = "SUPPLIER")
        self.prodtable.heading("NAME",text = "NAME")
        self.prodtable.heading("PRICE",text = "PRICE")
        self.prodtable.heading("QUANTITY",text = "QUANTITY")
        self.prodtable.heading("STATUS",text = "STATUS")
    
        self.prodtable["show"] = "headings"
        
        self.prodtable.column("PRODUCT ID",width = 80)
        self.prodtable.column("CATEGORY",width = 160)
        self.prodtable.column("SUPPLIER",width = 220)
        self.prodtable.column("NAME",width = 80)
        self.prodtable.column("PRICE",width = 110)
        self.prodtable.column("QUANTITY",width = 100)
        self.prodtable.column("STATUS",width = 100)
        self.prodtable.pack(fill = BOTH,expand=1)
        self.prodtable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
       
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
       # FUNCTIONS
       # #SAVE BUTTON FUNCTION

    def fetch_category_supplier(self):
        self.category_list.append("Empty")
        self.supplier_list.append("Empty")
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            cur.execute("select name from category ")
            category=cur.fetchall()
            if len(category)>0:
                 del self.category_list[:]
                 self.category_list.append("Select")
                 for i in category:
                    self.category_list.append(i[0])

            cur.execute("select name from supplier ")
            supplier=cur.fetchall()
            if len(supplier)>0:
                 del self.supplier_list[:]
                 self.supplier_list.append("Select")
                 for i in supplier:
                    self.supplier_list.append(i[0])


        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)

    def add(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            if self.var_category.get()=="Select" or self.var_category.get()=="Empty" or self.var_supplier.get() == "Select" or self.var_name.get() == "":
                messagebox.showerror("Error", "All  Fields Should Be Filled",parent = self.root)
            else:
                cur.execute("select * from product where Name = ?",(self.var_name.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error","This product already exists in the inventory, Try Different",parent = self.root)
                else:
                    cur.execute("insert into product (CATEGORY,SUPPLIER,NAME,PRICE,QUANTITY,STATUS,SOLD) values(?,?,?,?,?,?,?) " ,(
                                      self.var_category.get(),
                                      self.var_supplier.get(),
                                      self.var_name.get(),
                                      self.var_price.get(),
                                      self.var_quantity.get(),
                                      self.var_status.get(),
                                      0,
                                       ))
                    con.commit()
                    messagebox.showinfo("Success","Product added successfully",parent = self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)
    #FUNCTION TO SHOW DATA IN THE TREE
    def show(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            cur.execute("select * from product")
            row = cur.fetchall()
            self.prodtable.delete(*self.prodtable.get_children())
            for i in row:
                self.prodtable.insert('',END,values=i)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)
    #FUNCTION TO CLICK ON DATA TO SHOW ON BOXES
    def get_data(self,ev):
        f=self.prodtable.focus()
        content = (self.prodtable.item(f))
        row = content['values']
        self.var_pid.set(row[0]),
        self.var_supplier.set(row[1]),
        self.var_category.set(row[2]),
        self.var_name.set(row[3]),
        self.var_price.set(row[4]),
        self.var_quantity.set(row[5]),
        self.var_status.set(row[6])
       
    #UPDATE FUNCTION
    def update(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error", "Select Product From List",parent = self.root)
            else:
                cur.execute("select * from product where pid = ?",(self.var_pid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Invalid Product ID",parent = self.root)
                else:
                    cur.execute("Update product set Category= ?,Supplier= ?,name= ?,price= ?,quantity= ?,status= ? where pid = ?",(
                                      self.var_category.get(),
                                      self.var_supplier.get(),
                                      self.var_name.get(),
                                      self.var_price.get(),
                                      self.var_quantity.get(),
                                      self.var_status.get(),
                                      self.var_pid.get()

                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product updated successfully",parent = self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)

    #DELETE FUNCTION
    def delete(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error", "Select Product from the List",parent = self.root)
            else:
                cur.execute("select * from product where pid = ?",(self.var_pid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Invalid Product ID",parent = self.root)
                else:
                    op = messagebox.askyesno("Confirm","Are You sure You want to delete this record ?",parent = self.root)
                    if op == True:
                        cur.execute("delete from product where pid = ?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Product record deleted successfully",parent = self.root)
                        self.clear()
                        cur.execute("select count(PID) from product")
                        cnt = cur.fetchone()
                        if cnt[0] == 0:
                            cur.execute("truncate table product")
                            cur.commit()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)

    #Clear Function
    def clear(self):
        self.var_category.set("Select"),
        self.var_supplier.set("Select"),
        self.var_name.set(""),
        self.var_price.set(""),
        self.var_quantity.set(""),
        self.var_status.set("Active"),
        self.var_pid.set("")
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
                cur.execute("select * from product where "+self.var_searchby.get()+" like '%"+self.var_searchtxt.get()+"%'")
                row = cur.fetchall()
                if len(row) != 0:
                   self.prodtable.delete(*self.prodtable.get_children())
                   for i in row:
                       self.prodtable.insert('',END,values=i)
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
   obj = productclass(root)
   root.mainloop()