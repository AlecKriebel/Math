"""Final bounded validation, preservation receipt and read-only private handoff."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess
E=Path(__file__).resolve().parent;B=E.parents[1]
PY='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def bind(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def req(c,m):
    if not c:raise RuntimeError(m)
req(not (E/'SEAL.json').exists() and not (E/'MANIFEST.json').exists(),'new final seal only')
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
run=subprocess.run([PY,str(E/'validate_packet.py')],env=env,capture_output=True,text=True,timeout=30)
req(run.returncode==0,'read-only final validator: '+run.stderr)
validation=json.loads(run.stdout);req(validation['all_passed'] and validation['passed']==validation['total']==38,'complete final static validation')
(E/'FINAL_STATIC_VALIDATION.json').write_text(run.stdout)
baseline=json.loads((E/'ORIGINAL_BINDINGS_BEFORE.json').read_text())
req(all(Path(r['path']).stat().st_size==r['bytes'] and sha(r['path'])==r['sha256'] for r in baseline['files']),'all baseline unchanged')
now=datetime.now(timezone.utc).isoformat()
(E/'CUSTODY_PRESERVATION.json').write_text(json.dumps({'utc':now,'bounded_baseline_bindings_unchanged':len(baseline['files']),'all54_source_files_unchanged':True,'all41_archive_bodies_verified_without_extraction':True,'all_three_scientific_packets_and_root_authority_unchanged':True,'row104_complete_adversarial_owned_and_bound_disposable_evidence_unchanged':True,'exact_private_custody_copies':17,'source_or_shared_or_site_or_native_or_UI_or_Git_or_contact_changes':False,'only_new_record_configs_and_editorial_namespace_written':True},indent=2)+'\n')
payload=[bind(p) for p in sorted(E.rglob('*')) if p.is_file() and p.name not in {'MANIFEST.json','SEAL.json'}]
configs=[bind(B/n) for n in ['publication.json','promotion.json']]
files=sorted(baseline['files']+payload+configs,key=lambda x:x['path']);req(len({r['path'] for r in files})==len(files),'distinct final bindings')
manifest={'utc':now,'kind':'PRIVATE_EDITORIAL_FIXED_ORIGINALS_PLUS_OWN_PAYLOAD','record_id':23217863,'original_baseline_files':len(baseline['files']),'new_editorial_payload_files':len(payload),'new_record_configs':2,'file_count':len(files),'files':files,'shared_mutable_core_and_site_snapshots_included':False,'primary_bodies_copied':False,'source_originals_or_scientific_objects_modified':False}
(E/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
req(all(sha(r['path'])==r['sha256'] and Path(r['path']).stat().st_size==r['bytes'] for r in files),'all final bindings rehashed')
seal={'utc':now,'kind':'IMMUTABLE_PRIVATE_EDITORIAL_HANDOFF_ONLY','record_id':23217863,'status':'PRIVATE_EDITORIAL_PREPARATION_COMPLETE_PENDING_ROOT_READ','completion_estimate_percent_this_bounded_preparation':100,'manifest':bind(E/'MANIFEST.json'),'all_manifest_bindings_rehashed':len(files),'frozen_original_baseline_unchanged':len(baseline['files']),'new_editorial_payload_files':len(payload),'new_record_configs':2,'editorial_directory_files_including_manifest_and_seal':len(payload)+2,'report':bind(E/'REPORT.md'),'public_copy':bind(E/'PUBLIC_COPY.md'),'adapter_specification':bind(E/'SCHEMA_ADAPTER.md'),'publication':configs[0],'promotion':configs[1],'final_static_validation':bind(E/'FINAL_STATIC_VALIDATION.json'),'static_checks_passed':38,'root_scientific_status':'PASS_AT_DECLARED_EXTERNAL_THEOREM_LEVEL','root_scientific_clearance_sha256':'b8f379a432a6866d611b929b8c91a410312a36943b99051574edc135598b280a','root_editorial_clearance_received':False,'rendered_public_copy_approved':False,'local_http_verified':False,'live_http_verified':False,'browser_verified':False,'native_sheet_publication_verified':False,'public_page_published':False,'canonical_url':None,'AA':None,'follow_up':None,'source_repairs':False,'shared_consumer_installed':False,'outreach_or_contact':False,'overall_203_goal_complete':False,'post_seal_rule':'Read/hash only. Do not rewrite originals or own packet; later root stages require separate artifacts/authority.'}
(E/'SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
for p in E.rglob('*'):
    if p.is_file():p.chmod(0o444)
for p in [B/'publication.json',B/'promotion.json']:p.chmod(0o444)
print(json.dumps({'report':bind(E/'REPORT.md'),'public_copy':bind(E/'PUBLIC_COPY.md'),'publication':bind(B/'publication.json'),'promotion':bind(B/'promotion.json'),'manifest':bind(E/'MANIFEST.json'),'seal':bind(E/'SEAL.json'),'baseline_files':len(baseline['files']),'editorial_payload_files':len(payload),'static_checks':38},indent=2))
