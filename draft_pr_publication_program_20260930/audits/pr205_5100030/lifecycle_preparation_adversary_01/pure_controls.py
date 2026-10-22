"""Independent PR205 operational mutation controls; no real backend/API/action.

Use ordinary Python -B. Source modules import only their own standard libraries;
all data, mock native lookups and writable paths used here are local synthetic
fixtures below this adversary directory. No actual phase entry point is called.
"""
from pathlib import Path
from types import SimpleNamespace
import copy,datetime,hashlib,json,runpy,sys

HERE=Path(__file__).resolve().parent
CASE=HERE.parent
SOURCE=CASE/'publication_lifecycle_preparation_01'
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
WORK=HERE/('synthetic_'+stamp)
WORK.mkdir()

def load(name):
    return SimpleNamespace(**runpy.run_path(str(SOURCE/name)))

# Namespace functions retain runpy globals: modify those dictionaries directly.
S=load('support205.py'); R=load('ready205.py'); L=load('lifecycle205.py'); N=load('make_native205.py')
SG=S.need.__globals__; RG=R.configure.__globals__; LG=L.configure.__globals__; NG=N.configure.__globals__
def sset(name,value):setattr(S,name,value);SG[name]=value
for m in (R,N):m.configure(S)
L.configure(S,R,N)
sset('A',WORK);sset('D',WORK/SOURCE.name);S.D.mkdir();sset('ROOT',WORK/'views');S.ROOT.mkdir()
source_pins={name:S.pin((SOURCE/name).read_bytes()) for name in sorted(S.SOURCES)}
portable=(CASE/'publication_package_v2/verification/verify.py').read_bytes()
if S.pin(portable)!={'bytes':14419,'sha256':'7fbee76b89716091b84e2ec4f99f252d7cd1b0a47f517e4f605c806f762398bd'}:raise RuntimeError('Actual portable byte pin drift')

def put(path,raw):
    p=WORK/path;p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():p.chmod(0o644)
    p.write_bytes(raw);p.chmod(0o444)
    return S.pin(raw)
def jout(path,j):return put(path,S.enc(j))
for name in S.SOURCES:put(SOURCE.name+'/'+name,(SOURCE/name).read_bytes())
put('ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json',(CASE/'ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json').read_bytes())
custody=json.loads((CASE/'ORIGINAL_SUBMISSION_CUSTODY.json').read_bytes())
results=[]
def check(name,fn,reject=False):
    try:
        value=fn()
        results.append({'name':name,'expected':'reject' if reject else 'accept','observed':'accept','pass':not reject})
        return value
    except Exception as e:
        results.append({'name':name,'expected':'reject' if reject else 'accept','observed':'reject','exception':type(e).__name__,'message':str(e),'pass':reject})
def need(ok,msg='Independent predicate'):S.need(ok,msg)

package='publication_package_synthetic'
metadata={'title':'Synthetic operational fixture'}
for path,raw in {'odd_period_focal_pedal.tex':b'tex\n','odd_period_focal_pedal.pdf':b'pdf\n','bundle.zip':b'zip\n','PACKAGE_SEAL.json':b'{"synthetic":true}\n','verification/verify.py':portable}.items():put(package+'/'+path,raw)
upload={p:S.pin((WORK/package/p).read_bytes()) for p in ('odd_period_focal_pedal.tex','odd_period_focal_pedal.pdf','bundle.zip')}
jout(package+'/zenodo-deposit.json',{'metadata':metadata,'files':[{'path':p} for p in upload]})
safe={p.relative_to(WORK/package).as_posix():S.pin(p.read_bytes()) for p in (WORK/package).rglob('*') if p.is_file()}
math={'mathematical_clearance':True,'source_contract_clearance':True,'known_original_harness_defects':['synthetic historical defect'],'independent_family_limits':{}}
priority={'bounded_priority_audit_complete':True,'novelty_clearance':False,'positive_prior_implication':[],'remaining_exact_priority_gaps':[]}
sset('MATH_PIN',jout(S.MATH,math));sset('PRIORITY_PIN',jout(S.PRIORITY,priority))
for constant,name in (('PORTABLE_RECEIPT_PIN',S.PORTABLE_RECEIPT),('REPAIRS_PIN',S.REPAIRS)):
    sset(constant,jout(name,{'accepted':True,'PR':205,'evidence_scope':'ACTUAL_ROOT_RECEIPT'}))
