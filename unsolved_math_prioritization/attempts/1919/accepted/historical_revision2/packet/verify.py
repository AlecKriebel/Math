#!/usr/bin/env python3
"""Strict frozen-file integrity and finite diagnostics; no theorem certification."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

EXPECTED={'REPORT.md','STATUS.json','SOURCES.json','LEDGER.json','README.md','proof_checks.py','verify.py','CORRECTION.patch','CORRECTIONS.md'}
MAX_FILE=2_000_000

def require(test,message):
    if not test:raise ValueError(message)

def pairs(items):
    d={}
    for k,v in items:
        require(k not in d,'duplicate JSON key')
        d[k]=v
    return d

def reject_constant(value):raise ValueError('nonfinite JSON constant')

def parse(raw):
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=reject_constant)

def regular(path,limit):
    info=path.lstat()
    require(stat.S_ISREG(info.st_mode) and not path.is_symlink(),'not a regular nonsymlink file')
    require(0<=info.st_size<=limit,'file size limit')
    return path.read_bytes()

def digest(raw):return hashlib.sha256(raw).hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--packet',required=True)
    parser.add_argument('--manifest',required=True)
    parser.add_argument('--manifest-sha256',required=True)
    args=parser.parse_args()
    require(sys.flags.isolated==1,'isolated Python mode required')
    root=Path(args.packet);manifest=Path(args.manifest)
    require(not root.is_symlink() and root.is_dir(),'invalid packet root')
    require(re.fullmatch('[0-9a-f]{64}',args.manifest_sha256) is not None,'invalid manifest pin')
    raw=regular(manifest,100_000)
    require(digest(raw)==args.manifest_sha256,'manifest pin mismatch')
    data=parse(raw)
    require(type(data) is dict and set(data)=={'schema','files'},'invalid manifest shape')
    require(data['schema']=='erdos-cycle-sets-packet-v1','invalid manifest schema')
    files=data['files']
    require(type(files) is dict and set(files)==EXPECTED,'unexpected manifest paths')
    require({p.name for p in root.iterdir()}==EXPECTED,'extra or missing packet files')
    for name,rec in files.items():
        require(re.fullmatch('[A-Za-z_][A-Za-z_0-9.]*',name) is not None and '..' not in name,'unsafe path')
        require(type(rec) is dict and set(rec)=={'bytes','sha256'},'invalid file record')
        require(type(rec['bytes']) is int and 0<=rec['bytes']<=MAX_FILE,'invalid byte count')
        require(type(rec['sha256']) is str and re.fullmatch('[0-9a-f]{64}',rec['sha256']) is not None,'invalid file digest')
        content=regular(root/name,MAX_FILE)
        require(len(content)==rec['bytes'] and digest(content)==rec['sha256'],'file content mismatch: '+name)
    status=parse(regular(root/'STATUS.json',100_000))
    require(type(status) is dict,'invalid status object')
    require(type(status.get('problem_id')) is int and status['problem_id']==1919,'wrong problem id')
    require(type(status.get('turns')) is int and status['turns']==5,'wrong proof-turn count')
    require(status.get('code')=='EP-84' and status.get('status')=='unsolved','wrong status scope')
    require(status.get('upper_assertion')=='already_proved_in_prior_literature' and status.get('lower_assertion')=='unresolved_here','subpart status mismatch')
    require(status.get('independent_review')=='not_yet_performed','unearned review claim')
    require(status.get('main_problem_resolved') is False and status.get('formal_certification') is False and status.get('novelty_claim') is False,'unsupported result claim')
    ledger=parse(regular(root/'LEDGER.json',100_000))
    require(type(ledger) is dict and ledger.get('schema')=='erdos-cycle-sets-ledger-v1','invalid ledger')
    require(type(ledger.get('approaches')) is list and len(ledger['approaches'])==5,'ledger approach count')
    require([r.get('turn') if type(r) is dict else None for r in ledger['approaches']]==list(range(1,6)),'ledger turn order')
    sources=parse(regular(root/'SOURCES.json',100_000))
    require(type(sources) is dict and sources.get('source_documents_included') is False,'source redistribution scope')
    flags=['-I','-B']+(['-OO'] if sys.flags.optimize==2 else ['-O'] if sys.flags.optimize==1 else [])
    out=subprocess.run([sys.executable,*flags,str(root/'proof_checks.py')],capture_output=True,text=True,timeout=30,check=False)
    require(out.returncode==0,'finite diagnostics failed')
    result=parse(out.stdout)
    require(type(result) is dict and result.get('main_problem_resolved') is False and result.get('formal_certification') is False,'finite diagnostic scope mismatch')
    require(result.get('optimize')==sys.flags.optimize,'optimization mode not propagated')
    print(json.dumps({'integrity':'pass','finite_checks':result,'uid':os.geteuid(),'optimize':sys.flags.optimize,'isolated':sys.flags.isolated,'no_formal_certification':True},sort_keys=True))

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,UnicodeError,json.JSONDecodeError,subprocess.SubprocessError) as exc:
        print('REJECT: '+str(exc),file=sys.stderr)
        sys.exit(1)
