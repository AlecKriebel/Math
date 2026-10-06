#!/usr/bin/env python3
"""External pinned gate for second-review payload; no archive imports before validation."""
import ast
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tempfile
import zipfile

MANIFEST_SHA256 = '6a919c2af4dc6b4e967b8a546287aa363883353a9efc0ae90bb0abc9bd30470c'

def need(ok, text):
    if not ok:
        raise RuntimeError(text)

def unique(pairs):
    result = {}
    for k,v in pairs:
        need(k not in result, 'duplicate JSON key')
        result[k] = v
    return result

def file_bytes(p):
    need(p.is_file() and not p.is_symlink(), 'regular nonsymlink input required')
    return p.read_bytes()

def main():
    need(sys.flags.isolated == 1, 'isolated execution required')
    need(sys.flags.no_site == 1, 'site initialization must be disabled')
    need(sys.flags.dont_write_bytecode == 1, 'bytecode writes must be disabled')
    need(sys.flags.optimize == 0, 'optimized execution rejected')
    need(len(sys.argv) == 3, 'usage: python -I -S -B bootstrap.py SAFE.zip MANIFEST.json')
    archive,manifest = map(Path,sys.argv[1:])
    mb=file_bytes(manifest)
    need(hashlib.sha256(mb).hexdigest()==MANIFEST_SHA256, 'external manifest mismatch')
    m=json.loads(mb,object_pairs_hook=unique)
    data=file_bytes(archive)
    need(len(data)==m['archive']['bytes'], 'archive size mismatch')
    need(hashlib.sha256(data).hexdigest()==m['archive']['sha256'], 'archive hash mismatch')
    payload={}
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        infos=z.infolist();names=[i.filename for i in infos]
        need(len(set(names))==len(names), 'duplicate member')
        need(set(names)==set(m['members']), 'inventory mismatch')
        for i in infos:
            n=i.filename; p=PurePosixPath(n)
            need(not p.is_absolute() and p.parts and all(x not in ('.','..','') for x in p.parts)
                 and '\\' not in n and str(p)==n, 'unsafe path')
            need(not i.is_dir() and stat.S_ISREG(i.external_attr>>16), 'nonregular member')
            e=m['members'][n];b=z.read(i)
            need(i.file_size==e['bytes'] and len(b)==e['bytes'], 'member size mismatch')
            need(hashlib.sha256(b).hexdigest()==e['sha256'], 'member hash mismatch')
            payload[n]=b
    for n,b in payload.items():
        if n.endswith('.py'):ast.parse(b,filename=n)
    with tempfile.TemporaryDirectory(prefix='higher-koszul-second-review-') as temp:
        td=Path(temp)
        for n,b in payload.items():
            p=td/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);p.chmod(0o444)
        r=subprocess.run([sys.executable,'-I','-S','-B',str(td/'independent_check.py')],cwd=td,
                         stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                         timeout=120,check=False)
        need(r.returncode==0, 'independent checker failed: '+r.stderr.decode())
        need(r.stdout==payload['INDEPENDENT_RESULTS.json'], 'frozen independent results mismatch')
    print(json.dumps({'status':'PASS','archive_sha256':m['archive']['sha256'],
                      'manifest_sha256':MANIFEST_SHA256,'members_verified':len(payload),
                      'all_members_verified_before_payload_execution':True,
                      'child_flags':['-I','-S','-B'],'optimization_rejected':True,
                      'independent_results_byte_exact':True,
                      'mathematical_proof_replaced_by_computation':False,
                      'source_inspection_performed_by_replay':False},sort_keys=True,indent=2))

if __name__=='__main__':main()
