from pathlib import Path
import datetime as dt,hashlib,json,os
Q=Path(__file__).resolve().parent;B=Q.parent.parent
SOURCE='b8bf6aea20822d53b82af962dd8462a82ff2f71f1f802fc5484ab6d723695fcf'
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
assert sha((B/'coverage_snapshot.py').read_bytes())==SOURCE
m=json.loads((Q/'INPUT_MANIFEST.json').read_text());changed=[]
for e in m['files']:
 p=Q/e['path'];b=p.read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'],e['path'];s=Path(e['source']);current=s.read_bytes()
 if sha(current)!=e['sha256']:changed.append(dict(source=str(s),captured_sha256=e['sha256'],current_sha256=sha(current)))
prior=[]
for e in json.loads((Q/'PRIOR_SEAL_VALIDATION.json').read_text()):
 r=B/'reviews'/e['review'];mb=(r/'OUTPUT_MANIFEST.json').read_bytes();assert sha(mb)==e['manifest_sha256'];d=json.loads(mb)
 for row in d['files']:
  p=r/row['path'];assert not p.is_symlink();b=p.read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256']
 for row in d.get('symlinks',[]):
  p=r/row['path'];assert p.is_symlink() and os.readlink(p)==row['target'] and str(p.resolve())==row['resolved_target']
 prior.append(dict(review=e['review'],files=e['files'],symlinks=e['symlinks'],unchanged=True))
