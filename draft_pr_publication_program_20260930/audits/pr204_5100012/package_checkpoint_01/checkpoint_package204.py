"""PR204 proposed package75. No binding/preparation until exact final Root gate.
Root alone executes remote native object preparation; ref/CAS/PR writes absent.
"""
from pathlib import Path
import base64,datetime,hashlib,importlib.util,json,os,re,sys
if sys.flags.optimize or not sys.dont_write_bytecode:raise RuntimeError('Use ordinary Python with -B; no optimization or bytecode writes')
D=Path(__file__).resolve().parent;A=D.parent;P=A.parent.parent;ROOT=P.parent
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
PRIOR_HELPER_PIN={'bytes':23095,'sha256':'f6ba74702b686b477c36771ac2293b0554339dd98ac9414b21bf523dad9a4002'}
f=A/'priority_checkpoint_01/checkpoint_priority204.py';require(pin(f.read_bytes())==PRIOR_HELPER_PIN,'Sealed priority helper drift')
s=importlib.util.spec_from_file_location('package204_priority_native_primitives',f);p=importlib.util.module_from_spec(s);s.loader.exec_module(p);v=p.v
CASE=v.CASE;PREFIX=v.PREFIX;Q=v.Q;HEAD=v.HEAD;VIEWS=v.VIEWS;OWN=CASE+'package_checkpoint_01/'
PRIOR=A/'priority_checkpoint_01/priority60_02';BASE_COMMIT='bee7f68f35cb1b74053ff3be320fd459c3488287';BASE_TREE='fa73688a491bc15d68ac882542012d4be980399b'
BASE_DIGEST='3e0fbf43b99eb1407b1476e6dbf2d3e080629d945d61f53ca78670bb410977df'
BASE_ACCEPT={'bytes':2363,'sha256':'c2a517b26837226d7e29e61e0dc68ff083874af1b337e401c942fe8c1e9b6508'}
BASE_MAP={'bytes':1088220,'sha256':'176703e8cceccfe82125dddae14d38eb76ef4a19825729b494fb893a928c98af'}
GATE='ROOT_PACKAGE_PREPARATION_ACCEPTANCE_01.json'
OWN_FILES=['checkpoint_package204.py','CHECKPOINT_CONTRACT.md','RESEARCH_LOG.md','SAFE_AUTHORED_MANIFEST.json']
STATUS='ATTRIBUTED_PACKAGE_PREPARED_FRESH_WHOLE_PACKAGE_REVIEW_REQUIRED'
REMAIN='Assign a NEW independent entire-package adversary to the sealed attributed package; repair every substantive issue, then obtain another NEW entire-package review until clean. Package preparation supplies no publication/release authority. Actual DOI/deposit/publicdownload verification, tracker append/readback, originalHEAD-safe merge and factual completion remain; no next-PR advance.'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def enc(j):return (json.dumps(j,indent=2)+'\n').encode()
def read(f):return json.loads(f.read_bytes())
def save(f,b):
    require(f.resolve().is_relative_to(D),'Output outside own package helper directory')
    with f.open('xb') as h:h.write(b);h.flush();os.fsync(h.fileno())
    f.chmod(0o444)
def frozen(rel,x=None):
    p.m.safe_relative(rel);f=A/rel;require(f.is_file() and not f.is_symlink() and f.stat().st_mode&0o777==0o444,'Missing/unfrozen public artifact '+rel);b=f.read_bytes()
    if x is not None:require(pin(b)==x,'Pinned public artifact drift '+rel)
    return b
