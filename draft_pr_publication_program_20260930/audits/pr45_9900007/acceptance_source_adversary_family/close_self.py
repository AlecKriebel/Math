"""Close only this adversary family; no production import, compilation or execution."""
from pathlib import Path,PurePosixPath
import datetime as dt,hashlib,json,math,os,stat
H=Path(__file__).resolve().parent
PIN='867faf71a96ada5acf2a92539bfdacd3b69bd3a1a1e0cb7e37ea6a106be1958e'
def insist(x,label):
    if not x:raise ValueError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def parse(b):
    def pairs(xs):
        d={}
        for k,v in xs:
            insist(k not in d,'Duplicate JSON key');d[k]=v
        return d
    def floating(s):
        x=float(s);insist(math.isfinite(x),'Nonfinite JSON float');return x
    return json.loads(b,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda s:(_ for _ in()).throw(ValueError('Nonfinite JSON')))
def equal(x,y):
    if type(x)is not type(y):return False
    if type(x)is dict:return x.keys()==y.keys()and all(equal(x[k],y[k])for k in x)
    if type(x)is list:return len(x)==len(y)and all(equal(a,b)for a,b in zip(x,y))
    return x==y
def utc(s):
    insist(type(s)is str and s==s.strip(),'Clock string');t=dt.datetime.fromisoformat(s.replace('Z','+00:00'));insist(t.utcoffset()==dt.timedelta(0),'Aware UTC required');return t
def relative(s):
    insist(type(s)is str and s and '\\'not in s and '\0'not in s,'Relative path type');p=PurePosixPath(s);insist(not p.is_absolute()and p.as_posix()==s and not set(p.parts)&{'.','..','.git','__pycache__'},'Literal safe relative');return p
def body_ref(p):
    insist(p.is_file()and not p.is_symlink()and all(not x.is_symlink()for x in p.parents),'Real file/ancestors');b=p.read_bytes();return{'path':p.relative_to(H).as_posix(),'bytes':len(b),'sha256':sha(b)}
