"""Prepared exact operations17 launch; no authority is authored by this file.

The caller must externally hash-check this complete file before executing it.
This corrects the original-head argument in PREPARATION_PLAN.md. It does not
activate the actor or repair/replace a consumed production intention.
"""
import sys
if sys.flags.optimize or not(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):
    raise RuntimeError('Use nonoptimized Python -I -S -B; no project read allowed')
from pathlib import Path
import argparse, hashlib, re, stat

HEAD='9601e1e768c94522bc8ad105db4dfae4770bad75'
SOURCE_MANIFEST_SHA='623a85eca963527260367dd192bb0373f6a81972179633fa6f219c72a6237803'
BOOTSTRAP_SHA='5a60e8743ab5dd72e113a75f9af370974a0895bdabd8e68321d58701c947ae94'
SOURCE=Path(__file__).resolve().parent.parent/'operations17/source'
RUNTIME=SOURCE.parent/'runtime'

def need(v,m):
    if not v:raise RuntimeError(m)
def read_exact(path,digest):
    need(type(digest)is str and re.fullmatch('[a-f0-9]{64}',digest),'Exact external SHA required')
    need(not path.is_symlink()and not path.parent.is_symlink()and stat.S_ISREG(path.lstat().st_mode),'Nonregular/symlink fixed input')
    b=path.read_bytes();need(hashlib.sha256(b).hexdigest()==digest,'Externally pinned fixed input changed: '+path.name);return b
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['resume-stage','publish','verify-public','ledger'])
    p.add_argument('--clearance-sha256',required=True)
    p.add_argument('--deposit-id',type=int)
    a=p.parse_args()
    need((a.action=='resume-stage'and a.deposit_id is None)or(a.action!='resume-stage'and type(a.deposit_id)is int and a.deposit_id>0),'Exact action/ID combination required')
    need(not SOURCE.is_symlink()and not SOURCE.parent.is_symlink()and not RUNTIME.is_symlink(),'Fixed source/runtime symlink')
    # Check the original authority bytes BEFORE any project code is executed.
    read_exact(RUNTIME/'ROOT_OPERATIONAL_CLEARANCE17.json',a.clearance_sha256)
    read_exact(SOURCE/'SOURCE_MANIFEST.json',SOURCE_MANIFEST_SHA)
    raw=read_exact(SOURCE/'bootstrap17.py',BOOTSTRAP_SHA)
    argv=[str(SOURCE/'bootstrap17.py'),'--bootstrap-sha256',BOOTSTRAP_SHA,'--sources-sha256',SOURCE_MANIFEST_SHA,a.action,'--expected-pr-head',HEAD,'--clearance-sha256',a.clearance_sha256]
    if a.deposit_id is not None:argv+=['--deposit-id',str(a.deposit_id)]
    sys.argv=argv
    exec(compile(raw,str(SOURCE/'bootstrap17.py'),'exec',dont_inherit=True,optimize=0),{'__name__':'__main__','__file__':str(SOURCE/'bootstrap17.py')})
if __name__=='__main__':main()
