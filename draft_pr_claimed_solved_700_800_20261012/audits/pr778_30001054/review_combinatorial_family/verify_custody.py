#!/usr/bin/env python3
"""Read-only portable exact recursive custody; excludes only top MANIFEST.json.

No mtimes, absolute paths, network, or adjacent inputs enter this check.
All hidden/nested files are included; symlinks/special files/empty dirs rejected.
"""
import hashlib,json,os,stat,sys
from pathlib import Path


def need(value,message):
    if not value:raise ValueError(message)


def path_ok(path):
    p=Path(path)
    return isinstance(path,str) and path!='' and not p.is_absolute() and '..' not in p.parts and p.as_posix()==path


def classify(mode):
    if stat.S_ISREG(mode):return 'file'
    if stat.S_ISDIR(mode):return 'dir'
    raise ValueError('symlink or special filesystem entry')


def snapshot(root):
    need(classify(root.lstat().st_mode)=='dir','root must be directory')
    files={};dirs=[]
    def visit(path,rel):
        for entry in sorted(os.scandir(path),key=lambda e:e.name):
            name=(rel+'/'+entry.name).lstrip('/')
            kind=classify(entry.stat(follow_symlinks=False).st_mode)
            if kind=='dir':
                dirs.append(name);visit(Path(entry.path),name)
            elif name!='MANIFEST.json':
                body=Path(entry.path).read_bytes()
                files[name]={'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}
    visit(root,'')
    for d in dirs:
        need(any(f.startswith(d+'/') for f in files),'empty directory: '+d)
    return {'files':files,'directories':sorted(dirs)}


def compare(manifest,observed):
    need(set(manifest)=={'schema','files','directories'},'manifest fields')
    need(type(manifest['schema']) is int and manifest['schema']==1,'manifest schema')
    need(all(path_ok(p) and p!='MANIFEST.json' for p in manifest['files']),'unsafe file name')
    need(all(path_ok(p) for p in manifest['directories']),'unsafe directory name')
    need(manifest['directories']==sorted(set(manifest['directories'])),'directory uniqueness')
    for p,d in manifest['files'].items():
        need(set(d)=={'bytes','sha256'} and type(d['bytes']) is int and d['bytes']>=0,'file fields')
        need(isinstance(d['sha256'],str) and len(d['sha256'])==64
             and all(c in '0123456789abcdef' for c in d['sha256']),'hash syntax')
    need(manifest['files']==observed['files'],'recursive file membership/bytes/hash mismatch')
    need(manifest['directories']==observed['directories'],'directory membership mismatch')


def selftest():
    import copy
    f={'.hidden':{'bytes':1,'sha256':'a'*64},'nested/x':{'bytes':2,'sha256':'b'*64}}
    o={'files':f,'directories':['nested']};m={'schema':1,**copy.deepcopy(o)}
    compare(m,o);cases=[]
    def reject(name,fn):
        try:fn()
        except ValueError:cases.append(name);return
        raise RuntimeError('custody negative accepted: '+name)
    for name,mutate in [
            ('missing nested',lambda q:q['files'].pop('nested/x')),
            ('extra hidden',lambda q:q['files'].update({'.extra':{'bytes':0,'sha256':'c'*64}})),
            ('changed bytes',lambda q:q['files']['.hidden'].update(bytes=2)),
            ('changed hash',lambda q:q['files']['nested/x'].update(sha256='d'*64)),
            ('extra directory',lambda q:q['directories'].append('empty'))]:
        q=copy.deepcopy(o);mutate(q);reject(name,lambda q=q:compare(m,q))
    bad=copy.deepcopy(m);bad['files']['../escape']=bad['files'].pop('.hidden')
    reject('traversal manifest',lambda:compare(bad,o))
    for name,mode in [('symlink',stat.S_IFLNK),('fifo',stat.S_IFIFO),('socket',stat.S_IFSOCK)]:
        reject(name,lambda mode=mode:classify(mode))
    return cases


if __name__=='__main__':
    if len(sys.argv)==2 and sys.argv[1]=='--selftest':
        print(json.dumps({'status':'PASS','custody_negative_controls':selftest()},sort_keys=True))
    else:
        need(len(sys.argv)==1,'usage: verify_custody.py [--selftest]')
        root=Path(__file__).absolute().parent
        manifest=json.loads((root/'MANIFEST.json').read_text())
        observed=snapshot(root);compare(manifest,observed)
        print(json.dumps({'status':'PASS','files':len(observed['files']),
                          'directories':len(observed['directories'])},sort_keys=True))
