#-*-encoding: utf-8 -*-
import networkx as nx
import numpy
import re
edge_list = []
node_list = {}
Dump = {}
data = []
class Item:
	def __init__(self):
		self.item_id = -1
		self.title = 'NULL'
		self.Year = -1
		self.Publisher = 'NULL'
		self.author = []
		self.cite = []

def make_Author(str):
	data = str.split(",")
	return data
def parsing_data(chunk):
	partition = re.findall(r'(.*?)\n', chunk, re.DOTALL)
	if len(partition) ==0: 
		t = Item()
		t.item_id = -1
		return t
	title = partition[0]
	author = make_Author(partition[1][2:])
	year = int(partition[2][2:])
	publisher = partition[3][2:]
	item_id = int(partition[4][6:])
	cite = []	
	for t in partition[5:]:
		if len(t.strip()) >=3:
			cite.append(int(t[2:]))

	I = Item() 
	I.item_id = item_id
	I.title = title
	I.author = author
	I.year = year
	I.publisher = publisher
	I.cite = cite
	return I

def id_year_printer():
	for i in range(1960,2014):
		pwd = "./preprocessing/"+str(i)+".txt"
		f_out_1 = open(pwd, "a")

		for j in data:
			if (j.year == i):
				f_out_1.write(str(j.item_id) + "," + str(j.year)+"\n")
def all_cite_printer():
	pwd = "all_cite.txt"
	f_out_2 = open(pwd,"a")

	for i in data:
		if (len(i.cite)>=1):
			for j in i.cite:
				f_out_2.write(str(i.item_id)+"," + str(j) + "\n")

def all_id_year_printer():
	pwd = "all_id_year.txt"
	f_out_1 = open(pwd, "a")
	for j in data:
		f_out_1.write(str(j.item_id) + "," + str(j.year)+"\n")	

def all_author_printer():
	pwd = "all_author.txt"
	f_out_1 = open(pwd, "a")
	for i in data:
		for j in i.author:
			f_out_1.write(j + ","+ str(i.item_id) + "," + str(i.year) + "\n")	

def all_publisher_printer():
	pwd = "all_publisher.txt"
	f_out_1 = open(pwd, "a")
	for i in data:
		f_out_1.write(i.publisher + "," + str(i.item_id) + "," + str(i.year) + "\n")	
def calc():
	f_in = open("./data/publications3.txt", "r")
	line = f_in.read()
	f_in.close()
	m = re.findall('\#\*(.*?)\#\!', line, re.DOTALL)
	print len(m)
	for chunk in m:
		I = Item()
		I = parsing_data(chunk)
		if (I.item_id == -1):
			continue
		if (I.item_id % 10000 ==0):
			print I.item_id


		data.append(I)

	#id_year_printer()
	all_cite_printer()	
	all_id_year_printer()
	all_author_printer()
	all_publisher_printer()


def data_cutter():
	#메모리가 터져서 ... 데이터를 잘랐다.
	f_in = open("./data/publications.txt", "r")
	f_out_1 = open("./data/publications1.txt","w")
	f_out_2 = open("./data/publications2.txt","w")
	f_out_3 = open("./data/publications3.txt","w")

	lines = f_in.readlines()
	num = 1

	for line in lines:
		partition = re.findall(r'#index(.*?)\n', line, re.DOTALL)

		if len(partition) == 1:
			if int(partition[0]) > 727320:
				num = 2
			if int(partition[0]) > 2858594:
				num = 3

		if num == 1:
			f_out_1.write(line)
		elif num == 2:
			f_out_2.write(line)
		else:
			f_out_3.write(line)


def year_sizer_node():
	#연도별 데이터의 크기를 알아보자, a마지막을 제외하고 계속 증가한다. 

	year_saved = {}
	year_cumul_saved = {}
	year_saved[-1] = 0
	for i in range(1936,2014):
		year_saved[i] = 0 
		year_cumul_saved[i] = 0

	print year_saved

	f_in = open("./pre-processed data/all_id_year.txt")
	data = f_in.readlines()

	for i in data:
		t2 = i.split(",")
		t = int(t2[1])
		#if (int(t2[0]) > 3490000 ):
		#if (int(t2[0]) % 10000  == 0):
		#	print t2
		year_saved[t] = year_saved[t]  + 1


	temp  = 0
	for i in range(1936,2014):
		temp = temp + year_saved[i]
		year_cumul_saved[i] = temp


	f_out = open("year_cited.csv","w")

	for i in range(1936,2014):
		f_out.write(str(i)+","+str(year_saved[i])+","+str(year_cumul_saved[i])+"\n")