events=[];accepts=[]
for i in (1,2):
    directory='review'+str(i);report='report.txt';report_pin=put(directory+'/'+report,b'Pure synthetic operational review\n')
    event={'directory':directory,'review_number':i,'whole_package_scope':True,'open_findings':0,'verdict':'CLEANPASS','safe_files':{report:report_pin},'report_file':report,'report_pin':report_pin,'reviewed_package':package,'reviewed_package_seal':safe['PACKAGE_SEAL.json']}
    acceptance={'schema':'pr205-root-whole-package-review-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','accepted':True,'PR':205,'original_head':S.HEAD,'review_accepted':True,'NEW_whole_package_reviews_completed':i,'review_event':copy.deepcopy(event),'review_cycle_repairs_required_now':False}
    accepts.append(acceptance);events.append(event)

def gate_fixture(gmut=None,amut=None):
    ev=copy.deepcopy(events);aa=copy.deepcopy(accepts)
    if amut:amut(aa)
    for i,a in enumerate(aa):
        path='ROOT_REVIEW_'+str(i+1)+'.json';ev[i].update(Root_acceptance_file=path,Root_acceptance_pin=jout(path,a))
    other={S.MATH:S.MATH_PIN,S.PRIORITY:S.PRIORITY_PIN,S.PORTABLE_RECEIPT:S.PORTABLE_RECEIPT_PIN,S.REPAIRS:S.REPAIRS_PIN}
    g={'schema':'pr205-root-publication-ready-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':205,'problem_id':5100030,'original_head':S.HEAD,'publication_ready_gate_accepted':True,'whole_package_review_loop_complete':True,'mathematical_clearance':True,'source_contract_clearance':True,'bounded_priority_audit_complete':True,'package':package,'package_safe_files':safe,'package_seal':safe['PACKAGE_SEAL.json'],'intended_upload_files':upload,'metadata':metadata,'whole_package_review_events':ev,'other_safe_files':other,'preparation_receipts':{role:S.pp(path,other[path]) for role,path in (('mathematics',S.MATH),('priority',S.PRIORITY),('portable',S.PORTABLE_RECEIPT),('repairs',S.REPAIRS))}}
    if gmut:gmut(g)
    gp=jout('ROOT_PUBLICATION_GATE_01.json',g)
    sp={SOURCE.name+'/'+n:source_pins[n] for n in S.SOURCES}
    adoption={'schema':'pr205-root-lifecycle-preparation-adoption-v1','accepted_preparation_only':True,'evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':205,'original_head':S.HEAD,'expected_publication_gate':S.pp('ROOT_PUBLICATION_GATE_01.json',gp),'sources':sp,'native_constructor':S.pp(SOURCE.name+'/make_native205.py',sp[SOURCE.name+'/make_native205.py']),'safe_artifacts':sp}
    ap=jout('ROOT_SOURCE_ADOPTION.json',adoption);S.configure_authority('ROOT_SOURCE_ADOPTION.json',ap);S._authority=SG['_authority']
    return gp,g

sset('_authority',None)
check('absent future Root adoption rejects runtime',S.runtime,True)
gp,g=gate_fixture()
check('exact canonical two-review gate accepts',lambda:S.gate(gp))
check('unadopted gate byte pin rejects',lambda:S.gate({'bytes':gp['bytes'],'sha256':'0'*64}),True)
gp,_=gate_fixture(lambda g:g['whole_package_review_events'].pop())
check('one accepted review rejects',lambda:S.gate(gp),True)
gp,_=gate_fixture(lambda g:g['whole_package_review_events'][1].update(directory='review1'))
check('duplicate review directory rejects',lambda:S.gate(gp),True)
gp,_=gate_fixture(amut=lambda aa:aa[1]['review_event'].pop('verdict'))
check('Root acceptance event missing verdict rejects exact-event contract',lambda:S.gate(gp),True)
gp,_=gate_fixture(amut=lambda aa:aa[1]['review_event'].pop('review_number'))
check('Root acceptance event missing review number rejects exact-event contract',lambda:S.gate(gp),True)
gp,_=gate_fixture(lambda g:g['whole_package_review_events'][1].update(unaccepted_extra_event_claim=True))
check('gate-added unaccepted event field rejects exact-event contract',lambda:S.gate(gp),True)
gp,_=gate_fixture(amut=lambda aa:aa[1].update(evidence_scope='PURE_SYNTHETIC_NOT_ROOT'))
check('nonactual Root review evidence rejects',lambda:S.gate(gp),True)
gp,_=gate_fixture(lambda g:g['whole_package_review_events'][-1].update(reviewed_package_seal={'bytes':1,'sha256':'0'*64}))
check('wrong final review seal rejects',lambda:S.gate(gp),True)
gp,g=gate_fixture()
source_copy=WORK/SOURCE.name/'ready205.py';source_copy.chmod(0o644);source_copy.write_bytes(b'# drift\n');source_copy.chmod(0o444)
check('adopted source drift rejects',S.authority,True)
put(SOURCE.name+'/ready205.py',(SOURCE/'ready205.py').read_bytes());gp,g=gate_fixture()

