"""PR204 priority60: actual math45 baseline; bounded priority, attributed note only.
Root alone executes prepare. Native objects only; no ref/PR/tracker/UI mutation.
"""
from pathlib import Path
import datetime,hashlib,importlib.util,json,os,re,sys
if sys.flags.optimize or not sys.dont_write_bytecode:raise RuntimeError('Use ordinary Python with -B; no optimization or bytecode writes')
D=Path(__file__).resolve().parent;A=D.parent;P=A.parent.parent;ROOT=P.parent
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
SCIENCE_PIN={'bytes':31582,'sha256':'0a7c6e203546b3f0ab4bd5ed5cd1c8e0df0886ce5338e3c2db006043a6119602'}
f=A/'science_checkpoint_01/checkpoint_math204.py';require(pin(f.read_bytes())==SCIENCE_PIN,'Sealed science helper drift')
s=importlib.util.spec_from_file_location('priority204_science_native_primitives',f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);v=m.v
CASE=v.CASE;PREFIX=v.PREFIX;Q=v.Q;HEAD=v.HEAD;VIEWS=v.VIEWS;OWN=CASE+'priority_checkpoint_01/'
PRIOR=A/'science_checkpoint_01/math45_01';BASE_COMMIT='2e33e14789b257bee9cc3a88ad212bc6da124abe';BASE_TREE='4a7b8ad23b994009c71b7c4d85d6341a5b7a4be6'
BASE_DIGEST='b8afd94dfe2cd3726b78c4986a7c7e104ef2fd0d5e648f6826a598b4e37b482b'
BASE_ACCEPT={'bytes':2290,'sha256':'660edd6df0d88c31c3a66727e12d9ad35c22219bbf9826afc52cae18a7fff9d5'}
BASE_MAP={'bytes':1081901,'sha256':'3e047bc8c50f87b55177c1dc7b565b06ebcfb533056ab025a287205a4ee35f0b'}
GATE='ROOT_PRIORITY_AND_EDITORIAL_GATE_01.json';GATE_PIN={'bytes':4331,'sha256':'a905da81ebee5d670065659d4a92ff267c8327ab3ae78efac00353feff88bfbe'}
OWN_FILES=['checkpoint_priority204.py','PRIORITY_INPUT_BINDINGS.json','CHECKPOINT_CONTRACT.md','RESEARCH_LOG.md','SAFE_AUTHORED_MANIFEST.json']
STATUS='BOUNDED_PRIORITY_COMPLETE_EXACT_OVERLAP_ATTRIBUTED_NOTE_PREPARATION_ALLOWED'
WARNING='Exact centered theorem and overlapping formula/method in Alper Ferudun DOI10.5281/zenodo.23085904; later method overlap DOI10.5281/zenodo.23400541 also credited. No novel theorem, formula, method, firstness, independent discovery or literal simultaneity established. Object timestamps are not discovery clocks. Printed source omits least/primitive; explicit least physical period remains a qualified necessary convention.'
REMAIN='Prepare and seal an explicitly attributed alternative-proof/reproducibility note and exact package; validate portable runner, then NEW whole-package review/repair/fresh-review loop. Priority novelty clearance false. No release, deposit, tracker change, original PR merge or next-PR advance. Package75 requires separate sealed inputs and gate.'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def enc(j):return (json.dumps(j,indent=2)+'\n').encode()
def read(p):return json.loads(p.read_bytes())
def save(p,b):
    require(p.resolve().is_relative_to(D),'Output outside own priority helper folder')
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    p.chmod(0o444)
def frozen(rel,x=None):
    m.safe_relative(rel);p=A/rel;require(p.is_file() and not p.is_symlink() and p.stat().st_mode&0o777==0o444,'Unfrozen artifact '+rel);b=p.read_bytes()
    if x is not None:require(pin(b)==x,'Frozen artifact drift '+rel)
    return b