def baseline(c):
    a=json.loads(frozen('priority_checkpoint_01/priority60_02/ACCEPTANCE.json',BASE_ACCEPT));mb=(PRIOR/'ACCEPTANCE_CURRENT_SELECTED_MAP.json').read_bytes();require(pin(mb)==BASE_MAP,'Actualpriority60 map drift');x=json.loads(mb)
    require(a['accepted'] and a['every_selected_identity_checked_at_actual_observed_MAIN'] and a['checkpoint_commit']==a['main_observed']==BASE_COMMIT and a['actual_tree']==BASE_TREE,'Actualpriority60_02 receipt required; unaccepted attempt01 excluded')
    require(a['phase']=='priority60' and a['case_percent']==60 and a['bounded_priority_audit_complete'] and not a['priority_novelty_clearance'] and a['verification_integrity_required_repairs_complete'],'Prior scientific/editorial scope')
    require(len(x['selected_files'])==a['selected_files']==3630 and x['selected_map_sha256']==a['actual_current_selected_map_sha256']==c.selected_digest(x['selected_files'])==BASE_DIGEST and a['actual_current_map_file']==BASE_MAP,'Actual3630selected baseline')
    require((a['fully_completed_count'],a['published_count'],a['last_completed_PR'],a['next_numeric_intake_cursor'],a['advance_to_next_PR_authorized_now'])==(46,30,203,204,False),'Prior actual counters')
    return {'commit':BASE_COMMIT,'tree':BASE_TREE,'selected_files':x['selected_files'],'selected_map_sha256':BASE_DIGEST}
def generation(name):require(re.fullmatch('[a-z][a-z0-9_]{0,48}',name) is not None,'Unsafe generation name');return D/name
def static_manifest():
    f=D/'SAFE_AUTHORED_MANIFEST.json';require(f.exists(),'Authored helper manifest missing');j=read(f);require(set(j['files'])==set(OWN_FILES)-{f.name},'Exact static helper allowlist')
    for name,x in j['files'].items():frozen('package_checkpoint_01/'+name,x)
    return pin(f.read_bytes())
def gate_inputs(gate_pin):
    require(set(gate_pin)=={'bytes','sha256'} and isinstance(gate_pin['bytes'],int) and gate_pin['bytes']>0 and re.fullmatch('[0-9a-f]{64}',gate_pin['sha256']) is not None,'Explicit exact final Root gate bytes/SHA256 required')
    require((A/GATE).exists(),'Final Root package gate missing; binding/preparation forbidden')
    gb=frozen(GATE,gate_pin);g=json.loads(gb)
    require((g['PR'],g['original_head'],g['estimate_case_completion_percent'])==(204,HEAD,75),'Package gate identity/phase')
    require(g['package_preparation_accepted'] is True and g['publication_ready'] is False and g['release_authorized_by_this_gate'] is False and g['whole_package_reviews_complete'] is False and g['NEW_whole_package_reviews_completed']==0,'Preparation-only gate; no release/review clearance')
    package=g['package'];require(re.fullmatch('publication_package_[a-zA-Z0-9_]+',package) is not None,'Explicit package directory name required')
    allowed=g['safe_files'];require(isinstance(allowed,dict) and allowed and GATE not in allowed,'Explicit nonrecursive public allowlist required');out={GATE:gate_pin}
    for rel,x in allowed.items():
        p.m.safe_relative(rel);require(set(x)=={'bytes','sha256'},'Public file pin schema')
        require(not any(t in Path(rel).parts for t in ['__pycache__','.venv','site-packages','primary_source_private']) and not rel.endswith(('.pyc','.pyo')),'Private/cache/dependency file forbidden')
        require('ACCEPTANCE_CURRENT_SELECTED_MAP.json' not in rel,'Private actual selected maps must not be copied')
        out[rel]=pin(frozen(rel,x))
    pd=A/package;require(pd.is_dir() and not pd.is_symlink(),'Package directory absent/unsafe');actual=set()
    for f in pd.rglob('*'):
        require(not f.is_symlink(),'Symlink inside public package')
        if f.is_file():actual.add(f.relative_to(A).as_posix())
    listed={rel for rel in allowed if rel.startswith(package+'/')};require(actual==listed and actual,'Full package directory differs from explicit final Root allowlist')
    seal=g['package_seal'];require(set(seal)=={'path','bytes','sha256'} and seal['path'].startswith(package+'/') and out.get(seal['path'])=={k:seal[k] for k in ['bytes','sha256']},'Exact package seal file binding')
    rel='priority_checkpoint_01/priority60_02/ACCEPTANCE.json';out[rel]=pin(frozen(rel,BASE_ACCEPT))
    return {'PR':204,'phase':'package75','case_percent':75,'Root_package_gate_pin':gate_pin,'package':package,'package_seal':seal,'files':out,'static_authored_manifest_pin':static_manifest(),'baseline_actual_commit':BASE_COMMIT,'baseline_actual_tree':BASE_TREE,'baseline_actual_acceptance_pin':BASE_ACCEPT,'baseline_actual_map_file_pin':BASE_MAP,'baseline_selected_files':3630,'baseline_selected_map_sha256':BASE_DIGEST,'release_authorized':False,'publication_ready':False,'fresh_whole_package_reviews_completed':0,'no_actual_deposit_tracker_or_merge':True}
