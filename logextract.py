#!/usr/bin/python
#This python script can be used to generate a summary file would list all the successful, failure, skip and errors

import os
import re
import sys

failure_count, failure_msg = 0 , []
success_count, success_msg = 0 , []
skip_count, skip_msg  = 0 , []
error_count, error_msg  = 0, []
skip_flag = 0

if len(sys.argv)!=3:
	print "./logextract.py jobID_path list_of_tests_path"
	sys.exit()

logFile=sys.argv[1]
listFile=sys.argv[2]

l = logFile.split('/')

summaryFile = "Summary_"+l[len(l)-1]+".txt"
summaryFile = open(summaryFile, "w")

text = open(logFile,'r')
readSecondLine = []

for line in text:

    if re.match("^failure:", line):
        skip_flag = 0
        #failure_count += 1
	msg=str(line.split('[')[0]).split('failure: ')[1]
	if msg.split(' ')[0] == 'setUpClass':
		listText=open(listFile,'r')
		temp=[]
		for xline in listText:
			if re.match(msg[msg.index('(')+1:msg.index(')')], xline):
				temp.append("SetUp :"+xline)
        			failure_count += 1		
		failure_msg.append(temp)
		listText.close()
    	else:
		failure_msg.append(msg)
        	failure_count += 1
        #failure_msg.append(str(line.split(' [ ')[0]).split('failure: ')[1])
	
    if re.match("^successful:", line):
        skip_flag = 0
        success_count += 1
        success_msg.append(str(line.split(' [ ')[0]).split('successful: ')[1])

    if re.match("^skip:", line):
        skip_flag = 1
        #skip_count += 1
	temp=[]
        #skip_msg.append(str(line.split(' [ ')[0]).split('skip: ')[1])
	msg= str(line.split('[')[0]).split('skip: ')[1]
	if msg.split(' ')[0] == 'setUpClass':
		listText=open(listFile,'r')
		for xline in listText:
			if re.match(msg[msg.index('(')+1:msg.index(')')], xline):
				skip_msg.append("SetUp: "+xline)
        			skip_count += 1
		listText.close()
	else:
		skip_msg.append(msg)
        	skip_count += 1

    if re.match("^error:", line):
        skip_flag = 0
        error_count += 1
        error_msg.append(str(line.split(' [ ')[0]).split('error: ')[1])

    if re.match("^reason",line) and skip_flag == 1:
	#tempMsg=' '
        readSecondLine.append(1)
	#if len(skip_msg)>1:
        tempMsg = skip_msg[len(skip_msg)-1]
        skip_msg.remove(tempMsg)

    if len(readSecondLine) >= 1:
        readSecondLine.append(1)
        if len(readSecondLine) == 4:
            skip_msg.append(tempMsg+" // reason :"+line)
            readSecondLine = []

text.close()

print "Log Summary :"
summaryFile.write("Log Summary :\n")
print "Number of tests :",failure_count+success_count+skip_count
summaryFile.write("Number of tests : %d\n" %(failure_count+success_count+skip_count))
print "Fails :",failure_count
summaryFile.write("Fails : %d\n" %(failure_count))
print "Successful :",success_count
summaryFile.write("Successful :%d\n"%(success_count))
print "Errors :",error_count
summaryFile.write("Errors : %d\n" %(error_count))
print "skip :",skip_count
summaryFile.write("skip : %d\n"%(skip_count))

print "_"*150
summaryFile.write("_"*150)
print "Details :"
summaryFile.write("\nDetails :\n")
print "Failure Details :"
summaryFile.write("Failure Details :\n")
xcount = 1
for item in failure_msg:
    if type(item)==list:
	for element in item:
		print "%d.\t%s"%(xcount,element)
		string = "%d.\t%s\n"%(xcount,element)
		summaryFile.write(string)
		xcount+=1
    else:
    	print "%d.\t%s"%(xcount,item)
	string = "%d.\t%s\n"%(xcount,item)
	summaryFile.write(string)
    	xcount += 1
print "_"*150
summaryFile.write("_"*150)
summaryFile.write("\n")


print "Skip Details :"
summaryFile.write("Skip Details :\n")
xcount = 1
for item in skip_msg:
    print "%d.\t%s"%(xcount,item)
    string = "%d.\t%s\n"%(xcount,item)
    summaryFile.write(string)
    xcount += 1
print "_"*150
summaryFile.write("_"*150)
summaryFile.write("\n")

print "Error Details :"
summaryFile.write("Error Details :\n")
xcount = 1
for item in error_msg:
    print "%d.\t%s"%(xcount,item)
    string = "%d.\t%s\n"%(xcount,item)
    summaryFile.write(string)
    xcount += 1
print "_"*150
summaryFile.write("_"*150)
summaryFile.write("\n")


print "Successful Details :"
summaryFile.write("Successful Details :\n")
xcount = 1
for item in success_msg:
    #print "%d.\t%s"%(xcount,item)
    string = "%d.\t%s\n"%(xcount,item)
    summaryFile.write(string)
    xcount += 1
print "_"*150
summaryFile.write("_"*150)
summaryFile.write("\n")
