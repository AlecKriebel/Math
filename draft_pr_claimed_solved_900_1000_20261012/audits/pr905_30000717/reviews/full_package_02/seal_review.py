"""Seal the intentional public review artifacts; exclude raw/private/temp data."""
from pathlib import Path
import hashlib,json,datetime
HERE=Path(__file__).resolve().parent; AUDIT=HERE.parent.parent
PUBLIC=[
'.gitignore','REVIEW.md','REVIEW_RESULT.json','RESEARCH_LOG.md','prepare_review.py','fetch_sources.py','replay.py','independent_math.py','tool_attacks.py','utility_replays.py','source_metadata_check.py','seal_review.py',
'evidence/archive_inventory.json','evidence/earlier_published_source.json','evidence/fresh_source_hashes.json','evidence/frozen_before.json','evidence/frozen_after.json','evidence/independent_math.json','evidence/independent_math_optimized.json','evidence/pdfinfo.txt',
'evidence/replay_normal.stdout','evidence/replay_normal.stderr','evidence/replay_normal.json','evidence/replay_optimized.stdout','evidence/replay_optimized.stderr','evidence/replay_optimized.json',
'evidence/source_metadata_package_checks.json','evidence/standalone_compile.stdout','evidence/standalone_compile.stderr','evidence/supplemental_computation_diagnostics.json','evidence/tool_attacks.json','evidence/utility_replays.json',
'evidence/utility_verify_review.stdout','evidence/utility_verify_review.stderr','evidence/utility_seal_manifest.stdout','evidence/utility_seal_manifest.stderr','evidence/utility_computation_diagnostics.stdout','evidence/utility_computation_diagnostics.stderr','evidence/visual_compile_checks.json']
def digest(b):return hashlib.sha256(b).hexdigest()
def require(ok,label):
 if not ok:raise RuntimeError(label)
require(len(PUBLIC)==len(set(PUBLIC)),'Duplicated public allowlist member')
records={}
for name in PUBLIC:
 p=HERE/name;require(p.is_file() and not p.is_symlink(),'Missing/nonregular intentional artifact '+name)
 require(not any(q in p.relative_to(HERE).parts for q in ('private_sources','raw_sources','tmp','__pycache__')),'Private member in public allowlist')
 b=p.read_bytes();b.decode('utf-8');records[name]={'bytes':len(b),'sha256':digest(b)}
result=json.loads((HERE/'REVIEW_RESULT.json').read_text());require(result['verdict']=='PASS_FROZEN_REVISION2_NO_REPAIRS' and result['required_repairs']==[] and result['optional_repairs']==[],'Wrong verdict')
before=json.loads((HERE/'evidence/frozen_before.json').read_text());after=json.loads((HERE/'evidence/frozen_after.json').read_text());require(before['freeze_sha256']==after['freeze_sha256'],'Frozen record disagreement')
require(digest((AUDIT/'publication/PREPUBLICATION_FREEZE.json').read_bytes())==after['freeze_sha256'],'Final freeze record changed')
for n,r in after['frozen_active_files'].items():
 b=(AUDIT/'publication'/n).read_bytes();require(len(b)==r['bytes'] and digest(b)==r['sha256'],'Final frozen active byte changed '+n)
for n,r in after['unchanged_original_files'].items():
 b=(AUDIT/'original'/n).read_bytes();require(len(b)==r['bytes'] and digest(b)==r['sha256'],'Final original byte changed '+n)
manifest={'schema_version':1,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'review_family':'fresh_full_package_02','pr':905,'problem_id':'30000717','candidate_revision':2,'verdict':result['verdict'],'completion_percent':100,'artifacts':records,'public_artifact_allowlist':PUBLIC,'artifact_selection':'Explicit intentional allowlist; never infer publication membership by scanning this directory.','nonpublic_ignored_directories':['private_sources/','tmp/'],'manifest_self_hash_excluded':True,'frozen_before_sha256':records['evidence/frozen_before.json']['sha256'],'frozen_after_sha256':records['evidence/frozen_after.json']['sha256'],'frozen_candidate_identifiers':result['frozen_identifiers'],'checkable_proof':'REVIEW.md universal mathematical reconstruction, supported by independent_math.py and exact controls.','verification':'Recompute allowlisted hashes and sizes; compare frozen_before/frozen_after records and externally trusted candidate identifiers. These local hashes are custody evidence, not a source of external trust.','no_candidate_or_git_mutations':True,'no_external_human_contact':True}
b=json.dumps(manifest,indent=2).encode()+b'\n';(HERE/'MANIFEST.json').write_bytes(b)
print(json.dumps({'status':'PASS','public_artifacts':len(PUBLIC),'manifest_sha256':digest(b),'verdict':result['verdict']},indent=2))
