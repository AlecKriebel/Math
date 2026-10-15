#!/usr/bin/env python3
"""Freeze bounded repair custody and terminal authored outputs; no services/Git."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import datetime,difflib,hashlib,json
R=Path(__file__).resolve().parent;A=R.parent.parent;P=A/'preprint_v1_0'
def require(x,m):
 if not x:raise RuntimeError(m)
def sha(d):return hashlib.sha256(d).hexdigest()
def record(p,base):
 d=p.read_bytes();return dict(path=p.relative_to(base).as_posix(),bytes=len(d),sha256=sha(d))
def writej(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
baseline=json.loads((R/'BASELINE_ALL_PINS.json').read_text());old={x['path']:x for x in baseline['files']}
changed=[];unchanged=[]
for name,before in old.items():
 path=A/name;require(path.is_file(),'Missing baseline file '+name)
 after=record(path,A)
 if any(before[k]!=after[k] for k in ['bytes','sha256']):
  require(name.startswith('preprint_v1_0/'),'Changed protected outside-candidate input '+name)
  rel=name[len('preprint_v1_0/'):]
  saved=R/'baseline_candidate'/rel
  require(saved.is_file() and sha(saved.read_bytes())==before['sha256'],'Baseline preservation failed '+rel)
  historical='repairs/package02/baseline_candidate/'+rel if rel=='supportkit-v1.0.tar.gz' else 'preprint_v1_0/history/before_package02_verifier_repair/'+rel
  require((A/historical).is_file() and sha((A/historical).read_bytes())==before['sha256'],'Old authored stage absent '+rel)
  changed.append(dict(path=name,before=before,after=after,exact_old_stage_copy=historical))
 else:unchanged.append(after)
require(len(changed)==17,'Unexpected changed input count')
current=[record(x,P) for x in sorted(P.rglob('*')) if x.is_file()]
added=[record(x,A) for x in sorted(P.rglob('*')) if x.is_file() and x.relative_to(A).as_posix() not in old]
require(len(added)==85,'Unexpected new member count')
tex=sha((P/'paper.tex').read_bytes());pdf=sha((P/'output/pdf/paper.pdf').read_bytes())
require(tex=='0ccac52f998823d98c020608c34ec2ad2cbd1d1f54db1815f0a00f898c5258c0' and pdf=='3ba83c50a4a2369a70897ee165a43f56324aa31574cf9c199e664174cbce0449','Protected paper bytes changed')
for name in ['publication/zenodo.json','zenodo-deposit.json']:
 require((P/name).read_bytes()==(R/'baseline_candidate'/name).read_bytes(),'Protected metadata/descriptor changed')
copies=json.loads((P/'EVIDENCE_COPY_MANIFEST.json').read_text());oldcopies=json.loads((R/'baseline_candidate/EVIDENCE_COPY_MANIFEST.json').read_text())
require(copies['files'][:95]==oldcopies['files'] and len(copies['files'])==161,'Old source-copy records altered')
for x in copies['files']:
 d=(P/x['package_path']).read_bytes();require(d==(A/x['source_path']).read_bytes() and len(d)==x['bytes'] and sha(d)==x['sha256'],'Copy identity mismatch')
whole=json.loads((A/'reviews/package_02/OUTPUT_PINS.json').read_text());require(len(whole['files'])==64,'Whole02 seal count')
for x in whole['files']:
 d=(A/'reviews/package_02'/x['path']).read_bytes();require(len(d)==x['bytes'] and sha(d)==x['sha256'],'Old whole02 output changed')
status=json.loads((P/'STATUS.json').read_text());require(status['new_whole_package_review']=='PENDING_NEW_WHOLE_03' and status['publication_ready'] is False and status['all_issues_resolved'] is False,'Readiness prematurely changed')
tests=json.loads((R/'TEST_RESULTS.json').read_text());negative=json.loads((R/'NEGATIVE_CONTROLS.json').read_text())
require(tests['all_expected_results'] and tests['independent_tar_gzip_bytes_identical'] and negative['total']==108 and negative['all_rejected_with_expected_failure'],'Incomplete tests')
archive_sha=sha((P/'supportkit-v1.0.tar.gz').read_bytes());require(archive_sha==tests['archive_sha256'],'Tested/current archive mismatch')
receipt=json.loads((P/'VERIFICATION_RECEIPT.json').read_text());require(receipt['external_wrapper_present'] and receipt['external_wrapper_metadata_and_files_verified'] and receipt['archive_checked'] and receipt['verification_mode']=='required_local_deposit','Current full-local receipt incomplete')
writej(R/'PROTECTED_UNCHANGED_RECEIPT.json',dict(utc=now,baseline_files=len(old),baseline_sha256=sha((R/'BASELINE_ALL_PINS.json').read_bytes()),unchanged_baseline_files=len(unchanged),authorized_changed_candidate_files=17,no_baseline_files_missing=True,no_outside_candidate_input_changed=True,old_95_copy_records_and_bytes_identical=True,all_11_originals_unchanged=True,all_original_root_family_priority_whole01_whole02_prior_repair_inputs_unchanged=True,whole02_sealed_outputs_rechecked=64,tex_sha256=tex,pdf_sha256=pdf,bare_metadata_sha256=sha((P/'publication/zenodo.json').read_bytes()),external_descriptor_sha256=sha((P/'zenodo-deposit.json').read_bytes()),metadata_and_descriptor_byte_unchanged=True,all_16_modified_old_authored_records_copied_exactly=True,old_archive_local_baseline_preserved_exactly=True,new_compile_render_or_marker=False,publication_ready=False,all_issues_resolved=False))
writej(R/'CHANGE_INVENTORY.json',dict(utc=now,policy='Before and after hashes only; old source/history pins remain unchanged. Added evidence is copied exactly and separately pinned.',changed=changed,added=added,unchanged_baseline_count=len(unchanged),changed_count=17,added_count=85,tex_pdf_math_and_metadata_changed=False))
writej(R/'FINAL_CURRENT_INPUT_PINS.json',dict(utc=now,scope='Complete final local preprint_v1_0 file tree, including intentionally non-distributed sidecars and untouched ignored tmp identity. This external current freeze is distinct from unretargeted distributed historical pins.',files=current,total_files=len(current),content_files=208,archive_members=210,archive_sha256=archive_sha,tex_sha256=tex,pdf_sha256=pdf,new_whole_package_review='PENDING_NEW_WHOLE_03',publication_ready=False,all_issues_resolved=False))
# Checkable machine resolution statement tied to actual final tests and code bytes.
writej(R/'P2_RESOLUTION_PROOF.json',dict(utc=now,finding='PR1041-P2-CLEAN-EXTRACTION-VERIFIER-02',disposition='BOUNDED_IMPLEMENTATION_AND_LOCAL_REPRODUCTIONS_PASS_PENDING_NEW_WHOLE_03',claim='A clean distributed extraction verifies content/provenance before and after byte-identical archive rebuild without the excluded external wrapper; an explicit required-local-deposit mode rejects absent wrappers; any malformed/mismatched present wrapper fails both modes.',mechanism=dict(default='distributable_kit',required_flag='--require-deposit',absent_wrapper_present=False,absent_wrapper_metadata_and_files_verified=False,present_wrapper_validation='Regular file, unambiguous JSON object, exact type-sensitive bare metadata, exact unchanged PDF/archive descriptors, verified regular local attachments',archive_absence_reported_honestly=True,existing_content_copy_historical_payload_cardinality_and_pending_status_checks_retained=True),actual_clean_sequences_normal_and_optimized=True,actual_full_local_verify_build_verify=True,actual_present_wrapper_both_modes_normal_and_optimized=True,actual_required_absent_failures=4,fault_runs=108,fault_families=27,fault_interpreters=['normal','-O'],fault_modes=['default','--require-deposit'],explicit_runtime_exceptions=True,independent_tar_gzip_rebuild_byte_identical=True,test_results_sha256=sha((R/'TEST_RESULTS.json').read_bytes()),negative_controls_sha256=sha((R/'NEGATIVE_CONTROLS.json').read_bytes()),verifier_sha256=sha((P/'verify_package.py').read_bytes()),builder_sha256=sha((P/'build_archive.py').read_bytes()),archive_sha256=archive_sha,mathematical_proof_review_performed=False,publication_ready=False,all_issues_resolved=False))
# Exact text diff excludes archive binary and keeps old stage records as snapshots.
patch=[]
for x in changed:
 rel=x['path'][len('preprint_v1_0/'):]
 if rel=='supportkit-v1.0.tar.gz':continue
 before=(R/'baseline_candidate'/rel).read_text().splitlines(True);after=(P/rel).read_text().splitlines(True)
 patch.extend(difflib.unified_diff(before,after,fromfile='before/'+rel,tofile='current/'+rel))
(R/'ALL_AUTHORED_TEXT_CHANGES.patch').write_text(''.join(patch))
(R/'REPAIR_REPORT.md').write_text(f'''# PR1041 package02 bounded repair report

The sole finding **PR1041-P2-CLEAN-EXTRACTION-VERIFIER-02** is resolved at the implementation and local reproduction level. The clean support kit now runs its documented `python3 verify_package.py` without the intentionally excluded external `zenodo-deposit.json`. An absent wrapper yields `external_wrapper_present=false` and `external_wrapper_metadata_and_files_verified=false`. Before rebuilding the absent local archive, archive/CRC/path validation is also explicitly unperformed. After `python3 build_archive.py`, verification checks the byte-identical reconstructed archive. `--require-deposit` requires the external wrapper and both checked local upload attachments. A present wrapper is strictly validated in either mode: regular file, unambiguous JSON keys, exact type-sensitive equality to the unchanged bare metadata, exact existing PDF/archive paths and names, and verified regular attachments.

The implementation preserves all existing current-content membership/hash, copy-map, original pin, historical output-pin/exclusion, archive payload/cardinality/path/order/mode/owner/epoch/gzip CRC/isize and pending-status guards. Explicit RuntimeError guards remain active under Python -O. Allowlisting authored text streams now includes both complete reviews through their exact copy-map identities. `prepare_support.py` preserves prior map records and was actually rerun: the complete 161-record copy map remained byte-identical.

## Actual verification

`test_repair.py`, `TEST_RESULTS.json` and the exact named stdout/stderr files preserve 21 actual interface/build/exclusion runs, including four intentionally failed required-mode absent-wrapper runs. Clean verify → build → verify succeeds in normal and optimized Python; absence flags are false and archive coverage changes honestly after the rebuild. Adding the exact unchanged descriptor yields success in default and required modes in both interpreters. A full local-candidate copy also passes required verify → build → verify. Clean, full-copy and independent reconstructions all produce identical final bytes.

`NEGATIVE_CONTROLS.json` records **108 intended failures: 27 distinct faults × normal/-O × default/required**. Wrapper tests attack syntax, duplicate keys, object/metadata/files types, extra keys, metadata/title/publication/upload types, file paths/names, nonexternal misbinding and duplicate attachments. Further tests attack wrapper symlink/broken-symlink/directory, missing local archive, changed/undeclared content, old authored copies, and pending readiness after a refreshed manifest. Tar payload, missing member, duplicate member and mode faults remain rejected even after rebuilding valid outer hashes. Historical output-pin corruption remains rejected after changing its copy-map hash and rebuilding current integrity. Excluded private/source/extract/render/replay/cache/discovery probes do not change the archive.

The final archive has **208 content files and 210 regular tar members**, retaining every old 125-member path and adding 85 content paths: 66 exact whole02/root copies, 18 old-stage snapshot/navigation files and one stage index. Independent code reconstructed every closed tar byte and the complete gzip stream, with sorted safe/casefold-unique paths, regular 0644 files, uid/gid0, empty owner names, epoch1791849600, gzip mtime0 and correct CRC/isize. All distributed non-PDF files decode as UTF-8 and parseable JSONs were parsed; no hidden source PDF/image/archive signature was found. The sole distributed binary is the unchanged authored paper PDF.

Final archive SHA-256: `{archive_sha}`. The final complete local candidate contains {len(current)} pinned files; `FINAL_CURRENT_INPUT_PINS.json` includes the external descriptor/sidecars and untouched ignored temporary identities while distinguishing those from the distributed content. `CHANGE_INVENTORY.json` gives before/after hashes for all 17 changed candidate files and all 85 additions. `P2_RESOLUTION_PROOF.json` binds the exact final code and actual test/control receipts.

## Preserved history and protected data

The immediate 2505-file `BASELINE_ALL_PINS.json` covers the entire prior audit. All {len(unchanged)} baseline file bytes outside the 17 authorized candidate changes remain identical; no baseline file is missing and no outside-candidate input changed. Complete original/root/family/priority/clean-whole01/P2-whole02/repair01 records are unchanged. Every changed old authored record was saved verbatim before editing: 16 code/docs/pins/status/receipts in `history/before_package02_verifier_repair/`, plus the old archive in the external local baseline. Their original meanings and locators are documented without retargeting a pin. Initial preparation history remains exact. `HASH_STAGE_INDEX.json` separates historical stages from current integrity/current external freeze.

All **95 old copy records and bytes** remain identical, including eleven originals. Exactly **64 terminal authored whole02 outputs**, its `OUTPUT_PINS.json`, and `ROOT_WHOLE_PACKAGE_REVIEW_02.json` were appended byte-for-byte, giving 161 copies. Whole02 retains its complete P2 verdict rather than being relabeled clean. Legitimate authored test output, including the reviewer's transparently diagnosed initial checker error, is included; rawprivate/raw/replay/render/extracted/cache/source bodies remain absent. Both successful earlier repair test stages are retained externally under `test_stages/attempt01/` and `attempt02/`. The harness-only initial rerun error is recorded separately; it resulted from reusing the prior test extraction after adding a wrapper, was corrected by resetting tmp, and was never treated as a package or manuscript finding.

Protected TeX SHA-256: `{tex}`. Protected PDF SHA-256: `{pdf}`. Both paper bytes, all mathematical/source/credit/priority claims, and the exact bare `publication/zenodo.json` and external descriptor are unchanged. This repair did not compile, export, render, insert a marker, or newly inspect PDF pages. Current PDF QA explicitly inherits the exact prior nine-page layout evidence; the old receipt remains verbatim in its historical stage. No new complete mathematical or whole-package review is claimed. `PROTECTED_UNCHANGED_RECEIPT.json` checks these facts against the immediate baseline.

## Current disposition

The bounded repair estimate is **100%**. Current state is **PENDING_NEW_WHOLE_03**, **publication_ready=false**, **all_issues_resolved=false**. Root will assign a fresh complete independent whole review and decide readiness. This report establishes the narrow interface repair and reproducible package custody, not a new mathematics or global-priority verdict. Author/date/version/ORCID/license and extensive AI/unrefereed boundaries remain unchanged.

Writes were confined to repairs/package02 and necessary preprint code/docs/evidence/receipts/archive. No branch/index/Git mutation, PR action, release, upload, DOI, network/service call, contact with an individual, outreach, other shard or subagent occurred. Only local package/deposit binding checks were performed.
''')
with (R/'RESEARCH_LOG.md').open('a') as f:f.write(f'- {now}: Final supplied candidate tested after all package writes: 21 interface/build/exclusion runs, 108 intended failures, 208 content files/210 archive members, independently byte-identical tar/gzip, 161 exact copies, all 2505 baseline paths checked with only 17 authorized candidate changes and 85 additions. Complete current pins, change inventory, protected-data receipt, checkable P2 resolution and final report written; terminal authored output seal follows with no later authored edits. Bounded repair estimate: 100%; publication_ready=false/all_issues_resolved=false, PENDING_NEW_WHOLE_03. Final archive SHA-256 {archive_sha}.\n')
# All terminal authored repair files (including preserved completed test stages),
# excluding raw disposable trees and the local binary baseline. This seal is last.
outputs=[]
for x in sorted(R.rglob('*')):
 if not x.is_file():continue
 rel=x.relative_to(R)
 if rel.as_posix()=='OUTPUT_PINS.json' or any(z in {'tmp','baseline_candidate','__pycache__'} for z in rel.parts):continue
 outputs.append(record(x,R))
writej(R/'OUTPUT_PINS.json',dict(utc=now,policy='Terminal authored repair outputs and exact earlier completed test stages only; seal excluded from own hash domain. Local baseline bodies/binary archive and disposable tmp excluded. No authored edit follows this seal.',files=outputs,publication_ready=False,all_issues_resolved=False,new_whole_package_review='PENDING_NEW_WHOLE_03'))
print(json.dumps(dict(status='BOUNDED_REPAIR_SEALED_PENDING_NEW_WHOLE_03',output_files=len(outputs),current_input_files=len(current),archive_sha256=archive_sha,final_current_input_pins_sha256=sha((R/'FINAL_CURRENT_INPUT_PINS.json').read_bytes()),change_inventory_sha256=sha((R/'CHANGE_INVENTORY.json').read_bytes()),repair_report_sha256=sha((R/'REPAIR_REPORT.md').read_bytes()),output_pins_sha256=sha((R/'OUTPUT_PINS.json').read_bytes()),publication_ready=False,all_issues_resolved=False)))
