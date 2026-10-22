"""Seal the completed independent review, with final byte checks."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,zipfile,shutil
D=Path(__file__).resolve().parent;C=D.parent
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def pin(p,base):return dict(path=p.relative_to(base).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes()))
# Only a checkable duplicate of a zero-byte owned lock is compacted here.
folder=D/'lock_control';files={p.relative_to(folder).as_posix():p for p in folder.rglob('*') if p.is_file()}
zpath=D/'LOCK_CONTROL.zip'
with zipfile.ZipFile(zpath,'x',compression=zipfile.ZIP_DEFLATED) as z:
 for name,p in sorted(files.items()):z.write(p,name)
with zipfile.ZipFile(zpath) as z:
 assert len(z.namelist())==len(files) and set(z.namelist())==set(files) and z.testzip() is None
 assert all(z.read(n)==p.read_bytes() for n,p in files.items())
shutil.rmtree(folder)
freeze=json.loads((D/'FROZEN_SOURCES.json').read_bytes());sourcechecks=[]
for row in freeze['rows']:
 for p in [D/row['path'],C/'publication'/row['path']]:assert p.stat().st_size==row['bytes'] and sha(p.read_bytes())==row['sha256']
 sourcechecks.append(dict(**row,current_candidate_matches=True,frozen_copy_matches=True))
science=json.loads((D/'SCIENTIFIC_PACKAGE_FREEZE.json').read_bytes())
assert sorted(r['path'] for r in science['rows'])==sorted(p.relative_to(C/'preprint').as_posix() for p in (C/'preprint').rglob('*') if p.is_file() and not p.is_symlink())
for row in science['rows']:
 p=C/'preprint'/row['path'];assert p.stat().st_size==row['bytes'] and sha(p.read_bytes())==row['sha256']
assert len(science['rows'])==230
zchecks=[]
for p in sorted(D.glob('FIXTURE_*.zip')):
 mp=p.with_name(p.stem+'_MANIFEST.json');m=json.loads(mp.read_bytes());assert m['archive']==pin(p,D)
 rows=m['files'];byname={r['path']:r for r in rows};assert len(byname)==len(rows)
 with zipfile.ZipFile(p) as z:
  assert len(z.namelist())==len(rows) and set(z.namelist())==set(byname) and z.testzip() is None
  for name,r in byname.items():
   raw=z.read(name);assert len(raw)==r['bytes'] and sha(raw)==r['sha256']
 zchecks.append(dict(archive=pin(p,D),payloads=len(rows),exact_set_CRC_every_body_SHA256=True,initial_uncompressed_equality_manifest=pin(mp,D)))
assert not any(p.is_file() for p in (D/'fixtures').rglob('*'))
first=json.loads((D/'CONTROLS_EXIT.json').read_bytes());additional=json.loads((D/'ADDITIONAL_EXIT.json').read_bytes());corruption=json.loads((D/'CORRUPTION_EXIT.json').read_bytes())
assert first['actual_exit']==0 and additional['actual_exit']==1 and corruption['actual_exit']==0
cr=json.loads((D/'RECEIPT_CORRUPTION_RESULT.json').read_bytes());assert cr['all6_corruptions_accepted'] is True
inputs=[C/'initial_review_20261016/ROOT_RELEASE_HELPER_REVIEW01_RESOLUTION.json',C/'initial_review_20261016/ROOT_RELEASE_HELPER_REVIEW02_RESOLUTION.json',C/'release_helpers_adversary_01/ASSESSMENT.json',C/'release_helpers_adversary_01/AUTHORED_MANIFEST.json',C/'release_helpers_adversary_02/ASSESSMENT.json',C/'release_helpers_adversary_02/AUTHORED_MANIFEST.json',C/'publication/binding_repair_02/AUTHORED_MANIFEST.json',C/'publication/native_repair_02/AUTHORED_MANIFEST.json']
assert pin(inputs[1],C)['sha256']=='4b58338b848aef5e0681541a98863f0722358ee5574c384ebb687bf68890d4db'
dump(D/'INPUT_AUTHORITY_PINS.json',dict(utc=utc(),files=[pin(p,C) for p in inputs]))
completed=utc()
report=r'''# Release helper adversarial review 03

**REPAIRS_REQUIRED: one mandatory finding, zero optional findings.** Reviewer: `release_helpers_adversary_03`. Case checkpoint remains **65%**; this review is complete. No actual publication, tracker append, native write, or release clearance is authorized by this report.

The six exact candidate files were frozen at 2026-10-16T07:34:00.430766Z, after the actual review02 root resolution at 07:32:02.019872Z. The independent workflow contract and eight source hypotheses were recorded before reading any candidate implementation or prior source reports. The first parent milestone preceded prior-report intake. `FROZEN_SOURCES.json` lists the ordered normalized six source identities; every current candidate and frozen copy was rechecked at completion.

## Mandatory finding RH209-03-M01

**Existing completion receipts are accepted with unchecked contradictory or incorrect facts.** In `verify_and_merge.py:326–338`, `complete_merge` compares only eleven selected keys of an existing `PR_MERGED.json`, freshly checks native provider state, then returns the entire old object. The locally rederived receipt at lines312–324 contains many additional static fields. The old DOI, tracker range, merged/completion flags, percentage and body pins are not compared. Fresh provider checks validate current facts but do not authenticate those omitted old fields.

The counterexample changes just one generated completion artifact at a time, after a completely successful synthetic preparation and merge. It leaves all scientific bytes, clearance/review seals, publication/tracker ancestry, durable once-intents, prepared records, provider state and eleven compared keys unchanged. The source itself supplies a deductive counterexample: the changed field is not referenced before returning `old`; `PR_MERGED.json` is also excluded from the public scientific packet, so no prior packet pin detects its change.

`receipt_corruption_probe.py` additionally reproduced all six variants against the byte-exact compiled candidate, using only provider/path substitutions. It first called the real preparation and merge workflow, then independently reloaded the actual prepared authority, progress baseline and merge ancestry with the real helper functions. It called exact `complete_merge` after each one-field alteration. Every call ran the actual local binding, fresh public/tracker readbacks, complete native tree/body checks and final native refresh; none changed providers. Each call successfully returned the corrupt value, leaving the corrupt retained bytes unchanged:

| Field | Accepted incorrect value |
|---|---|
| `doi_url` | `https://doi.org/10.5281/zenodo.999999999` |
| `tracker_range` | `'Wrong tab'!Z999:AC999` |
| `case_completion_percent` | `1` |
| `actual_publication_tracker_native_merge_complete` | `false` |
| `exact_native_body_readbacks` | `[]` |
| `merged` | `false` |

This program genuinely exited **0**. That exit confirms the counterexample was observed, not that the candidates are clean. See `RECEIPT_CORRUPTION_RESULT.json`, `CORRUPTION_EXIT.json`, raw `corruption.stdout.jsonl`/`corruption.stderr.txt`, and `FIXTURE_receipt_corruption_final.zip` with its exact membership/CRC/every-body manifest. The archive includes the generated legitimate receipt, each changed receipt, all outcomes and raw provider observations. Candidate functions, source text and AST were never rewritten.

**Required repair:** validate every static completion-receipt fact against independently rederived authority before accepting an existing receipt, including identity/URLs, exact queue/body pins, attempt/history, flags, percentage, counts/scope and local-mutation facts. Explicitly distinguish historical dynamic evidence and timestamps from freshly observed evidence; validate its retained bindings, schema and chronology as applicable. Preserve immutable existing evidence, reject corruption without overwriting it or retrying any provider write, and obtain a new independent review of the repaired exact six sources. This finding concerns accepted completion-record correctness; the test does not show an extra native write or a wrong actual scientific merge.

## Verified guarantees and prior dispositions

The complete first program genuinely exited **0**. It authenticated the real current seven-core scientific bindings and the exact211-member source archive, checked every member against `SOURCE_MANIFEST.json` through actual `frozen_source`, and independently verified all23 original archives against intake size/SHA256/native-blob/mode pins. It executed actual review-chain parsing for both scientific reviews (result2/1). It authenticated both historical helper assessment/manifests, all13 actual finding dispositions and repaired-source chronology, using an explicitly synthetic third parser successor (result3/1). That successor is a parser control and grants no review or release authority.

The source review challenged the entire workflow, rather than only the latest regressions:

- Prior M01: actual sealed chronological scientific/helper review chains and exact current bindings are required; counters alone are insufficient.
- Prior M02: stage/inspect/publish/provider/public-byte and append-intent ancestry is independently validated. DOI version identity and resolution are bound.
- Prior M03: exact all-four-cell target and full-grid unique problem/DOI scans are required, including read-only recovery.
- Prior M04/M05: explicit public exports, exact ZIP/source bytes,23 original members, native modes/bodies and full changed scope are derived independently from current clearance and receipts. Extra native members, missing members and executable-mode substitution were rejected in new controls.
- Prior M06: exact canonical PR title/body are revalidated; one-whitespace changes failed. Actual late body changes remained pending.
- Prior M07 and O01–O03: main overlays preserve foreign scope and exact target QUEUE changes, complete trees avoid compare-file caps, object/ref/metadata/ready/main intents precede their corresponding writes, counts derive from the authenticated baseline, and tracker version/date derive from cleared metadata. Source inspection supports these mechanisms. The new full terminal control independently completed one synthetic actual merge and recovered read-only to45/22/22/0 exactly once.
- Review02 M01: a canonical finite1115-row grid response with trimmed trailing rows was accepted. Boolean/negative/undersized grid bounds, duplicate gid metadata, oversized rows/value coverage, missing/corrupt range coverage, COLUMNS, leading-zero/row1/mismatched/unquoted targets were rejected.
- Review02 M02: a real local invalid-UTF8 child preserved exact binary stdout/stderr before decode failure. An HTTP cursor that emitted two chunks then `IncompleteRead.partial` retained every available byte. These observations supplement the source inspection of all three binary readers and the authenticated prior repair evidence.
- Review02 M03: the final native refresh correctly rejected late body, merge-event and non-containing-main changes after long publication reads. A prior successful synthetic main PATCH with an unknown response left both write-capable modes disabled; read-only recovery produced the derived counts once, and another read-only run left its accepted receipt immutable. The separate existing-receipt comparison still has M01 above.

All six actual local optimized-Python processes exited1 before action; a provider-trapped normal import of all six exited0 with no provider calls. The initial terminal suite's lock check hit the earlier already-verified guard; it therefore did not prove lock exclusion. The subsequent distinct direct second acquisition of the actual shared lock correctly failed with `Another release stage is active`. This correction is explicit in `ADDITIONAL_RESULTS.json` and does not infer the stronger observation from the first check.

The actual manuscript/metadata retain exact contemporary Ferudun v1.1 Theorem2/Section6 credit, DOI10.5281/zenodo.23088516, and the older mechanisms. The domain remains the signed outer tangent polygon and true center-perpendicular feet on boundary tangent lines, strict nondegenerate confocal ellipses, periods not divisible by4, admitted coprime stars/reversal/fixed repeats and a separate circle case. No firstness, novelty, historical non-derivation/independence or current-worldwide-open claim was added. These claims were authenticated against the already reviewed package; this source review is not another proof/priority or scientific whole-package review.

## Storage, reproducibility and limits

`additional_controls.py` genuinely exited **1**. Its direct lock control passed. A stage-unknown control reached first-stage/second-attempt rejection, then a harness-only inherited trace method required absent `native_calls`; the remaining once-path matrix was not completed and is not counted as passing. Its first receipt-corruption setup encountered real ENOSPC before reaching corruption. No semantic rejection or defect is inferred from that storage failure. Both raw streams and exit metadata are preserved. Later shell retry creation and compactor ZIP-open attempts also failed with ENOSPC; no nonexistent retry program/result is claimed.

After the parent made space by verifying and compacting only root-owned duplicates, this reviewer compacted both owned interrupted fixtures. Every original file and raw failure was retained in ZIP only after exact-member/CRC/every-body SHA256 and original-byte equality verification. The final concrete corruption program then completed with exit0. Its raw fixture was also compacted by that full check. Final validation reread every ZIP member and rechecked all six current/frozen candidates plus all230 scientific files; no scientific byte or candidate changed.

The strongest conclusion is a whole-six-source end-to-end review with one reproducible retained-completion-record defect. Positive provider controls are synthetic authority only; no actual GitHub/GWS/Zenodo/network call, local Git/index/ref change, environment/cache/secret mutation, release, clearance or scientific edit occurred. This review assumes ordinary trusted local anchors and provider identity; it does not certify future permissions/rules, globally atomic cross-service snapshots, dependency implementations, absolute priority, human peer review or universal mathematical truth. No external individual was contacted. No proof or numerical result is strengthened by the synthetic controls.
'''
(D/'REPORT.md').write_text(report)
finding=dict(id='RH209-03-M01',classification='mandatory',status='open',title='Existing completion receipt accepts incorrect unvalidated static facts',source='verify_and_merge.py',source_lines=[326,338],reproducer='receipt_corruption_probe.py: successful full synthetic preparation/merge, exact authority reload, then exact complete_merge under six one-field PR_MERGED corruptions; all six accepted with zero provider mutations',evidence=['RECEIPT_CORRUPTION_RESULT.json','CORRUPTION_EXIT.json','corruption.stdout.jsonl','FIXTURE_receipt_corruption_final.zip','FIXTURE_receipt_corruption_final_MANIFEST.json'],required_fix='Authenticate every static field of an existing completion receipt against rederived authority and validate historical dynamic evidence separately; preserve corrupt bytes and reject read-only without any retry. Obtain a NEW exact-source independent review.')
a=dict(schema='pr209-release-helper-assessment-v1',reviewer='release_helpers_adversary_03',completed_utc=completed,verdict='REPAIRS_REQUIRED',frozen_sources=freeze['rows'],mandatory_findings=[finding],optional_findings=[],case_completion_percent=65,helper_audit_completion_percent=100,scope=dict(frozen_utc=freeze['frozen_utc'],independent_contract='WORKFLOW_CONTRACT.md',source_text_or_AST_rewrites=False,provider_and_path_substitutions_only=True,no_actual_provider_calls=True,no_candidate_or_scientific_modifications=True,no_release_authority=True),verification=dict(initial_program_actual_exit=0,additional_program_actual_exit=1,additional_harness_and_storage_failures_preserved=True,final_corruption_program_actual_exit=0,corruptions_reproduced=6,actual_zip_payloads=211,actual_originals=23,actual_whole_review_chain=[2,1],actual_two_helper_seals_and_all13_dispositions_authenticated_with_synthetic_successor=True,all230_scientific_files_unchanged=True,all6_current_and_frozen_sources_match=True,all_fixture_zip_members_CRC_SHA256_and_original_equality_checked=True),report='REPORT.md')
dump(D/'ASSESSMENT.json',a)
validation=dict(utc=utc(),frozen_sources=sourcechecks,scientific_files_verified=230,scientific_unchanged=True,archives=zchecks,lock_archive=pin(zpath,D),lock_archive_exact_set_CRC_every_body_original_equality=True,actual_child_exits=dict(initial=0,additional=1,corruption=0),mandatory_findings=1,optional_findings=0,no_release_authority=True)
dump(D/'FINAL_VALIDATION.json',validation)
with (D/'RESEARCH_LOG.md').open('a') as log:
 log.write('- '+completed+' — Review100%; case65%. Actual211ZIP/23originals, real2whole and2helper seals/all13 prior dispositions authenticated; current6 and all230 B bytes unchanged. Initial childexit0, additional childexit1 (documented harness/storage interruptions), concrete corruption childexit0. One mandatory RH209-03-M01 independently reproduced in six variants; zero optional. Owned fixture ZIP exact members/CRC/every-body SHA256/original equality checked before duplicate removal. No actual release authority.\n')
# Source and science final checks immediately before author manifest construction.
for row in freeze['rows']:assert sha((C/'publication'/row['path']).read_bytes())==row['sha256']==sha((D/row['path']).read_bytes())
for row in science['rows']:assert sha((C/'preprint'/row['path']).read_bytes())==row['sha256']
rows=[]
for p in sorted(D.rglob('*')):
 if not p.is_file():continue
 assert not p.is_symlink()
 if p==D/'AUTHORED_MANIFEST.json':continue
 r=pin(p,D);assert 'private_transport' not in Path(r['path']).parts;rows.append(r)
manifest=dict(schema='pr209-authored-manifest-v1',reviewer='release_helpers_adversary_03',sealed_utc=utc(),self_excluded=True,files=rows)
dump(D/'AUTHORED_MANIFEST.json',manifest)
for row in rows:
 p=D/row['path'];assert p.stat().st_size==row['bytes'] and sha(p.read_bytes())==row['sha256']
print(json.dumps(dict(assessment=pin(D/'ASSESSMENT.json',D),manifest=pin(D/'AUTHORED_MANIFEST.json',D),sealed_payloads=len(rows),verified_fixture_archives=len(zchecks),mandatory_findings=1,optional_findings=0,case_completion_percent=65),indent=2),flush=True)
