#!/usr/bin/env python3
"""Fail-closed flat-file manifest verifier and isolated mutation controls."""
import hashlib,json,pathlib,shutil,tempfile,sys

NAME='MANIFEST.json'
def object_pairs(pairs):
    result={}
    for key,value in pairs:
        if key in result: raise ValueError('duplicate JSON key')
        result[key]=value
    return result

def verify(root):
    root=pathlib.Path(root)
    if root.is_symlink() or not root.is_dir(): raise ValueError('root is not a regular directory')
    p=root/NAME
    if p.is_symlink() or not p.is_file(): raise ValueError('missing regular manifest')
    obj=json.loads(p.read_text(),object_pairs_hook=object_pairs)
    if set(obj)!={'schema','problem_id','status','files'} or obj['schema']!=1 or obj['problem_id']!=1929:
        raise ValueError('incorrect manifest schema')
    if obj['status']!='unresolved-author-freeze': raise ValueError('incorrect status')
    entries=obj['files']
    if not isinstance(entries,list) or not entries: raise ValueError('missing entries')
    expected=set()
    for e in entries:
        if set(e)!={'path','bytes','sha256'}: raise ValueError('incorrect entry schema')
        name=e['path']
        if not isinstance(name,str) or not name or name in ('.','..',NAME) or '/' in name or '\\' in name:
            raise ValueError('unsafe path')
        if name in expected: raise ValueError('duplicate entry')
        expected.add(name)
        if not isinstance(e['bytes'],int) or isinstance(e['bytes'],bool) or e['bytes']<0: raise ValueError('invalid size')
        if not isinstance(e['sha256'],str) or len(e['sha256'])!=64 or any(c not in '0123456789abcdef' for c in e['sha256']):
            raise ValueError('invalid hash')
    actual=set()
    for p in root.iterdir():
        if p.is_symlink() or not p.is_file(): raise ValueError('nonregular member')
        actual.add(p.name)
    if actual!=expected|{NAME}: raise ValueError('unexpected or missing member')
    for e in entries:
        p=root/e['path']; b=p.read_bytes()
        if len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['sha256']: raise ValueError('size/hash mismatch')
    return {'passed':True,'files':len(entries),'bytes':sum(e['bytes'] for e in entries)}

def self_test(root):
    verify(root); rejected=[]
    def trial(label,change):
        with tempfile.TemporaryDirectory(prefix='erdos100-manifest-') as d:
            dst=pathlib.Path(d)/'packet';shutil.copytree(root,dst);change(dst)
            try: verify(dst)
            except (ValueError,OSError,json.JSONDecodeError): rejected.append(label)
            else: raise AssertionError('mutation accepted: '+label)
    trial('altered-file',lambda p:(p/'README.md').write_bytes((p/'README.md').read_bytes()+b'!'))
    trial('missing-file',lambda p:(p/'README.md').unlink())
    trial('extra-file',lambda p:(p/'UNEXPECTED.txt').write_text('x'))
    trial('nested-directory',lambda p:(p/'nested').mkdir())
    def symlink(p):
        (p/'README.md').unlink();(p/'README.md').symlink_to('PROOFS.md')
    trial('symlink',symlink)
    def duplicate_key(p):
        t=(p/NAME).read_text();(p/NAME).write_text(t.replace('"schema": 1','"schema": 1, "schema": 1'))
    trial('duplicate-json-key',duplicate_key)
    def duplicate_entry(p):
        o=json.loads((p/NAME).read_text());o['files'].append(o['files'][0]);(p/NAME).write_text(json.dumps(o))
    trial('duplicate-entry',duplicate_entry)
    def path_escape(p):
        o=json.loads((p/NAME).read_text());o['files'][0]['path']='../escape';(p/NAME).write_text(json.dumps(o))
    trial('path-escape',path_escape)
    def wrong_hash(p):
        o=json.loads((p/NAME).read_text());o['files'][0]['sha256']='0'*64;(p/NAME).write_text(json.dumps(o))
    trial('wrong-hash',wrong_hash)
    def wrong_size(p):
        o=json.loads((p/NAME).read_text());o['files'][0]['bytes']+=1;(p/NAME).write_text(json.dumps(o))
    trial('wrong-size',wrong_size)
    return {'passed':True,'mutations_rejected':rejected,'count':len(rejected)}

if __name__=='__main__':
    root=pathlib.Path(__file__).resolve().parent
    result={'manifest':verify(root)}
    if '--self-test' in sys.argv[1:]: result['self_test']=self_test(root)
    print(json.dumps(result,sort_keys=True,indent=2))
