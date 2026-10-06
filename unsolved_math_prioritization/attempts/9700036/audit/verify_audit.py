#!/usr/bin/env python3
"""Verify externally pinned audit bytes and replay finite diagnostic programs."""
import argparse,hashlib,json,pathlib,re,subprocess,sys,zipfile

def need(ok,msg):
    if not ok:raise ValueError(msg)

def read_bound(path,record):
    need(path.is_file() and not path.is_symlink(),'nonregular file: '+path.name)
    b=path.read_bytes();need(len(b)==record['bytes'],'byte count: '+path.name)
    need(hashlib.sha256(b).hexdigest()==record['sha256'],'SHA-256: '+path.name)
    return b

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--manifest-sha',required=True)
    ap.add_argument('--catalog',type=pathlib.Path)
    ap.add_argument('--problems',type=pathlib.Path)
    ap.add_argument('--reports',type=pathlib.Path)
    ap.add_argument('--sources-dir',type=pathlib.Path)
    ap.add_argument('--author-zip',type=pathlib.Path)
    ap.add_argument('--clarified-zip',type=pathlib.Path)
    a=ap.parse_args();root=pathlib.Path(__file__).absolute().parent
    need(re.fullmatch('[0-9a-f]{64}',a.manifest_sha) is not None,'manifest pin format')
    mp=root/'MANIFEST.json';need(mp.is_file() and not mp.is_symlink(),'manifest file')
    raw=mp.read_bytes();need(hashlib.sha256(raw).hexdigest()==a.manifest_sha,'external audit manifest pin')
    m=json.loads(raw);need(m['problem_id']==9700036,'audit identity')
    files=m['files'];wanted=set(files)|{'MANIFEST.json'};dirs=set()
    for name in files:
        p=pathlib.PurePosixPath(name);need(not p.is_absolute() and '..' not in p.parts,'unsafe member')
        dirs.update(x.as_posix() for x in p.parents if x.as_posix()!='.')
    actual=set()
    for p in root.rglob('*'):
        name=p.relative_to(root).as_posix();need(not p.is_symlink(),'symlink: '+name)
        if p.is_dir():need(name in dirs,'extra directory: '+name)
        else:need(p.is_file(),'unexpected node: '+name);actual.add(name)
    need(actual==wanted,'audit member set')
    for name,record in files.items():read_bound(root/name,record)
    accepted=json.loads((root/'ACCEPTANCE.json').read_text())
    need(accepted['claim_status']=='ACCEPTED_PRIOR_LITERATURE_RESOLUTION','acceptance status')
    need(accepted['original_search_approaches_used']==0,'approach attribution')
    need(accepted['source_proof_repair']==files['SOURCE_PROOF_REPAIR.md'],'proof repair acceptance pin')
    need(accepted['application_result']==files['accepted/RESULT.md'],'application acceptance pin')
    archives=[]
    for arg,key,folder in [(a.author_zip,'author_freeze','author'),(a.clarified_zip,'clarified_archive','accepted')]:
        if arg is None:continue
        read_bound(arg,accepted[key])
        with zipfile.ZipFile(arg) as z:
            names=z.namelist();expected={'sirsn_tree_9700036/'+p.name for p in (root/folder).iterdir()}
            need(len(names)==len(set(names)) and set(names)==expected,'archive member set')
            for name in names:need(z.read(name)==(root/folder/pathlib.PurePosixPath(name).name).read_bytes(),'archive member content')
        archives.append(key)
    options=[]
    for key in ['catalog','problems','reports','sources_dir']:
        v=getattr(a,key)
        if v is not None:options += ['--'+key.replace('_','-'),str(v.absolute())]
    py=[sys.executable,'-I','-B']+(['-O'] if sys.flags.optimize else [])
    outcomes={}
    for folder in ['author','accepted']:
        r=subprocess.run(py+[str(root/folder/'verify.py')]+options,cwd=root,text=True,capture_output=True)
        need(r.returncode==0,folder+' replay: '+r.stderr);outcomes[folder]=json.loads(r.stdout)
    r=subprocess.run(py+[str(root/'independent_checks.py')],cwd=root,text=True,capture_output=True)
    need(r.returncode==0,'independent finite checks: '+r.stderr);outcomes['independent']=json.loads(r.stdout)
    print(json.dumps({'status':'PASS','problem_id':9700036,'audit_files_bound':len(files),'archives_checked':archives,'outcomes':outcomes,'scope':'Externally pinned integrity and finite checks; mathematical assessment remains an AI audit.'},sort_keys=True))
if __name__=='__main__':
    try:main()
    except (OSError,ValueError,KeyError,TypeError,zipfile.BadZipFile) as e:
        print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
