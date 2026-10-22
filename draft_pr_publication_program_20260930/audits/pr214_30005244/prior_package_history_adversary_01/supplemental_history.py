"""Supplemental read-only validation of original private/source and native custody references."""
from pathlib import Path
from datetime import datetime,timezone
import ast,difflib,hashlib,json,stat
P=Path("/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr214_30005244/preprint");A=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr214_30005244/prior_package_history_adversary_01");D=P.parent/'initial_review_20261015'
pins=[];missing=[]
def rd(p):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink()
 b=p.read_bytes();pins.append({'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':oct(stat.S_IMODE(s.st_mode))})
 return b
def j(p):return json.loads(rd(p))
def cp(p,r):
 b=rd(p);assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],str(p)
 return b
sources=[]
for k in (1,2):
 o=j(P/f'fresh_review_0{k}/SOURCE_PINS.json')
 rr=o['primary_source_files']+o['inherited_evidence_reports'] if k==1 else o['primary_sources']+o['bounded_audit_records']
 for r in rr:
  p=Path(r.get('provenance_path',r.get('path',str(D/r.get('path_relative_to_initial_review','')))))
  if not p.exists():
   missing.append({'review':k,'path':str(p),'expected_bytes':r['bytes'],'expected_sha256':r['sha256']});continue
  cp(p,r)
 sources.append({'review':k,'specified_local_sources_and_reports':len(rr),'available_hash_verified':sum(1 for r in rr if Path(r.get('provenance_path',r.get('path',str(D/r.get('path_relative_to_initial_review',''))))).exists())})
# Native body pins are not provider assertions: check exact preserved custody bodies.
C=A.parent/'native_source_custody_01'
recs=j(C/'BODY_RECORDS.json')['records'];bodymap={}
for r in recs:
 b=cp(C/r['reading_copy'],r)
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['sha']
 assert r['mode']=='100644'
 bodymap[(r['snapshot'],r['path'])]=b
orig=j(P/'pr_update/30005244/ORIGINAL_SUBMISSION_MANIFEST.json')
prefix='unsolved_math_prioritization/attempts/30005244/'
for r in orig['files']:
 n=r['native_path'];b=rd(P/'pr_update/30005244'/r['archive_path'])
 assert b==bodymap[('original',n)]==bodymap[('current',prefix+r['archive_path'])]
native_manifest=json.loads(bodymap[('current',prefix+'CURRENT_SOURCE_MANIFEST.json')])
for r in native_manifest['current_files']:cp(C/'_private/reading/current'/prefix/r['path'],r)
for r in native_manifest['frozen_preprint_submission_files']:cp(P/r['path'],r)
native_candidate=bodymap[('current',prefix+'CANDIDATE.md')].decode()
reviewed_candidate=rd(P/'pr_update/30005244/CANDIDATE.md').decode()
# Exactly one old administrative status paragraph replaced; entire analytic tail unchanged.
oldpara='The entire original 31-file submission, including its original version of this file and historical reviews/readiness claims, is preserved byte-for-byte under history/original_submission_20261015. Those reviews retain their original input bindings. Publication and merge are pending final sequential manuscript reviews and later explicit receipts.'
newpara='The entire original 31-file submission, including its original version of this file and historical reviews/readiness claims, is preserved byte-for-byte under history/original_submission_20261015. Those reviews retain their original input bindings. The preprint has completed the required sequential manuscript reviews and is published at https://doi.org/10.5281/zenodo.23390551. The verified publication/tracker receipts and FINAL_ACCEPTANCE.json record this administrative release update; native merge remains pending exact readback.'
assert reviewed_candidate.count(oldpara)==1 and reviewed_candidate.replace(oldpara,newpara)==native_candidate
assert bodymap[('current',prefix+'SOURCE_AUDIT.md')]==rd(P/'pr_update/30005244/SOURCE_AUDIT.md')
# Read generated constant AST literals only, reconstruct fixed status transformations without executing code.
source=rd(P/'prepare_supporting_materials.py').decode();tree=ast.parse(source)
constants={}
for n in tree.body:
 if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and isinstance(n.value,ast.Constant):
  constants[n.targets[0].id]=n.value.value
old=rd(P/'pr_update/30005244/history/original_submission_20261015/CANDIDATE.md').decode()
replacement={}
for n in tree.body:
 if isinstance(n,ast.Assign) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=='replace' and isinstance(n.value.args[0],ast.Name):
  replacement[n.value.args[0].id]=ast.literal_eval(n.value.args[1])
built=constants['header']+old.replace(constants['old_status'],replacement['old_status']).replace(constants['old_review'],replacement['old_review'])
assert built==reviewed_candidate
# Inspect all11 frozen render-pair records; record availability of physical historical images without creating new images.
renders=[]
for k in (1,2):
 o=j(P/f'fresh_review_0{k}/RENDER_BINDING.json')
 rows=o['pages'] if k==1 else o['fresh_comparison']
 assert len(rows)==11 and {r['page'] for r in rows}==set(range(1,12))
 for r in rows:
  assert r['identical'] is True
  a,b=(r['viewed_sha256'],r['fresh_render_sha256']) if k==1 else (r['fresh_sha256'],r['existing_sha256'])
  assert a==b and len(a)==64
 renders.append({'review':k,'page_pairs_valid':11,'pinned_pdf_sha256':o.get('frozen_pdf_sha256',o.get('pdf_sha256'))})
result={'UTC':datetime.now(timezone.utc).isoformat(),'all_checked_assertions_passed':True,'sources':sources,'unavailable_preserved_source_files':missing,
 'native_body_records_verified_offline':len(recs),'original31_directly_matched_with_both_native_custody_snapshots':True,
 'native_current_manifest_rows_verified':len(native_manifest['current_files']),'native_submission_pins_verified':len(native_manifest['frozen_preprint_submission_files']),
 'native_candidate_delta':'Exactly one administrative header paragraph; all mathematical and priority text unchanged.',
 'generator_status_transformation_reconstructed_from_AST_constants_exactly':True,'render_receipt_page_pairs':renders,
 'this_audit_did_not_repeat_historical_page_views_or_third_party_full_source_reading':True}
(A/'SUPPLEMENTAL_RESULT.json').open('x').write(json.dumps(result,indent=2)+'\n')
(A/'SUPPLEMENTAL_INPUTS_VERIFIED.json').open('x').write(json.dumps({'files':pins},indent=2)+'\n')
print(json.dumps(result,indent=2))
