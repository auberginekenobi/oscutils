# oscutils.py
# OSC
# 2021 05 13
# misc python file utilities.
import os
from collections import OrderedDict

def tsv_to_dict_of_list(filepath):
	with open(filepath, 'r') as f:
		d = OrderedDict()
		for line in f:
			t = line.strip().split('\t')
			d[t[0]] = t[1:]
		return d
	
def write_dict_of_list(od,filepath):
	with open(filepath,'w') as f:
		for (key,li) in od.items():
			line='\t'.join(li)
			line=key+'\t'+line+'\n'
			f.write(line)
		
def reverse_dict_of_list(d):
	nd = {}
	for k,v in d.items():
		for i in v:
			nd[i]=k
	return nd