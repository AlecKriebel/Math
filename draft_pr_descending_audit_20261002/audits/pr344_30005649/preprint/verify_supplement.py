#!/usr/bin/env python3
"""Verify the exact portable package; --full reproduces the mathematical controls."""
from pathlib import Path
import argparse, hashlib, json, os, subprocess, sys
ROOT=Path(__file__).resolve().parent
def require(condition,message):
    if not condition: raise RuntimeError(message)
def inventory():
    found={}
    for p in ROOT.rglob('*'):
        require(not p.is_symlink(),'Symlink in package')
        if p.is_file():
            data=p.read_bytes()
            found[p.relative_to(ROOT).as_posix()]=dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
    return found
def main():
    require(__debug__,'Run without optimization: preserved controls use assertions')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full',action='store_true')
    args=parser.parse_args()
    before=inventory()
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    require(set(before)==set(manifest['files'])|{'MANIFEST.json'},'Actual inventory mismatch')
    for name,pin in manifest['files'].items():
        require(not Path(name).is_absolute() and '..' not in Path(name).parts,'Unsafe path')
        require(before[name]==pin,'Payload mismatch: '+name)
    source=json.loads((ROOT/'SOURCE_IDENTITY.json').read_text())
    for name,pin in source['control_source_pins'].items():
        require(before[name]==pin,'Reviewed control source mismatch: '+name)
    commands=[('priority','priority/verify_public.py',[])]
    if args.full:
        commands.extend((name,code,[]) for name,code in [
            ('honda','controls/check_realization.py'),
            ('semilinear','controls/verify_semilinear.py'),
            ('intrinsic','controls/verify_intrinsic.py'),
            ('integral_flag','controls/check_integral_flag.py')])
    results=[]
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
    for name,code,flags in commands:
        result=subprocess.run([sys.executable,'-B',str(ROOT/code),*flags],cwd=ROOT,env=env,capture_output=True)
        require(result.returncode==0,name+' failed: '+result.stderr.decode(errors='replace'))
        require(not result.stderr,name+' emitted stderr')
        require(result.stdout==(ROOT/'expected'/(name+'.stdout')).read_bytes(),'Complete stdout mismatch: '+name)
        require(inventory()==before,name+' changed package bodies or file inventory')
        results.append(dict(name=name,exit_status=result.returncode,stdout_bytes=len(result.stdout),
                            stdout_sha256=hashlib.sha256(result.stdout).hexdigest(),complete_streams_match=True))
    print(json.dumps(dict(status='PASS',mode='full' if args.full else 'integrity',
                         payload_files=len(manifest['files']),runs=results,package_bytes_inventory_unchanged=True,
                         limitations=['Finite controls corroborate the symbolic proof; named classical classification inputs are not computationally proved.',
                                      'Hashes establish integrity relative to supplied records, not an independent priority or human-review certificate.',
                                      'Raw copyrighted sources and full private provenance are omitted; no network or installation is required.']),indent=2))
if __name__=='__main__': main()
