# File writers to write pandas dataframe objects to the file formats required for GSEA.
# See https://software.broadinstitute.org/cancer/software/gsea/wiki/index.php/Data_formats

import pandas as pd
from collections.abc import Iterable

def exp2gct(df,outfile):
    '''
    Format a pandas dataframe of expression values as gct. See https://software.broadinstitute.org/cancer/software/gsea/wiki/index.php/Data_formats
    Input df: samples on column names, genes on row names.
    Returns: None
    '''
    # checks
    df=df.copy()
    assert ~df.columns.duplicated().all()
    assert ~df.index.duplicated().all()
    # format table
    df.index.name = 'Name'
    df.insert(loc=0,column='Description',value='')
    # write
    with open(outfile,'w') as f:
        f.write('#1.2\n')
        f.write(f'{len(df.index)}\t{len(df.columns)-1}\n')
        df.to_csv(f,sep='\t')
    return

def labels2cls(series,outfile):
    # checks
    series=series.copy()
    assert(~series.index.duplicated().all())
    # format table
    df = pd.DataFrame(series).T
    # write
    with open(outfile,'w') as f:
        a = df.iloc[0].unique()
        b = df.iloc[0].values
        f.write(f'{len(b)} {len(a)} 1\n')
        f.write(f'# {" ".join(a)}\n')
        f.write(" ".join(b))
    return

def iterable2grp(iterable,outfile,comment=None):
    '''
    Write a list (or other iterable) of gene IDs to a .grp file.
    comment may be string or iterable for multiple comments.
    '''
    assert(isinstance(iterable, Iterable))
    with(open(outfile,'w')) as f:
        # Add comments to header
        if comment is not None:
            if isinstance(comment,str):
                if not comment.startswith('#'):
                    comment='# '+comment
                f.write(comment+'\n')
            elif isinstance(comment,Iterable):
                for c in comment:
                    if not c.startswith('#'):
                        c='# '+c
                    f.write(c+'\n')
        # Write set
        f.write('\n'.join(iterable))
    return