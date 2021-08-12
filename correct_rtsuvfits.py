from astropy.io import fits
import sys
import glob


uvfits_list = glob.glob('uvdump_??.uvfits')
uvfiles = []
for uu in uvfits_list:
	ii0 = uu.find('p_')+2
	num = int(uu[ii0:-7])
	uvfiles.append(num)

uvfiles.sort()
print(uvfiles)
for nn in range(len(uvfiles)):
	fnum = uvfiles[nn]
	if fnum < 10:
		str_indx = '0%s' %(str(fnum))
	else:
		str_indx = '%s' %(str(fnum))


	with fits.open('uvdump_%s.uvfits' %str_indx) as hdu:
		hdu[0].header['CRVAL4'] = hdu[0].header['CRVAL4'] + 40e+3
		hdu.writeto('uvdump_edit_%s.uvfits' %str_indx, overwrite=True)
