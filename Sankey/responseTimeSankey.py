# This file creates json for each for the sankey diagrams

import json
from operator import itemgetter

def getInterVal(time):
	time=int(time)
	if time==0:
		return 0
	if time>=1 and time<=4:
		return 1
	elif time>=5 and time<=8:
		return 2
	elif time>=9 and time<=12:
		return 3
	elif time>=13:
		return 4

def getIndex(val,dictionary):
	for i,node in enumerate(dictionary):
		if val in node.values():
			return i

def getIndex1(val,dictionary):
	for i,node in enumerate(dictionary):
		if val in node.values():
			return i

def addNameDictionary(val,dictionary):
	for node in dictionary:

		if val in node.values():
			return -1
	dictionary.append({"name":val,"id":val})

def addLinkDictionary(source, target,dictionaryLink,dictionaryNode):
	
	source=getIndex(source,dictionaryNode)
	target=getIndex(target,dictionaryNode)
	for i,node in enumerate(dictionaryLink):
		#if getIndex(source,dictionaryNode) in node.values() and getIndex(target,dictionaryNode) in node.values():
		if source == node["source"] and target == node["target"]:
			dictionaryLink[i]["value"]+=1
			return 1
	
	dictionaryLink.append({"source":source,"target":target,"value":1})

def getTotalDecisions(sheet):
	sum=0
	for row_index in range(1,sheet.nrows):
		val=sheet.cell_value(row_index,0)
		sum+=int(val)
	return sum


##########.......................Range for category................##################3
#Thermal Range : 112+5, 112+7*16, 7
#Visual Range: 244+5, 244+7*16, 7
#Thermal+Visual Range: 5, 5+7*16 7


#..................Range for Level...................................#####################
#Thermal Range : 112+4, 112+7*16, 7
#Visual Range: 244+4, 244+7*1, 7
#Thermal+Visual Range: 4, 4+7*16 7

from xlrd import open_workbook

def createJsonNodes(ind):
	for direction in ["North","South"]:
		if direction=="North":
			sheet=sheetN
		else:
			sheet=sheetS
		#addNDictionary(direction,NSdiction)
		for row_index in range(1, 46):
		    for col_index in range(ind+5,ind+6):

		    	val=sheet.cell_value(row_index,col_index)
		    	#print(row_index,col_index,val)
		    	resTime=((sheet.cell_value(row_index,col_index+1)))
		    	#print("res time is "+str(resTime))
		    	if resTime==None:
		    		print(row_index,col_index)
		    	#addNameDictionary(val,jsonDict["nodes"])
		    	addNameDictionary((resTime),jsonDict["nodes"])

def createJSonLinks(ind):
	for direction in ["North","South"]:
		if direction=="North":
			sheet=sheetN
		else:
			sheet=sheetS
		#addNDictionary(direction,NSdiction)
		for row_index in range(1, 46):
		    for col_index in range(ind+5,ind+6):

		    	#val=sheet.cell_value(row_index,col_index)
		    	#print(row_index,col_index,val)
		    	resTime=((sheet.cell_value(row_index,col_index+1)))
		    	if resTime==None:
		    		print(row_index,col_index)
		    
		    	addLinkDictionary(direction,resTime,jsonDict["links"],jsonDict["nodes"])

book = open_workbook('NSDecisionCateg.xlsx')
sheetN = book.sheet_by_index(0)
sheetS = book.sheet_by_index(1)
for col_index in range(112+5,112+6):
	print(sheetN.cell_value(0,col_index),sheetN.cell_value(0,col_index+1))
dict_list = []
rownum=sheetN.nrows
colnum=sheetN.ncols
nameNodes=[]
links=[]
jsonDict={"nodes":[],"links":[]}
numNDec=getTotalDecisions(sheetN)
numSDec=getTotalDecisions(sheetS)
tottarget={}

	

fileWrite=open("NSThermalDecisionTime.json",'w')
createJsonNodes(112)
jsonDict["nodes"] = sorted(jsonDict["nodes"], key=itemgetter('name'))
jsonDict["nodes"].append({"name":"North","id":"North"})
jsonDict["nodes"].append({"name":"South","id":"South"})
createJSonLinks(112)
print(jsonDict)
j=json.dumps(jsonDict)
fileWrite.write(j)
#print(sheetN.cell_value(0,0))