q,base,head=S.queue_rows();doi='10.5281/zenodo.999999999'
published=S.published_row(doi);foreign=b'| 224 | 999999 / X | synthetic | 0 | 0 | 0 | 2020 | queued | 0/5 |  |  |  |\n'
check('exact BASE121 merge row replaces only own line',lambda:need(S.replace_queue(foreign+base,doi)==foreign+published))
check('submitted HEAD371 cannot substitute for BASE121',lambda:S.replace_queue(foreign+head,doi),True)
check('duplicate own row rejects',lambda:S.replace_queue(base+base,doi),True)
check('published own row retains claimed_solved1/5',lambda:need(published.decode().split('|')[8:10]==[' claimed_solved ',' 1/5 ']))

real_body=S.body
def reconciliation(old,new,post=False,protected=False):
    sset('body',lambda h,path,commit:old if commit=='base' else new)
    m={S.Q:S.bpin(old)}
    if protected:m['unsolved_math_prioritization/attempts/999999/README.md']=S.bpin(b'protected')
    try:return S.reconcile(SimpleNamespace(byte_pin=S.bpin),None,{'commit':'base','selected_files':m},'main',doi if post else None)
    finally:sset('body',real_body)
check('pre95 BASE own queue unchanged accepts',lambda:reconciliation(foreign+base,foreign+base))
check('post95 published own queue unchanged accepts',lambda:reconciliation(foreign+published,foreign+published,True))
check('pre95 HEAD own queue rejects',lambda:reconciliation(foreign+head,foreign+head),True)
check('post95 BASE own queue rejects',lambda:reconciliation(foreign+base,foreign+base,True),True)
changedforeign=foreign.replace(b'queued',b'claimed_solved')
check('unprotected foreign queue change reconciles',lambda:reconciliation(foreign+base,changedforeign+base))
check('protected foreign queue change rejects',lambda:reconciliation(foreign+base,changedforeign+base,protected=True),True)
check('own queue mutation rejects',lambda:reconciliation(foreign+base,foreign+head),True)

old={n:('historical '+n+'\n').encode() for n in custody['files']};old['readiness.json']=S.enc({'historical':True});p={'doi':doi,'doi_url':'https://doi.org/'+doi,'id':999999999};t={'range':"'Math Puzzles'!A9:D9"};f={'UTC':'2026-10-16T00:00:00+00:00'}
native=N._render('published_pending_merge',f,old,portable,g,p,t,math,priority)
check('both native checker paths exact portable14419',lambda:need(all(S.pin(native[S.NATIVE+n])==S.PORTABLE for n in ('check_candidate.py','independent_review/independent_check.py'))))
check('native rendering leaves archived17 input bytes unchanged',lambda:need(all(old[n]==native[S.NATIVE+n] for n in set(old)-N.WRAPPERS)))
provenance=S.decode(native[S.NATIVE+'CURRENT_PROVENANCE.json'])
check('historical favorable/source freeze labels explicit',lambda:need(provenance['all_preserved_files_explicitly_historical'] is True and provenance['historical_PASS_counts_not_current_validation'] is True and len(provenance['historical_favorable_review_files'])==4))
freeze=S.decode(native[S.NATIVE+'FROZEN_MANIFEST.json'])
check('current FROZEN recomputes current body pins',lambda:need(all(x==S.bpin(native[S.NATIVE+n]) for n,x in freeze['files'].items()) and freeze['files']['check_candidate.py']==S.bpin(portable)))
check('optimized/old checker bytes rejected by native rendering',lambda:N._render('published_pending_merge',f,old,b'old checker',g,p,t,math,priority),True)

