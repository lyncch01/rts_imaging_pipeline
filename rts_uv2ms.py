'''Reads in a list of uvfits files from a text file and converts them
into measurement sets'''
import glob
import sys


def make_ms(uvfits_file):
	name = uvfits_file[:-7]
	importuvfits(fitsfile=uvfits_file, vis='%s.ms' %name)

uvfits_list = glob.glob('uvdump_edit_??.uvfits')
uvfiles = []
for uu in uvfits_list:
	ii0 = uu.find('t_')+2
	num = int(uu[ii0:-7])
	uvfiles.append(num)

uvfiles.sort()
#print(sys.argv[3])
#indx = int(sys.argv[3])

for nn in range(len(uvfiles)):
	fnum = uvfiles[nn]
	if fnum < 10:
		fname = 'uvdump_edit_0%s.uvfits' %(str(fnum))

	else:
		fname = 'uvdump_edit_%s.uvfits' %(str(fnum))

#print fname
	make_ms(fname)
