# csn2bedgraph.py v0.1

# Owen Chapman
# 02/23/2024
# Command line usage:
# python3 cns2bedgraph.py [file]

# Convert .cns file to bedgraph
# chromosome	start	end	gene	log2	depth	probes	weight	ci_lo	ci_hi
# > 
# chrom start   end value

import pandas as pd
import os
import argparse
import sys

def cns2bedgraph(file,outfile=None):
    if outfile==None:
        basename = os.path.basename(os.path.splitext(file)[0])
        outfile = basename+'.bdg'
    df = pd.read_csv(file,sep='\t')
    df=df[['chromosome','start','end','log2']]
    df.to_csv(path_or_buf=outfile,sep='\t',header=False,index=False)
    return

if __name__ == "__main__":
    # Parse input params
    parser = argparse.ArgumentParser('Generate .bedgraph by stacking bed files.')
    parser.add_argument('file')
    parser.add_argument('-o','--outfile', help='outfile (optional)',default=None)
    args = parser.parse_args()


    # Run
    cns2bedgraph(args.file,args.outfile)

