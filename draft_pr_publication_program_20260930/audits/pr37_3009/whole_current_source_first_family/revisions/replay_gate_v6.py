#!/usr/bin/env python3
"""Actual private whole-current PR37 replay. This imports no prior PASS verdict.

Use /usr/bin/python3 replay_gate.py --repository-root PATH --output-root NEWDIR.
Only NEWDIR is written. Git is allowlisted read-only. All full streams survive.
Semantic checks are explicit necessary-condition controls, not proof checkers.
"""
import argparse,datetime,hashlib,json,os,shutil,subprocess,sys,traceback
from pathlib import Path,PurePosixPath
sys.dont_write_bytecode=True
AR=Path('draft_pr_publication_program_20260930/audits/pr37_3009')
PIN_MANIFEST='ca440e7d4f378db294256e3d9a7a7b3f4e5344df562db9a2c4bb5092952dd2de'
PIN_DEPS='978f8e80fbccc453ec027c428414b6e7420df0c392d3d1c669df91a66f72b263'
PIN_ROOT='b4d2aea15afe6fa07d5614198404ee35d5dd1ddcfb11e1aaef8884d3244de6c6'
PY='/usr/bin/python3'
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def require(v,m):
 if not v:raise AssertionError(m)
def safe(s):
 p=PurePosixPath(s);require(not p.is_absolute() and '..' not in p.parts and str(p)==s and '\\' not in s,'unsafe path');return p
def regular(p):
 require(p.is_file() and not p.is_symlink(),'nonregular member: '+str(p))
def inventory(packet,expected_digest=None):
 regular(packet/'MANIFEST.json');m=load(packet/'MANIFEST.json')
 if expected_digest:require(sha((packet/'MANIFEST.json').read_bytes())==expected_digest,'manifest pin')
 require(m['self_excluded']==['MANIFEST.json'] and m['files_count']==96==len(m['files']),'strict packet schema')
 paths=[r['path']for r in m['files']];require(len(set(paths))==len(paths),'duplicate inventory')
 actual={str(p.relative_to(packet))for p in packet.rglob('*')if p.is_file()or p.is_symlink()}
 require(actual==set(paths)|{'MANIFEST.json'},'unlisted or missing packet member')
 for r in m['files']:
  safe(r['path']);p=packet/r['path'];regular(p)
  require(all(not q.is_symlink()for q in p.parents),'symlink ancestor')
  b=p.read_bytes();require(len(b)==r['bytes']and sha(b)==r['sha256'],'member bytes: '+r['path'])
 return m
def dependencies(packet,audit):
 p=packet/'CURRENT_PROOF_DEPENDENCIES.json';require(sha(p.read_bytes())==PIN_DEPS,'dependency document pin');d=load(p)
 require(d['dependency_anchor_repository_relative']==str(AR)and len(d['files'])==443,'dependency anchor/count')
 require(d['family_member_counts']=={'planar_fixed_continuum_family':10,'primary_scope_family':17,'recurrence_orientation_family':21},'family closure counts')
 seen=set();rows=[]
 for r in d['files']:
  safe(r['path']);require(r['path']not in seen,'duplicate dependency');seen.add(r['path']);p=audit/r['path'];regular(p)
  b=p.read_bytes();require(len(b)==r['bytes']and sha(b)==r['sha256'],'dependency changed: '+r['path']);rows.append({'path':r['path'],'bytes':len(b),'sha256':sha(b),'role':r['role'],'at':utc()})
 require(sha((packet/'root_verification/ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json').read_bytes())==PIN_ROOT,'root receipt pin')
 return rows
