#!/usr/bin/env python3
"""Seal the completed bounded review; never mutates candidate or live state."""
from pathlib import Path
import datetime,hashlib,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent;PACKAGE=BASE/'package'
def require(test,message):
 if not test:raise RuntimeError(message)
def fingerprint(path):
 b=path.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
freeze_bytes=(HERE/'FROZEN_INPUT.json').read_bytes();require(freeze_bytes==(BASE/'PACKAGE_REVIEW_INPUT_4.json').read_bytes(),'Freeze changed')
freeze=json.loads(freeze_bytes);checked=[]
for name,expected in freeze['files'].items():
 actual=fingerprint(PACKAGE/name);require(actual==expected,'Frozen file changed: '+name);checked.append({'path':name,**actual,'expected':expected,'match':True})
payloads=[]
for name,expected in json.loads((PACKAGE/'SHA256SUMS.json').read_text())['files'].items():
 actual=fingerprint(PACKAGE/name);require(actual==expected,'Payload changed: '+name);payloads.append({'path':name,**actual,'match':True})
positive=json.loads((HERE/'POSITIVE_REPRODUCTION.json').read_text());controls=json.loads((HERE/'FRESH_ADVERSARIAL_CONTROLS.json').read_text());archive=json.loads((HERE/'ARCHIVE_CHECKS.json').read_text());meta=json.loads((HERE/'METADATA_CHECKS.json').read_text())
require(controls['valid_intended_construction_rejections']==32 and controls['valid_intended_driver_rejections']==18 and controls['permitted_acceptances_verified']==2,'Control totals')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
final={'rechecked_at_utc':now,'freeze_path':'PACKAGE_REVIEW_INPUT_4.json','freeze_sha256':hashlib.sha256(freeze_bytes).hexdigest(),'freeze_copy_byte_equal':True,'frozen_files':checked,'all_frozen_files_match':True,'selected_payloads':payloads,'selected_payload_count':67,'all_selected_payloads_match':True,'full_archive_sha256':archive['archive']['sha256'],'candidate_mutation':False,'live_api_client_created':False,'credentials_or_state_loaded':False,'external_communication':False,'mandatory_issues':0,'blocking_issues':0,'new_optional_issues':0}
(HERE/'FINAL_INPUT_RECHECK.json').write_text(json.dumps(final,indent=2,sort_keys=True)+'\n')
math=(HERE/'INITIAL_VERDICT.md').read_text().split('## Exact claim and endpoints',1)[1]
header='''# Complete independent package review, round four — PR468 / problem30000689

**PASS for this bounded full-package adversarial review. Mandatory issues: 0. Blocking issues: 0. New optional issues: 0.** No additional candidate correction is requested. This verdict is a fallible AI-assisted mathematical/package review, not formal proof certification, independent human peer review, a security certificate, or a first-priority determination. The root owns all later publication and repository decisions.

The complete frozen candidate was reviewed, including the unchanged source/PDF, canonical metadata, rebuilt supplement, and every bound payload. The initial proof reconstruction was saved in `INITIAL_VERDICT.md` before any earlier review, priority, or repair prose was read. Only raw foreign primary PDFs were reused during that initial phase. All eight manuscript PDF pages were freshly rendered and visually inspected; they are legible, with no clipping, broken symbols, overlaps, missing text, or bibliography layout defect identified. The principal theorem pages in the source ledger were read from fresh raw-source extractions and visually inspected as renders; the full original NW Section 5 was read, including every step of its proof.

No source/candidate/index/branch/PR/tracker/Zenodo mutation, external communication or prepared outreach occurred. All reviewer writes are within this review folder. Foreign texts, foreign renders/extractions, independent archive extraction, and intentionally invalid fixtures remain under ignored `private_sources/` and are excluded from `OUTPUT_MANIFEST.json`.

## Independent proof and exact hypothesis reconstruction

## Exact claim and endpoints'''
package='''

## Complete archive, original evidence and current-code validation

The fresh archive was first checked for duplicate/unsafe names, path traversal, absolute/backslash paths, directory/symlink entries, private foreign/derived file inclusion, and exact membership. It contains exactly **68 regular entries**, equal to the **67 payload paths** bound by SHA256SUMS plus SHA256SUMS itself. Every member CRC was independently recalculated; `ZipFile.testzip()` returned no failing member. Every size/SHA256 matched the payload manifest and every archived byte matched the candidate's local payload. The archive hash is `3d87ba2ae2a4c9e7dc1cc99a08d75345df0b1f854c6a37ec6d4900a2c48118fa`, size **152980 bytes**. The evidence is in `ARCHIVE_CHECKS.json`, with all 68 entries enumerated.

All **15 original historical files** match the source snapshot at the frozen claimed-solved head `8527ccdba064bca52035fc6c8d96caa750ac9c00`. The original publication/author/audit manifests' **24 size/SHA256 references** match, and six additional author crosschecks match. Both distributed patch files apply to independently copied historical programs and produce byte-identical current programs. `HISTORICAL_PATCH_CHECKS.json` enumerates each original and each reference. The legacy independent patch header says frozen/hardened; the README explicitly maps that historical nomenclature to historical/checks/patches, and applying it to the selected historical input works exactly.

The complete current source of all three checkers and the driver was inspected. Current checker ASTs contain **zero Assert nodes**; conditions are explicit RuntimeErrors and remain active under optimized Python. Historical original scripts retain 9 and 18 assertions as preserved historical inputs, not the recommended current verification entrypoint. All current paths/hashes bind the derived programs and expected outputs. The standard-library-only, Python>=3.10 claim is compatible with the inspected APIs. Seeded finite move choices use floating-point weighted selection, expressly disclosed; universal cross-future-Python/platform byte stability is not claimed.

From an independently extracted archive, all three programs ran directly in both normal and optimized modes: **six direct successful runs**, each stderr-empty and byte-identical to the bound expected output. Two additional whole-driver passes (normal and optimized interpreter, driver's default both child modes) produced **12 successful child runs**. Actual runtime was Python **3.14.6**. Evidence is in `POSITIVE_REPRODUCTION.json`, the six recorded direct JSON outputs, and two driver receipts.

| Program | Independently replayed finite coverage | Normal/-O stdout SHA256 |
| --- | --- | --- |
| Author | Four stellar examples and four Flores cycles, d=1..4; eight quotient ranks at F101 for d=1,2; one flag example with 104 face-poset vertices, 3084 comparable triples, zero missing triangles; arithmetic metastable checks for d=1..8 | `35f779a32720c6ca5314d1111ade9ffd88a3b09aed200e80a266c8a95805f657` |
| Prior audit derivative | Seed 49830000689, 100 moves with p-counts 9,20,28,30,13; 3542 complement calculations, 824 persistent missing-triangle checks, 28 middle identities, 70 new-face witnesses | `455b2a632604159a9abf35d3e62091740808d2cd101b24d568f81fc7c7d9b1f7` |
| Independent bitmask | Four stellar/Flores examples; 24 quotient ranks over F7/F101/F103; seed 202610120468, 100 moves with p-counts 9,20,30,28,13; 3548 complements, 580 persistent missing triangles, 30 middle identities, 52 new-face witnesses | `d542b3b38ab27a77f979d1d5207d617e2b71638ee82f79193e1935de6a7e4b6e` |

These are finite consistency computations. They do not prove generic characteristic-zero algebra, recognize all TOP spheres, show integral acyclicity or contractibility, distinguish exotic PL structures, prove the universal obstruction or assign a probability of truth. In particular the complement computation is only reduced H0/H1 over F2. The universal theorem is assessed through the proof/source reconstruction above.

## Fresh actual fault controls and accepted probes

A new harness (`fresh_controls.py`) mutates computed constructions, not just expected constants or assertion predicates. All mutant sources parse before execution. Its **16 distinct construction faults** ran in both modes, **32 runs total**, and **all 32 rejected at the intended RuntimeError**. No construction fault was accepted, and no syntax, indentation, missing import or arbitrary nonzero exit was credited as a valid mathematical rejection. Full actual tracebacks, intended diagnostic strings, return codes, stdout sizes and fixture hashes are in `FRESH_ADVERSARIAL_CONTROLS.json`.

| Family | Actual altered constructions | Valid intended rejections |
| --- | --- | --- |
| Author | Added missing face back to computed source; damaged computed h-vector; incremented computed quotient rank; damaged computed Flores boundary; incremented computed crossing count | 5 faults × 2 modes = 10 |
| Prior audit | Corrupted computed boundary rank/Betti value; dropped a computed filling triangle; dropped a transferred witness cell; cleared computed M partner chain; damaged computed crossing parity | 5 × 2 = 10 |
| Bitmask | Corrupted computed quotient rank; changed a computed affine-circuit coefficient; dropped a computed Flores cell; dropped a returned filling triangle; dropped a transferred cell; damaged computed witness parity | 6 × 2 = 12 |

Nine fresh driver rejection variants each ran under normal and optimized interpreter/child modes: **18/18 intended RuntimeError rejections**. They covered script checksum corruption, expected-output checksum corruption, missing file, directory in place of file, an internal direct symlink, resolved path escaping the package, wrong expected bytes with a coherently updated expected hash, correct stdout accompanied by unexpected stderr with a coherently updated script hash, and a real quotient-rank fault with a coherently updated script hash. The last case reached the program's intended finite rank check and the driver rejected its failed execution; it was not a syntax/import failure.

There were also **two deliberately permitted acceptance probes**: checks/ was an ancestor symlink to an internal actual_checks/ directory holding the same regular program bytes. All resolved paths stayed inside the package, direct control files were regular, and hashes/outputs matched. Both probes were accepted, as expected. This is disclosed rather than counted as a rejection or defect: neither the manuscript nor README/driver promises a security guarantee or a ban on internal ancestor symlinks. These controls demonstrate documented bounded checks, not resistance to every coherent manifest rewrite or hostile environment.

## Canonical metadata and the exact latest global correction

`METADATA_CHECKS.json` compares the complete canonical metadata object, its deposit copy, the preserved round-three accepted metadata/deposit, old/new archive member bytes, and the two authorized safe reconciliation receipts. Metadata and deposit metadata are exactly equal. Title, publication/preprint type, complete description/disclosures, creator/name/affiliation/ORCID, date, version, language, all keyword order/content, open access and CC BY 4.0 all agree with the manuscript and README. Deposit file-list objects retain exactly the reviewed PDF remote filename and supplement name.

Relative to round three, the sole metadata field change is the description's single `d >= 3` becoming `d &gt;= 3`, in both canonical JSON copies. HTML-unescaping gives identical descriptions, and the current description equals the safe recorded server serialization exactly. Every other metadata/deposit field is unchanged. The changed canonical hashes are exactly those in the frozen input and correction receipt. Only three old/new ZIP member byte strings differ: `metadata.json`, `verification/audit_evidence/current_package_corrections.json`, and `SHA256SUMS.json`; membership is unchanged. Removing the one appended `subsequent_live_metadata_encoding` object makes correction history equal its previous object, and that appended object equals `ROUND3_LIVE_METADATA_REPAIR_RECEIPT.json` exactly. Source, PDF, README, every current program/result and every historical input remain prior bytes.

The unchanged PDF hash is `055a6ff8f3451bedc7b75a106329bf2ffd1f02805a568f7f063c13a9b0eb9e59` (96399 bytes); unchanged source hash is `74bb774b46c75deac52e8f77cdb690e30f509c7e5f34b030c69f461f7a6072e1` (26321 bytes). The two deposit files are locally fingerprinted by the existing upload kit's **pure load_manifest** function, imported with bytecode writes disabled. No API client was instantiated; no credentials or saved service state were loaded. The unpublished production draft identifier **23310484** is known only from the explicitly authorized safe receipt; its earlier supplement size/hash are a historical stage, not a claim that the current ZIP has already been uploaded. No fresh live status or publication operation was performed here.

## Earlier corrections, historical stages and attribution/disclosures

After preserving the independent mathematical verdict, I read/reconciled the earlier root mathematical review, correction requirements, bounded mechanism and lineage priority reports, current correction history, historical explanatory addendum/publication notes, reproduction verdict and file-type receipts. The current manuscript incorporates the regular-parameter/infinite-field qualification, restricts overlong parameters to d>=1, handles actual-vertex d=0 separately, includes all induced/open-star/map-agreement hypotheses, says disk **interior**, uses cones in the **old unaugmented** skeleton, and cites the original Weber equality case. Its natural quotient explicitly includes additional nonface relations. The current driver checks direct symlink status on the unresolved path after checking resolved containment. No global standard PL4 sphere/ball assertion appears.

The first hardened author checker/output hashes in historical audit prose describe the earlier output-scope wording. The subsequent correction history records the accompanying-manuscript wording change without numerical changes, and current manifest/receipt hashes bind the final derivative. The original outputs remain historical. Likewise the preliminary root mathematical document explicitly calls itself a checkpoint, and the preserved pending-review author wording and original assertion-based programs are clearly under historical/; the README directs current users to checks/ and the current manuscript. Staged receipts are not promoted to final universal or human-review certificates. No unresolved stale current instruction or false present-byte claim was identified.

The title/abstract/README/metadata make no first-priority or new-general-method claim and explicitly acknowledge extensive AI use, unrefereed status, no independent human peer review, and finite consistency limits. Nevo's 2006 exact conjecture, its journal renumbering, NW's PL-source/TOP-embedding theorem and broader-source conjecture, Adiprasito's existing quotient mechanism, AP's retained-complex completion/familiarity and KX/Weber are credited. The note supplies an explicit actual-PL-class scope extension rather than falsely attributing it as NW's verbatim published theorem.

The preserved priority searches found no documentary earlier full-target resolution in their checked sources. This review does **not** convert that bounded negative finding into novelty/open-status certification. The reports openly retain the Wagner 2013 chapter full-text gap, incomplete discovery indices and unindexed/folklore possibility. Finite controls supply no priority evidence. Any benefit of independent human bibliographic review is recorded as a coverage limitation only; no outreach or draft outreach was prepared.

## Final disposition and exact remaining limits

No blocking proof dependency, complete-package inconsistency, undisclosed byte change, invalid claimed fault rejection or false advertised driver guarantee was found. **Mandatory/blocking/new optional counts are exactly 0/0/0.** The strongest result is a coherent independently reconstructed universal proof using the exact inspected theorem hypotheses, together with exact reproducibility/integrity of this specific frozen package and valid rejection of the specified fresh finite faults. The result remains unrefereed and not formally certified; comprehensive priority and arbitrary-environment security are outside what was established.

`FINAL_INPUT_RECHECK.json` fingerprints all seven frozen top-level files and all 67 selected payloads at completion, checks the freeze copy against the unchanged live freeze bytes and finds every match. `OUTPUT_MANIFEST.json` binds every valid non-private reviewer artifact by byte size/SHA256, excluding itself to avoid self-reference and excluding all private foreign material, extracted fixtures and intentionally invalid programs. Review assignment completion is 100%; that percentage measures completed audit scope, not confidence that mathematics or priority can no longer be challenged.
'''
(HERE/'FULL_PACKAGE_REVIEW.md').write_text(header+math+package+'\nCompleted at '+now+'.\n')
qa={'pages':8,'all_pages_freshly_rendered_and_visually_inspected':True,'per_page':[{'page':i,'path':f'rendered/manuscript-{i}.png','legible':True,'clipping_or_overlap':False,'math_symbols_and_links_usable':True} for i in range(1,9)],'source_pdf':fingerprint(PACKAGE/'manuscript.pdf'),'content_read':'Entire manuscript source and fresh PDF text; all 8 pages inspected','identified_visual_issues':0}
(HERE/'PDF_QA.json').write_text(json.dumps(qa,indent=2,sort_keys=True)+'\n')
with (HERE/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now+' — 100%: concrete full report, exact source/hypothesis ledger, fresh actual fault diagnostics and final unchanged-input recheck completed. Mandatory/blocking/new optional issues 0/0/0. Completion refers to bounded review scope, not formal certainty or novel-priority confidence. Valid artifacts sealed; no live/repository/candidate mutation.\n')
manifest={}
for f in sorted(HERE.rglob('*')):
 if f.is_file() and 'private_sources' not in f.relative_to(HERE).parts and f.name!='OUTPUT_MANIFEST.json':
  manifest[str(f.relative_to(HERE))]=fingerprint(f)
(HERE/'OUTPUT_MANIFEST.json').write_text(json.dumps({'created_at_utc':now,'scope':'All valid non-private round-four reviewer artifacts; excludes itself, ignored foreign texts/renders/extractions and intentionally invalid fixtures.','artifact_count':len(manifest),'artifacts':manifest,'mandatory_issues':0,'blocking_issues':0,'new_optional_issues':0},indent=2,sort_keys=True)+'\n')
print(json.dumps({'completed_at_utc':now,'valid_artifacts':len(manifest),'mandatory':0,'blocking':0,'new_optional':0,'final_frozen_matches':7,'final_payload_matches':67,'report_bytes':(HERE/'FULL_PACKAGE_REVIEW.md').stat().st_size},indent=2))
