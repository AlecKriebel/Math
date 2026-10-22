#!/usr/bin/env python3
"""Describe and bind completed local operational controls; no remote operations."""
import datetime as dt
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent


def load(name):return json.loads((HERE/name).read_text())
def require(condition,message):
    if not condition:raise RuntimeError(message)


def main():
    modes=[]
    for optimized in [False,True]:
        current=load('CURRENT_CONTROLS_OPTIMIZED.json' if optimized else 'CURRENT_CONTROLS.json')
        old=load('OLD_COUNTEREXAMPLES_OPTIMIZED.json' if optimized else 'OLD_COUNTEREXAMPLES.json')
        prior=load('regression404_'+('optimized' if optimized else 'normal')+'/SUMMARY.json')
        root=load('ROOT_METAMORPHIC_'+('OPTIMIZED' if optimized else 'NORMAL')+'.json')
        resume=load('RESUME_CONTROLS_OPTIMIZED.json' if optimized else 'RESUME_CONTROLS.json')
        require(current['all_controls_passed'] and current['controls']==994,'New controls incomplete')
        require(prior['all404_passed'] and prior['controls']==404,'Old404 incomplete')
        require(resume['all_controls_passed'] and resume['controls']==3,'Resume controls incomplete')
        require(old['old_false_uniqueness_reproductions']==32,'Old counterexamples not preserved')
        require(root['positive_outcomes']['silently_missed']==0 and root['conservative_positive_cases']==296,'Root obligations missed')
        require(len(root['negative_cases'])==7 and all(c['outcome']=='distinct_no_target' for c in root['negative_cases']),'Root nearby negatives failed')
        require(all(x['actual_provider_access_attempts']==0 for x in [current,old,prior,resume]) and root['provider_access']==0,'Actual provider attempted')
        require(all(c['collector_matching_rows']==0 and c['gate_accepted'] and c['append_calls']==1 and c['append_returned_verified'] for c in old['cases']),'Frozen counterexample changed')
        modes.append({'optimization':int(optimized),'new_route_controls':994,'prior_regressions':404,'root_lexical_obligations':303,
          'already_pushed_resume_controls':3,'total_passing_current_controls':1704,'frozen_old_false_uniqueness_reproductions':32,
          'actual_provider_access_attempts':0,'new_case_counts':current['case_counts'],'root_positive_outcomes':root['positive_outcomes']})
    binding=load('CURRENT_HELPER_BINDING.json')
    expected=next(e['sha256'] for e in binding['files'] if e['path']=='ops_binding.py')
    require(all(load('ROOT_METAMORPHIC_'+m+'.json')['source_sha256']==expected for m in ['NORMAL','OPTIMIZED']),'Root controls bound stale source')
    timestamp=dt.datetime.now(dt.timezone.utc).isoformat()
    summary={'timestamp':timestamp,'pr':280,'completion_estimate_percent':100,'publication_ready':False,
          'pending':'NEW COMPLETE history-free whole-package reviewer05 and root decision','modes':modes,
          'scope':'Finite synthetic actual-function controls, not proof of universal URL equivalence or live publication outcome'}
    (HERE/'TEST_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    rows='\n'.join('| '+e['path']+' | '+str(e['bytes'])+' | `'+e['sha256']+'` |' for e in binding['files'])
    report=f'''# PR280 record URL repair

Completed local repair of P280-OPS-04 at {timestamp}. Publication readiness remains **false**. A NEW COMPLETE history-free whole-package reviewer05 and root decision are required. This report makes no scientific-clearance or actual-publication claim.

## Defect and preserved failure

The former record regex omitted singular trailing slash, default port, dot segment and export routes. With any of the four root-confirmed URL forms in any of the four sheet cells, the frozen actual collector found zero matching rows; the frozen gate accepted; the synthetic append added a row; and readback incorrectly declared uniqueness. A contradictory exact root non-target row digest did not stop this. `OLD_COUNTEREXAMPLES.json` and its optimized counterpart preserve all32 failing full-pipeline combinations per mode, with zero actual providers. These were reproduced before canonical edits from the exact frozen seven-helper binding.

The original122 artifacts plus manifest/checksum are reconstructible byte for byte in `pre_record_url_binding/` from `INPUT_PRESERVATION.json` (130 initial files including root finding, suspended clearance, historical true clearance and review04 report/verdict/manifest). `SUPPLEMENTAL_PRESERVATION.json` adds43 files to preserve the remaining complete44 review04 artifacts and checksum. Historical manifests and reviews were not rewritten. Review04's scoped pass predates the root finding and does not authorize this repaired binding.

## Mechanism and exact scope

Four helpers changed; `CURRENT_REPAIR.diff` is the complete diff against the frozen source. `ops_binding.py` now parses bounded URL candidates with the standard URL parser and embeds the shared conservative recognizer within the existing seven-helper contract. `record_url_parser.py` is a development code artifact, not an eighth operational helper.

The recognizer distinguishes exact ASCII official authorities from nearby alien hosts. It handles host ASCII case, bounded default ports, protocol-relative and bare official references, bounded dot segments, repeated/trailing slashes, unreserved percent octets, singular/plural/API record prefixes and subsequent subresources. It takes the whole ASCII numeric route segment as a record lead. Leading zeros in record URLs are conservative aliases; leading zeros and distinct extensions in DOI suffixes remain distinct. Query and fragment do not hide the record path. Nested combinations are exercised.

These are **conservative identity leads**, not assertions that every variant actually resolves or that different URLs are globally equivalent. Root/sibling evidence authenticates particular public routes on a known public record; this agent read the evidence JSON and test source, not the cached remote response bodies, and made no new HTTP requests. Root's296-case metamorphic benchmark is explicitly a finite lexical obligation set, not296 authenticated HTTP equivalences.

Recognized official URLs with unsupported or malformed ports/authority, userinfo, multiple terminal hostname dots, unsupported transport, ambiguous/reserved/nested path encodings, unknown route, absent or malformed ID, root escape or excessive numeric length require explicit identity review. A malformed single-slash official scheme and unreserved-encoded official authority also require review. Unknown recognized shortDOI/resolver aliases remain fail closed, including before a target ID exists. No arbitrary Unicode folding or digit coercion is introduced. Unknown/unrecognized external redirects and arbitrary disguised text remain outside this finite lexical recognizer; nothing here claims universal alias discovery. Official unknown routing can conservatively block an unrelated row until root reviews it.

`prepublication_check.gather` scans **all four cells of every full-sheet row before account search/allocation or a model-term shortcut**. After full account enumeration it compares the precomputed leads to exact target/concept/version-parent IDs. The gate independently scans each lead row before root digest filtering. `record_publication_ledger.matches` scans every cell before its model-pattern shortcut, and existing independent preappend and readback target checks use the same recognizer. A recognized ambiguity cannot be hidden by an earlier matching cell, an exact desired row, or a contradictory non-target digest. Exact literal desired-row idempotence is preserved; an alias-only row is a review conflict, not silently canonicalized into an idempotent result.

The exact path/hash/integer-ID/full account projection requirements for unrelated local state are unchanged; there is no broad new exemption. Directory inventory preservation, original parent/QUEUE row binding, source17 plus selected5 overlay and non-force protections remain unchanged. `repository_integration.py`, `publication_lifecycle.py` and `verify_published_files.py` are byte-identical to the frozen binding.

## Offline validation

Both normal and optimized Python pass **1,704 current controls per mode**:

| Suite | Controls per mode |
| --- | ---: |
| New actual collector/gate/independent append/readback controls | 994 |
| Complete prior regression suite | 404 |
| Root finite lexical benchmark (296 positive obligations and7 nearby negatives) | 303 |
| Already-pushed-head resume verification | 3 |

The994 controls comprise176 complete alias pipelines,176 independent append checks with upstream approval bypassed synthetically,280 ambiguous-route independent append checks,280 collector/gate checks before allocation,57 readback-introduced alias/ambiguity checks,15 nearby distinct identities,7 recognized rejection controls, literal idempotence, genuine absence with one synthetic append, and a later-cell short-circuit check. Every alias/cell check is exercised with and without a contradictory exact root digest exemption. Full pipelines retain actual account-search/gather/reconcile/append/readback bodies; only provider interfaces and specified clearance preconditions are synthetic. Provider/socket/subprocess mutation traps record zero actual attempts.

The404 replay is120+53+73+158. Fixture adapters redirect output/scratch locations and load the current canonical recognizer rather than the old development prototype; prior truthful directory fixtures remain unchanged. No production guard or expected outcome was weakened. Frozen previous DOI/directory failure reproductions inside the old suites remain historical counterexamples. Root benchmark outcomes are295 target leads,1 explicit ambiguity rejection, zero silent misses, and all7 nearby negatives distinct. These finite overlapping checks are evidence, not exhaustive correctness proof.

`resume_path_controls.py` invokes actual `verify-test-merge` at the parent-reported already-pushed head `8aebb819bfac9c12340d2f1469408943549ab530` with synthetic GET-only responses and actual leaf/directory/QUEUE/source guards. It accepts the correct resume, rejects a wrong expected head and rejects a stale merge parent. An initial test-fixture omission lacked the source snapshot after relocating the receipt root; `HARNESS_NOTES.json` preserves that failure and its correction by copying the exact17-file approved snapshot. The actual production snapshot guard was retained.

## Preservation and operational handoff

`PRESERVATION_FINAL.json` verifies all initial130 frozen files, reconstruction of old122, complete44 review04 preservation, all unselected initial inputs, original17, five scientific payloads plus RELEASE, root lead, suspended clearance and prior true clearance history. The complete314-file `.zenodo-state` inventory remains byte-identical, aggregate SHA256 `1d241f0c6e2450ec0df942bf36bfe438f937d5ad530414028b3b47fcf827010b`. No state file was deleted. No Git/index/ref, GitHub/PR, Zenodo, GWS or actual lifecycle operation was performed by this repair agent.

The parent already pushed the branch once. After fresh whole-package review and any newly bound root clearance, resume with `repository_integration.py verify-test-merge --expected-pr-head 8aebb819bfac9c12340d2f1469408943549ab530`; do not rerun `commit` or create a second integration commit. Recheck fresh provider/ledger/account/public-byte gates at every later lifecycle transition using the reviewed workflow. Do not blindly retry a mutation after an uncertain outcome. This is a descriptive future handoff, not execution or permission.

Reproduce from this folder with normal Python and `-O`: `reproduce_old.py`, `current_controls.py`, `replay_404.py`, `resume_path_controls.py`; run the root-owned `private/record_url_metamorphic_controls.py` against this audit's canonical `ops_binding.py` and retain its JSON outside historical sealed folders. Use `PYTHONDONTWRITEBYTECODE=1`. `seal_current.py --verify` checks the final inventory and immutable inputs without provider access. The new manifest binds every authored repair artifact and all seven canonical helpers; previous seals remain historical inputs.

## Current seven-helper binding

| Helper | Bytes | SHA256 |
| --- | ---: | --- |
{rows}

Local repair preparation is100% complete. Publication is pending reviewer05/root decision. Remaining limitations are finite lexical coverage and conservative false blocks on unreviewed recognized routes; no live record has been allocated for PR280 and no live publication/ledger outcome is asserted here.
'''
    (HERE/'REPORT.md').write_text(report)
    (HERE/'RESEARCH_LOG.md').write_text(f'''# PR280 record URL operational repair log

- 2026-10-21T14:13:27Z — 10%: Verified and froze all122 previously bound artifacts, old manifest/checksum, root finding/clearance history and review04 binding before edits. Whole local state inventory captured. Scope is PR280 helper repair only.
- 2026-10-21T14:17:59Z and14:18:00Z — 25%: Reproduced all32 old false-uniqueness pipelines in normal and optimized Python from exact frozen code; no actual provider attempts. Chose a shared structural parser with conservative explicit ambiguity rejection.
- 2026-10-21T14:26:15Z through14:29:09Z — 75%: Initial909 new controls and all404 regressions passed in both modes. Initial resume fixture failed because relocated synthetic receipt root lacked SOURCE_SNAPSHOT.json; retained production guard and corrected fixture using the exact snapshot17.
- 2026-10-21T14:32:40Z and14:32:46Z — 90%: Extended malformed scheme and encoded-authority controls; final994 actual-function route controls pass normal and optimized. No guard is implemented with assert.
- 2026-10-21T14:32:58Z through14:33:00Z — 95%: Final404 regression replay passes both modes; root296+7 lexical benchmark has zero silent misses/false target negatives; existing-head resume3 passes each mode. No real provider access, no Git action.
- {timestamp} — 100% local preparation: Exact four-helper diff and current seven binding recorded, all130 initial copies plus43 supplemental review04 files verified, original17/science5/RELEASE/root lead/clearance history and314 state files unchanged. Publication readyfalse; NEW COMPLETE reviewer05/root decision pending. New seal will bind this report and all authored repair evidence.
''')
    print(json.dumps({'current_controls_per_mode':1704,'frozen_failure_reproductions_per_mode':32,'publication_ready':False}))


if __name__=='__main__':main()
