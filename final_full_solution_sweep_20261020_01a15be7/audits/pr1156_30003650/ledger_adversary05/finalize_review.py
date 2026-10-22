#!/usr/bin/env python3
"""Seal only this independent offline review directory."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import re

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
write=lambda name,value:(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
files=['RESULTS_NORMAL.json','RESULTS_OPTIMIZED.json','RESULTS_DOCSTRINGS_REMOVED.json']
results=[json.loads((HERE/name).read_bytes()) for name in files]
if any(v['case_count']!=238 or not v['originals_unchanged'] or v['denied_real_service_attempts'] for v in results):
    raise RuntimeError('Unexpected matrix or custody result')
signature=lambda v:[(r['case'],r['expected'],r['passed'],re.sub(r'/case-[^/]+/','/case-FIXTURE/',r['error']) if r['error'] else None,r['state']['append'],r['receipt_saved']) for r in v['results']]
if any(signature(v)!=signature(results[0]) for v in results[1:]):raise RuntimeError('Mode outcomes differ')
failures=[r for r in results[0]['results'] if not r['passed']]
if len(failures)!=26 or any(r['error'] is not None or r['state']['append']!=1 or not r['receipt_saved'] for r in failures):
    raise RuntimeError('Unexpected independent finding shape')
base=[r for r in results[0]['results'] if not r['case'].startswith('independent_')]
if len(base)!=156 or not all(r['passed'] for r in base):raise RuntimeError('Inherited guard regression failed')
pins=results[0]['original_pins']
after={p:{'bytes':len(Path(p).read_bytes()),'sha256':sha(Path(p).read_bytes())} for p in pins}
if after!=pins:raise RuntimeError('Original inputs changed after all modes')
if (AUDIT/'ROOT_LEDGER_REVIEW05_ACCEPTANCE.json').exists():raise RuntimeError('Actual acceptance unexpectedly present')
now=dt.datetime.now(dt.timezone.utc).isoformat()
write('BOUNDARY_RECHECK.json',{'at':now,'all_original_pins_unchanged':True,'original_pins':pins,'root_review05_acceptance_absent':True,'retained_case_fixture_files':list(str(p.relative_to(HERE)) for p in (HERE/'private').rglob('*') if p.is_file()),'external_mutations':0,'real_network_or_process_attempts':0,'git_index_or_ref_operations':0,'note':'Only fixture copies executed. Service responses, account pagination, Git/GWS/GitHub process calls, and public reads were replaced with deterministic functions; a process audit hook rejects actual network/process operations.'})
write('SUMMARY.json',{'at':now,'helper_sha256':results[0]['helper_sha256'],'plan_sha256':results[0]['plan_sha256'],'modes':[{'optimization':v['mode'],'cases':v['case_count'],'expected_outcomes':sum(r['passed'] for r in v['results']),'unexpected_verified_simulated_appends':sum(not r['passed'] for r in v['results']),'originals_unchanged':v['originals_unchanged'],'real_service_attempts':v['denied_real_service_attempts']} for v in results],'base_guard_regression_cases_per_mode':156,'base_guard_regression_all_passed':True,'independent_added_cases_per_mode':82,'independent_adopted_plan_guard_cases_per_mode':8,'same_outcomes_across_modes':True,'finding_count':1,'failing_cases':[r['case'] for r in failures]})
write('VERDICT.json',{'at':now,'reviewer':'ledger_adversary05','review_complete':True,'adopt_for_live_append':False,'blocking_material_findings':[{'id':'L05-1','priority':'P1','location':'reconcile_external_ledger_v5.py:97','title':'Trailing-dot DOI resolver references bypass conservative unresolved-alias gate','minimal_cell':'//shortdoi.org./abc','effect':'A conservative unresolved alias in any ledger column or owned-account metadata is missed; exact full-helper main entry performs one simulated append and emits a verified receipt.','mechanism':'Host regex lookahead excludes a terminal hostname dot. The imported recognizer also ignores this short alias.','reproduced_modes':[0,1,2],'counterexample_variants':26,'required_action':'Recognize resolver trailing-dot authority references and fail closed pending root identity review; rerun whole-helper normal/-O/-OO controls before adoption.','claim_limit':'No asserted actual duplicate, alias resolution, URI equivalence, or live-service outcome.'}],'strongest_verified_result':'All 156 inherited guard regressions and 56 of 82 new independent controls have expected results in each mode. The original bare/protocol-relative v4 gap is repaired. The remaining gap is one trailing-dot resolver-reference family.','input_custody_unchanged':True,'live_helper_executed':False,'actual_external_mutations':0,'scope':'Existing external Ferudun record23350364/concept23350363 only; no new DOI, authorship transfer, chronology, human/global priority, or scientific theorem certification.'})
report='''# Independent existing-publication ledger review05

**Do not adopt v5 for a live append yet. One material conservative alias-guard defect remains.** The full helper and plan were read before prior review artifacts, and the supplied SHA-256 pins match. The prior harness was inspected and adapted only afterward; fresh controls and judgment are independent.

## L05-1 — trailing-dot DOI resolver references escape the alias gate

At `reconcile_external_ledger_v5.py:97`, the new resolver host regex requires the recognized domain to be followed by end-of-text or one of `/ : ? # @ \\`. A hostname dot is absent from that boundary. Consequently `//shortdoi.org./abc`, `https://doi.org./abc`, `doi.org./abc`, `https://www.shortdoi.org./abc`, and `//dx.doi.org.:443/abc` are skipped. The imported names reader also does not flag these short resolver references. Percent-encoding the reference does not close the gap.

The minimal reproduction adds `//shortdoi.org./abc` to the second cell of an otherwise unrelated four-cell ledger row. The exact full v5 source is compiled with the fixture's canonical `__file__` and `__name__='__main__'`; its main entry reaches one simulated GWS append, runs read-back, and saves a verified receipt. The same result occurs with each tested reference in each of the four columns and in owned-account metadata. This is a failure to stop on a conservative unresolved resolver lead. It is **not** evidence that any fabricated suffix actually resolves, identifies this theorem, or duplicates a real ledger record.

Recognize resolver authorities with a trailing dot and stop for root identity review, rather than silently skipping them. Preserve the intentional allowance for a resolver homepage with no identifier and lexical proper long DOI names. Rerun independent whole-helper controls after correction. No live execution is authorized by this report.

## Checkable outcome

Each of normal Python, `-O`, and `-OO` ran **238 whole-helper cases**: **212 expected results and 26 unexpected verified simulated appends**, all in the single defect family above. Outcomes agree across modes. Every one of the **156 inherited guard regression cases** passed, and **56 of 82** new independent cases passed. The eight newly adopted-fixture plan changes fail at the actual destination, attribution/DOI, and PR/problem guards, beyond the earlier immutable-plan hash gate. The helper has no `assert` nodes, and optimization does not remove its checks.

The new v5 guard successfully blocks the four originally reported v4 variants (`//shortdoi.org/abc`, `//doi.org/abc`, bare `shortdoi.org/abc`, and bare `doi.org/abc`), including all four ledger columns and owned-account metadata. Additional undotted scheme, port, www, encoded, non-short-circuit, and harmless long-DOI/home/foreign-host controls behave as expected.

The full passing regression covers externally pinned root acceptance; exact six-module byte snapshots compiled directly, ignoring shadow modules and pyc; one plan read/hash snapshot; complete owned-account pagination and known-record23408971; raw owned IDs/parents/pids/metadata/files, semantic and encoded aliases, and all known MD5s; fresh immutable PR head/base/body and all immediate state flags; 180-second boundary and clock reversal; published record family and metadata, exact three-file inventory and all payload bytes, and DOI destination; live sheet ID/title/gid, four headers and every cell, full ROWS read range; durable exclusive intent with file and directory fsync, races and failures; lost/unknown outcome without blind retry and exact-row recovery; immediate ledger equality; exact nested append response, four cells, spreadsheet/range/ROWS; unique exact final row, matching response range, and preexisting prefix preservation.

## Custody, scope, and reproduction

No actual helper was executed against live services. The complete helper ran only on short-lived private fixture trees. The harness supplies deterministic account/public/GitHub/GWS/Git responses, rejects unforeseen process boundaries, and installs an audit hook denying actual network and process operations. All modes report zero actual service/process attempts and unchanged original input pins. No Git index/ref operations or external writes were performed. Fixture trees were removed; only results and source reconstructing their captured inputs remain. The real `ROOT_LEDGER_REVIEW05_ACCEPTANCE.json` is absent and was never created; acceptance files existed only under the private temporary trees.

The plan has four cells, credits Alper Ferudun, keeps the chat cell empty, uses existing DOI10.5281/zenodo.23350364, records separate Question2 with singular/attainment and direct same-rank coverage, and keeps Question1's general pointwise gap open. It claims no new publication, Alec Kriebel authorship, or chronological firstness. Those mathematical/source conclusions are the root's separately audited premise; this operational review does not replace their proof or certify human/global priority.

Run `offline_whole_helper.py --output <result-name>.json` under normal Python, `-O`, and `-OO`, with bytecode writes disabled. Exit1 is expected for this reviewed v5 because the counterexamples intentionally expose its remaining defect. `SOURCE_PINS.json`, the per-mode results, `IMPORT_CLOSURE.json`, `MINIMAL_COUNTEREXAMPLE.json`, and `BOUNDARY_RECHECK.json` provide the evidence. `MANIFEST.json` binds every retained review payload and excludes only itself and its separate SHA seal.
'''
(HERE/'REPORT.md').write_text(report)
with (HERE/'RESEARCH_LOG.md').open('a') as f:
 f.write(f'- {now}: Final 238-case matrices agree in all three modes: 212 expected outcomes, 26 unexpected verified simulated appends in one trailing-dot alias family. All156 inherited regressions pass; eight adopted-fixture plan controls directly hit the intended guards. All15 original input pins rechecked unchanged; real review05 acceptance remains absent; zero service/process attempts and no retained case trees. Review completion estimate: 100%; live-ledger operational readiness estimate: 95%, pending fail-closed correction and new review. Verdict: do not adopt v5.\n')
# Closed, non-self-referential manifest. A separate SHA seals the manifest bytes.
excluded={'MANIFEST.json','MANIFEST.sha256'}
entries=[]
for p in sorted(HERE.rglob('*')):
 if p.is_file() and p.name not in excluded:
  b=p.read_bytes();entries.append({'path':p.relative_to(HERE).as_posix(),'bytes':len(b),'sha256':sha(b)})
write('MANIFEST.json',{'schema':1,'at':now,'scope':'All retained review payload files; excludes only MANIFEST.json and MANIFEST.sha256 to avoid self-reference.','files':entries})
manifest_sha=sha((HERE/'MANIFEST.json').read_bytes())
(HERE/'MANIFEST.sha256').write_text(manifest_sha+'  MANIFEST.json\n')
for entry in entries:
 b=(HERE/entry['path']).read_bytes()
 if len(b)!=entry['bytes'] or sha(b)!=entry['sha256']:raise RuntimeError('Seal verification failed')
print(json.dumps({'files':len(entries),'manifest_sha256':manifest_sha,'verdict':'blocking_material_finding_L05-1','cases_per_mode':238,'unexpected_verified_simulated_appends_per_mode':26,'input_pins_unchanged':True},indent=2))
