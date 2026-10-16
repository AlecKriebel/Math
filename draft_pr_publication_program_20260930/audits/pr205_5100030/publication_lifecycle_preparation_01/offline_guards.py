"""Meaningful source-preparation guards. Only new pure modules are executed.
No backend import, actual phase, API, cache installation or service call.
Synthetic future receipts stay in memory; only own synthetic package files exist.
"""
from pathlib import Path
import ast,copy,hashlib,json,sys,types
D=Path(__file__).resolve().parent;REAL_A=D.parent;checks=[]
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def check(name,fn):fn();checks.append(name)
def reject(name,fn):
    try:fn()
    except Exception:checks.append(name);return
    raise RuntimeError('Unexpected acceptance '+name)
def load(name):
    path=D/(name+'.py');tree=ast.parse(path.read_bytes());removed=[n for n in tree.body if isinstance(n,ast.If) and 'sys.flags.optimize' in ast.unparse(n.test)];need(name=='support205' and len(removed)==1 or name!='support205' and not removed,'Only production interpreter guard may be omitted for optimized pure tests');tree.body=[n for n in tree.body if n not in removed];m=types.ModuleType(name);m.__file__=str(path);exec(compile(tree,str(path),'exec'),m.__dict__);return m
S=load('support205');R=load('ready205');L=load('lifecycle205');N=load('make_native205');R.configure(S);N.configure(S);L.configure(S,R,N)
protected=[REAL_A/'original_submitted_head'/n for n in S.obj('ORIGINAL_SUBMISSION_CUSTODY.json',S.CUSTODY)['files']]+[REAL_A/'ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json',REAL_A/'CURRENT_CASE_STATUS.json']+[S.ROOT/p for p in S.VIEWS]
before={str(p):(S.pin(p.read_bytes()),p.stat().st_mtime_ns,p.stat().st_mode) for p in protected}
check('actual custody10 4124selected baseline exact',lambda:need(len(S.baseline_intake()['selected_files'])==4124,'Actual baseline'))
reject('no source adoption blocks readiness binding before output/backend',lambda:R.bind('must_not_exist',{'bytes':1,'sha256':'0'*64}))
reject('no source adoption blocks lifecycle binding before output/backend',lambda:L.bind('merge','must_not_exist',{}))
reject('no source adoption blocks native constructor',lambda:N.construct('published_pending_merge',{}))
check('missing authority created no generation/backend',lambda:need(not (D/'must_not_exist').exists() and S._backend is None,'No premature action'))
source_raw={D.name+'/'+n:(D/n).read_bytes() for n in S.SOURCES};source_pins={n:S.pin(raw) for n,raw in source_raw.items()};activation={'schema':'pr205-root-lifecycle-preparation-adoption-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','accepted_preparation_only':True,'PR':205,'original_head':S.HEAD,'sources':source_pins,'safe_artifacts':source_pins,'native_constructor':S.pp(D.name+'/make_native205.py',source_pins[D.name+'/make_native205.py']),'expected_publication_gate':S.pp('ROOT_PUBLICATION_GATE_01.json',S.pin(b'synthetic future gate'))};saved_read=S.read
def auth_case(value,source_drift=False):
    raw=S.enc(value);S._authority=('SYNTHETIC_ACTIVATION.json',S.pin(raw))
    def auth_read(path,wanted=None,readonly=True):
        body=raw if path=='SYNTHETIC_ACTIVATION.json' else source_raw[path]+(b' ' if source_drift else b'')
        if wanted is not None:need(S.pin(body)==wanted,'Synthetic source authority pin')
        return body
    S.read=auth_read;return S.authority()