def semantic(packet,audit,queue):
 """Independent necessary semantic checks; human proof reasoning is sealed separately."""
 s=load(packet/'source_record.json');p=load(packet/'pinned_problem.json');f=load(packet/'pinned_importer_prior_fallback.json')
 require(s==p==load(audit/'pinned_problem.json'),'literal source semantic substitution')
 require(s['id']==3009 and s['problem_number']=='KP-5.2'and f=={},'wrong source or invented prior report')
 require((json.dumps(s,indent=2)+'\n').encode()==(packet/'source_record.json').read_bytes(),'historical ASCII serialization')
 sr=load(packet/'CURRENT_SOURCE_SERIALIZATION_RECEIPT.json');require(sr['full_JSON_content_equal']is True and sr['BYTE_equal']is False,'serialization distinction')
 require((packet/'source_record.json').read_bytes()!=(packet/'pinned_problem.json').read_bytes(),'two serializations really differ')
 turns=load(packet/'turns.json');require(turns==load(audit/'source_snapshot/turns.json'),'original ledger changed')
 require(turns['substantive_turns_used']==1 and turns['turn_limit']==5 and turns['outcome']=='unsolved'and[x['turn']for x in turns['responses']]==[1],'1/5 accounting')
 for name in ['status.json','readiness.json']:
  x=load(packet/name);require(x['exact_target']==p['statement']and not x['full_problem_solved']and not x['positive_novelty_claim'],'full/novel claim inflation')
  require(x['budget']['cumulative_attempts']=='1/5'and x['budget']['new_substantive_attempts']==0 and x['budget']['verification_attempts']==0,'budget inflation')
  require(x['current_model']is None and x['current_reasoning_effort']is None and x['current_deadline_utc']is None,'historical runtime promoted to current')
  require(x['source_qualification'].endswith('The printed 1998 disk passage remains unverified.'),'source priority promotion')
  require(not x['native_historical_readiness_or_proof_event_claimed'],'fabricated native event')
 native=load(packet/'CURRENT_NATIVE_HISTORICAL_STATE.json');require(len(native['states'])==2 and all(v['entire_object']=={}and not v['target_entry_present']for v in native['states'].values()),'native empty states')
 text=(packet/'PARTIAL.md').read_text()
 require('has exactly two fixed points.'in text and 'has exactly three fixed points.'not in text,'sphere theorem statement corrupted')
 require('sequence $n_j\\to+\\infty$'in text and 'one finite constant $D$'in text,'return exponents/common bound omitted')
 require('compact-open recurrence' in text and 'not uniform Euclidean convergence' in text,'recurrence topology weakened')
 require('more than $6D$ apart' in text and 'No claim that the intermediate maps are homeomorphisms' in text,'separation/proper homotopy prerequisites')
 require('The printed 1998 disk passage has not been directly verified.'in text,'unread printed source promoted')
 require('complete target remains unresolved' in text and 'No new discovery' in text,'partial promoted to full/novel')
 patch=load(packet/'CURRENT_PARTIAL_SOURCE_PATCH_RECEIPT.json');raw=(packet/'original_archive/PARTIAL.md').read_bytes()
 require(patch['replacement_count']==3 and len(patch['replacements'])==3,'source-only patch count')
 for r in patch['replacements']:
  a,b=r['before'].encode(),r['after'].encode();require(raw.count(a)==1,'patch exact preimage');raw=raw.replace(a,b,1)
 require(raw==(packet/'PARTIAL.md').read_bytes(),'unrecorded mathematical/source proof edit')
 sm=load(audit/'snapshot_manifest.json')
 for r in sm['files']:require((packet/'original_archive'/r['path']).read_bytes()==(audit/'source_snapshot'/r['path']).read_bytes(),'archive preservation')
 q=load(packet/'CURRENT_QUEUE_PATCH.json');require(q['column_count']==12 and q['allowed_named_changes']==['Status','Turns','Findings'],'queue schema')
 require(sha(queue)==q['whole_queue_preimage_sha256']and queue.count(q['row_before'].encode())==1,'queue preimage guard')
 before=q['row_before'].split('|');after=q['row_prospective'].split('|');require(len(before)==len(after)==14,'12-column row')
 require([i for i in range(14)if before[i]!=after[i]]==[8,9,11],'unrelated queue/Chat/DOI mutation')
 require(before[8].strip()=='queued'and before[9].strip()=='0/5'and after[8].strip()=='unsolved'and after[9].strip()=='1/5','queue outcome/turns')
 prospective=queue.replace(q['row_before'].encode(),q['row_prospective'].encode(),1)
 require(sha(prospective)==q['whole_queue_prospective_sha256'],'prospective queue exact bytes')
 return {'source_semantic_equal':True,'source_BYTE_equal':False,'budget':'1/5','new_attempts':0,'native_states_empty':True,'scope':'Explicit necessary controls and manual sealed theorem application; no automatic mathematical proof certificate.'}
