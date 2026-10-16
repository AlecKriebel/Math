#!/usr/bin/env python3
"""Read exact frozen PR36 inputs; run ONLY exact private first-party copies.
No Git, external messaging, live queue, canonical or closed-family writes.
Run --run for a fresh retained replay; --seal / --verify manage this audit's closure.
Foreign source bytes under tmp/ are intentionally excluded from closure.
"""
from pathlib import Path, PurePosixPath
import argparse,ast,copy,datetime,difflib,hashlib,json,shutil,subprocess,sys,xml.etree.ElementTree as ET
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ANCHOR=HERE.parent
PACKET=ANCHOR/'reviewed_candidate'
PIN_MANIFEST='75d103fcfe2bce2322ff091fea73d0f03c7875b00c7c7af8f6e20ff741a2975c'
PIN_DEP='f6b0af0f11ee8aae60678cc37e7cb24373d99484918f893e1a94e9e703d43261'
PIN_BUILD='1c7b8ba0bd02d3c6945dde278fc4c0216140c8175acad577028536b462dd3ea5'
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def check(c,label):
 if not c:raise ValueError(label)
def safe(s):
 p=PurePosixPath(s);check(bool(s) and not p.is_absolute() and '..' not in p.parts and p.as_posix()==s,'unsafe path '+s);return p
def members(m):
 a=m['files'];return [dict(v,path=k) for k,v in a.items()] if isinstance(a,dict) else a

def closure(base,m,self_name=None,exact=False):
 rows=members(m);seen=set()
 for a in rows:
  s=a['path'];safe(s);check(s not in seen and s!=self_name,'duplicate/self '+s);seen.add(s)
  p=base/s;check(p.is_file() and not p.is_symlink(),'nonregular '+s);b=p.read_bytes()
  check(len(b)==a.get('bytes',a.get('size')) and sha(b)==a['sha256'],'hash/size '+s)
 if exact:
  actual={str(p.relative_to(base)) for p in base.rglob('*') if p.is_file()}
  check(actual==seen|({self_name} if self_name else set()),'strict inventory')
 return seen

def inputs():
 check(sha((PACKET/'MANIFEST.json').read_bytes())==PIN_MANIFEST,'manifest pin')
 check(sha((PACKET/'CURRENT_PROOF_DEPENDENCIES.json').read_bytes())==PIN_DEP,'dependencies pin')
 check(sha((PACKET/'CURRENT_BUILD_RECEIPT.json').read_bytes())==PIN_BUILD,'build pin')
 m=load(PACKET/'MANIFEST.json');d=load(PACKET/'CURRENT_PROOF_DEPENDENCIES.json')
 check(len(m['files'])==60 and m['self_excluded']==['MANIFEST.json'],'packet count/self')
 closure(PACKET,m,'MANIFEST.json',True)
 check(len(d['files'])==480 and d['dependency_anchor_repository_relative']=='draft_pr_publication_program_20260930/audits/pr36_20001424','dependency scope')
 closure(ANCHOR,d)
 allrows=[(PACKET,x) for x in m['files']]+[(ANCHOR,x) for x in d['files']]
 parsed=[];code=[];svg=[];unique={};flat=[]
 def scalars(x,key='$'):
  if isinstance(x,dict):
   for k,v in x.items():yield from scalars(v,key+'.'+k)
  elif isinstance(x,list):
   for i,v in enumerate(x):yield from scalars(v,key+f'[{i}]')
  else:yield (key,x)
 for base,x in allrows:
  p=base/x['path'];b=p.read_bytes();h=sha(b)
  if h in unique:continue
  unique[h]=str(p.relative_to(ANCHOR))
  if p.suffix=='.json':
   obj=json.loads(b);parsed.append(str(p.relative_to(ANCHOR)));flat.append({'path':str(p.relative_to(ANCHOR)),'scalars':list(scalars(obj))})
  elif p.suffix=='.jsonl':
   objs=[json.loads(s) for s in b.splitlines() if s.strip()];parsed.append(str(p.relative_to(ANCHOR)));flat.append({'path':str(p.relative_to(ANCHOR)),'scalars':list(scalars(objs))})
  elif p.suffix=='.py':ast.parse(b);code.append(str(p.relative_to(ANCHOR)))
  elif p.suffix=='.svg':ET.fromstring(b);svg.append(str(p.relative_to(ANCHOR)))
 for family,name,n in [('graph_family','authored_manifest.json',190),('algebraic_family','authored_manifest.json',50),('primary_scope_family','AUTHORED_MANIFEST.json',27),('antipodal_priority_family','AUTHORED_MANIFEST.json',79),('arithmetic_graph_priority_family','AUTHORED_MANIFEST.json',18)]:
  fm=load(ANCHOR/family/name);check(len(members(fm))==n,'family count');closure(ANCHOR/family,fm,name)
 rt=load(PACKET/'root_verification/ROOT_REPLAY_RETENTION.json');check(rt['authored_count']==72 and len(rt['files'])==72,'retention72');closure(ANCHOR,rt)
 sm=load(ANCHOR/'snapshot_manifest.json');check(len(sm['files'])==16,'snapshot16')
 for x in sm['files']:
  b=(PACKET/'original_archive'/x['path']).read_bytes();check(sha(b)==x['sha256'] and len(b)==x['size'],'original archive '+x['path'])
  check(b==(ANCHOR/'source_snapshot'/x['path']).read_bytes(),'original source equality')
 source=load(PACKET/'source_record.json');check(source['problem']==load(PACKET/'problem.json') and source['upstream_prior_report']==load(PACKET/'prior_report.json'),'full nested source equality')
 check(sha(json.dumps([source['problem'],source['upstream_prior_report']],sort_keys=True).encode())=='772b051437b7dbf9ab9eddf38e10981f681b99ac4d83f44fbc886600c5c06270','native source pair')
 check(sha((ANCHOR/'pr_input/diff.patch').read_bytes())==sm['diff_sha256'],'full diff pin')
 # Exact blob hashes independently recomputed from preserved source bytes; no Git call.
 for x in sm['files']:
  b=(ANCHOR/'source_snapshot'/x['path']).read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();check(blob==x['git_blob'],'native Git object hash '+x['path'])
 return {'packet_members':60,'dependencies':480,'unique_contents':len(unique),'unique_json_jsonl_parses':len(parsed),'unique_python_AST_parses':len(code),'unique_svg_XML_parses':len(svg),'closure_verified_families':5,'original16_preserved':True,'exact_source_pair':True,'root72_retention_bound':True,'scalar_inspection_files':flat}

