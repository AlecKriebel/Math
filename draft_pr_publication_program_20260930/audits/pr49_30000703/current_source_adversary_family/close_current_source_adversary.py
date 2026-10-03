"""ROOT ONLY after reviewer finishes: self-only closure, no production/helper calls."""
from pathlib import Path, PurePosixPath
import argparse, datetime as dt, hashlib, json, math, os, re, stat, sys
F=Path(__file__).absolute().parent;R=Path('/Users/alec/Documents/Math');A=F.parent;S=A/'current_preparation_family';SELF='MANIFEST.json'
CAPTURES={'FIXED_INPUT_INSPECTION_ACTUAL_CAPTURE':1,'FIXED_INPUT_INSPECTION_V2_ACTUAL_CAPTURE':0,'PRIVATE_GUARD_CONTROLS_ACTUAL_CAPTURE':1,'PRIVATE_GUARD_CONTROLS_V2_ACTUAL_CAPTURE':1,'PRIVATE_GUARD_CONTROLS_V3_ACTUAL_CAPTURE':1,'PRIVATE_GUARD_CONTROLS_V4_ACTUAL_CAPTURE':0,'SCOPE_AND_LIMITS_ACTUAL_CAPTURE':0,'FINAL_REVIEW_READ_ACTUAL_CAPTURE':0}
def need(x,n):
    if not x:raise ValueError(n)
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(p):
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'regular nonsymlink');return p.read_bytes()
def load(b):
    def pairs(items):
        d={}
        for k,v in items:need(k not in d,'duplicate JSON');d[k]=v
        return d
    def number(s):
        v=float(s);need(math.isfinite(v),'finite JSON');return v
    def const(s):raise ValueError('nonfinite JSON')
    return json.loads(b,object_pairs_hook=pairs,parse_float=number,parse_constant=const)
def utc(s):
    need(type(s) is str,'UTC string');t=dt.datetime.fromisoformat(s);need(t.utcoffset()==dt.timedelta(0),'aware UTC');return t
def rel(s):
    need(type(s) is str and s and '\\' not in s and '\0' not in s,'path string');p=PurePosixPath(s);need(not p.is_absolute() and str(p)==s and s!='.' and not set(p.parts)&{'.','..','.git','__pycache__'},'canonical relative');return s