def year_sizer_author():
	#나중에 진행하시오 
	f_in = open("./pre-processed data/all_author.txt")
	data = f_in.readlines()

	author = []
	for i in data:
		#print str (i) + "\n"
		t = i.split(",")
		author.append(t[0])

	author = list(set(author))

	author_year = {}

	for i in author:
		author_year[i] = 9999

	for i in data:
		t = i.split(",")
		name = t[0]
		year = int(t[2])

		if (author_year[name] > year):
			author_year[name] = year

	yearly = {}
	for i in range(1936, 2014):
		yearly[i] = 0

	for j in author_year:
		try:
			yearly[author_year[j]] = yearly[author_year[j]] + 1
		except:
			print author_year[j]
	f_out = open("year_author.csv","w")
	for i in range(1936, 2014):
		f_out.write(str(i) +","+ str(yearly[i]) + "\n")

def cite_year_divider():
	#연도별로 인용 링크를 나누어준다.
	f_in_1 = open("./pre-processed data/all_cite.txt","r")
	f_in_2 = open("./pre-processed data/all_id_year.txt", "r")

	t_year = f_in_2.readlines()
	t_cite = f_in_1.readlines()

	f_in_1.close()
	f_in_2.close()
	item_id = {}

	for i in t_year:
		t = i.split(",")
		t1 = int(t[0])
		t2 = int(t[1])
		if (t2 != -1):
			item_id[t1] = t2


	f_error = open("cite_year_divider_error.txt","w")
	for i in range(2013, 2014):
		print i
		f_out = open("./divided_by_year_data/" +str(i) + "_cite.csv","w")

		for j in t_cite:
			tt = j.split(",")
			id1 = int(tt[0])
			id2 = int(tt[1])
			try:
				if (item_id[id1] <= i and item_id[id2] <=i):
					f_out.write(str(id1) + ","+ str(id2) + "\n")
			except:
				f_error.write(str(id1) + "," +str(id2)+"\n")
		f_out.close()


def initialize():
	f_in = open("./divided_by_year_data/2013_cite.csv", "r")
	lines = f_in.readlines()
	
	for line in lines:
		data = line.split(",")
		Dump[int(data[0])] = {}
		Dump[int(data[1])] = {}


def make_net():
	#네트워크를 만들고 Centurality를 계산하고 저장할 것이다.
	initialize()

	for i in range(2013, 2014):
		print i
		f_in = open("./divided_by_year_data/" +str(i) + "_cite.csv","r")
		year = i

		lines = f_in.readlines()
		f_in.close()
		edge_list = []
		for line in lines:
			data = line.split(",")
			data_tuple = (int(data[0]), int(data[1]))
			edge_list.append(data_tuple)

		Net = nx.DiGraph(edge_list)
		#Cen_in = nx.in_degree_centrality(Net)
		Cen_in = nx.degree_centrality(Net)
		#Cen_in = nx.eigenvector_centrality(Net)
		#Cen_in = nx.katz_centrality(Net)
		#Cen_in = nx.pagerank(Net)

		f_out = open("./in_degree/" + str(i) + ".csv","w")
		for j in Cen_in:
			key = j
			val = Cen_in[j]
			f_out.write(str(key) + "," + str(val) + "\n")
		f_out.close()
"""
		for j in Cen_in:
			key = j
			val = Cen_in[j]
			#print str(key) + " " + str(val)
			Dump[key][year] = val


	f_out = open("degree_centrality.csv", "w")
	for key in Dump:
		line = str(key)
		for year in range(1936, 2014):
			data = Dump[key].get(year, 0)
			line = line + ","+ str(data)
		line = line + "\n"
		f_out.write(line)
	f_out.close()
"""

def Cited_count():
	initialize()
	for i in range(1936, 2014):
		year = i
		print i
		f_in = open("./divided_by_year_data/"+str(i) + "_cite.csv", "r")

		lines = f_in.readlines()
		edge_list = []
		for line in lines:
			data = line.split(",")
			key = int(data[1])
			Dump[key][year] = Dump[key].get(year,0) + 1

	f_out = open("cited_count.csv", "w")
	for key in Dump:
		line = str(key)
		for year in range(1936, 2014):
			data = Dump[key].get(year, 0)
			line = line + ","+ str(data)
		line = line + "\n"
		f_out.write(line)

def test():
	print "in the server"
#calc()
#data_cutter()
#cite_year_divider()
#make_net() 
#Cited_count()

