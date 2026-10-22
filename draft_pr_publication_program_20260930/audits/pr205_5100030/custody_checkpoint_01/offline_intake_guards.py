"""Offline AST-extracted custody guards; no API, helper phase, cache or writes.
Run ordinary and optimized Python -B. Production helpers reject optimization.
"""
from pathlib import Path
import ast,copy,hashlib,json,subprocess,sys,types
D=Path(__file__).resolve().parent;A=D.parent;source=D/'checkpoint_intake205.py';tree=ast.parse(source.read_bytes());results=[]
def need(ok,label):
    if not ok:raise RuntimeError(label)
def check(label,call):call();results.append(label)
def rejects(label,call):
    try:call()
    except (RuntimeError,ValueError,KeyError,UnicodeDecodeError):results.append(label);return
    raise RuntimeError('Unexpected acceptance: '+label)
names={'need','now','pin','bpin','enc','read','safe','frozen','baseline','inputs','reconcile','project','overlay','unchanged_pr'}
nodes=[x for x in tree.body if isinstance(x,(ast.Import,ast.ImportFrom)) or isinstance(x,ast.FunctionDef) and x.name in names or isinstance(x,ast.Assign) and all(isinstance(t,ast.Name) and t.id.isupper() for t in x.targets)]
e={'__file__':str(source)};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),e)
pin=e['pin'];bpin=e['bpin'];q=json.loads((A/'ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json').read_bytes());custody=json.loads((A/'ORIGINAL_SUBMISSION_CUSTODY.json').read_bytes());base=q['base_own_row']['text'].encode();head=q['original_QUEUE_row']['text'].encode()
check('actual BASE121 queued0/5 distinct from HEAD371 claimed_solved1/5',lambda:need(len(base)==121 and len(head)==371 and pin(base)==e['BASE_ROW_PIN'] and base!=head,'Actual rows'))
check('actual204 completion3062/map1229790/4084 identities and47/31 counters',lambda:need(len(e['baseline']()['selected_files'])==4084,'Baseline'))
protected=[A.parent/'pr204_5100012/publication_lifecycle_02/finish204.py',e['P']/'CURRENT_PROGRESS.json',e['P']/'CURRENT_PROGRESS.md',e['P']/'RESEARCH_LOG.md',A.parent/'pr204_5100012/CURRENT_CASE_STATUS.json',A.parent/'pr204_5100012/RESEARCH_LOG.md']
before={str(p):(pin(p.read_bytes()),p.stat().st_mtime_ns,p.stat().st_mode) for p in protected}
p=json.loads((e['P']/'CURRENT_PROGRESS.json').read_bytes());old=copy.deepcopy(p);case,program=e['project'](p,'2026-10-16T00:00:00+00:00')
check('project leaves original204 object unchanged',lambda:need(p==old,'Input mutation'))
check('all204 current aliases retained solely in historical snapshot',lambda:need(all(program['historical_current_case_snapshots'][-1]['values'][k]==v for k,v in p.items() if k.lower().startswith(('current_','next_','conditional_','program_snapshot_'))),'Historical retirement'))
check('205 current gates false and original1/5 retained',lambda:need(case['case_percent']==10 and case['original_QUEUE_effort_cell']=='1/5' and program['current_PR']==205 and all(program[k] is False for k in ('current_mathematical_clearance','current_source_contract_clearance','current_priority_clearance','current_theorem_accepted','current_publication_ready','current_Zenodo_published','current_tracker_updated','current_original_PR_actual_merged','current_completed')),'205 clearance'))
check('205 no previous DOI, package or acceptance aliases leak',lambda:need(program['current_DOI'] is None and program['current_record_id'] is None and program['current_new_publication_ledger']==[] and 'current_publication_gate' not in program and 'current_mathematical_gate' not in program and 'current_whole_package_review_events' not in program,'Stale authority'))
check('47completed31published,last204,cursor205 advancefalse retained',lambda:need((program['fully_completed_count'],program['published_count'],program['last_completed_PR'],program['next_numeric_intake_cursor'],program['advance_to_next_PR_authorized_now'])==(47,31,204,205,False) and program['fully_completed_eligible_PRs']==p['fully_completed_eligible_PRs'] and program['published_PRs']==p['published_PRs'],'Counters'))
check('no206 intake and zero custody mathematical acceptance',lambda:need(program['next_status_only_intake_performed'] is False and case['mathematical_family_output_acceptance_contributed_by_custody']==0 and program['next_intake_requires_actual_completed_PR']==205,'No206'))
for key,value in [('current_PR',203),('current_PR_workflow_percent',90),('fully_completed_count',46),('published_count',30),('last_completed_PR',203)]:
    damaged=copy.deepcopy(p);damaged[key]=value;rejects('reject incorrect prior completion '+key,lambda x=damaged:e['project'](x,'stamp'))
