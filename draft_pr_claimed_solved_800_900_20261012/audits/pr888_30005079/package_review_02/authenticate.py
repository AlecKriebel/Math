"""Independent read-only authentication. Writes only the selected output."""
import argparse,ast,datetime,hashlib,io,json,stat,subprocess,zipfile
from pathlib import Path,PurePosixPath

def require(ok,why):
    if not ok: raise RuntimeError(why)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def load(p):return json.loads(p.read_bytes())
def write(p,o):p.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
def inventory(root):
    files={};dirs=set()
    for p in root.rglob('*'):
        mode=p.lstat().st_mode;n=p.relative_to(root).as_posix()
        require(not p.is_symlink(),'symlink '+n)
        if stat.S_ISDIR(mode):dirs.add(n)
        else:
            require(stat.S_ISREG(mode),'nonregular '+n);files[n]=pin(p.read_bytes())
    return files,dirs

def measured(command):
    start=now();proc=subprocess.run(command,cwd=args.repo,capture_output=True);end=now()
    row={'start_utc':start,'end_utc':end,'returncode':proc.returncode,'stdout':pin(proc.stdout),'stderr':pin(proc.stderr)}
    out['actual_git_processes'].append(row);write(args.output,out)
    return proc,row

a=argparse.ArgumentParser();a.add_argument('audit',type=Path);a.add_argument('repo',type=Path);a.add_argument('output',type=Path);args=a.parse_args()
A=args.audit;C=A/'candidate';out={'sampled_utc':now(),'actual_git_processes':[]}
anchor=A/'final_package_engineering_01/CANDIDATE_CORE_PINS.json'
require(pin(anchor.read_bytes())=={'bytes':32964,'sha256':'5321e2621183505838c7bc2dd195edf1d87791ab76673dade5b52ff50143c8ea'},'core anchor')
actual,dirs=inventory(C);expected={r['path']:{k:r[k] for k in ('bytes','sha256')} for r in load(anchor)['files']}
require(actual==expected and len(actual)==179,'exact179 core')
require(dirs=={str(p) for n in actual for p in PurePosixPath(n).parents if str(p)!='.'},'closed dirs')
out['core']={'files':179,'bytes':sum(r['bytes'] for r in actual.values()),'external_anchor':pin(anchor.read_bytes()),'all_rows':actual,'closed_regular_tree':True}
manifest=C/'CURRENT_PUBLICATION_MANIFEST.json'
require(pin(manifest.read_bytes())=={'bytes':32740,'sha256':'db1810399e605970d022afc971438561bbf4f3bca60ee93f457919d7b7a051c1'},'current anchor')
require({r['path']:{k:r[k] for k in ('bytes','sha256')} for r in load(manifest)['files']}=={n:r for n,r in actual.items() if n!=manifest.name},'current inventory')
portable,_=inventory(C/'verification');index=C/'verification/package_index.json'
require(pin(index.read_bytes())=={'bytes':26138,'sha256':'a41885c94a6a7d97ac16700256d10a29b616895b80b37db693239e59f7475480'},'index anchor')
require({r['path']:{k:r[k] for k in ('bytes','sha256')} for r in load(index)['files']}=={n:r for n,r in portable.items() if n!='package_index.json'},'inner inventory')
raw=(C/'rank-two-fano-verification.zip').read_bytes()
require(pin(raw)=={'bytes':349829,'sha256':'0d1d415108c0fede7405ef6e2704d348782121d879571d123532676ed6f8f957'},'zip anchor')
with zipfile.ZipFile(io.BytesIO(raw)) as z:
    require(z.namelist()==sorted(portable) and len(z.namelist())==len(set(z.namelist()))==150,'150 exact members')
    for i in z.infolist():
        require((i.external_attr>>16)==(stat.S_IFREG|0o644),'zip mode '+i.filename)
        require(z.read(i)==(C/'verification'/i.filename).read_bytes(),'zip payload '+i.filename)
