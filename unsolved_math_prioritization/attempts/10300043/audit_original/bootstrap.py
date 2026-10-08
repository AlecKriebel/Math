#!/usr/bin/env python3
"""Authenticate this launcher externally first. This is an audit integrity gate."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

MANIFEST_SHA256 = '63da4944baf6b34043972ea0b9cda30692890fba65be2973c22c5c0ed2638476'

def need(ok, message):
    if not ok: raise ValueError(message)

def pairs(items):
    d = {}
    for k,v in items:
        need(k not in d, 'duplicate JSON key');d[k]=v
    return d

def no_constant(c): raise ValueError('nonfinite JSON constant')

def load(p):
    return json.loads(p.read_text(),object_pairs_hook=pairs,parse_constant=no_constant)

def pin(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def inventory(root):
    files=set();dirs=set()
    for base,dd,ff in os.walk(root,followlinks=False):
        for name in dd+ff:
            p=Path(base)/name;mode=p.lstat().st_mode;r=p.relative_to(root).as_posix()
            need(not stat.S_ISLNK(mode),'symlink member')
            if stat.S_ISDIR(mode):dirs.add(r)
            elif stat.S_ISREG(mode):files.add(r)
            else:raise ValueError('nonregular member')
    return files,dirs

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    ap.add_argument('--author-freeze',type=Path)
    a=ap.parse_args();need(not a.root.is_symlink(),'root symlink');root=a.root.resolve()
    files,dirs=inventory(root);need(dirs=={'payload'},'directory inventory')
    need(pin(root/'bootstrap.py')==pin(Path(__file__).resolve()),'launcher mismatch')
    need(pin(root/'MANIFEST.json')['sha256']==MANIFEST_SHA256,'manifest pin')
    m=load(root/'MANIFEST.json')
    need(set(m)=={'schema','problem_id','files'} and m['schema']=='short-geodesics-independent-audit-manifest-v1','manifest schema')
    need(type(m['problem_id']) is int and m['problem_id']==10300043,'manifest identity')
    need(files==set(m['files'])|{'MANIFEST.json','bootstrap.py'},'file inventory')
    for rel,want in m['files'].items():
        p=Path(rel);need(len(p.parts)==2 and p.parts[0]=='payload' and '..' not in p.parts,'unsafe path')
        need(pin(root/rel)==want,'payload pin: '+rel)
    accept=load(root/'payload/ACCEPTANCE.json')
    need(accept['disposition']=='ACCEPT_UNCHANGED_SCOPED_PARTIALS' and accept['status']=='unsolved','acceptance scope')
    for k in ['correction_required','universal_isotopy_solution','universal_homotopy_solution','geodesic_counterexample','formal_verification','original_otal_proof_certified']:
        need(accept[k] is False,'unsupported acceptance: '+k)
    runs=[load(root/('payload/INDEPENDENT_'+mode+'.json')) for mode in ['NORMAL','O','OO']]
    need(runs[0]==runs[1]==runs[2],'optimization result disagreement')
    r=runs[0]
    need(r['status']=='PASS_INDEPENDENT_AUDIT_CONTROLS' and r['independent_case_count']==len(r['cases'])==111,'independent controls')
    need(r['effective_uid']==1000 and r['actual_freeze_denied_file_write_probes']==13 and r['actual_freeze_denied_directory_create_probes']==2,'read-only evidence')
    need(r['original_freeze_unchanged'] is True and r['mathematical_proof_machine_verified'] is False,'test scope')
    author=load(root/'payload/AUTHOR_CONTROLS_REPLAY.json')
    need(author['status']=='PASS_FREEZE_CONTROLS' and author['case_count']==84 and all(c['pass'] is True for c in author['cases']),'author controls')
    original_match=None
    if a.author_freeze is not None:
        need(not a.author_freeze.is_symlink(),'author root symlink');original=a.author_freeze.resolve()
        af,ad=inventory(original);need(ad=={'packet'},'author directories')
        for rel,key in [('packet/PROOF.md','author_proof'),('MANIFEST.json','author_manifest'),('bootstrap.py','author_bootstrap')]:
            need(pin(original/rel)==accept[key],'original external pin')
        am=load(original/'MANIFEST.json')
        need(af==set(am['files'])|{'MANIFEST.json','bootstrap.py'},'author inventory')
        for rel,want in am['files'].items():need(pin(original/rel)==want,'author payload pin')
        original_match=True
    print(json.dumps({'status':'PASS_AUTHENTICATED_SCOPED_AUDIT','problem_id':10300043,
                      'manifest_sha256':MANIFEST_SHA256,'authenticated_payload_files':len(m['files']),
                      'disposition':accept['disposition'],'original_author_freeze_match':original_match,
                      'stored_independent_cases':111,'stored_author_cases':84,
                      'full_tests_rerun_by_this_gate':False,'formal_verification':False},sort_keys=True))

if __name__=='__main__':
    try:main()
    except (ValueError,TypeError,KeyError,UnicodeError,OSError) as e:
        print('FAIL: '+str(e),file=sys.stderr);sys.exit(2)
