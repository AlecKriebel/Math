"""Independent PR47 SOURCE controls. Production files are read as data only."""
from pathlib import Path, PurePosixPath
import copy, ctypes, datetime as dt, hashlib, json, math, os, stat, sys
assert __debug__ and sys.flags.optimize == 0
F=Path(__file__).absolute().parent; A=F.parent; R=A.parents[2]; P=A/'acceptance_preparation_family'; C=A/'reviewed_candidate'; W=A/'current_whole_adversary_family'
START=dt.datetime.now(dt.timezone.utc).isoformat(); N=0; CACHE={}; REFS={}; NEG=[]
MF='1a10442d9962db99c608412f53fef754870bfadf24fd76e7e899112fc38ebef1'
def need(ok,label):
 global N
 N+=1
 if not ok:raise ValueError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def parse(raw):
 def pairs(items):
  out={}
  for k,v in items:
   if k in out:raise ValueError('duplicate key')
   out[k]=v
  return out
 def floating(s):
  v=float(s)
  if not math.isfinite(v):raise ValueError('nonfinite float')
  return v
 return json.loads(raw,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def typed(a,b):
 if type(a)!=type(b):return False
 if isinstance(a,dict):return set(a)==set(b) and all(typed(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(typed(x,y) for x,y in zip(a,b))
 return a==b
def name(n):
 if type(n)!=str or not n or '\\' in n or '\0' in n:raise ValueError('path type')
 p=PurePosixPath(n)
 if p.is_absolute() or p.as_posix()!=n or n=='.' or set(p.parts)&{'.','..','.git','__pycache__'}:raise ValueError('noncanonical path')
 return n
def raw(p,bind=True):
 p=Path(p).absolute();need(not p.is_symlink() and all(not x.is_symlink() for x in p.parents) and stat.S_ISREG(p.stat().st_mode),'regular nonsymlink '+str(p))
 b=p.read_bytes();mode=stat.S_IMODE(p.stat().st_mode)
 if p in CACHE:need(CACHE[p]==b,'unchanged repeated complete bytes '+str(p))
 CACHE[p]=b
 if bind and not p.is_relative_to(F):
  REFS[p.relative_to(R).as_posix()]={'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':mode}
 return b
def load(p):return parse(raw(p))
def check(base,z,mode=True):
 b=raw(base/name(z['path']));need(type(z['bytes'])==int and z['bytes']>=0 and len(b)==z['bytes'] and sha(b)==z['sha256'],'complete binding '+z['path'])
 if mode:need(type(z['full_mode'])==int and stat.S_IMODE((base/z['path']).stat().st_mode)==z['full_mode'],'exact fullmode '+z['path'])
 return b
def closed(base,selfname,pin,count,dirs):
 b=raw(base/selfname);need(sha(b)==pin,'explicit manifest pin');m=parse(b);rr=m['files'];need(type(m['files_count'])==int and m['files_count']==len(rr)==count and m['self_excluded']==[selfname],'exact closure count/self')
 paths=[]
 for z in rr:
  need(set(z)<={'path','bytes','sha256','full_mode'} and {'path','bytes','sha256'}<=set(z),'typed manifest row')
  check(base,{**z,'full_mode':0o444});paths.append(z['path'])
 need(len(set(paths))==len(paths) and selfname not in paths,'unique self excluded')
 seenfiles=set();seendirs=set()
 for p in base.rglob('*'):
  need(not p.is_symlink() and (p.is_dir() or p.is_file()),'exact regular topology')
  (seenfiles if p.is_file() else seendirs).add(name(p.relative_to(base).as_posix()))
 expected={x.as_posix() for n in paths for x in PurePosixPath(n).parents if x.as_posix()!='.'}
 need(seenfiles==set(paths)|{selfname} and seendirs==expected and len(seendirs)==dirs,'full recursive exact topology')
 need(stat.S_IMODE((base/selfname).stat().st_mode)==0o444,'manifest full444');return m

def utc(s):
 if type(s)!=str:raise ValueError('clock type')
 v=dt.datetime.fromisoformat(s)
 if v.tzinfo is None or v.utcoffset()!=dt.timedelta(0):raise ValueError('aware UTC required')
 if v>dt.datetime.now(dt.timezone.utc):raise ValueError('future clock')
 return v

def reject(label,fn):
 try:fn()
 except (ValueError,TypeError,KeyError,OSError):NEG.append(label);return
 raise ValueError('accepted malformed '+label)

def capture(folder,kind,code=0):
 c=load(folder/'CAPTURE.json');need(type(c.get('pid'))==int and c['pid']>0 and type(c['exit_code'])==int and c['exit_code']==code and c['actual_execution'] is True and c['completed'] is True and c['stdin_supplied'] is False,'actual PID/exit/truths')
 need(utc(c['started_utc'])<=utc(c['finished_utc']),'capture chronology')
 for ch in ['stdout','stderr']:
  z=c[ch];need(set(z)=={'path','bytes','sha256'},'exact splitstream rows');check(folder,z,False)
 need((folder/'stderr.bin').read_bytes()==b'' if code==0 else (folder/'stderr.bin').read_bytes()!=b'','literal successful/failed stderr')
 if kind=='prepared':
  need({x.name for x in folder.iterdir()}=={'CAPTURE.json','PRELAUNCH.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'},'six actual private members')
  q=load(folder/'PRELAUNCH.json');need(c['schema']=='pr47-acceptance-source-preparation-private-actual-capture/v1' and c['production_import_compile_or_execution'] is False,'private class scope')
  need(c['source_unchanged'] is True and c['operator_unchanged'] is True and sha(raw(folder/'PRELAUNCH_SOURCE.py'))==c['source_sha256']==q['source_sha256'] and sha(raw(folder/'PRELAUNCH_OPERATOR.py'))==c['operator_sha256']==q['operator_sha256'],'full prelaunch source/operator')
  need(c['argv']==q['argv'] and c['cwd']==q['cwd']==str(R) and utc(q['started_utc'])<=utc(c['started_utc']),'actual prelaunch binding')
 elif kind=='root':
  need({x.name for x in folder.iterdir()}=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'},'four literal ROOT members')
  need(c['schema']=='root-explicit-command-capture/v1' and c['operator_unchanged'] is True and sha(raw(folder/'prelaunch_operator.py'))==c['operator_sha256'],'actual ROOT operator')
 return c

def original_capture(c,kind):
 if type(c)!=dict or c['schema']!='pr47-root-literal-operation-capture/v1':raise ValueError('class')
 if type(c['pid'])!=int or c['pid']<=0 or type(c['exit_code'])!=int or c['exit_code']!=0:raise ValueError('PID/exit')
 if c['actual_execution'] is not True or c['completed'] is not True or c['stdin_supplied'] is not False:raise ValueError('truths')
 if c['cwd']!=str(R) or utc(c['started_utc'])>utc(c['finished_utc']):raise ValueError('argv/clock')
 if kind=='git':
  if c['source'] is not None or c['source_unchanged'] is not None or c['argv'][0]!='git':raise ValueError('Git exact null')
 else:
  if type(c['source'])!=dict or c['source_unchanged'] is not True or c['argv'][:2]!=['/usr/bin/python3','-B']:raise ValueError('helper typed source')
 return True

def main():
 pm=closed(P,'PREPARATION_MANIFEST.json',MF,126,18)
 cm=closed(C,'MANIFEST.json','a7d1acc9dbbf8cd5435d0bebd8f6b1a540ecb0f2aea8d0c616c46bc5bf6b4ea5',1328,282)
 wm=closed(W,'MANIFEST.json','658133399198e8528aa2a45b89c87a19f3b69edd6998b86b7e8227c850f5fd78',385,84)
 inputs=load(P/'INPUT_BINDINGS.json');need(inputs['actual_predecessor_PR46_completed'] is False and all(inputs[k] is None for k in ['previous_mirror','previous_post','previous_root_post','previous_post_contract']),'pending actual46')
 for z in list(inputs['pins'].values())+inputs['external_input_rows']:check(R,z)
 need(len(inputs['external_input_rows'])==2933 and len({z['path'] for z in inputs['external_input_rows']})==2933,'exact unique external scope')
 design=inputs['unfinished_design_reference'];check(R,design,False);design_actual=REFS[design['path']];need(design_actual['full_mode'] in [design['full_mode'],0o444],'narrow dated unfinished design mode');need(inputs['dated_native_external_rows']==[],'mutable native not immutable external')
 deps=load(C/'CURRENT_DEPENDENCIES.json');need(typed(deps,load(P/'EXPECTED_CURRENT_DEPENDENCIES.json')) and len(deps['files'])==1422,'entire1422dependency object')
 for z in deps['files']:check(R,z)
 rw=load(A/'ROOT_WHOLE_CURRENT_REVIEW.json');need(sha(raw(A/'ROOT_WHOLE_CURRENT_REVIEW.json'))=='b10320f4ca9bc5fb233e4a8cce4baecafc3fff71a7f0b0e5966495aafcd61c9a' and typed(rw,load(P/'EXPECTED_ROOT_WHOLE_REVIEW.json')),'entire ROOT whole typed object')
 need(typed(load(W/'VERDICT.json'),load(P/'EXPECTED_WHOLE_VERDICT.json')) and typed(wm,load(P/'EXPECTED_WHOLE_MANIFEST.json')),'whole entire copies')
 for live,expected in [('ROOT_SCIENCE_CARD.json','EXPECTED_SCIENCE_CARD.json'),('ROOT_PRIMARY_READ_LEDGER.json','EXPECTED_PRIMARY_READ_LEDGER.json')]:need(typed(load(A/live),load(P/expected)),'entire ROOT prerequisite attribution')
 original=load(P/'EXPECTED_ORIGINAL_CAPTURE_RESULT.json');need(typed(original,load(A/'root_original_actual_reproduction/ROOT_REPRODUCTION_RESULT.json')),'full literal original record')
 gc=original['complete_actual_Git_captures'];hc=original['complete_actual_helper_captures'];need(len(gc)==33 and len(hc)==3,'exact original classes')
 for c,kind in [(x,'git') for x in gc]+[(x,'helper') for x in hc]:
  need(original_capture(c,kind),'real original class accepted')
  for ch in ['stdout','stderr']:check(R,c[ch],False)
  if kind=='helper':check(R,c['source'],False)
  need(c['stderr']['bytes']==0,'original empty fullstderr')
  for field,val in [('pid',True),('exit_code',False),('actual_execution',1),('stdin_supplied',None),('finished_utc','2099-01-01T00:00:00+00:00')]:
   bad=copy.deepcopy(c);bad[field]=val;reject(kind+'/'+field,lambda b=bad,k=kind:original_capture(b,k))
  bad=copy.deepcopy(c);bad['source_unchanged']=True if kind=='git' else None;reject(kind+'/sourceclass',lambda b=bad,k=kind:original_capture(b,k))
 archive={z['path'][len('original_archive/'):] for z in cm['files'] if z['path'].startswith('original_archive/')};need(len(archive)==16,'original archive16')
 immutable=['turns.json','source_checksums.json','review/independent_checks.py','prior_report.json','verification.json','review/submitted_results.json','verify.py','review/independent_results.json','review/submitted_verify.py','source_record.json']
 for n in archive:need(raw(C/'original_archive'/n)==raw(A/'source_snapshot'/n),'exact original16archive')
 for n in immutable:need(raw(C/n)==raw(C/'original_archive'/n),'operative immutable10')
 need(raw(C/'prior_report.json')==b'null\n' and load(C/'prior_report.json') is None,'literal null not absence/fallback')
 need(typed(load(C/'turns.json'),load(P/'EXPECTED_ORIGINAL_LEDGER.json')) and load(C/'turns.json')['count']==1,'whole object original1/5')
 for n in ['status.json','readiness.json','review/verdict.json','review/review_summary.json']:need(typed(load(C/n),load(P/'EXPECTED_CURRENT_ADMIN.json')),'archival current administrative4')
 science=load(P/'SCIENTIFIC_SCOPE.json');need(science['literal_target_status']=='unsolved' and science['original_substantive_attempts']==1 and science['turn_limit']==5 and science['partial_valid'] is True,'science unsolved1/5')
 for k in ['full_problem_solved','full_problem_solved_by_project','counterexample_to_full_target_claimed','quartic_model_realized_as_Chern_Simons','realized_example_instanton_rank_computed','novelty_claimed','priority_claimed','paper_or_new_doi_or_tracker','human_referee_review_claimed']:need(science[k] is False,'no promotion '+k)
 for n,pin in science['operative_artifact_sha256'].items():need(sha(raw(C/n))==pin,'scope artifact exact')
 plan=load(P/'DRAFT_FINAL_PLAN.json');need(plan['pr']==47 and typed(plan['scientific_scope'],science) and plan['plan_status']=='PENDING_ROOT_FULL_REVIEW_AND_ACTUAL_RECONCILIATION','exact pending plan')
 for k in ['root_acceptance_source_review_completed','root_actual_PR46_predecessor_read_completed','root_full_current_read_completed','root_full_whole_read_completed','independent_whole_current_pass','historical_PASS_transferred','science_reexecution_of_current']:need(plan[k] is False,'draft future false '+k)
 for n in ['DRAFT_ROOT_PRIMARY_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json','DRAFT_ROOT_SCOPE_CERTIFICATE.json']:
  d=load(P/n);need(d['created_utc'] is None and d['actual_pid'] is None and d['root_completed'] is False and d['future_acceptance_approved'] is False and typed(d['entire_known_scientific_scope'],science),'draft not approval')
 contract=load(P/'ROOT_POST_CONTRACT.json');need(len(contract['future47_required_ROOT_complete_keyset'])==22 and len(set(contract['future47_required_ROOT_complete_keyset']))==22 and contract['future_ROOT_post_completed'] is False,'22-key future contract')
 need(contract['predecessor']['actually_completed'] is False and all(contract['predecessor'][k] is None for k in ['mirror','post','ROOT_post','ROOT_post_contract']),'pending entire predecessor')
 required=contract['future47_required_completed_values'];need(required['completed_primary_prs']==37 and required['program_completion_percent']==37*100/180 and required['new_substantive_attempts']==0 and required['audit_turns']==0,'exact whole-accounting22contract')
 for n in ['state_mirror_bindings.json','post_acceptance_verification.json','ROOT_ACTUAL_POST_INSPECTION.json']:need(not (R/'draft_pr_publication_program_20260930/audits/pr46_30004438'/n).exists(),'actual46 remains absent '+n)
 expected={'inspect_inputs_v1_actual_capture':0,'author_sources_v1_actual_capture':0,'private_controls_v1_actual_capture':1,'repair_sources_v2_actual_capture':0,'private_controls_v2_actual_capture':0,'expected_negative_actual_capture':1,'harden_sources_v3_actual_capture':0,'precision_sources_v4_actual_capture':0,'final_readback_v4_actual_capture':0,'final_readback_v5_actual_capture':0}
 records=[capture(P/n,'prepared',code) for n,code in expected.items()]
 a45=R/'draft_pr_publication_program_20260930/audits/pr45_9900007';rootcaps=[capture(a45/n,'root') for n in ['root_pr47_acceptance_source_closure_actual_capture','root_pr47_acceptance_source_closed_readback_actual_capture']]
 need(rootcaps[0]['pid']==35179 and rootcaps[1]['pid']==35553 and utc(rootcaps[0]['finished_utc'])<=utc(rootcaps[1]['started_utc']),'actual separate ROOTclose/readback')
 final=load(P/'FINAL_READY_CHECK.json');need(final['actual_pid']==25105 and final['production_imported_compiled_executed'] is False and final['future_acceptance_approved'] is False and final['actual_PR46_predecessor_completed'] is False,'final actual qualification')
 for n,z in final['source_files'].items():check(P,{'path':n,**z},False)
 files={z['path'] for z in cm['files']};admin={'status.json','readiness.json','review/verdict.json','review/review_summary.json'}
 overlay=files|{'reviewed_pending_administration/'+n for n in admin}|{'reviewed_pending_administration/MANIFEST.json','ACCEPTED_QUEUE_PATCH.json','CURRENT_ACCEPTANCE_SCOPE.md','CURRENT_CONTEXT_PRESENT.md','CURRENT_AUDIT_SCOPE_PRESENT.md'}
 accepted=overlay|{'acceptance.json','ACCEPTANCE.md'};need(len(overlay)==1337 and len(accepted)==1339 and 'MANIFEST.json' not in accepted,'exact canonical1337/1339+self')
 # Handwritten independent safety models: no source extraction/import/compile.
 for x in ['','.', './x','x//y','x/../y','/x','x\\y','x\0y','.git/a','__pycache__/a',True,None]:reject('path/'+repr(x),lambda x=x:name(x))
 for x in [b'{"x":1,"x":2}',b'{"n":NaN}',b'{"n":Infinity}',b'{"n":1e999}']:reject('json/'+repr(x),lambda x=x:parse(x))
 need(not typed({'x':True},{'x':1}) and not typed(None,{}) and not typed([1],[1.0]),'recursive scalar type/null distinctions')
 for x in ['2026-10-03T01:00:00','2026-10-03T01:00:00-07:00','2099-01-01T00:00:00+00:00',True]:reject('clock/'+str(x),lambda x=x:utc(x))
 # Exact ownership, with adjacent prefixes and other program bodies remaining foreign.
 native={z['path'] for z in inputs['dated_native13']};program='draft_pr_publication_program_20260930/RESEARCH_LOG.md';ap=A.relative_to(R).as_posix();kp='unsolved_math_prioritization/attempts/2849'
 def owned(n):
  name(n);return n in native or n==program or n.startswith(ap+'/') or n.startswith(kp+'/')
 for n in [program,ap+'/ROOT_RESEARCH_LOG.md',kp+'/acceptance.json']:need(owned(n),'exact authorized ownership')
 for n in [program+'.bak','draft_pr_publication_program_20260930/unrelated/RESEARCH_LOG.md',ap+'0/file',kp+'0/file','draft_pr_publication_program_20260930/audits/pr46_30004438/ROOT_RESEARCH_LOG.md']:need(not owned(n),'adjacent/foreign no broad exemption')
 def foreign(names):
  if type(names)!=list or names!=sorted(set(names)) or any(owned(n) for n in names):raise ValueError('owned foreign protection contradiction')
 reject('programlogdeclaredforeign',lambda:foreign([program]));foreign(['draft_pr_publication_program_20260930/unrelated/RESEARCH_LOG.md'])
 fixtures=F/'private_fixtures';fixtures.mkdir(exist_ok=False);q=fixtures/'mode.bin';q.write_bytes(b'actual fullmode probe\n')
 for mode in range(4096):q.chmod(mode);need(stat.S_IMODE(q.stat().st_mode)==mode,'actual full S_IMODE mode');need((stat.S_IMODE(q.stat().st_mode)==0o444)==(mode==0o444),'only exact444 freeze')
 q.chmod(0o644);foreignfile=fixtures/'foreign.bin';foreignfile.write_bytes(b'unrelated dirty exact prefix\n');foreignfile.chmod(0o640);foreignbefore=foreignfile.read_bytes();foreignmode=stat.S_IMODE(foreignfile.stat().st_mode)
 appendrows=[]
 for label,mode in [('root_problem',0o644),('program',0o6754)]:
  p=fixtures/(label+'.log');prefix=(label+' retained prefix\n').encode();p.write_bytes(prefix);p.chmod(mode);before=stat.S_IMODE(p.stat().st_mode);retained=fixtures/(label+'.preimage.bin');retained.write_bytes(prefix)
  note=b'\nPRIVATE MODEL ONLY; no actual acceptance or ROOT authority.\n';stage=fixtures/(label+'.tmp');stage.write_bytes(prefix+note);stage.replace(p);p.chmod(before)
  need(p.read_bytes()==retained.read_bytes()+note and stat.S_IMODE(p.stat().st_mode)==before,'exact two retained-prefix appends/fullmode');appendrows.append({'label':label,'mode':before,'prefix_sha256':sha(prefix),'after_sha256':sha(p.read_bytes())})
 need(foreignfile.read_bytes()==foreignbefore and stat.S_IMODE(foreignfile.stat().st_mode)==foreignmode,'foreign bytes/fullmode preserved')
 link=fixtures/'symlink';link.symlink_to(q.name);reject('actualsymlink',lambda:raw(link,False));link.unlink();fifo=fixtures/'fifo';os.mkfifo(fifo);reject('actualFIFO',lambda:raw(fifo,False));fifo.unlink()
 # Real macOS exclusive directory rename, private only; does not execute sealer.
 libc=ctypes.CDLL(None,use_errno=True);fn=libc.renamex_np;fn.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint];fn.restype=ctypes.c_int
 stage=fixtures/'rename_stage';stage.mkdir();(stage/'member').write_bytes(b'own private exclusive publication\n');dest=fixtures/'published';need(fn(os.fsencode(stage),os.fsencode(dest),4)==0,'actual private absent-only rename')
 stage=fixtures/'second_stage';stage.mkdir();(stage/'member').write_bytes(b'unchanged secondstage\n');need(fn(os.fsencode(stage),os.fsencode(dest),4)!=0 and (stage/'member').read_bytes()==b'unchanged secondstage\n' and (dest/'member').read_bytes()==b'own private exclusive publication\n','actual existing directory overwrite rejected')
 # An approval fixture is explicitly not an actual approval; missing predecessor always rejects.
 def predecessor(actual):
  if actual is None or type(actual)!=dict or set(actual)!=set(contract['future47_required_ROOT_complete_keyset']) or not typed(actual.get('entire_post'),{'actual':'complete'}):raise ValueError('missing/full predecessor contract')
 reject('pendingprednoauthority',lambda:predecessor(None));reject('SOURCEpassnoauthority',lambda:predecessor({'status':'PASS_SOURCE_ONLY_SCOPED'}));reject('booleanactualpostnoauthority',lambda:predecessor(True))
 # Own observation clocks must be inside operator clocks, never falsely equal to them.
 c=records[-1];need(utc(c['started_utc'])<=utc(final['created_utc'])<=utc(c['finished_utc']),'actual final child observation contained in operator interval')
 bindings=sorted(REFS.values(),key=lambda z:z['path']);(F/'EXTERNAL_INPUT_BINDINGS.json').write_text(json.dumps({'schema':'pr47-source-adversary-exact-external-bindings/v1','preparation_manifest_sha256':MF,'mutable_native4_are_dated_observations_not_live_closure_dependencies':True,'unfinished_design_recorded_mode_is_dated':True,'files_count':len(bindings),'files':bindings},indent=2)+'\n')
 result={'schema':'pr47-source-adversary-private-controls/v1','status':'PASS_SOURCE_ONLY_CONTROLS','actual_pid':os.getpid(),'started_utc':START,'finished_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'assertions':N,'malformed_models_rejected':len(NEG),'malformed_model_labels':NEG,'preparation_payload':126,'current_payload':1328,'whole_payload':385,'whole_relative_directories':84,'dependencies':1422,'individual_preparation_external':2933,'own_complete_unique_external_bindings':len(bindings),'unique_complete_bytes_read':sum(len(b) for p,b in CACHE.items()),'complete_source_preparation_captures':len(records),'real_original_Git_null':33,'real_original_helpers_typed':3,'actual_ROOT_source_closer_pid':rootcaps[0]['pid'],'actual_ROOT_source_readback_pid':rootcaps[1]['pid'],'original16_archive':16,'immutable10':10,'current_admin4':4,'actual_full_modes':4096,'private_actual_owned_append_models':appendrows,'canonical_overlay':1337,'accepted_payload':1339,'accepted_self_total':1340,'future_native_expected':13,'dated_native4_not_live_authority':True,'actual_PR46_predecessor_completed':False,'production_imported_compiled_executed':False,'future_acceptance_approved':False,'new_substantive_attempts':0,'audit_turns':0,'paper_or_new_doi_or_tracker':False}
 (F/'PRIVATE_CONTROL_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['malformed_model_labels','private_actual_owned_append_models']},sort_keys=True))
if __name__=='__main__':main()
