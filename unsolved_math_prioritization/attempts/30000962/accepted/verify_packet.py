#!/usr/bin/env python3
"""Integrity/replay check. Authenticate this executable using the external receipt."""
import argparse,hashlib,json,pathlib,re,subprocess,sys,tempfile

def fail(message):raise SystemExit(message)
def pairs(pairs):
    d={}
    for k,v in pairs:
        if k in d:fail('duplicate JSON key')
        d[k]=v
    return d

def main():
    p=argparse.ArgumentParser();p.add_argument('--manifest-sha256',required=True);a=p.parse_args()
    if not re.fullmatch('[0-9a-f]{64}',a.manifest_sha256):fail('bad external manifest pin')
    root=pathlib.Path(__file__).resolve().parent
    man=root/'MANIFEST.json'
    if not man.is_file() or man.is_symlink():fail('manifest missing or symlinked')
    raw=man.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=a.manifest_sha256:fail('manifest pin mismatch')
    d=json.loads(raw,object_pairs_hook=pairs)
    if set(d)!={'schema','files'} or type(d['schema']) is not int or d['schema']!=1 or not isinstance(d['files'],dict):fail('bad manifest schema')
    listed=d['files']
    if 'MANIFEST.json' in listed or not listed:fail('invalid inventory')
    for name,meta in listed.items():
        if not isinstance(name,str) or pathlib.PurePosixPath(name).name!=name or name in ('.','..') or '/' in name or '\\' in name:fail('bad inventory name')
        if not isinstance(meta,dict) or set(meta)!={'sha256','bytes'}:fail('bad entry schema')
        if not isinstance(meta['bytes'],int) or isinstance(meta['bytes'],bool) or meta['bytes']<0:fail('bad size')
        if not isinstance(meta['sha256'],str) or not re.fullmatch('[0-9a-f]{64}',meta['sha256']):fail('bad hash')
    entries=list(root.iterdir())
    if {x.name for x in entries}!=set(listed)|{'MANIFEST.json'}:fail('inventory mismatch')
    for x in entries:
        if x.is_symlink() or not x.is_file():fail('non-regular entry')
    saved={}
    for name,meta in listed.items():
        b=(root/name).read_bytes()
        if len(b)!=meta['bytes'] or hashlib.sha256(b).hexdigest()!=meta['sha256']:fail('content mismatch: '+name)
        saved[name]=b
    required={'check_math.py','CHECK_RESULTS.json'}
    if not required<=saved.keys():fail('replay inputs absent')
    # Use the authenticated in-memory snapshot so the replay inputs cannot change
    # between integrity checking and copying to a fresh execution directory.
    with tempfile.TemporaryDirectory(prefix='knot-recursion-replay-') as td:
        loc=pathlib.Path(td);(loc/'check_math.py').write_bytes(saved['check_math.py'])
        for mode in ([],['-O']):
            result=subprocess.run([sys.executable,'-I','-S','-B',*mode,str(loc/'check_math.py')],cwd=td,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
            if result.returncode or result.stdout!=saved['CHECK_RESULTS.json']:fail('diagnostic replay failed')
    print(json.dumps({'integrity':'pass','replays':2,'files_verified':len(listed),'manifest_sha256':a.manifest_sha256},sort_keys=True))
if __name__=='__main__':main()
