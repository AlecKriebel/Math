"""ROOT-only SOURCE closer; private source text and closed inputs only, no production import or execution."""
import argparse, datetime as dt, hashlib, json, math, os, re, stat
from pathlib import Path, PurePosixPath
H=Path(__file__).absolute().parent;R=H.parents[3];NAME='PREPARATION_MANIFEST.json'
def need(v,m):
    if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def parse(b):
    def pairs(v):
        o={}
        for k,x in v:need(k not in o,'Duplicate JSON key');o[k]=x
        return o
    def floating(s):x=float(s);need(math.isfinite(x),'Nonfinite');return x
    return json.loads(b,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def name(n):
    need(type(n) is str and n and '\\' not in n and '\0' not in n,'Path');p=PurePosixPath(n);need(not p.is_absolute() and p.as_posix()==n and n!='.' and not {'.','..','.git','__pycache__'}.intersection(p.parts),'Canonical path');return n
def read(p):need(not p.is_symlink() and all(not x.is_symlink() for x in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink');return p.read_bytes()
def check(base,z,mode=False):
    p=base/name(z['path']);b=read(p);need(type(z['bytes']) is int and z['bytes']>=0 and type(z['sha256']) is str and re.fullmatch('[0-9a-f]{64}',z['sha256']) and len(b)==z['bytes'] and sha(b)==z['sha256'],'Entire bound body '+str(p))
    if mode:need(type(z['full_mode']) is int and stat.S_IMODE(p.stat().st_mode)==z['full_mode'],'Full external mode')
def tree():
    need(H.is_dir() and not H.is_symlink(),'Owned root');files={};dirs=set()
    for p in H.rglob('*'):
        n=name(p.relative_to(H).as_posix());need(not p.is_symlink() and (p.is_file() or p.is_dir()),'No special/symlink');
        if p.is_file():files[n]=p
        else:dirs.add(n)
    expected={p.as_posix() for n in files for p in PurePosixPath(n).parents if p.as_posix()!='.'};need(dirs==expected,'Exact topology, no empty/unbound directory');return files,dirs
def actual(folder,expected):
    need({p.name for p in folder.iterdir()}=={'CAPTURE.json','PRELAUNCH.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'},'Exact six-member private capture');c=parse(read(folder/'CAPTURE.json'));pre=parse(read(folder/'PRELAUNCH.json'))
    need(set(c)=={'schema','argv','cwd','operator_pid','started_utc','source_sha256','operator_sha256','production_import_compile_or_execution','actual_execution','completed','pid','exit_code','stdin_supplied','finished_utc','source_unchanged','operator_unchanged','stdout','stderr'},'Exact capture schema')
    need(c['schema']=='pr48-acceptance-source-preparation-private-actual-capture/v1' and c['production_import_compile_or_execution'] is False and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['operator_pid']) is int and c['operator_pid']>0 and type(c['exit_code']) is int and c['exit_code']==expected and c['source_unchanged'] is True and c['operator_unchanged'] is True and c['stdin_supplied'] is False,'Actual complete typed capture')
    need(c['argv']==pre['argv'] and c['cwd']==pre['cwd']==str(R) and type(c['argv']) is list and c['argv'][:2]==['/usr/bin/python3','-B'] and len(c['argv'])==3 and Path(c['argv'][2]).parent==H and Path(c['argv'][2]).name in ['inspect_acceptance_inputs.py','author_acceptance_source.py','private_acceptance_controls.py','expected_negative.py'],'Private argv whitelist')
    need(sha(read(folder/'PRELAUNCH_SOURCE.py'))==c['source_sha256']==pre['source_sha256'] and sha(read(folder/'PRELAUNCH_OPERATOR.py'))==c['operator_sha256']==pre['operator_sha256'],'Whole prelaunch sources')
    for ch in ['stdout','stderr']:need(set(c[ch])=={'path','bytes','sha256'} and c[ch]['path']==ch+'.bin','Complete literal stream');check(folder,c[ch])
    start=dt.datetime.fromisoformat(c['started_utc']);end=dt.datetime.fromisoformat(c['finished_utc']);need(start.tzinfo is not None and start.utcoffset()==dt.timedelta(0) and end.tzinfo is not None and end.utcoffset()==dt.timedelta(0) and start<=end<=dt.datetime.now(dt.timezone.utc),'Actual UTC chronology')
    need((read(folder/'stderr.bin')==b'') if expected==0 else (b'EXPECTED_REJECTION' in read(folder/'stderr.bin')),'Whole actual stderr disposition')
def external(inputs):
    need(inputs['actual_predecessor_PR47_completed'] is False and inputs['previous_mirror'] is None and inputs['previous_post'] is None and inputs['previous_root_post'] is None and inputs['future_native13_and_main_required'] is True,'No future predecessor authority')
    rr=list(inputs['pins'].values())+inputs['external_input_rows']+list(inputs['source_pattern_dated_references'].values())+[inputs['known_predecessor_source_contract'],inputs['known_predecessor_source_manifest']]
    for z in rr:check(R,z,True)
    need(len(inputs['external_input_rows'])==3912 and len({z['path'] for z in inputs['external_input_rows']})==3912,'All3912 fixed external bodies; four native historical rows excluded')
def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-report-sha256',required=True);a=p.parse_args();need(not (H/NAME).exists() and not (H/NAME).is_symlink(),'Absent root self');need(sha(read(H/'REPORT.md'))==a.expected_report_sha256,'ROOT supplied report SHA');inputs=parse(read(H/'INPUT_BINDINGS.json'));external(inputs)
    for n,code in {'inspect_inputs_v1_actual_capture':0,'author_sources_v1_actual_capture':0,'repair_sources_v2_actual_capture':0,'repair_metadata_v3_actual_capture':0,'private_controls_v1_actual_capture':0,'private_controls_v2_actual_capture':0,'expected_negative_actual_capture':1,'final_readback_actual_capture':0}.items():actual(H/n,code)
    controls=parse(read(H/'PRIVATE_CONTROLS_RESULT.json'));need(controls['status']=='PASS_PRIVATE_PREDICATES_ONLY' and controls['actual_full_permission_modes']==4096 and controls['all_original_actual_Git_captures']==38 and controls['literal_historical_and_final_typed_helpers']==4 and controls['canonical_overlay']==1955 and controls['canonical_accepted_payload']==1957 and controls['ROOT_post_keys']==22 and controls['proposed_source_imported_compiled_executed'] is False,'Actual private controls scope only')
    final=parse(read(H/'FINAL_READY_CHECK.json'));need(final['status']=='READY_SOURCE_ONLY_WAIT_ROOT_CLOSURE_AND_NEW_ADVERSARY' and final['production_imported_compiled_executed'] is False and final['actual_PR47_predecessor_completed'] is False,'Final source-only readback')
    for n,z in final['source_files'].items():check(H,{'path':n,'bytes':z['bytes'],'sha256':z['sha256']})
    files,dirs=tree();need(NAME not in files,'Literal self excluded');payload=[]
    for n,p in sorted(files.items()):b=read(p);payload.append({'path':n,'bytes':len(b),'sha256':sha(b)})
    for z in payload:check(H,z)
    again,dd=tree();need(set(again)==set(files) and dd==dirs,'Topology unchanged before close')
    body=(json.dumps({'schema':'pr48-acceptance-source-closure/v1','status':'CLOSED_SOURCE_ONLY','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'self_excluded':[NAME],'files_count':len(payload),'files':payload,'source_only':True,'proposed_helpers_imported_compiled_executed':False,'future_acceptance_or_ROOT_approval_claimed':False},sort_keys=True,indent=2)+'\n').encode()
    for p in files.values():p.chmod(0o444)
    for z in payload:check(H,z);need(stat.S_IMODE((H/z['path']).stat().st_mode)==0o444,'Full0444 including special bits')
    stage=H/'.PREPARATION_MANIFEST.staging'
    with stage.open('xb') as h:h.write(body);h.flush();os.fsync(h.fileno())
    stage.chmod(0o444);os.link(stage,H/NAME,follow_symlinks=False);stage.unlink();fd=os.open(H,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)
    external(inputs);closed,dd=tree();need(set(closed)==set(files)|{NAME} and dd==dirs and stat.S_IMODE((H/NAME).stat().st_mode)==0o444,'Exact self-only complete closed topology');print(json.dumps({'status':'CLOSED_SOURCE_ONLY','actual_closing_pid':os.getpid(),'files_count':len(payload),'directories_count':len(dirs),'manifest_sha256':sha(read(H/NAME)),'production_imported_compiled_executed':False,'future_acceptance_approved':False},sort_keys=True))
if __name__=='__main__':main()
