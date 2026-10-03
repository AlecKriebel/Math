"""Bind completed literal V1 adverse evidence only after actual ROOT inspection."""
from pathlib import Path, PurePosixPath
import datetime as dt, hashlib, json, math, os, stat
H=Path(__file__).resolve().parent;A=H.parent;R=A.parents[2]
READS=[]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(o):return (json.dumps(o,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode()
def parse(b):
    def pairs(items):
        o={}
        for k,v in items:need(k not in o,'Duplicate key');o[k]=v
        return o
    def floating(v):
        f=float(v);need(math.isfinite(f),'Nonfinite');return f
    return json.loads(b,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda v:(_ for _ in ()).throw(ValueError('Nonfinite')))
def same(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b
def rel(n):
    need(type(n) is str and n and n!='.' and '\\' not in n and '\0' not in n,'Path');p=PurePosixPath(n);need(not p.is_absolute() and p.as_posix()==n and not {'.','..','.git','__pycache__'}&set(p.parts),'Canonical path');return p
def read(p,z=None,mode=None):
    p=Path(p);need(not p.is_symlink() and stat.S_ISREG(p.lstat().st_mode) and all(not d.is_symlink() for d in p.parents),'Regular input');b=p.read_bytes();m=stat.S_IMODE(p.stat().st_mode)
    if z is not None:need(type(z['bytes']) is int and z['bytes']==len(b) and z['sha256']==sha(b),'Literal bound body')
    if mode is not None:need(type(mode) is int and m==mode,'Full mode')
    READS.append({'path':str(p),'bytes':len(b),'sha256':sha(b),'full_mode':m});return b
def put(p,b):
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def reference(p):
    b=read(p);return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)}
def family(row,count=None):
    rel(row['path']);p=R/row['path'];o=parse(read(p,row,0o444));need(o['self_excluded']==[p.name] and type(o['files_count']) is int and (count is None or o['files_count']==count),'Self-only manifest')
    rows=o['files'];need(len(rows)==o['files_count'] and len({z['path'] for z in rows})==len(rows),'Rows');names={p.name};dirs=set();refs=[reference(p)]
    for z in rows:
        rel(z['path']);need(z['path'] not in names,'Self/duplicate');names.add(z['path']);q=p.parent/z['path'];read(q,z,0o444);refs.append(reference(q));dirs|={d.as_posix() for d in PurePosixPath(z['path']).parents if d.as_posix()!='.'}
    af=set();ad=set()
    for q in p.parent.rglob('*'):
        need(not q.is_symlink() and (stat.S_ISDIR(q.lstat().st_mode) or stat.S_ISREG(q.lstat().st_mode)),'Unsafe member');(ad if q.is_dir() else af).add(q.relative_to(p.parent).as_posix())
    need(af==names and ad==dirs,'Strict complete self-only topology');return o,refs
def actual_capture(path,expected_exit=0):
    p=R/rel(path);c=parse(read(p));base=p.parent;members=list(base.iterdir());need({q.name for q in members}=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'},'Actual external complete four-member capture')
    need(c['actual_execution'] is True and c['completed'] is True and type(c['exit_code']) is int and c['exit_code']==expected_exit and type(c['pid']) is int and c['pid']>0 and c['status']==('PASS' if expected_exit==0 else 'FAIL') and c['operator_unchanged'] is True,'Actual retained ROOT process outcome')
    need(dt.datetime.fromisoformat(c['started_utc'])<=dt.datetime.fromisoformat(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'Actual chronology')
    need(sha(read(base/'prelaunch_operator.py'))==c['operator_sha256'],'Actual operator source')
    for key in ['stdout','stderr']:
        need(c[key]['path']==key+'.bin','Literal full stream');read(base/c[key]['path'],c[key])
    return c,[reference(q) for q in members]
def main():
    need(__debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'Optimization')
    specification=parse(read(H/'ROOT_ADVERSE_BINDING_INPUT.json'))
    v1=specification['v1_manifest'];need(v1['sha256']=='d97fb190b4b20a2566a1415130e4b7729cb1f8377f8b823e0fd0b263a3315dab','Exact rejected V1')
    vm,refs=family(v1,166);need(same(vm,parse(read(H/'EXPECTED_REJECTED_V1_MANIFEST.json'))),'Complete V1 typed closure')
    am,ar=family(specification['closed_adverse_manifest']);refs+=ar
    adverse_parent=(R/specification['closed_adverse_manifest']['path']).parent;need(adverse_parent==A/'acceptance_source_adversary_family','Exact actually closed adverse family')
    verdict=parse(read(R/specification['closed_adverse_verdict']['path'],specification['closed_adverse_verdict'],0o444));need((R/specification['closed_adverse_verdict']['path']).parent==adverse_parent,'Adverse verdict same closed family')
    mandatory=verdict['mandatory_corrections'];need(type(mandatory) is list and mandatory and 'S1' in json.dumps(mandatory),'Actual final mandatory S1')
    need(verdict['production_imported_compiled_executed'] is False and verdict['future_acceptance_approved'] is False,'No adverse future approval')
    rootrow=specification['root_complete_adverse_inspection'];rel(rootrow['path']);rootpath=R/rootrow['path'];need(rootpath.parent==A,'Actual standalone adjacent ROOT adverse record');root=parse(read(rootpath,rootrow));refs.append(reference(rootpath))
    for key,value in specification['required_ROOT_values'].items():need(key in root and same(root[key],value),'Actual ROOT complete typed required value '+key)
    need(same(root['complete_VERDICT_object'],verdict),'ROOT personally complete adverse verdict')
    captures=[]
    for path in specification['actual_capture_paths']:
        c,cr=actual_capture(path);captures.append(c);refs+=cr
    need(len(captures)>=5,'V1 closure/readback and actual adverse closure/readback/ROOT-author captures')
    author=captures[-1];body=parse(read((R/specification['actual_capture_paths'][-1]).parent/'stdout.bin'))
    need(rootrow['sha256'] in json.dumps(body) and rootrow['path'].split('/')[-1] in json.dumps(body),'Completed actual ROOT author output binds literal root record')
    need(dt.datetime.fromisoformat(author['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'Author finished before binding')
    for path in specification.get('preserved_failure_capture_paths',[]):
        failed,fr=actual_capture(path,1);captures.append(failed);refs+=fr
    for row in specification.get('preserved_diagnosis_records',[]):
        rel(row['path']);read(R/row['path'],row);refs.append(reference(R/row['path']))
    normalized={}
    for z in refs:
        need(z['path'] not in normalized or same(z,normalized[z['path']]),'Conflicting evidence ref');normalized[z['path']]=z
    for name,raw in [('EXPECTED_REJECTED_V1_ADVERSE_MANIFEST.json',read(R/specification['closed_adverse_manifest']['path'])),('EXPECTED_REJECTED_V1_ADVERSE_VERDICT.json',read(R/specification['closed_adverse_verdict']['path'])),('EXPECTED_ROOT_REJECTED_V1_INSPECTION.json',read(rootpath))]:put(H/name,raw)
    old=read(H/'SOURCE_REPAIR_BINDINGS.json');put(H/'SOURCE_REPAIR_BINDINGS_PENDING.json',old)
    record={'schema':'pr46-acceptance-source-v2-repair-bindings/v1','status':'COMPLETED_REJECTED_V1_ADVERSE_BINDINGS','closed_adverse_binding_completed':True,'superseded_v1_manifest_sha256':v1['sha256'],'closed_adverse_manifest':specification['closed_adverse_manifest'],'closed_adverse_verdict':specification['closed_adverse_verdict'],'root_complete_adverse_inspection':rootrow,'complete_first_party_refs':sorted(normalized.values(),key=lambda z:z['path']),'future_acceptance_approved':False,'production_imported_compiled_executed':False}
    (H/'SOURCE_REPAIR_BINDINGS.json').write_bytes(enc(record));put(H/'COMPLETED_ADVERSE_BINDING_READS.json',enc({'schema':'pr46-source-v2-complete-adverse-binding-readback/v1','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'complete_input_reads':READS,'complete_actual_captures':captures,'mandatory_corrections':mandatory,'future_acceptance_approved':False,'production_imported_compiled_executed':False}))
    status=parse(read(H/'SOURCE_STATUS.json'));status.update(status='BOUND_COMPLETED_ADVERSE_PENDING_PRIVATE_CONTROLS',closed_adverse_binding_completed=True,preparation_completion_percent=65);(H/'SOURCE_STATUS.json').write_bytes(enc(status))
    print(json.dumps({'status':'PASS_ACTUAL_COMPLETED_ADVERSE_BINDINGS_ONLY','actual_pid':os.getpid(),'v1_files':166,'adverse_files':am['files_count'],'complete_first_party_refs':len(normalized),'root_record':rootrow,'future_acceptance_approved':False,'production_imported_compiled_executed':False},sort_keys=True))
if __name__=='__main__':main()