h=json.loads((Q/'HISTORICAL_REPLAY.json').read_text());assert h['executions']==770
f=json.loads((Q/'FOCUSED_CONTROL_RESULTS.json').read_text());assert f['executions']==114 and all(v['control_pass'] for v in f['results'])
save(Q/'CUSTODY_AND_VALIDATION.json',dict(at=now(),source_sha256=SOURCE,canonical_source_unchanged=True,captured_input_files=len(m['files']),all_captured_input_hashes_reverified=True,current_source_changes=changed,prior_output_seals_reverified=prior,scope='Expected source progress is not a claim of atomic live/provider state. No canonical files/provider/Git operations or outside contact performed.'))
verdict=dict(at=now(),verdict='PASS_SCOPED_NO_SUBSTANTIVE_CONCERNS',source_sha256=SOURCE,substantive_findings=[],historical_helper_executions=770,new_focused_helper_executions=114,direct_actual_baseline_executions=2,total_helper_executions=886,asserted_helper_executions=842,exploratory_helper_executions=44,direct_function_checks=44,false_accepts_in_asserted_controls=0,false_rejects=0,remaining_limits=['Read-only local structural consistency only, no live-provider/proof/priority/final-sweep clearance','Source A cells are free prose/ID labels, not canonical catalogue URL schema','URL extraction supports tested sentence and Markdown punctuation; not a general URL authenticity/security parser','Top-level input symlink sandboxing and simultaneous coherent replacement of the entire unkeyed evidence set are outside this contract'],review_completion_estimate_percent=100)
save(Q/'VERDICT.json',verdict)
report='''# Independent accounting-validator review 05

**Verdict: PASS within the stated local structural scope; no remaining substantive concerns.**

Reviewed `coverage_snapshot.py` SHA256 `b8bf6aea20822d53b82af962dd8462a82ff2f71f1f802fc5484ab6d723695fcf`. The canonical source remains unchanged after this review. No paper, publication, spreadsheet, Git state, skill, prior review or canonical input was changed. Every write is in this new review directory. No provider calls or external contact occurred.

## Captured accounting and independent checks

The coherent capture contains606 dispositions, PR9–614 inclusive, next615, highest1446. There are three historical publication dispositions and four effective completed publications: reopened280 replaces its old priority-hold exactly once. Its preserved historical receipt has SHA256 `12786fed27bdc64dc25404de4d559f04611947006cfb62f0ee6e8bf1399009b1`. The old journal is not rewritten.

Independent arithmetic and direct receipt inspection reproduce all four associations: PR292/problem30001608/record23524971/row174; PR397/problem9700002/record23527793/row176; PR399/problem30001179/record23539283/row177; PR280/problem30000156/record23539734/row178. Canonical evidence names, actual source/ID/title labels, primary DOI cells, PR/record links, merge identifiers and root/nested file hashes agree. The legacy292 receipt has its exact unconditional pin; modern roots and nested receipts retain modern archive-manifest evidence. These are local crossartifact checks, not another live-provider or mathematical audit.

## Adversarial reproduction

All four previous output seals were checked before capture and rechecked after testing:1395,2934,5531 and6803 regular files, with respectively0,0,1 and2 separately inventoried symlinks. They remain unchanged. Historical harnesses, their expectations, source inputs and saved outcomes were preserved. Full recursive fixture inputs were copied into this review; only the code under test was replaced by the current source.

The unchanged historical programs performed770 helper executions:368 original/review02,20 supplementary,206 review03,176 review04. The review04 source-prose substitutions retain their original assertions and results but are interpreted as exploratory under its sealed `CONTROL_ADJUDICATION.json`. This is not a newly invented canonical catalogue-URL requirement. Together with earlier explicit probes,44 historical executions are exploratory.

A new independently written harness adds57 full-report cases in each of normal and optimized Python,114 executions. It tests valid space-delimited, quoted, parenthesized, autolink and Markdown PR links for all four publications; invalid word/Unicode prefixes, relative and foreign URL prefixes, numeric extensions and query suffixes; same-content symlinks for ordinary and reopened dispositions, publication receipts, a ledger receipt and an audit ancestor directory. All asserted cases behave correctly. In particular both review04 findings are repaired: embedded invalid URL schemes do not become canonical links, and ordinary saved dispositions now receive the same safe evidence-path checks.

Two direct actual-baseline helper runs also pass, one per Python mode. The total is886 helper executions:842 asserted and44 exploratory, with zero asserted false acceptances and zero false rejections. An additional44 direct function checks exercise URL boundaries and modern download/archive-manifest rejection. Direct checks are not counted as separate helper executions or independent scientific instances.

## Remaining scope limits

This report establishes local structural consistency. It does not authenticate public bytes, scientific correctness, historical priority, arbitrary source-label prose, or final sweep completion. The emitted final-reconciliation flag remains false. Positive ledger source cells are actual free-text source/ID/title labels. General prose semantics cannot be inferred from a numeric token, and no contrary schema is imposed.

The URL recognizer supports the tested prose and Markdown punctuation; it is not a general URL-authenticity or security parser. Top-level input sandboxing and simultaneous coherent replacement of an entire unkeyed trust set are outside the stated contract. These limits do not leave a material objection to the actual four-publication accounting or the repaired guarantees.

## Custody and reproduction

`INPUT_MANIFEST.json` binds exact captures. `REPLAY_MOUNTS.json` records the deliberate current-code mounts. Before any replay, a capture-manifest bookkeeping issue was corrected by preserving each historical code file separately and pointing its input entry to those exact bytes; no historical test logic, expectation or prior output was changed. `replay_historical.py`, `focused_controls.py` and `inspect_accounting.py` record the checks and actual stdout/stderr. Run reproduction on a separate copy; this sealed directory must stay unchanged. Source progress after capture is disclosed in `CUSTODY_AND_VALIDATION.json` rather than treated as corruption.

`OUTPUT_MANIFEST.json` seals every regular output except itself and records symlinks separately. Raw fixture captures remain local. A public projection may contain the report, verdict, manifests, custody, scripts and aggregate results without redistributing its full fixture corpus. Review completion:100%; overall sweep completion is not asserted.
'''
(Q/'REPORT.md').write_text(report)
p=Q/'RESEARCH_LOG.json';log=json.loads(p.read_text());log.append(dict(at=now(),completion_estimate_percent=100,event='770 historical plus114 independent focused plus2 actual baseline helper executions complete.842 asserted and44 exploratory,0 asserted false accepts/rejects.44 additional direct function checks pass. All four prior seals reverified unchanged; bounded review passes with no substantive concerns.'));save(p,log)
files=[];links=[]
for p in sorted(Q.rglob('*')):
 if p.name=='OUTPUT_MANIFEST.json' and p.parent==Q:continue
 if p.is_symlink():links.append(dict(path=str(p.relative_to(Q)),target=os.readlink(p),resolved_target=str(p.resolve())))
 elif p.is_file():
  b=p.read_bytes();files.append(dict(path=str(p.relative_to(Q)),bytes=len(b),sha256=sha(b)))
save(Q/'OUTPUT_MANIFEST.json',dict(at=now(),files=files,symlinks=links,note='Every regular review output except this manifest; symlink targets are inventoried without following the link as a separate file. Private fixture captures remain local.'))
print(json.dumps(dict(verdict=verdict['verdict'],files=len(files),symlinks=len(links),manifest_sha256=sha((Q/'OUTPUT_MANIFEST.json').read_bytes()),current_source_changes=changed)))
