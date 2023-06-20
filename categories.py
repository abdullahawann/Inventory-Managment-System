from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import pypyodbc as odbc
class categoryclass:
    def __init__(self,root):
        self.root=root
        self.root.geometry(self.get_window_geometry())
        self.root.title("Inventory Management System")
        self.root.config(bg = "white")
        self.root.focus_force()
        #defining variables==========
        self.var_cat_id= StringVar()
        self.var_name= StringVar()       
        
        #label tittle==============================
        lbl_title= Label(self.root,text="Manage Product Category",font=("goudy old style",30),bg="black",fg="white").pack (side=TOP,fill=X)
        lbl_title= Label(self.root,text="Enter Category Name:", font=("goudy old style",30),bg="white").place(x=50,y=100)
        lbl_title= Entry(self.root,textvariable=self.var_name, font=("goudy old style",18),bg="lightyellow").place(x=50,y=170,width = 300)
        
        
        #adding buttons =================
        btn_add = Button (self.root,text = "Add",command = self.add, font=("goudy old style",18),bg="#4caf50",fg="white",cursor="hand2").place(x=360,y=170,width = 150,height = 30)
        btn_delete = Button (self.root,text = "Delete",command = self.delete, font=("goudy old style",18),bg="red",fg="white",cursor="hand2").place(x=520,y=170,width = 150,height = 30)



        #scrollbar in category
        cat_view_frame = Frame(self.root,bd = 3,relief=SUNKEN)
        cat_view_frame.place(x=800,y=100,width=350,height = 100)

        scrolly = Scrollbar(cat_view_frame,orient=VERTICAL)
        scrollx = Scrollbar(cat_view_frame,orient=HORIZONTAL)
        
        self.category_table = ttk.Treeview(cat_view_frame,columns=("cid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side = BOTTOM,fill = X) 
        scrolly.pack(side = RIGHT,fill = Y)
        scrollx.config(command=self.category_table.xview) 
        scrolly.config(command=self.category_table.yview) 
        
        self.category_table.heading("cid",text = "C. ID")
        self.category_table.heading("name",text = "NAME")
        self.category_table["show"] = "headings"
        
        self.category_table.column("cid",width = 100)
        self.category_table.column("name",width = 100)
     
        self.category_table.pack(fill = BOTH,expand=1)
        self.category_table.bind("<ButtonRelease-1>",self.get_data)
        self.show() 

        #==========image=============
        self.im1=Image.open("images/cat.jpg")
        self.im1=self.im1.resize((1000,400),Image.ANTIALIAS)
        self.im1=ImageTk.PhotoImage(self.im1)
        self.lbl_im1=Label(self.root,image=self.im1)
        self.lbl_im1.place(x=250,y=300)

        #==========add function==============
    def add(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            if self.var_name.get()== "":
                messagebox.showerror("Error", "Category must be required",parent = self.root)
            else:
                cur.execute("select * from category where name = ?",(self.var_name.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error","Category already added, Try New",parent = self.root)
                else:
                    cur.execute("insert into category (name) values(?)",(self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success","Category added successfully",parent = self.root)
                    self.show()
        except Exception as ex:
           messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)


 #FUNCTION TO SHOW DATA===============
    def show(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            cur.execute("select * from category")
            row = cur.fetchall()
            self.category_table.delete(*self.category_table.get_children())
            for i in row:
                self.category_table.insert('',END,values=i)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)
   
#show==================
    def get_data(self,ev):
        f=self.category_table.focus()
        content = (self.category_table.item(f))
        row = content['values']
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])



#delet=============================
    def delete(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error", "please select category from list",parent = self.root)
            else:
                cur.execute("select * from category where cid = ?",(self.var_cat_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Invalid !!! Try Again",parent = self.root)
                else:
                    op = messagebox.askyesno("Confirm","Are you sure you want to delete ?",parent = self.root)
                    if op == True:
                        cur.execute("delete from category where cid = ?",(self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Category deleted successfully",parent = self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_name.set("")
                        cur.execute("select count(CID) from category")
                        cnt = cur.fetchone()
                        if cnt[0] == 0:
                            cur.execute("truncate table category")
                            cur.commit()

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
   obj = categoryclass(root)
   root.mainloop()