c=types.SimpleNamespace(byte_pin=bpin);oldq=b'header\n'+base+b'| 1 | 9999999 / FOREIGN | title | a | b | c | d | queued | 0/5 |  |  |  |\n'
foreign=oldq.replace(b'| title |',b'| changed title |');b={'commit':'a'*40,'selected_files':{e['Q']:bpin(oldq),'unsolved_math_prioritization/attempts/5100012/README.md':{}}};bodies={'a'*40:oldq,'b'*40:foreign};e['v']=types.SimpleNamespace(native_body=lambda h,path,commit:bodies[commit])
selected,ack=e['reconcile'](c,None,b,'b'*40)
check('exact BASE survives allowed unprotected foreign QUEUE change',lambda:need(selected[e['Q']]==bpin(foreign) and len(ack['foreign_changed_rows'])==1 and ack['own_checkpoint_writes_no_QUEUE_bytes'] is True,'Reconcile'))
for label,bad in [('HEAD371 preimage',oldq.replace(base,head)),('claimed_solved arbitrary own row',oldq.replace(b'| queued | 0/5 |',b'| claimed_solved | 2/5 |',1)),('missing own row',oldq.replace(base,b'')),('duplicate own row',oldq+base),('own newline change',oldq.replace(base,base.rstrip(b'\n'))),('foreign row ID change',foreign.replace(b'9999999 / FOREIGN',b'8888888 / FOREIGN')),('protected foreign change',oldq.replace(b'9999999 / FOREIGN',b'5100012 / FOREIGN').replace(b'| title |',b'| changed |'))]:
    bodies['b'*40]=bad;rejects('reject '+label,lambda:e['reconcile'](c,None,b,'b'*40))
protectedq=oldq.replace(b'9999999 / FOREIGN',b'5100012 / FOREIGN');bodies['a'*40]=protectedq;bodies['b'*40]=protectedq.replace(b'| title |',b'| changed |');pb=copy.deepcopy(b);pb['selected_files'][e['Q']]=bpin(protectedq)
rejects('reject protected selected native QUEUE row change',lambda:e['reconcile'](c,None,pb,'b'*40))
bodies['a'*40]=oldq;bodies['b'*40]=oldq;damaged=copy.deepcopy(b);damaged['selected_files'][e['Q']]=bpin(b'drift');rejects('reject prior accepted QUEUE pin drift',lambda:e['reconcile'](c,None,damaged,'b'*40))
materials={n:(A/n).read_bytes() for n in ['ROOT_ORIGINAL_STATUS_ONLY_INTAKE_01.json','ORIGINAL_SUBMISSION_CUSTODY.json','ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json','ORIGINAL_PR_METADATA.json']+list(e['METADATA_FILES'])+['original_submitted_head/'+n for n in custody['files']]}
own={'custody_checkpoint_01/'+n:b'own fixture\n' for n in e['OWN_FILES']-{'SAFE_AUTHORED_MANIFEST.json'}}
manifest={'files':{n:pin(own['custody_checkpoint_01/'+n]) for n in e['OWN_FILES']-{'SAFE_AUTHORED_MANIFEST.json'}},'original_material':{n:pin(raw) for n,raw in materials.items()}}
def mock_read(path):need(path.name=='SAFE_AUTHORED_MANIFEST.json','Only manifest fixture');return manifest
def mock_frozen(path,expected=None):
    raw={**materials,**own}[path]
    if expected is not None:need(pin(raw)==expected,'Fixture exact pin '+path)
    return raw
