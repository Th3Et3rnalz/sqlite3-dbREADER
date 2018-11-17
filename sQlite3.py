import sqlite3

columnWidth = 20

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
	for name in c.execute(sql):
		print name
try:
	file = raw_input('What file do you want to open?: ')
	conn = sqlite3.connect(file)
	c = conn.cursor()
except:
	print ("Something went wrong. Connecting to the file and/or opening it didn't work.")

try:
	table = raw_input("what table do you want to use? ")
	existence = tableExists(table)
        if table == "DEV":
                print "You have now entered developper mode"
                a = devMode()
		exit()
	if existence != table:
		print("This table does not exist")
		build = raw_input("Do you want to create it?")
		if build == "yes" or build == "y":
			sql = "CREATE IF NOT EXISTS "+table + " (date text, trans, text, qty real, price real)"
			c.execute(sql)
		else:
			exit()
except:
	print ("Error, couldn't open or create the table")
try:
	proceed = raw_input("What do you want to do? ")
except:
	print "Goodbye"
	proceed = ""

if proceed == "W" or proceed == "Write" or proceed == "write":
	print (table)
	date = raw_input("DATE : ")
	trans = raw_input("TRANS: ")
	qty = raw_input("QTY:   ")
	price = raw_input("PRICE: ")
	try:
		sql = "INSERT INTO "+table+"  VALUES ('"+date+"','"+trans+"',"+qty+","+price+")"
		c.execute(sql)
		conn.commit()
	except:
		print ("Error: couldn't enter the values")
if proceed == "R" or proceed == "Read" or proceed == "read":
	Col = int(readColumns(table))
	for row in c.execute('SELECT * FROM '+table+' ORDER BY date'):
		for i in range(Col):
			rowing = row[i]
			if isinstance(rowing, float):
				rowing = int(rowing)
			try:
				if len(rowing) < columnWidth:
					whitespace = " "*(columnWidth - len(rowing))
					rowing = rowing + whitespace
			except:
				if lenI(rowing) < columnWidth:
					whitespace = " "*(columnWidth- lenI(rowing))
					rowing = str(rowing) + whitespace
		        print rowing, #
		print(" ")

if proceed == "C":
	print(readColumns(table))
