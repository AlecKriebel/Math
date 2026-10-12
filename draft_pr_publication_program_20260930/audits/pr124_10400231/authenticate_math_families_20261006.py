"""Read-only authentication and actual replay of sealed PR124 mathematical/source families."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent
D=A/'root_math_family_reproduction_20261006'
PY='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
events=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def req(b,s):
 if not b:raise RuntimeError(s)
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
CONFIG=json.loads((A/'MATH_FAMILY_SEAL_BINDINGS_20261006.json').read_text())
req(not D.exists(),'Actual family replay already exists; inspect before retry')
D.mkdir()
env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
families=[];allpins={}
for item in CONFIG['families']:
 F=A/item['directory'];manifest=F/'SHA256SUMS.json'
 req(sha(manifest.read_bytes())==item['manifest_sha256'],'Reported manifest changed')
 req(sha((F/'REPORT.md').read_bytes())==item['report_sha256'],'Reported report changed')
 raw=json.loads(manifest.read_text())['files']
 if isinstance(raw,dict):members=[{'path':k,'bytes':v.get('bytes',v.get('size_bytes')),'sha256':v['sha256']} for k,v in raw.items()]
 else:members=raw
 req(len(members)==item['member_count'],'Expected public member count')
 pins={}
 for m in members:
  relative=Path(m['path'])
  req(not relative.is_absolute() and '..' not in relative.parts and not {'private','private_sources','__pycache__'}.intersection(relative.parts),'Public path scope')
  path=F/relative
  req(path.is_file() and not path.is_symlink(),'Regular sealed public member')
  body=path.read_bytes();req(len(body)==m['bytes'] and sha(body)==m['sha256'],'Sealed public body '+str(path))
  pins[str(path)]={'bytes':len(body),'sha256':sha(body)}
 result=json.loads((F/'RESULT.json').read_text())
 families.append({'family':item['directory'],'manifest_sha256':item['manifest_sha256'],'report_sha256':item['report_sha256'],'member_count':len(members),'full_members_authenticated':True,'result':result})
 allpins.update(pins);allpins[str(manifest)]={'bytes':manifest.stat().st_size,'sha256':sha(manifest.read_bytes())}
def run(family,script,tag,args,opt,expect,reason=None):
 path=A/family/script
 argv=[PY,'-E','-S','-B','-P']+(['-O'] if opt else [])+[str(path),*args]
 ch=subprocess.Popen(argv,cwd=D,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 out,err=ch.communicate()
 entry={'family':family,'tag':tag,'optimized':opt,'PID':ch.pid,'argv':argv,'UTC':now(),'exit_code':ch.returncode,'expected_exit_code':expect,'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err)}
 (D/(tag+'.stdout.txt')).write_bytes(out);(D/(tag+'.stderr.txt')).write_bytes(err)
 events.append(entry);dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'events':events})
 req(ch.returncode==expect,'Unexpected exit '+tag)
 if reason:req(reason.encode() in out+err,'Expected actual guard rejection missing '+tag)
 if expect==0:
  data=json.loads(out);entry['result']=data
  if family.startswith('integral_topology'):
   req(data['pid']==ch.pid and data['total_checks']==17047 and data['optimized']==opt,'Actual topology baseline')
  elif family.startswith('integral_algebra'):
   req(data['status']=='PASS' and data['explicit_checks']==3360 and data['matrix_cases']==673,'Actual algebra baseline')
  else:req(data['scope_mutations_rejected']==12 and data['source_pdf_hashes_verified']==3,'Actual source baseline')
 return entry
for opt in [False,True]:
 suffix='_optimized' if opt else '_normal'
 F='integral_topology_adversary_20261006'
 for mode in ['normal','false-arbitrary-module','mutant-drop-torsion','mutant-strengthen-by-one']:
  run(F,'checks.py','topology_'+mode+suffix,['--mode',mode],opt,0 if mode=='normal' else 1,None if mode=='normal' else 'guard_reject:')
 F='integral_algebra_adversary_20261006'
 run(F,'audit_exact.py','algebra_baseline'+suffix,[],opt,0)
 for mutant in ['order_one','zero_order_zero','empty_det_zero','primitive_content','drop_torsion','remove_tminus1','valuation_as_nullity','rectangular_as_square']:
  run(F,'audit_exact.py','algebra_'+mutant+suffix,['--mutant',mutant],opt,1,'"status": "REJECTED"')
 F='primary_scope_adversary_20261006'
 run(F,'verify_scope.py','source_baseline'+suffix,[],opt,0)
 negatives=json.loads((A/F/'FALSEGUARDS.json').read_text())['runs']
 for n in [x for x in negatives if x['mode']=='normal']:
  run(F,'verify_scope.py','source_'+n['falseguard']+suffix,['--falseguard',n['falseguard']],opt,1,n['decisive_error'])
for p,pin in allpins.items():
 body=Path(p).read_bytes();req(len(body)==pin['bytes'] and sha(body)==pin['sha256'],'Sealed family mutated by root replay')
original=json.loads((A/'original_head_authentication_20261006/ORIGINAL_AUTHENTICATION.json').read_text())
for pin in original['original_files']:
 body=(A/'original_head_authentication_20261006/original_attempt'/pin['path']).read_bytes()
 req(len(body)==pin['bytes'] and sha(body)==pin['sha256'],'Original changed')
receipt={'schema':'pr124-root-math-family-authentication-and-actual-replay/v1','UTC':now(),'actual_operator_PID':os.getpid(),'families':families,'public_member_count':sum(x['member_count'] for x in families),'actual_child_count':len(events),'all_actual_expected_exits_passed':True,'normal_and_physical_optimized_modes':True,'original17_and_all_sealed_members_unchanged':True,'new_central_proof_search_turns':0,'publication_or_native_or_service_mutations':False}
dump(A/'ROOT_MATH_FAMILY_AUTHENTICATION_20261006.json',receipt)
gate={'schema':'pr124-mathematical-source-gate/v1','status':'PASS','UTC':now(),'original_head':original['original_head'],'original_candidate_sha256':'483bc7e3dccd4d6d262d36341becdf05bfa22f7d52e721eae4f51ecdc0fb95e5','original_attempts':'2/5','review_hash':original['review_hash'],'literal_original_counterexample_valid':True,'independent_families':3,'root_authentication_receipt':'ROOT_MATH_FAMILY_AUTHENTICATION_20261006.json','remaining_mandatory_mathematical_or_source_findings':[],'guard_only_diagnostic_repair_separate':True,'novelty_established':False,'priority_clearance':False,'priority_audit_may_now_begin':True,'publication_clearance':False,'new_central_proof_search_turns':0,'goal_active':True,'program_completed':20,'dated_eligible_total':99}
dump(A/'MATHEMATICAL_SOURCE_GATE_20261006.json',gate)
(A/'MATH_FAMILY_CHECKPOINT_LOG_20261006.md').write_text('# PR124 mathematical/source checkpoint\n\n'+now()+': Three independent complete math/source families fully authenticated and actualnormal/-O replayed with deliberate mutant/falseguard rejection; mathematics/sourcePASS100%. Full original counterexample valid, novelty and priority remain unestablished. Bounded priority may now begin; workflow25%, publication0%, program20/99=20.20%, goalactive; original2/5/newcentralturns0 preserved. Root writer released, no tracked/global/native/service mutations. This untracked checkpoint log joins the tracked effort log at the next coordinated checkpoint.\n')
print(json.dumps({'UTC':receipt['UTC'],'PID':os.getpid(),'public_members':receipt['public_member_count'],'children':len(events),'math_source_gate':'PASS','publication_clearance':False,'priority_audit_may_now_begin':True}))
