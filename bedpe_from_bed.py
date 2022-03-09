import argparse
import os
import functools

# Parse input params
parser = argparse.ArgumentParser('Intersect bed with itself to get complete bedpe file.')
parser.add_argument('bedfile',help='bedfile')
parser.add_argument('-o','--outfile', help='outfile (optional)',default=None)
args = parser.parse_args()

def tabify(iterable):
	return functools.reduce(lambda x,y: x+'\t'+y,iterable)+'\n'

def bedpe_from_bed(file,outfile=None):
	assert str.endswith(file,'.bed'), "Input must be bed file"
	if outfile == None:
		root = functools.reduce(lambda x,y: x+'.'+y, str.split(os.path.basename(file),'.')[:-2])
		outfile = root + '.bedpe'
	print('Writing to',outfile)
	f = open(file,'r')
	o = open(outfile,'w')
	ct=0
	lines = [] #crude
	for line in f:
		if line.startswith('#'):
			continue
		(chr1, start1, end1) = line.split()[:3]
		lines.append((chr1,start1,end1))
		for l2 in lines:
			(chr2, start2, end2) = l2
			o.write(tabify([chr1,start1,end1,chr2,start2,end2]))
			ct+=1
	print('Wrote',ct,'lines to',outfile)
	f.close();o.close()
				
bedpe_from_bed(args.bedfile,args.outfile)