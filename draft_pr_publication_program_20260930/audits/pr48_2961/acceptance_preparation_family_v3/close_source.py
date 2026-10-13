"""ROOT-only SOURCE V3 closer; private source text and closed inputs only, no production import or execution."""
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
    need(c['schema']=='pr48-acceptance-source-preparation-private-actual-capture/v3' and c['production_import_compile_or_execution'] is False and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['operator_pid']) is int and c['operator_pid']>0 and type(c['exit_code']) is int and c['exit_code']==expected and c['source_unchanged'] is True and c['operator_unchanged'] is True and c['stdin_supplied'] is False,'Actual complete typed capture')
    need(c['argv']==pre['argv'] and c['cwd']==pre['cwd']==str(R) and type(c['argv']) is list and c['argv'][:2]==['/usr/bin/python3','-B'] and len(c['argv'])==3 and Path(c['argv'][2]).parent==H and Path(c['argv'][2]).name in ['private_path_controls.py','verify_private_readback.py'],'Private argv whitelist')
    need(sha(read(folder/'PRELAUNCH_SOURCE.py'))==c['source_sha256']==pre['source_sha256'] and sha(read(folder/'PRELAUNCH_OPERATOR.py'))==c['operator_sha256']==pre['operator_sha256'],'Whole prelaunch sources')
    for ch in ['stdout','stderr']:need(set(c[ch])=={'path','bytes','sha256'} and c[ch]['path']==ch+'.bin','Complete literal stream');check(folder,c[ch])
    start=dt.datetime.fromisoformat(c['started_utc']);end=dt.datetime.fromisoformat(c['finished_utc']);need(start.tzinfo is not None and start.utcoffset()==dt.timedelta(0) and end.tzinfo is not None and end.utcoffset()==dt.timedelta(0) and start<=end<=dt.datetime.now(dt.timezone.utc),'Actual UTC chronology')
    need((read(folder/'stderr.bin')==b'') if expected==0 else (b'EXPECTED_REJECTION' in read(folder/'stderr.bin')),'Whole actual stderr disposition')
def external(inputs):
    need(inputs['actual_predecessor_PR47_completed'] is True and all(type(inputs[n]) is dict for n in ['previous_mirror','previous_post','previous_root_post']) and inputs['future_native13_and_main_required'] is True,'Genuine completed47 binding, no future48 approval')
    rr=list(inputs['pins'].values())+inputs['external_input_rows']+list(inputs['source_pattern_dated_references'].values())+[inputs['known_predecessor_source_contract'],inputs['known_predecessor_source_manifest']]+[inputs[n] for n in ['previous_mirror','previous_post','previous_root_post']]
    for z in rr:check(R,z,True)
    need(len(inputs['external_input_rows'])==3912 and len({z['path'] for z in inputs['external_input_rows']})==3912,'All3912 fixed external bodies; four native historical rows excluded')
def superseded():
    o=parse(read(H/'SUPERSEDED_SOURCE_BINDINGS.json'));need(o['status']=='SUPERSEDED_V1_NEEDS_M1_REPAIR_NOT_PROMOTED' and o['previous_PASS_transferred'] is False,'Closed failedV1 is not promoted')
    for key,pin_value,count in [('superseded_source','2f5e572078066a5a895ac813e813106b140f4cc3beabd38f488b7633d07b9c86',121),('closed_adverse','e32146a5f566158b30de3b403184e38067f4628a924c11748e43a28e514b35f6',45)]:
        c=o[key];check(R,c['manifest'],True);need(c['manifest']['sha256']==pin_value and c['payload_files']==count,'Exact actual closed history')
        m=parse(read(R/c['manifest']['path']));need(m==c['entire_manifest'] and type(m['files_count']) is int and m['files_count']==count,'Entire old closure metadata')
        base=(R/c['manifest']['path']).parent;need(m['self_excluded']==[(R/c['manifest']['path']).name],'Literal old self-only')
        for z in c['individual_closed_members']:check(R,z,True);need(z['full_mode']==0o444,'Closed old full444')
        names={p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file()};need(names=={z['path'] for z in m['files']}|{(R/c['manifest']['path']).name},'Entire preserved old payload names')
    for k in ['report','verdict']:check(R,o[k],True)
    verdict=parse(read(R/o['verdict']['path']));need(verdict==o['entire_adverse_verdict'] and verdict['verdict']=='NEEDS_SOURCE_CORRECTION_SCOPED' and [z['id'] for z in verdict['mandatory_corrections']]==['M1'],'Honest entire closed M1 verdict')
    for row in o['actual_source_and_adverse_closure_readback_captures']:
        check(R,row['capture'],True);c=parse(read(R/row['capture']['path']));need(c==row['complete_capture'] and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==0 and c['status']=='PASS' and c['operator_unchanged'] is True,'Entire genuine old CAP4')
        for z in row['complete_members']:check(R,z,True)

