"""Offline lifecycle guards. No real runtime/API/native02/service invocation."""
import sys
if sys.flags.optimize or not sys.dont_write_bytecode:raise RuntimeError('Ordinary Python -B required')
from pathlib import Path
import ast,copy,datetime,hashlib,importlib.util,json,subprocess,types
from unittest.mock import patch
D=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('offline_pr204_lifecycle',D/'finish204.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
passed=[]
def ok(name,value):m.need(value,name);passed.append(name)
def reject(name,fn):
    try:fn()
    except (RuntimeError,KeyError,TypeError,ValueError):passed.append(name);return
    raise RuntimeError('Negative control unexpectedly passed '+name)
def actual_fixture(which):
    return ('publication_lifecycle_02/SYNTHETIC_'+which,{'checkpoint_commit':'a'*40},{},{})
seal={'bytes':3,'sha256':'b'*64};small={'bytes':9,'sha256':'c'*64}
b={'package':'publication_package_SYNTHETIC_ONLY','package_seal':seal,'package_seal_file':'FINAL_SEAL.json','Root_publication_gate_pin':small,'publication_receipt_pin':small,'tracker_receipt_pin':small,'whole_package_reviews_completed':3,'whole_package_review_events':[{'SYNTHETIC_EVENT':i} for i in range(3)],'DOI':'10.5281/zenodo.999999999','record_id':999999999,'tracker_range':"'Math Puzzles'!A999:D999"}

for phase in m.PHASE:
    ok(phase+' exact parent list',m.parents(phase,'d'*40)==(['d'*40,m.HEAD] if phase=='merge' else ['d'*40]))
    ok(phase+' no unaccepted completion',m.counts(phase)==m.BASE_COUNTS)
    with patch.object(m,'actual',side_effect=actual_fixture),patch.object(m,'frozen',return_value=b'synthetic receipt'):
        f=m.native_facts(phase,'2026-10-16T15:00:00Z',b);a=m.accepted_aliases(phase,b,'d'*40,'2026-10-16T15:00:00Z')
    expected={'publication_receipt','tracker_receipt'}|({'merge_receipt'} if phase!='merge' else set())|({'factual_receipt'} if phase=='completion' else set())
    ok(phase+' exact native receipt stage',set(k for k in f if k.endswith('_receipt'))==expected)
    ok(phase+' custom seal filename retained',f['package_seal']=={'path':b['package']+'/FINAL_SEAL.json',**seal} and a['package_seal']==f['package_seal'])
    if phase=='factual':ok('Factual98 authentic incomplete aliases',a['actual_factual_accepted'] is True and a['full_scope_MAIN_accepted'] is True and a['completed'] is False and a['completion_facts']=={'case_completed':False,**m.BASE_COUNTS} and a['merge_receipt_sha256']==m.pin(b'synthetic receipt')['sha256'])
reject('Unknown phase',lambda:m.parents('unknown','d'*40));reject('Malformed parent',lambda:m.parents('merge','bad'))

qraw=(m.A/m.QUEUE_RECEIPT).read_bytes();qreceipt,row,submitted=m.queue_rows();old=b'foreign prefix\r\n'+row+b'foreign suffix\n';new=m.queue(old,b['DOI']);cells=new.splitlines()[1].decode().split('|')
ok('Exact1833-byte original QUEUE receipt authenticated',m.pin(qraw)==m.QUEUE_RECEIPT_PIN)
ok('Actual BASE queued0/5 becomes submitted HEAD claimed_solved1/5',row==qreceipt['base_own_row']['text'].encode() and submitted==qreceipt['original_QUEUE_row']['text'].encode() and cells[:10]==submitted.decode().rstrip('\n').split('|')[:10] and row.decode().split('|')[8:10]==[' queued ',' 0/5 '])
ok('Original own claimed_solved1/5 retained',cells[8].strip()=='claimed_solved' and cells[9].strip()=='1/5')
ok('Foreign QUEUE bytes retained exactly',new.splitlines(keepends=True)[0]==old.splitlines(keepends=True)[0] and new.splitlines(keepends=True)[-1]==old.splitlines(keepends=True)[-1])
ok('Strict centered product-positive scope',b'signed shoelace areas in both orientations' in new and b'their product is strictly positive' in new and b'zero/negative' not in new and b'23085904' in new and b'23400541' in new)
reject('Own BASE QUEUE effort drift',lambda:m.queue(old.replace(b'0/5',b'1/5'),b['DOI']));reject('Duplicate own row',lambda:m.queue(old+row,b['DOI']));reject('Credited prior DOI reused',lambda:m.queue(old,'10.5281/zenodo.23085904'))
reject('Submitted HEAD is not premerge MAIN preimage',lambda:m.queue(b'foreign prefix\r\n'+submitted+b'foreign suffix\n',b['DOI']))
reject('Arbitrary claimed_solved row is not premerge preimage',lambda:m.queue(old.replace(b' queued | 0/5 ',b' claimed_solved | 1/5 '),b['DOI']))
reject('BASE eligibility drift refused',lambda:m.queue(old.replace(b'0.1905',b'0.1906'),b['DOI']))
with patch.object(m,'frozen',return_value=qraw+b' '):reject('Original row receipt byte drift refused',lambda:m.queue(old,b['DOI']))
for prefix,suffix in ((b'foreign\n',b'tail without newline'),(b'foreign\r\n',b'tail\r\n\r\n')):
    before=prefix+row+suffix;after=m.queue(before,b['DOI']);m.need(after.splitlines(keepends=True)[0]==before.splitlines(keepends=True)[0] and after.splitlines(keepends=True)[2:]==before.splitlines(keepends=True)[2:],'Foreign edge line endings')
ok('Foreign final-newline and CRLF variants preserved',True)
diag=json.loads((D/'merge95_01/ROOT_QUEUE_PREIMAGE_DIAGNOSTIC.json').read_bytes());ready=m.actual('ready')
ok('Failed observation and actual ready map authenticate BASE receipt',diag['current_matches_original_base'] is True and diag['current_own_row']['text'].encode()==row and ready[3]['selected_files'][m.CASE+m.QUEUE_RECEIPT]==m.bpin(qraw) and ready[3]['selected_files'][m.Q]==diag['current_QUEUE'])

# Authenticate real archive bytes only; all publication/integration data are fixtures.
custody,original=m.originals();ok('Actual20 archive59343 bytes and native blob pins',len(original)==20 and sum(len(x) for x in original.values())==59343)
class C:
    byte_pin=staticmethod(m.bpin)
    selected_digest=staticmethod(m.digest_selected)
base={m.CASE+'original_submitted_head/'+n:m.bpin(x) for n,x in original.items()};base['foreign/untouched']=m.bpin(b'foreign');base[m.Q]=m.bpin(new)
out={m.NATIVE+n:(b'new qualified wrapper' if n in m.WRAPPERS else raw) for n,raw in original.items()};out.update({m.NATIVE+n:b'new current index' for n in m.ADDED})
chosen=m.selected(C(),base,out,original,'merge');ok('Native27/archive20/foreign selected identities retained',len(out)==27 and all(chosen[k]==x for k,x in base.items()))
bad=dict(out);bad[m.NATIVE+'PROOF.md']=b'changed';reject('Native scientific rewrite',lambda:m.selected(C(),base,bad,original,'merge'))
bad=dict(out);bad['foreign/untouched']=b'changed';reject('Foreign overlay path',lambda:m.selected(C(),base,bad,original,'merge'))
bad=dict(out);bad[m.NATIVE+'undeclared']=b'changed';reject('Undeclared native file',lambda:m.selected(C(),base,bad,original,'merge'))
bad=dict(out);bad[m.Q]=new+b'changed';reject('Postmerge QUEUE rewrite',lambda:m.selected(C(),base,bad,original,'factual'))
for phase in ('factual','completion'):
    m.selected(C(),base,{**out,m.Q:new},original,phase)
    reject(phase+' refuses rollback to original BASE after accepted merge',lambda:m.selected(C(),base,{**out,m.Q:old},original,phase))
ok('Later phases preserve their accepted published row without BASE requirement',True)

for phase in m.PHASE:
    case={'PR':204,'original_head':m.HEAD,'case_percent':m.PHASE[phase][1],'original_effort':'Original1/5 unverified actual effort','scope_sentinel':'Retain qualified source/family limits','priority_clearance':True}
    p={'current_PR':204,'current_PR_workflow_percent':m.PHASE[phase][1],**m.BASE_COUNTS,'last_completed_DOI':'PR203_ORIGINAL_SENTINEL','last_completed_PR':203,'last_published_PR':203,'current_scope_sentinel':'Retain qualified source/family limits','fully_completed_eligible_PRs':list(range(45))+[203],'published_PRs':list(range(29))+[203],'dated_eligible_total':99}
    before=m.enc([case,p])
    with patch.object(m,'actual',side_effect=actual_fixture),patch.object(m,'frozen',return_value=b'synthetic actual factual receipt'):
        x,y,note=m.project(case,p,'2026-10-16T15:00:00Z',phase,b,'SYNTHETIC_ONLY')
    ok(phase+' projection preserves input and source limits',m.enc([case,p])==before and x['scope_sentinel']==case['scope_sentinel'] and y['current_scope_sentinel']==p['current_scope_sentinel'])
    ok(phase+' event count derived3 and noveltyfalse',x['NEW_whole_package_reviews_completed']==3 and y['current_NEW_whole_publication_package_reviews_completed']==3 and x['priority_novelty_clearance'] is False and y['current_priority_novelty_clearance'] is False)
    expected=m.DONE_COUNTS if phase=='completion' else m.BASE_COUNTS
    ok(phase+' conditional postimage counters correct',all(x[k]==value for k,value in expected.items()) and all(y[k]==value for k,value in expected.items() if k!='goal_complete') and x['completion_postimage_effective_only_after_own_actual_MAIN_full_scope_acceptance'] is True and y['current_completion_postimage_effective_only_after_own_actual_MAIN_full_scope_acceptance'] is True)
    if phase=='completion':ok('Actual203 completion provenance retired before replacing counters',y['historical_prior_completion_metadata'][-1]['values']['last_completed_PR']==203 and y['historical_prior_completion_metadata'][-1]['values']['last_completed_DOI']=='PR203_ORIGINAL_SENTINEL' and len(y['fully_completed_eligible_PRs'])==47 and len(y['published_PRs'])==31)

ack={'schema':'pr204-root-pr-metadata-acknowledgement-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':204,'original_head':m.HEAD,'accepted':True,'actual_PR_readback_verified':True,'acknowledged_actual_PR_open_nondraft':True,'original_native_range_delta_unchanged':True,'original_native_custody_pin':m.CUSTODY_PIN,'expected_base_ref':'main','expected_title':'Root acknowledged title','expected_body_pin':m.pin(b'Root acknowledged body')}
rp=m.pp('SYNTHETIC_ACK.json',small)
with patch.object(m,'frozen',return_value=m.enc(ack)):
    ok('Actual metadata acknowledgement schema accepted only as pinned input',m.metadata_ack(rp)==ack)
    bad=copy.deepcopy(ack);bad['actual_PR_readback_verified']=False
    with patch.object(m,'frozen',return_value=m.enc(bad)):reject('Missing actual metadata readback',lambda:m.metadata_ack(rp))
wrong_pr={'head':{'sha':'e'*40},'base':{'ref':'main'},'title':ack['expected_title'],'body':'Root acknowledged body'}
with patch.object(m,'metadata_ack',return_value=ack),patch.object(m,'originals',side_effect=RuntimeError('must not reach custody on wrong HEAD')):
    h=types.SimpleNamespace(api=lambda endpoint:wrong_pr);reject('Original PR HEAD rewrite before custody/API work',lambda:m.original(h,'merge',{'PR_metadata_acknowledgement':rp}))

with patch.object(m,'binding',side_effect=RuntimeError('missing future actual binding')),patch.object(m.v,'load',side_effect=RuntimeError('real runtime forbidden')) as loader:
    reject('Missing future binding fails before API runtime',lambda:m.run('merge','prepare','SYNTHETIC_MISSING'));ok('No actual runtime loader invoked',loader.call_count==0)
adoption={'accepted':True,'evidence_scope':'ACTUAL_ROOT_RECEIPT','original_head':m.HEAD,'constructor':{'path':'native_publication_preparation_01/make_native.py',**small}}
with patch.object(m,'frozen',return_value=m.enc(adoption)):reject('Unadopted/native01 source refused',lambda:m.native_adoption(rp))

context={'gate_pin':small,'gate':{'metadata':{'title':'SYNTHETIC ONLY'}}};pub={'doi':b['DOI']};cp={'SYNTHETIC_CONTEXT':True}
t={'PR':204,'doi':pub['doi'],'gate_sha256':small['sha256'],'publication_receipt':small,'context':cp,'spreadsheet_id':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','sheet_gid':1254632077,'range':"'Math Puzzles'!A999:D999",'row':m.tracker_row(context['gate'],pub['doi']),'original_preappend_baseline':{'file':'SYNTHETIC.json','pin':small,'row_count':1,'counter_sha256':'f'*64}}
for k in ('actual_tracker_row_verified','own_row_readback_verified','foreign_rows_retained','original_preappend_baseline_retained','two_fresh_full_prechecks','RAW_INSERT_ROWS','B_intentionally_blank_no_verified_chat_share_URL'):t[k]=True
with patch.object(m.ops,'context_pin',return_value=cp):
    with patch.object(m,'frozen',return_value=m.enc(t)):ok('Authentic operation uses exact DOI URL four-cell row',m.tracker(context,pub,small)[1]==t)
    bad=copy.deepcopy(t);bad['row'][2]=pub['doi']
    with patch.object(m,'frozen',return_value=m.enc(bad)):reject('Bare DOI in tracker C refused',lambda:m.tracker(context,pub,small))
    bad=copy.deepcopy(t);bad['foreign_rows_retained']=False
    with patch.object(m,'frozen',return_value=m.enc(bad)):reject('Missing foreign tracker retention refused',lambda:m.tracker(context,pub,small))

# Full native-object verification uses a complete fake API/tree, never the network.
ex={'own/path':m.bpin(b'new')};r={'phase':'merge','original_head':m.HEAD,'selected_files':ex,'selected_map_sha256':m.digest_selected(ex),'commit':'1'*40,'expected_main':'2'*40,'tree':'3'*40,'parent_tree':'4'*40,'changed_paths':['own/path'],'overlay_paths':['own/path']};payload={'own/path':b'new'}
class H:
    def __init__(self):self.foreign=False;self.wrong_parent=False;self.wrong_blob=False;self.m=types.SimpleNamespace(m=types.SimpleNamespace(h=types.SimpleNamespace(warm_selected_directories=lambda *a:None)))
    def api(self,endpoint):
        if endpoint=='git/commits/'+r['commit']:return {'parents':[{'sha':'9'*40 if self.wrong_parent else r['expected_main']},{'sha':m.HEAD}],'tree':{'sha':r['tree']},'message':m.message('merge',r['selected_map_sha256'])}
        if endpoint=='git/commits/'+r['expected_main']:return {'tree':{'sha':r['parent_tree']}}
        raise RuntimeError('Unexpected fake endpoint '+endpoint)
    def lookup(self,tree,path):return ('100644','blob','f'*40 if self.wrong_blob else ex[path]['git_blob']) if tree==r['tree'] else None
    def changed_leaves(self,*a):return {'own/path','foreign/hidden'} if self.foreign else {'own/path'}
h=H()
with patch.object(m.v,'validate_caches',return_value=None):
    m.verify(C(),h,r,payload,ex,'merge');ok('Full selected/trueparent/change-set positive fixture',True)
    h.foreign=True;reject('Unselected foreign changed leaf refused',lambda:m.verify(C(),h,r,payload,ex,'merge'));h.foreign=False;h.wrong_parent=True;reject('Wrong ordered native parent refused',lambda:m.verify(C(),h,r,payload,ex,'merge'));h.wrong_parent=False;h.wrong_blob=True;reject('Every-selected blob mismatch refused',lambda:m.verify(C(),h,r,payload,ex,'merge'))

source=(D/'finish204.py').read_text();tree=ast.parse(source);run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='run');calls=[(n.lineno,ast.unparse(n.func)) for n in ast.walk(run) if isinstance(n,ast.Call)]
ok('Binding precedes native runtime source order',min(n for n,f in calls if f=='binding')<min(n for n,f in calls if f=='v.load'))
inputs_node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='inputs');ok('Input queue receipt authentication precedes ready/native/ops work',min((n.lineno,n.col_offset) for n in ast.walk(inputs_node) if isinstance(n,ast.Call) and ast.unparse(n.func)=='queue_rows')<min((n.lineno,n.col_offset) for n in ast.walk(inputs_node) if isinstance(n,ast.Call) and ast.unparse(n.func)=='native_adoption'))
overlay_node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='overlay');merge_blocks=[n for n in ast.walk(overlay_node) if isinstance(n,ast.If) and ast.unparse(n.test)=="phase == 'merge'"]
ok('BASE-to-HEAD queue projection is restricted to merge phase',len(merge_blocks)==1 and any(isinstance(n,ast.Call) and ast.unparse(n.func)=='queue' for n in ast.walk(merge_blocks[0])) and sum(isinstance(n,ast.Call) and ast.unparse(n.func)=='queue' for n in ast.walk(overlay_node))==1)
ok('Old unchanged_draft guard absent','unchanged_pr(' not in source)
posts=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='api' and len(n.args)>1 and isinstance(n.args[1],ast.Constant) and n.args[1].value!='GET']
ok('Only unreferenced trees/commits POSTs exist',len(posts)==2 and {ast.literal_eval(n.args[0]) for n in posts}=={'git/trees','git/commits'})
command=[sys.executable,'-O','-B','-c','exec('+repr(source)+',{"__file__":'+repr(str(D/'finish204.py'))+',"__name__":"offline_optimized_guard"})'];p=subprocess.run(command,capture_output=True)
ok('Optimized interpreter fails before source loading',p.returncode!=0 and b'Ordinary Python -B required' in p.stderr)
report={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'OFFLINE_OPERATIONAL_GUARDS_ONLY','controls_passed':len(passed),'controls':passed,'real_API_or_runtime_or_native02_or_services_invoked':False,'actual_ready_publication_tracker_merge_or_completion_contributed':False,'science_or_whole_package_review_events_contributed':0,'source_pins':{n:m.pin((D/n).read_bytes()) for n in ['finish204.py','offline_guard_tests.py']},'retained_input_pins':{'ready02_helper':m.READY_PIN,'operations02_common':m.OPS_PIN,'operations02_tracker_source':m.TRACKER_SOURCE_PIN,'Root_ready02_preparation':m.READY_ADOPTION_PIN,'original_custody':m.CUSTODY_PIN,'original_QUEUE_row_receipt':m.QUEUE_RECEIPT_PIN}}
print(json.dumps(report,indent=2))
