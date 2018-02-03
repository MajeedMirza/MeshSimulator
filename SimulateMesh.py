import random
import math
import matplotlib.pyplot as plt
import time
import itertools


CURRTIME = 0
MAX_DIST = 10
#Node schema:
#0 xCoord,1 yCoord,2 Table(time,node,val),3 nodeName,4 TimeDict(node:time)
nodes = [[0,0,"NODE_A"],[0,10,"NODE_B"],[10,0,"NODE_C"]]


def main():
	global CURRTIME
	global nodes
	setup()
	while True:
		cleanPrint()
		for l in xrange(0, len(nodes)):
			nodes[l][4][nodes[l][3]] = CURRTIME
		for i in xrange(0, len(nodes)):
			for j in xrange(0, len(nodes)):
				simulate(i,j)
			#print nodes[i][3] + " " + str(nodes[i][4])
		if whatNext() == 'Q':
			return


def setup():
	global nodes
	for i in xrange(0, len(nodes)):
		nodes[i].insert(2,[])
		nodes[i].append({})
		nodes[i][4][nodes[i][3]] = CURRTIME


def whatNext():
	global CURRTIME
	instructions = "C to create new entries for each node, Enter to continue"
	instructions += ", type in node names separated by spaces, P to plot, N to create a new node or Q to quit\n"
	YorN = raw_input(instructions)
	CURRTIME += 1
	if YorN == 'C':
		print
		createEntries()
	elif YorN == 'Q':
		return 'Q'
	elif YorN == 'P':
		plot()
	elif YorN == 'N':
		newNode()
	else:
		createSpecificEntry(YorN)


def simulate(i,j):
	global nodes
	#print 'dist' + str(dist(nodes[i],nodes[j]))
	if (j != i) and (dist(nodes[i],nodes[j]) <= MAX_DIST):
		arr1 = [[nodes[i][0], nodes[i][1]], [nodes[j][0], nodes[j][1]]]
		plt.plot(*zip(*itertools.chain.from_iterable(itertools.combinations(arr1,2))))
		for key, value in nodes[j][4].iteritems():
			compareDBs(i, j, key, value)


def compareDBs(i, j, key, value):
	global nodes
	if key != nodes[i][3]:
		if not key in nodes[i][4]:
			nodes[i][4][key] = -50
		if nodes[i][4][key] < value:
			synchronize(i, j, key)


def synchronize(i, j, key):
	global nodes
	storeVal = nodes[i][4][key]
	for k in xrange(0, len(nodes[j][2])):
		if nodes[j][2][k][1] == key and nodes[j][2][k][0] > nodes[i][4].get(key):
			nodes[i][2].append(nodes[j][2][k])
			if nodes[j][2][k][0] > storeVal:
				storeVal = nodes[j][2][k][0]
	nodes[i][4][key] = storeVal


def newNode():
	xin = int(raw_input("X coordinate: "))
	yin = int(raw_input("Y coordinate: "))
	name = raw_input("Node name: ")
	newNode = [xin,yin,name]
	newNode.insert(2,[])
	newNode.append({})
	newNode[4][newNode[3]] = CURRTIME
	nodes.append(newNode)


def createEntries():
	for i in xrange(0, len(nodes)):
		nodes[i][2].append((nodes[i][4][nodes[i][3]],nodes[i][3],"test" + str(random.randint(100,999))))


def createSpecificEntry(nodeName):
	nodeName = nodeName.split(" ") 
	for i in xrange(0, len(nodes)):
		if nodes[i][3] in nodeName:
			nodes[i][2].append((nodes[i][4][nodes[i][3]],nodes[i][3],"test" + str(random.randint(100,999))))

	
def dist(n1,n2):
	return math.hypot(n2[0]-n1[0], n2[1]-n1[1])
	

def cleanPrint():
	print
	global nodes
	for i in xrange(0, len(nodes)):
		print nodes[i][3] + ': ' + ', '.join(map(str, nodes[i][2]))
	print


def plot():
	global nodes
	for i in xrange(0, len(nodes)):
		plt.scatter(nodes[i][0],nodes[i][1])
	plt.grid()
	plt.show()


if __name__ == "__main__":
    main()
