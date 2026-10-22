"""Proposed PR204 ready90: actual priority60 directly to future final Root gate.
No bind/prepare until exact future gate with >=2 Root-accepted whole reviews.
Unaccepted package75 is historical preparation only, never baseline authority.
"""
from pathlib import Path
import datetime,hashlib,importlib.util,json,os,re,sys
if sys.flags.optimize or not sys.dont_write_bytecode:raise RuntimeError('Ordinary Python -B required')
D=Path(__file__).resolve().parent;A=D.parent;P=A.parent.parent;ROOT=P.parent
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
PACKAGE_HELPER_PIN={'bytes':22340,'sha256':'14194bd950bdff00e0793072b742d7dce9f613655fc96e0a92ccd2f23bc1ec44'}
f=A/'package_checkpoint_01/checkpoint_package204.py';require(pin(f.read_bytes())==PACKAGE_HELPER_PIN,'Sealed package helper drift')
s=importlib.util.spec_from_file_location('ready204_existing_native_primitives',f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);v=m.v
CASE=v.CASE;PREFIX=v.PREFIX;HEAD=v.HEAD;Q=v.Q;VIEWS=v.VIEWS;OWN=CASE+'publication_checkpoint_02/'
GATE='ROOT_PUBLICATION_GATE_01.json';FIRST_REVIEW='ROOT_WHOLE_PACKAGE_REVIEW_ACCEPTANCE_01.json'
FIRST_REVIEW_PIN={'bytes':4290,'sha256':'3014eae5a1bf70938c43556fad732235b7c08359971b775bb8f0ee36f6fdbbc7'}
OWN_FILES=['checkpoint_ready204.py','run_ready_with_tree_cache.py','CHECKPOINT_CONTRACT.md','RESEARCH_LOG.md','SAFE_AUTHORED_MANIFEST.json']
STATUS='FINAL_ATTRIBUTED_PACKAGE_ROOT_READY_AFTER_NEW_WHOLE_PACKAGE_REVIEWS'
REMAIN='Publish only the exact final reviewed upload files with the repository Zenodo kit; verify public metadata/download SHA256/DOI, append and read back the tracker, then originalHEAD-safe MAIN merge and factual/completion checkpoints. Readiness supplies no actual deposit, tracker or PR-merge fact; no next-PR advance.'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def enc(j):return (json.dumps(j,indent=2)+'\n').encode()
def read(f):return json.loads(f.read_bytes())
def fsync_directory(directory):
    fd=os.open(directory,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:os.fsync(fd)
    finally:os.close(fd)
def save(f,b):
    require(f.resolve().is_relative_to(D),'Output outside own readiness directory')
    with f.open('xb') as out:out.write(b);out.flush();os.fchmod(out.fileno(),0o444);os.fsync(out.fileno())
    fsync_directory(f.parent)
def frozen(rel,x=None):
    if x is None:return m.frozen(rel) # Own helper artifacts retain readonly guards.
    relative(rel);f=A/rel;require(f.is_file() and not f.is_symlink(),'Pinned external artifact missing/nonregular '+rel);b=f.read_bytes();require(pin(b)==x,'Pinned external artifact drift '+rel);return b
def relative(s):return m.p.m.safe_relative(s)
def byte_pin_record(x):
    require(isinstance(x,dict) and set(x)=={'bytes','sha256'} and type(x['bytes']) is int and x['bytes']>=0 and re.fullmatch('[0-9a-f]{64}',x['sha256']) is not None,'Exact byte/SHA256 pin schema');return x
def generation(name):require(re.fullmatch('[a-z][a-z0-9_]{0,48}',name) is not None,'Unsafe generation');return D/name
def static_manifest():
    f=D/'SAFE_AUTHORED_MANIFEST.json';require(f.is_file(),'Readiness authored manifest missing');j=read(f);require(set(j['files'])==set(OWN_FILES)-{f.name},'Exact readiness helper allowlist')
    for name,x in j['files'].items():frozen('publication_checkpoint_02/'+name,x)
    return pin(f.read_bytes())
def accepted_events(g,out):
    events=g['whole_package_review_events'];require(isinstance(events,list) and len(events)>=2,'At least two actual Root-accepted review events required')
    directories=set();acceptances=set();repairs_in_history=False;last_acceptance=None
    for index,event in enumerate(events,1):
        require(event['review_number']==index and isinstance(event['verdict'],str) and event['verdict'],'Sequential actual review events required')
        directory=relative(event['directory']);require(directory not in directories,'Review directory reused');directories.add(directory)
        safe=event['safe_files'];require(isinstance(safe,dict) and safe,'Explicit review safe files required')
        for name,x in safe.items():rel=directory+'/'+relative(name);x=byte_pin_record(x);out[rel]=pin(frozen(rel,x))
        report=relative(event['report_file']);require(report in safe,'Review report not explicitly bound')
        if 'report_pin' in event:require(event['report_pin']==safe[report],'Review report pin mismatch')
        af=relative(event['Root_acceptance_file']);ap=byte_pin_record(event['Root_acceptance_pin']);require(af not in acceptances,'Root acceptance reused');acceptances.add(af)
        ab=frozen(af,ap);out[af]=pin(ab);a=json.loads(ab)
        require(a['PR']==204 and a['original_head']==HEAD and a['review_accepted'] is True and a['NEW_whole_package_reviews_completed']==index,'Root whole-review acceptance/count missing')
        repairs_in_history=repairs_in_history or event['verdict']!='CLEANPASS' or a['review_cycle_repairs_required_now'] is not False;last_acceptance=a
        ae=a['review_event'];require(isinstance(ae,dict) and all(event.get(k)==x for k,x in ae.items()),'Final gate event differs from its exact Root-accepted event')
        require(ae['safe_files']==safe and ae['reviewed_package']==event['reviewed_package'] and ae['reviewed_package_seal']==event['reviewed_package_seal'],'Root review package/safe-file binding')
        if index==1:require(af==FIRST_REVIEW and ap==FIRST_REVIEW_PIN,'Preserve exact accepted first review')
    final=events[-1];require(final['verdict']=='CLEANPASS' and last_acceptance['review_cycle_repairs_required_now'] is False and final['reviewed_package']==g['package'] and final['reviewed_package_seal']==g['package_seal'],'Last clean review must bind exact final package/seal with no unresolved repair')
    if repairs_in_history:require(g.get('fresh_final_review_after_documented_editorial_repairs') is True,'Repair history requires documented repairs and a fresh final full review')
    return events
def gate_inputs(gate_pin):
    byte_pin_record(gate_pin);require(gate_pin['bytes']>0,'Nonempty exact final gate required')
    require((A/GATE).is_file(),'Future final Root publication gate absent; no binding or prepare allowed')
    gb=frozen(GATE,gate_pin);g=json.loads(gb)
    require((g['PR'],g['problem_id'],g['original_head'])==(204,5100012,HEAD),'Final publication gate identity')
    for key in ['publication_ready_gate_accepted','whole_package_review_loop_complete','mathematical_clearance','source_contract_clearance','bounded_priority_audit_complete']:require(g[key] is True,'Final Root clearance absent '+key)
    require(g['historical_priority_established'] is False,'Historical priority cannot be promoted')
    for key in ['theorem_novelty_cleared','formula_novelty_cleared','proof_method_novelty_cleared','first_disclosure_certified','independent_discovery_certified','literal_simultaneity_established','actual_publication_verified','actual_tracker_row_verified','actual_original_PR_merged']:require(g.get(key,False) is False,'Forbidden novelty/actual-publication fact '+key)
    package=g['package'];require(re.fullmatch('publication_package_[a-zA-Z0-9_]+',package) is not None,'Explicit final package directory')
    out={GATE:gate_pin};safe=g['package_safe_files'];require(isinstance(safe,dict) and safe,'Explicit complete package allowlist')
    for name,x in safe.items():rel=package+'/'+relative(name);out[rel]=pin(frozen(rel,byte_pin_record(x)))
    pd=A/package;require(pd.is_dir() and not pd.is_symlink(),'Final package directory unsafe');actual=set()
    for f in pd.rglob('*'):
        require(not f.is_symlink(),'Symlink in final package')
        if f.is_file():actual.add(f.relative_to(pd).as_posix())
    require(actual==set(safe),'Complete final package path set differs from gate')
    seal=byte_pin_record(g['package_seal']);seal_file=relative(g.get('package_seal_file','PACKAGE_SEAL.json'));require(safe.get(seal_file)==seal,'Exact final package seal file')
    metadata_name=relative(g.get('metadata_file','zenodo-deposit.json'));require(metadata_name in safe,'Exact final metadata file required');md=json.loads(frozen(package+'/'+metadata_name,safe[metadata_name]));require(md.get('metadata',md)==g['metadata'],'Gate metadata differs from exact final package metadata')
    uploads=g['intended_upload_files'];require(isinstance(uploads,dict) and uploads,'Explicit final intended upload files')
    for name,x in uploads.items():require(relative(name)==Path(name).name and safe.get(name)==byte_pin_record(x),'Intended upload absent or differently pinned')
    require({'.pdf','.tex','.zip'}<={Path(name).suffix.lower() for name in uploads},'Final PDF/source/verification ZIP upload bindings required')
    events=accepted_events(g,out)
    other=g['other_safe_files'];require(isinstance(other,dict),'Explicit other-safe-files map')
    for rel,x in other.items():relative(rel);require(rel!=GATE,'Recursive gate self-binding');out[rel]=pin(frozen(rel,byte_pin_record(x)))
    for required in ['ROOT_MATHEMATICAL_ACCEPTANCE_01.json','ROOT_VERIFICATION_REPAIR_ACCEPTANCE_01.json','ROOT_PRIORITY_AND_EDITORIAL_GATE_01.json','ROOT_SOURCE_FIRST_CONTRACT_01.md','ROOT_PACKAGE_PREPARATION_ACCEPTANCE_01.json','ROOT_PORTABLE_VERIFICATION_ACCEPTANCE_01.json']:
        require(required in other,'Final gate must explicitly retain preparation/scientific record '+required)
    require(any('PDF' in rel and 'VISUAL' in rel for rel in other),'Final Root PDF visual preparation record missing')
    for rel in out:
        require('ACCEPTANCE_CURRENT_SELECTED_MAP.json' not in rel and not any(part in Path(rel).parts for part in ['private_tree_cache','__pycache__','primary_source_private','.venv','site-packages']) and not rel.endswith(('.pyc','.pyo')),'Private cache/map/runtime artifact forbidden')
    prior='priority_checkpoint_01/priority60_02/ACCEPTANCE.json';out[prior]=pin(frozen(prior,m.BASE_ACCEPT))
    require(not (A/'package_checkpoint_01/package75_01/ACCEPTANCE.json').exists(),'Unexpected actual75 record: stop for baseline review')
    return {'PR':204,'phase':'ready90','case_percent':90,'Root_publication_gate_pin':gate_pin,'package':package,'package_seal':seal,'metadata':g['metadata'],'intended_upload_files':uploads,'whole_package_review_events':events,'whole_package_reviews_completed':len(events),'files':out,'static_authored_manifest_pin':static_manifest(),'baseline_actual_commit':m.BASE_COMMIT,'baseline_actual_tree':m.BASE_TREE,'baseline_actual_acceptance_pin':m.BASE_ACCEPT,'baseline_actual_map_file_pin':m.BASE_MAP,'baseline_selected_files':3630,'baseline_selected_map_sha256':m.BASE_DIGEST,'package75_historical_unaccepted_not_baseline':True,'publication_ready':True,'actual_publication_tracker_or_merge':False}
def bind(name,size,digest):
    dest=generation(name);require(not dest.exists(),'Fresh readiness generation required');j=gate_inputs({'bytes':size,'sha256':digest});j['UTC']=now();dest.mkdir();save(dest/'READY_INPUT_BINDINGS.json',enc(j));print(json.dumps({'bound':True,'generation':name,'files':len(j['files']),'whole_reviews':j['whole_package_reviews_completed'],'input_bytes':sum(x['bytes'] for x in j['files'].values()),'Root_gate_pin':j['Root_publication_gate_pin'],'no_remote_mutation':True}))
def binding(name):
    f=generation(name)/'READY_INPUT_BINDINGS.json';require(f.is_file(),'Future final Root publication binding missing; no phase allowed');j=read(f);fresh=gate_inputs(j['Root_publication_gate_pin']);require({k:x for k,x in j.items() if k!='UTC'}==fresh,'Final publication binding drift');return j
def overlay(c,h,parent,stamp,b,name):
    out={CASE+rel:frozen(rel,x) for rel,x in b['files'].items()}
    for n in OWN_FILES:out[OWN+n]=frozen('publication_checkpoint_02/'+n)
    out[OWN+name+'/READY_INPUT_BINDINGS.json']=(generation(name)/'READY_INPUT_BINDINGS.json').read_bytes()
    case=json.loads(v.native_body(h,CASE+'CURRENT_CASE_STATUS.json',parent));progress=json.loads(v.native_body(h,PREFIX+'CURRENT_PROGRESS.json',parent));m.prior_views(case,progress)
    case.setdefault('historical_phase_snapshots',[]).append({'UTC':stamp,'phase':'actualpriority60_direct_to_ready90','actual_checkpoint':m.BASE_COMMIT,'values':{k:x for k,x in case.items() if k!='historical_phase_snapshots'}})
    progress.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':204,'prior_phase':'actualpriority60_direct_to_ready90','actual_checkpoint':m.BASE_COMMIT,'values':{k:x for k,x in progress.items() if k.startswith('current_')}})
    # Prior priority60 preparation-only release field is history, not a ready90 claim.
    case.pop('release_authorized_by_this_gate',None);progress.pop('current_release_authorized_by_this_gate',None)
    ref={'path':'audits/pr204_5100012/'+GATE,**b['Root_publication_gate_pin']};count=b['whole_package_reviews_completed']
    case.update(UTC=stamp,status=STATUS,case_percent=90,priority_clearance=True,priority_clearance_scope='bounded_priority_audit_and_qualified_attributed_note_only',priority_novelty_clearance=False,qualified_attributed_note_editorially_cleared=True,paper_prepared=True,publication_package=b['package'],publication_package_seal=b['package_seal'],package_prepared=True,publication_gate=ref,publication_ready=True,whole_publication_package_reviews_complete=True,NEW_whole_package_reviews_completed=count,NEW_whole_package_review_active=False,whole_package_review_loop_complete=True,whole_package_review_events=b['whole_package_review_events'],active_whole_package_adversary=None,package75_historical_unaccepted_not_baseline=True,actual_baseline_before_ready='priority60_02',actual_publication_verified=False,actual_tracker_row_verified=False,actual_Zenodo_published=False,deposit_prepared=False,actual_tracker_updated=False,actual_original_PR_merged=False,actual_factual_MAIN_accepted=False,completed=False,remaining_required_steps=REMAIN)
    out[CASE+'CURRENT_CASE_STATUS.json']=enc(case)
    progress.update(UTC=stamp,updated_UTC=stamp,current_status=STATUS,current_PR_workflow_percent=90,current_priority_clearance=True,current_priority_clearance_scope='bounded_priority_audit_and_qualified_attributed_note_only',current_priority_novelty_clearance=False,current_qualified_attributed_note_editorially_cleared=True,current_workflow_estimate_percent=90,current_paper_prepared=True,current_publication_package=b['package'],current_publication_package_seal=b['package_seal'],current_package_prepared=True,current_publication_gate=ref,current_publication_ready=True,current_publication_package_reviews_complete=True,current_NEW_whole_publication_package_reviews_completed=count,current_NEW_whole_publication_package_review_active=False,current_whole_package_review_loop_complete=True,current_whole_package_review_events=b['whole_package_review_events'],current_active_whole_package_adversary=None,current_package75_historical_unaccepted_not_baseline=True,current_actual_baseline_before_ready='priority60_02',current_Zenodo_published=False,current_DOI=None,current_deposit_prepared=False,current_tracker_updated=False,current_tracker_range=None,current_actual_publication_verified=False,current_actual_tracker_row_verified=False,current_actual_merge_accepted=False,current_actual_factual_checkpoint_accepted=False,current_completed=False,current_remaining_required_steps=REMAIN,remaining_current_step=REMAIN,next_step=REMAIN,next_numeric_intake_cursor=204,conditional_next_numeric_intake_cursor=205,advance_to_next_PR_authorized_now=False,program_snapshot_semantics='PR204 final attributed package ready90 only after exact Root publication gate and '+str(count)+' actual accepted NEW whole-package reviews, last clean review on exact final seal. Exact Ferudun overlap/no novelty/firstness/independent-discovery/simultaneity and qualified least-period source retained. Actual baseline priority60; prepared75 unaccepted history. No actual deposit/tracker/PRmerge/advance.46completed/30published,last203,cursor204/advancefalse.',program_snapshot_authority_condition='Ready90 postimage effective only after actual trueparent/fullforeignscope/everyselectedidentity acceptance. Root final scientific/editorial gate supplies readiness; no invented actual publication or completion facts.')
    out[PREFIX+'CURRENT_PROGRESS.json']=enc(progress)
    note='\n'+stamp+' — PR204 ready90% direct from actualpriority60: exact final Root gate and '+str(count)+' accepted NEW whole-package review events, last CLEANPASS on exact final package/seal. Attributed note only; exact contemporary overlap and no novelty/firstness/independence/simultaneity; qualified least period retained. Prepared75 stays historical/unaccepted. Publicationready true; no actual Zenodo/deposit/tracker/PRmerge/advance.46completed/30published,last203,cursor204/advancefalse.\n'
    for rel in [CASE+'RESEARCH_LOG.md',PREFIX+'CURRENT_PROGRESS.md',PREFIX+'RESEARCH_LOG.md']:out[rel]=v.native_body(h,rel,parent)+note.encode()
    require(Q not in out and not any(k.startswith('unsolved_math_prioritization/attempts/') for k in out),'Native/QUEUE edit forbidden');return out
def message(d):return 'PR204 ready90: final attributed package and accepted whole reviews\n\nActualpriority60 baseline; prepared75 historical/unaccepted. No novelty/firstness/independence certificate or actual deposit/tracker/PRmerge.46completed/30published,last203,cursor204,advancefalse.\nPR204 readiness selected-map SHA256: '+d
v.message=message
def facts(b):return {'case_percent':90,'Root_publication_gate_pin':b['Root_publication_gate_pin'],'baseline_actual_priority60_acceptance_pin':m.BASE_ACCEPT,'package75_historical_unaccepted_not_baseline':True,'mathematical_clearance':True,'source_contract_clearance':True,'source_contract_clearance_qualified':True,'verification_integrity_required_repairs_complete':True,'assigned_mathematical_audits_complete':4,'bounded_priority_audit_complete':True,'priority_clearance':True,'priority_clearance_scope':'bounded_priority_audit_and_qualified_attributed_note_only','qualified_attributed_note_editorially_cleared':True,'exact_contemporary_theorem_overlap':True,'priority_novelty_clearance':False,'historical_firstness_independence_established':False,'historical_firstness_independence_simultaneity_established':False,'whole_package_review_loop_complete':True,'whole_package_reviews_complete':True,'NEW_whole_package_reviews_completed':b['whole_package_reviews_completed'],'publication_ready':True,'package':b['package'],'package_seal':b['package_seal'],'actual_publication_verified':False,'actual_tracker_row_verified':False,'actual_original_PR_merged':False,'fully_completed_count':46,'published_count':30,'last_completed_PR':203,'next_numeric_intake_cursor':204,'advance_to_next_PR_authorized_now':False,'goal_complete':False}
def run(mode,name):
    b=binding(name) # Fail before native runtime/API if future gate is absent.
    c,h,rv,n=v.load();base=m.baseline(c);dest=generation(name)
    if mode=='prepare':
        require(not (dest/'PREPARATION.json').exists(),'Generation already prepared');parent=h.api('git/ref/heads/main')['object']['sha'];require(h.api('compare/'+m.BASE_COMMIT+'...'+parent)['status'] in ['identical','ahead'],'MAIN lacks actualpriority60_02')
        inherited,ack=v.reconcile(c,h,base,parent);pt=c.selected_current(h,parent,inherited,base['tree']);v.validate_caches(h);v.unchanged_pr();stamp=now();out=overlay(c,h,parent,stamp,b,name);local_pre={}
        for rel in VIEWS:
            f=ROOT/rel;remote=v.native_body(h,rel,parent);require(f.is_file() and not f.is_symlink() and pin(f.read_bytes())==pin(remote),'Fresh-parent60/local5 drift '+rel);local_pre[rel]=pin(remote)
        save(dest/'FOREIGN_QUEUE_RECONCILIATION.json',enc(ack));out[OWN+name+'/FOREIGN_QUEUE_RECONCILIATION.json']=(dest/'FOREIGN_QUEUE_RECONCILIATION.json').read_bytes();expected=v.selected(c,inherited,out)
        tree=h.api('git/trees','POST',{'base_tree':pt,'tree':m.entries(c,h,out)})['sha'];commit=h.api('git/commits','POST',{'tree':tree,'parents':[parent],'message':message(c.selected_digest(expected))})['sha'];h.m.m.h.warm_selected_directories([pt,tree],expected)
        r={'UTC':stamp,'PR':204,'phase':'ready90',**facts(b),'original_head':HEAD,'expected_main':parent,'parent_tree':pt,'tree':tree,'commit':commit,'selected_files':expected,'selected_map_sha256':c.selected_digest(expected),'overlay_paths':sorted(out),'changed_paths':sorted(k for k,x in expected.items() if h.lookup(pt,k)!=('100644','blob',x['git_blob'])),'local_five_expected_preimages':local_pre,'MAIN_moved':False};save(dest/'PREPARATION.json',enc(r))
    else:
        r=read(dest/'PREPARATION.json');require(r['phase']=='ready90' and all(r[k]==x for k,x in facts(b).items()),'Prepared phase facts');parent=r['expected_main'];ack=read(dest/'FOREIGN_QUEUE_RECONCILIATION.json');inherited={**base['selected_files'],Q:ack['current_QUEUE']};out=overlay(c,h,parent,r['UTC'],b,name);out[OWN+name+'/FOREIGN_QUEUE_RECONCILIATION.json']=(dest/'FOREIGN_QUEUE_RECONCILIATION.json').read_bytes();expected=v.selected(c,inherited,out)
    v.verify(c,h,r,out,expected);main=h.api('git/ref/heads/main')['object']['sha']
    if mode in ['prepare','verify']:
        require(main==parent,'MAIN changed; fresh binding/prepare generation required');pre={'UTC':now(),'PR':204,'phase':'ready90','commit':r['commit'],'expected_main':parent,'observed_MAIN':main,'exact_single_trueparent_fullforeignscope_everyselectedidentity_verified':True,'original_head_unchanged':True,'no_QUEUE_native_or_PR_mutation':True,'selected_files':len(expected),'selected_map_sha256':r['selected_map_sha256'],'actual_MAIN_acceptance':False,**facts(b)}
        if mode=='prepare':save(dest/'ROOT_PRE_MOVE_VERIFICATION.json',enc(pre))
        print(json.dumps({'mode':mode,'expected_main':parent,'commit':r['commit'],'tree':r['tree'],'selected_files':len(expected),'selected_map_sha256':r['selected_map_sha256'],'changed_paths':len(r['changed_paths']),'observed_MAIN':main,**facts(b)}));return
    require(mode=='accept','Unsupported phase');require(h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'],'ActualMAIN lacks ready checkpoint');actual,post=v.reconcile(c,h,r,main);at=c.selected_current(h,main,actual,r['tree']);v.validate_caches(h);v.unchanged_pr()
    for k,z in out.items():require(c.byte_pin(z)==expected[k] and h.lookup(at,k)==('100644','blob',expected[k]['git_blob']),'Actualoverlay drift '+k)
    body=enc({'selected_files':actual,'selected_map_sha256':c.selected_digest(actual),'foreign_QUEUE_reconciliation_after_checkpoint':post});save(dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json',body)
    a={'UTC':now(),'PR':204,'phase':'ready90','accepted':True,'checkpoint_commit':r['commit'],'sole_parent':parent,'main_observed':main,'actual_tree':at,'original_head':HEAD,'original_PR_open_draft_unchanged':True,'selected_files':len(actual),'selected_map_sha256':r['selected_map_sha256'],'actual_current_selected_map_sha256':c.selected_digest(actual),'actual_current_map_file':pin(body),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_overlay_body_identities_verified':True,'full_foreign_tree_scope_preserved':True,'full_foreign_tree_scope_preserved_at_checkpoint':True,'foreign_QUEUE_exact_byte_acknowledgement':True,'QUEUE_native_original_PR_unchanged':True,'QUEUE_native_original_PR_unchanged_by_checkpoint':True,**facts(b)};save(dest/'ACCEPTANCE.json',enc(a));print(json.dumps(a))
def sync(name):
    b=binding(name);c,h,rv,n=v.load();dest=generation(name);r=read(dest/'PREPARATION.json');a=read(dest/'ACCEPTANCE.json');mp=read(dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json');require(a['accepted'] and a['every_selected_identity_checked_at_actual_observed_MAIN'] and a['checkpoint_commit']==r['commit'] and all(a[k]==x for k,x in facts(b).items()),'Actual ready90 acceptance required');require(a['actual_current_map_file']==pin((dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json').read_bytes()) and mp['selected_map_sha256']==a['actual_current_selected_map_sha256']==c.selected_digest(mp['selected_files']),'Actualmap drift')
    main=h.api('git/ref/heads/main')['object']['sha'];require(h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'],'Ready checkpoint no longer on MAIN');c.selected_current(h,main,mp['selected_files'],a['actual_tree']);v.validate_caches(h);rows=[]
    for rel in VIEWS:
        f=ROOT/rel;post=v.native_body(h,rel,r['commit']);require(c.byte_pin(post)==r['selected_files'][rel],'Localpostimage drift');old=f.read_bytes();require(pin(old) in [r['local_five_expected_preimages'][rel],pin(post)],'Unexpected localview change '+rel)
        if old!=post:
            tmp=f.with_name(f.name+'.pr204_ready90_sync_tmp')
            with tmp.open('xb') as stream:stream.write(post);stream.flush();os.fsync(stream.fileno())
            require(tmp.read_bytes()==post,'Temporarybytes');tmp.chmod(0o444);os.replace(tmp,f);fsync_directory(f.parent)
        f.chmod(0o444);require(f.read_bytes()==post,'Localreadback');rows.append({'path':rel,'postimage':pin(post),'prior_or_postimage_guard':True})
    j={'UTC':now(),'PR':204,'phase':'ready90','actual_checkpoint':r['commit'],'all_five_local_files_match_actual_checkpoint':True,'files':rows,**facts(b)};save(dest/'LOCAL_GLOBAL_FIVE_SYNC.json',enc(j));print(json.dumps(j))
def pointer(name):
    b=binding(name);dest=generation(name);r=read(dest/'PREPARATION.json');a=read(dest/'ACCEPTANCE.json');x=read(dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json');require(a['accepted'] and a['phase']=='ready90' and a['checkpoint_commit']==r['commit'] and a['every_selected_identity_checked_at_actual_observed_MAIN'] and all(a[k]==z for k,z in facts(b).items()),'Actual final ready90 receipt required')
    require(pin((dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json').read_bytes())==a['actual_current_map_file'],'Actual ready map pin');c,h,rv,n=v.load();require(c.selected_digest(x['selected_files'])==x['selected_map_sha256']==a['actual_current_selected_map_sha256'],'Actual ready selected digest');main=h.api('git/ref/heads/main')['object']['sha'];require(h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'],'Ready checkpoint not on MAIN');c.selected_current(h,main,x['selected_files'],a['actual_tree']);v.validate_caches(h);v.unchanged_pr()
    j={'UTC':now(),'PR':204,'phase':'ready','directory':'publication_checkpoint_02/'+name,'checkpoint_commit':a['checkpoint_commit'],'main_observed':a['main_observed'],'fresh_MAIN_revalidated_before_pointer':main,'acceptance_pin':pin((dest/'ACCEPTANCE.json').read_bytes()),'Root_recorded_only_after_actual_full_scope_acceptance':True};f=A/'ROOT_ACTUAL_READY_CHECKPOINT.json'
    with f.open('xb') as out:out.write(enc(j));out.flush();os.fchmod(out.fileno(),0o444);os.fsync(out.fileno())
    fsync_directory(f.parent);print(json.dumps(j))
if __name__=='__main__':
    require(len(sys.argv)>=2,'bind GEN GATE_BYTES GATE_SHA256 | prepare/verify/accept/sync/pointer GEN');mode=sys.argv[1]
    if mode=='bind':require(len(sys.argv)==5 and sys.argv[3].isdigit(),'bind GEN GATE_BYTES GATE_SHA256');bind(sys.argv[2],int(sys.argv[3]),sys.argv[4])
    elif mode in ['sync','pointer']:require(len(sys.argv)==3,mode+' GEN');{'sync':sync,'pointer':pointer}[mode](sys.argv[2])
    else:require(mode in ['prepare','verify','accept'] and len(sys.argv)==3,'Unknown phase');run(mode,sys.argv[2])
