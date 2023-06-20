import pypyodbc as odbc
conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=LAPTOP-98LVI7ST\SQLEXPRESS;'
    r'DATABASE=proj;'
    r'Trusted_Connection=yes;'
)

con = odbc.connect(conn_str)
cur = con.cursor()

#cur.execute("create table employee(emp_id int PRIMARY KEY ,name VARCHAR(50),email VARCHAR(50),gender VARCHAR(50),contact VARCHAR(50),dob_yy_mm_dd date, doj_yy_mm_dd date,password VARCHAR(50),usertype VARCHAR(50),address VARCHAR(50),salary VARCHAR(50))")
#cur.commit()

#cur.execute("create table supplier(invoice int PRIMARY KEY ,name VARCHAR(50), contact VARCHAR(50), descr VARCHAR(50))")
#cur.commit()

#cur.execute("create table category(CID int PRIMARY KEY IDENTITY (1,1),name VARCHAR(50))")
#cur.commit()

cur.execute("create table product(PID int PRIMARY KEY IDENTITY (1,1),SUPPLIER varchar(50), CATEGORY varchar(50), NAME varchar(50), PRICE varchar(50), QUANTITY varchar(50), STATUS varchar(50), SOLD int)")
cur.commit()


cur.execute("CREATE PROCEDURE get_max_sold_product_name AS BEGIN SELECT TOP 1 name,sold FROM product ORDER BY sold DESC END")
cur.commit()

cur.execute("CREATE PROCEDURE get_min_sold_product_name AS BEGIN SELECT TOP 1 name,sold FROM product ORDER BY sold ASC END")
cur.commit()