def bind(name,size,digest):
    dest=generation(name);require(not dest.exists(),'Generation already exists; choose a fresh name');j=gate_inputs({'bytes':size,'sha256':digest});j['UTC']=now();dest.mkdir();save(dest/'PACKAGE_INPUT_BINDINGS.json',enc(j));print(json.dumps({'bound':True,'generation':name,'files':len(j['files']),'input_bytes':sum(x['bytes'] for x in j['files'].values()),'Root_gate_pin':j['Root_package_gate_pin'],'no_remote_mutation':True}))
def binding(name):
    f=generation(name)/'PACKAGE_INPUT_BINDINGS.json';require(f.is_file(),'Final Root gate binding missing; no prepare allowed');j=read(f);fresh=gate_inputs(j['Root_package_gate_pin']);require({k:x for k,x in j.items() if k!='UTC'}==fresh,'Sealed package binding drift');return j
def prior_views(case,progress):
    require((case['PR'],case['original_head'],case['case_percent'],progress['current_PR'],progress['current_PR_workflow_percent'])==(204,HEAD,60,204,60),'Actualpriority60 views required')
    require(case['mathematical_clearance'] and case['source_contract_clearance_qualified'] and case['verification_integrity_required_repairs_complete'] and case['independent_mathematical_families_complete']==4 and case['bounded_priority_audit_complete'] and not case['priority_novelty_clearance'],'Accepted limited-independence science/repair/priority scope must remain')
    require((progress['fully_completed_count'],progress['published_count'],progress['last_completed_PR'],progress['advance_to_next_PR_authorized_now'])==(46,30,203,False),'Prior counters')
