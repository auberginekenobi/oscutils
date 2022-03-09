import argparse
import os
import functools

# Parse input params
parser = argparse.ArgumentParser('Pair every interval in bed 1 with every interval in bed 2.')
parser.add_argument('bed1',help='bed 1')
parser.add_argument('bed2',help='bed 2')
parser.add_argument('-o','--outfile',required=True)
args = parser.parse_args()

def tabify(iterable):
	return functools.reduce(lambda x,y: x+'\t'+y,iterable)+'\n'

def bedpe_from_bed_pair(file1,file2,outfile):
	'''
	bedpe format:  chr1, start1, end1, chr2, start2, end2, name, score, strand1, strand2, args
	'''
	assert str.endswith(file1,'.bed'), "Input must be bed file"
	assert str.endswith(file2,'.bed'), "Input must be bed file"
	print('Writing to',outfile)
	f = open(file1,'r')
	o = open(outfile,'w')
	ct=0
	for line in f:
		if line.startswith('#'):
			continue
		(chr1, start1, end1) = line.split()[:3]
		g = open(file2,'r')
		for l2 in g:
			if l2.startswith('#'):
				continue
			(chr2, start2, end2) = l2.split()[:3]
			o.write(tabify([chr1,start1,end1,chr2,start2,end2]))
			ct+=1
		g.close()
	print('Wrote',ct,'lines to',outfile)
	f.close();o.close()
				
bedpe_from_bed_pair(args.bed1,args.bed2,args.outfile)