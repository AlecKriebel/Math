"""Own closure inspection. Inspect evidence only; no candidate program execution."""
from pathlib import Path
import datetime,hashlib,json,os,stat
D=Path(__file__).absolute().parent;R=D.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def ck(c,s):
    if not c:raise AssertionError(s)
def stamp(s):
    d=datetime.datetime.fromisoformat(s.replace('Z','+00:00'));ck(d.utcoffset()==datetime.timedelta(0),'aware UTC');return d
inputs=load(D/'INDIVIDUAL_INPUTS.json');checked=0
for row in inputs['files']:
    p=R/row['path'];ck(p.is_file() and not p.is_symlink(),'foreign regular');b=p.read_bytes();ck(len(b)==row['bytes'] and sha(b)==row['sha256'],'final individual body stable');checked+=1
captures=[]
for p in sorted([*D.glob('actual_controls_*/CAPTURE.json'),*D.glob('FINAL_INSPECTION*/CAPTURE.json')]):
    c=load(p);pre=load(p.parent/'PRELAUNCH.json')
    ck(type(c['pid']) is int and c['pid']>0 and type(c['operator_pid']) is int and c['operator_pid']>0,'real PIDs')
    ck(c['completed'] is True and c['actual_execution'] is True and type(c['exit_code']) is int,'actual completion')
    ck(stamp(c['started_utc'])<=stamp(c['finished_utc']),'real ordered clocks')
    for k in pre:ck(pre[k]==c[k] or k in {'pid','actual_execution','exit_code','completed'},'prelaunch frozen prefix')
    ck(sha((p.parent/'PRELAUNCH_SOURCE.py').read_bytes())==c['source_sha256'],'exact actual source')
    ck(sha((p.parent/'PRELAUNCH_OPERATOR.py').read_bytes())==c['operator_sha256'],'exact actual operator')
    for k in ['stdout','stderr']:
        b=(p.parent/c[k]['path']).read_bytes();ck(len(b)==c[k]['bytes'] and sha(b)==c[k]['sha256'],'whole streams')
    captures.append({'path':p.relative_to(D).as_posix(),'pid':c['pid'],'exit_code':c['exit_code'],'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
result=load(D/'RESULT.json');ck(result['actual_pid']==79792 and result['full_SQL_rows']==15458 and result['own_assertions']==75769 and result['rejected_count']==51,'operative result exact')
verdict=load(D/'VERDICT.json');ck(verdict['report_sha256']==sha((D/'REPORT.md').read_bytes()),'current entire report bound')
ck('02:30:57.738129 UTC' in (D/'REPORT.md').read_text(),'correct captured finish precision')
ck((D/'INITIAL_SELF_MANIFEST_BEFORE_TIME_PRECISION_CORRECTION.json').is_file() and (D/'REPORT_BEFORE_TIME_PRECISION_CORRECTION.md').is_file(),'dated initial closure and report preserved')
for row in load(D/'SOURCE_READ_RECEIPT.json')['PDF_pins']:
    b=(D.parent/row['path']).read_bytes();ck(len(b)==row['bytes'] and sha(b)==row['sha256'],'five operative original source PDF pins')
operative=next(p for p in D.glob('actual_controls_*/CAPTURE.json') if load(p)['pid']==79792)
ck(load(operative)['exit_code']==0 and load(operative)['status']=='PASS_OWN_CONTROLS','operative actual positive')
ck(load(operative)['source_sha256']==sha((D/'independent_whole_controls.py').read_bytes()),'operative final source')
ck(json.loads((operative.parent/'stdout.bin').read_bytes())==result,'entire operative stdout=result')
ck(any(x['pid']==77312 and x['exit_code']==1 for x in captures),'failed own exclusion retained')
ck(load(D/'RESULT_FIRST_SUCCESS_METADATA_DEFECT.json')['full_SQL_rows']==4,'summary bug preserved honest')
# Actual own Git commands retain whole project-native4 streams; no raw cache.
for p in [D/'IMMUTABLE_GIT_COMMANDS_FIRST_SUCCESS.json',D/result['own_git_commands']]:
    for c in load(p):
        ck(c['actual_execution'] is True and c['completed'] is True and c['exit_code']==0 and c['argv'][0]=='git','actual readonly Git')
        for k in ['stdout','stderr']:
            q=D/c[k]['path'];b=q.read_bytes();ck(len(b)==c[k]['bytes'] and sha(b)==c[k]['sha256'],'full own Git stream')
foreign_hashes={x['sha256'] for x in inputs['files'] if x['path'].endswith(('.pdf','.png')) or ('/evidence/' in x['path'] and x['path'].endswith('.txt'))}
for p in D.rglob('*'):
    ck(not p.is_symlink(),'own no symlink')
    if p.is_file():ck(sha(p.read_bytes()) not in foreign_hashes,'no foreign primary body copied')
out={'schema':'pr44-own-final-inspection/v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_pid':os.getpid(),'individual_foreign_inputs_reverified':checked,'own_complete_captures':captures,'operative_own_child':79792,'whole_SQL_rows':15458,'raw_cache_or_primary_body_copied':False,'candidate_manifest_sha256':result['frozen_candidate_sha256'],'mandatory_corrections':[],'future_ROOT_reconciliation_approved':False}
(D/'FINAL_INSPECTION_CORRECTED_RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