check('explicit synthetic source activation binds exact4sources/native/futuregate only',lambda:auth_case(activation))
for label,mutate in [('not accepted',lambda x:x.update(accepted_preparation_only=False)),('wrong HEAD',lambda x:x.update(original_head='0'*40)),('missing source',lambda x:x['sources'].pop(D.name+'/ready205.py')),('wrong native source',lambda x:x['native_constructor'].update(path=D.name+'/ready205.py')),('bad gate pin',lambda x:x['expected_publication_gate'].update(bytes=True))]:
    damaged=copy.deepcopy(activation);mutate(damaged);reject('source authority rejects '+label,lambda x=damaged:auth_case(x))
reject('source authority rejects reopened source drift',lambda:auth_case(activation,True));S.read=saved_read;S._authority=None
q,base,head=S.queue_rows();doi='10.5281/zenodo.2050000';published=S.published_row(doi);other=b'| 1 | 9999999 / FOREIGN | title | a | b | c | d | queued | 0/5 |  |  |  |\n';oldq=b'header\n'+base+other;newq=S.replace_queue(oldq,doi)
check('first merge exact BASE121 to HEAD371-derived own row only',lambda:need(newq.splitlines(keepends=True)==[b'header\n',published,other] and published.decode().split('|')[8:10]==head.decode().split('|')[8:10] and b'1/5' in published,'Queue projection'))
for label,damaged in [('HEAD preimage',oldq.replace(base,head)),('arbitrary claimed_solved',oldq.replace(base,base.replace(b'queued',b'claimed_solved'))),('absent own',oldq.replace(base,b'')),('duplicate own',oldq+base),('changed BASE effort',oldq.replace(b'0/5',b'4/5',1))]:reject('queue refuses '+label,lambda x=damaged:S.replace_queue(x,doi))
body_original=S.body;bodies={'a'*40:oldq,'b'*40:oldq.replace(b'| title |',b'| concurrent foreign |')};S.body=lambda h,p,c:bodies[c];c=types.SimpleNamespace(byte_pin=S.bpin);prior={'commit':'a'*40,'selected_files':{S.Q:S.bpin(oldq),'unsolved_math_prioritization/attempts/5100012/README.md':{}}}
check('premerge foreign update preserves exact own BASE',lambda:S.reconcile(c,None,prior,'b'*40))
bodies['a'*40]=newq;bodies['b'*40]=newq;postbase={'commit':'a'*40,'selected_files':{S.Q:S.bpin(newq)}}
check('post95 exact accepted published row works through later phases',lambda:S.reconcile(c,None,postbase,'b'*40,doi))
reject('post95 cannot accidentally demand BASE again',lambda:S.reconcile(c,None,postbase,'b'*40))
reject('post95 wrong DOI refused',lambda:S.reconcile(c,None,postbase,'b'*40,'10.5281/zenodo.999'))
bodies['b'*40]=newq.replace(published,base);reject('post95 reverting own row to BASE refused',lambda:S.reconcile(c,None,postbase,'b'*40,doi));S.body=body_original
check('exact merge95 two parents/factual98 and100 single parent',lambda:need(L.parents('merge','a'*40)==['a'*40,S.HEAD] and L.parents('factual','a'*40)==L.parents('completion','a'*40)==['a'*40],'Parent lists'))
for phase in L.PHASE:check('counter preparation stays47/31 '+phase,lambda p=phase:need(L.counts(p)==S.BASE_COUNTS,'Counts'))
check('only actual100 yields48/32/205/206',lambda:need(L.counts('completion',True)==S.DONE_COUNTS and L.counts('merge',True)==L.counts('factual',True)==S.BASE_COUNTS,'Actual counts'))
# Build a synthetic final-package directory only for complete path-set checks.
fixture=D/'synthetic_fixture';package='publication_package_synthetic';pd=fixture/package;pd.mkdir(parents=True,exist_ok=True)
portable=S.read('portable_verification_01/verify.py',S.PORTABLE,False);pkg={'odd_period_focal_pedal.tex':b'synthetic TeX\n','odd_period_focal_pedal.pdf':b'%PDF synthetic\n','verification-package.zip':b'PK synthetic\n','verification/verify.py':portable,'PACKAGE_SEAL.json':b'{"synthetic":true}\n'};uploads={n:S.pin(pkg[n]) for n in ('odd_period_focal_pedal.tex','odd_period_focal_pedal.pdf','verification-package.zip')};metadata={'title':'Synthetic k601 fixture','creators':[{'name':'Kriebel, Alec','orcid':'0009-0001-9320-500X'}]};pkg['zenodo-deposit.json']=S.enc({'metadata':metadata,'files':[{'path':n} for n in uploads]})
for name,raw in pkg.items():
    path=pd/name;path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():need(path.read_bytes()==raw,'Fixture drift')
    else:path.write_bytes(raw);path.chmod(0o444)
