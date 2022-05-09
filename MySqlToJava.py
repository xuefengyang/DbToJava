import pymysql
import os


def openDb():
	db = pymysql.connect(host="127.0.0.1",user="root",password="Yxf1234!",port=3306,database="xt_prod",charset="utf8")
	return db


def writeToJavaFile(fields,tableName):
	file = open(tableName,"w+")

	file.write("package com.sousou.social.api.entity;")
	file.write(os.linesep)
	file.write(os.linesep)
	file.write(os.linesep)
	file.write("import java.math.BigDecimal;")
	file.write(os.linesep)
	file.write("import java.util.Date;")
	file.write(os.linesep)
	file.write(os.linesep)

	file.write("public class GoodsPriority {")
	file.write(os.linesep)
	for field in fields:
		file.write("private %s %s ;" % (field['type'], underscore_to_camelcase(field['name'])))
		file.write(os.linesep)

	file.write(os.linesep)
	file.write("}")
	file.flush()

def underscore_to_camelcase(value):
	res = []
	loop = 0
	for x in value.split("_"):
		loop = loop + 1
		if loop == 1:
			res.append(x)
		else:
			res.append(x.capitalize())
	return "".join(res)

def getTypeToJavaMap(mysqlType):
	maps = {"bigint(20) unsigned":"Long", "bigint": "Long", "bigint(20)": "Long"}
	if mysqlType.startswith("bigint"):
		return "long"
	elif mysqlType.startswith("int"):
		return "int"
	elif mysqlType.startswith("varchar"):
		return "String"
	elif mysqlType.startswith("timestamp"):
		return "Date"
	elif mysqlType.startswith("decimal"):
		return "BigDecimal"
	elif mysqlType.startswith("datetime"):
		return "Date"
	elif mysqlType.startswith("smallint"):
		return "int"
	elif mysqlType.startswith("longtext"):
		return "String"
	elif mysqlType.startswith("text"):
		return "String"
	elif mysqlType.startswith("tinyint"):
		return "int"
	else:
		return "undefined"

if __name__ == '__main__':
	print("*** Open DB ***")
	SQL = " DESC zzkj_goods"
	try:
		db = openDb()
		cursor = db.cursor(pymysql.cursors.DictCursor)
		cursor.execute(SQL)
		rows = cursor.fetchall()
		fields = []
		for row in rows:
			#print(row['Field'],row['Type'])
			fields.append({"name": row["Field"], "type": getTypeToJavaMap(row['Type'])})
		#print(fields)
		print("*** Start Gen ***")
		writeToJavaFile(fields,"test")
		print("*** End Gen ***")
		cursor.close()
		db.close()

	except Exception as e:
		raise
	else:
		pass
	finally:
		pass
	print("*** Close DB ***")

