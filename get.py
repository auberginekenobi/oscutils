# get.py
# OSC
# 2021 02 18
# getter functions for all the data that's everywhere on my hard drive.

import os
import pandas as pd
import oscutils

MESIROV_ROOT  = '/mnt/c/Users/ochapman/Documents/Mesirov/'
GDRIVE_ROOT = '/home/ochapman/Google_Drive/Chavez/ecDNA/ecDNA'

def medullo_patients():
	#cohort_tbl_file = os.path.join(GDRIVE_ROOT,'2020_06_04_Cohort_Table_Master.xlsx')
	cohort_tbl_file = os.path.join(GDRIVE_ROOT,'Manuscript','Supplementary Table 1 Patient Cohort.xlsx')
	cohort_tbl = pd.read_excel(cohort_tbl_file,sheet_name='1a Patients',index_col=0)
	return cohort_tbl
	
def medullo_models():
	tbl_file = os.path.join(GDRIVE_ROOT,'Manuscript','Supplementary Table 3 Model Cohort.xlsx')
	tbl = pd.read_excel(tbl_file,sheet_name='3a Cell lines & PDXs',index_col=0)
	return tbl

def medullo_samples():
	cohort_tbl_file = os.path.join(GDRIVE_ROOT,'2020_06_04_Cohort_Table_Master.xlsx')
	cohort_tbl = pd.read_excel(cohort_tbl_file,sheet_name='S2_Samples',index_col=0)
	return cohort_tbl

def medullo_AmpliconClassifier():
	cohort_tbl_file = os.path.join(GDRIVE_ROOT,'2020_06_04_Cohort_Table_Master.xlsx')
	cohort_tbl = pd.read_excel(cohort_tbl_file,sheet_name='S3_AmpliconClassifier')
	return cohort_tbl

def medullo_plots():
	cohort_tbl_file = os.path.join(GDRIVE_ROOT,'2020_06_04_Cohort_Table_Master.xlsx')
	cohort_tbl = pd.read_excel(cohort_tbl_file,sheet_name='Plots',index_col=0)
	return cohort_tbl

def medullo_p53():
	cohort_tbl_file = os.path.join(GDRIVE_ROOT,'2020_06_04_Cohort_Table_Master.xlsx')
	cohort_tbl = pd.read_excel(cohort_tbl_file,sheet_name='Mut_status',index_col=0)
	#cohort_tbl['p53 mut (Germline)'] = ~cohort_tbl['p53 mut (Germline)'].isna()
	return cohort_tbl
	
def patient_aliases():
	pt_file = os.path.join(MESIROV_ROOT,'medullo_ecDNA','2021-05-13_p53','patient_aliases.tsv')
	pt_tbl = oscutils.tsv_to_dict_of_list(pt_file)
	return pt_tbl