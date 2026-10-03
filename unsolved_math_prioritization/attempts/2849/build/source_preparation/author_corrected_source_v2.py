"""SOURCE authoring only; never imports, compiles or runs production sources."""
import datetime as dt, hashlib, json, os, stat
from pathlib import Path, PurePosixPath
F=Path(__file__).absolute().parent; A=F.parent; R=A.parents[2]; OLD=A/'current_preparation_family'; ADV=A/'current_source_adversary_family'
def need(v,m):
    if not v: raise ValueError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def raw(p):
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink input'); return p.read_bytes()
def row(p):
    b=raw(p); return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)}
def put(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as h: h.write(b); h.flush(); os.fsync(h.fileno())
def enc(o): return (json.dumps(o,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
def main():
    need(__debug__ and F.name=='current_preparation_family_v2','Distinct SOURCE V2')
    groups={}; reads=[]
    for root,name,pin in [(OLD,'PREPARATION_MANIFEST.json','cc29dc830448d8ddf232f3fc080e457c6a8a015428104bba2d4fc15f62f56631'),(ADV,'SELF_MANIFEST.json','ed0aba6a7a42e752012399daed24d460e25108afd7b66c89ee1907473eb76a85')]:
        mb=raw(root/name); need(sha(mb)==pin,'Exact closed predecessor'); m=json.loads(mb); need(m['self_excluded']==[name] and m['files_count']==len(m['files']),'True closed predecessor self')
        names={r['path'] for r in m['files']}|{name}; actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}; ds={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir()}
        need(actual==names and ds==set(m['directories']) and ds=={q.as_posix() for n in names for q in PurePosixPath(n).parents if str(q)!='.'},'Exact predecessor topology')
        memberrows=[]
        for rr in m['files']:
            p=root/rr['path']; b=raw(p); need(len(b)==rr['bytes'] and sha(b)==rr['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444,'Full predecessor byte/mode read'); memberrows.append(row(p)); reads.append(row(p))
        need(stat.S_IMODE((root/name).stat().st_mode)==0o444,'Closed predecessor self full0444'); reads.append(row(root/name))
        groups[root.name]={'manifest':row(root/name),'members':memberrows,'directories':sorted(ds),'full_modes0444':True}
    verdict=json.loads(raw(ADV/'VERDICT.json')); need(verdict['verdict']=='REPAIR_REQUIRED_GENUINE_GIT_NULL_SOURCE_CONTRACT' and verdict['closed_clean'] is False and len(verdict['mandatory_corrections'])==1 and verdict['mandatory_corrections'][0]['line']==150,'Closed ADVERSE single mandatory defect')
    externals=[]
    for n,pid in [('root_pr47_adverse_source_closure_actual_capture',12168),('root_pr47_adverse_source_closed_readback_actual_capture',13238)]:
        d=A.parent/'pr45_9900007'/n; need({p.name for p in d.iterdir()}=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'},'Real external four-member capture'); c=json.loads(raw(d/'CAPTURE.json')); need(c['pid']==pid and c['completed'] is True and type(c['exit_code']) is int and c['exit_code']==0,'Completed genuine ROOT close/readback')
        for ch in ['stdout','stderr']:
            b=raw(d/c[ch]['path']); need(len(b)==c[ch]['bytes'] and sha(b)==c[ch]['sha256'],'Complete predecessor external streams')
        externals.extend(row(p) for p in sorted(d.iterdir()))
    exports=[row(OLD/n) for n in ['PREPARATION_MANIFEST.json','prepare_current_packet.py','capture_root_builder_operation.py']]+[row(ADV/n) for n in ['SELF_MANIFEST.json','REPORT.md','VERDICT.json','MANDATORY_NULL_SOURCE_WITNESS.json','GENUINE_ROOT_GIT_NULL_SOURCE_CAPTURE.json']]
    repair={'schema':'PR47_SOURCE_V2_CLOSED_ADVERSE_REPAIR_BINDINGS_v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'closed_groups':groups,'complete_fixed_member_reads':reads,'external_ROOT_closure_and_readback_members':externals,'qualified_current_packet_exports':exports,'single_mandatory_defect':'V1 line150 rejects all33 genuine null-source Git receipts as helpers','old_SOURCE_V1_promoted':False,'ADVERSE_promoted_to_clean_PASS':False,'production_import_compile_or_execution':False,'future_acceptance_approved':False}
    put(F/'SOURCE_V1_REPAIR_BINDINGS.json',enc(repair))
    selected=['STATIC_INPUT_BINDINGS.json','ROOT_FIXED_EVIDENCE.json','CURRENT_QUEUE_PATCH.json','SOURCE_PROVENANCE_CORRECTION.md','DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json','DRAFT_ROOT_CURRENT_SCOPE_CERTIFICATE.md','DRAFT_ROOT_EVIDENCE_BINDINGS.json','DRAFT_ROOT_NEW_SOURCE_ADVERSARY_RECORD.json','DRAFT_ROOT_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json']
    suffix='''

## Distinct SOURCE V2 administrative repair

The operative preparation is current_preparation_family_v2. Closed SOURCE V1 manifest cc29dc830448d8ddf232f3fc080e457c6a8a015428104bba2d4fc15f62f56631 remains unchanged and unpromoted. The complete closed [ADVERSE SOURCE report](../current_source_adversary_family/REPORT.md), manifest ed0aba6a7a42e752012399daed24d460e25108afd7b66c89ee1907473eb76a85, identifies one mandatory administrative defect at V1 builder line150. That source rejected all33 genuine read-only Git receipts because their source and source_unchanged fields are null. No old PASS is transferred.

V2 separates the three typed-source unchanged mathematical-helper receipts from the exact33 read-only Git receipts. Both classes retain the genuine pr47-root-literal-operation-capture/v1 schema, complete actual child records and full streams. Helper argv/source identities are exact; Git argv is the exact original16 show/16 ls-tree/one full-diff sequence with explicit null source fields. Invalid substitutions, malformed types, missing fields and changed argv must be rejected. Original16 archives, immutable operative helper/results/plain source/object ledger/literal null and every historical capture remain byte-exact. The closed V1 and ADVERSE bodies and separate actual ROOT closing/readback captures are fixed read-only dependencies.

This repairs an administrative evidence contract only. KP3.51 remains UNSOLVED at original1/5,new0,audit0. The known realized normal degeneracy still has no instanton rank computation here. Production builder/operator are text only, never imported, compiled or executed during preparation. All five ROOT prerequisite drafts remain false/null. A new different clean SOURCE audit, genuine ROOT prerequisites, actual current freeze, another whole-current audit, fresh13/currentHEAD reconciliation and native acceptance remain PENDING. No paper, DOI, tracker row, outside communication or Git/native/canonical mutation is supplied by SOURCE V2.
'''
    for n in selected:
        b=raw(OLD/n)
        if n.startswith('DRAFT_ROOT_') and n.endswith('.json'):
            o=json.loads(b)
            if 'operative_preparation_directory' in o: o['operative_preparation_directory']='current_preparation_family_v2'
            b=enc(o)
        elif n.endswith('.md'): b=b+suffix.encode()
        put(F/n,b)
    for folder in ['original_archive','operative_proposal','presentations','native4_proposal']:
        for p in sorted((OLD/folder).rglob('*')):
            if p.is_file():
                b=raw(p)
                if p.suffix=='.md' and folder in ['operative_proposal','presentations']: b=b+suffix.encode()
                put(F/folder/p.relative_to(OLD/folder),b)
    for n in ['SOURCE_PRECISION_QUALIFICATIONS.md','CURRENT_OVERVIEW.md','EXECUTION_CONTRACT.md','ROOT_REPRODUCTION_PREREQUISITES.md']:
        b=raw(OLD/n).decode().replace('operative_preparation_directory current_preparation_family,','operative_preparation_directory current_preparation_family_v2,')
        put(F/n,(b+suffix).encode())
    builder=raw(OLD/'prepare_current_packet.py').decode(); need(builder.count("FAMILY='current_preparation_family'")==1,'Exact V1 family marker')
    builder=builder.replace("FAMILY='current_preparation_family'","FAMILY='current_preparation_family_v2'").replace("prep['schema']=='PR47_CURRENT_SOURCE_ONLY_CLOSURE_v1'","prep['schema']=='PR47_CURRENT_SOURCE_ONLY_CLOSURE_v2'")
    marker='def build(args,script,A,R,attempt):\n'
    validator='''def validate_completed_original_capture(c,kind,expected_argv,expected_source,operator_pid,checked,R):
    keys={'schema','argv','cwd','started_utc','actual_operator_pid','stdin_supplied','source','actual_execution','pid','completed','exit_code','finished_utc','stdout','stderr','source_unchanged'}
    need(type(c) is dict and set(c)==keys and c['schema']=='pr47-root-literal-operation-capture/v1','Exact genuine ROOT capture schema/keys')
    need(kind in {'helper','git'} and type(c['argv']) is list and all(type(x) is str for x in c['argv']) and equal(c['argv'],expected_argv) and c['cwd']==str(R),'Exact bound capture class/argv/cwd')
    need(type(operator_pid) is int and operator_pid>0 and type(c['actual_operator_pid']) is int and c['actual_operator_pid']==operator_pid and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==0 and c['stdin_supplied'] is False and clock(c['started_utc'])<=clock(c['finished_utc'])<=clock(utc()),'Actual complete nonboolean child/time records')
    streams={k:checked(c[k]) for k in ['stdout','stderr']}; need(streams['stderr']==b'','Successful original child has empty complete stderr')
    if kind=='helper':
        need(type(c['source']) is dict and equal(c['source'],expected_source) and c['source_unchanged'] is True,'Exact typed unchanged mathematical helper source')
        checked(c['source'])
    else:
        need(expected_source is None and c['source'] is None and c['source_unchanged'] is None,'Genuine readonly Git null-source/null-unchanged fields')
    return streams
'''
    need(builder.count(marker)==1,'Single build marker'); builder=builder.replace(marker,validator+marker)
    old="""    caps=summary['complete_actual_helper_captures']; need(type(caps) is list and len(caps)==3,'All3 real unchanged ROOT helper captures')
    for c in caps+summary['complete_actual_Git_captures']:
        need(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==0 and c['stdin_supplied'] is False and clock(c['started_utc'])<=clock(c['finished_utc'])<=clock(utc()),'Actual complete child records')
        for k in ['stdout','stderr']: checked(c[k])
        if 'source' in c: checked(c['source']); need(c['source_unchanged'] is True,'Unchanged mathematical helper')
    need(len(summary['complete_actual_Git_captures'])==33,'Actual full16body/tree/full17diff captures')
"""
    replacement="""    caps=summary['complete_actual_helper_captures']; gitcaps=summary['complete_actual_Git_captures']; need(type(caps) is list and len(caps)==3 and type(gitcaps) is list and len(gitcaps)==33,'Exact separate3 helper/33 readonly Git classes')
    helper_specs=[('author/verify.py','verify.py'),('submitted_copy/submitted_verify.py','review/submitted_verify.py'),('historical_independent/independent_checks.py','review/independent_checks.py')]
    for c,(actual_n,original_n) in zip(caps,helper_specs):
        source_row={'path':(A/'source_snapshot'/original_n).relative_to(R).as_posix(),'bytes':len(original[original_n]),'sha256':sha(original[original_n])}
        validate_completed_original_capture(c,'helper',['/usr/bin/python3','-B',str(root/actual_n)],source_row,summary['actual_operator_pid'],checked,R)
        need(bindrepo((root/actual_n).relative_to(R).as_posix())==original[original_n],'Actual private helper source equals unchanged original')
    expected_git_argv=[]
    for r in snap['files']: expected_git_argv.extend([['git','show',HEAD+':'+r['path']],['git','ls-tree',HEAD,'--',r['path']]])
    expected_git_argv.append(['git','diff','--no-ext-diff','--no-textconv','--binary',BASE,HEAD,'--']); need(len(expected_git_argv)==33,'Exact original readonly argv whitelist')
    for c,argv in zip(gitcaps,expected_git_argv): validate_completed_original_capture(c,'git',argv,None,summary['actual_operator_pid'],checked,R)
    need(len({c['pid'] for c in caps+gitcaps})==36,'All36 real child identities distinct')
"""
    need(builder.count(old)==1,'Exact mandatory old block'); builder=builder.replace(old,replacement)
    prior="""    repair=load(bind(FAMILY+'/SOURCE_V1_REPAIR_BINDINGS.json')); need(repair['schema']=='PR47_SOURCE_V2_CLOSED_ADVERSE_REPAIR_BINDINGS_v1' and repair['old_SOURCE_V1_promoted'] is False and repair['ADVERSE_promoted_to_clean_PASS'] is False and repair['future_acceptance_approved'] is False,'Qualified prior ADVERSE never promoted')
    for group,info in repair['closed_groups'].items():
        mraw=checked(info['manifest']); m=load(mraw); oldroot=(R/info['manifest']['path']).parent; ownname=Path(info['manifest']['path']).name
        need(group in {'current_preparation_family','current_source_adversary_family'} and m['self_excluded']==[ownname] and type(m['files_count']) is int and m['files_count']==len(m['files']) and topology(oldroot)==({r['path'] for r in m['files']}|{ownname},set(info['directories'])),'Exact prior closed SOURCE/ADVERSE topology')
        need(info['manifest']['sha256']==('cc29dc830448d8ddf232f3fc080e457c6a8a015428104bba2d4fc15f62f56631' if group=='current_preparation_family' else 'ed0aba6a7a42e752012399daed24d460e25108afd7b66c89ee1907473eb76a85'),'Actual closed prior manifest pin')
    for r in repair['complete_fixed_member_reads']+repair['external_ROOT_closure_and_readback_members']: checked(r)
    for r in repair['qualified_current_packet_exports']: outputs['prior_adverse_source_repair/'+r['path']]=checked(r)
"""
    insertion="    pins=load(bind(FAMILY+'/STATIC_INPUT_BINDINGS.json'));"
    need(builder.count(insertion)==1,'Single prior evidence insertion'); builder=builder.replace(insertion,prior+insertion)
    put(F/'prepare_current_packet.py',builder.encode())
    operator=raw(OLD/'capture_root_builder_operation.py').decode().replace("F.name=='current_preparation_family'","F.name=='current_preparation_family_v2'")
    put(F/'capture_root_builder_operation.py',operator.encode())
    status={'schema':'PR47_CURRENT_SOURCE_PREPARATION_STATUS_v2','operative_preparation_directory':F.name,'status':'SOURCE_ONLY_DISTINCT_V2_MANDATORY_NULL_SOURCE_REPAIR','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'builder_executed':False,'ROOT_operator_executed':False,'production_import_compile_or_execution':False,'actual_current_freeze':False,'ROOT_approval':None,'current_verdict':None,'full_problem_solved':False,'original_substantive_attempts':1,'new_substantive_attempts':0,'audit_turns':0,'new_whole_current_gate':'PENDING','new_different_clean_SOURCE_adversary':'PENDING','native_mirror_disposition':'PENDING','foreign_bodies_copied':False,'closed_adverse_manifest_sha256':'ed0aba6a7a42e752012399daed24d460e25108afd7b66c89ee1907473eb76a85'}
    put(F/'SOURCE_STATUS.json',enc(status))
    put(F/'SOURCE_PREPARATION_RESEARCH_LOG.md',(status['created_utc']+' — Distinct SOURCE V2 authoring80%; actual current freeze0%; target discovery0%. Closed V1 and ADVERSE full read; one administrative capture-class repair. Production never imported, compiled or executed. Original1/5,new0,audit0; all genuine ROOT prerequisites and fresh reviews pending.\n'+suffix).encode())
    put(F/'AUTHORING_RESULT.json',enc({'schema':'PR47_SOURCE_V2_AUTHORING_RESULT_v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_authoring_pid':os.getpid(),'full_predecessor_body_reads':reads,'full_predecessor_read_bytes':sum(r['bytes'] for r in reads),'production_import_compile_or_execution':False,'builder_text_sha256':sha(raw(F/'prepare_current_packet.py')),'operator_text_sha256':sha(raw(F/'capture_root_builder_operation.py')),'original_and_historical_bytes_mutated':False,'new_SOURCE_clean_review':'PENDING'}))
    print(json.dumps({'status':'DISTINCT_SOURCE_V2_AUTHORED_TEXT_ONLY','builder_sha256':sha(raw(F/'prepare_current_packet.py')),'operator_sha256':sha(raw(F/'capture_root_builder_operation.py')),'predecessor_files_read':len(reads),'production_executed':False}))
if __name__=='__main__': main()
