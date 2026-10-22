#!/usr/bin/env python3
"""Seal local bounded repair; does not promote publication readiness."""
from pathlib import Path
import datetime,difflib,hashlib,json,zipfile
E=Path(__file__).resolve().parent;R=E.parents[1];P=R/'NEWpreprint_v1_0'
def need(ok,message):
    if not ok:raise RuntimeError(message)
def sha(q):return hashlib.sha256(q.read_bytes()).hexdigest()
def record(q,root):return {'path':q.relative_to(root).as_posix(),'bytes':q.stat().st_size,'sha256':sha(q)}
def save(n,d): (E/n).write_text(json.dumps(d,indent=2)+'\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
base=json.loads((E/'BASELINE_INPUT_PINS.json').read_text())['records'];changes=[];protected=[]
for x in base:
 q=R/x['path'];same=q.is_file() and q.stat().st_size==x['bytes'] and sha(q)==x['sha256']
 if same:protected.append(x)
 else:
  need(x['path'].startswith('NEWpreprint_v1_0/'),'Unplanned non-candidate mutation: '+x['path']);n=x['path'].split('/',1)[1];before=E/'before'/n;need(before.is_file() and before.stat().st_size==x['bytes'] and sha(before)==x['sha256'],'Before bytes missing: '+n)
  changes.append({'path':x['path'],'before':x,'after':record(q,R) if q.is_file() else None,'before_bytes_path_relative_to_audit':before.relative_to(R).as_posix(),'authorized':'P3 output/bootstrap/citation repair or regenerated dependent custody/manifest/archive/binding/prose.'})
expected={'CITATION.cff','INPUT_COPY_MAP.json','PACKAGE_MANIFEST.json','PR1071_preprint_v1_0_support.zip','PR1071_preprint_v1_0_support.zip.sha256','README.md','SUPPLEMENT.md','UPLOAD_BINDINGS.json','scripts/build_archive.py','scripts/build_pdf.py','scripts/check.py','scripts/verify_package.py'}
need({x['path'].split('/',1)[1] for x in changes}==expected,'Unexpected candidate mutation set')
save('CHANGE_INVENTORY.json',{'utc':now,'authorized_existing_changes':changes,'count':len(changes),'new_candidate_files':[record(q,P) for q in sorted(P.rglob('*')) if q.is_file() and 'NEWpreprint_v1_0/'+q.relative_to(P).as_posix() not in {x['path'] for x in base}]})
save('PROTECTED_UNCHANGED.json',{'utc':now,'baseline_count':len(base),'authorized_existing_changes':len(changes),'unchanged_records':protected,'count':len(protected)})
# Exact original 204 preparation inputs and author instructions remain unchanged.
frozen=json.loads((P/'FROZEN_INPUTS.json').read_text());original=[]
for x in frozen['records']:
 q=R/x['path'];need(q.is_file() and q.stat().st_size==x['bytes'] and sha(q)==x['sha256'],'Original preparation input drift '+x['path']);original.append(x)
workspace=Path('/Users/alec/Documents/Math/AGENTS.md');need(sha(workspace)==frozen['workspace_AGENTS']['sha256'],'AGENTS drift')
save('PREPARATION_204_INPUT_RECHECK.json',{'utc':now,'records':original,'workspace_AGENTS':frozen['workspace_AGENTS'],'all_unchanged':True})
# Original 92 output stage is unchanged, but every mutation now resolves to exact saved before bytes.
resolution=[]
for x in json.loads((P/'INPUT_OUTPUT_PINS.json').read_text())['records']:
 q=P/x['path'];same=q.is_file() and q.stat().st_size==x['bytes'] and sha(q)==x['sha256'];before=E/'before'/x['path']
 if not same:need(before.is_file() and before.stat().st_size==x['bytes'] and sha(before)==x['sha256'],'Historical output resolution missing '+x['path'])
 resolution.append(dict(x,current_unchanged=same,before_bytes_path_relative_to_audit=None if same else before.relative_to(R).as_posix()))
save('PREPARATION_92_PIN_RESOLUTION.json',{'utc':now,'records':resolution,'count':len(resolution),'all_resolved':True,'scope':'Local audit; old ZIP/sidecar/external preparation receipts not all redistributed.'})
# Old copy records order/bytes unchanged; every appended source uses actual source or before-byte snapshot.
oldcopies=json.loads((E/'before/INPUT_COPY_MAP.json').read_text())['copies'];copies=json.loads((P/'INPUT_COPY_MAP.json').read_text())['copies'];need(copies[:len(oldcopies)]==oldcopies,'Original 50 copy records changed')
for x in copies:
 q=P/x['package_copy'];source=R/x.get('source_snapshot',x['original_path']);need(q.is_file() and source.is_file() and q.read_bytes()==source.read_bytes() and q.stat().st_size==x['bytes'] and sha(q)==x['sha256'],'Copy/source equality drift '+x['package_copy'])
save('COPY_EQUALITY_RECHECK.json',{'utc':now,'count':len(copies),'original_first_50_preserved_exactly':True,'records':copies,'all_source_equal':True})
review=R/'reviews/package_01';outputs=json.loads((review/'OUTPUT_PINS.json').read_text())['files']
for x in outputs:
 q=review/x['path'];need(q.is_file() and q.stat().st_size==x['bytes'] and sha(q)==x['sha256'],'Whole01 output drift '+x['path'])
excluded=json.loads((P/'WHOLE01_COPY_EXCLUSIONS.json').read_text())['records'];selected={x['original_path'] for x in copies if x['original_path'].startswith('reviews/package_01/')};need(all('reviews/package_01/'+x['path'] in selected or any(y['path']=='reviews/package_01/'+x['path'] for y in excluded) for x in outputs),'Whole01 selective copy ledger incomplete')
save('WHOLE01_OUTPUT_RECHECK.json',{'utc':now,'outputs_rehashed':len(outputs),'records':outputs,'all_unchanged':True,'individually_excluded':excluded,'seal_sha256':sha(review/'SEAL.json'),'root_adoption_sha256':sha(R/'ROOT_WHOLE_PACKAGE_REVIEW_01.json')})
# Exact bibliographic byte identities, not merely parsed equality.
protected_names=['paper.tex','paper.pdf','metadata.json','metadata_wrapped.json','deposit.json','STATUS.json','FINAL_VERIFICATION.json','FROZEN_INPUTS.json','INPUT_OUTPUT_PINS.json','checks/original_finite_checks.py','checks/original_expected.json']
lookup={x['path']:x for x in base};core=[]
for n in protected_names:
 q=P/n;x=lookup['NEWpreprint_v1_0/'+n];need(sha(q)==x['sha256'] and q.stat().st_size==x['bytes'],'Core protected input drift '+n);core.append(x)
meta=json.loads((P/'metadata.json').read_text());need(meta==json.loads((P/'metadata_wrapped.json').read_text())['metadata']==json.loads((P/'deposit.json').read_text())['metadata'],'Metadata objects differ')
originals=[x for x in protected if x['path'].startswith('submitted/')];need(len(originals)==9,'Unexpected original submitted count')
save('CORE_PROTECTED_IDENTITIES.json',{'utc':now,'records':core,'three_bibliographic_objects_byte_exact_and_equal':True,'original_nine_unchanged':originals,'actual_compile_render_or_marker':False})
# Every active code/prose change is in one full patch; huge hash ledgers are separately inventoried.
patch=[]
for n in ['scripts/package_paths.py','scripts/verify_package.py','scripts/build_archive.py','scripts/check.py','scripts/build_pdf.py','README.md','SUPPLEMENT.md','CITATION.cff','CITATION.txt','CURRENT_STATUS.json','REPAIR_NOTES.md','WHOLE01_COPY_EXCLUSIONS.json']:
 a=E/'before'/n;b=P/n;old=a.read_text().splitlines(keepends=True) if a.is_file() else [];new=b.read_text().splitlines(keepends=True) if b.is_file() else [];patch.extend(difflib.unified_diff(old,new,fromfile='before/'+n,tofile='current/'+n))
(E/'CODE_AND_PROSE_CHANGES.patch').write_text(''.join(patch))
current=[record(q,P) for q in sorted(P.rglob('*')) if q.is_file()];save('CURRENT_OUTPUT_PINS.json',{'utc':now,'scope':'All current candidate files, including existing excluded preparation outputs/private render derivatives; archive is explicit subset. Does not overwrite dated INPUT_OUTPUT_PINS.','records':current,'count':len(current)})
control=json.loads((E/'CONTROL_RECEIPTS.json').read_text());need(control['status']=='PASS' and control['actual_command_count']==168 and control['archive_sha256']==sha(P/'PR1071_preprint_v1_0_support.zip') and all(x['expected_outcome'] for x in control['records']),'Control receipts do not bind current archive')
with zipfile.ZipFile(P/'PR1071_preprint_v1_0_support.zip') as z:
 names=z.namelist();need(names==sorted(names) and len(names)==len(set(names)) and z.testzip() is None,'ZIP member/order/CRC defect');members=json.loads((P/'PACKAGE_MANIFEST.json').read_text())['members'];need(set(names)=={x['path'] for x in members}|{'PACKAGE_MANIFEST.json'},'ZIP allowlist differs')
 for n in names:need(z.read(n)==(P/n).read_bytes(),'ZIP current payload differs '+n)
archive_record=record(P/'PR1071_preprint_v1_0_support.zip',P)
save('FINAL_INTEGRITY.json',{'utc':now,'status':'PASS_BOUNDED_REPAIR_PENDING_ROOT_AND_NEW_WHOLE02','baseline_files':len(base),'authorized_existing_changes':len(changes),'protected_unchanged':len(protected),'original_inputs_unchanged':len(original),'historical_outputs_resolved':len(resolution),'source_equal_copies':len(copies),'whole01_outputs_unchanged':len(outputs),'candidate_current_files':len(current),'archive':archive_record,'archive_members':len(names),'manifest_payloads':len(members),'normal_optimized_actual_commands':168,'independent_closed_archive_byte_identical':True,'canonical_compile_render_or_marker':False,'metadata_objects_unchanged':True,'publication_ready':False,'issues_resolved':False,'published':False,'fresh_whole_reviews_completed':1,'minimum_required':2,'remaining_gate':'Root bounded repair adoption, then NEW complete whole02 adversarial review including real compilation and all seven current PDF pages; all service/disposition operations held behind PR1032.'})
print(json.dumps({'status':'PASS','baseline':len(base),'changes':len(changes),'protected':len(protected),'current':len(current),'copies':len(copies),'archive':archive_record,'members':len(names)},indent=2))
