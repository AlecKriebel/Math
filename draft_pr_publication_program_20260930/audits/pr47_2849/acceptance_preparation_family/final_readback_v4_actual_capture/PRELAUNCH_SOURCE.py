"""Handwritten private predicates/fixtures; no production import, parse or compile."""
import copy, ctypes, datetime as dt, hashlib, json, math, os, stat
from pathlib import Path, PurePosixPath
F=Path(__file__).absolute().parent;A=F.parent;R=F.parents[3]
COUNT=0; NEGATIVE=0
def need(ok,msg):
    global COUNT
    COUNT+=1
    if not ok:raise ValueError(msg)
def reject(f,*args):
    global NEGATIVE
    try:f(*args)
    except (ValueError,TypeError,KeyError,FileNotFoundError):NEGATIVE+=1
    else:raise ValueError('Malformed control accepted')
def typed(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return a.keys()==b.keys() and all(typed(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(typed(x,y) for x,y in zip(a,b))
    return a==b
def parse(b):
    def pairs(x):
        d={}
        for k,v in x:need(k not in d,'duplicate');d[k]=v
        return d
    def floating(x):
        z=float(x);need(math.isfinite(z),'finite');return z
    return json.loads(b,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def sha(b):return hashlib.sha256(b).hexdigest()
def path(n):
    need(type(n) is str and n and '\\' not in n and '\0' not in n,'path type');p=PurePosixPath(n);need(not p.is_absolute() and p.as_posix()==n and not {'.','..','.git','__pycache__'}.intersection(p.parts) and n!='.','canonical');return p
def ref(z):
    need(type(z) is dict and set(z)=={'path','bytes','sha256'},'ref keys');path(z['path']);need(type(z['bytes']) is int and z['bytes']>=0,'int byte count');need(type(z['sha256']) is str and len(z['sha256'])==64 and set(z['sha256'])<=set('0123456789abcdef'),'sha');return z
def capture(z,kind,argv):
    keys={'schema','argv','cwd','started_utc','actual_operator_pid','stdin_supplied','source','actual_execution','pid','completed','exit_code','finished_utc','stdout','stderr','source_unchanged'}
    need(type(z) is dict and set(z)==keys and z['schema']=='pr47-root-literal-operation-capture/v1','capture schema');need(typed(z['argv'],argv) and z['cwd']==str(R),'literal argv/cwd')
    for n in ['actual_operator_pid','pid']:need(type(z[n]) is int and z[n]>0,'positive actual PID')
    need(type(z['exit_code']) is int and z['exit_code']==0 and z['stdin_supplied'] is False and z['actual_execution'] is True and z['completed'] is True,'capture scalar types')
    clocks=[]
    for n in ['started_utc','finished_utc']:
        need(type(z[n]) is str,'clock string');c=dt.datetime.fromisoformat(z[n]);need(c.tzinfo is not None and c.utcoffset()==dt.timedelta(0),'UTC');clocks.append(c)
    need(clocks==sorted(clocks),'clock order')
    for n in ['stdout','stderr']:ref(z[n]);p=R/z[n]['path'];need(p.is_file() and not p.is_symlink(),'stream regular');b=p.read_bytes();need(len(b)==z[n]['bytes'] and sha(b)==z[n]['sha256'],'complete stream')
    need((R/z['stderr']['path']).read_bytes()==b'','complete stderr')
    if kind=='Git':need(z['source'] is None and z['source_unchanged'] is None,'Git null/null')
    else:ref(z['source']);need(z['source_unchanged'] is True,'helper true');b=(R/z['source']['path']).read_bytes();need(len(b)==z['source']['bytes'] and sha(b)==z['source']['sha256'],'complete typed helper source')
def owned(n):
    path(n);return n=='draft_pr_publication_program_20260930/RESEARCH_LOG.md' or n.startswith(A.relative_to(R).as_posix()+'/') or n.startswith('unsolved_math_prioritization/attempts/2849/') or n in {'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
def foreign(v):
    need(type(v) is list and all(type(n) is str for n in v) and v==sorted(set(v)),'sorted foreign');need(all(not owned(n) for n in v),'owned excluded');return True
def append_guard(prefix,after,note,before_mode,after_mode):
    need(type(prefix) is bytes and type(after) is bytes and type(note) is str and after==prefix+note.encode(),'exact prefix+note');need(type(before_mode) is int and type(after_mode) is int and 0<=before_mode<=4095 and before_mode==after_mode,'exact mode')
def predecessor(o):
    need(type(o) is dict and set(o)=={'completed','pr','targets','turns','primary','duplicate','inventory','proofs','paper'},'predecessor schema');need(typed(o,{'completed':True,'pr':46,'targets':37,'turns':44,'primary':36,'duplicate':1,'inventory':36,'proofs':0,'paper':False}),'actual completed predecessor only')
def write(n,o):
    with (F/n).open('xb') as s:s.write((json.dumps(o,indent=2,sort_keys=True)+'\n').encode());s.flush();os.fsync(s.fileno())
def main():
    source=(F/'pr47_guards.py').read_text();contract=parse((F/'ROOT_POST_CONTRACT.json').read_bytes())
    # Textual conditions catch adaptation defects, without evaluating production.
    need("identities.count(47)==1" in source,'SOURCE selected identity must47')
    need("contract['required_ROOT_complete_keyset']" in source and "contract['required_entire_post_values']" in source,'SOURCE actual predecessor contract field names')
    need("canonical1339_plus_manifest_fullbytes_modes" in contract['future47_required_ROOT_complete_keyset'],'SOURCE exact accepted payload count')
    need("merge1337_overlay_plus_queue_Git_bodies_and_parents" in contract['future47_required_ROOT_complete_keyset'],'SOURCE exact overlay count')
    need(contract['future47_required_entire_post_values']['pr']==47,'SOURCE correct selected post PR')
    for name in ['pr47_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py','capture_root_final_operation.py']:
        text=(F/name).read_text();need('import pr45' not in text and '9900007' not in text and 'AMR-098' not in text,'no wrong source scope');need('compile(' not in text and 'eval(' not in text and 'exec(' not in text,'no production bypass')
    need('protected_foreign_paths(fresh)' in source and "paths=protected_foreign_paths(fresh)" in source,'foreign filtering repeats');need("ADDITIONAL_OWNED_MUTATION_PATHS={PROGRAM_LOG.relative_to(R).as_posix()}" in source,'only exact program log');need("before==after==stat.S_IMODE" in source,'fullmode log guard');need('g.owned_log_append_check(pre)' in (F/'integrate_reviewed_partial.py').read_text() and 'g.owned_log_append_check(pre)' in (F/'state_mirror_reconciliation.py').read_text() and 'g.owned_log_append_check(pre)' in (F/'verify_post_acceptance.py').read_text(),'append verification in three phases')
    originals=parse((A/'snapshot_manifest.json').read_bytes())['files'];record=parse((F/'EXPECTED_ORIGINAL_CAPTURE_RESULT.json').read_bytes());expected=[]
    for z in originals:expected += [['git','show','487327b2412c436ae69e8c52bf353a9a1fb7594e:'+z['path']],['git','ls-tree','487327b2412c436ae69e8c52bf353a9a1fb7594e','--',z['path']]]
    expected += [['git','diff','--no-ext-diff','--no-textconv','--binary','c6975ca76f9f667f1250ba403d0e6da2aafe14d0','487327b2412c436ae69e8c52bf353a9a1fb7594e','--']]
    need(len(expected)==33 and len(record['complete_actual_Git_captures'])==33,'33 actual Git')
    for z,argv in zip(record['complete_actual_Git_captures'],expected):
        capture(z,'Git',argv)
        for key,value in [('pid',True),('exit_code',False),('source',{}),('source_unchanged',True),('completed',1),('stdin_supplied',None),('argv',argv+['--unexpected'])]:
            mutant=copy.deepcopy(z);mutant[key]=value;reject(capture,mutant,'Git',argv)
        mutant=copy.deepcopy(z);mutant['argv']=record['complete_actual_helper_captures'][0]['argv'];reject(capture,mutant,'Git',argv)
    for z in record['complete_actual_helper_captures']:
        capture(z,'helper',z['argv'])
        for k,v in [('source',None),('source_unchanged',None),('pid',True),('exit_code',False)]:m=copy.deepcopy(z);m[k]=v;reject(capture,m,'helper',z['argv'])
    need(typed(1,True) is False and typed(0,False) is False and typed(None,{}) is False and typed('1',1) is False,'recursive scalar types')
    for b in [b'{"a":1,"a":2}',b'NaN',b'Infinity',b'1e9999']:reject(parse,b)
    for n in ['.','../x','/x','a//b','a/./b','a/../b','a\\b','a\0b','.git/config','__pycache__/x']:reject(path,n)
    good=['draft_pr_publication_program_20260930/OTHER.md','draft_pr_publication_program_20260930/audits/pr48_2961/RESEARCH_LOG.md','unsolved_math_prioritization/attempts/2850/README.md'];foreign(sorted(good))
    for n in ['draft_pr_publication_program_20260930/RESEARCH_LOG.md',A.relative_to(R).as_posix()+'/ROOT_RESEARCH_LOG.md','unsolved_math_prioritization/attempts/2849/x']:reject(foreign,[n])
    for n in ['draft_pr_publication_program_20260930/RESEARCH_LOG.md.backup','draft_pr_publication_program_20260930/sub/RESEARCH_LOG.md','draft_pr_publication_program_20260930/audits/pr47_28490/x']:need(not owned(n),'adjacent paths stay foreign')
    prefix=b'Full previous research log\n';note='\nExact fixed acceptance append\n';append_guard(prefix,prefix+note.encode(),note,0o644,0o644)
    for args in [(prefix,prefix[:-1]+note.encode(),note,0o644,0o644),(prefix,prefix+note.encode()+b'x',note,0o644,0o644),(prefix,prefix+note.encode(),note,True,1),(prefix,prefix+note.encode(),note,0o644,0o444)]:reject(append_guard,*args)
    previous={'completed':True,'pr':46,'targets':37,'turns':44,'primary':36,'duplicate':1,'inventory':36,'proofs':0,'paper':False};predecessor(previous)
    for k,v in [('completed',False),('completed',1),('pr',45),('targets',36),('turns',45),('primary',35),('duplicate',0),('inventory',37),('proofs',True),('paper',True)]:m=copy.deepcopy(previous);m[k]=v;reject(predecessor,m)
    fixture=F/'private_fixtures';fixture.mkdir(exist_ok=False);modefile=fixture/'mode_file.bin';modefile.write_bytes(b'actual permission-bit control\n');modes=[]
    for m in range(4096):
        modefile.chmod(m);got=stat.S_IMODE(modefile.stat().st_mode);need(got==m,'actual all4096 modes');need((got==0o444)==(m==0o444),'special bits not low-bit masked');modes.append({'requested':m,'actual':got})
    modefile.chmod(0o600);write('ALL_4096_ACTUAL_FULL_MODES.json',modes)
    staged=fixture/'staged.bin';staged.write_bytes(b'full completed bytes');target=fixture/'target.bin';os.link(staged,target,follow_symlinks=False);need(target.read_bytes()==b'full completed bytes','atomic absent publication')
    try:os.link(staged,target,follow_symlinks=False)
    except FileExistsError:need(target.read_bytes()==b'full completed bytes','intervening target retained')
    else:raise ValueError('existing publication overwritten')
    libc=ctypes.CDLL(None,use_errno=True);rename=libc.renamex_np;rename.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint];rename.restype=ctypes.c_int
    stage=fixture/'stage_dir';dest=fixture/'published_dir';stage.mkdir();(stage/'member').write_bytes(b'complete staged directory');need(rename(os.fsencode(stage),os.fsencode(dest),4)==0 and (dest/'member').read_bytes()==b'complete staged directory','actual exclusive macOS directory rename')
    nextstage=fixture/'second_stage';nextstage.mkdir();(nextstage/'member').write_bytes(b'must retain');need(rename(os.fsencode(nextstage),os.fsencode(dest),4)!=0 and (dest/'member').read_bytes()==b'complete staged directory' and (nextstage/'member').read_bytes()==b'must retain','existing directory never replaced')
    link=fixture/'symlink';link.symlink_to(target);need(link.is_symlink(),'actual symlink fixture');fifo=fixture/'fifo';os.mkfifo(fifo);need(stat.S_ISFIFO(fifo.stat().st_mode),'actual FIFO fixture');link.unlink();fifo.unlink();write('SPECIAL_FIXTURE_OBSERVATIONS.json',{'symlink_observed_and_removed':True,'FIFO_observed_and_removed':True,'no_special_member_in_final_family':True})
    for n in ['DRAFT_ROOT_IMMUTABLE_BINDINGS.json','DRAFT_FINAL_PLAN.json','DRAFT_ROOT_PRIMARY_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json','DRAFT_ROOT_SCOPE_CERTIFICATE.json']:
        obj=parse((F/n).read_bytes());need(obj.get('future_acceptance_approved',False) is False,'no future acceptance');need(obj.get('actual_PR46_predecessor_completed',False) is False,'pending46')
    payload=set(z['path'] for z in parse((A/'reviewed_candidate/MANIFEST.json').read_bytes())['files']);admin={'status.json','readiness.json','review/verdict.json','review/review_summary.json'};overlay=payload|{'reviewed_pending_administration/'+n for n in admin}|{'reviewed_pending_administration/MANIFEST.json','ACCEPTED_QUEUE_PATCH.json','CURRENT_ACCEPTANCE_SCOPE.md','CURRENT_CONTEXT_PRESENT.md','CURRENT_AUDIT_SCOPE_PRESENT.md'};accepted=overlay|{'acceptance.json','ACCEPTANCE.md','MANIFEST.json'};need(len(overlay)==1337 and len(accepted-{'MANIFEST.json'})==1339,'actual set-derived counts')
    out={'schema':'pr47-handwritten-private-acceptance-controls/v1','status':'PASS_PRIVATE_PREDICATES_AND_SOURCE_TEXT_ONLY','actual_pid':os.getpid(),'assertions':COUNT,'malformed_cases_rejected':NEGATIVE,'actual_full_modes':4096,'genuine_null_Git_positive':33,'genuine_typed_helper_positive':3,'private_exclusive_macOS_rename':True,'exact_overlay_files':len(overlay),'accepted_payload':len(accepted)-1,'production_imported_compiled_executed':False,'independent_adversarial_review':False,'future_PR46_predecessor_actual':False,'future_acceptance_approved':False}
    write('PRIVATE_CONTROLS_RESULT.json',out);print(json.dumps(out,sort_keys=True))
def final_readback():
    inputs=parse((F/'INPUT_BINDINGS.json').read_bytes());total=0
    need(parse((F/'DRAFT_FINAL_PLAN.json').read_bytes())['pr']==47,'Exact47 draft final plan');need(parse((F/'ROOT_POST_CONTRACT.json').read_bytes())['future47_required_completed_values']['program_completion_percent']==20.555555555555557,'Exact requested binary float percentage')
    for z in list(inputs['pins'].values())+inputs['external_input_rows']:
        p=R/z['path'];need(not p.is_symlink() and all(not x.is_symlink() for x in p.parents) and stat.S_ISREG(p.stat().st_mode),'Full fixed input regular');b=p.read_bytes();need(type(z['bytes']) is int and len(b)==z['bytes'] and sha(b)==z['sha256'],'Every full individual input');need(type(z['full_mode']) is int and stat.S_IMODE(p.stat().st_mode)==z['full_mode'],'Every fixed fullmode');total+=len(b)
    z=inputs['unfinished_design_reference'];b=(R/z['path']).read_bytes();need(len(b)==z['bytes'] and sha(b)==z['sha256'],'Unfinished design body; mode is dated only')
    source=(F/'pr47_guards.py').read_text();need("cp.parent.name=='acceptance_preparation_family_v2'" in source and 'Closed corrected46V2 log contract, rejectedV1 cannot confer authority' in source,'New corrected predecessor46 source required');need('Complete real predecessor prelaunch source/operator' in source and 'Real predecessor source argv whitelist' in source,'Actual complete predecessor sources/operators/argv/chronology');need("identities.count(47)==1" in source,'Selected47 only');need("expected.append(['git','diff','--no-ext-diff','--no-textconv','--binary',ORIGINAL_BASE,HEAD,'--'])" in source,'Exact33Git binary diff whitelist')
    sources=['pr47_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py','capture_root_final_operation.py','close_source.py','verify_closed_source.py'];bindings={}
    for n in sources:
        b=(F/n).read_bytes();need(b and b'compile(' not in b and b'eval(' not in b and b'exec(' not in b,'Read complete source without evaluating it');bindings[n]={'bytes':len(b),'sha256':sha(b),'lines':len(b.splitlines())}
    codes={'inspect_inputs_v1_actual_capture':0,'author_sources_v1_actual_capture':0,'private_controls_v1_actual_capture':1,'repair_sources_v2_actual_capture':0,'private_controls_v2_actual_capture':0,'expected_negative_actual_capture':1,'harden_sources_v3_actual_capture':0,'precision_sources_v4_actual_capture':0};captures=[]
    for n,code in codes.items():
        d=F/n;need({p.name for p in d.iterdir()}=={'CAPTURE.json','PRELAUNCH.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'},'All six actual capture members');c=parse((d/'CAPTURE.json').read_bytes());need(type(c['pid']) is int and c['pid']>0 and c['completed'] is True and c['actual_execution'] is True and type(c['exit_code']) is int and c['exit_code']==code and c['source_unchanged'] is True and c['operator_unchanged'] is True,'Actual child exit and source flags');need(sha((d/'PRELAUNCH_SOURCE.py').read_bytes())==c['source_sha256'] and sha((d/'PRELAUNCH_OPERATOR.py').read_bytes())==c['operator_sha256'],'Complete private prelaunch')
        for channel in ['stdout','stderr']:
            ref(c[channel]);b=(d/c[channel]['path']).read_bytes();need(len(b)==c[channel]['bytes'] and sha(b)==c[channel]['sha256'],'Entire private stream')
        captures.append({'capture':n,'actual_pid':c['pid'],'exit_code':c['exit_code'],'complete_CAPTURE_object':c})
    own=[]
    for p in sorted(F.rglob('*')):
        need(not p.is_symlink() and (p.is_file() or p.is_dir()),'All own topology regular')
        if p.is_file():b=p.read_bytes();own.append({'path':p.relative_to(F).as_posix(),'bytes':len(b),'sha256':sha(b)})
    write('FINAL_READY_CHECK.json',{'schema':'pr47-acceptance-source-final-private-readback/v4','status':'READY_SOURCE_ONLY_WAIT_ROOT_CLOSURE_AND_NEW_ADVERSARY','actual_pid':os.getpid(),'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'complete_fixed_input_count':len(inputs['pins'])+len(inputs['external_input_rows']),'complete_fixed_input_bytes':total,'source_files':bindings,'complete_existing_private_captures':captures,'complete_own_pre_output_members':own,'assertions':COUNT,'earlier_private_control_assertions':17361,'all4096_actual_modes':True,'preserved_failed_control_pid':8441,'preserved_expected_negative_pid':17860,'actual_PR46_predecessor_completed':False,'production_imported_compiled_executed':False,'independent_acceptance_adversary_completed':False,'future_acceptance_approved':False,'paper_or_new_doi_or_tracker':False});print(json.dumps({'status':'READY_SOURCE_ONLY_WAIT_ROOT_CLOSURE_AND_NEW_ADVERSARY','actual_pid':os.getpid(),'complete_fixed_input_count':len(inputs['pins'])+len(inputs['external_input_rows']),'complete_fixed_input_bytes':total,'source_files':bindings,'assertions':COUNT,'production_imported_compiled_executed':False},sort_keys=True))
if __name__=='__main__':
    if (F/'PRIVATE_CONTROLS_RESULT.json').exists():final_readback()
    else:main()
