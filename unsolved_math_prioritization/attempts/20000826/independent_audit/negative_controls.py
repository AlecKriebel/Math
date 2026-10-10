#!/usr/bin/env python3
"""Run semantically incorrect mutations of the author verifier in temporary copies."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--author-dir',type=Path,required=True)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    source=(args.author_dir/'verify.py').read_text()
    mutations=[
        ('drop_weight_two_variables',
         'E = weights.count(2) + r * (r + 1) // 2',
         'E = r * (r + 1) // 2'),
        ('replace_contraction_with_ordinary_derivatives',
         'rows = [[F[index[add(v, q)]] for q in quad] for v in units]',
         'rows = [[sum(i*(i+j) for i,j in zip(v,q))*F[index[add(v,q)]] for q in quad] for v in units]'),
        ('wrong_haiman_incidence_equation',
         'equation = a[1]*b[1] % p == 0',
         'equation = a[1]*b[0] % p == 0'),
        ('pretend_equal_full_hilbert_functions',
         'assert low == [2,3]',
         'assert low == [2,2]'),
        ('pretend_constant_third_layer_rank',
         'assert counts == [9,6]',
         'assert counts == [9,9]')]
    outcomes=[]
    with tempfile.TemporaryDirectory(prefix='connected-audit-mutations-') as folder:
        for label,old,new in mutations:
            if source.count(old)!=1:
                raise RuntimeError('Mutation target is not unique: '+label)
            path=Path(folder)/(label+'.py')
            path.write_text(source.replace(old,new))
            run=subprocess.run([sys.executable,str(path)],cwd=folder,
                env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
            caught=run.returncode!=0 and 'AssertionError' in run.stderr
            if not caught:
                raise RuntimeError('Negative control escaped: '+label)
            outcomes.append({'mutation':label,'rejected':True,'exit_code':run.returncode,
                             'exception':'AssertionError'})
    encoded=json.dumps({'status':'PASS','negative_controls':outcomes},indent=2,sort_keys=True)+'\n'
    if args.output: args.output.write_text(encoded)
    else: print(encoded,end='')


if __name__=='__main__': main()
