"""Private read-only complete-byte inventory; never imports production sources."""
import datetime as dt, hashlib, json, os, stat
from pathlib import Path, PurePosixPath
F=Path(__file__).absolute().parent; A=F.parent; R=F.parents[3]; C=A/'reviewed_candidate'; W=A/'current_whole_adversary_family'
def need(v,m):
    if not v: raise ValueError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def pairs(v):
    d={}
    for k,x in v: need(k not in d,'Duplicate JSON key'); d[k]=x
    return d
def parse(b): return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def raw(p):
    need(not p.is_symlink() and all(not x.is_symlink() for x in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular source only'); return p.read_bytes()
def pin(p):
    b=raw(p); return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)}
def dump(n,v):
    p=F/n
    with p.open('xb') as h: h.write((json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode());h.flush();os.fsync(h.fileno())
def checkrow(base,z,frozen=False):
    n=z['path']; q=PurePosixPath(n)
    need(type(n) is str and q.as_posix()==n and not q.is_absolute() and not {'.','..','.git','__pycache__'}.intersection(q.parts),'Canonical path')
    need(type(z['bytes']) is int and z['bytes']>=0 and type(z['sha256']) is str,'Typed reference'); p=base/n; b=raw(p)
    need(len(b)==z['bytes'] and sha(b)==z['sha256'],'Full bytes differ '+n)
    if frozen: need(stat.S_IMODE(p.stat().st_mode)==0o444,'Full0444 '+n)
    elif 'full_mode' in z: need(type(z['full_mode']) is int and stat.S_IMODE(p.stat().st_mode)==z['full_mode'],'Exact fullmode '+n)
    return len(b)
def closed(base,pinned,count,dirs):
    b=raw(base/'MANIFEST.json');need(sha(b)==pinned,'Manifest pin');m=parse(b)
    need(m['self_excluded']==['MANIFEST.json'] and type(m['files_count']) is int and m['files_count']==count and len(m['files'])==count,'Self-only closure')
    names={z['path'] for z in m['files']}|{'MANIFEST.json'};actual=set();dd=set()
    for p in base.rglob('*'):
        need(not p.is_symlink() and (p.is_file() or p.is_dir()),'No special member')
        (actual if p.is_file() else dd).add(p.relative_to(base).as_posix())
    expected={p.as_posix() for n in names for p in PurePosixPath(n).parents if p.as_posix()!='.'}
    need(actual==names and dd==expected and len(dd)==dirs and sorted(dd)==sorted(m['directories']),'Whole files/directories')
    total=sum(checkrow(base,z,True) for z in m['files']);need(stat.S_IMODE((base/'MANIFEST.json').stat().st_mode)==0o444,'Manifest444')
    return m,total+len(b)
def scalar_walk(o):
    if type(o) is dict:return 1+sum(scalar_walk(k)+scalar_walk(v) for k,v in o.items())
    if type(o) is list:return 1+sum(map(scalar_walk,o))
    need(type(o) in {str,int,float,bool,type(None)},'JSON scalar type');return 1
def stream(z):
    for c in ['stdout','stderr']:checkrow(R,z[c])
    need(raw(R/z['stderr']['path'])==b'','Full stderr')
def main():
    cm,cb=closed(C,'a7d1acc9dbbf8cd5435d0bebd8f6b1a540ecb0f2aea8d0c616c46bc5bf6b4ea5',1328,282)
    wm,wb=closed(W,'658133399198e8528aa2a45b89c87a19f3b69edd6998b86b7e8227c850f5fd78',385,84)
    rootbody=raw(A/'ROOT_WHOLE_CURRENT_REVIEW.json');need(len(rootbody)==974387 and sha(rootbody)=='b10320f4ca9bc5fb233e4a8cce4baecafc3fff71a7f0b0e5966495aafcd61c9a','Entire genuine ROOT');root=parse(rootbody);nodes=scalar_walk(root)
    need(root['actual_readback_pid']==89547 and type(root['actual_readback_pid']) is int and root['future_acceptance_approved'] is False and root['mandatory_corrections']==[],'Actual ROOT partial gate')
    need(root['complete_VERDICT_object']==parse(raw(W/'VERDICT.json')) and len(root['normalized_complete_first_party_members'])==385 and len(root['normalized_complete_external_input_bindings'])==2933,'Entire verdict/member bindings')
    fbytes=sum(checkrow(R,z) for z in root['normalized_complete_first_party_members'])
    native={'draft_pr_publication_program_20260930/inventory.json'}|{'unsolved_math_prioritization/'+n for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']}
    mutable={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
    foreign=root['normalized_complete_external_input_bindings'];need(len({z['path'] for z in foreign})==2933,'Unique external bindings')
    stable=[];dated=[];fbytes2=0
    for z in foreign:
        if z['path'] in mutable:dated.append(z)
        else:fbytes2+=checkrow(R,z);stable.append(z)
    refs=[pin(C/'MANIFEST.json'),pin(C/'CURRENT_DEPENDENCIES.json'),pin(W/'MANIFEST.json'),pin(W/'AUDIT.md'),pin(W/'VERDICT.json'),pin(A/'ROOT_WHOLE_CURRENT_REVIEW.json'),pin(A/'snapshot_manifest.json'),pin(A/'original_diff.patch')]
    for z in root['ROOT_evidence_and_actual_prerequisite_bindings']:checkrow(R,z);refs.append(z)
    for e in root['complete_actual_closing_and_postclosing_readback_captures']:
        need(e['complete_capture']['pid'] in [86916,87026] and e['complete_capture']['exit_code']==0,'Actual closing/readback')
        need(parse(raw(R/e['capture']['path']))==e['complete_capture'],'Entire actual parent')
        for z in e['complete_members']:checkrow(R,z);refs.append(z)
        need(parse(raw((R/e['capture']['path']).parent/'stdout.bin'))==e['complete_stdout_object'],'Entire actual child stdout')
    a45=R/'draft_pr_publication_program_20260930/audits/pr45_9900007'
    capdir=a45/'root_pr47_whole_ROOT_record_authoring_actual_capture';capture=parse(raw(capdir/'CAPTURE.json'))
    need(type(capture['pid']) is int and capture['pid']==89547 and capture['exit_code']==0 and capture['completed'] is True,'Actual ROOT authoring')
    for p in sorted(capdir.iterdir()):refs.append(pin(p));raw(p)
    result=parse(raw(A/'root_original_actual_reproduction/ROOT_REPRODUCTION_RESULT.json'));helpers=result['complete_actual_helper_captures'];git=result['complete_actual_Git_captures']
    need(len(helpers)==3 and len(git)==33,'Actual3helpers33Git')
    expectedkeys={'schema','argv','cwd','started_utc','actual_operator_pid','stdin_supplied','source','actual_execution','pid','completed','exit_code','finished_utc','stdout','stderr','source_unchanged'}
    for i,z in enumerate(helpers+git):
        need(set(z)==expectedkeys and z['schema']=='pr47-root-literal-operation-capture/v1' and type(z['pid']) is int and z['pid']>0 and z['exit_code']==0 and z['actual_execution'] is True and z['completed'] is True and z['stdin_supplied'] is False,'Exact capture types')
        stream(z)
        if i<3:need(type(z['source']) is dict and z['source_unchanged'] is True and z['argv'][:2]==['/usr/bin/python3','-B'],'Typed actual helper');checkrow(R,z['source'])
        else:need(z['source'] is None and z['source_unchanged'] is None and z['argv'][0]=='git' and z['argv'][1] in ['show','ls-tree','diff'],'Genuine Git null fields')
    refs.append(pin(A/'root_original_actual_reproduction/ROOT_REPRODUCTION_RESULT.json'))
    for name in ['ROOT_ACTUAL_CURRENT_FREEZE_INSPECTION.json','ROOT_NEW_SOURCE_ADVERSARY_RECORD.json','ROOT_PRIMARY_READ_LEDGER.json','ROOT_SCIENCE_CARD.json']:scalar_walk(parse(raw(A/name)))
    originals=parse(raw(A/'snapshot_manifest.json'));need(len(originals['files'])==16,'Original16')
    for z in originals['files']:
        b=raw(A/'source_snapshot'/z['relative_path']);need(len(b)==z['bytes'] and sha(b)==z['sha256'],'Original16 unchanged')
    immutable=['verify.py','verification.json','source_checksums.json','source_record.json','turns.json','prior_report.json','review/independent_checks.py','review/independent_results.json','review/submitted_verify.py','review/submitted_results.json']
    for n in immutable:need(raw(C/n)==raw(A/'source_snapshot'/n),'Operative immutable10')
    deps=parse(raw(C/'CURRENT_DEPENDENCIES.json'));need(deps['anchor']=='repository_root' and len(deps['files'])==1422,'Exact1422 dependencies anchor')
    need(root['ROOT_actual_inner49_complete_read'] is True and root['frozen_inner47_honest_prefix'] is True,'49final47prefix')
    records={'EXPECTED_CURRENT_DEPENDENCIES.json':deps,'EXPECTED_CURRENT_ADMIN.json':parse(raw(C/'status.json')),'EXPECTED_WHOLE_MANIFEST.json':wm,'EXPECTED_WHOLE_VERDICT.json':parse(raw(W/'VERDICT.json')),'EXPECTED_ROOT_WHOLE_REVIEW.json':root,'EXPECTED_PRIMARY_READ_LEDGER.json':parse(raw(A/'ROOT_PRIMARY_READ_LEDGER.json')),'EXPECTED_SCIENCE_CARD.json':parse(raw(A/'ROOT_SCIENCE_CARD.json')),'EXPECTED_ORIGINAL_LEDGER.json':parse(raw(C/'turns.json')),'EXPECTED_ORIGINAL_CAPTURE_RESULT.json':result}
    for n,v in records.items():dump(n,v)
    bypath={z['path']:z for z in refs};inputs={'schema':'pr47-acceptance-source-input-bindings/v1','whole_binding_completed':True,'actual_predecessor_PR46_completed':False,'previous_mirror':None,'previous_post':None,'previous_root_post':None,'previous_post_contract':None,'pins':bypath,'closed_whole_manifest':pin(W/'MANIFEST.json'),'closed_whole_result':pin(W/'VERDICT.json'),'closed_whole_report':pin(W/'AUDIT.md'),'closed_root_whole_inspection':pin(A/'ROOT_WHOLE_CURRENT_REVIEW.json'),'external_input_rows':stable,'external_input_count':len(stable),'dated_native_external_rows':dated,'dated_native13':deps['current_native13'],'future_native13_and_main_required':True,'foreign_bodies_copied':False,'production_import_compile_or_execution':False}
    dump('INPUT_BINDINGS.json',inputs)
    out={'schema':'pr47-acceptance-private-complete-input-inspection/v1','actual_pid':os.getpid(),'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'current_payload':1328,'whole_payload':385,'current_total_bytes':cb,'whole_total_bytes':wb,'ROOT_full_json_nodes':nodes,'ROOT_full_bytes':len(rootbody),'first_party_bytes':fbytes,'external_count':2933,'stable_external_count':len(stable),'stable_external_bytes':fbytes2,'dated_mutable_external_count':len(dated),'original16':True,'immutable10':True,'literal_original_turns':1,'new_turns':0,'audit_turns':0,'actual33Git_null_and3helper_typed':True,'actual_whole_close_pid':86916,'actual_whole_readback_pid':87026,'actual_ROOT_record_pid':89547,'historical_final49_prefix47_preserved':True,'actual_PR46_predecessor_completed':False,'future_acceptance_approved':False,'production_import_compile_or_execution':False,'foreign_bodies_copied':False}
    dump('COMPLETE_INPUT_INSPECTION.json',out);print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
