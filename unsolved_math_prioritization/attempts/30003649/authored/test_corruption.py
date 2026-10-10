#!/usr/bin/env python3
"""Reject modified public inputs using the independently authored checker."""
import copy
from fractions import Fraction
import gzip
import json
from pathlib import Path
import shutil
import sys
import tempfile
from verify_certificate import verify, selftest


def main(source):
    records=[]
    with tempfile.TemporaryDirectory(prefix='cp-independent-controls-') as temp:
        target=Path(temp)/'data';shutil.copytree(source,target)
        cases=[('orthogonal_matrix','exact_algebraic_certificate.json'),
               ('trace','exact_algebraic_certificate.json'),
               ('generator','rational_cone_certificate.json'),
               ('missing_facet','facets.json'),
               ('gram_entry','A_integer.mtx.gz')]
        for name,filename in cases:
            path=target/filename
            original=path.read_bytes()
            if name=='gram_entry':
                lines=gzip.decompress(original).decode().splitlines()
                eligible=[i for i,line in enumerate(lines) if line and not line.startswith('%')]
                i=eligible[1];x,y,z=map(int,lines[i].split());lines[i]=f'{x} {y} {z+1}'
                path.write_bytes(gzip.compress(('\n'.join(lines)+'\n').encode(),mtime=0))
            else:
                obj=json.loads(original)
                if name=='orthogonal_matrix':
                    v=obj['orthogonal_matrix'][0][0];v[0]=str(Fraction(v[0])+1)
                elif name=='trace':
                    v=obj['Q'][0][0];v[0]=str(Fraction(v[0])+1)
                elif name=='generator':
                    obj['generators'][0][0]=str(Fraction(obj['generators'][0][0])+1)
                else:
                    obj['facet_normals'].pop()
                path.write_text(json.dumps(obj))
            try:
                verify(target)
            except ValueError as exc:
                records.append({'mutation':name,'rejected':True,'reason':str(exc)})
            else:
                raise RuntimeError(f'corrupted input accepted: {name}')
            path.write_bytes(original)
    return {'status':'PASS','arithmetic_controls':selftest(),'corruption_controls':records}


if __name__=='__main__':
    print(json.dumps(main(Path(sys.argv[1])),indent=2,sort_keys=True))
