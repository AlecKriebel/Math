#!/usr/bin/env python3
"""Auditor-owned immutable-release binding and independent corruption controls."""
import argparse,hashlib,json,pathlib,stat,zipfile,tempfile,shutil
MANIFEST='4396be5d06045d5f619dbded61846c83008b2ea6d578a2d913273f136f691c22'
ARCHIVE='1cc570a6030395b0e4e3677d9c492cd8f0ab11402479f51053f0438d50b879eb'
def digest(data):return hashlib.sha256(data).hexdigest()
def inventory(root):
    p=root/'MANIFEST.json'
    if not stat.S_ISREG(p.lstat().st_mode):raise ValueError('manifest is not a regular file')
    data=p.read_bytes()
    if digest(data)!=MANIFEST:raise ValueError('manifest digest mismatch')
    objects=json.loads(data)['files'];names=[entry['path'] for entry in objects]
    if len(names)!=len(set(names)):raise ValueError('duplicate inventory')
    if any('/' in n or '\\' in n or n in ('','.', '..','MANIFEST.json') for n in names):raise ValueError('unsafe inventory')
    if set(x.name for x in root.iterdir())!=set(names)|{'MANIFEST.json'}:raise ValueError('nonexact directory inventory')
    out=[]
    for entry in objects:
        p=root/entry['path']
        if not stat.S_ISREG(p.lstat().st_mode):raise ValueError('nonregular member')
        data=p.read_bytes()
        if len(data)!=entry['bytes'] or digest(data)!=entry['sha256']:raise ValueError('member bytes mismatch')
        out.append(dict(entry))
    return out

def archive_check(path,root,pin=True):
    if pin and digest(path.read_bytes())!=ARCHIVE:raise ValueError('archive digest mismatch')
    expected={p.name for p in root.iterdir()}
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        if len(names)!=len(set(names)):raise ValueError('duplicate ZIP member')
        if set(names)!=expected:raise ValueError('nonexact ZIP inventory')
        for info in z.infolist():
            if info.is_dir() or '/' in info.filename or '\\' in info.filename:raise ValueError('unsafe ZIP member')
            mode=(info.external_attr>>16)&0xffff
            if mode and not stat.S_ISREG(mode):raise ValueError('nonregular ZIP member')
            if z.read(info)!=(root/info.filename).read_bytes():raise ValueError('ZIP member bytes mismatch')
    return names

def main():
    ap=argparse.ArgumentParser();ap.add_argument('author_directory',type=pathlib.Path);args=ap.parse_args()
    root=args.author_directory/'release';archive=args.author_directory/'AUTHOR_RELEASE.zip'
    entries=inventory(root);members=archive_check(archive,root);negatives=[]
    for name in ['changed_file','missing_file','extra_file','extra_directory','symlink','changed_manifest']:
        with tempfile.TemporaryDirectory() as td:
            copied=pathlib.Path(td)/'release';shutil.copytree(root,copied);p=copied/'RESULT.md'
            if name=='changed_file':p.write_bytes(p.read_bytes()+b'audit mutation')
            elif name=='missing_file':p.unlink()
            elif name=='extra_file':(copied/'unknown.txt').write_text('mutation')
            elif name=='extra_directory':(copied/'unknown').mkdir()
            elif name=='symlink':p.unlink();p.symlink_to(copied/'README.md')
            elif name=='changed_manifest':(copied/'MANIFEST.json').write_bytes((copied/'MANIFEST.json').read_bytes()+b' ')
            try:inventory(copied)
            except (ValueError,FileNotFoundError) as error:negatives.append({'mutation':name,'outcome':'REJECTED','reason':str(error)})
            else:raise RuntimeError('corruption accepted: '+name)
    zipneg=[]
    for mode in ['changed_member','extra_member','duplicate_member']:
        with tempfile.TemporaryDirectory() as td:
            path=pathlib.Path(td)/'changed.zip'
            with zipfile.ZipFile(archive) as original,zipfile.ZipFile(path,'w') as changed:
                for info in original.infolist():
                    data=original.read(info)
                    if mode=='changed_member' and info.filename=='RESULT.md':data+=b'corrupt'
                    changed.writestr(info,data)
                if mode=='extra_member':changed.writestr('extra.txt',b'extra')
                if mode=='duplicate_member':
                    import warnings
                    with warnings.catch_warnings():
                        warnings.simplefilter('ignore');changed.writestr('RESULT.md',(root/'RESULT.md').read_bytes())
            try:archive_check(path,root,pin=False)
            except ValueError as error:zipneg.append({'mutation':mode,'outcome':'REJECTED','reason':str(error)})
            else:raise RuntimeError('ZIP corruption accepted')
    # A final re-read confirms that originals were not changed by the audit.
    if inventory(root)!=entries or archive_check(archive,root)!=members:raise RuntimeError('originals changed')
    print(json.dumps({'status':'PASS_EXACT_IMMUTABLE_BINDING','problem_id':'30002129','manifest':{'bytes':(root/'MANIFEST.json').stat().st_size,'sha256':MANIFEST},'archive':{'bytes':archive.stat().st_size,'sha256':ARCHIVE},'manifest_files':entries,'archive_members':members,'archive_members_byte_identical_to_release':True,'independent_inventory_corruptions':negatives,'independent_zip_corruptions':zipneg,'originals_rechecked_unchanged':True,'trust_anchor':'Externally supplied manifest and archive SHA-256; no substituted verifier or substituted trust anchor can be authenticated by a self-contained package.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