def overlay(c,h,parent,stamp,b,name):
    out={CASE+rel:frozen(rel,x) for rel,x in b['files'].items()}
    for n in OWN_FILES:out[OWN+n]=frozen('package_checkpoint_01/'+n)
    out[OWN+name+'/PACKAGE_INPUT_BINDINGS.json']=(generation(name)/'PACKAGE_INPUT_BINDINGS.json').read_bytes()
    case=json.loads(v.native_body(h,CASE+'CURRENT_CASE_STATUS.json',parent));progress=json.loads(v.native_body(h,PREFIX+'CURRENT_PROGRESS.json',parent));prior_views(case,progress)
    case.setdefault('historical_phase_snapshots',[]).append({'UTC':stamp,'phase':'actualpriority60_before_package75','actual_checkpoint':BASE_COMMIT,'values':{k:x for k,x in case.items() if k!='historical_phase_snapshots'}})
    progress.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':204,'prior_phase':'actualpriority60_before_package75','actual_checkpoint':BASE_COMMIT,'values':{k:x for k,x in progress.items() if k.startswith('current_')}})
    ref={'path':'audits/pr204_5100012/'+GATE,**b['Root_package_gate_pin']}
    case.update(UTC=stamp,status=STATUS,case_percent=75,paper_prepared=True,publication_package=b['package'],publication_package_seal=b['package_seal'],package_preparation_gate=ref,package_prepared=True,portable_and_visual_preparation_accepted_by_Root=True,whole_publication_package_reviews_complete=False,NEW_whole_package_reviews_completed=0,NEW_whole_package_review_active=False,next_NEW_whole_package_review_planned=True,release_authorized_by_this_gate=False,publication_ready=False,deposit_prepared=False,actual_Zenodo_published=False,actual_tracker_updated=False,actual_original_PR_merged=False,actual_factual_MAIN_accepted=False,completed=False,remaining_required_steps=REMAIN)
    out[CASE+'CURRENT_CASE_STATUS.json']=enc(case)
    progress.update(UTC=stamp,updated_UTC=stamp,current_status=STATUS,current_PR_workflow_percent=75,current_workflow_estimate_percent=75,current_paper_prepared=True,current_publication_package=b['package'],current_publication_package_seal=b['package_seal'],current_package_preparation_gate=ref,current_package_prepared=True,current_portable_and_visual_preparation_accepted_by_Root=True,current_publication_package_reviews_complete=False,current_NEW_whole_publication_package_reviews_completed=0,current_NEW_whole_publication_package_review_active=False,current_next_NEW_whole_package_review_planned=True,current_release_authorized_by_this_gate=False,current_publication_ready=False,current_deposit_prepared=False,current_Zenodo_published=False,current_DOI=None,current_tracker_updated=False,current_tracker_range=None,current_actual_publication_verified=False,current_actual_tracker_row_verified=False,current_actual_merge_accepted=False,current_actual_factual_checkpoint_accepted=False,current_completed=False,current_remaining_required_steps=REMAIN,remaining_current_step=REMAIN,next_step=REMAIN,next_numeric_intake_cursor=204,conditional_next_numeric_intake_cursor=205,advance_to_next_PR_authorized_now=False,program_snapshot_semantics='PR204 sealed attributed alternative-proof/reproducibility package prepared75; exact Ferudun theorem/formula/method overlap and no novelty/firstness/independence/simultaneity retained. Root accepted portable/visual/assembly preparation; zero NEW whole-package reviews, next fresh review planned. Package preparation is not release readiness.46completed/30published,last203,cursor204/advancefalse.',program_snapshot_authority_condition='Package75 postimage effective only after actual trueparent/fullforeignscope/everyselectedidentity acceptance. Exact final Root package gate required; no release/DOI/tracker/PRmerge/advance authority.')
    out[PREFIX+'CURRENT_PROGRESS.json']=enc(progress)
    note='\n'+stamp+' — PR204 package75%: exact Root-gated attributed alternative-proof/reproducibility package '+b['package']+' prepared and sealed, portable/visual/assembly records authenticated. Four assigned mathematical audits, qualified source/required repairs and exact Ferudun overlap retained; no novelty/firstness/independent-discovery/simultaneity. Zero fresh whole-package reviews; next NEW adversary planned. Publicationready/releasefalse, no DOI/deposit/tracker/PRmerge/advance.46completed/30published,last203,cursor204/advancefalse.\n'
    for rel in [CASE+'RESEARCH_LOG.md',PREFIX+'CURRENT_PROGRESS.md',PREFIX+'RESEARCH_LOG.md']:out[rel]=v.native_body(h,rel,parent)+note.encode()
    require(Q not in out and not any(k.startswith('unsolved_math_prioritization/attempts/') for k in out),'Native/QUEUE edit forbidden');return out
def message(d):return 'PR204 package75: attributed package prepared; fresh review required\n\nExact contemporary theorem/formula/method credited; no novelty/firstness/independence certificate. Zero fresh whole-package reviews; release/publicationready false.46completed/30published,last203,cursor204,advancefalse.\nPR204 package selected-map SHA256: '+d
v.message=message
def facts(b):return {'case_percent':75,'Root_package_gate_pin':b['Root_package_gate_pin'],'baseline_actual_priority60_acceptance_pin':BASE_ACCEPT,'mathematical_clearance':True,'source_contract_clearance_qualified':True,'verification_integrity_required_repairs_complete':True,'assigned_mathematical_audits_complete':4,'bounded_priority_audit_complete':True,'exact_contemporary_theorem_overlap':True,'priority_novelty_clearance':False,'qualified_attributed_note_preparation_authorized':True,'historical_firstness_independence_simultaneity_established':False,'package_prepared':True,'package':b['package'],'package_seal':b['package_seal'],'fresh_whole_package_reviews_completed':0,'next_fresh_review_planned':True,'whole_package_reviews_complete':False,'release_authorized':False,'publication_ready':False,'actual_deposit_tracker_or_PR_merge':False,'fully_completed_count':46,'published_count':30,'last_completed_PR':203,'next_numeric_intake_cursor':204,'advance_to_next_PR_authorized_now':False,'goal_complete':False}
def entries(c,h,out):
    result=[]
    for rel,b in sorted(out.items()):
        try:content=b.decode('utf-8')
        except UnicodeDecodeError:
            sha=h.api('git/blobs','POST',{'encoding':'base64','content':base64.b64encode(b).decode()})['sha'];require(sha==c.byte_pin(b)['git_blob'],'Binary native blob identity');result.append({'path':rel,'mode':'100644','type':'blob','sha':sha})
        else:result.append({'path':rel,'mode':'100644','type':'blob','content':content})
    return result
