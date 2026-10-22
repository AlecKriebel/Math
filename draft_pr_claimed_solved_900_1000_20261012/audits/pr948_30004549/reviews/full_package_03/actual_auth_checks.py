from pathlib import Path
import json,hashlib,stat,datetime,subprocess,zipfile,io,re
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr948_30004549';D=A/'preprint';O=A/'reviews/full_package_03'
def need(x,s):
 if not x:raise RuntimeError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p,v):
 b=p.read_bytes();need(len(b)==v['bytes'] and sha(b)==v['sha256'],str(p))
core=P/'accept_pr948.py';raw=core.read_bytes();need(sha(raw)=='3be81538c4e17e6b220208992a8d56422218f37773f84c8a690a4ab10a41d823','core')
N={'__name__':'_independent_readonly_auth_','__file__':str(core)};exec(compile(raw,str(core),'exec',dont_inherit=True,optimize=0),N)
context=N['capture_inventory']('500866df6a5c92a38f133dbe7088da956bc52b54ade02b3fa258a07c3af4e002')
current=N['freeze_check']((D/'FREEZE.json').read_bytes(),'1bbfc6c554984f8f8a4a6c467c92ff6e5e87f22b2b79d2d9d91766bf0822e68c',context)
B=D/'reviewed_candidates/candidate01';pres=B/'PRESERVATION.json';need(sha(pres.read_bytes())=='dfb4a95b998f4b200ba8755fefe104126383667ee6ea927d338d144d396a2535','preservation')
pr=json.loads(pres.read_text())
for n,v in pr['files'].items():pin(B/n,v)
old=json.loads((B/'FREEZE.json').read_text());need(sha((B/'FREEZE.json').read_bytes())=='65add90a6ac3a539cacdc41152cea5828c95cad95608a95e2dad054341a37c02','old freeze')
for n,v in old['files'].items():pin(B/n,v)
for n,v in old['evidence_files'].items():pin(B/'evidence'/n,v);need(stat.S_IMODE((B/'evidence'/n).stat().st_mode)==0o600,'private mode')
need(stat.S_IMODE((B/'evidence').stat().st_mode)==0o700,'private root mode')
oldinv=json.loads((B/'OPERATIONS_INVENTORY.json').read_text())
for n,v in oldinv['files'].items():pin(B/'operations'/n,v)
actual_old=N['freeze_check']((B/'FREEZE.json').read_bytes(),'65add90a6ac3a539cacdc41152cea5828c95cad95608a95e2dad054341a37c02',context,B,historical=True)
Q=A/'reviews/full_package_01';qraw=(Q/'MANIFEST.json').read_bytes();need(sha(qraw)=='348cf0e067b1a0532cb79172510c247ea3d079dcb315dab899143dc53dca0c66','old review seal');qr=json.loads(qraw);need(set(qr['files'])==set(qr['explicit_public_allowlist']),'review allowlist')
for n,v in qr['files'].items():pin(Q/n,v)
res=json.loads((Q/'RESULT.json').read_text());need(res['clean_for_preprint'] is False and [v['id'] for v in res['required_issues']]==['R948-FULL01-R01'] and res['inherited_finding_dispositions']['PF01-R04']['verified'] is False and res['inherited_finding_dispositions']['R948-WORKFLOW-ROOT-01']['verified'] is False,'old honest adverse preserved')
originals=N['original_check']();pins=res['candidate_pins'];old_auth={}
for name in ('AUTHENTICATION_START.json','AUTHENTICATION_END.json'):
 ok,t=N['review_authentication'](json.loads((Q/name).read_text()),pins,actual_old,originals);need(ok,'old auth');old_auth[name]=t.isoformat()
ok,t=N['review_cold'](json.loads((Q/'COLD_REPLAY.json').read_text()),pins,actual_old,B);need(ok,'old cold');old_auth['COLD_REPLAY.json']=t.isoformat()
parent=subprocess.check_output(['git','rev-parse','refs/heads/main'],cwd=R,text=True).strip();source=N['source_gate'](parent);native=N['native_safety'](parent)
wrappers={}
for name,action in [('merge_pr948.py','merge'),('run_pr948_zenodo.py','zenodo'),('append_pr948_tracker.py','tracker'),('update_pr948_publication_ledger.py','native'),('finalize_pr948_and_gate_next.py','finalize')]:
 s=(P/name).read_text();body=s[:s.rindex("if __name__=='__main__':")];need(s[s.rindex("if __name__=='__main__':"):].strip()=="if __name__=='__main__':\n    entry('"+action+"')",name+' selector');wrappers[name]={'sha256':sha(s.encode()),'common_body_sha256':sha(body.encode()),'action':action}
need(len(set(r['common_body_sha256'] for r in wrappers.values()))==1,'wrapper common source')
# Independent original7 ZIP closure/mode/hash against immutable author mirrors and external manifest.
orig=A/'original/unsolved_math_prioritization/attempts/30004549';ext=json.loads((orig/'ANTI_INVARIANT_30004549_R3_AUTHOR_EXTERNAL_MANIFEST.json').read_text());zraw=(orig/ext['archive']['filename']).read_bytes();need(len(zraw)==ext['archive']['bytes'] and sha(zraw)==ext['archive']['sha256'],'original zip')
expected={e['path']:e for e in ext['files']};members={}
with zipfile.ZipFile(io.BytesIO(zraw)) as z:
 infos=z.infolist();need(len(infos)==7 and set(i.filename for i in infos)==set(expected),'7member closure')
 for i in infos:
  need(not i.is_dir() and i.create_system==3 and i.external_attr>>16 in (0o644,0o100644) and i.filename==str(Path(i.filename)) and '..' not in Path(i.filename).parts and not Path(i.filename).is_absolute() and not i.flag_bits&1 and i.file_size<=16384,'7member metadata')
 for i in infos:
  b=z.read(i);need(b==(orig/'author'/i.filename).read_bytes() and len(b)==expected[i.filename]['bytes'] and sha(b)==expected[i.filename]['sha256'],'7member bytes');members[i.filename]={'bytes':len(b),'sha256':sha(b),'archive_mode':'100644','disk_mode':oct(stat.S_IMODE((orig/'author'/i.filename).stat().st_mode))}
obj={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','actual_current_freeze_check':True,'actual_historical_freeze_check':True,'historical_preservation_sha256':sha(pres.read_bytes()),'historical_preservation_files':len(pr['files']),'old_candidate_frozen_files':len(old['files']),'old_candidate_evidence_files':len(old['evidence_files']),'old_candidate_operations':len(oldinv['files']),'old_review_manifest_sha256':sha(qraw),'old_review_payloads':len(qr['files']),'old_review_authentication_and_cold':old_auth,'old_adverse_and_false_dispositions_unchanged':True,'source_gate_cached_local_main_only':source,'native_safety_cached_local_main_only':native,'source_limit':'No fetch performed; cached local-main source/native check is not a fresh remote-main operational acceptance gate. Current absent native records do not establish historical author turn count.','wrappers':wrappers,'original7_members':members,'private_snapshot_contents_copied_to_public_review':False,'real_action_functions_called':False}
(O/'ACTUAL_AUTH_CHECKS.json').write_text(json.dumps(obj,indent=2)+'\n');print(json.dumps({k:v for k,v in obj.items() if not isinstance(v,dict)}))
