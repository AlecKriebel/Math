#!/usr/bin/env python3
"""Pinned independent audit replay. Extracts only the verified ten-file safe archive.
Rejects archive/member/fixture drift before mathematical acceptance; Python 3 only.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

ARCHIVE_SHA='0b194b2b9ee859709b8e668f881aeb2db4939cc3939b2a99a6d79bfebbc02dda'
MANIFEST_SHA='fee2951571dfc9e040fb822d077d10eead948d6ab60abc93a62f0936ec59004d'
INDEPENDENT_SHA='9ee1764662160702894e816f522782f4f2aeef00fa5bafc45127b95c022be0fd'
INDEPENDENT_RESULT_SHA='50faf016562c74da55974e793cd472b417034c0d331e747e7d15d2f90bb2bbf1'

def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def call(argv,cwd):return subprocess.run([sys.executable]+argv,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
def main():
    root=Path(__file__).resolve().parent
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive',type=Path,default=root/'AUTHOR_SAFE_FREEZE.zip')
    parser.add_argument('--manifest',type=Path,default=root/'AUTHOR_EXTERNAL_MANIFEST.json')
    args=parser.parse_args()
    b=args.archive.read_bytes();need(len(b)==14473 and sha(b)==ARCHIVE_SHA,'author archive pin mismatch')
    mb=args.manifest.read_bytes();need(sha(mb)==MANIFEST_SHA,'external manifest pin mismatch')
    m=json.loads(mb); files=m['files']
    need(m['archive_sha256']==ARCHIVE_SHA and len(files)==10,'external manifest inconsistent')
    ib=(root/'independent_check.py').read_bytes();need(sha(ib)==INDEPENDENT_SHA,'independent checker pin mismatch')
    expected_i=(root/'INDEPENDENT_RESULTS.json').read_bytes();need(sha(expected_i)==INDEPENDENT_RESULT_SHA,'independent results pin mismatch')
    results={'problem_id':2851,'full_problem_solved':False,'archive_pin_verified':True,'member_count':10}
    with tempfile.TemporaryDirectory(prefix='strong-heegaard-independent-') as td:
        td=Path(td);author=td/'author';author.mkdir();unrelated=td/'unrelated';unrelated.mkdir()
        with zipfile.ZipFile(args.archive) as z:
            names=z.namelist();need(len(names)==len(set(names))==10,'duplicate or wrong ZIP member count')
            need(set(names)=={f['path'] for f in files},'member set mismatch')
            for f in files:
                name=f['path'];need(Path(name).name==name and name not in ('.','..'),'unsafe member name')
                data=z.read(name);need(len(data)==f['bytes'] and sha(data)==f['sha256'],'member pin mismatch: '+name)
                (author/name).write_bytes(data)
        internal=json.loads((author/'MANIFEST.json').read_text())
        need(internal['allowed_files']==[x for x in files if x['path']!='MANIFEST.json'],'internal manifest mismatch')
        expected=(author/'CHECK_RESULTS.json').read_bytes()
        runs=[]
        for mode in [[],['-O']]:
            p=call(mode+[str(author/'verify.py')],author)
            need(p.returncode==0 and p.stdout==expected and not p.stderr,'author replay mismatch')
            p=call(mode+[str(author/'verify.py')],unrelated)
            need(p.returncode==0 and p.stdout==expected and not p.stderr,'relocated author replay mismatch')
            runs.append({'mode':'optimized' if mode else 'normal','normal_and_unrelated_cwd_match_record':True})
        data=json.loads((author/'claims.json').read_text());cases={}
        def add(name,fn):
            d=copy.deepcopy(data);fn(d);cases[name]=json.dumps(d).encode()
        add('wrong_id',lambda d:d.__setitem__('problem_id',2852))
        add('boolean_id',lambda d:d.__setitem__('problem_id',True))
        add('wrong_number',lambda d:d.__setitem__('problem_number','KP-3.54'))
        add('entry_removed',lambda d:d['matrix'][0].__setitem__(0,0))
        add('weighted_entry',lambda d:d['matrix'][0].__setitem__(0,2))
        add('negative_entry',lambda d:d['matrix'][0].__setitem__(0,-1))
        add('boolean_entry',lambda d:d['matrix'][0].__setitem__(0,True))
        add('float_entry',lambda d:d['matrix'][0].__setitem__(0,1.0))
        add('ragged_matrix',lambda d:d['matrix'][0].pop())
        add('missing_row',lambda d:d['matrix'].pop())
        add('wrong_determinant',lambda d:d.__setitem__('expected_determinant',23))
        add('float_determinant',lambda d:d.__setitem__('expected_determinant',24.0))
        add('wrong_histogram_count',lambda d:d['expected_boundary_histogram'].__setitem__('5',2015))
        add('extra_histogram_bin',lambda d:d['expected_boundary_histogram'].__setitem__('7',0))
        add('missing_histogram_bin',lambda d:d['expected_boundary_histogram'].pop('1'))
        add('float_histogram_count',lambda d:d['expected_boundary_histogram'].__setitem__('1',2688.0))
        add('wrong_minimum_genus',lambda d:d.__setitem__('minimum_neighborhood_genus',7))
        add('float_minimum_genus',lambda d:d.__setitem__('minimum_neighborhood_genus',9.0))
        add('overclaimed_scope',lambda d:d.__setitem__('claim_scope','KP-3.53 solved'))
        add('missing_field',lambda d:d.pop('matrix'))
        add('extra_field',lambda d:d.__setitem__('arbitrary_signings',True))
        cases.update({'invalid_json':b'{','wrong_top_level':b'[]','null_top_level':b'null'})
        rejection=[]
        for name,raw in sorted(cases.items()):
            f=td/(name+'.json');f.write_bytes(raw)
            for mode in [[],['-O']]:
                p=call(mode+[str(author/'verify.py'),'--fixture',str(f)],unrelated)
                need(p.returncode==1 and p.stderr.startswith(b'REJECT: ') and not p.stdout,'mutation accepted or not explicit: '+name)
                rejection.append({'case':name,'mode':'optimized' if mode else 'normal','exit_code':p.returncode,'stderr':p.stderr.decode().strip()})
        for mode in [[],['-O']]:
            p=call(mode+[str(author/'verify.py'),'--fixture',str(td/'absent.json')],unrelated)
            need(p.returncode==1 and p.stderr.startswith(b'REJECT: ') and not p.stdout,'missing fixture not explicit rejection')
            rejection.append({'case':'missing_fixture','mode':'optimized' if mode else 'normal','exit_code':p.returncode,'stderr_prefix':'REJECT:'})
        independent=td/'independent_check.py';independent.write_bytes(ib)
        for mode in [[],['-O']]:
            p=call(mode+[str(independent)],unrelated)
            need(p.returncode==0 and p.stdout==expected_i and not p.stderr,'independent replay mismatch')
        results.update(author_runs=runs,negative_cli_results=rejection,negative_cli_count=len(rejection),
          independent_normal_optimized_relocated_match=True,finite_case_count=16384,
          status='PASS_FULL_PACKAGE_AUDIT_REPLAY',scope='Positive unweighted Fano diagnostic; KP-3.53 unresolved')
    print(json.dumps(results,indent=2,sort_keys=True))
if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,TypeError,zipfile.BadZipFile,subprocess.TimeoutExpired) as exc:
        print('REJECT: '+str(exc),file=sys.stderr);sys.exit(1)