def tree():
    need(F==Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr49_30000703/current_source_adversary_family') and F.is_dir() and not F.is_symlink(),'exact self-only root');files={};dirs={'.':stat.S_IMODE(F.stat().st_mode)}
    for p in F.rglob('*'):
        need(not p.is_symlink(),'no symlink');n=rel(p.relative_to(F).as_posix());m=p.stat().st_mode
        if stat.S_ISREG(m):files[n]=p
        else:need(stat.S_ISDIR(m),'no special member');dirs[n]=stat.S_IMODE(m)
    expected={'.'}|{str(q) for n in files for q in PurePosixPath(n).parents if str(q)!='.'};need(set(dirs)==expected,'no empty/extra directories');return files,dirs
def capture_checks():
    need({p.name for p in F.glob('*_ACTUAL_CAPTURE')}==set(CAPTURES),'exact complete actual capture set');result=[]
    for n,expected in sorted(CAPTURES.items()):
        d=F/n;need({p.name for p in d.iterdir()}=={'CAPTURE.json','PRELAUNCH.json','prelaunch_operator.py','prelaunch_target.py','stdout.bin','stderr.bin'},'complete capture6');c=load(raw(d/'CAPTURE.json'));pre=load(raw(d/'PRELAUNCH.json'))
        need(c['schema']==pre['schema']=='pr49-current-source-adversary-actual-command/v1' and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==expected and c['expected_exit']==0 and c['operator_unchanged'] is True and c['target_unchanged'] is True and c['stdin_supplied'] is False and 'operator_error' not in c and c['cwd']==str(R),'real complete child including retained failed controls')
        need(c['capture_status']==('EXPECTED_ACTUAL_EXIT_COMPLETE' if expected==0 else 'UNEXPECTED_OR_INCOMPLETE_ACTUAL_EXIT'),'true retained outcome');need(type(c['operator_pid']) is int and c['operator_pid']>0 and utc(c['started_utc'])<utc(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'actual child chronology')
        need(pre['actual_execution'] is False and pre['completed'] is False and pre['pid'] is None and pre['exit_code'] is None and pre['target_unchanged'] is None,'genuine prelaunch not final receipt')
        need(all(c[k]==v for k,v in pre.items() if k not in ('actual_execution','completed','pid','exit_code','target_unchanged')),'prelaunch literal equality')
        target=c['target_source'];need(set(target)=={'path','bytes','sha256'} and type(target['bytes']) is int and target['bytes']>=0 and Path(target['path']).parent==F and c['argv']==['/usr/bin/python3','-B',target['path']],'own private source argv')
        for p in [d/'prelaunch_target.py',Path(target['path'])]:b=raw(p);need(len(b)==target['bytes'] and sha(b)==target['sha256'],'real unchanged private target')
        need(sha(raw(d/'prelaunch_operator.py'))==c['operator_sha256']==sha(raw(F/'capture_actual_command.py')),'real unchanged operator source')
        for k in ('stdout','stderr'):
            v=c[k];need(set(v)=={'path','bytes','sha256'} and v['path']==k+'.bin' and type(v['bytes']) is int and v['bytes']>=0,'exact typed split stream');b=raw(d/v['path']);need(len(b)==v['bytes'] and sha(b)==v['sha256'],'complete actual stream')
        need(c['stderr']['bytes']==0 if expected==0 else c['stderr']['bytes']>0 and c['stdout']['bytes']==0,'actual success/failure stdout/stderr')
        result.append(dict(directory=n,actual_pid=c['pid'],exit_code=expected,capture_sha256=sha(raw(d/'CAPTURE.json')),finished_utc=c['finished_utc']))
    return result
def prior_evidence():
    need(sha(raw(S/'PREPARATION_MANIFEST.json'))=='4324c2a69762752b42b159b141a629b55a6dda5351817afff12e4f2d0950e4cd','reviewed exact SOURCE remains')
    v=load(raw(F/'VERDICT.json'));need(v['verdict']=='PASS_CURRENT_SOURCE_WITH_EXPLICIT_BOUNDED_QUALIFICATIONS' and v['mandatory_corrections']==[] and v['future_acceptance_approved'] is False and v['ROOT_native_acceptance'] is False and v['production_builder_imported_compiled_executed'] is False and v['production_operator_imported_compiled_executed'] is False and v['new_whole_current_review_gate']=='PENDING','bounded own SOURCE verdict')
    need(v['original_substantive_attempts']==0 and type(v['original_substantive_attempts']) is int and v['new_substantive_attempts']==0 and v['audit_turns']==0 and v['separate_original_source_response_count'] is None,'literal counts, no invented response')
    need(v['report']['sha256']==sha(raw(F/'REPORT.md')),'complete report pin')
    result=load(raw(F/'FIXED_READ_RESULT.json'));need(result['status']=='PASS_COMPLETE_CURRENT_SOURCE_AND_FIXED_FIRST_PARTY_INSPECTION' and result['fixed_files']==1184 and result['source_files']==119 and result['future_acceptance_approved'] is False,'complete fixed read')
    for r in result['checked_body_mode_rows']:
        p=R/rel(r['path']);b=raw(p);need(type(r['bytes']) is int and type(r['full_mode']) is int and len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==r['full_mode'],'all external fixed rows remain exact')
    limits=load(raw(F/'SCOPE_AND_LIMITS_RESULT.json'));need(limits['mandatory_corrections']==[] and limits['production_imported_compiled_executed'] is False and limits['future_acceptance_approved'] is False,'scope limits preserved');r=limits['ROOT_source_closer_prelaunch'];p=R/rel(r['path']);need(len(raw(p))==r['bytes'] and sha(raw(p))==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==r['full_mode'],'real ROOT closer prelaunch bound')
    controls=load(raw(F/'PRIVATE_CONTROL_RESULT.json'));need(controls['status']=='PASS_BOUNDED_INDEPENDENT_PREDICATE_AND_MACOS_CONTROLS' and controls['cases_count']==9254 and len(controls['cases'])==9254 and controls['negative_predicates_rejected']==5103 and len(controls['actual_permission_mode_observations'])==4096 and controls['fabricated_approval_models_only_in_memory'] is True and controls['future_acceptance_approved'] is False and controls['production_imported_compiled_executed'] is False,'bounded independent controls')
    for i,r in enumerate(controls['actual_permission_mode_observations']):need(type(r['requested_full_mode']) is int and r['requested_full_mode']==i and type(r['actual_full_mode']) is int and r['actual_full_mode']==i,'every actual full mode')
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--expected-report-sha256',required=True);args=parser.parse_args();need(not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'checks enabled');need(re.fullmatch('[0-9a-f]{64}',args.expected_report_sha256) and sha(raw(F/'REPORT.md'))==args.expected_report_sha256,'ROOT exact full report SHA');need(not (F/SELF).exists() and not (F/SELF).is_symlink(),'never overwrite own manifest');files,dirs=tree();prior_evidence();caps=capture_checks()
    for p in files.values():p.chmod(0o444)
    members=[]
    for n,p in sorted(files.items()):b=raw(p);need(stat.S_IMODE(p.stat().st_mode)==292,'every own full0444');members.append(dict(path=n,bytes=len(b),sha256=sha(b),full_mode=292))
    created=dt.datetime.now(dt.timezone.utc).isoformat();need(all(utc(v['finished_utc'])<utc(created) for v in caps),'self closure after all real operations')
    m=dict(schema='pr49-current-source-adversary-self-only-closure/v1',created_utc=created,actual_closing_pid=os.getpid(),self_excluded=[SELF],files_count=len(members),files=members,directories=[dict(path=n,full_mode=v) for n,v in sorted(dirs.items())],manifest_full_mode=292,report_sha256=args.expected_report_sha256,SOURCE_verdict='PASS_CURRENT_SOURCE_WITH_EXPLICIT_BOUNDED_QUALIFICATIONS',mandatory_corrections=[],production_imported_compiled_executed=False,helpers_executed=False,reused_boundary_mathematical_context=True,did_author_current_SOURCE=False,new_blind_mathematical_review=False,future_acceptance_approved=False,new_whole_current_review_gate='PENDING',original_substantive_attempts=0,turn_limit=5,new_substantive_attempts=0,audit_turns=0,separate_original_source_response_count=None,retained_actual_captures=caps,retained_actual_failures=4,external_postexit_capture_and_separate_readback_required=True)
    data=(json.dumps(m,indent=2,allow_nan=False)+'\n').encode()
    with (F/SELF).open('xb') as h:h.write(data);h.flush();os.fsync(h.fileno())
    (F/SELF).chmod(0o444);current,cd=tree();need(set(current)==set(files)|{SELF} and cd==dirs,'exact self-only closed topology')
    for r in members:p=F/r['path'];b=raw(p);need(len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==292,'complete final closed body/modes')
    need(raw(F/SELF)==data and stat.S_IMODE((F/SELF).stat().st_mode)==292,'closed manifest bytes/mode')
    print(json.dumps(dict(status='PASS_ROOT_CURRENT_SOURCE_ADVERSARY_SELF_ONLY_CLOSURE',actual_closing_pid=os.getpid(),manifest_sha256=sha(data),files_count=len(members),directories_count=len(dirs),future_acceptance_approved=False,new_whole_current_review_gate='PENDING')))
if __name__=='__main__':main()