virtual={package+'/'+n:raw for n,raw in pkg.items()};fixed={S.MATH:S.MATH_PIN,S.PRIORITY:S.PRIORITY_PIN,S.PORTABLE_RECEIPT:S.PORTABLE_RECEIPT_PIN,S.REPAIRS:S.REPAIRS_PIN}
for name,x in fixed.items():virtual[name]=S.read(name,x)
events=[]
for index in (1,2):
    directory='synthetic_review_'+str(index);report=b'synthetic complete review\n';virtual[directory+'/report.md']=report;event={'review_number':index,'directory':directory,'verdict':'CLEANPASS','whole_package_scope':True,'open_findings':0,'safe_files':{'report.md':S.pin(report)},'report_file':'report.md','report_pin':S.pin(report),'reviewed_package':package,'reviewed_package_seal':S.pin(pkg['PACKAGE_SEAL.json'])};accepted={'schema':'pr205-root-whole-package-review-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','accepted':True,'PR':205,'original_head':S.HEAD,'review_accepted':True,'NEW_whole_package_reviews_completed':index,'review_cycle_repairs_required_now':False,'review_event':copy.deepcopy(event)};af='SYNTHETIC_ROOT_REVIEW_'+str(index)+'.json';virtual[af]=S.enc(accepted);events.append({**event,'Root_acceptance_file':af,'Root_acceptance_pin':S.pin(virtual[af])})
gate={'schema':'pr205-root-publication-ready-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':205,'problem_id':5100030,'original_head':S.HEAD,'publication_ready_gate_accepted':True,'whole_package_review_loop_complete':True,'mathematical_clearance':True,'source_contract_clearance':True,'bounded_priority_audit_complete':True,'historical_priority_established':False,'package':package,'package_safe_files':{n:S.pin(raw) for n,raw in pkg.items()},'package_seal':S.pin(pkg['PACKAGE_SEAL.json']),'metadata':metadata,'intended_upload_files':uploads,'whole_package_review_events':events,'other_safe_files':fixed,'preparation_receipts':{role:S.pp(name,fixed[name]) for role,name in [('mathematics',S.MATH),('priority',S.PRIORITY),('portable',S.PORTABLE_RECEIPT),('repairs',S.REPAIRS)]}}
real_read=S.read;real_authority=S.authority;real_A=S.A;real_slot=S._authority
def fake_read(path,wanted=None,readonly=True):
    raw=virtual[path]
    if wanted is not None:need(S.pin(raw)==wanted,'Synthetic byte pin '+path)
    return raw
def invoke_gate(candidate):
    virtual['ROOT_PUBLICATION_GATE_01.json']=S.enc(candidate);wanted=S.pin(virtual['ROOT_PUBLICATION_GATE_01.json']);S.authority=lambda:{'expected_publication_gate':S.pp('ROOT_PUBLICATION_GATE_01.json',wanted),'safe_artifacts':{}};S._authority=('SYNTHETIC_SOURCE_ADOPTION.json',S.pin(b'synthetic authority'));return S.gate(wanted)
