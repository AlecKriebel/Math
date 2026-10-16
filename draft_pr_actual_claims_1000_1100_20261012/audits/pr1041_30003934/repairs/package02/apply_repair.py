#!/usr/bin/env python3
"""Bounded PR1041 package-verifier repair; no service/Git operations."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import hashlib,json,shutil,datetime
R=Path(__file__).resolve().parent;A=R.parent.parent;P=A/'preprint_v1_0'
def require(x,m):
 if not x:raise RuntimeError(m)
def sha(d):return hashlib.sha256(d).hexdigest()
def writej(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
# The old mutable records are first preserved verbatim, with old pin locators.
names=['README.md','SUPPLEMENT.md','EVIDENCE_INDEX.md','PREPARATION_REPORT.md','STATUS.json','PDF_QA.json','INTEGRITY_QA.json','RESEARCH_LOG.md','EVIDENCE_COPY_MANIFEST.json','CURRENT_INTEGRITY.json','BUILD_RECEIPT.json','ARCHIVE_SHA256.json','VERIFICATION_RECEIPT.json','build_archive.py','verify_package.py','prepare_support.py']
stage=P/'history/before_package02_verifier_repair';stage.mkdir(parents=True,exist_ok=True)
records=[]
for name in names:
 data=(R/'baseline_candidate'/name).read_bytes();require(data==(P/name).read_bytes(),'baseline changed '+name)
 (stage/name).write_bytes(data);records.append(dict(path=name,bytes=len(data),sha256=sha(data)))
writej(stage/'STAGE_PINS.json',dict(scope='Exact pre-package02 candidate authored records; each old locator remains relative to its original stage. These records retain PENDING_NEW_WHOLE_02 and the old verifier requirement. No current-input certification.',archive_sha256='1b51dd3d85d82b5fe8c080c3b535545db42762e28e7ddc803898e34813853614',files=records))
(stage/'README_STAGE.md').write_text('# Frozen stage before the package02 verifier repair\n\nAll sibling records are exact old bytes. Their historical input locators are interpreted relative to the original pre-repair package, not this history folder. The current manifest is at ../../CURRENT_INTEGRITY.json. STAGE_PINS.json identifies the preserved stage; current package records must not replace its source pins. The complete local baseline, including the old archive, is preserved externally in repairs/package02/baseline_candidate. The unchanged first clean review and the second P2 review retain their own input/output pins in evidence/reviews/package_01 and package_02.\n')
# Validate every terminal whole02 author output before copying, including text logs.
copies=json.loads((P/'EVIDENCE_COPY_MANIFEST.json').read_text());old=copies['files'].copy();require(len(old)==95,'old copy cardinality')
for rec in old:require((A/rec['source_path']).read_bytes()==(P/rec['package_path']).read_bytes(),'old copy mismatch')
pins=json.loads((A/'reviews/package_02/OUTPUT_PINS.json').read_text());require(len(pins['files'])==64,'whole02 output count')
for rec in pins['files']:
 data=(A/'reviews/package_02'/rec['path']).read_bytes();require(len(data)==rec['bytes'] and sha(data)==rec['sha256'],'whole02 sealed output mismatch')
for name in sorted([r['path'] for r in pins['files']]+['OUTPUT_PINS.json']):
 require('/' not in name and name.lower()!='fullsource.txt','unexpected terminal path')
 src='reviews/package_02/'+name;dst='evidence/'+src;data=(A/src).read_bytes();(P/dst).parent.mkdir(parents=True,exist_ok=True);(P/dst).write_bytes(data)
 copies['files'].append(dict(source_path=src,package_path=dst,group='frozen_package_02',bytes=len(data),sha256=sha(data),copy_policy='byte-identical authored terminal record; full second whole review retains its P2 finding and exact frozen inputs; rawprivate/render/replay absent'))
src='ROOT_WHOLE_PACKAGE_REVIEW_02.json';dst='evidence/root/'+src;data=(A/src).read_bytes();(P/dst).write_bytes(data)
copies['files'].append(dict(source_path=src,package_path=dst,group='root_whole_package_02_adoption',bytes=len(data),sha256=sha(data),copy_policy='unchanged root adoption of sole P2 finding; frozen candidate scope'))
copies['policy']='Only pinned authored prose, code, receipts, metadata and legitimate authored test output, including whole01 and whole02. No third-party raw/private bodies, source extracts, renders, replay/caches or discovery response dumps. Historical pins are never retargeted.'
copies['previous_copy_records_preserved']=95;copies['appended_second_whole_review_records']=65;copies['appended_root_whole02_adoption_records']=1
writej(P/'EVIDENCE_COPY_MANIFEST.json',copies)
# Both builder and verifier permit only copy-map-whitelisted authored text streams.
for name in ['build_archive.py','verify_package.py']:
 s=(P/name).read_text();s=s.replace("r['group']=='frozen_package_01' and r['package_path'].endswith(('_stdout.txt','_stderr.txt'))", "r['group'] in {'frozen_package_01','frozen_package_02'} and Path(r['package_path']).suffix.lower()=='.txt'")
 (P/name).write_text(s)
s=(P/'build_archive.py').read_text().replace('its exact metadata and file bindings are verified separately.', 'the default verifier checks packaged content and validates this wrapper strictly when present; --require-deposit additionally requires it and both verified local attachments.')
(P/'build_archive.py').write_text(s)
s=(P/'verify_package.py').read_text().replace('import gzip,hashlib,json,re,struct,tarfile,zlib','import argparse,gzip,hashlib,json,os,re,struct,tarfile,zlib')
s=s.replace('def main():\n    manifest=', '''def unique_object(pairs):
    result={}
    for key,value in pairs:
        require(key not in result,'Duplicate JSON key: '+key)
        result[key]=value
    return result

def main():
    parser=argparse.ArgumentParser(description='Verify distributable package content; strictly verify an external deposit wrapper when present.')
    parser.add_argument('--require-deposit',action='store_true',help='Require the external zenodo-deposit.json wrapper and both verified local upload attachments.')
    args=parser.parse_args()
    manifest=''')
s=s.replace("'priority_01','package_01']", "'priority_01','package_01','package_02']")
start=s.index("    wrapper=json.loads((ROOT/'zenodo-deposit.json').read_text())")
end=s.index("    result=dict(",start)
s=s[:start]+'''    require('zenodo-deposit.json' not in current,'Archive wrapper self-reference')
    wrapper_path=ROOT/'zenodo-deposit.json'
    wrapper_present=os.path.lexists(wrapper_path)
    require(wrapper_present or not args.require_deposit,'Required external deposit wrapper is absent: zenodo-deposit.json')
    wrapper_verified=False
    if wrapper_present:
        require(wrapper_path.is_file() and not wrapper_path.is_symlink(),'External wrapper must be a regular local file')
        wrapper=json.loads(wrapper_path.read_text(),object_pairs_hook=unique_object)
        require(type(wrapper) is dict and set(wrapper)=={'metadata','files'},'Malformed external wrapper object')
        metadata=json.loads((ROOT/'publication/zenodo.json').read_text())
        # Canonical JSON equality keeps types distinct (False is not 0, etc.).
        require(type(wrapper['metadata']) is dict and json.dumps(wrapper['metadata'],sort_keys=True,separators=(',',':'))==json.dumps(metadata,sort_keys=True,separators=(',',':')),'External wrapper metadata mismatch')
        expected_files=[{'path':'output/pdf/paper.pdf','name':'paper.pdf'},{'path':'supportkit-v1.0.tar.gz','name':'supportkit-v1.0.tar.gz'}]
        require(type(wrapper['files']) is list and wrapper['files']==expected_files,'External wrapper file binding mismatch')
        for entry in wrapper['files']:
            attachment=ROOT/entry['path']
            require(attachment.is_file() and not attachment.is_symlink(),'Missing or nonregular local upload attachment')
        record_ok(ROOT/'output/pdf/paper.pdf',current['output/pdf/paper.pdf'])
        require(archive_checked,'External wrapper requires a verified local support archive')
        wrapper_verified=True
''' +s[end:]
s=s.replace('gzip_crc_isize_verified=True,safe_sorted_casefold_unique_paths=True,external_wrapper_metadata_and_files_verified=True', "gzip_crc_isize_verified=archive_checked,safe_sorted_casefold_unique_paths=archive_checked,verification_mode='required_local_deposit' if args.require_deposit else 'distributable_kit',packaged_content_verified=True,external_wrapper_present=wrapper_present,external_wrapper_metadata_and_files_verified=wrapper_verified")
(P/'verify_package.py').write_text(s)
# Keep the staging helper current; historical copy retained above.
s=(P/'prepare_support.py').read_text();i=s.index("manifest=dict(")
s=s[:i]+'''base=AUDIT/'reviews/package_02'
pins=json.loads((base/'OUTPUT_PINS.json').read_text())
if len(pins['files'])!=64:raise RuntimeError('whole02 sealed output count')
for rec in pins['files']:
    data=(base/rec['path']).read_bytes()
    if len(data)!=rec['bytes'] or hashlib.sha256(data).hexdigest()!=rec['sha256']:raise RuntimeError('frozen whole02 mismatch')
for name in sorted([rec['path'] for rec in pins['files']]+['OUTPUT_PINS.json']):
    if '/' in name or name.lower()=='fullsource.txt':raise RuntimeError('unexpected terminal whole02 member')
    copy('reviews/package_02/'+name,'evidence/reviews/package_02/'+name,'frozen_package_02')
copy('ROOT_WHOLE_PACKAGE_REVIEW_02.json','evidence/root/ROOT_WHOLE_PACKAGE_REVIEW_02.json','root_whole_package_02_adoption')
'''+s[i:]
s=s.replace('pins and pinned first-complete-review test stdout/stderr.', 'pins and pinned first/second complete-review authored test output.').replace('appended_first_whole_review_records=41,files=records','appended_first_whole_review_records=41,previous_copy_records_preserved=95,appended_second_whole_review_records=65,appended_root_whole02_adoption_records=1,files=records')
(P/'prepare_support.py').write_text(s)
status=json.loads((P/'STATUS.json').read_text());status['new_whole_package_review']='PENDING_NEW_WHOLE_03';status['root_release_wording_issue']='ROOT-P3-RELEASE-WORDING-01 repaired before NEW_WHOLE_02; historical review records preserved'
status['second_whole_package_review']=dict(review='NEW_WHOLE_02',verdict='REQUIRES_P2_PACKAGE_REPAIR_COMPLETE_REVIEW',severity_counts=dict(P0=0,P1=0,P2=1,P3=0),verdict_path='evidence/reviews/package_02/VERDICT.json',root_adoption_path='evidence/root/ROOT_WHOLE_PACKAGE_REVIEW_02.json',frozen_input_scope='evidence/reviews/package_02/FINAL_INPUT_PINS.json')
status['package_verifier_repair']=dict(finding='PR1041-P2-CLEAN-EXTRACTION-VERIFIER-02',status='IMPLEMENTED_PENDING_NEW_WHOLE_03',scope='Distributable content and optional strict external wrapper; --require-deposit enforces local deposit coverage',manuscript_and_pdf_changed=False)
writej(P/'STATUS.json',status)
# Record current PDF coverage honestly as inherited; no compile/render occurs.
qa=json.loads((P/'PDF_QA.json').read_text());qa['scope']='Unchanged supplied TeX/PDF; prior actual nine-page compile/render/visual evidence retained in history/before_package02_verifier_repair/PDF_QA.json. This code-only repair did not compile, render or inspect new pages.';qa['readiness']='PENDING_NEW_WHOLE_03';qa['package02_new_compile_or_render']=False;writej(P/'PDF_QA.json',qa)
# Documentation uses separate packaged content and local external deposit coverage.
s=(P/'README.md').read_text().replace('The root subsequently recorded an editorial release-wording issue; the repair and subsequent review state are tracked in `STATUS.json`.', 'The root subsequently recorded an editorial release-wording issue. `evidence/reviews/package_02/` preserves the second complete review, including its sole P2 finding about the clean-extraction verifier. This code-only repair addresses that interface; the complete next review is pending in `STATUS.json`.')
s=s.replace('Its preparation does not create an uploaded record or reserve a DOI.', 'It is intentionally absent from the support archive. Its preparation does not create an uploaded record or reserve a DOI.')
s=s.replace('PYTHONDONTWRITEBYTECODE=1 python3 build_archive.py\n```','PYTHONDONTWRITEBYTECODE=1 python3 build_archive.py\nPYTHONDONTWRITEBYTECODE=1 python3 verify_package.py\n```\n\nThe default command verifies distributed content and provenance in a clean extraction. Before the archive is rebuilt, it reports `archive_checked=false`; afterwards it checks the rebuilt archive and its sidecar. An absent external wrapper is reported as `external_wrapper_present=false` and `external_wrapper_metadata_and_files_verified=false`. If the wrapper is present, both modes strictly validate its type, exact bare metadata, exact PDF/archive paths and names, and verified local attachments. For the complete local deposit kit, require that external wrapper explicitly:\n\n```sh\nPYTHONDONTWRITEBYTECODE=1 python3 verify_package.py --require-deposit\n```\n\nThis required mode fails if the wrapper is absent. Malformed or mismatched present wrappers fail in either mode. Verification does not upload, reserve a DOI or certify the mathematics.')
(P/'README.md').write_text(s)
s=(P/'SUPPLEMENT.md').read_text().replace('and first complete manuscript/package review retain', 'and first/second complete manuscript/package reviews retain').replace('Its legitimate exact-test stdout/stderr streams are retained;', 'The second complete review is frozen at `evidence/reviews/package_02/`, including its sole P2 finding and all 64 sealed authored outputs plus its seal. Both reviews’ legitimate authored test output streams are retained;')
s=s.replace('its exact metadata equality and both supplied-file hashes are checked externally.', 'a present wrapper is strictly checked against the unchanged bare metadata and the two verified local attachments. The default mode does not require an absent wrapper; `--require-deposit` does. Coverage flags distinguish these cases.')
s=s.replace('Use `verify_package.py` to check', 'Use `python3 verify_package.py` in a clean extraction to check').replace('It also enforces exclusions. It does not claim formal proof verification.', 'It also enforces exclusions and validates a present external wrapper strictly. An absent wrapper yields `external_wrapper_present=false` and `external_wrapper_metadata_and_files_verified=false`; the local archive is also honestly marked unchecked until rebuilt. `python3 verify_package.py --require-deposit` requires the external wrapper and both verified local attachments. Missing required, malformed present, wrong metadata/type or misbound wrappers fail. Neither mode claims formal proof verification.')
s=s.replace('from the first complete review are distributed;', 'from both complete reviews are distributed;').replace('and a later root editorial release-wording observation.', 'and a later root editorial release-wording observation, then NEW_WHOLE_02 with one P2 clean-extraction-verifier finding. The bounded code/documentation repair is awaiting NEW_WHOLE_03; both readiness flags remain false.')
s=s.replace('Root `PREPARATION_REPORT.md`, `PDF_QA.json`, and build receipts describe the editorially repaired inputs.', 'The next frozen stage at `history/before_package02_verifier_repair/` preserves all modified pre-repair records byte-for-byte. `HASH_STAGE_INDEX.json` distinguishes stage pins from current integrity. Root `PREPARATION_REPORT.md`, `PDF_QA.json`, and build receipts describe the code-only repaired package with unchanged supplied paper bytes.')
(P/'SUPPLEMENT.md').write_text(s)
s=(P/'EVIDENCE_INDEX.md').read_text().replace('| `RESEARCH_LOG.md`,', '| `evidence/reviews/package_02/` | Exact second whole-review terminal outputs and seal; one P2 verifier finding on its frozen inputs, not a current clean verdict. |\n| `evidence/root/ROOT_WHOLE_PACKAGE_REVIEW_02.json` | Unchanged root adoption of the second review and bounded repair requirement. |\n| `history/before_package02_verifier_repair/`, `HASH_STAGE_INDEX.json` | Old authored code, documentation, status and receipts preserved byte-for-byte with original stage meanings; current input pins are separate. |\n| `RESEARCH_LOG.md`,')
s=s.replace('Current package integrity and deterministic archive/check tooling, distinct from historic pin identities.', 'Current packaged-content integrity and deterministic archive tooling. Default clean-extraction verification; optional strict external wrapper checks; required local deposit mode via --require-deposit. Distinct from historic pin identities.')
(P/'EVIDENCE_INDEX.md').write_text(s)
(P/'PREPARATION_REPORT.md').write_text('''# Current package02 verifier repair preparation report

The sole finding PR1041-P2-CLEAN-EXTRACTION-VERIFIER-02 is addressed by separating distributable content verification from required local deposit coverage. `python3 verify_package.py` now works without the intentionally external wrapper and records its absence and unperformed check honestly. `--require-deposit` requires the wrapper. A wrapper present in either mode must be a regular file with valid unambiguous JSON, exactly the unchanged bare metadata and exactly the existing PDF/archive file descriptors; both local attachments must pass their content/archive checks. This is integrity/provenance verification, not formal proof verification or a new whole mathematical review.

All 95 old source-to-package mappings and bytes remain unchanged, including eleven originals and the first clean whole review. All 64 sealed terminal outputs of NEW_WHOLE_02, its OUTPUT_PINS.json and root adoption are appended unchanged (161 authored copies total). Its full report and sole P2 verdict retain their original meaning. Old modified top-level code/docs/pins/status/receipts are preserved verbatim under `history/before_package02_verifier_repair/`; initial history also remains unchanged. `HASH_STAGE_INDEX.json` navigates historical and current pin roles without retargeting old locators. Authored test outputs from both whole reviews are explicitly permitted by the copy map; raw/private source bodies, extracts, page images, replay trees, caches, discovery dumps and other third-party binaries remain excluded.

The supplied TeX and PDF are byte-identical to the NEW_WHOLE_02 inputs: TeX SHA-256 0ccac52f998823d98c020608c34ec2ad2cbd1d1f54db1815f0a00f898c5258c0; PDF SHA-256 3ba83c50a4a2369a70897ee165a43f56324aa31574cf9c199e664174cbce0449. No TeX compilation, new page marker, PDF export or render occurred in this code-only repair. Existing layout receipts remain historical evidence for these same bytes. Bare publication/zenodo.json and external zenodo-deposit.json are unchanged.

Current BUILD_RECEIPT.json and ARCHIVE_SHA256.json bind the closed distributed member set, safe sorted/casefold-unique paths, regular 0644 files, uid/gid zero, empty names, epoch 1791849600, gzip mtime zero and CRC/isize. The archive and its hash sidecar are absent from a clean extraction before a rebuild; default content verification reports that boundary. After building, it additionally validates that actual archive. A full local candidate includes the strictly checked external wrapper. New actual clean verify/build/verify, full required-deposit checks, fault controls in normal and optimized Python, independent closed tar/gzip reconstruction, copy/hash/type checks and unchanged protected-input custody are recorded externally under repairs/package02. Old game/flow scripts and their receipts remain unchanged.

STATUS.json is PENDING_NEW_WHOLE_03; publication_ready=false and all_issues_resolved=false. Root will assign the next complete independent review. No readiness promotion, global-priority conclusion, whole mathematical review, service/publication/DOI action, Git mutation or outside communication occurred. Alec Kriebel, independent researcher, ORCID 0009-0001-9320-500X, version 1.0, 13 October 2026 and CC BY 4.0 remain unchanged; extensive AI assistance/unrefereed-review boundaries remain disclosed.
''')
writej(P/'HASH_STAGE_INDEX.json',dict(policy='Historical records and source locators keep original byte identity and meaning; never rehash or retarget an old authored pin to the new stage.',historical_stages=[dict(path='history/initial_preparation/',scope='First 85-content-file preparation; exact old records retained'),dict(path='evidence/reviews/package_01/OUTPUT_PINS.json',scope='First clean whole review; frozen pre-editorial-repair inputs'),dict(path='history/before_package02_verifier_repair/STAGE_PINS.json',scope='Exact 16 old mutable authored records; original whole02 candidate input'),dict(path='evidence/reviews/package_02/OUTPUT_PINS.json',scope='64 exact terminal authored outputs; complete whole02 review with sole P2'),dict(path='evidence/root/ROOT_WHOLE_PACKAGE_REVIEW_02.json',scope='Exact root adoption of whole02 P2')],current_stage=dict(integrity='CURRENT_INTEGRITY.json',copy_map='EVIDENCE_COPY_MANIFEST.json',external_input_freeze='../repairs/package02/FINAL_CURRENT_INPUT_PINS.json',external_changes='../repairs/package02/CHANGE_INVENTORY.json',status='PENDING_NEW_WHOLE_03',publication_ready=False,all_issues_resolved=False)))
writej(R/'APPLY_RECEIPT.json',dict(timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),old_copy_records_unchanged=95,whole02_sealed_outputs_copied=64,whole02_output_seal_copied=True,root_adoption_copied=True,total_authored_copies=161,old_stage_records_preserved=16,tex_changed=False,pdf_changed=False,metadata_and_wrapper_changed=False,publication_ready=False,all_issues_resolved=False,new_whole_package_review='PENDING_NEW_WHOLE_03'))
print('Applied bounded code/docs repair; 161 copy records and 16 old stage records preserved')