for phase in L.PHASE:
    parent='1'*40
    check(phase+' exact parent projection',lambda phase=phase:need(L.parents(phase,parent)==([parent,S.HEAD] if phase=='merge' else [parent])))
check('completion counts remain baseline without actual acceptance',lambda:need(L.counts('completion')==S.BASE_COUNTS))
check('completion counts advance only actual selector',lambda:need(L.counts('completion',True)==S.DONE_COUNTS))
check('factual98 actual counters stay baseline',lambda:need(L.counts('factual',True)==S.BASE_COUNTS))

b={'DOI':doi,'record_id':999999999,'tracker_range':t['range'],'publication_receipt_pin':S.pin(b'pub'),'tracker_receipt_pin':S.pin(b'tracker'),'actual_predecessor':{'directory':'synthetic/factual'}}
def projection(phase,mut=None):
    case={'PR':205,'original_head':S.HEAD,'case_percent':L.PHASE[phase][1],**S.BASE_COUNTS}
    progress={'current_PR':205,'current_PR_workflow_percent':L.PHASE[phase][1],**S.BASE_COUNTS,'fully_completed_eligible_PRs':list(range(1,48)),'published_PRs':list(range(1,32)),'dated_eligible_total':200,'last_completed_DOI':'prior204','last_published_DOI':'prior204'}
    if mut:mut(case,progress)
    return L.project(case,progress,'2026-10-16T00:00:00+00:00',phase,b,'synthetic')
check('factual98 projection incomplete47/31last204cursor205',lambda:need(all(projection('factual')[0][k]==v for k,v in S.BASE_COUNTS.items()) and projection('factual')[0]['completed'] is False))
check('completion100 postimage explicit conditional48/32last205cursor206',lambda:need(all(projection('completion')[0][k]==v for k,v in S.DONE_COUNTS.items()) and projection('completion')[0]['completion_postimage_effective_only_after_own_actual_MAIN_full_scope_acceptance'] is True))
check('completion rejects premature95 predecessor',lambda:projection('completion',lambda c,p:c.update(case_percent=95)),True)
check('completion rejects advanced counters preimage',lambda:projection('completion',lambda c,p:p.update(fully_completed_count=48)),True)
check('completion rejects duplicate completion-list entry',lambda:projection('completion',lambda c,p:p['fully_completed_eligible_PRs'].append(1)),True)

# The following "api" callable is a total in-memory dictionary projection. No
# network client, project backend, service or actual phase runner is imported.
def topology(phase,mutation=None):
    raw=b'selected';path=S.CASE+'selected_synthetic.md';ex={path:S.bpin(raw)};out={path:raw};parent='1'*40;commit='2'*40;pt='3'*40;tree='4'*40
    r={'PR':205,'phase':phase,'original_head':S.HEAD,'selected_files':ex,'selected_map_sha256':S.digest(ex),'commit':commit,'expected_main':parent,'tree':tree,'parent_tree':pt,'changed_paths':[path],'overlay_paths':[path]}
    co={'parents':[{'sha':z} for z in L.parents(phase,parent)],'tree':{'sha':tree},'message':L.message(phase,S.digest(ex))}
    store={'git/commits/'+commit:co,'git/commits/'+parent:{'tree':{'sha':pt}}};lookup={(tree,path):('100644','blob',ex[path]['git_blob'])};changes={path}
    if mutation:mutation(co,lookup,changes)
    h=SimpleNamespace(api=lambda endpoint:copy.deepcopy(store[endpoint]),lookup=lambda tr,p:lookup.get((tr,p)),changed_leaves=lambda a,b:set(changes),m=SimpleNamespace(native_tree_cache={},m=SimpleNamespace(h=SimpleNamespace(warm_selected_directories=lambda *args:None))))
    return L.verify(SimpleNamespace(selected_digest=S.digest),h,r,out,ex,phase)
for phase in L.PHASE:
    check(phase+' full selected/topology positive control',lambda phase=phase:topology(phase))
