"""Independent pure source/gate/native/projection boundary controls, synthetic only."""
from pathlib import Path
import copy, hashlib, json, sys, types
HERE=Path(__file__).absolute().parent
MODS={}
for name in ('support206.py','ready206.py','lifecycle206.py','make_native206.py'):
    path=HERE/'sealed_source'/name;m=types.ModuleType(name[:-3]);m.__file__=str(path)
    exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);MODS[name]=m
S,R,L,N=(MODS[name] for name in ('support206.py','ready206.py','lifecycle206.py','make_native206.py'))
R.configure(S);N.configure(S);L.configure(S,R,N)
RESULT=[]
def run(label,fn,reject=False,predicate=None):
    try:
        value=fn();passed=not reject and (predicate is None or bool(predicate(value)))
        error=None;observed='accepted'
    except Exception as exc:
        passed=reject;error=type(exc).__name__+': '+str(exc);observed='rejected'
    RESULT.append({'case':label,'expected':'reject' if reject else 'accept','observed':observed,'pass':passed,'error':error})
class Patch:
    def __init__(self,**kw):self.kw=kw
    def __enter__(self):
        self.old={k:getattr(S,k) for k in self.kw}
        for k,v in self.kw.items():setattr(S,k,v)
    def __exit__(self,*a):
        for k,v in self.old.items():setattr(S,k,v)
PIN=S.pin(b'SYNTHETIC')
def event(i):
    return {'review_number':i,'whole_package_scope':True,'open_findings':0,'directory':f'SYNTHETIC_NEW_{i}',
            'Root_acceptance_file':f'ROOT_SYNTHETIC_NEW_{i}.json','verdict':'CLEANPASS',
            'reviewed_package':'publication_package_SYNTHETIC','reviewed_package_seal':PIN}
G={'schema':'pr206-root-publication-ready-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
   'PR':206,'problem_id':5100062,'original_head':S.HEAD,'claim':S.CLAIM,'source_facts':copy.deepcopy(S.SOURCE_FACTS),
   'metadata':{'title':'SYNTHETIC ONLY'},'whole_package_review_events':[event(1),event(2)],
   'package':'publication_package_SYNTHETIC','package_seal':PIN}
TRUE=('publication_ready_gate_accepted','whole_package_review_loop_complete','mathematical_clearance','source_contract_clearance',
      'bounded_priority_audit_complete','qualified_attributed_note_editorially_cleared','current_verifier_source_accepted')
FALSE=('historical_priority_established','theorem_novelty_cleared','formula_novelty_cleared','proof_method_novelty_cleared',
       'first_disclosure_certified','independent_discovery_certified','literal_simultaneity_established','current_openness_established',
       'actual_publication_verified','actual_tracker_row_verified','actual_original_PR_merged')
G.update({k:True for k in TRUE});G.update({k:False for k in FALSE})
run('final_gate_shape_baseline',lambda:S.validate_gate_shape(copy.deepcopy(G)))
for key in TRUE+FALSE:
    for value in (None,1 if key in TRUE else 0):
        g=copy.deepcopy(G);g[key]=value
        run('final_gate_flag_'+key+'_'+repr(value),lambda g=g:S.validate_gate_shape(g),True)
for label,mutate in (
    ('one_event',lambda g:g['whole_package_review_events'].pop()),
    ('same_directory',lambda g:g['whole_package_review_events'][1].update(directory='SYNTHETIC_NEW_1')),
    ('same_acceptance',lambda g:g['whole_package_review_events'][1].update(Root_acceptance_file='ROOT_SYNTHETIC_NEW_1.json')),
    ('out_of_order',lambda g:g['whole_package_review_events'][1].update(review_number=1)),
    ('false_scope',lambda g:g['whole_package_review_events'][0].update(whole_package_scope=False)),
    ('clean_findings',lambda g:g['whole_package_review_events'][-1].update(open_findings=1)),
    ('final_not_clean',lambda g:g['whole_package_review_events'][-1].update(verdict='OPEN')),
    ('wrong_final_seal',lambda g:g['whole_package_review_events'][-1].update(reviewed_package_seal=S.pin(b'WRONG'))),
    ('repairs_no_fresh_final',lambda g:g['whole_package_review_events'][0].update(verdict='OPEN',open_findings=1)),
    ('novel_source_fact',lambda g:g['source_facts'].update(novelty_established=True)),
    ('wrong_rgk_date',lambda g:g['source_facts'].update(RGK_row_date='row10of20')),
    ('odd_repetition_only',lambda g:g['source_facts'].update(repetition_multiplicity='odd r only')),
):
    g=copy.deepcopy(G);mutate(g);run('final_gate_'+label,lambda g=g:S.validate_gate_shape(g),True)
g=copy.deepcopy(G);g['whole_package_review_events'][0].update(verdict='OPEN',open_findings=1);g['fresh_final_review_after_documented_editorial_repairs']=True
run('repaired_with_fresh_final',lambda:S.validate_gate_shape(g))

