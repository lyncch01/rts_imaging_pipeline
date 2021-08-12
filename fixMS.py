import glob
import sys
import os

uvfits_list = glob.glob('uvdump_edit_??.uvfits')
uvfiles = []
for uu in uvfits_list:
        ii0 = uu.find('t_')+2
        num = int(uu[ii0:-7])
        uvfiles.append(num)

uvfiles.sort()
#indx = int(sys.argv[2])

for nn in range(len(uvfiles)):
	fnum = uvfiles[nn]

	if fnum < 10:
       		fname = 'uvdump_edit_0%s.uvfits' %(str(fnum))

	else:
       		fname = 'uvdump_edit_%s.uvfits' %(str(fnum))
	
	#print fname

	obsID = str(sys.argv[1])
	metafile = obsID+'_metafits_ppds.fits'

	cmd = 'fixmwams %s.ms %s' %(fname[:-7], metafile)
	#print cmd
	os.system(cmd)