def administration(packet=PACKET):
 s=load(packet/'status.json');r=load(packet/'readiness.json');p=load(packet/'problem.json');prior=load(packet/'prior_report.json');turns=[json.loads(x) for x in (packet/'turns.jsonl').read_text().splitlines() if x.strip()]
 q=load(packet/'CURRENT_QUEUE_PATCH.json');before=q['row_before'].split('|');after=q['row_prospective'].split('|')
 b=s['budget'];checks={
 'id':s['id']==r['id']==p['id']==q['id']==20001424,
 'literal':p['statement']==r['exact_target']=='field of definition vs field of moduli\n\nAre all PCF maps defined over their field of moduli?',
 'ledger':len(turns)==1 and turns[0]['turn']==1 and b['used_substantive_attempts']==b['original_substantive_attempts']==1 and b['maximum_substantive_attempts']==5 and b['new_substantive_attempts']==b['verification_attempts']==0,
 'same_budget':b==r['budget'],
 'historical_scope':b['historical_original_reasoning']=='xhigh' and s['current_deadline_utc'] is None and r['native_queue_lifecycle_claimed'] is False,
 'turn_hash':sha((packet/'turns.jsonl').read_bytes())==s['original_turns_sha256'],
 'priority':s['priority_classification']==r['priority_classification']=='PRIOR_APPLICATION' and s['queue_status_proposed']==r['queue_outcome_requested']=='already_solved',
 'pending_gate':s['current_gate']==r['status']==q['current_gate']=='pending_NEW_whole_current_packet_source_first_adversary',
 'no_novelty':not s['new_discovery_claim'] and not r['positive_novelty_claim'] and not s['earliest_worldwide_recognition_claim'] and not r['narrow_degree11_priority_verified'],
 'no_paper':s['paper_or_new_doi_or_tracker'] is r['paper_or_new_doi_or_tracker'] is False,
 'queue12':len(before)==len(after)==14 and q['column_count']==len(q['header_names'])==12,
 'queue_changed_only_named':all(before[i]==after[i] for i in range(14) if i not in [8,9,11]),
 'queue_status_turns':before[8].strip()=='queued' and before[9].strip()=='0/5' and after[8].strip()=='already_solved' and after[9].strip()=='1/5',
 'queue_Chat_DOI':before[10]==after[10] and before[12]==after[12],
 'current_source_hash':r['source_record_sha256']==sha((packet/'source_record.json').read_bytes()),
 'current_proof_hash':r['current_prior_application_sha256']==sha((packet/'CURRENT_PRIOR_APPLICATION.md').read_bytes()),
 }
 return checks