out['portable']={'files':150,'zip':pin(raw),'member_bytes_exact':True,'index':pin(index.read_bytes())}
sm=A/'SOURCE_MANIFEST.json'
require(pin(sm.read_bytes())=={'bytes':5587,'sha256':'49a72d6bf90d3a74be69ed855c7a9cfc0f3b1d83a4e4e3ce997c0ca7c07d1cbc'},'source anchor')
source=load(sm)
for r in source['files']:
    b=(C/'verification/source'/r['path']).read_bytes();require(pin(b)=={k:r[k] for k in ('bytes','sha256')},'original '+r['path'])
    proc,receipt=measured(['git','cat-file','blob',r['git_blob']]);receipt['path']=r['path'];write(args.output,out)
    require(proc.returncode==0 and not proc.stderr and proc.stdout==b,'actual Git blob '+r['path'])
    require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob'],'blob formula')
proc,receipt=measured(['git','ls-tree','-r',source['head'],'--',source['source_prefix']]);receipt['kind']='original_tree';write(args.output,out)
require(proc.returncode==0 and not proc.stderr,'Git tree')
tree={}
for line in proc.stdout.decode().splitlines():
    left,path=line.split('\t');mode,kind,blob=left.split();require(kind=='blob','tree kind');tree[path.removeprefix(source['source_prefix'])]=(mode,blob)
require(tree=={r['path']:(r['mode'],r['git_blob']) for r in source['files']},'original tree modes')
out['originals']={'files':21,'bytes':sum(r['bytes'] for r in source['files']),'actual_git_blobs_and_tree_modes':True,'source_manifest':pin(sm.read_bytes())}
families=[]
for d in sorted((C/'verification').iterdir()):
    if not d.is_dir() or d.name in ('source','root_evidence'):continue
    manifests=list(d.glob('*MANIFEST*.json'));require(len(manifests)==1,'one envelope '+d.name);m=manifests[0]
    require((A/d.name/m.name).read_bytes()==m.read_bytes(),'external envelope '+d.name)
    rows={r['path']:{k:r[k] for k in ('bytes','sha256')} for r in load(m)['files']};f,ds=inventory(d)
    require(f==dict(rows,**{m.name:pin(m.read_bytes())}),'closed safe family '+d.name)
    for n,r in rows.items():require(pin((d/n).read_bytes())==r and (d/n).read_bytes()==(A/d.name/n).read_bytes(),'safe copy '+d.name+'/'+n)
    families.append({'name':d.name,'manifest':m.name,'envelope':pin(m.read_bytes()),'payload_count':len(rows),'external_copies_exact':True})
require(len(families)==9,'nine families');out['safe_families']=families
for n in ['note.tex','metadata.json','zenodo-deposit.json','portable.py','README.md']:require((C/n).read_bytes()==(C/'verification'/n).read_bytes(),'outer copy '+n)
require((C/'portable.py').read_bytes()==(C/'verification/publication_tools_01/portable.py').read_bytes(),'third tool')
changed=[r['path'] for r in source['files'] if (C/r['path']).read_bytes()!=(C/'verification/source'/r['path']).read_bytes()]
require(changed==['LITERATURE_AND_SCOPE.md','PUBLICATION.md','README.md','RESEARCH_LOG.md'],'four guide changes')
out['changed_original_guides']=changed;out['copies_exact']=True
out['original_checker_assert_nodes']={n:sum(isinstance(x,ast.Assert) for x in ast.walk(ast.parse((C/'verification/source'/n).read_bytes()))) for n in ['checks/verify_construction.py','audits/reviewer_b/independent_checks.py']}
out['status']='PASS';out['completed_utc']=now();write(args.output,out)
print(json.dumps({'status':'PASS','core_files':179,'zip_members':150,'original_files':21,'safe_families':9,'assert_nodes':out['original_checker_assert_nodes']}))
