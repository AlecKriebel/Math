#!/usr/bin/env python3
"""Pin and validate every input before executing packet code. Python -I -S required."""
import hashlib
import json
import pathlib
import subprocess
import sys
PIN = "3770f2377bd62309dc72af56862be11ad97115964d7efab36ed2014d503ada2c"
EXPECTED = {'APPROACHES.md','CLAIMS.json','MANIFEST.json','README.md','RESULT.md','SOURCES.json','verify.py'}
def need(ok,msg):
    if not ok:
        raise ValueError(msg)
def unique(pairs):
    out={}
    for k,v in pairs:
        need(k not in out,'duplicate JSON key')
        out[k]=v
    return out
def main():
    need(sys.flags.isolated == 1 and sys.flags.no_site == 1,'run with -I -S')
    need(len(sys.argv)==2,'one packet directory required')
    root=pathlib.Path(sys.argv[1]).absolute()
    need(root.is_dir() and not any(p.is_symlink() for p in [root,*root.parents]),'root symlink or missing directory')
    entries=list(root.iterdir())
    need({p.name for p in entries} == EXPECTED,'closed inventory mismatch')
    need(all(p.is_file() and not p.is_symlink() for p in entries),'nonregular member')
    raw=(root/'MANIFEST.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest()==PIN,'untrusted manifest')
    m=json.loads(raw,object_pairs_hook=unique)
    need(set(m)=={'schema','files'} and m['schema']==1,'manifest shape')
    need(set(m['files'])==EXPECTED-{'MANIFEST.json'},'manifest inventory')
    for name,rec in m['files'].items():
        need(set(rec)=={'bytes','sha256'},'metadata keys')
        raw=(root/name).read_bytes()
        need(type(rec['bytes']) is int and len(raw)==rec['bytes'],'byte count')
        need(hashlib.sha256(raw).hexdigest()==rec['sha256'],'member digest')
    # No packet code has been imported or executed before this point.
    flags=['-I','-S','-B']
    if sys.flags.optimize:
        flags.append('-O')
    child=subprocess.run([sys.executable,*flags,str(root/'verify.py')],check=False,capture_output=True,text=True)
    need(child.returncode==0,'verified checker failed')
    need(not child.stderr,'unexpected stderr')
    print(child.stdout,end='')
if __name__=='__main__':
    try:
        main()
    except (ValueError,OSError,json.JSONDecodeError) as exc:
        print('REJECT: '+str(exc),file=sys.stderr)
        sys.exit(2)