def baseline(c):
    ab=frozen('science_checkpoint_01/math45_01/ACCEPTANCE.json',BASE_ACCEPT);mb=(PRIOR/'ACCEPTANCE_CURRENT_SELECTED_MAP.json').read_bytes();require(pin(mb)==BASE_MAP,'Actual math45 map file drift');a=json.loads(ab);x=json.loads(mb)
    require(a['accepted'] and a['every_selected_identity_checked_at_actual_observed_MAIN'] and a['checkpoint_commit']==a['main_observed']==BASE_COMMIT and a['actual_tree']==BASE_TREE,'Actual math45 acceptance authority')
    require(a['phase']=='math45' and a['case_percent']==45 and a['mathematical_clearance'] and a['source_contract_clearance_qualified'] and a['verification_integrity_required_repairs_complete'],'Actual math/source/code scope')
    require(len(x['selected_files'])==a['selected_files']==3608 and x['selected_map_sha256']==a['actual_current_selected_map_sha256']==c.selected_digest(x['selected_files'])==BASE_DIGEST and a['actual_current_map_file']==BASE_MAP,'Actual3608selected math45 map')
    require((a['fully_completed_count'],a['published_count'],a['last_completed_PR'],a['next_numeric_intake_cursor'],a['advance_to_next_PR_authorized_now'])==(46,30,203,204,False),'Actual baseline program counters')
    return {'commit':BASE_COMMIT,'tree':BASE_TREE,'selected_files':x['selected_files'],'selected_map_sha256':BASE_DIGEST}
def inputs():
    gb=frozen(GATE,GATE_PIN);g=json.loads(gb)
    require((g['PR'],g['problem_id'],g['original_head'],g['estimate_case_completion_percent'],g['original_QUEUE_status'],g['original_QUEUE_effort'])==(204,5100012,HEAD,60,'claimed_solved','1/5'),'Priority gate original identity/phase')
    require(g['bounded_priority_audit_complete'] and g['editorial_manuscript_preparation_authorized'] and not g['priority_novelty_clearance'] and not g['release_authorized_by_this_gate'] and not g['publication_ready'],'Qualified editorial gate scope')
    for key in ['novel_theorem_verified','novel_formula_verified','novel_method_verified','independent_discovery_established','historical_firstness_established','literal_simultaneity_established','claim_of_presently_unsolved_problem_resolution_authorized','whole_package_reviews_complete','actual_deposit','actual_tracker_append','actual_PR_merge']:
        require(g[key] is False,'Forbidden priority/publication authority '+key)
    require(g['mathematical_gate']=={'path':m.ROOT_GATE,**m.ROOT_GATE_PIN} and g['verification_repair_gate']=={'path':m.REPAIR_GATE,**m.REPAIR_GATE_PIN},'Prior scientific authority binding')
    out={GATE:GATE_PIN};mr=g['priority_allowlist']['path'];mp={k:g['priority_allowlist'][k] for k in ['bytes','sha256']};man=json.loads(frozen(mr,mp));out[mr]=mp
    require(man['authored_files_only'] and man['third_party_full_text_or_pdf_excluded'],'Priority manifest privacy scope');rows=man['files'];require(len(rows)==g['priority_files_verified']==11 and sum(x['bytes'] for x in rows)==g['priority_content_bytes']==man['total_bytes']==67697,'Priority content census')
    seen=set();folder=Path(mr).parent.as_posix()
    for x in rows:
        name=x['path'];m.safe_relative(name);require(name not in seen,'Duplicate priority file');seen.add(name);rel=folder+'/'+name;out[rel]=pin(frozen(rel,{k:x[k] for k in ['bytes','sha256']}))
    for key in ['priority_report','priority_receipt']:
        x=g[key];require(out[x['path']]=={k:x[k] for k in ['bytes','sha256']},'Root priority report/receipt binding')
    for key in ['Root_primary_access','Root_full_proof_comparison']:
        x=g[key];out[x['path']]=pin(frozen(x['path'],{k:x[k] for k in ['bytes','sha256']}))
    rel='science_checkpoint_01/math45_01/ACCEPTANCE.json';out[rel]=pin(frozen(rel,BASE_ACCEPT))
    require(len(out)==16,'Exact16 existing priority/provenance inputs')
    return {'UTC':now(),'PR':204,'phase':'priority60','case_percent':60,'authority':'Root bounded priority/editorial gate; operational helper authenticates artifacts only.','Root_priority_gate_pin':GATE_PIN,'baseline_actual_commit':BASE_COMMIT,'baseline_actual_tree':BASE_TREE,'baseline_actual_acceptance_pin':BASE_ACCEPT,'baseline_actual_map_file_pin':BASE_MAP,'baseline_actual_selected_files':3608,'baseline_actual_selected_map_sha256':BASE_DIGEST,'actual_map_is_consumed_not_copied_into_overlay':True,'files':out,'bounded_priority_audit_complete':True,'priority_novelty_clearance':False,'qualified_note_preparation_authorized':True,'release_authorized':False,'manuscript_or_package_payload_selected':False}
