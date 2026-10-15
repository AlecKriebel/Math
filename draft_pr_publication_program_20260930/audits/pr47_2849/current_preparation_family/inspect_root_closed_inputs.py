"""Only byte-read completed genuine ROOT evidence after its closure; no approval."""
import datetime as dt, hashlib, json, os, stat
from pathlib import Path, PurePosixPath
F=Path(__file__).absolute().parent; A=F.parent; R=A.parents[2]
def require(v,m):
    if not v: raise ValueError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def raw(p):
    require(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink'); return p.read_bytes()
def row(p):
    b=raw(p); return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)}
def main():
    root=A/'root_original_actual_reproduction'; mr=row(root/'MANIFEST.json'); m=json.loads(raw(root/'MANIFEST.json'))
    require(mr['sha256']=='71109d8643eeff305b9e8200e2e7be0e62e79ad1cc7ad8a22b4456f5a108d278' and mr['bytes']==44049 and mr['full_mode']==0o444,'Final genuine ROOT closure pin')
    require(m['schema']=='pr47-root-original-complete-reproduction-self-only-closure/v1' and m['self_excluded']==['MANIFEST.json'] and len(m['files'])==m['files_count']==219,'Exact ROOT219+self')
    fs=set(); ds=set()
    for p in root.rglob('*'):
        require(not p.is_symlink(),'No symlinks')
        if p.is_file(): fs.add(p.relative_to(root).as_posix())
        else: require(p.is_dir(),'No special members'); ds.add(p.relative_to(root).as_posix())
    require(fs=={r['path'] for r in m['files']}|{'MANIFEST.json'} and len(ds)==46 and ds=={q.as_posix() for n in fs for q in PurePosixPath(n).parents if str(q)!='.'},'Exact ROOT topology46')
    rs=[]
    for r in m['files']:
        x=row(root/r['path']); require(x['bytes']==r['bytes'] and x['sha256']==r['sha256'] and x['full_mode']==0o444,'Exact closed ROOT body/mode'); rs.append(x)
    for n in ['ROOT_COMPLETE_RAW_SQL_AUDIT.json','ROOT_MATHEMATICAL_REVIEW.md']:
        require(raw(A/n)==raw(root/n),'Root top record equals closed archived record'); rs.append(row(A/n))
    external=root.parent.parent/'pr45_9900007/root_pr47_reproduction_closure_actual_capture'; es=[]
    require({p.name for p in external.iterdir()}=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'},'Actual4-member outer ROOT closure')
    cap=json.loads(raw(external/'CAPTURE.json')); require(cap['pid']==72331 and cap['completed'] is True and cap['exit_code']==0,'Real completed ROOT closure')
    for ch in ['stdout','stderr']:
        b=raw(external/cap[ch]['path']); require(len(b)==cap[ch]['bytes'] and sha(b)==cap[ch]['sha256'],'Root final closure streams')
    for p in sorted(external.iterdir()): es.append(row(p))
    result={'schema':'PR47_FIXED_COMPLETED_ROOT_EVIDENCE_v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_inspection_pid':os.getpid(),'manifest':mr,'members':rs,'directories':[{'path':n,'full_mode':stat.S_IMODE((root/n).stat().st_mode)} for n in sorted(ds)],'separate_actual_closure_members':es,'ROOT_D_closed_payload_files':219,'full_closed_D_bytes_and_modes_read':True,'ROOT_scope_or_current_acceptance_approved':False,'source_record_plain':True,'old_prior_null_not_absent_fallback':True,'production_import_compile_or_execution':False}
    with (F/'ROOT_FIXED_EVIDENCE.json').open('xb') as h: h.write((json.dumps(result,indent=2,sort_keys=True)+'\n').encode())
    print(json.dumps({'status':'PASS_FINAL_ROOT219_PLUS_SELF_FULL_READ','closed_ROOT_manifest_sha256':mr['sha256'],'production_import_compile_or_execution':False,'ROOT_approval':None}))
if __name__=='__main__': main()
