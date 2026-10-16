"""Independent bounded private models; reviewed sources are read as text only."""
from pathlib import Path, PurePosixPath
import copy, datetime as dt, hashlib, json, math, os, re, stat
F=Path(__file__).absolute().parent; A=F.parent; R=F.parents[3]; S=A/'acceptance_preparation_family'; C=A/'reviewed_candidate'
observations=[]; assertions=0
def need(v,m):
    global assertions
    assertions+=1
    if not v: raise ValueError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def equal(a,b):
    if type(a) is not type(b): return False
    if type(a) is dict: return a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a)
    if type(a) is list: return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
    return a==b
def parse(b):
    def pairs(v):
        d={}
        for k,x in v: need(k not in d,'Duplicate key'); d[k]=x
        return d
    def fl(s): x=float(s); need(math.isfinite(x),'Finite scalar'); return x
    return json.loads(b,object_pairs_hook=pairs,parse_float=fl,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def load(p): return parse(p.read_bytes())
def rel(n):
    need(type(n) is str and n and n!='.' and '\\' not in n and '\0' not in n,'Literal path')
    p=PurePosixPath(n); need(not p.is_absolute() and p.as_posix()==n and not {'.','..','.git','__pycache__'}.intersection(p.parts),'Canonical path'); return n
def reject(label,fn):
    try: fn()
    except (ValueError,TypeError,KeyError,IndexError,OSError,json.JSONDecodeError) as e: observations.append({'label':label,'expected_rejected':True,'exception':type(e).__name__,'message':str(e)})
    else: raise ValueError('Failed negative control '+label)
def emit(n,o):
    with (F/n).open('xb') as h: h.write((json.dumps(o,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()); h.flush(); os.fsync(h.fileno())
def typed_ref(z):
    need(type(z) is dict and set(z)=={'path','bytes','sha256'},'Exact three-field row'); rel(z['path']); need(type(z['bytes']) is int and z['bytes']>=0 and type(z['sha256']) is str and re.fullmatch('[0-9a-f]{64}',z['sha256']),'Typed row values')
inputs=load(S/'INPUT_BINDINGS.json')
native={z['path'] for z in inputs['dated_native13']}; ap=A.relative_to(R).as_posix()+'/'; cp='unsolved_math_prioritization/attempts/2961/'; program='draft_pr_publication_program_20260930/RESEARCH_LOG.md'
def owned(n): rel(n); return n in native or n==program or n.startswith(ap) or n.startswith(cp)
def foreign(ns):
    need(type(ns) is list and all(type(n) is str for n in ns) and ns==sorted(set(ns)),'Sorted distinct foreign identities'); need(all(not owned(n) for n in ns),'Foreign excludes owned')
def ledger(raw,used,limit):
    need(type(raw) is bytes and raw==literal and raw.endswith(b'\n') and type(used) is int and type(limit) is int and used==2 and limit==5,'Exact original shared budget'); z=[parse(b) for b in raw.splitlines()]; need(equal(z,events) and len(z)==2 and all(type(x['turn']) is int for x in z) and [x['turn'] for x in z]==[1,2],'Exact two literal turns')
literal=(C/'turns.jsonl').read_bytes(); events=load(S/'EXPECTED_ORIGINAL_LEDGER.json')
def exact_post(root,post,contract):
    need(type(root) is dict and set(root)==set(contract['future48_required_ROOT_complete_keyset']),'ROOT22 exact keyset'); need(root['schema']==contract['future48_required_ROOT_schema'],'ROOT schema')
    for k,v in contract['future48_required_completed_values'].items(): need(k in root and equal(root[k],v),'Typed mandatory ROOT field '+k)
    need(equal(root['entire_post'],post),'Entire typed post equality')
    for k,v in contract['future48_required_entire_post_values'].items(): need(k in post and equal(post[k],v),'Typed mandatory post field '+k)
def inventory(before):
    need(type(before) is dict and type(before['items']) is list and len(before['items'])==180 and all(type(x) is dict and type(x['number']) is int for x in before['items']),'Inventory types')
    ids=[x['number'] for x in before['items']]; need(len(set(ids))==180 and ids.count(48)==1 and type(before['completed_count']) is int and before['completed_count']==37 and sum(x['stage']=='complete' for x in before['items'])==37,'37 actual predecessor primaries')
    out=copy.deepcopy(before); chosen=next(x for x in out['items'] if x['number']==48); need(chosen['stage']!='complete','Selected incomplete'); chosen.update(stage='complete',original_attempts='2/5',outcome='unsolved_accepted_partial'); out.update(completed_count=38,current_pr=49,completion_estimate_percent=38*100/180); return out
def queue_transition(before):
    need(type(before) is bytes and before.endswith(b'\n'),'Whole queue bytes'); text=before.decode(); lines=text.splitlines(keepends=True)
    need(not any(len(s.split('|'))==14 and s.split('|')[2].strip().startswith('30004403 / ') for s in lines),'Alias QUEUE absent')
    indices=[i for i,s in enumerate(lines) if len(s.split('|'))==14 and s.split('|')[2].strip()=='2961 / KP-4.85']; need(len(indices)==1,'Unique selected primary row'); i=indices[0]; cells=lines[i].rstrip('\n').split('|'); need(cells[8].strip()=='queued' and cells[9].strip()=='0/5','Original queue status/turns')
    old=list(cells); cells[8]=' unsolved '; cells[9]=' 2/5 '; cells[11]=' Included subgroup all-powers bound4 and signed averaging route obstruction; full target unsolved. '; need(all(cells[j]==old[j] for j in range(14) if j not in {8,9,11}),'Only Status/Turns/Findings'); lines[i]='|'.join(cells)+'\n'; after=''.join(lines).encode(); return after,old,cells
def prefix(logs,before,note,modes):
    need(type(logs) is list and len(logs)==2,'Exactly two owned logs')
    for z,p,b,m in zip(logs,[ap+'ROOT_RESEARCH_LOG.md',program],before,modes):
        need(set(z)=={'path','before','after','mode'} and z['path']==p and z['before']==b.hex() and z['after']==(b+note).hex() and type(z['mode']) is int and z['mode']==m,'Literal full prefix+note+mode')
def private_atomic_body_replace(target,body,preserve=False):
    # Independently handwritten the OS-level two-file operation identified by source reading.
    before=stat.S_IMODE(target.stat().st_mode); staged=target.with_name(target.name+'.independent-temp')
    with staged.open('xb') as h: h.write(body); h.flush(); os.fsync(h.fileno())
    if preserve: staged.chmod(before)
    os.replace(staged,target); return before,stat.S_IMODE(target.stat().st_mode)
def main():
    need(len(native)==13,'Exact native13 source identities')
    sources={n:(S/n).read_bytes() for n in ['pr48_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py','capture_root_final_operation.py']}
    g=sources['pr48_guards.py'].decode(); need('os.replace(tmp,p)' in g and 'native_modes(remaining)' in g and "if z['path'] not in allowed" in g,'Text basis for replacement and allowed skip')
    foreign(['README.md','draft_pr_publication_program_20260930/other_notes.md',ap[:-1]+'-foreign/LOG.md',cp[:-1]+'0/PARTIAL.md'])
    for n in sorted(native|{program,ap+'ROOT_RESEARCH_LOG.md',cp+'PARTIAL.md'}): reject('owned_excluded_as_foreign:'+n,lambda n=n:foreign([n]))
    for ns in [['a','a'],['z','a'],[True],['../README.md']]: reject('foreign_shape:'+repr(ns),lambda ns=ns:foreign(ns))
    for s in ['.','../x','x/../y','a//b','./a','/a','a\\b','a\0b','.git/x','__pycache__/x']: reject('path:'+repr(s),lambda s=s:rel(s))
    for b in [b'{"k":1,"k":2}',b'{"k":NaN}',b'{"k":Infinity}',b'{"k":1e999}']: reject('JSON:'+repr(b),lambda b=b:parse(b))
    z={'path':'member','bytes':2,'sha256':sha(b'ab')}; typed_ref(z)
    for field,v in [('bytes',True),('bytes',2.0),('path','./member'),('sha256','0'*63),('extension',1)]: t=copy.deepcopy(z); t[field]=v; reject('reference:'+field+repr(v),lambda t=t:typed_ref(t))
    need(not equal(True,1) and not equal(None,False) and not equal([2],[2.0]),'Recursive scalar distinctions')
    ledger(literal,2,5)
    for b,u,l in [(literal,True,5),(literal,2.0,5),(literal,3,5),(literal,2,4),(literal+b'{}\n',2,5),(literal.rstrip(b'\n'),2,5),(b'',2,5)]: reject('ledger:'+repr((len(b),u,l)),lambda b=b,u=u,l=l:ledger(b,u,l))
    cells=['',' 42 ',' 2961 / KP-4.85 ',' category ',' owner ',' model ',' seed ',' route ',' queued ',' 0/5 ',' [chat](keep://literal) ',' old finding ',' 10.000/example ','']; selected=('|'.join(cells)+'\n').encode(); before=b'PREFIX EXACT\n'+selected+b'| other | 42 / KP-x | untouched |\nTAIL\n'; after,old,new=queue_transition(before)
    need(after.startswith(b'PREFIX EXACT\n') and after.endswith(b'| other | 42 / KP-x | untouched |\nTAIL\n') and old[10]==new[10] and old[12]==new[12],'Every nonselected row/prefix and literal Chat DOI preserved')
    reject('queue_alias_inserted',lambda:queue_transition(before+selected.replace(b'2961 / KP-4.85',b'30004403 / OWR-17471-009')))
    reject('queue_duplicate_primary',lambda:queue_transition(before+selected)); reject('queue_turn_typed_text_changed',lambda:queue_transition(before.replace(b' 0/5 ',b' 1/5 ')))
    inv={'items':[{'number':i,'stage':'complete' if i<=37 else 'pending','opaque':{'nested':[i,None,False]}} for i in range(1,181)],'completed_count':37,'opaque':'retained'}; out=inventory(inv)
    need(all(equal(x,y) for x,y in zip(inv['items'],out['items']) if x['number']!=48) and out['opaque']=='retained' and out['completion_estimate_percent']==21.11111111111111 and out['current_pr']==49,'All179 untouched inventory objects and exact38/180')
    for field,v in [('completed_count',True),('completed_count',36)]: t=copy.deepcopy(inv); t[field]=v; reject('inventory:'+field+repr(v),lambda t=t:inventory(t))
    t=copy.deepcopy(inv); t['items'][47]['number']=True; reject('inventory_boolean_identity',lambda:inventory(t)); t=copy.deepcopy(inv); t['items'][47]['number']=47; reject('inventory_duplicate_identity',lambda:inventory(t))
    cm=load(C/'MANIFEST.json'); frozen={z['path'] for z in cm['files']}; admin=['status.json','readiness.json','review/verdict.json','review/review_summary.json']; overlay=frozen|{'reviewed_pending_administration/'+n for n in admin}|{'reviewed_pending_administration/MANIFEST.json','ACCEPTED_QUEUE_PATCH.json','CURRENT_ACCEPTANCE_SCOPE.md','CURRENT_CONTEXT_PRESENT.md','CURRENT_AUDIT_SCOPE_PRESENT.md'}
    need(len(overlay)==1955 and len(overlay|{'acceptance.json','ACCEPTANCE.md','MANIFEST.json'})==1958,'Canonical1955 overlay and1957payload+self distinct')
    contract=load(S/'ROOT_POST_CONTRACT.json'); need(len(contract['future48_required_ROOT_complete_keyset'])==22,'Actual closed ROOT22 contract'); post=copy.deepcopy(contract['future48_required_entire_post_values']); root={k:None for k in contract['future48_required_ROOT_complete_keyset']}; root.update(contract['future48_required_completed_values'],schema=contract['future48_required_ROOT_schema'],entire_post=post); exact_post(root,post,contract)
    for k in root: t=copy.deepcopy(root); t.pop(k); reject('ROOT22_missing:'+k,lambda t=t:exact_post(t,post,contract))
    t=copy.deepcopy(root); t['unexpected']=False; reject('ROOT22_extension',lambda:exact_post(t,post,contract))
    for k,v in [('completed_primary_prs',True),('original_attempts',2.0),('program_completion_percent',21),('full_problem_solved',True),('audit_turns',False)]: t=copy.deepcopy(root); t[k]=v; reject('ROOT22_scalar:'+k,lambda t=t:exact_post(t,post,contract))
    prefixes=[b'COMPLETE A48 PREFIX\n',b'COMPLETE PROGRAM PREFIX\n']; note=b'\nFIXED UTC-DERIVED NOTE\n'; modes=[0o644,0o600]; logs=[{'path':p,'before':b.hex(),'after':(b+note).hex(),'mode':m} for p,b,m in zip([ap+'ROOT_RESEARCH_LOG.md',program],prefixes,modes)]; prefix(logs,prefixes,note,modes)
    for j in range(2):
        for k,v in [('path','README.md'),('before',b'truncated'.hex()),('after',b'wrong note'.hex()),('mode',True),('mode',0o755)]: t=copy.deepcopy(logs); t[j][k]=v; reject('log:'+str(j)+':'+k+repr(v),lambda t=t:prefix(t,prefixes,note,modes))
    reject('log_third_append',lambda:prefix(logs+[logs[0]],prefixes,note,modes))
    d=F/'private_mode_countermodels'; d.mkdir(); oldmask=os.umask(0o022); results=[]
    try:
        for n in ['QUEUE.md','inventory.json','state.json','history.jsonl']:
            p=d/n; p.write_bytes(b'original body\n'); p.chmod(0o600); beforemode,aftermode=private_atomic_body_replace(p,b'allowed new body\n')
            need(beforemode==0o600 and aftermode==0o644 and p.read_bytes()==b'allowed new body\n','Actual nonexclusive replace resets valid arbitrary fresh mode')
            results.append({'private_path':p.relative_to(F).as_posix(),'before_full_mode':beforemode,'after_full_mode':aftermode,'umask':0o022,'production_executed':False,'new_body_correct':True,'mode_preserved':False})
        p=d/'fixed_preserve600.bin'; p.write_bytes(b'before'); p.chmod(0o600); bm,am=private_atomic_body_replace(p,b'after',preserve=True); need(bm==am==0o600,'Independent staged mode preservation repair mechanism')
        p=d/'domain0644.bin'; p.write_bytes(b'before'); p.chmod(0o644); bm,am=private_atomic_body_replace(p,b'after'); need(bm==am==0o644,'Nominal0644/umask0022 domain remains sound')
    finally: os.umask(oldmask)
    emit('PRIVATE_MODE_COUNTERMODEL.json',{'schema':'pr48-independent-native-mode-countermodel/v1','actual_pid':os.getpid(),'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'source_guard_sha256':sha(sources['pr48_guards.py']),'method':'Independent OS-level model of newly created fsynced temp followed by os.replace; no production execution','rows':results,'mandatory_scope_correction':'Preserve the preimage full mode on each mutable native replacement, or restrict and recheck the supported source/runtime domain explicitly. Existing source permits fresh0600 but silently produces0644 for all four body updates under umask0022.','actual0644_domain_counterexample':False,'preserve_mode_repair_model_passed':True,'SOURCE_imported_compiled_executed':False})
    # A metadata-count predicate cannot distinguish six references to one phase.
    # This is a toy, never a genuine capture or approval; full ROOT role reading is still required by the contract.
    toy={'role':'preflight','private_model_only':True}; repeated=[toy]*6
    need(type(repeated) is list and len(repeated)>=6,'Literal len>=6 predicate accepts repetition'); need(len({x['role'] for x in repeated})==1,'Private repetition does not provide all six roles')
    emit('PRIVATE_COUNTERMODEL_OBSERVATIONS.json',observations)
    result={'schema':'pr48-independent-acceptance-source-private-controls/v1','status':'PASS_PRIVATE_CONTROLS_WITH_NATIVE_MODE_DEFECT','actual_pid':os.getpid(),'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'assertions':assertions,'expected_negative_controls':len(observations),'actual_private_mode_countermodels':4,'mandatory_mode_correction_identified':True,'guard_capture_distinct_roles_automated':False,'complete_ROOT_capture_role_reading_still_required':True,'source_sha256':{n:sha(b) for n,b in sources.items()},'source_imported_compiled_executed':False,'native_index_remote_mutated':False,'future_acceptance_approved':False,'countermodels_are_production_execution_tests':False}; emit('PRIVATE_CONTROLS_RESULT.json',result); print(json.dumps(result,sort_keys=True))
if __name__=='__main__': main()
