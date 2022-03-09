# put.py
# OSC
# 2021 05 13
# putter functions for all the data that's everywhere on my hard drive.

import os
import pandas as pd
import oscutils

MESIROV_ROOT  = '/mnt/c/Users/ochapman/Documents/Mesirov/'
GDRIVE_ROOT = '/home/ochapman/Google_Drive/Chavez/ecDNA/ecDNA'

def patient_aliases(d):
	pt_file = os.path.join(MESIROV_ROOT,'medullo_ecDNA','2021-05-13_p53','patient_aliases.tsv')
	oscutils.write_dict_of_list(d,pt_file)
	