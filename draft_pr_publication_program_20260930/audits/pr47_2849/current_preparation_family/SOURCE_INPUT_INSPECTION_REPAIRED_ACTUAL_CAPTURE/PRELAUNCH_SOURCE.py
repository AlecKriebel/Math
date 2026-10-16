"""Read complete fixed first-party inputs; record honest scoped topology and hashes."""
import datetime as dt, hashlib, json, os, stat
from pathlib import Path, PurePosixPath
F=Path(__file__).absolute().parent; A=F.parent; R=A.parents[2]
def sha(b): return hashlib.sha256(b).hexdigest()
def require(v,m):
    if not v: raise ValueError(m)
def raw(p):
    require(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular file')
    return p.read_bytes()
def row(p):
    b=raw(p); return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)}
def topology(root):
    files=set(); dirs=set()
    for p in root.rglob('*'):
        require(not p.is_symlink(),'No symlinks'); n=p.relative_to(root).as_posix()
        if stat.S_ISREG(p.stat().st_mode): files.add(n)
        else: require(p.is_dir(),'No special members'); dirs.add(n)
    require(dirs=={q.as_posix() for n in files for q in PurePosixPath(n).parents if str(q)!='.'},'No empty/extra dirs')
    return files,dirs
def dump(n,o):
    with (F/n).open('xb') as h: h.write((json.dumps(o,indent=2,sort_keys=True,allow_nan=False)+'\n').encode())
def main():
    require(not (A/'reviewed_candidate').exists() and not (A/'reviewed_candidate').is_symlink(),'Candidate absent')
    groups={}; allrows={}
    def bind(p):
        x=row(p); require(x['full_mode']==0o444,'Closed full0444 required'); allrows[x['path']]=x; return x
    pm=A/'ORIGINAL_PREPARATION_MANIFEST.json'; m=json.loads(raw(pm)); require(sha(raw(pm))=='d27e4f27be1743926b89a79dbb616773127c81f01b093c4be7caa6f941cc72b6','Original manifest pin')
    require(len(m['files'])==301 and m['self_excluded']==['ORIGINAL_PREPARATION_MANIFEST.json'],'Original scoped301+self')
    scoped=set(m['authorship_root_files']); scoped_dirs=set()
    for n in m['authorship_directory_roots']:
        fs,ds=topology(A/n); scoped|={n+'/'+p for p in fs}; scoped_dirs|={n}|{n+'/'+p for p in ds}
    require(scoped=={x['path'] for x in m['files']} and len(scoped_dirs)==55,'Exact original ownership, not whole audit root')
    for x in m['files']:
        y=bind(A/x['path']); require(y['bytes']==x['bytes'] and y['sha256']==x['sha256'],'Original body')
    groups['original']={'manifest':bind(pm),'members':[allrows[(A/x['path']).relative_to(R).as_posix()] for x in m['files']], 'authorship_root_files':m['authorship_root_files'],'authorship_directory_roots':m['authorship_directory_roots'],'directories':[{'path':n,'full_mode':stat.S_IMODE((A/n).stat().st_mode)} for n in sorted(scoped_dirs)]}
    for family,count,dirs,pin in [('cover_algebra_family',143,23,'3ef0383c70a0ed8c08bd7f4a403b1e82057a9d7038a45bac45cbd3fe271814fe'),('gauge_geometry_family',71,16,'0133b0499de07f9eda83e1572d8f87ccece779065520ba439b200e5be478f79d')]:
        root=A/family; manifest=root/'SELF_MANIFEST.json'; obj=json.loads(raw(manifest)); require(sha(raw(manifest))==pin,'Math family manifest pin')
        fs,ds=topology(root); require(len(obj['files'])==count and fs=={x['path'] for x in obj['files']}|{'SELF_MANIFEST.json'} and len(ds)==dirs,'Exact math family topology')
        rows=[]
        for x in obj['files']:
            y=bind(root/x['path']); require(y['bytes']==x['bytes'] and y['sha256']==x['sha256'],'Math family body'); rows.append(y)
        groups[family]={'manifest':bind(manifest),'members':rows,'directories':[{'path':n,'full_mode':stat.S_IMODE((root/n).stat().st_mode)} for n in sorted(ds)]}
    external=[]
    for n,expected in [('original_preparation_closure_actual_capture',0),('../pr45_9900007/root_cover_algebra_closure_actual_capture',1),('../pr45_9900007/root_cover_algebra_closed_readback_actual_capture',0),('../pr45_9900007/root_gauge_geometry_verify_actual_capture',0)]:
        root=(A/n).resolve(); fs,ds=topology(root); require(not ds and len(fs)==5,'Separate actual capture5')
        cap=json.loads(raw(root/'CAPTURE.json')); require(cap['exit_code']==expected,'Real success/failure retained')
        for member in sorted(fs): external.append(bind(root/member))
    snapshot=json.loads(raw(A/'snapshot_manifest.json')); require(snapshot['original_files']==16 and len(snapshot['files'])==16,'All16 originals')
    diff=raw(A/'original_diff.patch'); require(len(diff)==59460 and sha(diff)=='17a6b488f85b54d22af865a5e0c9644b016211c3c985bd352631b46632dedc27','Whole17-path diff')
    source=json.loads(raw(A/'source_snapshot/source_record.json')); require(source['id']==2849 and 'problem' not in source,'Plain raw source')
    turns=json.loads(raw(A/'source_snapshot/turns.json')); require(type(turns) is dict and type(turns['count']) is int and turns['count']==1 and len(turns['attempts'])==1,'Object turns1/5')
    require(raw(A/'source_snapshot/prior_report.json')==b'null\n','Original literal null')
    record={'schema':'PR47_FIXED_CURRENT_SOURCE_INPUTS_v1','status':'SOURCE_ONLY_ROOT_PREREQUISITES_PENDING','groups':groups,'separate_original_and_ROOT_actual_captures':external,'complete_fixed_member_reads':list(allrows.values()),'source_first_reviews_require_global_route_and_source_correction':True,'original_scientific_count':16,'original_diff_bytes':59460,'original_diff_sha256':sha(diff),'original_turns_object_count':1,'original_prior_literal':'null\n','upstream_key_presence_attributed':'ABSENT','upstream_absence_fallback':{},'whole_audit_root_ownership_claimed':False,'production_import_compile_or_execution':False}
    dump('STATIC_INPUT_BINDINGS.json',record)
    dump('SOURCE_INPUT_INSPECTION.json',dict(schema='PR47_SOURCE_INPUT_INSPECTION_v1',utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_pid=os.getpid(),complete_fixed_reads_count=len(allrows),complete_fixed_member_reads=list(allrows.values()),groups={k:{'members':len(v['members']),'directories':len(v['directories'])} for k,v in groups.items()},production_import_compile_or_execution=False,foreign_bodies_copied=False,ROOT_approval=None))
    print(json.dumps({'status':'PASS_COMPLETE_FIRST_PARTY_FIXED_INPUTS','complete_reads':len(allrows),'production_import_compile_or_execution':False}))
if __name__=='__main__': main()
