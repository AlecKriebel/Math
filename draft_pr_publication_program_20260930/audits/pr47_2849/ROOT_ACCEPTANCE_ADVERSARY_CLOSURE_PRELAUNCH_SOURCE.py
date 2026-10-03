"""ROOT-only SOURCE custody checks; no production/native/Git/index/remote operations."""
import argparse, datetime as dt, hashlib, json, math, os, stat
from pathlib import Path, PurePosixPath
H=Path(__file__).absolute().parent;R=H.parents[3];NAME='SELF_MANIFEST.json';PREP='1a10442d9962db99c608412f53fef754870bfadf24fd76e7e899112fc38ebef1'
def need(v,m):
    if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def parse(b):
    def pairs(items):
        d={}
        for k,v in items:need(k not in d,'Duplicate key');d[k]=v
        return d
    def floating(s):
        v=float(s);need(math.isfinite(v),'Finite float');return v
    return json.loads(b,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def equal(a,b):
    return type(a) is type(b) and (set(a)==set(b) and all(equal(a[k],b[k]) for k in a) if type(a) is dict else len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b)) if type(a) is list else a==b)
def name(n):
    need(type(n) is str and n and '\\' not in n and '\0' not in n,'Path type');p=PurePosixPath(n);need(not p.is_absolute() and p.as_posix()==n and n!='.' and not set(p.parts)&{'.','..','.git','__pycache__'},'Canonical safe path');return n
def raw(p):
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink source');return p.read_bytes()
def check(base,z,mode=False):
    b=raw(base/name(z['path']));need(type(z['bytes']) is int and z['bytes']>=0 and len(b)==z['bytes'] and sha(b)==z['sha256'],'Complete bound body '+z['path'])
    if mode:need(type(z['full_mode']) is int and stat.S_IMODE((base/z['path']).stat().st_mode)==z['full_mode'],'Exact external fullmode')
def clock(v):
    need(type(v) is str,'Clock type');t=dt.datetime.fromisoformat(v);need(t.tzinfo is not None and t.utcoffset()==dt.timedelta(0) and t<=dt.datetime.now(dt.timezone.utc),'Aware actual UTC');return t
def tree():
    need(H.is_dir() and not H.is_symlink(),'Owned family');files={};dirs=set()
    for p in H.rglob('*'):
        n=name(p.relative_to(H).as_posix());need(not p.is_symlink() and (p.is_file() or p.is_dir()),'No special/symlink topology')
        if p.is_file():files[n]=p
        else:dirs.add(n)
    parents={x.as_posix() for n in files for x in PurePosixPath(n).parents if x.as_posix()!='.'};need(dirs==parents,'No unbound/empty directory');return files,dirs
