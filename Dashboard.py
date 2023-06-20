from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
from employee import employeeclass
from supplier import supplierClass
from categories import categoryclass
from product import productclass
from sales import salesclass
from billing import BillClass
import os
import pypyodbc as odbc
import time

class IMS:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1440x900+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg = "white")
        #title
        self.main_icon = PhotoImage(file = "images/mainlogo.png") 
        title = Label(self.root , text = "Inventory Management System" ,image =self.main_icon,compound=LEFT , font=("Bahnschrift Light Condensed" , 25 , "bold"),bg ="black" ,fg="white").place(x=0,y=0,relwidth=1,height=70)
        #logout button
        logout_btn = Button(self.root,text = "Logout",font = ("Bahnschrift Light Condensed",10,"bold"),command=self.logout,bg = "white" , fg = "black",cursor = "hand2").place(x = 1300, y = 20 ,height = 40,width = 120)
        #CLOCK
        self.lbl_clock=Label(self.root, text="Welcome!\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("Bahnschrift Light Condensed",15,"bold"),bg="gray",fg="black")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        #Left side menu picture
        self.menulogo= Image.open("images/mainmenu.jpg")
        self.menulogo=self.menulogo.resize((35,35),Image.ANTIALIAS)
        self.menulogo=ImageTk.PhotoImage(self.menulogo)
        #left side menu frame
        leftmenu = Frame(self.root,bd=2,relief=FLAT,bg="gray30")
        leftmenu.place(x = 0 ,y = 70 , width = 200, height = 830)
        #Left side menu picture attributes
        lblmenu = Label(leftmenu,text = "MAIN MENU",image=self.menulogo,compound=LEFT,font=("Bahnschrift Light Condensed" , 20 , "bold"),bg = "gray60")
        lblmenu.pack(side = TOP,fill= X)
        #menu buttons
        btn_employee = Button(leftmenu,text="Employee",font=("Bahnschrift Light Condensed" , 15 , "bold"),command = self.employee, bg = "black",fg  = "white",cursor = "hand2",relief = FLAT).place(x = -2 , y = 55 ,height = 40 , width=200)
        btn_supplier = Button(leftmenu,text="Supplier",font=("Bahnschrift Light Condensed" , 15 , "bold"),command = self.supplier, bg = "black",fg  = "white",cursor = "hand2",relief = FLAT).place(x = -2 , y = 105 ,height = 40 , width=200)
        btn_category = Button(leftmenu,text="Category",font=("Bahnschrift Light Condensed" , 15 , "bold"),command = self.category, bg = "black",fg  = "white",cursor = "hand2",relief = FLAT).place(x = -2 , y = 155 ,height = 40 , width=200)
        btn_products = Button(leftmenu,text="Products",font=("Bahnschrift Light Condensed" , 15 , "bold"),command = self.product, bg = "black",fg  = "white",cursor = "hand2",relief = FLAT).place(x = -2 , y = 205 ,height = 40 , width=200)
        btn_sales = Button(leftmenu,text="Sales",font=("Bahnschrift Light Condensed" , 15 , "bold"),command = self.sales,bg = "black",fg  = "white",cursor = "hand2",relief = FLAT).place(x = -2 , y = 255 ,height = 40 , width=200)
        btn_billing = Button(leftmenu,text="Billing",font=("Bahnschrift Light Condensed" , 15 , "bold"),command = self.bill,bg = "black",fg  = "white",cursor = "hand2",relief = FLAT).place(x = -2 , y = 305 ,height = 40 , width=200)
        btn_exit = Button(leftmenu,text="Exit",font=("Bahnschrift Light Condensed" , 15 , "bold"),command= self.exit,bg = "black",fg  = "white",cursor = "hand2",relief = FLAT).place(x = -2 , y = 355 ,height = 40 , width=200)
        #main page contents
        self.lblemployee = Label(self.root , text = "Total Employees\n[0] ",bd = 5 , relief = SUNKEN,bg = "black", fg = "white" , font = ("Bahnschrift Light Condensed",20,"bold"))
        self.lblemployee.place(x = 300 , y = 120 , height = 150 , width  = 300)
        self.lblsupplier = Label(self.root , text = "Total Supplier\n[0] ",bd = 5 , relief = SUNKEN,bg = "black", fg = "white" , font = ("Bahnschrift Light Condensed",20,"bold"))
        self.lblsupplier.place(x = 650 , y = 120 , height = 150 , width  = 300)
        self.lblcategory = Label(self.root , text = "Total Categories\n[0] ",bd = 5 , relief = SUNKEN,bg = "black", fg = "white" , font = ("Bahnschrift Light Condensed",20,"bold"))
        self.lblcategory.place(x = 1000 , y = 120 , height = 150 , width  = 300)
        self.lblsales = Label(self.root , text = "Total Sales\n[0] ",bd = 5 , relief = SUNKEN,bg = "black", fg = "white" , font = ("Bahnschrift Light Condensed",20,"bold"))
        self.lblsales.place(x = 475 , y = 320 , height = 150 , width  = 300)
        self.lblproduct = Label(self.root , text = "Total Products\n[0] ",bd = 5 , relief = SUNKEN,bg = "black", fg = "white" , font = ("Bahnschrift Light Condensed",20,"bold"))
        self.lblproduct.place(x = 825 , y = 320 , height = 150 , width  = 300)
        self.bestseller = Label(self.root , text = "BEST SELLER ",bd = 5 , relief = SUNKEN,bg = "black", fg = "white" , font = ("Bahnschrift Light Condensed",20,"bold"))
        self.bestseller.place(x = 475, y = 520 , height = 150, width = 300)
        self.worstseller = Label(self.root , text = "WORST SELLER ",bd = 5 , relief = SUNKEN,bg = "black", fg = "white" , font = ("Bahnschrift Light Condensed",20,"bold"))
        self.worstseller.place(x = 825, y = 520 , height = 150, width = 300)
        self.reset_sold = Button(self.root , text = "RESET",font=("Bahnschrift Light Condensed" , 25 , "bold"),command=self.reset,bg = "black",fg  = "white",cursor = "hand2",relief = RIDGE).place(x = 750,y = 700,height = 60 , width = 110)
        #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.update_content()
        #connections with dashboard
    def employee(self):
        self.new_win = Toplevel(self.root)
        self.newobj = employeeclass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.newobj = supplierClass(self.new_win)  

    def category(self):
        self.new_win = Toplevel(self.root)
        self.newobj = categoryclass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.newobj = productclass(self.new_win)
    
    def sales(self):
        self.new_win = Toplevel(self.root)
        self.newobj = salesclass(self.new_win)

    def bill(self):
        self.new_win = Toplevel(self.root)
        self.newobj = BillClass(self.new_win)

    def logout(self):
        self.root.destroy()
        os.system("python signin.py")

    def exit(self):
        exit_op = messagebox.askyesno("Confirm","Are You sure You want to Exit?",parent = self.root)
        if exit_op == True:
            self.root.destroy()

    def reset(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        cur.execute("update product set sold = 0")
        cur.commit()

    def update_content(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            cur.execute("Select * from product")
            product=cur.fetchall()
            self.lblproduct.config(text=f'Total Products\n[{str(len(product))}]')
            cur.execute("Select * from supplier")
            supplier=cur.fetchall()
            self.lblsupplier.config(text=f'Total Suppliers\n[{str(len(supplier))}]')
            cur.execute("Select * from category")
            categories=cur.fetchall()
            self.lblcategory.config(text=f'Total Categories\n[{str(len(categories))}]')
            cur.execute("Select * from employee")
            employee=cur.fetchall()
            self.lblemployee.config(text=f'Total Employees\n[{str(len(employee))}]')
            bills=len(os.listdir('bills'))
            self.lblsales.config(text=f'Total Sales\n[{str(bills)}]')
            cur.execute("select name from employee")
            name = cur.fetchone()

            cur.execute('EXEC get_max_sold_product_name')
            best_prod_name = cur.fetchone()
            if best_prod_name[0] != None and best_prod_name[1] != 0:
                self.bestseller.config(text=f'BEST SELLER\n[{str(best_prod_name[0])}]')
            else:
                self.bestseller.config(text=f'BEST SELLER')

            cur.execute('EXEC get_min_sold_product_name')
            worst_prod_name = cur.fetchone()
            if worst_prod_name[0] != None and worst_prod_name[1] != 0:
                self.worstseller.config(text=f'WORST SELLER\n[{str(worst_prod_name[0])}]')
            else:
                self.worstseller.config(text=f'WORST SELLER')
            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome {str(name[0])}!\t\t Date:{str(date_)}\t\t Time: {str(time_)}")
            self.lbl_clock.after(200,self.update_content)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)

if __name__ == "__main__":
   root = Tk()
   obj = IMS(root)
   root.mainloop()