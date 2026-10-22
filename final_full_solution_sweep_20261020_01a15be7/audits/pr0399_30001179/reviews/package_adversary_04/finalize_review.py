#!/usr/bin/env python3
"""Seal assigned reviewer artifacts only; verify unchanged inputs without mutations."""
from pathlib import Path
import datetime,hashlib,json
R=Path(__file__).resolve().parent;A=R.parents[1];ROOT=A.parents[1];REPO=ROOT.parent;P=ROOT/'private/pr0399_package04'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def entries(root,exclude=()):
 result=[]
 for p in sorted(root.rglob('*')):
  if p.is_symlink():raise RuntimeError('Symlink in review custody')
  if p.is_file() and p.relative_to(root).as_posix() not in exclude:result.append({'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)})
 return result
now=datetime.datetime.now(datetime.timezone.utc).isoformat();baseline=json.loads((R/'BASELINE.json').read_text());changed=[]
for n,e in baseline['package'].items():
 p=REPO/n
 if not p.is_file() or p.stat().st_size!=e['bytes'] or sha(p)!=e['sha256']:changed.append(n)
if changed:raise RuntimeError('Initial bound inputs changed: '+repr(changed))
for n,e in baseline['local_state'].items():
 p=REPO/n
 if not p.is_file() or p.stat().st_size!=e['bytes'] or sha(p)!=e['sha256']:raise RuntimeError('Initial Git bytes changed')
def tupledigest(paths):
 triples=[[p.relative_to(REPO).as_posix(),p.stat().st_size,sha(p)] for p in sorted(paths) if p.is_file()]
 return len(triples),hashlib.sha256(json.dumps(triples,separators=(',',':')).encode()).hexdigest()
flat=tupledigest((REPO/'.zenodo-state').glob('*.json'));recursive=tupledigest((REPO/'.zenodo-state').rglob('*'))
if flat!=(241,'1f67238497dbd8d275232e10dcdda23a03f151480d6c853c84d6fff720f57033') or recursive!=(314,'fe319e19f015bf2654598d4456551ba9a3a73b58c72738bf80fca8aa02aef5cc'):raise RuntimeError('Frozen local deposit inventory changed')
helpers=['ops_binding.py','prepublication_check.py','publication_live_gates.py','repository_integration.py','verify_published_files.py','publication_lifecycle.py','record_publication_ledger.py']
paths=[A/n for n in helpers]+[A/'preprint/publication/free-product-tensor-core.tex',A/'original/CANDIDATE_PROOF.md',A/'original/EXPOSITION_NOTE.md',A/'original/README.md',A/'original/INDEPENDENT_MEASURE_FACTORIZATION_REVIEW.md',A/'original/independent_reviews/CONTINUITY_CORE_REVIEW.md']
paths += [A/'reviews'/f/'REPORT.md' for f in ['measure_ordinal','continuity_core','priority_source','package_adversary_01','package_adversary_02','package_adversary_03']]
paths += [A/'publication_support'/f for f in ['build_package.py','integrity.py','reproduce.py','test_integrity_controls.py','BUNDLE_README.md','REPRODUCE.md','CODE_LICENSE.txt','SOURCE_REFERENCE_LEDGER.json']]
(R/'READ_RECEIPTS.json').write_text(json.dumps({'recorded_utc':now,'scope':'Complete listed text bodies actually read; primary selected source scopes and viewed PDF pages are separately bound. Read chronology: early manuscript/source reconstruction before previous opinions.','files':[{'path':p.relative_to(A).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p),'complete_body_read':True} for p in paths]},indent=2)+'\n')
finalinput=P/'FINAL_INPUT_VERIFICATION.json'
if json.loads(finalinput.read_text())!=json.loads((R/'INPUT_VERIFICATION.json').read_text()):raise RuntimeError('Final replay differs')
(R/'FINAL_PRESERVATION.json').write_text(json.dumps({'timestamp_utc':now,'existing_package_files_verified':len(baseline['package']),'changed_existing_package_files':[],'git_HEAD_index_initial_bytes_unchanged':True,'zenodo_direct':{'count':flat[0],'sha256':flat[1]},'zenodo_recursive':{'count':recursive[0],'sha256':recursive[1]},'final_input_verification_private_path':str(finalinput),'final_input_verification_sha256':sha(finalinput),'final_inputs_identical_to_initial_independent_verification':True,'current_helper_bindings':[{'path':n,'bytes':(A/n).stat().st_size,'sha256':sha(A/n)} for n in helpers],'root_reconciliation_sha256':sha(A/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json'),'current356_manifest_sha256':sha(A/'ops_record_url_repair_20261021/MANIFEST.json'),'publication_clearance_exists':(A/'ROOT_PUBLICATION_CLEARANCE.json').exists(),'no_reviewer_git_or_provider_mutations':True},indent=2)+'\n')
(R/'PRIVATE_CUSTODY_MANIFEST.json').write_text(json.dumps({'schema':1,'sealed_utc':now,'root':str(P),'scope':'Reviewer-owned private renders, extracted copies/mutants, synthetic provider fixtures, selected supplied metadata and new offline replay receipts. No third-party body or raw full account/sheet copied into public review.','files':entries(P)},indent=2)+'\n')
exclude={'AUTHORED_FILE_MANIFEST.json','AUTHORED_FILE_MANIFEST.sha256'}
manifest={'schema':1,'sealed_utc':now,'pr':399,'problem_id':'30001179','reviewer':'package_adversary_04','verdict':'REPAIR_REQUIRED','completion_estimate_percent':100,'publication_ready':False,'self_exclusions':sorted(exclude),'files':entries(R,exclude)}
p=R/'AUTHORED_FILE_MANIFEST.json'
if p.exists() or (R/'AUTHORED_FILE_MANIFEST.sha256').exists():raise RuntimeError('Never rewrite frozen seal')
p.write_text(json.dumps(manifest,indent=2)+'\n');checksum=sha(p);(R/'AUTHORED_FILE_MANIFEST.sha256').write_text(checksum+'  AUTHORED_FILE_MANIFEST.json\n')
for e in manifest['files']:
 p=R/e['path']
 if p.stat().st_size!=e['bytes'] or sha(p)!=e['sha256']:raise RuntimeError('Authored seal mismatch')
print(json.dumps({'complete':True,'verdict':'REPAIR_REQUIRED','finding':'P399-04-OPS-01','authored_entries':len(manifest['files']),'manifest_sha256':checksum,'report_sha256':sha(R/'REPORT.md'),'report_bytes':(R/'REPORT.md').stat().st_size,'private_entries':len(entries(P)),'publication_ready':False},indent=2))
