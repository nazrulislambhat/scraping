import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password"
)
mycursor = mydb.cursor()
mycursor.execute("use productshistory")
#mycursor.execute("SELECT productname FROM historyvisualization")
#mycursor.execute("SELECT * FROM historyvisualization WHERE userinput='" + userinput + "'")
#rows = mycursor.fetchall()
#numofrows = rows.count()
#if numofrows < 4:
sql = "INSERT INTO historyvisualization (productname, productprice, userinput, website) VALUES (%s,%s,%s,%s,%s)"
val = ("Sam sung",4000.00,"Samsung","snapdeal")
mycursor.execute(sql, val)
mydb.commit()