check('merge95 rejects single parent',lambda:topology('merge',lambda c,l,x:c['parents'].pop()),True)
check('factual98 rejects extra HEAD parent',lambda:topology('factual',lambda c,l,x:c['parents'].append({'sha':S.HEAD})),True)
check('completion100 rejects extra parent',lambda:topology('completion',lambda c,l,x:c['parents'].append({'sha':S.HEAD})),True)
check('missing selected body rejects',lambda:topology('merge',lambda c,l,x:l.clear()),True)
check('unselected foreign changed leaf rejects',lambda:topology('merge',lambda c,l,x:x.add('foreign/not_allowed.txt')),True)
check('wrong commit message rejects',lambda:topology('merge',lambda c,l,x:c.update(message='unbound')),True)

def selected_projection(mutation=None,phase='merge'):
    out=dict(native);base_map={S.CASE+'original_submitted_head/'+n:S.bpin(raw) for n,raw in old.items()};base_map[S.Q]=S.bpin(base if phase=='merge' else published)
    if mutation:mutation(out,base_map)
    return L.selected(SimpleNamespace(byte_pin=S.bpin),base_map,out,old,phase)
check('exact native25 and archive17 selected projection accepts',selected_projection)
check('preserved historical native mutation rejects',lambda:selected_projection(lambda o,b:o.update({S.NATIVE+'REVIEWED_RESULT.md':b'changed'})),True)
check('selected foreign overlay path rejects',lambda:selected_projection(lambda o,b:o.update({'foreign/not_allowed.txt':b'bad'})),True)
check('native checker mismatch rejects',lambda:selected_projection(lambda o,b:o.update({S.NATIVE+'independent_review/independent_check.py':b'old'})),True)
check('selected original archive mismatch rejects',lambda:selected_projection(lambda o,b:b.update({S.CASE+'original_submitted_head/README.md':S.bpin(b'wrong')})),True)
check('post95 queue rewrite rejects',lambda:selected_projection(lambda o,b:o.update({S.Q:base}),phase='factual'),True)

