# Owen Chapman
# 10/26/2021
# Command line usage:
# python3 $bed_from_chopchop -o chopchop_1.bed chopchop_1.txt

import argparse
import sys
import functools

# Parse input params
parser = argparse.ArgumentParser('Generate bed file from CHOPCHOP text output')
parser.add_argument('chopchop',help='Output format for CHOPCHOP, eg. "2 ACGCGCTCTCCAAGTATACGTGG chr8:127735448 + 55 0 0 0 0 0 1.00"')
parser.add_argument('-o','--outfile', help='outfile (optional)',default=None)
args = parser.parse_args()

def tabify(iterable):
	return functools.reduce(lambda x,y: x+'\t'+y,iterable)+'\n'

def bed_from_chopchop(file,outfile=None):
	if outfile == None:
		write = sys.stdout.write
		outfile = 'stdout'
	else:
		o = open(outfile,'w')
		write = o.write
	print('Writing to',outfile)
	f = open(file,'r')
	ct=0
	for line in f:
		if line.startswith('#'):
			continue
		(rank,seq,start,strand) = line.split()[:4]
		chr=start.split(':')[0]
		start=int(start.split(':')[1])-1
		end=start+len(seq)
		write(tabify([chr,str(start),str(end),seq,rank,strand]))
		ct+=1
	print('Wrote',ct,'lines to',outfile)
	f.close()
	if outfile is not 'stdout':
		o.close() 

bed_from_chopchop(args.chopchop,args.outfile)