S.read=fake_read;S.A=fixture
check('canonical synthetic final gate complete package/twoRootreviews passes',lambda:invoke_gate(gate))
for label,mutate in [('one review',lambda x:x.update(whole_package_review_events=x['whole_package_review_events'][:1])),('duplicate review directory',lambda x:x['whole_package_review_events'][1].update(directory=x['whole_package_review_events'][0]['directory'])),('last wrong seal',lambda x:x['whole_package_review_events'][-1].update(reviewed_package_seal=S.pin(b'wrong'))),('bool review index',lambda x:x['whole_package_review_events'][0].update(review_number=True)),('clean with open finding',lambda x:x['whole_package_review_events'][0].update(open_findings=1)),('novelty true',lambda x:x.update(theorem_novelty_cleared=True)),('already published atready',lambda x:x.update(actual_publication_verified=True)),('missing current portable',lambda x:x['package_safe_files'].pop('verification/verify.py')),('wrong mandatory math gate',lambda x:x['other_safe_files'].update({S.MATH:S.pin(b'wrong')})),('wrong metadata',lambda x:x.update(metadata={'title':'wrong'}))]:
    damaged=copy.deepcopy(gate);mutate(damaged);reject('gate rejects '+label,lambda x=damaged:invoke_gate(x))
extra=pd/'unlisted.txt';extra.write_bytes(b'unlisted');reject('gate rejects extra full-package file',lambda:invoke_gate(gate));extra.unlink()
damaged=copy.deepcopy(gate);damaged['whole_package_review_events'][0]['unaccepted_new_fact']=True;reject('gate refuses event superset beyond two envelope pins',lambda:invoke_gate(damaged))
S.read=real_read;S.authority=real_authority;S.A=real_A;S._authority=real_slot
# Pure native projection uses real archived17 and portable bytes, synthetic
# publication facts explicitly confined to this process; no future receipt saved.
custody,old=S.originals();math_gate=S.obj(S.MATH,S.MATH_PIN);priority_gate=S.obj(S.PRIORITY,S.PRIORITY_PIN);pub={'doi':doi,'doi_url':'https://doi.org/'+doi,'id':2050000};tracker={'range':"'Math Puzzles'!A999:D999"};facts={'schema':'pr205-native-facts-v1','original_head':S.HEAD,'UTC':'2026-10-16T00:00:00+00:00','fixture_scope':'SYNTHETIC_RENDER_ONLY'};renders={}
for stage in N.STAGES:
    out=N._render(stage,facts,old,portable,gate,pub,tracker,math_gate,priority_gate);renders[stage]=out
    check(stage+' native25 path set/archive scientific preservation',lambda o=out:need(set(o)=={S.NATIVE+n for n in set(old)|N.ADDED} and len(o)==25 and all(o[S.NATIVE+n]==raw for n,raw in old.items() if n not in N.WRAPPERS),'Native paths/preservation'))
    check(stage+' both current checkers exact finite-exception source',lambda o=out:need(o[S.NATIVE+'check_candidate.py']==o[S.NATIVE+'independent_review/independent_check.py']==portable and not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(portable))),'Current executable repair'))
    manifest=S.decode(out[S.NATIVE+'FROZEN_MANIFEST.json']);check(stage+' regenerated current FROZEN hash map',lambda m=manifest,o=out:need(all(S.bpin(o[S.NATIVE+n])==x for n,x in m['files'].items()) and m['original_manifest']['sha256']==S.pin(old['FROZEN_MANIFEST.json'])['sha256'],'Current manifest'))
    current=S.decode(out[S.NATIVE+'CURRENT_STATUS.json']);check(stage+' native CURRENT omits program completion/counters/cursor',lambda x=current:need(not any(k in x for k in ('completed','case_completed','fully_completed_count','published_count','last_completed_PR','next_numeric_intake_cursor')) and x['goal_complete'] is False and x['original_effort_cell']=='1/5' and x['theorem_novelty_cleared'] is False,'Native program authority separation'))
    provenance=S.decode(out[S.NATIVE+'CURRENT_PROVENANCE.json']);check(stage+' historical favorable reports/sourcefreeze explicitly marked',lambda x=provenance:need(set(x['preserved_native_historical_files'])==set(old)-N.WRAPPERS and x['historical_PASS_counts_not_current_validation'] is True and x['all_preserved_files_explicitly_historical'] is True and x['current_native_checkers']['check_candidate.py']==S.PORTABLE,'Historical status'))
