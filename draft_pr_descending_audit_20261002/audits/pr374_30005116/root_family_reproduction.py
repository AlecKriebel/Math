"""Independently rerun sealed family programs privately; preserve full outputs."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,os,re,shutil,subprocess,sys
A=Path(__file__).resolve().parent; W=A/'tmp/root_family_reproduction';assert not W.exists();W.mkdir(parents=True)
O=A/'root_family_streams';O.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
families=['multipartite_triangle_review','cograph_review','local_rankone_review'];verified=[]
for family in families:
 p=A/family;m=json.loads((p/'PUBLIC_MANIFEST.json').read_text());entries=m.get('files',m.get('public_files',[]));assert entries
 for e in entries:
  assert '..' not in Path(e['path']).parts and not Path(e['path']).is_absolute()
  b=(p/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'],(family,e['path'])
  q=W/family/e['path'];q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
 shutil.copyfile(p/'PUBLIC_MANIFEST.json',W/family/'PUBLIC_MANIFEST.json')
 verified.append({'family':family,'members':len(entries),'manifest_sha256':sha((p/'PUBLIC_MANIFEST.json').read_bytes())})
seals=[]
p=A/families[0]
s=json.loads((p/'source_first_seal.json').read_text());v=json.loads((p/'mathematical_verdict_seal.json').read_text())
for name,digest in s['public_files'].items():assert sha((p/name).read_bytes())==digest;seals.append(f'{families[0]}/{name}')
assert sha((p/'MATHEMATICAL_VERDICT.md').read_bytes())==v['proof_sha256'];assert sha((p/'post_candidate_controls.py').read_bytes())==v['control_sha256'];seals.extend([families[0]+'/MATHEMATICAL_VERDICT.md',families[0]+'/post_candidate_controls.py'])
p=A/families[1]
for name in ['baseline_seal.sha256','verdict_seal.sha256']:
 for line in (p/name).read_text().splitlines():
  digest,member=line.split(maxsplit=1);assert sha((p/member).read_bytes())==digest;seals.append(f'{families[1]}/{member}')
p=A/families[2]
for line in (p/'pre_candidate_seal_manifest.md').read_text().splitlines():
 m=re.match(r'- (\S+) SHA256 `([0-9a-f]{64})`',line)
 if m:assert sha((p/m[1]).read_bytes())==m[2];seals.append(f'{families[2]}/{m[1]}')
mv=json.loads((p/'PUBLIC_MANIFEST.json').read_text());assert sha((p/'verdict_seal.md').read_bytes())==mv['verdict_seal_sha256'];seals.append(f'{families[2]}/verdict_seal.md')
jobs=[]
for family,names in [(families[0],['independent_controls.py','post_candidate_controls.py']),(families[1],['independent_controls.py','independent_union_gap_controls.py','independent_envelope_probe.py']),(families[2],['independent_controls.py','independent_post_candidate_controls.py','replay_relevant_author_controls.py'])]:
 for name in names:jobs.append((family,name))
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
def run(job):
 family,name=job;p=A/family;f=W/family/name
 r=subprocess.run([sys.executable,'-B',str(f)],cwd=f.parent,env=env,capture_output=True)
 label=family+'_'+name; (O/(label+'.stdout')).write_bytes(r.stdout);(O/(label+'.stderr')).write_bytes(r.stderr)
 assert r.returncode==0 and not r.stderr,(label,r.returncode,r.stderr.decode())
 if family==families[0]:
  expected=s if name=='independent_controls.py' else v
  assert sha(r.stdout)==expected['controls_stdout_sha256'] and sha(r.stderr)==expected['controls_stderr_sha256']
 elif family==families[1]:
  result={'independent_controls.py':'independent_controls_result.json','independent_union_gap_controls.py':'independent_union_gap_result.json','independent_envelope_probe.py':'independent_envelope_probe_result.json'}[name]
  assert r.stdout==(p/result).read_bytes(),label
 elif name=='replay_relevant_author_controls.py':
  got=json.loads(r.stdout);want=json.loads((p/'author_replay_results.json').read_text())
  for obj in [got,want]:obj.pop('completed_utc')
  assert got==want,label
  for i in [2,3,5]:
   assert (f.parent/f'author_turn{i}.stdout.fullstream.txt').read_bytes()==(p/f'author_turn{i}.stdout.fullstream.txt').read_bytes()==(A/f'root_original_streams/turn{i}.stdout').read_bytes()
   assert (f.parent/f'author_turn{i}.stderr.fullstream.txt').read_bytes()==b''
 else:assert r.stdout==(p/(name.replace('.py','.fullstream.txt'))).read_bytes(),label
 print(label+': PASS',flush=True)
 return {'family':family,'program':name,'exit':0,'entire_stdout_byte_exact':name!='replay_relevant_author_controls.py','entire_json_exact_except_completed_utc':name=='replay_relevant_author_controls.py','stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_empty':True}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:runs=list(pool.map(run,jobs))
primary=json.loads((A/'root_primary_source_receipt.json').read_text())['files'];known={e['sha256']:e for e in primary};sources=[]
for family in families:
 found=list((A/family/'tmp').glob('*.pdf'));assert len(found)==3
 for f in found:
  b=f.read_bytes();digest=sha(b);assert digest in known and len(b)==known[digest]['bytes']
  sources.append({'family':family,'private_file':f.name,'root_primary':known[digest]['file'],'bytes':len(b),'sha256':digest})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','workflow_percent':85,'unrestricted_discovery_percent':0,'public_manifest_members':sum(x['members'] for x in verified),'manifests':verified,'sealed_binding_instances':len(seals),'seals':seals,'programs':runs,'all_nine_fresh_family_PDFs_match_root_five_pinned_primaries':sources,'failures_preserved_in_owned_manifests_and_exclusions':True,'universal_proofs_read_and_reconstructed':'ROOT_MATHEMATICAL_RECONSTRUCTION.md','no_novelty_certification':True,'new_whole_package_gate_pending':True}
(A/'root_family_reproduction_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','families':len(families),'members':out['public_manifest_members'],'seals':len(seals),'programs':len(runs),'fresh_private_PDFs':len(sources)}))