def rehash(packet):
 m=load(packet/'MANIFEST.json')
 for r in m['files']:
  b=(packet/r['path']).read_bytes();r.update(bytes=len(b),sha256=sha(b))
 save(packet/'MANIFEST.json',m)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repository-root',type=Path,required=True);ap.add_argument('--output-root',type=Path,required=True);a=ap.parse_args()
 require(sys.flags.optimize==0,'assertions must be enabled');repo=a.repository_root.resolve();out=a.output_root.resolve();require(not out.exists(),'fresh output root required');out.mkdir(parents=True)
 audit=repo/AR;packet=audit/'reviewed_candidate';runs=[];checks=[];status='FAIL';private=out/'tmp/private_repository';support=out/'support';support.mkdir();ledger=[]
 def run(label,argv,cwd,env=None,expect=0):
  started=utc();cp=subprocess.run(list(map(str,argv)),cwd=cwd,capture_output=True,env=env or os.environ.copy(),timeout=180)
  r={'label':label,'argv':list(map(str,argv)),'cwd':str(cwd),'at':started,'exit':cp.returncode}
  for ch in ['stdout','stderr']:
   data=getattr(cp,ch);p=support/(label+'.'+ch);p.write_bytes(data);r[ch]={'path':str(p.relative_to(out)),'bytes':len(data),'sha256':sha(data)}
  runs.append(r);save(out/'RUNS.json',runs)
  if label=='actual_closed_collector':
   inner=private/AR
   if (inner/'new_actual_collector_support').exists():shutil.copytree(inner/'new_actual_collector_support',support/'complete_closed_collector_streams')
   if (inner/'NEW_ACTUAL_COLLECTOR.json').exists():shutil.copy2(inner/'NEW_ACTUAL_COLLECTOR.json',support/'NEW_ACTUAL_COLLECTOR.json')
  require(cp.returncode==expect,'unexpected exit: '+label);return cp
 try:
  m=inventory(packet,PIN_MANIFEST);deps=dependencies(packet,audit);queue=(repo/'unsolved_math_prioritization/QUEUE.md').read_bytes();checks.append(semantic(packet,audit,queue))
  for r in m['files']:
   p=packet/r['path'];b=p.read_bytes();mode='machine full-byte/hash read'
   if p.suffix=='.json':json.loads(b);mode='machine full-JSON parse and hash; human structural review for operative receipts'
   ledger.append({'path':'reviewed_candidate/'+r['path'],'at':utc(),'sha256':sha(b),'bytes':len(b),'read_kind':mode})
  ledger.extend(deps);save(out/'READ_LEDGER.json',ledger)
  require(run('live_branch',[PY,'-c','import subprocess;print(subprocess.check_output(["git","branch","--show-current"]).decode(),end="")'],repo).stdout==b'main\n','main branch')
  pins=load(audit/'root_replay_execution_revision/INPUT_PINS.json');rb=load(audit/'ROOT_DATED_REPLAY_INPUT_REBASE.json');overrides={r['path']:r for r in rb['files']}
  copies={str(AR/r['path']):r for r in deps}
  for r in pins['inputs']:copies[r['path']]=overrides.get(r['path'],r)
  for f in pins['families'].values():
   for r in f['members']+[f['manifest']]:copies[r['path']]=r
  for rel in ['root_replay_execution_revision/INPUT_PINS.json','root_replay_execution_revision/capture_runner.py','root_replay_execution_revision/collect_root_replays.py','ROOT_DATED_REPLAY_INPUT_REBASE.json']:
   p=audit/rel;b=p.read_bytes();copies[str(AR/rel)]={'sha256':sha(b),'size':len(b)}
  for path,r in copies.items():
   src=repo/path;regular(src);b=src.read_bytes();require(sha(b)==r['sha256']and len(b)==r.get('bytes',r.get('size')),'transport pin: '+path)
   dst=private/path;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
  pa=private/AR
  # Exact private hierarchy needs the same ignore semantics. The symlink is
  # only accessed by a local allowlisted read-only git shim below.
  (private/'.git').symlink_to(repo/'.git',target_is_directory=True);bindir=private/'readonly_bin';bindir.mkdir()
  wrapper='#!/usr/bin/python3\nimport os,sys\nallowed={"ls-tree","cat-file","diff","show","branch","rev-parse","merge-base","check-ignore"}\nassert sys.argv[1] in allowed\nassert sys.argv[1]!="branch" or sys.argv[2:]==["--show-current"]\nos.environ["GIT_OPTIONAL_LOCKS"]="0"\nos.execv("/usr/bin/git",["/usr/bin/git",*sys.argv[1:]])\n'
  (bindir/'git').write_text(wrapper);(bindir/'git').chmod(0o755);(support/'readonly_git_wrapper.py').write_text(wrapper)
  env=dict(os.environ,PATH=str(bindir)+os.pathsep+os.environ.get('PATH',''),PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
  pp=pa/'root_replay_execution_revision/INPUT_PINS.json';before=pp.read_bytes();pdoc=load(pp);pdoc['repository_root']=str(private);save(pp,pdoc)
  shutil.copy2(pp,support/'private_INPUT_PINS.json');save(support/'INPUT_PINS_PATH_TRANSPORT.json',{'original_sha256':sha(before),'revised_sha256':sha(pp.read_bytes()),'sole_semantic_change':{'field':'repository_root','before':str(repo),'after':str(private)},'no_science_pin_changes':True})
  collector=pa/'root_replay_execution_revision/collect_root_replays.py';old=collector.read_bytes()
  needle=b"value = value.replace(str(private), str(REPO))"
  require(old.count(needle)==1,'collector path normalization preimage')
  replacement=needle+b"\n            value = value.replace(str(REPO), "+repr(str(repo)).encode()+b")"
  changed=old.replace(needle,replacement,1)
  direct=b"execution['stderr_tail'].replace(str(private), str(REPO))"
  require(changed.count(direct)==1,'collector symmetric path normalization preimage')
  changed=changed.replace(direct,b"normalize(execution['stderr_tail'])",1)
  runtime=b"str(AUDIT/FAMILIES[2]/'tmp/replay_env/bin/python')"
  runtime_new=("str(Path("+repr(pins['repository_root'])+")/"+repr(str(AR))+"/FAMILIES[2]/'tmp/replay_env/bin/python')").encode()
  require(changed.count(runtime)==1,'collector historical runtime path preimage');changed=changed.replace(runtime,runtime_new,1);collector.write_bytes(changed)
  wrapperfile=pa/'reproduce_root_closed_families.py';originalwrapper=wrapperfile.read_bytes();require(originalwrapper.count(sha(old).encode())==1,'wrapper collector hash preimage');wrapperfile.write_bytes(originalwrapper.replace(sha(old).encode(),sha(changed).encode(),1))
  shutil.copy2(collector,support/'executed_path_transport_collector.py');shutil.copy2(wrapperfile,support/'executed_path_transport_entrypoint.py')
  save(support/'COLLECTOR_PATH_TRANSPORT_REVISION.json',{'original_collector_sha256':sha(old),'revised_collector_sha256':sha(changed),'replacements':[{'before':needle.decode(),'after':replacement.decode()},{'before':direct.decode(),'after':"normalize(execution['stderr_tail'])"},{'before':runtime.decode(),'after':runtime_new.decode()}],'original_wrapper_sha256':sha(originalwrapper),'revised_wrapper_sha256':sha(wrapperfile.read_bytes()),'purpose':'Restore original repository absolute paths symmetrically and preserve its documented historical runtime-path normalization for full dated receipt comparison after nested private hierarchy transport; every comparison remains equality, no failure outcome excluded.'})
  run('actual_closed_collector',[PY,pa/'reproduce_root_closed_families.py','--hamilton-complete-three-page-proof-read-by-root','--recurrence-closure-manifest',pa/'RECURRENCE_FAMILY_ROOT_CLOSURE.json','--root-dated-input-rebase-manifest',pa/'ROOT_DATED_REPLAY_INPUT_REBASE.json','--output',pa/'NEW_ACTUAL_COLLECTOR.json','--support-directory',pa/'new_actual_collector_support'],private,env)
  fresh=load(pa/'NEW_ACTUAL_COLLECTOR.json');require(fresh['status']=='PASS'and len(fresh['actual_outer_program_runs'])==9 and fresh['authored_members_verified_before_and_after']==48,'actual collector incomplete')
  # The flag is an inherited interface: it refers to an already recorded root
  # source-read attestation, not a claim that this worker is root.
  save(support/'COLLECTOR_ATTESTATION_SCOPE.json',{'flag_origin':'Unchanged inherited collector requires root-only attestation flag. Original root attestation is pinned input; this worker independently read Hamilton primary proof. No new attestation by root is fabricated.'})
  nested=[p for p in (support/'complete_closed_collector_streams').rglob('nested_runs.json')];nested_count=sum(len(load(p))for p in nested);require(nested_count==82,'nested actual execution count');checks.append({'actual_outer_runs':9,'actual_nested_runs':82,'all48_closed_members_unchanged':True})
  # Independent original baselines, completely compared rather than count-only.
  base=out/'tmp/baseline';shutil.copytree(packet/'original_archive',base)
  for label,code,receipt,n in [('original31','check_controls.py','check_results.json',31),('original8462','independent_review/independent_checks.py','independent_review/independent_results.json',8462)]:
   saved=(packet/'original_archive'/receipt).read_bytes();cp=run(label,[PY,base/code],base,env);generated=(base/receipt).read_bytes();j=json.loads(generated)
   require(generated==saved and j==json.loads(saved)and j['passed']==len(j['checks'])==n and j['failed']==0,'complete original receipt differs')
   wanted=saved if n==31 else (json.dumps({k:v for k,v in j.items()if k!='checks'},indent=2)+'\n').encode();require(cp.stdout==wanted and cp.stderr==b'','actual stdout interface mismatch')
   dst=support/(label+'.generated.json');dst.write_bytes(generated);checks.append({'label':label,'complete_BYTE_equal':True,'complete_JSON_equal':True,'stdout_interface':'full receipt'if n==31 else'metadata only','checks':n})
  # Material code corruption must fail for its mathematics, not missing imports.
  for label,code,old,new in [('bad_embedding','check_controls.py','2*x[0],2*x[1]','3*x[0],2*x[1]'),('bad_vectors','independent_review/independent_checks.py','i*i+j*j<=4','i*i+j*j<=8')]:
   dest=out/'tmp'/label;shutil.copytree(packet/'original_archive',dest);p=dest/code;t=p.read_text();require(t.count(old)==1,'code mutation preimage');p.write_text(t.replace(old,new));shutil.copy2(p,support/(label+'.executed.py'))
   cp=run(label,[PY,p],dest,env,1);require(b'AssertionError'in cp.stderr and b'ModuleNotFoundError'not in cp.stderr,'nonmaterial code failure');checks.append({'material_code_rejection':label,'exit':1})
  # Rehashing every member does not repair false source/proof/accounting claims.
  cases=[('false_fixedpoint_count','PARTIAL.md',lambda t:t.replace('has exactly two fixed points.','has exactly three fixed points.')),('false_literal_bound','pinned_problem.json',lambda t:t.replace('uniformly bounded in diameter','not bounded in diameter')),('false_turn_budget','turns.json',lambda t:t.replace('"substantive_turns_used": 1','"substantive_turns_used": 6')),('false_full_solution','status.json',lambda t:t.replace('"full_problem_solved": false','"full_problem_solved": true')),('false_current_model','readiness.json',lambda t:t.replace('"current_model": null','"current_model": "gpt-6-astra"')),('false_printed_priority','status.json',lambda t:t.replace('The printed 1998 disk passage remains unverified.','The printed 1998 disk passage was directly verified.')),('false_queue_DOI','CURRENT_QUEUE_PATCH.json',lambda t:t.replace('"row_prospective": "| 59 |','"row_prospective": "| 60 |'))]
  for label,file,mutate in cases:
   dest=out/'tmp'/label;shutil.copytree(packet,dest);p=dest/file;old=p.read_text();new=mutate(old);require(new!=old,'prose mutation preimage');p.write_text(new);rehash(dest);inventory(dest)
   shutil.copy2(p,support/(label+'.mutated'+p.suffix));save(support/(label+'.rehashed_manifest.json'),load(dest/'MANIFEST.json'))
   rejected=False
   try:semantic(dest,audit,queue)
   except AssertionError as e:rejected=True;save(support/(label+'.rejection.json'),{'at':utc(),'detector':'independent semantic necessary-condition controls after valid rehash','reason':str(e),'changed_file':file,'mutation_passes_inventory':True})
   require(rejected,'semantic mutation accepted: '+label);checks.append({'semantic_rejection':label,'valid_rehashed_inventory':True})
  for label,mutate in [('unlisted_nested',lambda d:(d/'nested').mkdir()or(d/'nested/PARTIAL.md').write_text('unlisted')),('missing_member',lambda d:(d/'CURRENT_CONTEXT.md').unlink()),('byte_tamper',lambda d:(d/'PARTIAL.md').write_bytes((d/'PARTIAL.md').read_bytes()+b'\n'))]:
   dest=out/'tmp'/label;shutil.copytree(packet,dest);mutate(dest);rejected=False
   try:inventory(dest,PIN_MANIFEST)
   except AssertionError as e:rejected=True;save(support/(label+'.rejection.json'),{'reason':str(e),'at':utc()})
   require(rejected,'inventory mutation accepted');checks.append({'inventory_rejection':label})
  # The entire private administrative builder is actually run on frozen inputs.
  # The collector transport changes are execution-only. Restore all three
  # exact sealed dependency bytes before challenging the administrative build.
  collector.write_bytes(old);wrapperfile.write_bytes(originalwrapper);pp.write_bytes(before)
  save(support/'PRE_BUILDER_TRANSPORT_RESTORATION.json',{'collector_sha256':sha(collector.read_bytes()),'wrapper_sha256':sha(wrapperfile.read_bytes()),'input_pins_sha256':sha(pp.read_bytes()),'exact_original_dependency_bytes_restored':True})
  build=pa/'current_preparation_family/prepare_current_packet.py';br=load(packet/'CURRENT_BUILD_RECEIPT.json')
  argv=[PY,build,'--execute','--third-manifest-sha256','e03a12707dc6b91f40be954a274657f2b7456feb8dd75a70e77c40630fa76734','--third-member-count','21','--root-receipt-sha256',PIN_ROOT,'--root-replay-script-sha256',br['actual_root_family_replay_script_sha256'],'--root-scope-certificate-sha256',br['root_scope_certificate_sha256'],'--root-support-manifest','ROOT_REPLAY_SUPPORT_MANIFEST_V2.json','--root-support-manifest-sha256',br['optional_root_support']['manifest_sha256']]
  run('private_actual_builder',argv,private,env);newpacket=pa/'reviewed_candidate';inventory(newpacket);semantic(newpacket,pa,queue)
  expected=load(packet/'MANIFEST.json');actual=load(newpacket/'MANIFEST.json');delta=[]
  for e,c in zip(expected['files'],actual['files']):
   require(e['path']==c['path'],'builder topology differs')
   if e!=c:delta.append({'path':e['path'],'historical':e,'actual':c})
  allowed={'CURRENT_BUILD_RECEIPT.json','CURRENT_PROOF_DEPENDENCIES.json','CURRENT_QUEUE_PATCH.json','MANIFEST.json','RESEARCH_LOG.md','readiness.json','status.json'}
  require(all(d['path']in allowed for d in delta),'nonclock administrative builder difference')
  save(support/'BUILDER_FULL_DIFF.json',{'differences':delta,'policy':'Only explicit dated output fields differ; all other complete96 member bytes equal. This comparison does not exclude arbitrary numbers/claims.'})
  checks.append({'builder_actual_replay':True,'complete96_structural_match':True,'explicit_dated_differences':len(delta)})
  inventory(packet,PIN_MANIFEST);dependencies(packet,audit);semantic(packet,audit,(repo/'unsolved_math_prioritization/QUEUE.md').read_bytes())
  status='PASS'
 except BaseException as e:
  save(out/'FAILURE.json',{'at':utc(),'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()})
 finally:
  save(out/'RESULT.json',{'at':utc(),'status':status,'manifest_pin':PIN_MANIFEST,'dependency_pin':PIN_DEPS,'root_evidence_pin':PIN_ROOT,'original_attempts':'1/5','new_substantive_attempts':0,'audit_attempts_added':0,'checks':checks,'runs':runs,'no_verdict_transfer':True,'limitations':'Actual computations/provenance controls; imported topology and manual mathematical audit remain separate.'})
  # Private foreign/raw copies and every mutation scratch tree are removed.
  # Retained support contains first-party code, full streams and JSON receipts.
  shutil.rmtree(out/'tmp',ignore_errors=True)
 print(json.dumps({'status':status,'output':str(out),'outer_subprocess_runs':len(runs),'checks':len(checks)}))
 if status!='PASS':raise SystemExit(1)
if __name__=='__main__':main()
