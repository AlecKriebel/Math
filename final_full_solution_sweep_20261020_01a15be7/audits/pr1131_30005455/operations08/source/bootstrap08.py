"""Externally hash-checked, standard-library-only loader for the operations08 overlay."""
from pathlib import Path
import argparse, hashlib, json, stat, sys, types

def need(v,m):
    if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def strict(b):
    def pairs(xs):
        d={}
        for k,v in xs:
            need(k not in d,'Duplicate JSON key');d[k]=v
        return d
    return json.loads(b,object_pairs_hook=pairs)
def source_bytes(root,manifest_sha,bootstrap_sha):
    need(not root.is_symlink(),'Source directory symlink')
    raw=(root/'SOURCE_MANIFEST.json').read_bytes()
    need(sha(raw)==manifest_sha,'Operations08 source seal changed')
    pins=strict(raw);actual=set()
    for p in root.rglob('*'):
        need(not p.is_symlink(),'Source symlink')
        if p.is_dir():raise RuntimeError('Unexpected directory in closed source')
        need(stat.S_ISREG(p.stat().st_mode),'Nonregular source')
        if p.name!='SOURCE_MANIFEST.json':actual.add(p.name)
    need(actual==set(pins),'Operations08 source closure changed')
    checked={}
    for n,p in pins.items():
        need(Path(n).name==n and n not in {'','.','..'},'Unsafe source name')
        b=(root/n).read_bytes()
        need(p=={'bytes':len(b),'sha256':sha(b)},'Operations08 source payload changed: '+n)
        checked[n]=b
    need(sha(checked['bootstrap08.py'])==bootstrap_sha,'Operations08 bootstrap changed')
    return checked
def load_verified(root,manifest_sha,bootstrap_sha):
    need(sys.flags.optimize==0 and __debug__,'Optimized execution unsupported')
    need(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode,'Use Python -I -S -B')
    checked=source_bytes(root,manifest_sha,bootstrap_sha)
    freeze=strict(checked['SOURCE_FREEZE.json']);prior=root.parent.parent/'operations'
    b=(prior/'bootstrap.py').read_bytes();need(sha(b)==freeze['prior_bootstrap_sha256'],'Immutable05 bootstrap changed')
    ns={'__file__':str(prior/'bootstrap.py'),'__name__':'immutable05_checked_bootstrap'}
    exec(compile(b,str(prior/'bootstrap.py'),'exec',dont_inherit=True),ns)
    load05,_=ns['load_verified'](prior,freeze['prior_operations_manifest_sha256'],freeze['prior_bootstrap_sha256'])
    context={'source_root':root,'sources_sha256':manifest_sha,'bootstrap_sha256':bootstrap_sha,
             'freeze':freeze,'check_sources':lambda:source_bytes(root,manifest_sha,bootstrap_sha)}
    policy=types.ModuleType('checked_pr_policy08');policy.__file__=str(root/'pr_policy08.py')
    policy.__dict__['_OPS08_VERIFIED']=True
    exec(compile(checked['pr_policy08.py'],policy.__file__,'exec',dont_inherit=True),policy.__dict__)
    sheet=types.ModuleType('checked_sheet08');sheet.__file__=str(root/'sheet08.py')
    sheet.__dict__['_OPS08_VERIFIED']=True
    exec(compile(checked['sheet08.py'],sheet.__file__,'exec',dont_inherit=True),sheet.__dict__)
    module=types.ModuleType('checked_lifecycle08');module.__file__=str(root/'lifecycle08.py')
    module.__dict__.update(_OPS08_VERIFIED=True,CONTEXT=context,PR_POLICY=policy,SHEET_POLICY=sheet,LOAD05=load05)
    exec(compile(checked['lifecycle08.py'],module.__file__,'exec',dont_inherit=True),module.__dict__)
    module.install()
    return module
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bootstrap-sha256',required=True);p.add_argument('--sources-sha256',required=True)
    p.add_argument('arguments',nargs=argparse.REMAINDER);a=p.parse_args()
    root=Path(__file__).resolve().parent
    m=load_verified(root,a.sources_sha256,a.bootstrap_sha256)
    return m.main(a.arguments)
if __name__=='__main__':main()