# Authenticate the complete source-adoption dependency shape with a synthetic
# file boundary. No author outcomes or original project files are read.
files={S.D.name+'/'+n:('SYNTHETIC '+n).encode() for n in S.SOURCE_FILES}
manifest={'files':{n:S.pin(files[S.D.name+'/'+n]) for n in S.SOURCE_FILES}}
files[S.D.name+'/SAFE_AUTHORED_MANIFEST.json']=S.enc(manifest)
seal={'safe_manifest':S.pin(files[S.D.name+'/SAFE_AUTHORED_MANIFEST.json'])}
files[S.D.name+'/SOURCE_SEAL.json']=S.enc(seal)
ADOPT={'schema':'pr206-root-lifecycle-source-adoption-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','accepted_preparation_only':True,
       'PR':206,'original_head':S.HEAD,'external_dispatcher_owns_authenticated_direct8_adapter_and_all_alias_cache_cleanup':True,
       'sources':{S.D.name+'/'+n:manifest['files'][n] for n in S.SOURCES},
       'source_manifest':S.pin(files[S.D.name+'/SAFE_AUTHORED_MANIFEST.json']),
       'source_seal':S.pin(files[S.D.name+'/SOURCE_SEAL.json']),
       'expected_publication_gate':{'path':S.PUBLICATION_GATE,**PIN}}
ADOPT['program_view_writer_protocol']=S.writer_protocol()
files[S.SOURCE_ADOPTION]=S.enc(ADOPT)
def frozen(name,expected=None,readonly=True):
    raw=files[name]
    if expected is not None:S.need(S.pin(raw)==S.bytepin(expected),'Synthetic exact dependency pin')
    return raw
with Patch(frozen=frozen,artifact=lambda n,expected=None:S.decode(frozen(n,expected))):
    pin=S.pin(files[S.SOURCE_ADOPTION]);run('source_adoption_full_dependency_shape',lambda:S.authority(pin))
    run('source_adoption_wrong_external_pin',lambda:S.authority(S.pin(b'WRONG')),True)
    for label,mutate in (
        ('missing',lambda a:a.pop('program_view_writer_protocol')),
        ('family_lock',lambda a:a['program_view_writer_protocol'].update(lock_path='family/LOCK')),
        ('false_CAS_claim',lambda a:a['program_view_writer_protocol'].update(uncooperative_same_UID_content_CAS_guaranteed=True)),
        ('wrong_lock_payload',lambda a:a['program_view_writer_protocol'].update(lock_payload=S.pin(b'WRONG'))),
    ):
        a=copy.deepcopy(ADOPT);mutate(a);files[S.SOURCE_ADOPTION]=S.enc(a)
        run('source_adoption_writer_protocol_'+label,lambda:S.authority(S.pin(files[S.SOURCE_ADOPTION])),True)
    for label,mutate in (
        ('no_gate',lambda a:a.pop('expected_publication_gate')),
        ('wrong_gate_path',lambda a:a['expected_publication_gate'].update(path='OTHER.json')),
        ('missing_source',lambda a:a['sources'].pop(next(iter(a['sources'])))),
        ('wrong_source_pin',lambda a:a['sources'].__setitem__(next(iter(a['sources'])),S.pin(b'WRONG'))),
        ('no_dispatcher',lambda a:a.update(external_dispatcher_owns_authenticated_direct8_adapter_and_all_alias_cache_cleanup=False)),
        ('preparation_only_scope',lambda a:a.update(evidence_scope='AUTHOR_PREPARATION_ONLY')),
    ):
        a=copy.deepcopy(ADOPT);mutate(a);files[S.SOURCE_ADOPTION]=S.enc(a)
        run('source_adoption_'+label,lambda:S.authority(S.pin(files[S.SOURCE_ADOPTION])),True)
    files[S.SOURCE_ADOPTION]=S.enc(ADOPT)
    old=files[S.D.name+'/ready206.py'];files[S.D.name+'/ready206.py']=b'SUBSTITUTED'
    run('source_adoption_substituted_dependency',lambda:S.authority(S.pin(files[S.SOURCE_ADOPTION])),True)
    files[S.D.name+'/ready206.py']=old

# Complete native current31 rendering uses artificial original21/55033 and a
# deliberately substituted synthetic portable pin only for positive construction.
# The real unmodified21804/SHA pin is checked separately and rejects wrong bytes.
run('real_portable_pin_exact',lambda:S.PORTABLE,predicate=lambda p:p=={'bytes':21804,'sha256':'dfa1ff339e1f3a6004563aec9c01f6f14d6bb65a94e2437f3ba3a41e5b393d85'})
old={'README.md':b'old','FROZEN_MANIFEST.json':b'{}','CANDIDATE.md':b'old','verify_triangles.py':b'old','independent_review/independent_check.py':b'old'}
old.update({f'history_{i}.json':b'{}' for i in range(16)})
old['README.md']+=b'x'*(55033-sum(len(v) for v in old.values()))
f={'schema':'pr206-native-actual-facts-v1','original_head':S.HEAD,'UTC':'2026-10-16T20:00:00+00:00',
   'package_seal':{'path':'publication_package_SYNTHETIC/SEAL.json',**PIN},
   'publication_ready_gate':{'path':S.PUBLICATION_GATE,**PIN},
   'publication_receipt':{'path':'ROOT_PUBLICATION_RECEIPT.json',**PIN},'tracker_receipt':{'path':'ROOT_TRACKER_RECEIPT.json',**PIN}}