e['read']=mock_read;e['frozen']=mock_frozen
check('inputs authenticate exact actual receipt, metadata,17archive and4native metadata paths',lambda:e['inputs']())
for path in ('ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json','ORIGINAL_PR_METADATA.json','original_submitted_head/check_candidate.py','original_git_metadata/ORIGINAL_COMMIT.json'):
    saved=materials[path];materials[path]=saved+b' ';rejects('reject material drift '+path,lambda:e['inputs']());materials[path]=saved
manifest['original_material']['original_git_metadata/unreviewed.json']=pin(b'bad');rejects('reject extra unlisted native metadata artifact',lambda:e['inputs']());del manifest['original_material']['original_git_metadata/unreviewed.json']
bad=json.loads(materials['ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json']);bad['base_own_row']=bad['original_QUEUE_row'];saved=materials['ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json'];materials['ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json']=e['enc'](bad);rejects('reject BASE replaced by self-consistent HEAD receipt',lambda:e['inputs']());materials['ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json']=saved
# The pure overlay uses real original materials and virtual own helper files;
# it never writes the five local views or calls a native transport.
materials['custody_checkpoint_01/SAFE_AUTHORED_MANIFEST.json']=e['enc'](manifest)
e['v']=types.SimpleNamespace(native_body=lambda h,path,parent:(e['P']/'CURRENT_PROGRESS.json').read_bytes() if path.endswith('CURRENT_PROGRESS.json') else b'prior Markdown\n')
out=e['overlay'](c,None,'p'*40,'2026-10-16T00:00:00+00:00')
check('overlay excludes QUEUE and all native attempt paths',lambda:need(e['Q'] not in out and not any(x.startswith('unsolved_math_prioritization/attempts/') for x in out),'Overlay scope'))
check('overlay includes all17 exact archive bodies and exact5views',lambda:need(all(out[e['CASE']+'original_submitted_head/'+n]==materials['original_submitted_head/'+n] for n in custody['files']) and all(x in out for x in e['VIEWS']),'Overlay original extent'))
check('only explicit25originals,12authored and5views included',lambda:need(set(out)=={e['CASE']+n for n in materials if not n.startswith('custody_checkpoint_01/')}|{e['CASE']+n for n in own}|{e['CASE']+'custody_checkpoint_01/SAFE_AUTHORED_MANIFEST.json'}|set(e['VIEWS']),'Exact overlay allowlist'))
run=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='run');calls=[x for x in ast.walk(run) if isinstance(x,ast.Call)]
check('authored transport POST endpoints only trees and unreferenced commits',lambda:need({x.args[0].value for x in calls if isinstance(x.func,ast.Attribute) and x.func.attr=='api' and len(x.args)>1 and isinstance(x.args[1],ast.Constant) and x.args[1].value=='POST'}=={'git/trees','git/commits'},'POST scope'))
check('inputs and actual baseline checked before native loader',lambda:need(next(x.lineno for x in calls if isinstance(x.func,ast.Name) and x.func.id=='inputs')<=next(x.lineno for x in calls if isinstance(x.func,ast.Attribute) and x.func.attr=='load') and next(x.col_offset for x in calls if isinstance(x.func,ast.Name) and x.func.id=='inputs')<next(x.col_offset for x in calls if isinstance(x.func,ast.Attribute) and x.func.attr=='load'),'Pre-loader gates'))
for script in ('checkpoint_intake205.py','run_intake205_with_tree_cache.py'):
    r=subprocess.run([sys.executable,'-O','-B',str(D/script)],capture_output=True)
    check('production '+script+' rejects optimized interpreter before phase',lambda x=r:need(x.returncode!=0 and b'Ordinary Python -B required' in x.stderr,'Optimization refusal'))
check('all protected204 sources and existing five views byte/time/mode unchanged',lambda:need(before=={str(p):(pin(p.read_bytes()),p.stat().st_mtime_ns,p.stat().st_mode) for p in protected},'Protected bytes'))
print(json.dumps({'ordinary_or_optimized_test_mode':'optimized' if sys.flags.optimize else 'ordinary','controls_passed':len(results),'controls':results,'production_source_pin':pin(source.read_bytes()),'no_API_or_helper_phase_or_remote_objects_or_current_view_writes':True,'mathematical_clearance':False,'priority_clearance':False,'case_percent':10},indent=2))
