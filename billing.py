from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import os
import pypyodbc as odbc
import time
import tempfile

class BillClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1440x900+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg = "white")
        self.cart_list=[]
        self.chk_print=0
        #title
        self.main_icon = PhotoImage(file = "images/mainlogo.png") 
        title = Label(self.root , text = "Inventory Management System" ,image =self.main_icon,compound=LEFT , font=("Bahnschrift Light Condensed" , 25 , "bold"),bg ="black" ,fg="white").place(x=0,y=0,relwidth=1,height=70)
        #logout button
        logout_btn = Button(self.root,text = "Logout",font = ("Bahnschrift Light Condensed",10,"bold"),command=self.logout,bg = "white" , fg = "black",cursor = "hand2").place(x = 1300, y = 20 ,height = 40,width = 120)
        #CLOCK
        self.lbl_clock=Label(self.root, text="Welcome to Inventory Management System!\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("Bahnschrift Light Condensed",15,"bold"),bg="gray",fg="black")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        #product frame
        self.var_search=StringVar()

        Productframe1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        Productframe1.place(x=6 , y=110, width=410, height=550) 

        pTitle = Label(Productframe1, text="All Products", font=("Bahnschrift Light Condensed", 20, "bold"), bg="gray", fg="black").pack(side=TOP, fill=X)

        #search frame
        Productframe2 = Frame(Productframe1, bd=2, relief=RIDGE, bg="white")
        Productframe2.place(x=2, y=42, width=398, height=90) 

        lbl_seacrh = Label(Productframe1, text="Search Product | By Name", font=("Bahnschrift Light Condensed", 15, "bold"), bg="white", fg="green").place(x=6, y=48)

        lbl_search = Label(Productframe2, text="Product Name", font=("Bahnschrift Light Condensed", 15, "bold"), bg="white").place(x=10, y=54)
        txt_search = Entry(Productframe2, textvariable=self.var_search, font=("Bahnschrift Light Condensed", 15), bg="lightyellow").place(x=140, y=56, width=150, height=22)
        btn_search = Button(Productframe2, text="Search", command=self.search,font=("Bahnschrift Light Condensed", 15), bg="black", fg="white", cursor="Hand2").place(x=296, y=54, width=90, height=25)
        btn_showall = Button(Productframe2, text="Show All", command=self.show,font=("Bahnschrift Light Condensed", 15), bg="black", fg="white", cursor="Hand2").place(x=296, y=10, width=90, height=25)
        
        #product detail frame
        ProductFrame3 = Frame(Productframe1,bd = 3,relief=RIDGE)
        ProductFrame3.place(x=2,y=140,width=398,height=374)
       
        scrolly = Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx = Scrollbar(ProductFrame3,orient=HORIZONTAL)
        
        self.ProductDetail = ttk.Treeview(ProductFrame3,columns=("PID","NAME","PRICE","QUANTITY", "STATUS"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side = BOTTOM,fill = X) 
        scrolly.pack(side = RIGHT,fill = Y)
        scrollx.config(command=self.ProductDetail.xview) 
        scrolly.config(command=self.ProductDetail.yview) 
        
        self.ProductDetail.heading("PID",text = "PID")
        self.ProductDetail.heading("NAME",text = "NAME")
        self.ProductDetail.heading("PRICE",text = "PRICE")
        self.ProductDetail.heading("QUANTITY",text = "QTY")
        self.ProductDetail.heading("STATUS",text = "STATUS")

        self.ProductDetail["show"] = "headings"
        
        self.ProductDetail.column("PID",width = 40)
        self.ProductDetail.column("NAME",width = 100)
        self.ProductDetail.column("PRICE",width = 100)
        self.ProductDetail.column("QUANTITY",width = 40)
        self.ProductDetail.column("STATUS",width = 90)

        self.ProductDetail.pack(fill = BOTH,expand=1)
        self.ProductDetail.bind("<ButtonRelease-1>",self.get_data)
        lbh_note=Label(Productframe1, text="Note: 'Enter 0 Quantity to remove Product from the Cart'", font=("Bahnschrift Light Condensed", 12), bg="white", fg="red").pack(side=BOTTOM, fill=X)

        #customer frame
        self.var_cname=StringVar()
        self.var_contact=StringVar()

        customerFrame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        customerFrame.place(x=420 , y=110, width=530, height=70)

        cTitle = Label(customerFrame, text="Customer Details", font=("Bahnschrift Light Condensed", 15), bg="lightgrey").pack(side=TOP, fill=X)
        lbl_name = Label(customerFrame, text="Name", font=("Bahnschrift Light Condensed", 15), bg="white").place(x=5, y=34)
        txt_name = Entry(customerFrame, textvariable=self.var_cname, font=("Bahnschrift Light Condensed", 13), bg="lightyellow").place(x=64, y=35, width=180)
        
        lbl_contact = Label(customerFrame, text="Contact No.", font=("Bahnschrift Light Condensed", 15), bg="white").place(x=270, y=34)
        txt_contact = Entry(customerFrame, textvariable=self.var_contact, font=("Bahnschrift Light Condensed", 13), bg="lightyellow").place(x=376, y=35, width=140)

        #Cal cart frame 
        CalCartFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        CalCartFrame.place(x=420 , y=190, width=530, height=360)

        # Cal frame
        self.var_cal_input= StringVar()
        CalFrame = Frame(CalCartFrame, bd=9, relief=RIDGE, bg="white")
        CalFrame.place(x=5, y=10, width=268, height=340)
        txt_cal_input= Entry(CalFrame, textvariable=self.var_cal_input, font=('Bahnschrift Light Condensed', 15, 'bold'), width=26, bd=10,relief=GROOVE, state='readonly', justify=RIGHT)
        txt_cal_input.grid(row=0, columnspan=4)
        button7= Button(CalFrame,text='7', font=('Bahnschrift Light Condensed',15,'bold'), command= lambda: self.getinput(7),bd=6, width=5, pady=10, cursor="hand2").grid(row=1, column=0)
        button8= Button(CalFrame,text='8', font=('Bahnschrift Light Condensed',15,'bold'), command= lambda: self.getinput(8),bd=6, width=5, pady=10, cursor="hand2").grid(row=1, column=1)
        button9= Button(CalFrame,text='9', font=('Bahnschrift Light Condensed',15,'bold'), command= lambda: self.getinput(9),bd=6, width=5, pady=10, cursor="hand2").grid(row=1, column=2)
        buttonsum= Button(CalFrame,text='+', font=('Bahnschrift Light Condensed',15,'bold'), command= lambda: self.getinput('+'),bd=7, width=5, pady=10, cursor="hand2").grid(row=1, column=3)

        button4= Button(CalFrame,text='4', font=('Bahnschrift Light Condensed',15,'bold'), command= lambda: self.getinput(4),bd=6, width=5, pady=10, cursor="hand2").grid(row=2, column=0)
        button5= Button(CalFrame,text='5', font=('Bahnschrift Light Condensed',15,'bold'), command= lambda: self.getinput(5),bd=6, width=5, pady=10, cursor="hand2").grid(row=2, column=1)
        button6= Button(CalFrame,text='6', font=('Bahnschrift Light Condensed',15,'bold'), command= lambda: self.getinput(6),bd=6, width=5, pady=10, cursor="hand2").grid(row=2, column=2)
        buttonsub= Button(CalFrame,text='-', font=('Bahnschrift Light Condensed',15,'bold'), command= lambda: self.getinput('-'),bd=7, width=5, pady=10, cursor="hand2").grid(row=2, column=3)

        button1= Button(CalFrame,text='1', font=('Bahnschrift Light Condensed',15,'bold'), command= lambda: self.getinput(1),bd=6, width=5, pady=10, cursor="hand2").grid(row=3, column=0)
        button2= Button(CalFrame,text='2', font=('Bahnschrift Light Condensed',15,'bold'), command= lambda: self.getinput(2), bd=6, width=5, pady=10, cursor="hand2").grid(row=3, column=1)
        button3= Button(CalFrame,text='3', font=('Bahnschrift Light Condensed',15,'bold'), command= lambda: self.getinput(3),bd=6, width=5, pady=10, cursor="hand2").grid(row=3, column=2)
        buttonmul= Button(CalFrame,text='*', font=('Bahnschrift Light Condensed',15,'bold'), command= lambda: self.getinput('*'),bd=7, width=5, pady=10, cursor="hand2").grid(row=3, column=3)

        button0= Button(CalFrame,text='0', font=('Bahnschrift Light Condensed',15,'bold'), command= lambda: self.getinput(0),bd=6, width=5, pady=15, cursor="hand2").grid(row=4, column=0)
        buttonc= Button(CalFrame,text='c', font=('Bahnschrift Light Condensed',15,'bold'), command=self.clearcal,bd=6, width=5, pady=15, cursor="hand2").grid(row=4, column=1)
        buttonequal= Button(CalFrame,text='=', font=('Bahnschrift Light Condensed',15,'bold'),command= self.performcal, bd=6, width=5, pady=15, cursor="hand2").grid(row=4, column=2)
        buttondiv= Button(CalFrame,text='/', font=('Bahnschrift Light Condensed',15,'bold'), command= lambda: self.getinput('/'),bd=6, width=5, pady=15, cursor="hand2").grid(row=4, column=3)



        #Cart Frame
        CartFrame = Frame(CalCartFrame,bd = 3,relief=RIDGE)
        CartFrame.place(x=280,y=8,width=245,height=342)
        self.cartTitle = Label(CartFrame, text="Cart \t Total Product: [0]", font=("Bahnschrift Light Condensed", 15), bg="lightgrey")
        self.cartTitle.pack(side=TOP, fill=X)
        
        scrolly = Scrollbar(CartFrame,orient=VERTICAL)
        scrollx = Scrollbar(CartFrame,orient=HORIZONTAL)
        
        self.cartTable = ttk.Treeview(CartFrame,columns=("PID","NAME","PRICE","QUANTITY"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side = BOTTOM,fill = X) 
        scrolly.pack(side = RIGHT,fill = Y)
        scrollx.config(command=self.cartTable.xview) 
        scrolly.config(command=self.cartTable.yview) 
        
        self.cartTable.heading("PID",text = "PID")
        self.cartTable.heading("NAME",text = "NAME")
        self.cartTable.heading("PRICE",text = "PRICE")
        self.cartTable.heading("QUANTITY",text = "QTY")

        self.cartTable["show"] = "headings"
        
        self.cartTable.column("PID",width = 40)
        self.cartTable.column("NAME",width = 40)
        self.cartTable.column("PRICE",width = 90)
        self.cartTable.column("QUANTITY",width = 40)

        self.cartTable.pack(fill = BOTH,expand=1)
        self.cartTable.bind("<ButtonRelease-1>",self.get_data_cart)
        
        #add cart frame
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()

        addcartFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        addcartFrame.place(x=420, y=550, width=530, height=110)

        lbl_p_name=Label(addcartFrame, text="Product Name", font=("Bahnschrift Light Condensed", 15), bg='white').place(x=5, y=5)
        txt_p_name=Entry(addcartFrame, textvariable=self.var_pname, font=("Bahnschrift Light Condensed", 15), bg='lightyellow', state='readonly').place(x=5, y=35, width=190, height=22)

        lbl_p_price=Label(addcartFrame, text="Price Per Qty", font=("Bahnschrift Light Condensed", 15), bg='white').place(x=230, y=5)
        txt_p_price=Entry(addcartFrame, textvariable=self.var_price, font=("Bahnschrift Light Condensed", 15), bg='lightyellow', state='readonly').place(x=230, y=35, width=150, height=22)

        lbl_p_qty=Label(addcartFrame, text="Quantity", font=("Bahnschrift Light Condensed", 15), bg='white').place(x=390, y=5)
        txt_p_qty=Entry(addcartFrame, textvariable=self.var_qty, font=("Bahnschrift Light Condensed", 15), bg='lightyellow').place(x=390, y=35, width=120, height=22)

        self.lbl_inStock=Label(addcartFrame, text="In Stock", font=("Bahnschrift Light Condensed", 15), bg='white')
        self.lbl_inStock.place(x=5, y=70) 

        btn_clear_cart=Button(addcartFrame, text='clear', command=self.clear_cart,font=('Bahnschrift Light Condensed', 15, 'bold'), bg='lightgray', cursor="hand2").place(x=180, y=70, width=150, height=30)
        btn_add_cart=Button(addcartFrame, text='Add | Update', command=self.add_update_cart,font=('Bahnschrift Light Condensed', 15, 'bold'), bg='orange', cursor="hand2").place(x=340, y=70, width=180, height=30)
######## BILLING SECTION
        billframe= Frame(self.root, bd=2, relief=RIDGE,bg='white')
        billframe.place(x=953, y=110, width=410,height=410)
        bTitle = Label(billframe, text="Bill of Customer", font=("Bahnschrift Light Condensed", 20, "bold"), bg="gray", fg="black").pack(side=TOP, fill=X)
        scrolling=Scrollbar(billframe, orient=VERTICAL)
        scrolling.pack(side=RIGHT, fill=Y)
        self.txtbillarea=Text(billframe, yscrollcommand=scrolling.set)
        self.txtbillarea.pack(fill=BOTH, expand=1)
        scrolling.config(command=self.txtbillarea.yview)

######## BUTTONS FOR BILLING
        billframemenu= Frame(self.root, bd=2, relief=RIDGE,bg='white')
        billframemenu.place(x=953, y=520, width=410,height=140)
        
        self.lblamnt= Label(billframemenu, text='Bill Amount\n[0]', cursor="hand2",font=("Bahnschrift Light Condensed", 15, "bold"), bg="Purple", fg="white",bd=6)
        self.lblamnt.place(x=2,y=5, width=120, height=70)

        self.lbldiscount= Label(billframemenu, text='Discount\n[5%]', cursor="hand2",font=("Bahnschrift Light Condensed", 15, "bold"), bg="Green", fg="white",bd=6)
        self.lbldiscount.place(x=124,y=5, width=120, height=70)

        self.lblnetpay= Label(billframemenu, text='Net Pay\n[0]', cursor="hand2",font=("Bahnschrift Light Condensed", 15, "bold"), bg="Red", fg="white",bd=6)
        self.lblnetpay.place(x=246,y=5, width=160, height=70)

        btnprint= Button(billframemenu, text='Print Bill', command=self.print_bill,cursor="hand2",font=("Bahnschrift Light Condensed", 15, "bold"), bg="Brown", fg="white",bd=6)
        btnprint.place(x=2,y=80, width=120, height=50)

        btnclearall= Button(billframemenu, text='Clear', command=self.clear_all,cursor="hand2",font=("Bahnschrift Light Condensed", 15, "bold"), bg="black", fg="white",bd=6)
        btnclearall.place(x=124,y=80, width=120, height=50)

        btngenerate= Button(billframemenu, text='Generate Bill', cursor="hand2",font=("Bahnschrift Light Condensed", 15, "bold"),command=self.generate_bill, bg="violet", fg="white",bd=6)
        btngenerate.place(x=246,y=80, width=160, height=50)

###### FOOTER_NOTE
        footer= Label(self.root, text="Inventory Management System\n For Queries Please Contact 090078601", font=("Bahnschrift Light Condensed",20,"bold"),bg= "black", fg="white", bd=1,cursor="hand2").place(y=700,x=0,width=1500)
        self.show()
        #self.bill_top()
        self.update_date_time()

#FUNCTIONS
    def logout(self):
        self.root.destroy()
        os.system("python signin.py")

    def getinput(self, num):
        x=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(x)

    def clearcal(self):
        self.var_cal_input.set('')

    def performcal(self):
        res=self.var_cal_input.get()
        self.var_cal_input.set(eval(res))

    def show(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            cur.execute("select PID,NAME,PRICE,QUANTITY,STATUS from product where STATUS= 'Active' ")
            row = cur.fetchall()
            self.ProductDetail.delete(*self.ProductDetail.get_children())
            for i in row:
                self.ProductDetail.insert('',END,values=i)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)

    def search(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            if self.var_search.get()== "":
                messagebox.showerror("Error","Please input a value",parent = self.root)
            else:
                cur.execute("select PID,NAME,PRICE,QUANTITY,STATUS from product where name like '%"+self.var_search.get()+"%' and STATUS='Active' ")
                row = cur.fetchall()
                if len(row) != 0:
                   self.ProductDetail.delete(*self.ProductDetail.get_children())
                   for i in row:
                       self.ProductDetail.insert('',END,values=i)
                else:
                    messagebox.showerror("Error","No record found",parent = self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)

    def get_data(self,ev):
        f=self.ProductDetail.focus()
        content = (self.ProductDetail.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')
        

    def get_data_cart(self,ev):
        f=self.cartTable.focus()
        content = (self.cartTable.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])

    def add_update_cart(self):
        if self.var_pid.get()=='':
            messagebox.showerror('Error', "Select Product from the List.", parent=self.root)
        elif self.var_qty.get()=='':
            messagebox.showerror('Error', "Quantity is Required.", parent=self.root)
        elif (int(self.var_qty.get()) > int(self.var_stock.get())) or (int(self.var_qty.get()) < 0):
            messagebox.showerror('Error', "Insufficient Quantity", parent=self.root)
        else:
            #price_cal=float(int(self.var_qty.get())*float(self.var_price.get()))
            price_cal = self.var_price.get()
            cart_data=[self.var_pid.get(), self.var_pname.get(), price_cal, self.var_qty.get(),self.var_stock.get()]
            ### UPDATE CART
            present='no'
            index_=-1
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            if present=='yes':
                op=messagebox.askyesno('Confirm', "Product is already Present \nDo you want to Update|Remove from Cart List.", parent= self.root)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        #self.cart_list[index_][2]=price_cal           #####PRICE
                        self.cart_list[index_][3]=self.var_qty.get()  #####QUANTITY
            else:                
                self.cart_list.append(cart_data)
            
            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))
        if self.bill_amnt >= 20000:
            self.net_pay=self.bill_amnt-((self.bill_amnt*5)/100)
            self.discount=(self.bill_amnt*5)/100
        else:
            self.net_pay=self.bill_amnt
            self.discount=0
        self.lblamnt.config(text=f'Bill Amnt\n{str(self.bill_amnt)}')
        self.lblnetpay.config(text=f'Net Pay\n{str(self.net_pay)}')
        self.cartTitle.config(text=f"Cart \t Total Product: [{str(len(self.cart_list))}]")


    def show_cart(self):
        try:
            self.cartTable.delete(*self.cartTable.get_children())
            for i in self.cart_list:
                self.cartTable.insert('',END,values=i)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)

    def generate_bill(self):
        if self.var_cname.get() == '' or self.var_contact.get() =='':
            messagebox.showerror('Error',f'Please enter Customer Name and Contact',parent=self.root)
        elif len(self.cart_list) == 0:
            messagebox.showerror('Error',f'Cart is Empty',parent=self.root)
        else:
            #================Bill Top Part==============
            self.bill_top()
            #================Bill Middle Part==============
            self.bill_middle()
            #================Bill Bottom Part==============
            self.bill_bottom()

            fp=open(f'bills/{str(self.invoice)}.txt','w')
            fp.write(self.txtbillarea.get('1.0',END))
            fp.close()
            messagebox.showinfo('Saved', "Bill has been saved in the Backend.", parent=self.root)
            self.chk_print=1


    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        bill_top_temp = f'''
\t\tIMS-INVENTORY
\tPHONE NO. : 090078601 , LHR-FAST-NU
{str("="*47)}
Customer Name : {self.var_cname.get()}
Customer PhNo. : {self.var_contact.get()}
Bill No. : {str(self.invoice)}\t\t\tDate : {str(time.strftime("%d/%m/%Y"))} 
{str("="*47)}
Product Name\t\t\tQTY\tPrice
{str("="*47)}
        '''
        self.txtbillarea.delete('1.0',END)
        self.txtbillarea.insert('1.0',bill_top_temp)

    def bill_middle(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        try:
            for row in self.cart_list:
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status='Inactive'
                if int(row[3])!=int(row[4]):
                    status='Active'
                price=float(row[2])*int(row[3])
                price=str(price)
                cur.execute("select SOLD from product where pid = ?",(
                    pid,
                ))
                sold = cur.fetchone()
                sold = sold[0] + int(row[3])
                self.txtbillarea.insert(END,"\n "+name+"\t\t\t"+row[3]+"\tRs."+price)
                cur.execute('Update product set quantity= ?,status= ? , sold = ? where pid = ?',(
                    qty,
                    status,
                    sold,
                    pid
                ))
                cur.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent = self.root)


    def bill_bottom(self):
        bill_bottom_temp = f'''
{str("="*47)}
Bill Amnt :\t\t\t\tRs{self.bill_amnt}
Discount :\t\t\t\tRs{self.discount}
Net Amnt :\t\t\t\tRs{self.net_pay}
{str("="*47)}\n
        '''
        self.txtbillarea.insert(END,bill_bottom_temp)

    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set('')

    def clear_all(self):
        self.chk_print=0
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txtbillarea.delete('1.0',END)
        self.cartTitle.config(text=f"Cart \t Total Product: [0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()

    def update_date_time(self):
        con = odbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'r'DATABASE=proj;'r'Trusted_Connection=yes;')
        cur = con.cursor()
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        cur.execute("select name from employee")
        name = cur.fetchone()

        self.lbl_clock.config(text=f"Welcome {str(name[0])}!\t\t Date:{str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)

    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Print',"Printing your Receipt.",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txtbillarea.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror('Print',"Generate Bill to Print Receipt.",parent=self.root)

if __name__ == "__main__":
   root = Tk()
   obj = BillClass(root)
   root.mainloop()
