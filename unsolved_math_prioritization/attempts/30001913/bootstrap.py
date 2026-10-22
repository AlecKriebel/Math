"""Pinned publication gate: authenticate inventory and bytes before bundled code."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: require -I -S -B before any nonbuiltin import')
import hashlib,io,json,os,stat,tempfile,zipfile
from pathlib import Path,PurePosixPath
FILES={'author/APPROACHES.md', 'verify_publication.py', 'README.md', 'audit/ACCEPTANCE.json', 'audit/replay_audit.py', 'test_publication.py', 'audit/README.md', 'audit/author/HODGE_EXTREMALITY_30001913_AUTHOR_EXTERNAL_MANIFEST.json', 'archives/HODGE_EXTREMALITY_30001913_AUTHOR_SAFE_FREEZE.zip', 'audit/author/HODGE_EXTREMALITY_30001913_AUTHOR_SAFE_FREEZE.zip', 'audit/REPLAY.json', 'archives/HODGE_EXTREMALITY_30001913_INDEPENDENT_AUDIT_SAFE.zip', 'bootstrap.py', 'audit/AUDIT.md', 'author/STATUS.json', 'author/EXPECTED.json', 'author/README.md', 'author/SOURCES.json', 'manifests/HODGE_EXTREMALITY_30001913_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json', 'PUBLICATION_METADATA.json', 'author/verify.py', 'audit/author/HODGE_EXTREMALITY_30001913_AUTHOR_FREEZE_RECEIPT.json', 'PUBLICATION_MANIFEST.json', 'audit/independent_math.py', 'manifests/HODGE_EXTREMALITY_30001913_AUTHOR_EXTERNAL_MANIFEST.json', 'audit/INDEPENDENT_MATH.json', 'author/bootstrap.py', 'author/RESULTS.md', 'PUBLICATION_TEST_RESULTS.json', 'receipts/HODGE_EXTREMALITY_30001913_AUTHOR_FREEZE_RECEIPT.json', 'receipts/HODGE_EXTREMALITY_30001913_INDEPENDENT_AUDIT_RECEIPT.json', 'audit/SOURCE_VERIFICATION.json'}
DIRS={'receipts', 'author', 'audit', 'archives', 'audit/author', 'manifests'}
PINS={'archives/HODGE_EXTREMALITY_30001913_INDEPENDENT_AUDIT_SAFE.zip': {'bytes': 38412, 'sha256': '34cedf4b60ba6266817863c2b58091557e40a87eee556bf903153fde270c692d'}, 'archives/HODGE_EXTREMALITY_30001913_AUTHOR_SAFE_FREEZE.zip': {'bytes': 17107, 'sha256': '3ac226f14b1e8b9912358006e11fd0130f688d5de20eccb1dea58a8da4f6fb36'}, 'manifests/HODGE_EXTREMALITY_30001913_AUTHOR_EXTERNAL_MANIFEST.json': {'bytes': 1145, 'sha256': 'b2679cde75abcc86b8f4f19302d284d5c36c367d403abdc2ef5ca9f557573bea'}, 'manifests/HODGE_EXTREMALITY_30001913_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json': {'bytes': 1810, 'sha256': '795fac5ca5f05c946821efb5f0000743d22bdaf8cfa1205f043cf22bcf7a09a4'}, 'receipts/HODGE_EXTREMALITY_30001913_AUTHOR_FREEZE_RECEIPT.json': {'bytes': 6214, 'sha256': '5e0914ffdcc290e037e08e4aff75470677635be2297d4cde72f9138a6516f690'}, 'receipts/HODGE_EXTREMALITY_30001913_INDEPENDENT_AUDIT_RECEIPT.json': {'bytes': 2176, 'sha256': '5add10b6bca8953db89013f7748a201906dbc25e6907c5d39348dd90378b5b59'}}
ROLES={'author': {'archive': 'HODGE_EXTREMALITY_30001913_AUTHOR_SAFE_FREEZE.zip', 'manifest': 'HODGE_EXTREMALITY_30001913_AUTHOR_EXTERNAL_MANIFEST.json', 'receipt': 'HODGE_EXTREMALITY_30001913_AUTHOR_FREEZE_RECEIPT.json', 'archive_root': 'hodge_extremality_30001913', 'files': ['APPROACHES.md', 'EXPECTED.json', 'README.md', 'RESULTS.md', 'SOURCES.json', 'STATUS.json', 'bootstrap.py', 'verify.py']}, 'audit': {'archive': 'HODGE_EXTREMALITY_30001913_INDEPENDENT_AUDIT_SAFE.zip', 'manifest': 'HODGE_EXTREMALITY_30001913_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json', 'receipt': 'HODGE_EXTREMALITY_30001913_INDEPENDENT_AUDIT_RECEIPT.json', 'archive_root': 'hodge_extremality_30001913_independent_audit', 'files': ['ACCEPTANCE.json', 'AUDIT.md', 'INDEPENDENT_MATH.json', 'README.md', 'REPLAY.json', 'SOURCE_VERIFICATION.json', 'author/HODGE_EXTREMALITY_30001913_AUTHOR_EXTERNAL_MANIFEST.json', 'author/HODGE_EXTREMALITY_30001913_AUTHOR_FREEZE_RECEIPT.json', 'author/HODGE_EXTREMALITY_30001913_AUTHOR_SAFE_FREEZE.zip', 'independent_math.py', 'replay_audit.py']}}

def need(ok,message):
    if not ok:raise ValueError(message)
def digest(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
    out={}
    for k,v in pairs:need(k not in out,'duplicate JSON key');out[k]=v
    return out
def js(b):return json.loads(b,object_pairs_hook=unique)
def ordinary_path(value,directory):
    p=Path(value);need(p.is_absolute() and '..' not in p.parts,'absolute lexical path required')
    for q in p.parents:need(stat.S_ISDIR(q.lstat().st_mode),'symlink/non-directory ancestry')
    mode=p.lstat().st_mode;need(stat.S_ISDIR(mode) if directory else stat.S_ISREG(mode),'nonregular root or entrypoint')
    return p
def read_regular(p):
    st=p.lstat();need(stat.S_ISREG(st.st_mode) and st.st_nlink==1,'nonregular or hardlinked payload')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        actual=os.fstat(fd);need(stat.S_ISREG(actual.st_mode) and actual.st_nlink==1 and (actual.st_dev,actual.st_ino)==(st.st_dev,st.st_ino),'entry changed during read')
        with os.fdopen(fd,'rb',closefd=False) as stream:data=stream.read()
    finally:os.close(fd)
    return data
def snapshot(value,pin):
    root=ordinary_path(value,True);paths={};dirs=set()
    for current,ds,fs in os.walk(root,followlinks=False):
        for name in ds+fs:
            p=Path(current)/name;rel=p.relative_to(root).as_posix();mode=p.lstat().st_mode
            if stat.S_ISDIR(mode):dirs.add(rel)
            else:need(stat.S_ISREG(mode),'nonregular payload: '+rel);paths[rel]=p
    need(dirs==DIRS and set(paths)==FILES,'strict inventory mismatch')
    data={n:read_regular(p) for n,p in paths.items()}
    need(digest(data['PUBLICATION_MANIFEST.json'])==pin,'external publication manifest pin mismatch')
    m=js(data['PUBLICATION_MANIFEST.json']);need(type(m) is dict and set(m)=={'schema','files'} and m['schema']=='hodge-extremality-publication-sha256-v1','publication schema')
    need(type(m['files']) is dict and set(m['files'])==FILES-{'PUBLICATION_MANIFEST.json'},'manifest inventory')
    for n,r in m['files'].items():
        need(type(r) is dict and set(r)=={'bytes','sha256'} and type(r['bytes']) is int,'manifest record schema')
        need(r=={'bytes':len(data[n]),'sha256':digest(data[n])},'payload hash mismatch: '+n)
    for n,r in PINS.items():need(r=={'bytes':len(data[n]),'sha256':digest(data[n])},'immutable input pin mismatch: '+n)
    for role,r in ROLES.items():
        members=js(data['manifests/'+r['manifest']])['files'];need(set(members)==set(r['files']),'frozen manifest inventory')
        with zipfile.ZipFile(io.BytesIO(data['archives/'+r['archive']])) as z:
            infos=z.infolist();need(len(infos)==len(r['files']) and set(z.namelist())=={r['archive_root']+'/'+n for n in r['files']},'archive inventory')
            for info in infos:
                p=PurePosixPath(info.filename);need(not p.is_absolute() and '..' not in p.parts and stat.S_ISREG(info.external_attr>>16) and not info.is_dir(),'archive path or type')
                n=info.filename[len(r['archive_root'])+1:];b=data[role+'/'+n]
                need(z.read(info)==b,'archive/member mismatch')
                need(members[n]=={'bytes':len(b),'sha256':digest(b)},'frozen member hash mismatch')
    return data

def main():
    ordinary_path(str(Path(__file__).absolute()),False)
    need(3<=len(sys.argv)<=4,'usage: ROOT MANIFEST_SHA [ENTRY]')
    root,pin=sys.argv[1:3];entry=sys.argv[3] if len(sys.argv)==4 else 'verify_publication.py'
    need(entry in {'verify_publication.py','test_publication.py','integrity'},'unsupported entrypoint')
    data=snapshot(root,pin)
    if entry=='integrity':print(json.dumps({'status':'PASS','files':len(data),'archives':2,'archive_members':19},sort_keys=True));return
    with tempfile.TemporaryDirectory(prefix='hodge validated snapshot ') as td:
        copied=Path(td)/'package';copied.mkdir()
        for name,b in data.items():
            p=copied/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
        sys.argv=[str(copied/entry),'--expected-manifest',pin]
        exec(compile(data[entry],str(copied/entry),'exec'),{'__name__':'__main__','__file__':str(copied/entry)})
if __name__=='__main__':
    try:main()
    except Exception as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