def external():
    b=parse(raw(H/'EXTERNAL_INPUT_BINDINGS.json'));need(b['schema']=='pr47-source-adversary-exact-external-bindings/v1' and b['preparation_manifest_sha256']==PREP and type(b['files_count']) is int and b['files_count']==len(b['files'])==3478,'Exact full external ledger')
    forbidden={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'};seen=set()
    for z in b['files']:
        need(type(z) is dict and set(z)=={'path','bytes','sha256','full_mode'} and z['path'] not in seen and z['path'] not in forbidden,'Unique fixed external, no live mutable4');check(R,z,True);seen.add(z['path'])
    p=R/'draft_pr_publication_program_20260930/audits/pr47_2849/acceptance_preparation_family/PREPARATION_MANIFEST.json';need(sha(raw(p))==PREP,'Exact preparation MF');return b

def own_capture(folder):
    cap=parse(raw(folder/'CAPTURE.json'));pre=parse(raw(folder/'PRELAUNCH.json'));need(cap['schema']=='pr47-source-adversary-real-command-capture/v1' and pre['schema']=='pr47-source-adversary-real-prelaunch/v1','Real own capture schema')
    need(type(cap['child_pid']) is int and cap['child_pid']>0 and type(cap['operator_pid']) is int and cap['operator_pid']==pre['operator_pid'] and type(cap['exit_code']) is int and cap['exit_code']==cap['expected_exit']==0 and cap['status']=='PASS_EXPECTED_EXIT','Real child/operator/exit')
    need(cap['argv']==pre['argv'] and cap['cwd']==pre['cwd']==str(R) and type(cap['argv']) is list and all(type(x) is str for x in cap['argv']),'Exact actual argv/cwd')
    need(clock(pre['created_utc'])<=clock(cap['started_utc'])<=clock(cap['finished_utc']),'Prelaunch/operator chronological containment')
    need(sha(raw(folder/'prelaunch_operator.py'))==cap['operator']['sha256']==pre['operator']['sha256']==sha(raw(H/'capture_private.py')),'Whole unchanged own operator source')
    need(cap['prelaunch']['path']==str(folder/'PRELAUNCH.json') and len(raw(folder/'PRELAUNCH.json'))==cap['prelaunch']['bytes'] and sha(raw(folder/'PRELAUNCH.json'))==cap['prelaunch']['sha256'],'Full prelaunch binding')
    names={'CAPTURE.json','PRELAUNCH.json','prelaunch_operator.py','stdout.bin','stderr.bin'}
    child=cap['child_source'];need(equal(child,pre['child_source']),'Entire actual child source row')
    if child is None:need(cap['argv'][0]=='git' and pre['source_copied_before_launch'] is False,'Read-only Git class, no invented source')
    else:
        names.add('prelaunch_child_source.py');need(pre['source_copied_before_launch'] is True and cap['argv'][:2]==['/usr/bin/python3','-B'] and cap['argv'][2]==child['path'],'Actual private Python source')
        source=Path(child['path']);need(source.parent==H and source.name in {'independent_source_controls.py','supplemental_source_models.py'},'Own private source only');need(sha(raw(folder/'prelaunch_child_source.py'))==child['sha256']==sha(raw(source)) and len(raw(source))==child['bytes'],'Full unchanged prelaunch own child body')
    need({x.name for x in folder.iterdir()}==names,'Exact five Git/six Python members')
    for ch in ['stdout','stderr']:
        z=cap[ch];need(set(z)=={'path','bytes','sha256','full_mode'} and z['path']==str(folder/(ch+'.bin')) and type(z['bytes']) is int and len(raw(folder/(ch+'.bin')))==z['bytes'] and sha(raw(folder/(ch+'.bin')))==z['sha256'],'Entire literal split stream')
    need(raw(folder/'stderr.bin')==b'','Actual successful stderr empty');return cap,pre

def semantics():
    v=parse(raw(H/'VERDICT.json'));need(v['schema']=='pr47-acceptance-source-adversary-verdict/v1' and v['verdict']=='PASS_SOURCE_ONLY_SCOPED' and v['preparation_manifest_sha256']==PREP and v['mandatory_corrections']==[],'Entire correct SOURCE disposition')
    for k in ['production_imported_compiled_executed','future_acceptance_approved','actual_PR46_predecessor_completed','own_closure_launched','full_problem_solved','novelty_claimed','priority_claimed','paper_or_new_doi_or_tracker']:need(v[k] is False,'No production/future authority')
    need(v['status']=='unsolved' and type(v['original_substantive_attempts']) is int and v['original_substantive_attempts']==1 and v['turn_limit']==5 and v['new_substantive_attempts']==v['audit_turns']==0 and sha(raw(H/'REPORT.md'))==v['report_sha256'],'Unsolved1/5/report pin')
    expected={'source_controls_v1','supplemental_models_v1','original_diff','original_diff_paths'}|{'historical_native4_'+kind+'_'+str(i) for i in range(4) for kind in ['body','tree']};root=H/'captures';need({p.name for p in root.iterdir()}==expected and len(expected)==12,'Every twelve own actual captures')
    captures={n:own_capture(root/n) for n in sorted(expected)}
    for file,folder in [('PRIVATE_CONTROL_RESULT.json','source_controls_v1'),('SUPPLEMENTAL_MODEL_RESULT.json','supplemental_models_v1')]:
        r=parse(raw(H/file));c,pre=captures[folder];need(type(r['actual_pid']) is int and r['actual_pid']==c['child_pid'] and clock(pre['created_utc'])<=clock(c['started_utc'])<=clock(r['started_utc'])<=clock(r['finished_utc'])<=clock(c['finished_utc']),'Actual child observation interval inside operator')
        need(r['production_imported_compiled_executed'] is False and r['future_acceptance_approved'] is False,'Private result only')
    r=parse(raw(H/'PRIVATE_CONTROL_RESULT.json'));need(r['actual_pid']==53258 and r['assertions']==34593 and r['actual_full_modes']==4096 and r['own_complete_unique_external_bindings']==3478,'Actual bounded primary controls')
    s=parse(raw(H/'SUPPLEMENTAL_MODEL_RESULT.json'));need(s['actual_pid']==55095 and s['read_only_actual_Git_children']==10 and s['private_ROOT22_fixture_is_actual_approval'] is False and len(s['historical_native4'])==4,'Actual bounded supplemental models')
    for i,z in enumerate(s['historical_native4']):
        b=raw(root/('historical_native4_body_'+str(i))/'stdout.bin');t=raw(root/('historical_native4_tree_'+str(i))/'stdout.bin').decode();need(len(b)==z['bytes'] and sha(b)==z['sha256'] and t==z['git_entry'] and captures['historical_native4_body_'+str(i)][0]['child_pid']==z['body_child_pid'] and captures['historical_native4_tree_'+str(i)][0]['child_pid']==z['mode_child_pid'],'Entire authenticated historical4 with actual identities')
    diff=raw(root/'original_diff/stdout.bin');need(len(diff)==59460 and sha(diff)=='17a6b488f85b54d22af865a5e0c9644b016211c3c985bd352631b46632dedc27','Actual whole diff');return v

def main():
    a=argparse.ArgumentParser();a.add_argument('--expected-report-sha256',required=True);a.add_argument('--expected-verdict-sha256',required=True);a.add_argument('--expected-bindings-sha256',required=True);a.add_argument('--expected-payload-set-sha256',required=True);o=a.parse_args()
    need(not (H/NAME).exists() and not (H/NAME).is_symlink(),'No prior closure');need(sha(raw(H/'REPORT.md'))==o.expected_report_sha256 and sha(raw(H/'VERDICT.json'))==o.expected_verdict_sha256 and sha(raw(H/'EXTERNAL_INPUT_BINDINGS.json'))==o.expected_bindings_sha256,'Explicit ROOT report/verdict/bindings pins')
    external();semantics();files,dirs=tree();need(NAME not in files,'Literal self excluded');names=sorted(files);need(sha(('\n'.join(names)+'\n').encode())==o.expected_payload_set_sha256,'Exact ROOT approved payload path set')
    payload=[]
    for n in names:b=raw(files[n]);payload.append({'path':n,'bytes':len(b),'sha256':sha(b)})
    for z in payload:check(H,z)
    again,dd=tree();need(set(again)==set(files) and dd==dirs,'Own topology stable before chmod')
    body=(json.dumps({'schema':'pr47-acceptance-source-adversary-self-only-closure/v1','status':'CLOSED_SOURCE_ONLY','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'self_excluded':[NAME],'files_count':len(payload),'files':payload,'directories':sorted(dirs),'full_permission_mode':'0444','preparation_manifest_sha256':PREP,'payload_path_set_sha256':o.expected_payload_set_sha256,'production_imported_compiled_executed':False,'future_acceptance_approved':False},sort_keys=True,indent=2)+'\n').encode()
    for p in files.values():p.chmod(0o444)
    for z in payload:check(H,z);need(stat.S_IMODE((H/z['path']).stat().st_mode)==0o444,'Own exact full444')
    stage=H/'.SELF_MANIFEST.staging'
    with stage.open('xb') as stream:stream.write(body);stream.flush();os.fsync(stream.fileno())
    stage.chmod(0o444);os.link(stage,H/NAME,follow_symlinks=False);stage.unlink();fd=os.open(H,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)
    external();semantics();closed,dd=tree();need(set(closed)==set(files)|{NAME} and dd==dirs and stat.S_IMODE((H/NAME).stat().st_mode)==0o444,'Exact final self-only444 topology')
    print(json.dumps({'status':'CLOSED_SOURCE_ONLY','actual_closing_pid':os.getpid(),'payload_files':len(payload),'relative_directories':len(dirs),'manifest_sha256':sha(raw(H/NAME)),'production_imported_compiled_executed':False,'future_acceptance_approved':False},sort_keys=True))
if __name__=='__main__':main()