def run_all():
 start=inputs();checks=administration();check(all(checks.values()),'administration baseline')
 stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
 out=HERE/'actual_replay'/stamp;out.mkdir(parents=True,exist_ok=False);runs=[]
 def run(label,src,args=(),expected=0,reference=None,optimized=False,transform=None):
  dst=out/label/'program.py';dst.parent.mkdir(parents=True);b=src.read_bytes()
  if transform:
   old,new=transform;text=b.decode();check(text.count(old)==1,'mutant replacement '+label);alt=text.replace(old,new,1).encode()
   (dst.parent/'source_original.py').write_bytes(b);(dst.parent/'mutation.patch').write_text(''.join(difflib.unified_diff(text.splitlines(True),alt.decode().splitlines(True),fromfile='original',tofile='mutant')));b=alt
  dst.write_bytes(b)
  argv=[sys.executable,*(['-O'] if optimized else []),str(dst),*map(str,args)]
  cp=subprocess.run(argv,cwd=dst.parent,capture_output=True,timeout=180)
  (dst.parent/'actual.stdout').write_bytes(cp.stdout);(dst.parent/'actual.stderr').write_bytes(cp.stderr)
  check(cp.returncode==expected,'unexpected exit '+label+': '+cp.stderr.decode()[-800:])
  equal=None
  if reference is not None:equal=cp.stdout==reference.read_bytes();check(equal,'byte replay '+label)
  rec={'label':label,'source_input':str(src.relative_to(ANCHOR)),'source_sha256':sha(src.read_bytes()),'private_sha256':sha(b),'unchanged_source':transform is None,'command':argv,'exit':cp.returncode,'expected_exit':expected,'stdout_sha256':sha(cp.stdout),'stderr_sha256':sha(cp.stderr),'reference_byte_equality':equal,'optimized':optimized};runs.append(rec)
  return dst.parent,cp
 for f,rec in [('verify_graph.py','graph_verification.json'),('review/independent_checks.py','review/independent_results.json')]:run('original_'+Path(f).stem,PACKET/f,reference=PACKET/rec)
 run('graph_family_exact',ANCHOR/'graph_family/independent_graph_audit.py')
 run('algebra_positive',ANCHOR/'algebraic_family/exact_algebra_controls.py')
 run('algebra_power_one',ANCHOR/'algebraic_family/exact_algebra_controls.py',args=['--power','1'],expected=1)
 run('algebra_no_resultant',ANCHOR/'algebraic_family/exact_algebra_controls.py',args=['--omit-resultant'],expected=1)
 run('arithmetic_exact',ANCHOR/'arithmetic_graph_priority_family/verify_silverman.py')
 run('independent_cubic_checker',ANCHOR/'antipodal_priority_family/silverman_independent_verifier/exact_checks.py',reference=ANCHOR/'antipodal_priority_family/controls/independent_checker_replay.stdout')
 ap=ANCHOR/'antipodal_priority_family';records=load(ap/'CONTROL_RESULTS.json')['records'];exe=load(ap/'EXECUTABLE_MUTANT_RESULTS.json')['records']
 for row in records+exe:
  cmd=row['command'][1:];src=ANCHOR.parents[2]/cmd[0];arg=ANCHOR.parents[2]/cmd[1] if len(cmd)>1 else None
  argcopy=[]
  if arg:
   private=out/('spec_'+row['case']+'.json');private.write_bytes(arg.read_bytes());argcopy=[private]
  if not src.is_file():raise ValueError('exact recorded program missing '+str(src))
  run('antipodal_'+row['case'],src,argcopy,expected=row['exit'])
 # Assertion stripping is an observed verifier limitation, not a certificate.
 transform=('if i<2 else','if i<4 else')
 run('graph_all_inside_rejected',PACKET/'verify_graph.py',transform=transform,expected=1)
 run('graph_all_inside_optimized_blind',PACKET/'verify_graph.py',transform=transform,optimized=True,expected=0)
 run('review_bad_coordinate',PACKET/'review/independent_checks.py',transform=('(-2,0),(0,-2),(0,-3)','(-3,0),(0,-2),(0,-3)'),expected=1)
 run('graph_false_degree_output_blind',PACKET/'verify_graph.py',transform=("'candidate_degree':11","'candidate_degree':12"),expected=0)
 # Prose is not loaded by either original checker. Actual false prose copy + unchanged execution.
 prose=out/'prose_blind';prose.mkdir();(prose/'CANDIDATE.md').write_text((PACKET/'CANDIDATE.md').read_text().replace('There exists a degree-11','There exists a degree-12',1))
 shutil.copyfile(PACKET/'verify_graph.py',prose/'verify_graph.py');cp=subprocess.run([sys.executable,str(prose/'verify_graph.py')],cwd=prose,capture_output=True)
 (prose/'actual.stdout').write_bytes(cp.stdout);(prose/'actual.stderr').write_bytes(cp.stderr);check(cp.returncode==0 and cp.stdout==(PACKET/'graph_verification.json').read_bytes(),'prose blind actual')
 # Actual metadata file mutants tested by all administration predicates.
 metadata=[]
 for label,file,key,value in [('hidden_turn','status.json','used_substantive_attempts',2),('wrong_id','status.json','id',20001425),('new_deadline','status.json','current_deadline_utc','2026-10-03T00:00:00Z'),('novelty','status.json','new_discovery_claim',True),('narrow_target','problem.json','statement','Are all PCF maps with odd postcritical sets defined over their field of moduli?')]:
  dst=out/('metadata_'+label);shutil.copytree(PACKET,dst);obj=load(dst/file)
  if key=='used_substantive_attempts':obj['budget'][key]=value
  else:obj[key]=value
  (dst/file).write_text(json.dumps(obj,indent=2)+'\n');obs=administration(dst);check(not all(obs.values()),'metadata mutant accepted '+label);metadata.append({'label':label,'actual_private_files':True,'checks':obs})
 # Exact manifest controls are integrity controls, distinct from mathematical falsification.
 controls=[];toy=out/'closure_controls';toy.mkdir();(toy/'a').write_text('one');mm={'files':[{'path':'a','bytes':3,'sha256':sha(b'one')}]};closure(toy,mm,exact=True)
 for label,mutate in [('missing',lambda: (toy/'a').rename(toy/'removed')),('extra',lambda:(toy/'extra').write_text('x')),('corrupt',lambda:(toy/'a').write_text('two'))]:
  base=out/('control_'+label);shutil.copytree(toy,base)
  if label=='missing':(base/'a').unlink()
  elif label=='extra':(base/'extra').write_text('x')
  else:(base/'a').write_text('two')
  try:closure(base,mm,exact=True)
  except ValueError as e:controls.append({'label':label,'rejected':True,'reason':str(e)})
  else:raise ValueError('integrity control accepted '+label)
 end=inputs();check({k:v for k,v in start.items() if k!='scalar_inspection_files'}=={k:v for k,v in end.items() if k!='scalar_inspection_files'},'input changed')
 receipt={'utc':now(),'status':'PASS_WITH_EXPLICIT_LIMITS','exact_manifest_pin':PIN_MANIFEST,'dependency_pin':PIN_DEP,'build_pin':PIN_BUILD,'input_scan':{k:v for k,v in start.items() if k!='scalar_inspection_files'},'administration_baseline':checks,'actual_runs':runs,'metadata_mutants':metadata,'integrity_mutants':controls,'actual_false_prose_pass_observed':True,'original_optimization_blind_spot_observed':True,'false_output_degree_blind_spot_observed':True,'new_substantive_attempts':0,'full_live_git_corpus_and_whole_queue_not_replayed':'Root-owned actions prohibited in this adversary. Bound original/family/root receipts and code audited; original blob hashes rederived from frozen bytes. Whole queue preimage/prospective bytes are not included in packet, so their entire hash must be checked by root at integration. No transferred earlier PASS.'}
 (HERE/('ACTUAL_REPLAY_'+stamp+'.json')).write_text(json.dumps(receipt,indent=2)+'\n')
 (HERE/'STRUCTURED_FULL_SCAN.json').write_text(json.dumps(start['scalar_inspection_files'],indent=2)+'\n')
 print(json.dumps({'status':receipt['status'],'actual_program_runs':len(runs),'private_root':str(out),'new_attempts':0},indent=2))

def authored(seal=False):
 name='AUTHORED_MANIFEST.json';files=[]
 for p in sorted(HERE.rglob('*')):
  rel=p.relative_to(HERE)
  if 'tmp' in rel.parts or '__pycache__' in rel.parts or str(rel)==name:continue
  if p.is_file():check(not p.is_symlink(),'authored symlink');b=p.read_bytes();files.append({'path':str(rel),'bytes':len(b),'sha256':sha(b)})
 if seal:(HERE/name).write_text(json.dumps({'utc':now(),'strict_self_excluding':True,'self_excluded':[name],'foreign_scratch_excluded':['tmp/','__pycache__/'],'files':files,'member_count':len(files)},indent=2)+'\n')
 else:
  m=load(HERE/name);check(m['files']==files and m['member_count']==len(files) and m['self_excluded']==[name],'strict authored closure differs')
 print(json.dumps({'authored_member_count':len(files),'mode':'seal' if seal else 'verify'},indent=2))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--run',action='store_true');a.add_argument('--seal',action='store_true');a.add_argument('--verify',action='store_true');v=a.parse_args()
 if v.run:run_all()
 if v.seal or v.verify:authored(v.seal)