# Project each conditional phase without running a backend or native phase.
case=S.obj('CURRENT_CASE_STATUS.json');progress=S.decode((S.ROOT/(S.PREFIX+'CURRENT_PROGRESS.json')).read_bytes());b={'gate_pin':S.pin(b'synthetic gate'),'package':package,'package_seal':gate['package_seal'],'whole_package_reviews_completed':2};ready_case,ready_progress=R.project(case,progress,'stamp',b,gate)
check('ready90 promotes all canonical science/editorial aliases without publication',lambda:need(ready_case['case_percent']==90 and ready_case['priority_audit_complete'] is True and ready_progress['current_priority_clearance'] is True and ready_progress['current_editorial_manuscript_preparation_authorized'] is True and ready_progress['current_verification_code_publication_clearance'] is True and ready_progress['current_Zenodo_published'] is False and ready_progress['current_DOI'] is None and ready_progress['next_numeric_intake_cursor']==205,'Ready flags'))
life_b={'DOI':doi,'record_id':2050000,'tracker_range':tracker['range'],'publication_receipt_pin':S.pin(b'synthetic pub'),'tracker_receipt_pin':S.pin(b'synthetic tracker'),'actual_predecessor':{'directory':S.D.name+'/synthetic_prior'}}
cc,cp=ready_case,ready_progress
for phase in ('merge','factual','completion'):
    cc,cp=L.project(cc,cp,'stamp',phase,life_b,'synthetic_generation');want=S.DONE_COUNTS if phase=='completion' else S.BASE_COUNTS
    check('conditional '+phase+' has exact required counters and1/5',lambda c=cc,p=cp,w=want:need(all(c[k]==v and p[k]==v for k,v in w.items()) and '1/5' in c['original_effort'] and c['completion_postimage_effective_only_after_own_actual_MAIN_full_scope_acceptance'] is True,'Phase postimage'))
