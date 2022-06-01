import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="mohamedbouhdida100*",
    auth_plugin="mysql_native_password"
)

my_cursor=mydb.cursor()
my_cursor.execute("create database TodoApp")
my_cursor.execute("show databases")
for db in my_cursor:
    print(db)