def run(mode,name):
    b=binding(name) # Missing final binding fails before native runtime load or API call.
    c,h,rv,n=v.load();base=baseline(c);dest=generation(name)
    if mode=='prepare':
        require(not (dest/'PREPARATION.json').exists(),'Generation already prepared');parent=h.api('git/ref/heads/main')['object']['sha'];require(h.api('compare/'+BASE_COMMIT+'...'+parent)['status'] in ['identical','ahead'],'MAIN lacks actualpriority60_02')
        inherited,ack=v.reconcile(c,h,base,parent);pt=c.selected_current(h,parent,inherited,base['tree']);v.validate_caches(h);v.unchanged_pr();stamp=now();out=overlay(c,h,parent,stamp,b,name);local_pre={}
        for rel in VIEWS:
            f=ROOT/rel;remote=v.native_body(h,rel,parent);require(f.is_file() and not f.is_symlink() and pin(f.read_bytes())==pin(remote),'Local5/freshparent60 drift '+rel);local_pre[rel]=pin(remote)
        save(dest/'FOREIGN_QUEUE_RECONCILIATION.json',enc(ack));out[OWN+name+'/FOREIGN_QUEUE_RECONCILIATION.json']=(dest/'FOREIGN_QUEUE_RECONCILIATION.json').read_bytes();expected=v.selected(c,inherited,out)
        tree=h.api('git/trees','POST',{'base_tree':pt,'tree':entries(c,h,out)})['sha'];commit=h.api('git/commits','POST',{'tree':tree,'parents':[parent],'message':message(c.selected_digest(expected))})['sha'];h.m.m.h.warm_selected_directories([pt,tree],expected)
        r={'UTC':stamp,'PR':204,'phase':'package75',**facts(b),'original_head':HEAD,'expected_main':parent,'parent_tree':pt,'tree':tree,'commit':commit,'selected_files':expected,'selected_map_sha256':c.selected_digest(expected),'overlay_paths':sorted(out),'changed_paths':sorted(k for k,x in expected.items() if h.lookup(pt,k)!=('100644','blob',x['git_blob'])),'local_five_expected_preimages':local_pre,'MAIN_moved':False};save(dest/'PREPARATION.json',enc(r))
    else:
        r=read(dest/'PREPARATION.json');require(r['phase']=='package75' and all(r[k]==x for k,x in facts(b).items()),'Prepared phase facts');parent=r['expected_main'];ack=read(dest/'FOREIGN_QUEUE_RECONCILIATION.json');inherited={**base['selected_files'],Q:ack['current_QUEUE']};out=overlay(c,h,parent,r['UTC'],b,name);out[OWN+name+'/FOREIGN_QUEUE_RECONCILIATION.json']=(dest/'FOREIGN_QUEUE_RECONCILIATION.json').read_bytes();expected=v.selected(c,inherited,out)
    v.verify(c,h,r,out,expected);main=h.api('git/ref/heads/main')['object']['sha']
    if mode in ['prepare','verify']:
        require(main==parent,'MAIN changed; fresh binding generation/prepare required');pre={'UTC':now(),'PR':204,'phase':'package75','commit':r['commit'],'expected_main':parent,'observed_MAIN':main,'exact_single_trueparent_fullforeignscope_everyselectedidentity_verified':True,'original_head_unchanged':True,'no_QUEUE_native_or_PR_mutation':True,'selected_files':len(expected),'selected_map_sha256':r['selected_map_sha256'],'actual_MAIN_acceptance':False,**facts(b)}
        if mode=='prepare':save(dest/'ROOT_PRE_MOVE_VERIFICATION.json',enc(pre))
        print(json.dumps({'mode':mode,'expected_main':parent,'commit':r['commit'],'tree':r['tree'],'selected_files':len(expected),'selected_map_sha256':r['selected_map_sha256'],'changed_paths':len(r['changed_paths']),'observed_MAIN':main,**facts(b)}));return
    require(mode=='accept','Unsupported phase');require(h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'],'ActualMAIN lacks checkpoint');actual,post=v.reconcile(c,h,r,main);at=c.selected_current(h,main,actual,r['tree']);v.validate_caches(h);v.unchanged_pr()
    for k,z in out.items():require(c.byte_pin(z)==expected[k] and h.lookup(at,k)==('100644','blob',expected[k]['git_blob']),'Actualoverlay drift '+k)
    body=enc({'selected_files':actual,'selected_map_sha256':c.selected_digest(actual),'foreign_QUEUE_reconciliation_after_checkpoint':post});save(dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json',body)
    a={'UTC':now(),'PR':204,'phase':'package75','accepted':True,'checkpoint_commit':r['commit'],'sole_parent':parent,'main_observed':main,'actual_tree':at,'original_head':HEAD,'original_PR_open_draft_unchanged':True,'selected_files':len(actual),'selected_map_sha256':r['selected_map_sha256'],'actual_current_selected_map_sha256':c.selected_digest(actual),'actual_current_map_file':pin(body),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_overlay_body_identities_verified':True,'full_foreign_tree_scope_preserved_at_checkpoint':True,'foreign_QUEUE_exact_byte_acknowledgement':True,'QUEUE_native_original_PR_unchanged_by_checkpoint':True,**facts(b)};save(dest/'ACCEPTANCE.json',enc(a));print(json.dumps(a))
def sync(name):
    b=binding(name);c,h,rv,n=v.load();dest=generation(name);r=read(dest/'PREPARATION.json');a=read(dest/'ACCEPTANCE.json');mp=read(dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json');require(a['accepted'] and a['every_selected_identity_checked_at_actual_observed_MAIN'] and a['checkpoint_commit']==r['commit'] and all(a[k]==x for k,x in facts(b).items()),'Actualpackage75 acceptance required');require(a['actual_current_map_file']==pin((dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json').read_bytes()) and mp['selected_map_sha256']==a['actual_current_selected_map_sha256']==c.selected_digest(mp['selected_files']),'Actualmap drift')
    main=h.api('git/ref/heads/main')['object']['sha'];require(h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'],'Checkpoint no longer on MAIN');c.selected_current(h,main,mp['selected_files'],a['actual_tree']);v.validate_caches(h);rows=[]
    for rel in VIEWS:
        f=ROOT/rel;post=v.native_body(h,rel,r['commit']);require(c.byte_pin(post)==r['selected_files'][rel],'Localpostimage drift');old=f.read_bytes();require(pin(old) in [r['local_five_expected_preimages'][rel],pin(post)],'Unexpected localview change '+rel)
        if old!=post:
            tmp=f.with_name(f.name+'.pr204_package75_sync_tmp')
            with tmp.open('xb') as stream:stream.write(post);stream.flush();os.fsync(stream.fileno())
            require(tmp.read_bytes()==post,'Temporarybytes');tmp.chmod(0o444);os.replace(tmp,f)
        f.chmod(0o444);require(f.read_bytes()==post,'Localreadback');rows.append({'path':rel,'postimage':pin(post),'prior_or_postimage_guard':True})
    j={'UTC':now(),'PR':204,'phase':'package75','actual_checkpoint':r['commit'],'all_five_local_files_match_actual_checkpoint':True,'files':rows,**facts(b)};save(dest/'LOCAL_GLOBAL_FIVE_SYNC.json',enc(j));print(json.dumps(j))
if __name__=='__main__':
    require(len(sys.argv)>=2,'bind GEN GATE_BYTES GATE_SHA256 | prepare/verify/accept/sync GEN');mode=sys.argv[1]
    if mode=='bind':require(len(sys.argv)==5 and sys.argv[3].isdigit(),'bind GEN GATE_BYTES GATE_SHA256');bind(sys.argv[2],int(sys.argv[3]),sys.argv[4])
    elif mode=='sync':require(len(sys.argv)==3,'sync GEN');sync(sys.argv[2])
    else:require(mode in ['prepare','verify','accept'] and len(sys.argv)==3,'Unknown phase');run(mode,sys.argv[2])