check('completion correctly retires old204 metadata and appends205 once',lambda:need(cp['historical_prior_completion_metadata'][-1]['values']['last_completed_PR']==204 and cp['fully_completed_eligible_PRs'].count(205)==1 and cp['published_PRs'].count(205)==1 and cp['current_original_PR_actual_merged'] is True,'Completion provenance'))
actual_original=S.actual;S.actual=lambda kind:('synthetic_merge',{},None,None);read_original=S.read;S.read=lambda *args,**kwargs:b'synthetic merge accepted';bb={'package':package,'package_seal_file':'PACKAGE_SEAL.json','package_seal':gate['package_seal'],'publication_receipt_pin':life_b['publication_receipt_pin'],'tracker_receipt_pin':life_b['tracker_receipt_pin']};alias=L.aliases('factual',bb,'b'*40,'stamp')
check('actual98 canonical aliases remain completedfalse47/31/204/205',lambda:need(alias['actual_factual_accepted'] is True and alias['completed'] is False and alias['completion_facts']=={'case_completed':False,**S.BASE_COUNTS} and alias['schema']=='pr205-root-factual-receipt-v1','Incomplete98 aliases'));S.actual=actual_original;S.read=read_original
# Authentic operation field schemas with synthetic, memory-only receipt bodies.
context={'gate_pin':S.pin(b'synthetic final gate'),'ready_pointer_pin':S.pin(b'synthetic pointer'),'ready_acceptance_pin':S.pin(b'synthetic ready'),'checkpoint_commit':'c'*40,'package_seal':gate['package_seal'],'package':package,'manifest_pin':S.pin(pkg['zenodo-deposit.json'])};publication={'PR':205,'state':'published','gate_sha256':context['gate_pin']['sha256'],'package':package,'context':context,'actual_publication_verified':True,'metadata_exact_verified':True,'all_three_public_download_SHA256_verified':True,'metadata_normalizations':[],'verified_public_download_names':list(uploads),'id':2050000,'doi':doi,'doi_url':'https://doi.org/'+doi,'record_url':'https://zenodo.org/records/2050000','doi_resolution':{'http_status':200,'status':'resolved'},'files':[{'name':n,'size':v['bytes'],'sha256':v['sha256']} for n,v in uploads.items()],'public_downloads':[{'name':n,**v,'url':'https://example.invalid/'+n,'final_url':'https://example.invalid/'+n} for n,v in uploads.items()]};opvirtual={'ROOT_PUBLICATION_RECEIPT.json':S.enc(publication)};tracking={'PR':205,'doi':doi,'gate_sha256':context['gate_pin']['sha256'],'publication_receipt':S.pin(opvirtual['ROOT_PUBLICATION_RECEIPT.json']),'context':context,'row':S.tracker_row(gate,doi),'spreadsheet_id':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','sheet_gid':1254632077,'range':"'Math Puzzles'!A999:D999",'original_preappend_baseline':{'file':'synthetic_baseline.json','pin':S.pin(b'baseline'),'row_count':128,'counter_sha256':'0'*64}}
for flag in ('actual_tracker_row_verified','own_row_readback_verified','foreign_rows_retained','original_preappend_baseline_retained','two_fresh_full_prechecks','RAW_INSERT_ROWS','B_intentionally_blank_no_verified_chat_share_URL'):tracking[flag]=True
opvirtual['ROOT_TRACKER_RECEIPT.json']=S.enc(tracking);saved_context=S.actual_context;saved_ops=S.operations;saved_auth=S.authority;S.actual_context=lambda:(gate,context);S.read=lambda path,*args,**kwargs:opvirtual[path]
check('unchanged authentic publication/tracker receipt schemas accepted',lambda:S.operations())
for label,path,key,bad in [('publication false','ROOT_PUBLICATION_RECEIPT.json','actual_publication_verified',False),('metadata normalization','ROOT_PUBLICATION_RECEIPT.json','metadata_normalizations',['changed']),('wrong full tracker DOI URL','ROOT_TRACKER_RECEIPT.json','row',[tracking['row'][0],'',doi,tracking['row'][3]]),('foreign tracker retention false','ROOT_TRACKER_RECEIPT.json','foreign_rows_retained',False),('different gate context','ROOT_PUBLICATION_RECEIPT.json','context',{})]:
    prior=opvirtual[path];damaged=S.decode(prior);damaged[key]=bad;opvirtual[path]=S.enc(damaged);reject('operation receipt rejects '+label,lambda:S.operations());opvirtual[path]=prior
S.authority=lambda:activation;S.operations=lambda:(gate,publication,tracking,context);pubpin=S.pin(opvirtual['ROOT_PUBLICATION_RECEIPT.json']);tpin=S.pin(opvirtual['ROOT_TRACKER_RECEIPT.json']);basic={'schema':'pr205-native-facts-v1','original_head':S.HEAD,'UTC':'2026-10-16T00:00:00+00:00','package_seal':S.pp(package+'/PACKAGE_SEAL.json',gate['package_seal']),'publication_ready_gate':S.pp('ROOT_PUBLICATION_GATE_01.json',context['gate_pin']),'publication_receipt':S.pp('ROOT_PUBLICATION_RECEIPT.json',pubpin),'tracker_receipt':S.pp('ROOT_TRACKER_RECEIPT.json',tpin)};ma={'schema':'pr205-root-merge-receipt-v1','original_head':S.HEAD,'case_percent':95,'completed':False,'merged':True,'original_HEAD_safe':True,'full_scope_verified':True,'checkpoint_commit':'d'*40,'merge_commit':'d'*40,'publication_receipt_sha256':pubpin['sha256'],'tracker_receipt_sha256':tpin['sha256'],'package_seal':basic['package_seal'],**S.BASE_COUNTS};opvirtual['synthetic_merge/ACCEPTANCE.json']=S.enc(ma);fa={'schema':'pr205-root-factual-receipt-v1','case_percent':98,'completed':False,'actual_factual_accepted':True,'full_scope_MAIN_accepted':True,'completion_facts':{'case_completed':False,**S.BASE_COUNTS},'publication_receipt_sha256':pubpin['sha256'],'tracker_receipt_sha256':tpin['sha256'],'merge_receipt_sha256':S.pin(opvirtual['synthetic_merge/ACCEPTANCE.json'])['sha256'],'package_seal':basic['package_seal'],**S.BASE_COUNTS};opvirtual['synthetic_factual/ACCEPTANCE.json']=S.enc(fa)
def fake_actual(kind):return ('synthetic_'+kind,S.decode(opvirtual['synthetic_'+kind+'/ACCEPTANCE.json']),None,None)
S.actual=fake_actual
for stage in N.STAGES:
    f=copy.deepcopy(basic)
    if stage!='published_pending_merge':f['merge_receipt']=S.pp('synthetic_merge/ACCEPTANCE.json',S.pin(opvirtual['synthetic_merge/ACCEPTANCE.json']))
    if stage=='factual_checkpoint_accepted':f['factual_receipt']=S.pp('synthetic_factual/ACCEPTANCE.json',S.pin(opvirtual['synthetic_factual/ACCEPTANCE.json']))
    check(stage+' exact stage native facts accepted',lambda x=f,s=stage:N.validate_facts(s,x));damaged=copy.deepcopy(f);damaged['invented_spent_turns']='5/5';reject(stage+' unknown/spentturn fact refused',lambda x=damaged,s=stage:N.validate_facts(s,x))
prior=opvirtual['synthetic_factual/ACCEPTANCE.json'];damaged=S.decode(prior);damaged['completed']=True;opvirtual['synthetic_factual/ACCEPTANCE.json']=S.enc(damaged);f=copy.deepcopy(basic);f['merge_receipt']=S.pp('synthetic_merge/ACCEPTANCE.json',S.pin(opvirtual['synthetic_merge/ACCEPTANCE.json']));f['factual_receipt']=S.pp('synthetic_factual/ACCEPTANCE.json',S.pin(opvirtual['synthetic_factual/ACCEPTANCE.json']));reject('native100 refuses circular actual98 completedtrue prerequisite',lambda:N.validate_facts('factual_checkpoint_accepted',f));opvirtual['synthetic_factual/ACCEPTANCE.json']=prior
S.actual=actual_original;S.operations=saved_ops;S.actual_context=saved_context;S.authority=saved_auth;S.read=read_original
check('all original archive/current5 bytes modes mtimes untouched',lambda:need(before=={str(p):(S.pin(p.read_bytes()),p.stat().st_mtime_ns,p.stat().st_mode) for p in protected},'Protected originals/current views'))
print(json.dumps({'mode':'optimized' if sys.flags.optimize else 'ordinary','controls_passed':len(checks),'controls':checks,'native_stage_postimage_digests':{stage:hashlib.sha256(S.enc({k:S.bpin(raw) for k,raw in sorted(out.items())})).hexdigest() for stage,out in renders.items()},'synthetic_future_receipts_in_memory_only':True,'only_own_new_pure_modules_executed':True,'no_backend_import_or_actual_phase_API_cache_service_Git_ref_current_view_actions':True,'scientific_or_whole_package_review_events_added':0},indent=2))
