from tkinter import*
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import pypyodbc as odbc
import sqlite3
import os

class salesclass:
    def __init__(self,root):
        self.root=root
        self.root.geometry(self.get_window_geometry())
        self.root.title("Inventory Managment System")
        self.root.config(bg="white")
        self.root.focus_force()
        #variable=====================
        self.var_invoice= StringVar()   
        self.bill_list = []
        #titlee==================
        lbl_title= Label(self.root,text="Customer Bills",font=("goudy old style",30),bg="black",fg="white").pack (side=TOP,fill=X)
        lbl_invoice= Label(self.root,text="Invoice Number:", font=("times new roman",18),bg="white").place(x=30,y=80)
        txt_invoice= Entry(self.root,textvariable=self.var_invoice, font=("times new roman",18),bg="lightyellow").place(x=200,y=80,width = 180,height=28)
        
# buttons===============
        btn_search = Button (self.root,text = "Search",command=self.search, font=("times new roman",15, "bold"),bg="#4caf50",fg="white",cursor="hand2").place(x=400,y=80,width = 120,height = 28)
        btn_clear = Button (self.root,text = "Clear",command=self.clear, font=("goudy old style",18),bg="red",fg="white",cursor="hand2").place(x=540,y=80,width = 120,height = 28)
 
#makingg frameof bill list============
        sales_frame= Frame(self.root,bd=3,relief=RIDGE)
        sales_frame.place(x=50,y=140,width=400,height=330)
        #scroll===========listbox===========
        scrolly= Scrollbar (sales_frame,orient=VERTICAL)
        self.sales_lists=Listbox(sales_frame,font=("goudy old style",30),bg="white",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.sales_lists.yview)
        self.sales_lists.pack(fill=BOTH,expand=1)

        #bill area 
        bill_list= Frame(self.root,bd=3,relief=RIDGE)
        bill_list.place(x=470,y=140,width=480,height=330)

        lbl_title2= Label(bill_list,text="Customer Bill Area",font=("goudy old style",20),bg="black",fg="white").pack (side=TOP,fill=X)
     



        #bill area scroll bar 
        scrolly2= Scrollbar (bill_list,orient=VERTICAL)
        self.bill_area=Text(bill_list,bg="lightyellow",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand=1)
        self.sales_lists.bind("<ButtonRelease-1>",self.getdata)




#image============================
        self.bill_photo= Image.open("images/bill.jpg")
        self.bill_photo=self.bill_photo.resize((400,300),Image.LANCZOS)
        self.bill_photo=ImageTk.PhotoImage(self.bill_photo) 

        lbl_image1=Label(self.root,image=self.bill_photo,border=0)
        lbl_image1.place(x=1000,y=150)

# show bill lists==========
        self.show()
    def show(self):
        self.sales_lists.delete(0,END)
        for i in os.listdir('bills'):
            if i.split('.')[-1]=='txt':
                self.sales_lists.insert(END,i)
                self.bill_list.append(i.split('.')[0])
            
# open bill file and show data=========
    def getdata(self,ev):
     index_= self.sales_lists.curselection()
     file_name= self.sales_lists.get(index_)
     print(file_name)
     self.bill_area.delete("1.0",END)
     fp= open(f'bills/{file_name}','r')
     for i in fp:
        self.bill_area.insert(END,i)
     fp.close()

     #search==============
    def search(self):
        if self.var_invoice.get()=="":
            messagebox.showerror("Error","Invoice NO. should be required",parent=self.root)
        else:
            print(self.bill_list,self.var_invoice.get())
            if self.var_invoice.get() in self.bill_list:
               fp= open(f'bills/{self.var_invoice.get()}.txt','r')
               self.bill_area.delete('1.0',END)
               for i in fp:
                  self.bill_area.insert(END,i)
               fp.close()
            else:
                messagebox.showerror("Error","Invalid Invoice Number",parent=self.root)

     

#clear function===============
    def clear(self):
        self.show()
        self.bill_area.delete('1.0',END)
        self.var_invoice.set("")


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
   obj = salesclass(root)
   root.mainloop()