def check_bindings():
    b=read(D/'PRIORITY_INPUT_BINDINGS.json');fresh=inputs();require({k:x for k,x in b.items() if k!='UTC'}=={k:x for k,x in fresh.items() if k!='UTC'},'Priority snapshot changed')
    j=read(D/'SAFE_AUTHORED_MANIFEST.json');require(set(j['files'])==set(OWN_FILES)-{'SAFE_AUTHORED_MANIFEST.json'},'Priority helper exact allowlist')
    for name,x in j['files'].items():frozen('priority_checkpoint_01/'+name,x)
    return b
def scientific_prior(case,p):
    require((case['PR'],case['original_head'],case['case_percent'],p['current_PR'],p['current_PR_workflow_percent'])==(204,HEAD,45,204,45),'Actual prior phase45 views required')
    require(case['mathematical_clearance'] and case['source_contract_clearance_qualified'] and case['verification_integrity_required_repairs_complete'] and case['independent_mathematical_families_complete']==4,'Retain accepted mathematics/source/repair scope')
    require((p['fully_completed_count'],p['published_count'],p['last_completed_PR'],p['advance_to_next_PR_authorized_now'])==(46,30,203,False),'Prior actual program baseline')
def overlay(c,h,parent,stamp):
    b=check_bindings();out={CASE+rel:frozen(rel,x) for rel,x in b['files'].items()}
    for name in OWN_FILES:out[OWN+name]=frozen('priority_checkpoint_01/'+name)
    case=json.loads(v.native_body(h,CASE+'CURRENT_CASE_STATUS.json',parent));p=json.loads(v.native_body(h,PREFIX+'CURRENT_PROGRESS.json',parent));scientific_prior(case,p)
    case.setdefault('historical_phase_snapshots',[]).append({'UTC':stamp,'phase':'actual_math45_before_priority60','actual_checkpoint':BASE_COMMIT,'values':{k:x for k,x in case.items() if k not in ['historical_phase_snapshots']}})
    p.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':204,'prior_phase':'actual_math45_before_priority60','actual_checkpoint':BASE_COMMIT,'values':{k:x for k,x in p.items() if k.startswith('current_')}})
    gr={'path':'audits/pr204_5100012/'+GATE,**GATE_PIN}
    case.update(UTC=stamp,status=STATUS,case_percent=60,priority_audit_active=False,priority_audit_complete=True,bounded_priority_audit_complete=True,priority_clearance=False,priority_novelty_clearance=False,priority_gate=gr,exact_contemporary_theorem_overlap=True,exact_theorem_overlap_DOI='10.5281/zenodo.23085904',related_later_method_overlap_DOI='10.5281/zenodo.23400541',theorem_novelty_cleared=False,formula_novelty_cleared=False,proof_method_novelty_cleared=False,historical_novelty_or_firstness_established=False,independent_discovery_certified=False,literal_simultaneity_established=False,source_priority_warning=WARNING,qualified_attributed_note_editorially_cleared=True,editorial_manuscript_preparation_authorized=True,release_authorized_by_this_gate=False,paper_draft_started=True,paper_prepared=False,publication_package=None,package_prepared=False,whole_publication_package_reviews_complete=False,NEW_whole_package_reviews_completed=0,publication_ready=False,deposit_prepared=False,actual_Zenodo_published=False,actual_tracker_updated=False,actual_original_PR_merged=False,actual_factual_MAIN_accepted=False,completed=False,remaining_required_steps=REMAIN,checkpoint_postimage_effective_only_after_own_actual_MAIN_full_scope_acceptance=True)
    out[CASE+'CURRENT_CASE_STATUS.json']=enc(case)
    p.update(UTC=stamp,updated_UTC=stamp,current_status=STATUS,current_PR_workflow_percent=60,current_workflow_estimate_percent=60,current_priority_audit_active=False,current_priority_audit_complete=True,current_bounded_priority_audit_complete=True,current_priority_clearance=False,current_priority_novelty_clearance=False,current_priority_gate=gr,current_exact_contemporary_theorem_overlap=True,current_exact_theorem_overlap_DOI='10.5281/zenodo.23085904',current_related_later_method_overlap_DOI='10.5281/zenodo.23400541',current_theorem_novelty_cleared=False,current_formula_novelty_cleared=False,current_proof_method_novelty_cleared=False,current_historical_novelty_or_firstness_established=False,current_independent_discovery_certified=False,current_literal_simultaneity_established=False,current_source_priority_warning=WARNING,current_qualified_attributed_note_editorially_cleared=True,current_editorial_manuscript_preparation_authorized=True,current_release_authorized_by_this_gate=False,current_paper_draft_started=True,current_paper_prepared=False,current_publication_package=None,current_package_prepared=False,current_publication_package_reviews_complete=False,current_NEW_whole_publication_package_reviews_completed=0,current_NEW_whole_publication_package_review_active=False,current_publication_ready=False,current_deposit_prepared=False,current_Zenodo_published=False,current_DOI=None,current_tracker_updated=False,current_tracker_range=None,current_actual_publication_verified=False,current_actual_tracker_row_verified=False,current_actual_merge_accepted=False,current_actual_factual_checkpoint_accepted=False,current_completed=False,current_remaining_required_steps=REMAIN,remaining_current_step=REMAIN,next_step=REMAIN,next_numeric_intake_cursor=204,conditional_next_numeric_intake_cursor=205,advance_to_next_PR_authorized_now=False,program_snapshot_semantics='PR204 bounded priority audit complete60: exact Ferudun DOI23085904 centered theorem/formula/method overlap; no novelty, firstness, certified independence or simultaneity. Root authorizes preparation of an attributed alternative-proof/reproducibility note only. Actualmath45/theorem/source/fourassignedaudits/verificationrepairs retained. Draft started; package not prepared/reviewed; release false.46completed/30published,last203,cursor204/advancefalse.',program_snapshot_authority_condition='Priority60 postimage effective only after actual trueparent/fullforeignscope/everyselectedidentity acceptance. Root gate authorizes manuscript preparation, not release or mathematical priority claims.')
    out[PREFIX+'CURRENT_PROGRESS.json']=enc(p)
    note='\n'+stamp+' — PR204 priority60%: bounded priority DONE; Root accepted exact Ferudun DOI10.5281/zenodo.23085904 theorem/formula/method overlap and later method overlap23400541. No novel theorem/formula/method, historical firstness, independent discovery or literal simultaneity established. Qualified attributed alternate-proof/reproducibility note preparation allowed; releasefalse. Actualmath45/fourassignedaudits and separately accepted verificationrepairs retained. Draft juststarted; package notprepared/reviewed, no manuscript selected in checkpoint. No deposit/tracker/PRmerge/advance.46completed/30published,last203,cursor204/advancefalse.\n'
    for rel in [CASE+'RESEARCH_LOG.md',PREFIX+'CURRENT_PROGRESS.md',PREFIX+'RESEARCH_LOG.md']:out[rel]=v.native_body(h,rel,parent)+note.encode()
    require(Q not in out and not any(k.startswith('unsolved_math_prioritization/attempts/') or k.endswith(('.tex','.pdf','.zip')) for k in out),'Forbidden native/QUEUE/manuscript overlay')
    return out
