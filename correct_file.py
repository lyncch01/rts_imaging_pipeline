import glob

#read in file with observation IDs
fname = 'LoBES13_093.txt'

obs=[]
for line in open(fname):
	obs.append(int(line))

#create new file with observation IDs
oname = open('LoBES13_093_corr.txt', 'w')
for o in obs:
	line = '%s\n' %(str(o))
	oname.write(line)

oname.close()
	
