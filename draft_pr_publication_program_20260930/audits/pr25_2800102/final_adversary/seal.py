from pathlib import Path
import json,hashlib,datetime
H=Path(__file__).resolve().parent;A=H.parent;R=A.parents[2]
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads(p.read_text())
# Refuse to seal a changed input package or changed earlier/canonical bytes.
checks=[]
def check(name,value):
 if not value:raise AssertionError(name)
 checks.append(name)
for d,mp in [('source_snapshot',A/'snapshot_manifest.json')]+[(d,A/d/'MANIFEST.json') for d in ['reviewed_candidate','primary_scope_family','complex_family','real_family','real_dependency_falsifier']]:
 for f in j(mp)['files']:
  b=(A/d/f['path']).read_bytes();check(d+'/'+f['path'],len(b)==f['bytes'] and sha(b)==f['sha256'])
for f in j(A/'reviewed_candidate/CURRENT_PROOF_DEPENDENCIES.json')['supporting_first_party_files']:
 b=(R/f['path']).read_bytes();check('dependency:'+f['path'],len(b)==f['bytes'] and sha(b)==f['sha256'])
for f in j(H/'EARLY_SEAL.json')['files']:
 b=(H/f['path']).read_bytes();check('own_early:'+f['path'],len(b)==f['bytes'] and sha(b)==f['sha256'])
v=j(H/'VERDICT.json');fg=j(H/'FINAL_GATE_RECEIPTS.json')
for p,k in [(H/'REPORT.md','report_sha256'),(H/'VERIFIED_RECONSTRUCTION.md','verified_reconstruction_sha256'),(H/'FINAL_GATE_RECEIPTS.json','final_gate_receipts_sha256')]:check('verdict:'+p.name,sha(p.read_bytes())==v[k])
for filename,key in [('state.json','canonical_state_sha256'),('history.jsonl','canonical_history_sha256')]:check('canonical:'+filename,sha((R/'unsolved_math_prioritization'/filename).read_bytes())==fg[key])
check('source_binding',sha((A/'reviewed_candidate/SOURCE_AUDIT.md').read_bytes())==v['source_audit_sha256']);check('manifest_binding',sha((A/'reviewed_candidate/MANIFEST.json').read_bytes())==v['candidate_manifest_sha256'])
selfexcluded=['MANIFEST.json','FINAL_SEAL.json'];entries=[]
for p in sorted(H.iterdir()):
 if not p.is_file() or p.name in selfexcluded:continue
 b=p.read_bytes();entries.append({'path':p.name,'bytes':len(b),'sha256':sha(b)})
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
manifest={'utc':utc,'scope':'fresh_complete_PR25_current23_adversary_first_party_only','self_excluded':selfexcluded,'excluded_runtime_or_foreign_directories':['tmp','__pycache__'],'files':entries}
(H/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
seal={'utc':utc,'verdict':'PASS','first_party_manifest_sha256':sha((H/'MANIFEST.json').read_bytes()),'first_party_entry_count':len(entries),'report_sha256':sha((H/'REPORT.md').read_bytes()),'verdict_sha256':sha((H/'VERDICT.json').read_bytes()),'early_seal_sha256':sha((H/'EARLY_SEAL.json').read_bytes()),'early_criterion_sha256':sha((H/'EARLY_CRITERION_AND_RECONSTRUCTION.md').read_bytes()),'original_head':v['original_head'],'current23_manifest_sha256':v['candidate_manifest_sha256'],'current_source_audit_sha256':v['source_audit_sha256'],'final_input_rechecks_passed':len(checks),'final_input_rechecks_failed':0,'canonical_state_sha256':fg['canonical_state_sha256'],'canonical_history_sha256':fg['canonical_history_sha256'],'all_prior_package_bytes_and_own_early_seal_preserved':True,'remote_or_current_accepted_mirror_mutation_done':False,'parent_final_integration_binding_required':True,'self_excluded_from_first_party_manifest':True}
(H/'FINAL_SEAL.json').write_text(json.dumps(seal,indent=2)+'\n');print(json.dumps(seal,indent=2))
