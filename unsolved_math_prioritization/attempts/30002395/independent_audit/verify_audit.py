#!/usr/bin/env python3
"""Verify the source-free recursive audit packet; no external writes or network.

Use --expected-sha256 with the independently retained manifest digest to anchor
identity. Without it, the command checks internal consistency only.
"""
import argparse,hashlib,json
from pathlib import Path,PurePosixPath

def sha(data):return hashlib.sha256(data).hexdigest()
def unique_object(pairs):
    d={}
    for k,v in pairs:
        if k in d:raise ValueError('duplicate JSON key')
        d[k]=v
    return d

def validate(files,expected=None):
    raw=files['MANIFEST.json']
    if expected is not None and sha(raw)!=expected:raise ValueError('manifest identity')
    m=json.loads(raw,object_pairs_hook=unique_object)
    rows=m['files'];names=[]
    for row in rows:
        name=row['path'];p=PurePosixPath(name)
        if not name or name!=p.as_posix() or p.is_absolute() or '..' in p.parts or '\\' in name or name=='MANIFEST.json':
            raise ValueError('unsafe or reserved path')
        names.append(name)
    if len(names)!=len(set(names)):raise ValueError('duplicate inventory entry')
    if set(files)!=set(names)|{'MANIFEST.json'}:raise ValueError('inventory mismatch')
    for row in rows:
        data=files[row['path']]
        if type(row['bytes']) is not int or len(data)!=row['bytes'] or sha(data)!=row['sha256']:
            raise ValueError('member mismatch: '+row['path'])
    return {'status':'PASS','verified_files':len(names),'manifest_sha256':sha(raw),'external_identity_checked':expected is not None}

def snapshot(root):
    paths=list(root.rglob('*'))
    if any(p.is_symlink() for p in paths):raise ValueError('symlink rejected')
    if any(not p.is_file() and not p.is_dir() for p in paths):raise ValueError('nonregular entry')
    return {p.relative_to(root).as_posix():p.read_bytes() for p in paths if p.is_file()}

def self_test():
    def make(rows=None):
        files={'one.txt':b'one','nested/two.txt':b'two'}
        if rows is None:rows=[{'path':n,'bytes':len(v),'sha256':sha(v)} for n,v in sorted(files.items())]
        files['MANIFEST.json']=(json.dumps({'files':rows},sort_keys=True)+'\n').encode()
        return files
    original=make();expected=sha(original['MANIFEST.json']);tests=[]
    if validate(original,expected)['verified_files']!=2:raise RuntimeError('positive case')
    tests.append('positive')
    cases={}
    x=dict(original);x['one.txt']=b'One';cases['same_size_mutation']=x
    x=dict(original);x['one.txt']+=b'!';cases['size_mutation']=x
    x=dict(original);x.pop('one.txt');cases['missing_file']=x
    x=dict(original);x['extra.txt']=b'extra';cases['unlisted_file']=x
    x=dict(original);x['MANIFEST.json']+=b' ';cases['manifest_identity_mutation']=x
    for name,x in cases.items():
        try:validate(x,expected)
        except (ValueError,KeyError):tests.append(name)
        else:raise RuntimeError('negative control accepted: '+name)
    rows=json.loads(original['MANIFEST.json'])['files']
    malformed={'duplicate_entry':rows+[rows[0]],'parent_path':[dict(rows[0],path='../one.txt'),rows[1]],'absolute_path':[dict(rows[0],path='/one.txt'),rows[1]],'reserved_manifest_path':[dict(rows[0],path='MANIFEST.json'),rows[1]],'wrong_size':[dict(rows[0],bytes=20),rows[1]],'wrong_hash':[dict(rows[0],sha256='0'*64),rows[1]],'boolean_size':[dict(rows[0],bytes=True),rows[1]]}
    for name,rs in malformed.items():
        x=make(rs)
        try:validate(x,sha(x['MANIFEST.json']))
        except (ValueError,KeyError):tests.append(name)
        else:raise RuntimeError('negative control accepted: '+name)
    return {'status':'PASS','tests':tests,'total_tests':len(tests),'scope':'Synthetic validator controls, not mathematical proof.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--expected-sha256');p.add_argument('--self-test',action='store_true');a=p.parse_args()
    result=self_test() if a.self_test else validate(snapshot(a.root),a.expected_sha256)
    print(json.dumps(result,indent=2,sort_keys=True))
