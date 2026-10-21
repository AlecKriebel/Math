from pathlib import Path,PurePosixPath
import json,hashlib,subprocess,datetime,re,zipfile
home=Path(__file__).resolve().parent; p=home/'extracted/congestion-fragmentation-verification'; repo=Path('/Users/alec/Documents/Math')
sha=lambda d:hashlib.sha256(d).hexdigest()
checks=[]
manifest_paths=[p/'MANIFEST.json',p/'candidate/PUBLIC_MANIFEST.json',p/'candidate/turns/turn_01/FREEZE_MANIFEST.json',p/'candidate/turns/turn_02/FREEZE_MANIFEST.json',p/'reviews/flow_adversary_01/MANIFEST.json',p/'reviews/probability_adversary_01/MANIFEST.json',p/'reviews/priority_scope_adversary_01/MANIFEST.json',p/'support-manifest.json']
for m in manifest_paths:
 d=json.loads(m.read_text()); fs=d['files']; rows=fs if isinstance(fs,list) else [dict(path=k,**v) for k,v in fs.items()]; count=0
 for r in rows:
  q=m.parent/r['path']; b=q.read_bytes(); assert len(b)==r['bytes'] and sha(b)==r['sha256'],str(q)
  if 'git_blob_sha' in r: assert hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==r['git_blob_sha']
  count+=1
 checks.append({'manifest':str(m.relative_to(p)),'payloads_verified':count})
outer=json.loads((p/'MANIFEST.json').read_text())['files']; actual={str(q.relative_to(p)) for q in p.rglob('*') if q.is_file()}; assert actual==set(outer)|{'MANIFEST.json'}
assert (p/'paper/main.tex').read_bytes()==(home/'bound_release/congestion-fragmentation.tex').read_bytes()
assert (p/'publication-metadata.json').read_bytes()==(home/'bound_release/zenodo-deposit.json').read_bytes()
bind=json.loads((p/'candidate-binding.json').read_text()); snap=json.loads((p/'SOURCE_SNAPSHOT.json').read_text()); assert sha((p/'SOURCE_SNAPSHOT.json').read_bytes())==bind['source_snapshot_sha256']
head=bind['source_head']; base=bind['source_comparison_base']; assert head=='3705c5102b58c48e29991c61771978bf756a62e7' and base=='28519ba7648c003d4e1212dd315005c93a21a9d6'
orig=[]
for r in bind['files']:
 b=(p/'candidate'/r['path']).read_bytes(); gb=subprocess.run(['git','show',head+':'+r['repository_path']],cwd=repo,capture_output=True,check=True).stdout
 assert b==gb and len(b)==r['bytes'] and sha(b)==r['sha256']; assert hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==r['git_blob']
 orig.append(r['repository_path'])
changed=subprocess.run(['git','diff','--name-only',base,head],cwd=repo,capture_output=True,text=True,check=True).stdout.splitlines(); assert set(changed)==set(orig)|{'unsolved_math_prioritization/QUEUE.md'}
qd=subprocess.run(['git','diff','--unified=0',base,head,'--','unsolved_math_prioritization/QUEUE.md'],cwd=repo,capture_output=True,text=True,check=True).stdout
lines=[s for s in qd.splitlines() if s[:1] in ('+','-') and s[:3] not in ('+++','---')]; assert len(lines)==2 and all('| 9700002 / AMR-096-0002 |' in s for s in lines); assert '| claimed_solved | 2/5 |' in lines[1]
previous=[]
expected={'package_adversary_01':'41e55632457b202827563e7cf3af5cb773ed62c5d4e6e0c34b11746d86308bae','package_adversary_02':'e31799ef60bd34134d743218e8e7f420cf6cc1531a9f56415456b7c9ab2892b6'}
for n,h in expected.items():
 m=home.parent/n/'OUTPUT_MANIFEST.json'; assert sha(m.read_bytes())==h; d=json.loads(m.read_text()); fs=d['files']; rows=fs if isinstance(fs,list) else [dict(path=k,**v) for k,v in fs.items()]
 for r in rows:
  b=(m.parent/r['path']).read_bytes(); assert len(b)==r['bytes'] and sha(b)==r['sha256'],r['path']
 previous.append({'review':n,'sha256':h,'sealed_files_verified':len(rows)})
# Inventory privacy screen: every payload decodes as text; only authored local evidence included.
secret=re.compile(r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|ya29\.[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{24,}|Authorization:\s*Bearer\s+\S+',re.I)
hits=[]; nottext=[]; emailhits=[]
for f in p.rglob('*'):
 if f.is_file():
  b=f.read_bytes()
  try: t=b.decode('utf-8')
  except UnicodeError: nottext.append(str(f.relative_to(p))); continue
  for x in secret.finditer(t): hits.append({'path':str(f.relative_to(p)),'offset':x.start(),'matched_type':'credential pattern'})
  if re.search(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b',t,re.I): emailhits.append(str(f.relative_to(p)))
assert not hits and not nottext
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifests':checks,'outer_exact_set':True,'members':len(actual),'source_and_metadata_exact':True,'originals_actual_Git_object_matches':len(orig),'head':head,'base':base,'changed_paths':len(changed),'own_queue_only_status_claimed_2_of_5':True,'previous_complete_seals':previous,'all_payloads_UTF8':True,'credential_pattern_hits':hits,'email_pattern_files_for_manual_review':emailhits,'private_source_bodies_included':False}
(home/'CUSTODY_AND_PRIVACY.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))
