#!/usr/bin/python3
"""ROOT only, after preparer exits. Self-only closure, never production execution."""
import argparse, datetime, hashlib, json, math, os, pathlib, re, stat, sys
F=pathlib.Path(__file__).absolute().parent;R=F.parent.parents[2];SELF='PREPARATION_MANIFEST.json'
CAPTURES={'INPUT_INSPECTION_ACTUAL_CAPTURE':0,'AUTHORING_ACTUAL_CAPTURE':0,'AUTHORING_V2_ACTUAL_CAPTURE':0,'QUALIFICATIONS_ACTUAL_CAPTURE':0,'PRIVATE_CONTROLS_ACTUAL_CAPTURE':1,'PRIVATE_CONTROLS_V2_ACTUAL_CAPTURE':0,'FINAL_SOURCE_READ_ACTUAL_CAPTURE':0}
def require(v,n):
    if not v:raise ValueError(n)
def digest(b):return hashlib.sha256(b).hexdigest()
def raw(p):
    require(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink file');return p.read_bytes()
def load(b):
    def pairs(ps):
        d={}
        for k,v in ps:require(k not in d,'Duplicate JSON key');d[k]=v
        return d
    def num(s):
        v=float(s);require(math.isfinite(v),'Finite JSON');return v
    def const(s):raise ValueError('Nonfinite JSON')
    return json.loads(b,object_pairs_hook=pairs,parse_float=num,parse_constant=const)
def utc(s):
    require(type(s) is str,'UTC text');t=datetime.datetime.fromisoformat(s);require(t.utcoffset()==datetime.timedelta(0),'Aware UTC');return t
def tree():
    require(F==pathlib.Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr49_30000703/current_preparation_family') and not F.is_symlink(),'Exact self-only family')
    files={};dirs={'.':stat.S_IMODE(F.stat().st_mode)}
    for p in F.rglob('*'):
        require(not p.is_symlink(),'No symlink');n=p.relative_to(F).as_posix()
        if stat.S_ISREG(p.stat().st_mode):files[n]=p
        else:require(stat.S_ISDIR(p.stat().st_mode),'No special member');dirs[n]=stat.S_IMODE(p.stat().st_mode)
    expected={'.'}|{str(q) for n in files for q in pathlib.PurePosixPath(n).parents if str(q)!='.'};require(set(dirs)==expected,'No empty or extra directory');return files,dirs
def captures():
    require({p.name for p in F.glob('*_ACTUAL_CAPTURE')}==set(CAPTURES),'Complete seven capture folders')
    result=[]
    for name,expected in sorted(CAPTURES.items()):
        d=F/name;c=load(raw(d/'CAPTURE.json'));pre=load(raw(d/'PRELAUNCH.json'))
        require(c['schema']=='pr49-source-preparation-actual-capture/v1' and pre['schema']=='pr49-source-preparation-prelaunch/v1','Actual preparation schemas')
        require(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==expected and c['stdin_supplied'] is False and c['source_unchanged'] is True and c['operator_unchanged'] is True and 'operator_failure' not in c,'Completed actual child, including preserved expected failure')
        require(c['status']==('PASS_SOURCE_ONLY_OPERATION' if expected==0 else 'FAIL_SOURCE_ONLY_OPERATION_PRESERVED'),'Expected status')
        require(c['production_builder_or_ROOT_operator_executed'] is False and c['cwd']==str(R) and type(c['operator_pid']) is int and c['operator_pid']>0 and utc(c['started_utc'])<=utc(c['finished_utc'])<=datetime.datetime.now(datetime.timezone.utc),'Actual source-only chronology')
        require(all(c[k]==pre[k] for k in pre if k!='schema'),'Literal real prelaunch values')
        require(digest(raw(d/'PRELAUNCH_SOURCE.py'))==c['source_sha256'] and digest(raw(d/'PRELAUNCH_OPERATOR.py'))==c['operator_sha256'],'Copied prelaunch sources')
        require(type(c['argv']) is list and len(c['argv'])==3 and c['argv'][:2]==['/usr/bin/python3','-B'] and pathlib.Path(c['argv'][2]).parent==F and pathlib.Path(c['argv'][2]).name not in {'prepare_current_packet.py','capture_root_builder_operation.py','close_source_preparation.py','verify_source_preparation_readonly.py'},'Only actual nonproduction source')
        require(digest(raw(pathlib.Path(c['argv'][2])))==c['source_sha256'],'Unchanged actual nonproduction source')
        for channel in ['stdout','stderr']:
            sr=c[channel];require(set(sr)=={'path','bytes','sha256'} and sr['path']==channel+'.bin' and type(sr['bytes']) is int and sr['bytes']>=0,'Exact split stream row');b=raw(d/sr['path']);require(len(b)==sr['bytes'] and digest(b)==sr['sha256'],'Complete split streams')
        require((c['stderr']['bytes']==0) if expected==0 else ('Normative text RENAME_EXCL' in raw(d/'stderr.bin').decode()),'Preserved success/failure streams')
        result.append({'directory':name,'actual_pid':c['pid'],'exit_code':expected,'capture_sha256':digest(raw(d/'CAPTURE.json')),'finished_utc':c['finished_utc']})
    return result
def fixed():
    pins=load(raw(F/'STATIC_INPUT_BINDINGS.json'));require(pins['schema']=='pr49-fixed-current-source-inputs/v1' and len(pins['fixed_rows'])==1184,'Actual fixed input schema/count')
    names=set()
    for row in pins['fixed_rows']:
        require(set(row)=={'path','bytes','sha256','full_mode'} and type(row['bytes']) is int and type(row['full_mode']) is int and row['path'] not in names,'Typed unique fixed rows');names.add(row['path']);p=R/row['path'];b=raw(p);require(len(b)==row['bytes'] and digest(b)==row['sha256'] and stat.S_IMODE(p.stat().st_mode)==row['full_mode'],'All fixed first-party body/modes')
    require(set(pins['closed_inputs'])=={'original','boundary','hyperbolic','ROOT'},'Four explicit schema inputs')
    for info in pins['closed_inputs'].values():
        for d in info['directories']:require(type(d['full_mode']) is int and stat.S_IMODE((R/info['root']/d['path']).stat().st_mode)==d['full_mode'],'Fixed directory modes')
def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-report-sha256',required=True);a=p.parse_args();require(not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'Checks enabled')
    require(re.fullmatch('[0-9a-f]{64}',a.expected_report_sha256) is not None and digest(raw(F/'SOURCE_REPORT.md'))==a.expected_report_sha256,'ROOT exact report SHA')
    require(not (F/SELF).exists(),'Never overwrite SOURCE manifest');files,dirs=tree();require(SELF not in files,'No premature closure');fixed();cs=captures()
    status=load(raw(F/'SOURCE_STATUS.json'));require(status['current_SOURCE_verdict'] is None and status['production_builder_executed'] is False and status['production_operator_executed'] is False and status['future_acceptance_approved'] is False,'Source status null/false')
    result=load(raw(F/'FINAL_SOURCE_READ_RESULT.json'));require(result['status']=='PASS_FINAL_SOURCE_ONLY_READ' and result['production_builder_imported_compiled_executed'] is False and result['production_operator_imported_compiled_executed'] is False and result['SOURCE_adversary_verdict'] is None,'Final nonproduction read complete')
    for q in files.values():q.chmod(0o444)
    members=[]
    for name,q in sorted(files.items()):
        b=raw(q);require(stat.S_IMODE(q.stat().st_mode)==0o444,'Every own full0444');members.append({'path':name,'bytes':len(b),'sha256':digest(b),'full_mode':0o444})
    created=datetime.datetime.now(datetime.timezone.utc).isoformat();require(all(utc(c['finished_utc'])<utc(created) for c in cs),'Closure after every completed child')
    m={'schema':'pr49-current-source-only-closure/v1','created_utc':created,'actual_closing_pid':os.getpid(),'files_count':len(members),'files':members,'directories':[{'path':n,'full_mode':v} for n,v in sorted(dirs.items())],'self_excluded':[SELF],'manifest_full_mode':0o444,'source_only':True,'production_builder_imported_compiled_executed':False,'production_operator_imported_compiled_executed':False,'SOURCE_adversary_verdict':None,'future_acceptance_approved':False,'original_attempts':'0/5','new_substantive_attempts':0,'audit_turns':0,'retained_actual_nonproduction_captures':cs}
    data=(json.dumps(m,indent=2,allow_nan=False)+'\n').encode()
    with (F/SELF).open('xb') as h:h.write(data);h.flush();os.fsync(h.fileno())
    (F/SELF).chmod(0o444);nowfiles,nowdirs=tree();require(set(nowfiles)==set(files)|{SELF} and nowdirs==dirs,'Complete closed topology')
    for r in members:b=raw(F/r['path']);require(len(b)==r['bytes'] and digest(b)==r['sha256'] and stat.S_IMODE((F/r['path']).stat().st_mode)==r['full_mode'],'Final closed body/mode')
    require(stat.S_IMODE((F/SELF).stat().st_mode)==0o444 and raw(F/SELF)==data,'Manifest self full0444')
    print(json.dumps({'status':'PASS_ROOT_SOURCE_SELF_ONLY_CLOSURE','actual_closing_pid':os.getpid(),'manifest_sha256':digest(data),'files_count':len(members),'directories_count':len(dirs),'SOURCE_adversary_verdict':None,'future_acceptance_approved':False,'production_execution':False}))
if __name__=='__main__':main()