ctx={'gate_pin':gp,'ready_pointer_pin':S.pin(b'pointer'),'ready_acceptance_pin':S.pin(b'acceptance'),'checkpoint_commit':'5'*40,'package_seal':g['package_seal'],'package':package,'manifest_pin':safe['zenodo-deposit.json']}
pub={'actual_publication_verified':True,'metadata_exact_verified':True,'all_three_public_download_SHA256_verified':True,'PR':205,'state':'published','gate_sha256':gp['sha256'],'package':package,'context':ctx,'metadata_normalizations':[],'id':999999999,'doi':doi,'doi_url':'https://doi.org/'+doi,'record_url':'https://zenodo.org/records/999999999','doi_resolution':{'http_status':200,'status':'resolved'},'files':[{'name':n,'size':x['bytes'],'sha256':x['sha256']} for n,x in upload.items()],'verified_public_download_names':list(upload),'public_downloads':[{'name':n,'bytes':x['bytes'],'sha256':x['sha256'],'url':'https://example.invalid/'+n,'final_url':'https://example.invalid/'+n} for n,x in upload.items()]}
tracker={'actual_tracker_row_verified':True,'own_row_readback_verified':True,'foreign_rows_retained':True,'original_preappend_baseline_retained':True,'two_fresh_full_prechecks':True,'RAW_INSERT_ROWS':True,'B_intentionally_blank_no_verified_chat_share_URL':True,'PR':205,'doi':doi,'gate_sha256':gp['sha256'],'context':ctx,'row':S.tracker_row(g,doi),'spreadsheet_id':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','sheet_gid':1254632077,'range':t['range'],'original_preappend_baseline':{'file':'synthetic_baseline.json','pin':S.pin(b'baseline'),'row_count':8,'counter_sha256':'1'*64}}
real_context=S.actual_context
def operation_receipts(pm=None,tm=None):
    pp=copy.deepcopy(pub);tt=copy.deepcopy(tracker)
    if pm:pm(pp)
    pubpin=jout('ROOT_PUBLICATION_RECEIPT.json',pp);tt['publication_receipt']=pubpin
    if tm:tm(tt)
    jout('ROOT_TRACKER_RECEIPT.json',tt);sset('actual_context',lambda:(g,ctx))
    try:return S.operations()
    finally:sset('actual_context',real_context)
check('exact synthetic publication tracker context accepts',operation_receipts)
check('stale publication context rejects',lambda:operation_receipts(lambda p:p['context'].update(checkpoint_commit='0'*40)),True)
check('foreign publication PR rejects',lambda:operation_receipts(lambda p:p.update(PR=204)),True)
check('public download hash mismatch rejects',lambda:operation_receipts(lambda p:p['public_downloads'][0].update(sha256='0'*64)),True)
check('unverified DOI resolution rejects',lambda:operation_receipts(lambda p:p['doi_resolution'].update(http_status=404)),True)
check('tracker stale publication receipt pin rejects',lambda:operation_receipts(tm=lambda t:t['publication_receipt'].update(sha256='0'*64)),True)
check('tracker foreign sheet gid rejects',lambda:operation_receipts(tm=lambda t:t.update(sheet_gid=1)),True)
check('tracker nonmatching A/D row rejects',lambda:operation_receipts(tm=lambda t:t.update(range="'Math Puzzles'!A9:D10")),True)
check('tracker foreign row loss flag rejects',lambda:operation_receipts(tm=lambda t:t.update(foreign_rows_retained=False)),True)
check('tracker incomplete full prechecks flag rejects',lambda:operation_receipts(tm=lambda t:t.update(two_fresh_full_prechecks=False)),True)
check('tracker row content mismatch rejects',lambda:operation_receipts(tm=lambda t:t['row'].__setitem__(1,'unverified URL')),True)
operation_receipts()

ack={'schema':'pr205-root-pr-metadata-acknowledgement-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':205,'original_head':S.HEAD,'accepted':True,'original_native_custody_pin':S.CUSTODY,'expected_base_ref':'main','expected_title':'Synthetic acknowledged title','expected_body_pin':S.pin(b'Synthetic acknowledged body'),'actual_PR_readback_verified':True,'acknowledged_actual_PR_open_nondraft':True,'original_native_range_delta_unchanged':True}
def acknowledgement(mut=None):
    value=copy.deepcopy(ack)
    if mut:mut(value)
    path='ROOT_METADATA_ACK.json';return L.metadata_ack(S.pp(path,jout(path,value)))
check('actual Root PR metadata acknowledgement context accepts',acknowledgement)
check('synthetic metadata acknowledgement scope rejects',lambda:acknowledgement(lambda a:a.update(evidence_scope='SYNTHETIC')),True)
check('foreign metadata original HEAD rejects',lambda:acknowledgement(lambda a:a.update(original_head='0'*40)),True)
check('unread metadata acknowledgement rejects',lambda:acknowledgement(lambda a:a.update(actual_PR_readback_verified=False)),True)
check('changed original native range acknowledgement rejects',lambda:acknowledgement(lambda a:a.update(original_native_range_delta_unchanged=False)),True)

real_ops=S.operations;real_actual=S.actual
package_fact=S.pp(package+'/PACKAGE_SEAL.json',g['package_seal'])
publication_fact=S.pp('ROOT_PUBLICATION_RECEIPT.json',S.pin(S.read('ROOT_PUBLICATION_RECEIPT.json')))
tracker_fact=S.pp('ROOT_TRACKER_RECEIPT.json',S.pin(S.read('ROOT_TRACKER_RECEIPT.json')))
merge_a={'schema':'pr205-root-merge-receipt-v1',**S.BASE_COUNTS,'completed':False,'merged':True,'original_HEAD_safe':True,'full_scope_verified':True,'merge_commit':'6'*40,'checkpoint_commit':'6'*40,'publication_receipt_sha256':publication_fact['sha256'],'tracker_receipt_sha256':tracker_fact['sha256'],'package_seal':package_fact}
merge_path=SOURCE.name+'/synthetic_merge';merge_pin=jout(merge_path+'/ACCEPTANCE.json',merge_a)
factual_a={'schema':'pr205-root-factual-receipt-v1',**S.BASE_COUNTS,'completed':False,'actual_factual_accepted':True,'full_scope_MAIN_accepted':True,'case_percent':98,'completion_facts':{'case_completed':False,**S.BASE_COUNTS},'merge_receipt_sha256':merge_pin['sha256'],'publication_receipt_sha256':publication_fact['sha256'],'tracker_receipt_sha256':tracker_fact['sha256'],'package_seal':package_fact}
factual_path=SOURCE.name+'/synthetic_factual';factual_pin=jout(factual_path+'/ACCEPTANCE.json',factual_a)
facts={'schema':'pr205-native-facts-v1','original_head':S.HEAD,'UTC':'2026-10-16T00:00:00+00:00','package_seal':package_fact,'publication_ready_gate':S.pp('ROOT_PUBLICATION_GATE_01.json',gp),'publication_receipt':publication_fact,'tracker_receipt':tracker_fact,'merge_receipt':S.pp(merge_path+'/ACCEPTANCE.json',merge_pin),'factual_receipt':S.pp(factual_path+'/ACCEPTANCE.json',factual_pin)}
def native_validation(fmut=None,amut=None):
    ff=copy.deepcopy(facts);mm=copy.deepcopy(merge_a);aa=copy.deepcopy(factual_a)
    if fmut:fmut(ff)
    if amut:amut(mm,aa)
    sset('operations',lambda:(g,p,t,ctx));sset('actual',lambda kind:(merge_path,mm,{}, {}) if kind=='merge' else (factual_path,aa,{},{}))
    try:return N.validate_facts('factual_checkpoint_accepted',ff)
    finally:sset('operations',real_ops);sset('actual',real_actual)
check('native factual98 exact actual predecessor facts accept',native_validation)
check('native factual98 completed true rejects',lambda:native_validation(amut=lambda m,a:a.update(completed=True)),True)
check('native factual98 premature48 completed rejects',lambda:native_validation(amut=lambda m,a:a.update(fully_completed_count=48)),True)
check('native factual98 advanced cursor206 rejects',lambda:native_validation(amut=lambda m,a:a.update(next_numeric_intake_cursor=206)),True)
check('native factual98 stale merge receipt digest rejects',lambda:native_validation(amut=lambda m,a:a.update(merge_receipt_sha256='0'*64)),True)
check('native predecessor stale publication context rejects',lambda:native_validation(amut=lambda m,a:a.update(publication_receipt_sha256='0'*64)),True)
check('native facts foreign tracker pin rejects',lambda:native_validation(fmut=lambda f:f['tracker_receipt'].update(sha256='0'*64)),True)

# Exercise all-five local CAS against files exclusively below WORK/views.
real_body=S.body
def local_five(mut=None,do_sync=False):
    before={path:('before '+path).encode() for path in S.VIEWS};after={path:('after '+path).encode() for path in S.VIEWS}
    for path,raw in before.items():
        file=S.ROOT/path;file.parent.mkdir(parents=True,exist_ok=True)
        if file.is_symlink():file.unlink()
        if file.exists():file.chmod(0o644)
        file.write_bytes(raw);file.chmod(0o444)
    if mut:mut(before,after)
    sset('body',lambda h,path,commit:after[path] if commit=='post' else before[path])
    r={'commit':'post','selected_files':{path:S.bpin(raw) for path,raw in after.items()},'local_five_expected_preimages':{path:S.pin(raw) for path,raw in before.items()}}
    try:
        result=S.sync_views(None,r) if do_sync else S.local_preimages(None,'pre')
        if do_sync:need(len(result)==5 and all((S.ROOT/path).read_bytes()==after[path] and (S.ROOT/path).stat().st_mode&0o777==0o444 for path in S.VIEWS))
        return result
    finally:sset('body',real_body)
def mutate_local(before,after):
    file=S.ROOT/S.VIEWS[-1];file.chmod(0o644);file.write_bytes(b'foreign concurrent edit');file.chmod(0o444)
check('all-five fresh local parent preimages accept',local_five)
check('all-five sync writes exact readonly synthetic postimages',lambda:local_five(do_sync=True))
check('foreign local preimage rejects read preflight',lambda:local_five(mutate_local),True)
check('foreign fifth local preimage rejects sync before writes',lambda:local_five(mutate_local,True),True)
check('foreign fifth preimage failure preserves earlier four local files',lambda:need(all((S.ROOT/path).read_bytes()==('before '+path).encode() for path in S.VIEWS[:-1])))

# Fixed actual custody10 receipts are read as opaque operational evidence only.
for filename in ('ACCEPTANCE.json','ACCEPTANCE_CURRENT_SELECTED_MAP.json'):
    put(S.INTAKE+'/'+filename,(CASE/S.INTAKE/filename).read_bytes())
check('fixed actual custody10 baseline4124 with47/31last204cursor205 accepts',S.baseline_intake)

def adoption_mutation(mut):
    gp,_=gate_fixture();ad=S.obj('ROOT_SOURCE_ADOPTION.json');mut(ad);ap=jout('ROOT_SOURCE_ADOPTION.json',ad);return S.configure_authority('ROOT_SOURCE_ADOPTION.json',ap)
check('unaccepted source adoption rejects',lambda:adoption_mutation(lambda a:a.update(accepted_preparation_only=False)),True)
check('nonactual source adoption rejects',lambda:adoption_mutation(lambda a:a.update(evidence_scope='SYNTHETIC')),True)
check('foreign source adoption HEAD rejects',lambda:adoption_mutation(lambda a:a.update(original_head='0'*40)),True)
check('source adoption missing constructor rejects',lambda:adoption_mutation(lambda a:a['sources'].pop(SOURCE.name+'/make_native205.py')),True)
check('source adoption foreign gate path rejects',lambda:adoption_mutation(lambda a:a['expected_publication_gate'].update(path='foreign_gate.json')),True)
gp,g=gate_fixture()

def completion_inputs(mut=None):
    directory=SOURCE.name+'/synthetic_factual';a={'package':package,'package_seal':package_fact,**S.BASE_COUNTS,'case_percent':98,'actual_merge_accepted':True,'actual_publication_verified':True,'actual_tracker_row_verified':True,'actual_factual_accepted':True,'completed':False,'completion_facts':{'case_completed':False,**S.BASE_COUNTS}}
    x={'selected_files':{S.CASE+'original_submitted_head/'+n:S.bpin(raw) for n,raw in old.items()}}
    x['selected_files'][S.CASE+'ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json']=S.bpin(S.read('ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json',S.QRECEIPT))
    if mut:mut(a)
    jout(directory+'/ACCEPTANCE.json',a);jout(S.POINTER['factual'],{'synthetic_pointer_only':True})
    ap=jout('ROOT_METADATA_ACK.json',ack);real_originals=S.originals
    sset('operations',lambda:(g,p,t,ctx));sset('actual',lambda kind:(directory,a,{},x));sset('originals',lambda:(custody,old))
    try:return L.inputs('completion',S.pp('ROOT_METADATA_ACK.json',ap))
    finally:sset('operations',real_ops);sset('actual',real_actual);sset('originals',real_originals)
check('completion binding requires actual incomplete98 positive',completion_inputs)
check('completion binding rejects already completed98',lambda:completion_inputs(lambda a:a.update(completed=True)),True)
check('completion binding rejects accepted phase95 as98',lambda:completion_inputs(lambda a:a.update(case_percent=95)),True)
check('completion binding rejects nonaccepted factual98',lambda:completion_inputs(lambda a:a.update(actual_factual_accepted=False)),True)
check('completion binding rejects prematurely advanced lastPR205',lambda:completion_inputs(lambda a:a.update(last_completed_PR=205)),True)
check('completion binding rejects prematurely advanced published32',lambda:completion_inputs(lambda a:a.update(published_count=32)),True)
check('completion binding rejects false completion_facts98',lambda:completion_inputs(lambda a:a['completion_facts'].update(case_completed=True)),True)

summary={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'PURE_SYNTHETIC_OPERATIONAL_NO_ACTUAL_PHASE','candidate_source_pins_at_run':source_pins,'candidate_source_pins_after_run':{n:S.pin((SOURCE/n).read_bytes()) for n in sorted(S.SOURCES)},'portable_pin':S.pin(portable),'work_directory':str(WORK),'controls':results,'passed':sum(z['pass'] for z in results),'failed':sum(not z['pass'] for z in results),'source_stable_during_run':all(source_pins[n]==S.pin((SOURCE/n).read_bytes()) for n in S.SOURCES)}
result_file=HERE/'controls_results.json'
if result_file.exists():result_file.chmod(0o644)
result_file.write_text(json.dumps(summary,indent=2)+'\n');result_file.chmod(0o444)
print(json.dumps({'passed':summary['passed'],'failed':summary['failed'],'source_stable_during_run':summary['source_stable_during_run'],'unexpected':[z for z in results if not z['pass']]},indent=2))