def captured(cp,expected):
    z=parse(cp.read_bytes());pre=parse((cp.parent/'PRELAUNCH.json').read_bytes())
    for k,v in pre.items():
        if k!='schema':insist(equal(z[k],v),'Entire retained prelaunch field')
    insist(z['actual_execution']is True and z['completed']is True and z['exit_code']==expected and type(z['exit_code'])is int,'Actual expected child outcome')
    insist(z['source_unchanged']is True and z['operator_unchanged']is True and z['production_imported_compiled_executed']is False and z['future_acceptance_approved']is False,'Source-only scope and unchanged bindings')
    insist(type(z['child_pid'])is int and z['child_pid']>0 and type(z['operator_pid'])is int and z['operator_pid']>0,'Actual child/operator PIDs')
    insist(utc(z['prepared_utc'])<=utc(z['started_utc'])<=utc(z['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'Actual ordered UTC')
    insist(sha((cp.parent/'PRELAUNCH_SOURCE.py').read_bytes())==z['source_sha256']and sha((cp.parent/'PRELAUNCH_OPERATOR.py').read_bytes())==z['operator_sha256'],'Complete prelaunch source/operator')
    insist(type(z['argv'])is list and z['argv'][1]=='-B'and z['cwd']==str(H)and z['stdin_supplied']is False and z['completed_capture_absent_before_launch']is True,'Actual full argv/cwd/launch boundary')
    for ch in ['stdout','stderr']:
        r=z[ch];insist(set(r)=={'path','bytes','sha256'}and r['path']==ch+'.bin'and type(r['bytes'])is int,'Entire stream reference');b=(cp.parent/r['path']).read_bytes();insist(len(b)==r['bytes']and sha(b)==r['sha256'],'Entire captured stream')
    return z
def main():
    insist(not (H/'SELF_MANIFEST.json').exists(),'Self manifest must be absent')
    verdict=parse((H/'VERDICT.json').read_bytes());expected={'schema':'pr45-acceptance-source-adversary-verdict/v1','verdict':'PASS_SOURCE_ONLY_SCOPED','preparation_manifest_sha256':PIN,'mandatory_corrections':[],'production_imported_compiled_executed':False,'future_acceptance_approved':False};insist(equal(verdict,expected),'Exact own required verdict schema')
    prep=H.parent/'acceptance_preparation_family/PREPARATION_MANIFEST.json';insist(sha(prep.read_bytes())==PIN,'Preparation remains exact')
    insist(len((H/'REPORT.md').read_bytes())>15000,'Complete substantive report')
    r=parse((H/'CONTROL_RESULTS.json').read_bytes());insist(r['status']=='PASS_STATIC_OWN_CONTROLS_ONLY'and r['preparation_manifest_sha256']==PIN and r['production_imported_compiled_executed']is False and r['future_acceptance_approved']is False,'Completed own healthy static result')
    bounds=parse((H/'BOUNDARY_CONTROL_RESULTS.json').read_bytes());insist(bounds['status']=='PASS_PRIVATE_HOSTILE_FIXTURES_ONLY'and len(bounds['rejected'])==21 and bounds['fixtures_are_own_inert_models_not_production_runtime_tests']is True,'Independent inert hostile fixtures only')
    inv=parse((H/'COMPLETE_READ_INVENTORY.json').read_bytes());insist(inv['foreign_bodies_copied']is False and len(inv['files'])==2469,'Identity-only full-read inventory')
    cases={'static_v1':1,'static_v2':1,'static_v3':0,'negative_boolean':1,'negative_permission':1,'negative_duplicate_json':1,'negative_path':1,'boundary_v1':0}
    insist({x.name for x in(H/'actual_runs').iterdir()}==set(cases),'Every own run retained exact')
    for label,exitcode in cases.items():
        z=captured(H/'actual_runs'/label/'CAPTURE.json',exitcode);insist(z['status']==('FAIL'if label in {'static_v1','static_v2'}else'PASS_OWN_EXPECTED_OUTCOME'),'Failed runs distinct from expected negatives')
    for cp in(H/'actual_git').rglob('CAPTURE.json'):
        z=parse(cp.read_bytes());pre=parse((cp.parent/'PRELAUNCH.json').read_bytes());insist(all(equal(z[k],v)for k,v in pre.items()),'Own Git entire prelaunch')
        insist(z['actual_execution']is True and z['completed']is True and z['exit_code']==0 and z['source_unchanged']is True and z['operator_unchanged']is True,'Own Git actual completed readonly queries');insist(z['argv'][0]=='git'and z['argv'][1]in{'rev-parse','branch','show','ls-tree'},'Only known own Git reads')
        insist(type(z['child_pid'])is int and z['child_pid']>0 and utc(z['started_utc'])<=utc(z['finished_utc']),'Own Git PID/clock')
        for key,name in [('source_sha256','PRELAUNCH_SOURCE.py'),('operator_sha256','PRELAUNCH_OPERATOR.py')]:insist(sha((cp.parent/name).read_bytes())==z[key],'Own Git full prelaunch source/operator')
        for ch in['stdout','stderr']:
            a=z[ch];p=Path(a['path']);insist(p.parent==cp.parent and p.name==ch+'.bin','Own Git fullstream path');b=p.read_bytes();insist(type(a['bytes'])is int and len(b)==a['bytes']and sha(b)==a['sha256'],'Own Git fullstream bytes')
    outside=H.parent/'acceptance_source_adversary_outer_closure_capture';insist(outside.is_dir()and not outside.is_symlink()and not(outside/'CAPTURE.json').exists(),'Outer completed capture is absent during child closure')
    insist((outside/'PRELAUNCH_SOURCE.py').read_bytes()==Path(__file__).read_bytes()and(outside/'PRELAUNCH_OPERATOR.py').read_bytes()==(H/'capture_own.py').read_bytes(),'Own actual closing source/operator prelaunch')
    names=[];actualdirs=set()
    for p in H.rglob('*'):
        n=p.relative_to(H).as_posix();relative(n);insist(not p.is_symlink()and(p.is_file()or p.is_dir()),'Own exact real topology')
        if p.is_file():
            if p.suffix=='.json':parse(p.read_bytes())
            p.chmod(0o444);insist(stat.S_IMODE(p.stat().st_mode)==0o444,'Own literal full0444');names.append(n)
        else:actualdirs.add(n)
    dirs={x.as_posix()for n in names for x in PurePosixPath(n).parents if str(x)!='.'};insist(dirs==actualdirs,'Own no undeclared empty dirs')
    files=[body_ref(H/n)for n in sorted(names)];m={'schema':'pr45-acceptance-source-adversary-self-closure/v1','status':'CLOSED_SOURCE_ONLY','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'self_excluded':['SELF_MANIFEST.json'],'files_count':len(files),'files':files,'directories':sorted(dirs),'full_permission_mode':'0444','production_imported_compiled_executed':False,'future_acceptance_approved':False}
    raw=(json.dumps(m,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    with(H/'SELF_MANIFEST.json').open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
    (H/'SELF_MANIFEST.json').chmod(0o444)
    insist({p.relative_to(H).as_posix()for p in H.rglob('*')if p.is_file()}==set(names)|{'SELF_MANIFEST.json'},'Own final sole-self exact files')
    insist({p.relative_to(H).as_posix()for p in H.rglob('*')if p.is_dir()}==dirs,'Own final exact dirs')
    for z in files:insist(body_ref(H/z['path'])==z and stat.S_IMODE((H/z['path']).stat().st_mode)==0o444,'Own closed fullbody/fullmode replay')
    insist(stat.S_IMODE((H/'SELF_MANIFEST.json').stat().st_mode)==0o444,'Own fullmode self')
    fd=os.open(H,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)
    print(json.dumps({'status':'CLOSED_SOURCE_ONLY','manifest_sha256':sha(raw),'manifest_bytes':len(raw),'files_count':len(files),'actual_child_pid':os.getpid(),'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'outer_completed_capture_exists_during_child':(outside/'CAPTURE.json').exists(),'production_imported_compiled_executed':False,'future_acceptance_approved':False},sort_keys=True))
if __name__=='__main__':main()
