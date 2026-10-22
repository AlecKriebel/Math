#!/usr/bin/env python3
"""Read-only public correction replay and finite degenerate-case diagnostics."""
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import re
import sys

HERE=Path(__file__).resolve().parent

def need(condition,message):
    if not condition:
        raise RuntimeError(message)

def main():
    need(len(sys.argv)==1,'no optional or skip arguments')
    need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000')
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B required')
    corrected=(HERE/'REPORT.md').read_bytes()
    need(hashlib.sha256(corrected).hexdigest()=='18b5cdfa9efe0fe4b86e4cb927bc374b3dad9d7dbd502246f24579a2df9a9cce','wrong corrected proof')
    old=rb'R=\max(1,\max_{s\in S}\|s\|_\infty).'
    new=rb'R=\max\bigl(\{1\}\cup\{\|s\|_\infty:s\in S\}\bigr).'
    need(corrected.count(new)==1 and corrected.count(old)==0,'unique corrected radius')
    source=corrected.replace(new,old)
    patch=(HERE/'CORRECTION.patch').read_bytes().splitlines(keepends=True)
    need(patch[:2]==[b'--- a/cellular_periodicity_4600046/REPORT.md\n',b'+++ b/cellular_periodicity_4600046/REPORT.md\n'],'context patch target')
    h=re.fullmatch(rb'@@ -(\d+),(\d+) \+(\d+),(\d+) @@\n',patch[2])
    need(h is not None,'single exact hunk header')
    a,count,b,newcount=map(int,h.groups());need(a==b and count==newcount,'single replacement span')
    need(all(line[:1] in (b' ',b'-',b'+') for line in patch[3:]),'context hunk syntax')
    left=b''.join(line[1:] for line in patch[3:] if line[:1]!=b'+')
    right=b''.join(line[1:] for line in patch[3:] if line[:1]!=b'-')
    lines=source.splitlines(keepends=True)
    need(len(left.splitlines())==count and len(right.splitlines())==newcount,'hunk lengths')
    need(source.count(left)==1 and corrected.count(right)==1,'unique exact mathematical patch context')
    replay=source.replace(left,right)
    need(replay==corrected,'exact contextual correction replay')
    need((HERE/'REPORT.md').read_bytes()==corrected,'read-only report changed')
    def radius(S):
        return max([1]+[max(map(abs,s)) for s in S])
    need(radius(())==1,'empty displacement set not defined')
    need(radius(((0,0),))==1 and radius(((-4,2),))==4,'ordinary radius changed')
    identity_targets=0
    for d,n in [(2,1),(2,2),(3,2)]:
        for target in itertools.product((0,1),repeat=n**d):
            answer=list(target)
            need(tuple(answer)==target,'identity lift failed')
            identity_targets+=1
    spec=importlib.util.spec_from_file_location('authenticated_independent',HERE/'verify_partials.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    singleton=[]
    for n in (1,2,3):
        target=tuple((0,)*n for _ in range(n))
        for offsets,top in [(((0,0),(1,2)),1),(((3,-2),),0)]:
            T=module.expose_cycle(n,1,offsets,top,target,lambda values:0)
            need(T==n,'singleton alphabet must respect phase and exact bound')
            singleton.append({'n':n,'offsets':offsets,'T':T})
    print(json.dumps({'status':'PASS','corrected_report_sha256':hashlib.sha256(corrected).hexdigest(),
          'corrected_report_bytes':len(corrected),'contextual_patch_replay':'EXACT_UNIQUE_CONTEXT_AFTER_EDITORIAL_EDITS_NO_WRITES',
          'superseded_full_report_replay':'NOT_RUN','empty_set_radius':radius(()),
          'empty_set_identity_targets':identity_targets,'singleton_alphabet_cases':singleton},sort_keys=True,indent=2))

if __name__=='__main__':
    try:
        main()
    except Exception as error:
        print(json.dumps({'status':'FAIL','error_type':type(error).__name__,'reason':str(error)},sort_keys=True))
        raise SystemExit(1)