def v3_history_inputs():
    h=parse(read(H/'V2_M2_HISTORY_BINDINGS.json'));need(h['status']=='CLOSED_V2_AND_CLOSED_M2_ADVERSE_UNPROMOTED' and h['previous_PASS_transferred'] is False,'M2 history not promoted')
    for section,pin_value,count in [('superseded_V2','48ddcccb22eb898c42598278fa4914d84fa0da640e098973a1e70d7c60577662',70),('closed_M2_adverse','9f9e9d0226f4cf1bb4439e46cf7ecfa7469ca1d4da52785569b96767eb2298a3',60)]:
        v=h[section];check(R,v['manifest'],True);need(v['manifest']['sha256']==pin_value and v['payload_files']==count and parse(read(R/v['manifest']['path']))==v['entire_manifest'],'Exact genuine M2-era closure')
        for z in v['individual_closed_members']:check(R,z,True);need(z['full_mode']==0o444,'Exact current historical-family full444')
    for n in ['report','verdict']:check(R,h[n],True)
    need(parse(read(R/h['verdict']['path']))==h['entire_M2_verdict'] and [z['id'] for z in h['entire_M2_verdict']['mandatory_corrections']]==['M2'],'Entire actual scoped M2 verdict')
    for row in h['actual_closure_and_readback_captures']:
        check(R,row['capture'],True);need(parse(read(R/row['capture']['path']))==row['complete_capture'],'Entire historical actual CAP4')
        for z in row['complete_members']:check(R,z,True)
    p=parse(read(H/'ACTUAL47_PREDECESSOR_BINDINGS.json'));need(p['actual_PR47_ROOT_post_completed'] is True and p['future_PR48_approval_supplied'] is False and p['post_native4_is_dated_not_future_live_authority'] is True,'Actual47 does not approve48 or freeze live native4')
    for n in ['root_post','verifier_post','mirror','original47_post_operator_source']:check(R,p[n],True)
    need(parse(read(R/p['root_post']['path']))==p['entire_ROOT22_post'] and len(p['entire_ROOT22_post'])==22 and p['entire_ROOT22_post']['entire_post']==p['entire_verifier_post'] and parse(read(R/p['verifier_post']['path']))==p['entire_verifier_post'],'Entire completed47 post binding')
    for row in [p['complete_actual_ROOT_post_capture']]+p['complete_six_actual_phase_captures']:
        check(R,row['capture'],True);c=parse(read(R/row['capture']['path']));need(c==row['complete_capture'] and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==0,'Complete genuine actual47 child')
        for z in row['complete_members']:check(R,z,True)

def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-report-sha256',required=True);a=p.parse_args();need(not (H/NAME).exists() and not (H/NAME).is_symlink(),'Absent root self');need(sha(read(H/'REPORT.md'))==a.expected_report_sha256,'ROOT supplied report SHA');inputs=parse(read(H/'INPUT_BINDINGS.json'));external(inputs)
    superseded();v3_history_inputs()
    for n in ['private_path_controls_v3_actual_capture','private_readback_v3_actual_capture']:actual(H/n,0)
    controls=parse(read(H/'PRIVATE_PATH_CONTROLS_RESULT.json'));need(controls['status']=='PASS_PRIVATE_PATH_PREDICATES_ONLY' and controls['operator_folder']=='acceptance_preparation_family_v3' and controls['M1_write_fresh_check_unchanged'] is True and controls['production_imported_compiled_executed'] is False and controls['sealer_launched'] is False,'Bounded private exact-V3 path models only')
    final=parse(read(H/'FINAL_READY_CHECK.json'));need(final['status']=='READY_SOURCE_ONLY_WAIT_ROOT_CLOSURE_AND_NEW_ADVERSARY' and final['production_imported_compiled_executed'] is False and final['actual_PR47_predecessor_completed'] is True,'Final source-only readback')
    for n,z in final['source_files'].items():check(H,{'path':n,'bytes':z['bytes'],'sha256':z['sha256']})
    files,dirs=tree();need(NAME not in files,'Literal self excluded');payload=[]
    for n,p in sorted(files.items()):b=read(p);payload.append({'path':n,'bytes':len(b),'sha256':sha(b)})
    for z in payload:check(H,z)
    again,dd=tree();need(set(again)==set(files) and dd==dirs,'Topology unchanged before close')
    body=(json.dumps({'schema':'pr48-acceptance-source-closure/v3','status':'CLOSED_SOURCE_ONLY','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'self_excluded':[NAME],'files_count':len(payload),'files':payload,'source_only':True,'proposed_helpers_imported_compiled_executed':False,'future_acceptance_or_ROOT_approval_claimed':False},sort_keys=True,indent=2)+'\n').encode()
    for p in files.values():p.chmod(0o444)
    for z in payload:check(H,z);need(stat.S_IMODE((H/z['path']).stat().st_mode)==0o444,'Full0444 including special bits')
    stage=H/'.PREPARATION_MANIFEST.staging'
    with stage.open('xb') as h:h.write(body);h.flush();os.fsync(h.fileno())
    stage.chmod(0o444);os.link(stage,H/NAME,follow_symlinks=False);stage.unlink();fd=os.open(H,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)
    external(inputs);closed,dd=tree();need(set(closed)==set(files)|{NAME} and dd==dirs and stat.S_IMODE((H/NAME).stat().st_mode)==0o444,'Exact self-only complete closed topology');print(json.dumps({'status':'CLOSED_SOURCE_ONLY','actual_closing_pid':os.getpid(),'files_count':len(payload),'directories_count':len(dirs),'manifest_sha256':sha(read(H/NAME)),'production_imported_compiled_executed':False,'future_acceptance_approved':False},sort_keys=True))
if __name__=='__main__':main()
