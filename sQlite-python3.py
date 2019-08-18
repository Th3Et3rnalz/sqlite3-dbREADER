import sqlite3


columnWidth = 40

def FileExtensionCheck(filename):
	part = filename.split(".")
	try:
		if part[1] == "db":
			print(filename)
			return filename
		elif part[1] != "db":
			file = part[0] + ".db"
			print(filename)
			return filename
	except:
		print(" Its seems you didn't use the db extension")
		file = part[0] + ".db"
		print(file)
		return file

def tableExists(tableName):
	sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='" + tableName + "'"
	for row in c.execute(sql):
		return ''.join(row)


def lenI(integer):
	count = 0
	while (integer > 0):
		integer = integer /10
		count = count + 1
	return count

def readColumns(table):
	columnsQuery = "PRAGMA table_info(%s)" % table
	c.execute(columnsQuery)
	numberOfColumns = len(c.fetchall())
	return numberOfColumns

def devMode():
	sql = "SELECT name FROM sqlite_master WHERE type='table'"
	print()
	for name in c.execute(sql):
		print("   {}".format(name[0]))
	print()
	table = input("What table do you want?")
	print()
	try:
		c.execute('PRAGMA TABLE_INFO('+table+')')
		columns = c.fetchall()
	except:
		print("It seems that table does not exist")
	print("Column names and types:")
	numberOfColumns = 0
	for row in columns:
		print("NAME: {}, TYPE: {}".format(fixWidth(row[1], 10), fixWidth(row[2], 10)))
		numberOfColumns += 1
	print()
	rows = c.execute('SELECT * from '+ table)
	numberOfRows = 0
	for row in rows:
		numberOfRows = numberOfRows + 1
	print("There are {} entries and {} columns".format(numberOfRows, numberOfColumns))


def fixWidth(var, width):
		variable = str(var)
		if len(variable) < width:
				space = (width - len(variable)) * " "
		else:
			space = ""
		return variable + space
    		

try:
	file = input('What file do you want to open?: ')
	file = FileExtensionCheck(file)
	conn = sqlite3.connect(file)
	c = conn.cursor()
except:
	print ("Something went wrong. Connecting to the file and/or opening it didn't work.")

table = input("what table do you want to use? ")
existence = tableExists(table)
if table == "ALL":
		devMode()
		exit()
if not existence:
    # print("This table does not exist")
	cr = input("Do you want to create it?")
	if cr == "yes" or cr == "y":
		sql = "CREATE IF NOT EXISTS "+table + " (date text, trans, text, qty real, price real)"
		c.execute(sql)
	else:
		exit()

try:
	proceed = input("What do you want to do? ")
except:
	print("Goodbye")
	proceed = ""

if proceed == "W" or proceed == "Write" or proceed == "write":
	print (table)
	date = input("DATE : ")
	trans = input("TRANS: ")
	qty = input("QTY:   ")
	price = input("PRICE: ")
	try:
		sql = "INSERT INTO "+table+"  VALUES ('"+date+"','"+trans+"',"+qty+","+price+")"
		c.execute(sql)
		conn.commit()
	except:
		print ("Error: couldn't enter the values")
if proceed == "R" or proceed == "Read" or proceed == "read":
	Col = int(readColumns(table))
	print(Col)
	for row in c.execute('SELECT * FROM '+table):
		for i in range(Col):
		    print(fixWidth(row[i], columnWidth), end="")
		print(" ")

if proceed == "C":
	print(readColumns(table))

if proceed == "S":
	c.execute('PRAGMA TABLE_INFO('+table+')')
	columns = c.fetchall()
	print()
	for row in columns:
		print("UNIX: {}, NAME: {}, TYPE: ".format(fixWidth(row[0], 10), fixWidth(row[1], 10), fixWidth(row[2], 10)))
	print()
	column =  int(input("What column do you wish to query?"))
	columnName = 0
	if isinstance(column, int):
		columnName = columns[column][1]
	print()
	search = input("what do you want to search for?")
	print()
	search = "'" + str(search) + "'" 

	sql = "SELECT * from " + table + " WHERE " +str(columnName) + "=" + search
	colN = readColumns(table)
	for row in c.execute(sql):
		for i in range(colN):
			print(fixWidth(row[i], columnWidth), end="")
		print()
