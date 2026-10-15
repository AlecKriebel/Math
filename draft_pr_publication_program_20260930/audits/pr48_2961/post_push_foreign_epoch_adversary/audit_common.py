"""Bounded administration for this independent adverse SOURCE family only."""
from pathlib import Path, PurePosixPath
import datetime as dt, hashlib, json, stat
F=Path(__file__).absolute().parent
R=F.parent.parents[2]
SELF='SELF_MANIFEST.json'
NAMES={'INITIAL_SCOPE.md','RESEARCH_LOG.md','private_review_controls.py','capture_private_controls.py','INPUT_OBSERVATIONS.json','PRIVATE_RESULTS.json','private_fixture/literal_source.txt','actual_private_control_capture/CAPTURE.json','actual_private_control_capture/PRELAUNCH.json','actual_private_control_capture/PRELAUNCH_SOURCE.py','actual_private_control_capture/PRELAUNCH_OPERATOR.py','actual_private_control_capture/stdout.bin','actual_private_control_capture/stderr.bin','REPORT.md','VERDICT.json','audit_common.py','close_adverse_family.py','verify_closed_adverse_family.py','READY.json'}
def need(v,m):
    if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def safe(n):
    need(type(n) is str and n and '\\' not in n and '\0' not in n,'Literal relative path')
    p=PurePosixPath(n);need(not p.is_absolute() and p.as_posix()==n and not {'.','..','.git','__pycache__'}.intersection(p.parts),'Canonical relative path');return n
def raw(p):
    s=p.lstat();need(stat.S_ISREG(s.st_mode) and all(not q.is_symlink() for q in p.parents),'Regular nonsymlink file');b=p.read_bytes();t=p.lstat();need((s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_mode)==(t.st_dev,t.st_ino,t.st_size,t.st_mtime_ns,t.st_mode),'Stable full read');return b
def parse(b):
    def pairs(items):
        d={}
        for k,v in items:need(k not in d,'Duplicate JSON key');d[k]=v
        return d
    return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
def load(p):return parse(raw(p))
def encode(v):return (json.dumps(v,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
def row(p):
    b=raw(p);return dict(path=p.relative_to(F).as_posix(),bytes=len(b),sha256=sha(b))
def topology(with_self):
    want=NAMES|({SELF} if with_self else set());files=set();dirs=set()
    need(F.is_dir() and not F.is_symlink() and all(not q.is_symlink() for q in F.parents),'Own regular family')
    for p in F.rglob('*'):
        s=p.lstat();n=p.relative_to(F).as_posix()
        if stat.S_ISREG(s.st_mode):files.add(n)
        elif stat.S_ISDIR(s.st_mode):dirs.add(n);need(stat.S_IMODE(s.st_mode)==0o755,'Own directory full0755')
        else:raise ValueError('Symlink/FIFO/device/nonregular member')
    need(files==want and dirs=={'actual_private_control_capture','private_fixture'},'Exact self-only topology, no extra empty directory')
def clock(s):
    need(type(s) is str,'UTC literal');v=dt.datetime.fromisoformat(s.replace('Z','+00:00'));need(v.tzinfo is not None and v.utcoffset()==dt.timedelta(0),'Aware UTC');return v
def own_evidence():
    verdict=load(F/'VERDICT.json');need(verdict['schema']=='pr48-post-push-epoch-independent-SOURCE-verdict/v1' and verdict['status']=='REJECT_SOURCE_ONLY' and verdict['source_ready_sha256']=='245f1af3127f1258c8262fa9ce8420286631b1f0e327c02a47de171bf2d670b1' and len(verdict['mandatory_findings'])==1 and verdict['mandatory_findings'][0]['id']=='M1' and verdict['production_executed'] is False and verdict['future_acceptance_approved'] is False,'Exact adverse verdict, no future approval')
    d=F/'actual_private_control_capture';c=load(d/'CAPTURE.json');pre=load(d/'PRELAUNCH.json');q=load(F/'PRIVATE_RESULTS.json');obs=load(F/'INPUT_OBSERVATIONS.json')
    need(c['status']=='PASS_PRIVATE_ONLY' and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']==q['actual_pid']==obs['actual_reader_pid']==1048 and type(c['exit_code']) is int and c['exit_code']==0 and c['candidate_or_production_execution'] is False,'Actual independent private child only')
    need(all(type(c[k]) is type(v) and c[k]==v for k,v in pre.items() if k!='schema'),'Whole actual prelaunch')
    need(c['argv']==['/usr/bin/python3','-B',str(F/'private_review_controls.py')] and c['cwd']==str(F),'Actual private argv/cwd')
    for k,name,live in [('source','PRELAUNCH_SOURCE.py','private_review_controls.py'),('operator','PRELAUNCH_OPERATOR.py','capture_private_controls.py')]:
        b=raw(d/name);need(b==raw(F/live) and len(b)==c[k]['bytes'] and sha(b)==c[k]['sha256'] and type(c[k]['full_mode']) is int and c[k]['full_mode']==0o644,'Complete actual captured source and dated prelaunch mode')
    for k in ['stdout','stderr']:
        b=raw(d/(k+'.bin'));need(len(b)==c[k]['bytes'] and sha(b)==c[k]['sha256'] and type(c[k]['full_mode']) is int and c[k]['full_mode']==0o644,'Full actual stream and dated observed mode')
    need(raw(d/'stderr.bin')==b'' and all(c[k] is True for k in ['source_unchanged','operator_unchanged','source_fullmode_unchanged','operator_fullmode_unchanged']),'Actual private capture predicates')
    need(clock(c['prepared_utc'])<=clock(c['started_utc'])<=clock(q['started_utc'])<=clock(q['finished_utc'])<=clock(c['finished_utc']),'True child observation interval inside actual caller interval')
    need(q['checks_count']==len(q['checks'])==37 and all(z['passed'] is True for z in q['checks']) and q['actual_candidate_imported_compiled_executed'] is False and q['actual_Git_native_remote_mutation'] is False and len(q['actual_private_chmod_counterexamples'])==3,'Only actual private counterexample checks')
    need(obs['source_only'] is True and obs['future_live_equality_claimed'] is False and len(obs['rows'])==q['input_observation_rows']==105,'105 dated first-party input observations')
    return obs
def check_observed_inputs_before_closure(obs):
    # This is a short-lived closure check of the audited ORIGINAL version, never
    # authority for repaired code. ROOT must close before altering that version.
    seen=set()
    for z in obs['rows']:
        n=safe(z['path']);need(n not in seen,'Distinct input observations');seen.add(n);p=R/n;b=raw(p)
        need(type(z['bytes']) is int and len(b)==z['bytes'] and sha(b)==z['sha256'] and type(z['full_mode']) is int and stat.S_IMODE(p.stat().st_mode)==z['full_mode'],'Audited version changed before closure; retain rejection and qualify new repair separately')
def ready(expected):
    need(sha(raw(F/'READY.json'))==expected,'ROOT supplied exact READY pin');v=load(F/'READY.json');need(v['status']=='READY_FOR_ROOT_CLOSURE_OF_REJECTED_SOURCE_AUDIT' and v['ROOT_approval'] is False and v['own_closure_executed'] is False,'No self closure or approval')
    need({z['path'] for z in v['payload_bindings_excluding_READY']}==NAMES-{'READY.json'} and len(v['payload_bindings_excluding_READY'])==len(NAMES)-1,'Exact READY payload set')
    for z in v['payload_bindings_excluding_READY']:need(row(F/safe(z['path']))==z,'Exact READY bound complete payload')
    return v
