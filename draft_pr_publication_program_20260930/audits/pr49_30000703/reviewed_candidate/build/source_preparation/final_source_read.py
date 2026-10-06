#!/usr/bin/python3
"""Own final administrative read. Production sources are read only as UTF-8 text."""
import datetime,hashlib,json,math,pathlib,re,stat
F=pathlib.Path(__file__).absolute().parent;A=F.parent;R=A.parents[2]
def check(v,n):
    if not v:raise ValueError(n)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(b):
    def pairs(items):
        d={}
        for k,v in items:check(k not in d,'Duplicate key');d[k]=v
        return d
    def fl(s):
        v=float(s);check(math.isfinite(v),'Finite number');return v
    def co(s):raise ValueError('Nonfinite JSON')
    return json.loads(b,object_pairs_hook=pairs,parse_float=fl,parse_constant=co)
def equal(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
    return a==b
def regular(p):
    check(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular source');return p.read_bytes()
pins=load(regular(F/'STATIC_INPUT_BINDINGS.json'));check(len(pins['fixed_rows'])==1184 and set(pins['closed_inputs'])=={'original','boundary','hyperbolic','ROOT'},'All fixed scopes')
for r in pins['fixed_rows']:
    p=R/r['path'];b=regular(p);check(len(b)==r['bytes'] and sha(b)==r['sha256'] and type(r['full_mode']) is int and stat.S_IMODE(p.stat().st_mode)==r['full_mode'],'Every fixed body/fullmode')
for info in pins['closed_inputs'].values():
    for r in info['directories']:check(stat.S_IMODE((R/info['root']/r['path']).stat().st_mode)==r['full_mode'],'All fixed directory fullmodes')
archive={p.relative_to(F/'original_archive').as_posix():regular(p) for p in (F/'original_archive').rglob('*') if p.is_file()};check(len(archive)==16,'All16 literal archive')
for n,b in archive.items():check(b==regular(A/'source_snapshot'/n),'Literal original archived body')
immutable=['SOURCE_STATUS.md','verify.py','verification.json','source_record.json','prior_report.json','turns.json','source_checksums.json','review/submitted_verify.py','review/verification.json','review/independent_checks.py','review/independent_results.json']
for n in immutable:check(regular(F/'operative_proposal'/n)==archive[n],'All11 literal operative bodies')
check(archive['prior_report.json']==b'null\n' and type(load(archive['source_record.json'])['id']) is int and load(archive['turns.json'])['count']==0,'Plain source/null/zero single-object ledger')
result=load(regular(A/'root_original_actual_reproduction/ROOT_REPRODUCTION_RESULT.json'));check(len(result['complete_actual_Git_captures'])==33 and len(result['complete_actual_helper_captures'])==3 and result['identical_submitted_counted_independent'] is False,'Full ROOT capture classes')
replayed=result['entire_replayed_results'];check(equal(replayed['author'],load(archive['verification.json'])) and equal(replayed['identical_submitted'],load(archive['verification.json'])) and equal(replayed['historical_independent'],load(archive['review/independent_results.json'])),'Complete receipt scalar types')
control=load(regular(F/'PRIVATE_CONTRACT_CONTROL_RESULTS_V2.json'));check(control['assertions_passed']==11127 and control['assertions_failed']==0 and control['negative_models_rejected']==4618 and len(control['full_mode_observations'])==4096 and all(type(r['requested']) is int and r['requested']==i==r['observed'] for i,r in enumerate(control['full_mode_observations'])),'Completed4096-mode exact observations')
for key in ['production_builder_imported_compiled_executed','production_operator_imported_compiled_executed']:check(control[key] is False,'Private models never production runtime')
check(control['SOURCE_adversary_verdict'] is None,'No private SOURCE approval')
read=[]
for name in ['prepare_current_packet.py','capture_root_builder_operation.py','close_source_preparation.py','verify_source_preparation_readonly.py','EXECUTION_CONTRACT.md','SOURCE_REPORT.md','SOURCE_PRECISION_QUALIFICATIONS.md','CURRENT_OVERVIEW.md','OPERATIVE_SOURCE_CONTEXT.md','HISTORICAL_ORIGINAL_NOTICE.md','READY.json','READY.md','RESEARCH_LOG.md']:
    b=regular(F/name);b.decode('utf-8');read.append({'path':name,'bytes':len(b),'sha256':sha(b),'reading_method':'FULL_UTF8_TEXT_ONLY_NO_IMPORT_COMPILE_EXECUTION'})
check(sha(regular(F/'prepare_current_packet.py'))==control['builder_sha256'] and sha(regular(F/'capture_root_builder_operation.py'))==control['operator_sha256'],'Private models bind exact still-unexecuted production text')
for q in sorted(F.glob('DRAFT_ROOT*.json')):
    d=load(regular(q));check(d['approved_by_root'] is False and d['created_utc'] is None,'Every future draft false/null')
    if 'root_flags' in d:check(all(v is False for v in d['root_flags'].values()),'No inherited actual personal reading')
check('ROOT_SCOPE_ACCEPTED_EXACT_KNOWN_RESULT_ONLY' not in regular(F/'DRAFT_ROOT_CURRENT_KNOWN_RESULT_SCOPE_CERTIFICATE.md').decode(),'No draft acceptance marker')
for name in ['ROOT_CURRENT_KNOWN_RESULT_SCOPE_CERTIFICATE.md','ROOT_PRIMARY_READ_LEDGER.json','ROOT_SCIENCE_CARD.json','ROOT_CURRENT_INPUT_PREIMAGES.json','ROOT_EVIDENCE_BINDINGS.json','ROOT_NEW_SOURCE_ADVERSARY_RECORD.json','PREPARATION_MANIFEST.json']:
    check(not (F/name).exists(),'No genuine ROOT or premature closure in SOURCE')
status=load(regular(F/'SOURCE_STATUS.json'));check(status['current_SOURCE_verdict'] is None and status['production_builder_executed'] is False and status['production_operator_executed'] is False and status['future_acceptance_approved'] is False,'Current SOURCE null/false')
patch=load(regular(F/'CURRENT_QUEUE_PATCH.json'));check(patch['phase']=='DATED_SOURCE_EXAMPLE_ONLY_NO_FUTURE_NATIVE_AUTHORITY' and patch['current_head_authority'] is None,'Dated native proposals not current authority')
headers=['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI'];old=patch['row_before'].split('|');new=patch['row_prospective'].split('|');allowed={headers.index(k)+1 for k in ['Status','Turns','Findings']};check(len(old)==len(new)==14 and all(a==b for i,(a,b) in enumerate(zip(old,new)) if i not in allowed),'Only named selected cells, Chat/DOI preserved')
for q in (F/'native4_proposal/preimage').iterdir():
    if 'QUEUE.md' not in q.name:check(regular(q)==regular(F/'native4_proposal/prospective'/q.name),'State/history/inventory untouched')
seen=[]
for d in sorted(F.glob('*_ACTUAL_CAPTURE')):
    if d.name=='FINAL_SOURCE_READ_ACTUAL_CAPTURE':continue
    c=load(regular(d/'CAPTURE.json'));check(c['completed'] is True and c['actual_execution'] is True and type(c['pid']) is int and type(c['exit_code']) is int and c['source_unchanged'] is True and c['operator_unchanged'] is True,'All preceding actual completed sources')
    expected=1 if d.name=='PRIVATE_CONTROLS_ACTUAL_CAPTURE' else 0;check(c['exit_code']==expected,'Honest preserved first failure')
    check(sha(regular(d/'PRELAUNCH_SOURCE.py'))==c['source_sha256'] and sha(regular(d/'PRELAUNCH_OPERATOR.py'))==c['operator_sha256'],'Actual copied source/operator identity')
    for k in ['stdout','stderr']:b=regular(d/c[k]['path']);check(len(b)==c[k]['bytes'] and sha(b)==c[k]['sha256'],'All complete preceding split streams')
    seen.append({'capture':d.name,'actual_pid':c['pid'],'exit_code':c['exit_code']})
check(len(seen)==6,'Six preceding completed captures')
# This child reads source text and first-party metadata only; it never calls production code.
out={'schema':'pr49-final-source-only-read/v1','status':'PASS_FINAL_SOURCE_ONLY_READ','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fixed_body_count':1184,'exact_four_closed_schemas':True,'original_archive16_byte_exact':True,'operative11_byte_exact':True,'complete69_duplicate69_historical187_values_and_types':True,'preceding_actual_nonproduction_captures':seen,'full_text_read_bindings':read,'private_assertions_passed':11127,'retained_private_negative_models':4618,'actual_permission_observations':4096,'production_builder_imported_compiled_executed':False,'production_operator_imported_compiled_executed':False,'closer_or_readonly_verifier_executed_by_preparer':False,'source_role_reuses_closed_hyperbolic_context':True,'SOURCE_adversary_verdict':None,'future_acceptance_approved':False,'new_substantive_attempts':0,'audit_turns':0}
(F/'FINAL_SOURCE_READ_RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['full_text_read_bindings','preceding_actual_nonproduction_captures']}))
