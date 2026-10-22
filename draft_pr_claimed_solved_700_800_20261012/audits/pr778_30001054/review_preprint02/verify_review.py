"""Read-only recursive exact custody; an external manifest digest is required."""
from pathlib import Path,PurePosixPath
import argparse,datetime,hashlib,json,os,re,stat,sys

def need(c,m):
    if not c:raise ValueError(m)

def regular(p):
    st=p.lstat();need(stat.S_ISREG(st.st_mode),'nonregular:'+str(p))
    fd=os.open(p,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0))
    try:
        a=os.fstat(fd);need((a.st_dev,a.st_ino)==(st.st_dev,st.st_ino),'changed inode')
        with os.fdopen(fd,'rb',closefd=False) as f:b=f.read()
        z=os.fstat(fd);need((a.st_size,a.st_mtime_ns)==(z.st_size,z.st_mtime_ns) and len(b)==z.st_size,'changed while reading')
        return b
    finally:os.close(fd)

def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def snapshot(root):
    need(stat.S_ISDIR(root.lstat().st_mode),'nonplain root')
    out={}
    def walk(p):
        entries=list(os.scandir(p));need(bool(entries),'emptydirectory:'+str(p))
        for e in entries:
            q=Path(e.path);mode=e.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):walk(q)
            else:
                need(stat.S_ISREG(mode),'symlink/special:'+str(q))
                n=q.relative_to(root).as_posix()
                if n!='MANIFEST.json':out[n]=identity(regular(q))
    walk(root);return out

def unique(pairs):
    out={}
    for k,v in pairs:need(k not in out,'duplicateJSONkey');out[k]=v
    return out

def verify(root,pin):
    need(type(pin) is str and re.fullmatch('[0-9a-f]{64}',pin),'externaldigestgrammar')
    root=root.absolute();raw=regular(root/'MANIFEST.json');need(identity(raw)['sha256']==pin,'externaldigestmismatch')
    def bad(x):raise ValueError('nonfiniteJSON')
    m=json.loads(raw,object_pairs_hook=unique,parse_constant=bad)
    need(type(m) is dict and set(m)=={'schema','sealed_at_utc','excluded','files'},'manifestshape')
    need(m['schema']=='review02-exact-recursive-v1' and m['excluded']==['MANIFEST.json'],'schema/exclusion')
    time=datetime.datetime.fromisoformat(m['sealed_at_utc']);need(time.utcoffset()==datetime.timedelta(0),'nonUTCseal')
    need(type(m['files']) is list and bool(m['files']),'files')
    expected={}
    for row in m['files']:
        need(type(row) is dict and set(row)=={'path','bytes','sha256'},'recordshape')
        n=row['path'];need(type(n) is str and n and n!='MANIFEST.json' and not n.startswith('/') and '\\' not in n and all(x not in ('','.','..') for x in n.split('/')) and str(PurePosixPath(n))==n,'unsafe path')
        need(n not in expected,'duplicatepath')
        need(type(row['bytes']) is int and row['bytes']>=0 and type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}',row['sha256']),'recordvalues')
        expected[n]={k:row[k] for k in ('bytes','sha256')}
    need([row['path'] for row in m['files']]==sorted(expected),'unsortedrecords')
    got=snapshot(root);need(got==expected,'inventory/contentmismatch')
    need(regular(root/'MANIFEST.json')==raw,'manifestchanged')
    return {'status':'PASS','manifest_sha256':pin,'files_excluding_manifest':len(got),'hidden_files_included':True,'excluded_only':'MANIFEST.json','mtime_independent':True,'symlinks_special_empty_dirs_rejected':True,'read_only':True}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).absolute().parent);p.add_argument('--manifest-sha256',required=True);a=p.parse_args()
    try:print(json.dumps(verify(a.root,a.manifest_sha256),sort_keys=True))
    except (OSError,ValueError,TypeError,KeyError) as e:print(json.dumps({'status':'FAIL','error':str(e)}));sys.exit(1)
