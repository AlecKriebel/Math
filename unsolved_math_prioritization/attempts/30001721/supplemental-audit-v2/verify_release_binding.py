#!/usr/bin/env python3
"""Read-only verification of the C1 corrected release; writes outside the freeze."""
from pathlib import Path
import difflib,hashlib,json
ROOT=Path('/workspace/shared/math-campaign/rank621-30001721')
R=ROOT/'release-v2'; OUT=ROOT/'supplemental-audit-v2'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inv(path):return {str(p.relative_to(path)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(path.rglob('*')) if p.is_file()}
def manifest(path):
 records={}
 for line in (path/'SHA256SUMS').read_text().splitlines():
  h,n=line.split(None,1); assert n not in records; assert not Path(n).is_absolute() and '..' not in Path(n).parts
  assert (path/n).is_file() and sha(path/n)==h,(path,n)
  records[n]=h
 return records
assert sha(R/'SHA256SUMS')=='1fbdf52823eca55c48ba8718a45a948d5df08cc1a2670e403c63fe9a2e99a67a'
assert sha(R/'author/SHA256SUMS')=='d0b38ae74653f2041d18bf5b2f300ff6b80a7ba079b2133c2e119ff5c474a3b2'
records=manifest(R)
actual=inv(R)
assert len(actual)==36
assert set(actual)==set(records)|{'SHA256SUMS'}
assert not any(p.is_symlink() for p in R.rglob('*'))
for d in ['author','original-author','original-audit']:manifest(R/d)
assert inv(ROOT/'author')==inv(R/'original-author')
assert inv(ROOT/'audit')==inv(R/'original-audit')
ledger=json.loads((R/'changes/RELEASE_LEDGER.json').read_text())
for key,d in [('original_author_files','original-author'),('preserved_full_audit_files','original-audit'),('corrected_author_files','author'),('fresh_replay_files','validation')]:
 assert ledger[key]==inv(R/d),(key,d)
assert ledger['original_author_manifest_sha256']==sha(R/'original-author/SHA256SUMS')
assert ledger['original_audit_manifest_sha256']==sha(R/'original-audit/SHA256SUMS')
assert ledger['original_audit_binding_sha256']==sha(R/'original-audit/AUDIT_BINDING.json')
assert ledger['corrected_author_manifest_sha256']==sha(R/'author/SHA256SUMS')
assert ledger['exact_patch_sha256']==sha(R/'changes/C1.patch')
assert ledger['replay_checks_sha256']==sha(R/'changes/REPLAY_CHECKS.json')
changed=[];patch=''
for p in sorted((R/'author').iterdir()):
 q=R/'original-author'/p.name
 if p.read_bytes()!=q.read_bytes():
  changed.append({'file':p.name,'before_sha256':sha(q),'after_sha256':sha(p),'before_bytes':q.stat().st_size,'after_bytes':p.stat().st_size})
  patch+=''.join(difflib.unified_diff(q.read_text().splitlines(keepends=True),p.read_text().splitlines(keepends=True),fromfile='original-author/'+p.name,tofile='author/'+p.name))
assert changed==ledger['exact_changed_author_files']
assert [x['file'] for x in changed]==['SHA256SUMS','control_results.json','verify_tree_controls.py']
assert patch==(R/'changes/C1.patch').read_text()
before=(R/'original-author/verify_tree_controls.py').read_text()
after=(R/'author/verify_tree_controls.py').read_text()
expected=before.replace("            'tested_basis_permutation_orbits':len(cache),","            'algebra_cases_evaluated':len(cache),\n            'basis_permutation_quotient_used':quotient,")
assert after==expected
old=json.loads((R/'original-author/control_results.json').read_text());new=json.loads((R/'author/control_results.json').read_text())
for name,item in old['enumerations'].items():
 item['algebra_cases_evaluated']=item.pop('tested_basis_permutation_orbits')
 item['basis_permutation_quotient_used']=name=='affine_D4_3_2_2_1_1'
assert old==new
assert [x['algebra_cases_evaluated'] for x in new['enumerations'].values()]==[32,12,1,485]
assert [x['basis_permutation_quotient_used'] for x in new['enumerations'].values()]==[False,False,False,True]
# All present paths are audit/research text, code or structured result artifacts.
assert all(Path(n).suffix in {'.md','.json','.py','.patch','.txt'} or Path(n).name=='SHA256SUMS' for n in actual)
assert all('\x00' not in (R/n).read_text() for n in actual)
# The release inventory is completely specified by the historical snapshots,
# corrected author and the eight explicit packaging/replay additions below.
expected_files={f'author/{n}' for n in inv(ROOT/'author')}|{f'original-author/{n}' for n in inv(ROOT/'author')}|{f'original-audit/{n}' for n in inv(ROOT/'audit')}|{
 'README.md','SHA256SUMS','changes/C1.patch','changes/RELEASE_LEDGER.json','changes/REPLAY_CHECKS.json',
 'validation/author_replay.json','validation/author_replay_stdout.json','validation/generation_stdout.json','validation/independent_results.json','validation/independent_stdout.txt'}
assert set(actual)==expected_files
result={'release_master_manifest_sha256':sha(R/'SHA256SUMS'),'corrected_author_manifest_sha256':sha(R/'author/SHA256SUMS'),'release_file_count':36,'master_manifest_coverage_exact':True,'all_nested_manifests_valid':True,'original_author_byte_preserved':True,'original_audit_byte_preserved':True,'ledger_all_hashes_bytes_match':True,'exact_patch_regenerated_matches':True,'author_only_changed_files':[x['file'] for x in changed],'C1_exactly_implemented':True,'nonmetadata_json_unchanged':True,'case_counts':[32,12,1,485],'quotient_flags':[False,False,False,True],'safe_inventory_complete':True,'no_symlinks_or_binary_source_payloads':True,'release_file_hashes':{n:x['sha256'] for n,x in actual.items()}}
(OUT/'binding_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='release_file_hashes'},indent=2))
