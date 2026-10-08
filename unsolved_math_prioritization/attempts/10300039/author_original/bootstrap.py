#!/usr/bin/env python3
"""Authenticate all bundle bytes before executing inner code. Trust this file externally."""
import argparse,hashlib,io,json,os,pathlib,re,stat,subprocess,sys,tempfile,zipfile
EXPECTED_MANIFEST='d179561ee1b36ae1d5fda2d8974a32ed23cd52f014fb98f08bbaf22e6b206c95'
EXPECTED_ARCHIVE='460994fabf6b31d69852a10a47e72db74590823043df6a0b0649a73c9b20ac44'

def require(x,msg):
    if not x:raise ValueError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()
def pairs(items):
    out={}
    for k,v in items:
        require(k not in out,'duplicate JSON key');out[k]=v
    return out
def constant(x):raise ValueError('nonfinite JSON constant')
def regular(p):
    s=p.lstat();require(stat.S_ISREG(s.st_mode) and not p.is_symlink(),'regular file required: '+str(p));return p.read_bytes()
def identity(b,x):
    require(type(x)is dict and set(x)=={'bytes','sha256'},'identity schema')
    require(type(x['bytes'])is int and x['bytes']>=0,'invalid size')
    require(type(x['sha256'])is str and re.fullmatch('[0-9a-f]{64}',x['sha256']) is not None,'invalid hash')
    require(len(b)==x['bytes'] and digest(b)==x['sha256'],'identity mismatch')
def authenticate(root):
    require(root.is_dir() and not root.is_symlink(),'regular bundle directory required')
    mb=regular(root/'EXTERNAL_MANIFEST.json');require(digest(mb)==EXPECTED_MANIFEST,'external manifest pin mismatch')
    m=json.loads(mb,object_pairs_hook=pairs,parse_constant=constant)
    require(type(m)is dict and set(m)=={'format','problem_id','archive','files'},'manifest schema')
    require(m['format']=='q10.1-author-v1' and type(m['problem_id'])is int and m['problem_id']==10300039,'manifest target')
    files=m['files'];require(type(files)is dict and len(files)>0,'file map')
    for n in files:require(type(n)is str and re.fullmatch('[A-Za-z0-9_.-]+',n) is not None and n not in {'.','..'},'unsafe member')
    allowed={'AUTHOR.zip','EXTERNAL_MANIFEST.json','author'}|{'author/'+n for n in files}
    actual=set()
    for p in root.rglob('*'):
        rel=p.relative_to(root).as_posix();actual.add(rel);require(not p.is_symlink(),'symlink rejected')
        require((rel=='author' and p.is_dir()) or (rel!='author' and p.is_file()),'unexpected object type')
    require(actual==allowed,'exact inventory mismatch')
    ab=regular(root/'AUTHOR.zip');identity(ab,m['archive']);require(digest(ab)==EXPECTED_ARCHIVE,'archive pin mismatch')
    verified={}
    with zipfile.ZipFile(io.BytesIO(ab)) as z:
        infos=z.infolist();require(len(infos)==len(files),'archive entry count')
        names=[i.filename for i in infos];require(len(set(names))==len(names) and set(names)==set(files),'archive exact names')
        for i in infos:
            require(not i.is_dir() and not(i.flag_bits&1),'archive type/encryption')
            mode=i.external_attr>>16;require(not stat.S_ISLNK(mode),'archive symlink')
            require(i.file_size==files[i.filename]['bytes'],'declared archive size')
            b=z.read(i);identity(b,files[i.filename]);require(regular(root/'author'/i.filename)==b,'expanded/archive mismatch');verified[i.filename]=b
    return verified

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--bundle',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent/'bundle')
    parser.add_argument('--problems',type=pathlib.Path);parser.add_argument('--reports',type=pathlib.Path);parser.add_argument('--sources',type=pathlib.Path);a=parser.parse_args()
    require((a.problems is None)==(a.reports is None),'both corpora required together')
    # Resolve user data locations before changing child working directory.
    arguments=[]
    for key in ['problems','reports','sources']:
        value=getattr(a,key)
        if value is not None:arguments.extend(['--'+key,str(value.absolute())])
    verified=authenticate(a.bundle)
    with tempfile.TemporaryDirectory(prefix='q10-verified-') as t:
        dest=pathlib.Path(t)
        for name,b in verified.items():(dest/name).write_bytes(b)
        flags=['-I','-S','-B']+(['-'+'O'*sys.flags.optimize] if sys.flags.optimize else [])
        r=subprocess.run([sys.executable,*flags,str(dest/'verify_math.py'),*arguments],cwd=dest,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120,check=False)
        require(r.returncode==0,'authenticated inner verifier rejected: '+r.stderr.decode(errors='replace'))
        got=json.loads(r.stdout,object_pairs_hook=pairs,parse_constant=constant)
        expected=json.loads(verified['CONTROL_OUTPUT.json'],object_pairs_hook=pairs,parse_constant=constant)
        if a.problems is not None:expected['corpus_binding']='full_files_and_exact_target_records_match'
        if a.sources is not None:expected['source_binding']='all_five_private_pdf_identities_match'
        require(got==expected,'inner output mismatch')
    print(json.dumps({'accepted':True,'problem_id':10300039,'archive_sha256':EXPECTED_ARCHIVE,'result':got},sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(2)
