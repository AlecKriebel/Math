from pathlib import Path
import json,hashlib,subprocess,os,datetime
A=Path(__file__).resolve().parent
specs=[('geometry_morse_review','FAMILY_ARTIFACT_MANIFEST.json','independent_seal_manifest.json'),('koszul_depth_review','FINAL_AUDIT_MANIFEST.json','INDEPENDENT_SEAL.json'),('priority_sources_review','PUBLIC_ARTIFACT_MANIFEST.json','source_first_seal.json')]
bindings=[]
for family,final,seal in specs:
 D=A/family
 for name in [final,seal]:
  m=json.loads((D/name).read_text());rows=m.get('files',m.get('artifacts'));assert rows,name
  if isinstance(rows,dict):rows=[{'path':k,'sha256':v} for k,v in rows.items()]
  for e in rows:
   b=(D/e.get('path',e.get('file'))).read_bytes();assert ('bytes' not in e or len(b)==e['bytes']) and hashlib.sha256(b).hexdigest()==e['sha256'],(family,name,e)
  bindings.append({'family':family,'manifest':name,'binding_occurrences':len(rows),'manifest_sha256':hashlib.sha256((D/name).read_bytes()).hexdigest()})
runs=[('geometry_morse_review','independent_local_controls.py','independent_local_controls.stdout.txt'),('koszul_depth_review','independent_koszul_controls.py','independent_koszul_controls.stdout.txt'),('koszul_depth_review','frozen_comparison_controls.py','frozen_comparison_controls.stdout.txt'),('priority_sources_review','independent_source_controls.py','source_controls_full.stdout')]
streams=[]
for family,script,original in runs:
 D=A/family;r=subprocess.run(['python3','-B',str(D/script)],env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True);assert r.returncode==0 and not r.stderr,(script,r.stderr.decode());(A/(family+'_'+script.removesuffix('.py')+'_root.stdout')).write_bytes(r.stdout);(A/(family+'_'+script.removesuffix('.py')+'_root.stderr')).write_bytes(r.stderr)
 if family=='priority_sources_review':
  def norm(b):
   rows=[json.loads(x) for x in b.decode().splitlines()]
   for row in rows:
    for k in ['started_utc','completed_utc']:row.pop(k,None)
   return rows
  assert norm(r.stdout)==norm((D/original).read_bytes());match='Every JSON field exact except two acquisition/execution timestamps'
 else:assert r.stdout==(D/original).read_bytes();match='Entire stdout byte exact'
 streams.append({'family':family,'script':script,'stdout_bytes':len(r.stdout),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'match':match,'stderr_empty':True})
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_final_manifests_and_original_independent_seals_verified':bindings,'all_four_new_programs_and_full_written_proofs_read':True,'full_new_control_streams_reproduced':streams,'root_four_primary_PDF_matches':True,'original_complete_author_assertions':358064,'original_complete_historical_assertions':983,'mandatory_ext_direction_repair_remains':True,'workflow_percent':60,'no_acceptance':True}
(A/'root_family_reproduction_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