proof=b'SYNTHETIC manuscript source';portable=b'SYNTHETIC portable source'
ng=copy.deepcopy(G);ng.update(package_safe_files={'note.tex':S.pin(proof)},manuscript_source_file='note.tex',manuscript_pdf_file='note.pdf')
p={'doi':'10.5281/zenodo.123456','id':123456};t={'doi':p['doi'],'range':"'Math Puzzles'!A100:D100"}
run('native_wrong_real_portable_rejected',lambda:N.render('published_pending_merge',f,old,portable,proof,ng,p,t),True)
for stage in sorted(N.STAGES):
    fact=copy.deepcopy(f)
    if stage!='published_pending_merge':fact['merge_receipt']={'path':'SYNTHETIC/merge/ACCEPTANCE.json',**PIN}
    if stage=='actual_factual_accepted_completion_pending':fact['factual_receipt']={'path':'SYNTHETIC/factual/ACCEPTANCE.json',**PIN}
    run('native_shape_'+stage,lambda st=stage,ff=fact:N.validate_shape(st,ff))
    future=copy.deepcopy(fact);future['actual100_accepted']=True
    run('native_future_fact_'+stage,lambda st=stage,ff=future:N.validate_shape(st,ff),True)
    with Patch(PORTABLE=S.pin(portable)):
        before=copy.deepcopy(old)
        out=N.render(stage,fact,old,portable,proof,ng,p,t)
        status=S.decode(out[S.NATIVE+'CURRENT_STATUS.json'])
        run('native_current31_'+stage,lambda out=out:out,predicate=lambda v:len(v)==31 and set(v)=={S.NATIVE+n for n in set(old)|set(N.ADDED)})
        run('native_original_archive_unmodified_'+stage,lambda:old==before,predicate=bool)
        run('native_same_portable_paths_'+stage,lambda out=out:out,predicate=lambda v:v[S.NATIVE+'verify_triangles.py']==v[S.NATIVE+'independent_review/independent_check.py']==portable)
        run('native_proof_byte_copy_'+stage,lambda out=out:out[S.NATIVE+'CURRENT_PROOF_SOURCE.tex']==proof,predicate=bool)
        run('native_factual_still_incomplete_'+stage,lambda st=status:st,predicate=lambda st:st['completed'] is False and st['program_completion_accepted'] is False and st['source_facts']==S.SOURCE_FACTS)

# Independent candidate invariants and conditional global-five projection.
base_data={'gate_pin':PIN,'package':'publication_package_SYNTHETIC','package_seal':PIN,'whole_package_reviews_completed':2,
           'gate':G,'DOI':p['doi'],'record_id':p['id'],'tracker_range':t['range'],
           'publication_receipt_pin':PIN,'tracker_receipt_pin':PIN,'predecessor':{'directory':'SYNTHETIC/factual/'}}
for phase in S.PHASES:
    before=S.PHASES[phase][0]
    case={'PR':206,'original_head':S.HEAD,'case_percent':before,'completed':False,**S.BASE_COUNTS}
    progress={'current_PR':206,'current_PR_workflow_percent':before,**S.BASE_COUNTS,
              'fully_completed_eligible_PRs':list(range(1,49)),'published_PRs':list(range(1,33)),'dated_eligible_total':100,
              'current_stale_207':True,'next_stale_207':True}
    outcase,outprogress=S.project(phase,case,progress,'2026-10-16T20:00:00+00:00',base_data)
    expected=S.DONE_COUNTS if phase=='completion' else S.BASE_COUNTS
    run('project_counters_'+phase,lambda:(outcase,outprogress),predicate=lambda v,expected=expected:all(v[0][k]==x and v[1][k]==x for k,x in expected.items()))
    run('project_retire_stale_alias_'+phase,lambda:'current_stale_207' not in outprogress and 'next_stale_207' not in outprogress,predicate=bool)
    if phase=='completion':run('project_completion_condition_explicit',lambda:outcase,predicate=lambda c:c['completion_postimage_effective_only_after_own_actual_MAIN_acceptance_sync_pointer'] is True)
    badcase=copy.deepcopy(case);badcase['fully_completed_count']=49
    run('project_future_predecessor_'+phase,lambda bc=badcase,pr=progress,ph=phase:S.project(ph,bc,pr,'2026-10-16T20:00:00+00:00',base_data),True)
out={'schema':'pr206-independent-boundaries-v1','optimized':bool(sys.flags.optimize),
     'sources':{name:S.pin((HERE/'sealed_source'/name).read_bytes()) for name in MODS},
     'test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'only_synthetic_objects':True,'tests':len(RESULT),'passed':sum(x['pass'] for x in RESULT),
     'failed':sum(not x['pass'] for x in RESULT),'outcomes':RESULT}
print(json.dumps(out,indent=2))
raise SystemExit(bool(out['failed']))