def message(d):return 'PR204 priority60: exact overlap; attributed note preparation allowed\n\nBounded priority complete; no theorem/formula/method novelty, firstness, certified independence or simultaneity. Actualmath45 and verificationrepairs retained; no release/package/DOI/tracker/merge.46completed/30published,last203,cursor204,advancefalse.\nPR204 priority selected-map SHA256: '+d
v.message=message
def facts():return {'case_percent':60,'Root_priority_gate_pin':GATE_PIN,'baseline_actual_math45_acceptance_pin':BASE_ACCEPT,'mathematical_clearance':True,'source_contract_clearance_qualified':True,'verification_integrity_required_repairs_complete':True,'assigned_mathematical_audits_complete':4,'bounded_priority_audit_complete':True,'priority_audit_active':False,'priority_clearance':False,'priority_novelty_clearance':False,'exact_contemporary_theorem_overlap':True,'theorem_formula_method_novelty_established':False,'historical_firstness_independence_simultaneity_established':False,'qualified_attributed_note_preparation_authorized':True,'release_authorized':False,'package_prepared':False,'whole_package_reviews_complete':False,'publication_ready':False,'actual_deposit_tracker_or_PR_merge':False,'fully_completed_count':46,'published_count':30,'last_completed_PR':203,'next_numeric_intake_cursor':204,'advance_to_next_PR_authorized_now':False,'goal_complete':False}
def generation(name):require(re.fullmatch('[a-z][a-z0-9_]{0,48}',name) is not None,'Unsafe generation name');return D/name
def run(mode,name):
    c,h,rv,n=v.load();base=baseline(c);dest=generation(name)
    if mode=='prepare':
        require(not dest.exists(),'Generation exists');parent=h.api('git/ref/heads/main')['object']['sha'];require(h.api('compare/'+BASE_COMMIT+'...'+parent)['status'] in ['identical','ahead'],'MAIN lacks actualmath45 baseline')
        inherited,ack=v.reconcile(c,h,base,parent);pt=c.selected_current(h,parent,inherited,base['tree']);v.validate_caches(h);v.unchanged_pr();stamp=now();out=overlay(c,h,parent,stamp);local_pre={}
        for rel in VIEWS:
            p=ROOT/rel;remote=v.native_body(h,rel,parent);require(p.is_file() and not p.is_symlink() and pin(p.read_bytes())==pin(remote),'Local5 must equal actual fresh-parent45 '+rel);local_pre[rel]=pin(remote)
        dest.mkdir();save(dest/'FOREIGN_QUEUE_RECONCILIATION.json',enc(ack));out[OWN+name+'/FOREIGN_QUEUE_RECONCILIATION.json']=(dest/'FOREIGN_QUEUE_RECONCILIATION.json').read_bytes();expected=v.selected(c,inherited,out)
        tree=h.api('git/trees','POST',{'base_tree':pt,'tree':[{'path':k,'mode':'100644','type':'blob','content':b.decode('utf-8')} for k,b in sorted(out.items())]})['sha'];commit=h.api('git/commits','POST',{'tree':tree,'parents':[parent],'message':message(c.selected_digest(expected))})['sha'];h.m.m.h.warm_selected_directories([pt,tree],expected)
        r={'UTC':stamp,'PR':204,'phase':'priority60',**facts(),'original_head':HEAD,'expected_main':parent,'parent_tree':pt,'tree':tree,'commit':commit,'selected_files':expected,'selected_map_sha256':c.selected_digest(expected),'overlay_paths':sorted(out),'changed_paths':sorted(k for k,x in expected.items() if h.lookup(pt,k)!=('100644','blob',x['git_blob'])),'local_five_expected_preimages':local_pre,'MAIN_moved':False};save(dest/'PREPARATION.json',enc(r))
    else:
        r=read(dest/'PREPARATION.json');require(r['phase']=='priority60' and all(r[k]==x for k,x in facts().items()),'Prepared phase facts');parent=r['expected_main'];ack=read(dest/'FOREIGN_QUEUE_RECONCILIATION.json');inherited={**base['selected_files'],Q:ack['current_QUEUE']};out=overlay(c,h,parent,r['UTC']);out[OWN+name+'/FOREIGN_QUEUE_RECONCILIATION.json']=(dest/'FOREIGN_QUEUE_RECONCILIATION.json').read_bytes();expected=v.selected(c,inherited,out)
    v.verify(c,h,r,out,expected);main=h.api('git/ref/heads/main')['object']['sha']
    if mode in ['prepare','verify']:
        require(main==parent,'MAIN changed; regenerate against fresh parent');pre={'UTC':now(),'PR':204,'phase':'priority60','commit':r['commit'],'expected_main':parent,'observed_MAIN':main,'exact_single_trueparent_fullforeignscope_everyselectedidentity_verified':True,'original_head_unchanged':True,'no_QUEUE_native_or_PR_mutation':True,'selected_files':len(expected),'selected_map_sha256':r['selected_map_sha256'],'actual_MAIN_acceptance':False,**facts()}
        if mode=='prepare':save(dest/'ROOT_PRE_MOVE_VERIFICATION.json',enc(pre))
        print(json.dumps({'mode':mode,'expected_main':parent,'commit':r['commit'],'tree':r['tree'],'selected_files':len(expected),'selected_map_sha256':r['selected_map_sha256'],'changed_paths':len(r['changed_paths']),'observed_MAIN':main,**facts()}));return
    require(mode=='accept','Unsupported phase');require(h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'],'Actual MAIN lacks checkpoint');actual,post=v.reconcile(c,h,r,main);at=c.selected_current(h,main,actual,r['tree']);v.validate_caches(h);v.unchanged_pr()
    for k,b in out.items():require(c.byte_pin(b)==expected[k] and h.lookup(at,k)==('100644','blob',expected[k]['git_blob']),'Actual overlay identity drift '+k)
    body=enc({'selected_files':actual,'selected_map_sha256':c.selected_digest(actual),'foreign_QUEUE_reconciliation_after_checkpoint':post});save(dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json',body)
    a={'UTC':now(),'PR':204,'phase':'priority60','accepted':True,'checkpoint_commit':r['commit'],'sole_parent':parent,'main_observed':main,'actual_tree':at,'original_head':HEAD,'original_PR_open_draft_unchanged':True,'selected_files':len(actual),'selected_map_sha256':r['selected_map_sha256'],'actual_current_selected_map_sha256':c.selected_digest(actual),'actual_current_map_file':pin(body),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_overlay_body_identities_verified':True,'full_foreign_tree_scope_preserved_at_checkpoint':True,'foreign_QUEUE_exact_byte_acknowledgement':True,'QUEUE_native_original_PR_unchanged_by_checkpoint':True,**facts()};save(dest/'ACCEPTANCE.json',enc(a));print(json.dumps(a))
def sync(name):
    c,h,rv,n=v.load();dest=generation(name);r=read(dest/'PREPARATION.json');a=read(dest/'ACCEPTANCE.json');mp=read(dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json')
    require(a['accepted'] and a['every_selected_identity_checked_at_actual_observed_MAIN'] and a['checkpoint_commit']==r['commit'] and all(a[k]==x for k,x in facts().items()),'Actualpriority60 acceptance required');require(a['actual_current_map_file']==pin((dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json').read_bytes()) and mp['selected_map_sha256']==a['actual_current_selected_map_sha256']==c.selected_digest(mp['selected_files']),'Actualmap drift')
    main=h.api('git/ref/heads/main')['object']['sha'];require(h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'],'Checkpoint no longer on MAIN');c.selected_current(h,main,mp['selected_files'],a['actual_tree']);v.validate_caches(h);rows=[]
    for rel in VIEWS:
        p=ROOT/rel;post=v.native_body(h,rel,r['commit']);require(c.byte_pin(post)==r['selected_files'][rel],'Localpostimage drift');old=p.read_bytes();require(pin(old) in [r['local_five_expected_preimages'][rel],pin(post)],'Unexpected localview change '+rel)
        if old!=post:
            tmp=p.with_name(p.name+'.pr204_priority60_sync_tmp')
            with tmp.open('xb') as f:f.write(post);f.flush();os.fsync(f.fileno())
            require(tmp.read_bytes()==post,'Temporary bytes');tmp.chmod(0o444);os.replace(tmp,p)
        p.chmod(0o444);require(p.read_bytes()==post,'Localreadback');rows.append({'path':rel,'postimage':pin(post),'prior_or_postimage_guard':True})
    j={'UTC':now(),'PR':204,'phase':'priority60','actual_checkpoint':r['commit'],'all_five_local_files_match_actual_checkpoint':True,'files':rows,**facts()};save(dest/'LOCAL_GLOBAL_FIVE_SYNC.json',enc(j));print(json.dumps(j))
if __name__=='__main__':
    require(len(sys.argv)>=2,'bindings | prepare GEN | verify GEN | accept GEN | sync GEN');mode=sys.argv[1]
    if mode=='bindings':require(len(sys.argv)==2,'bindings takes no generation');j=inputs();save(D/'PRIORITY_INPUT_BINDINGS.json',enc(j));print(json.dumps({'phase':'priority60','files':len(j['files']),'input_bytes':sum(x['bytes'] for x in j['files'].values()),'no_remote_mutation':True}))
    elif mode=='sync':require(len(sys.argv)==3,'sync GEN');sync(sys.argv[2])
    else:require(mode in ['prepare','verify','accept'] and len(sys.argv)==3,'Unknown phase');run(mode,sys.argv[2])
