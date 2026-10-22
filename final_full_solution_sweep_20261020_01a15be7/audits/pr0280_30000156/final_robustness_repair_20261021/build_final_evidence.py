#!/usr/bin/env python3
"""Final local v1.1 proof/package/operations custody; no external mutations."""
import datetime as dt
import difflib
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent;AUDIT=HERE.parent;ROOT=AUDIT.parents[1];REPO=ROOT.parent
HISTORY=AUDIT/'preprint/release_history/release02_pre_all_odd_prime_robustness_20261021'
FROZEN=AUDIT/'ops_bibliographic_context_repair_20261021/pre_bibliographic_binding'
PUB=AUDIT/'preprint/publication'
HELPERS=['ops_binding.py','prepublication_check.py','publication_live_gates.py','repository_integration.py',
         'publication_lifecycle.py','record_publication_ledger.py','verify_published_files.py']
RELEASE='da0388503e1c6f03c809ec256989d10039b1f1a1b2eba87528d77651a7863e60'
LEAD='3678face65a98b0c8f593877165b096993928393deee6ce1b2cf08e357363add'
OLD_LEAD='4db5e01602ed978612c58aaa1736cd894a8b4123f7de7c6d51e14a344546febb'


def sha(b):return hashlib.sha256(b).hexdigest()
def load(path):return json.loads(path.read_text())
def ck(v,m):
    if not v:raise RuntimeError(m)
def write(name,value):(HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def entry(path):
    ck(path.is_file() and not path.is_symlink(),'Unsafe file '+str(path))
    raw=path.read_bytes();return {'path':path.relative_to(AUDIT).as_posix(),'bytes':len(raw),'sha256':sha(raw)}
def matches(path,e):return path.is_file() and not path.is_symlink() and path.stat().st_size==e['bytes'] and sha(path.read_bytes())==e['sha256']


def verify_preserved():
    before=load(HERE/'INPUT_PRESERVATION.json')
    for e in before['files']:ck(matches(AUDIT/e['path'],e),'Preserved initial input changed')
    for e in load(HERE/'SUPPORT_INPUT_PRESERVATION.json')['files']:
        ck(matches(HERE/'before'/e['path'],e),'Preserved support input changed')
    for e in load(HERE/'BRANCH_RECEIPT_CUSTODY.json')['files']:
        ck(matches(AUDIT/e['path'],e) and matches(HERE/'before'/e['path'],e),'Root branch receipt changed')
    reconstructed=[]
    for rel,pinned,count in [('ops_record_url_repair_20261021/MANIFEST.json','b12e7262026d780029a7eeee1fb8d0c8a514c4a2ab382faadebad40a84dba55d',390),
                              ('ops_bibliographic_context_repair_20261021/PROPOSAL_MANIFEST.json','9fe9a074277ca7ff4de522cc079647b3c3fdaa812848e902afa44af30fb499b3',451)]:
        manifest=AUDIT/rel;ck(sha(manifest.read_bytes())==pinned,'Historical seal changed')
        files=load(manifest)['files'];ck(len(files)==count,'Historical inventory changed');substitutions=[]
        for e in files:
            actual=AUDIT/e['path']
            if matches(actual,e):continue
            candidates=[FROZEN/e['path'],HERE/'before'/e['path']]
            if e['path'].startswith('preprint/publication/'):candidates.append(HISTORY/Path(e['path']).name)
            found=next((p for p in candidates if matches(p,e)),None)
            ck(found is not None,'Cannot reconstruct historical '+e['path'])
            substitutions.append({'historical_path':e['path'],'preserved_path':found.relative_to(AUDIT).as_posix(),'sha256':e['sha256']})
        reconstructed.append({'manifest':rel,'manifest_sha256':pinned,'all_entries_reconstructed':count,
                              'current_paths_changed_not_relabelled_unchanged':substitutions})
    ck(sha((PUB/'RELEASE_FILES.json').read_bytes())==RELEASE,'Current scientific release changed')
    ck(sha((AUDIT/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json').read_bytes())==LEAD,'Current root lead changed')
    old=HERE/'before/ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json'
    ck(sha(old.read_bytes())==OLD_LEAD and (AUDIT/'publication_clearance_history/lead01_pre_scope_extension.json').read_bytes()==old.read_bytes(),'Old trusted decision history changed')
    current=load(AUDIT/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json');prior=load(old)
    for key in ['account_leads','ledger_leads','unrelated_local_state_exemptions','unresolved_leads']:
        ck(current[key]==prior[key],'Semantic root exemption changed')
    ck((AUDIT/'ROOT_PUBLICATION_CLEARANCE.json').read_bytes()==(HERE/'before/ROOT_PUBLICATION_CLEARANCE.json').read_bytes(),'False root clearance changed')
    ck(load(AUDIT/'ROOT_PUBLICATION_CLEARANCE.json')['publication_ready'] is False,'Root clearance must remain false')
    snapshot=load(AUDIT/'SOURCE_SNAPSHOT.json');ck(len(snapshot['files'])==17,'Original inventory changed')
    for e in snapshot['files']:
        ck(matches(AUDIT/e['snapshot'],{'bytes':e['bytes'],'sha256':e['sha256']}),'Original17 changed')
    state=REPO/'.zenodo-state';ck(not any(p.is_symlink() for p in state.rglob('*')),'State symlink changed')
    inventory=[{'path':p.relative_to(REPO).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(p for p in state.rglob('*') if p.is_file())]
    digest=sha(json.dumps(inventory,sort_keys=True,separators=(',',':')).encode())
    ck(len(inventory)==314 and digest=='1d241f0c6e2450ec0df942bf36bfe438f937d5ad530414028b3b47fcf827010b','Whole local state inventory changed')
    return {'historical_reconstruction':reconstructed,'state':{'files':314,'inventory_sha256':digest},
            'root_current_lead_sha256':LEAD,'old_lead_preserved_sha256':OLD_LEAD,'root_clearance_unchanged_false':True,
            'source17_unchanged':True,'branch_receipts_unchanged':True}


def main():
    preserved=verify_preserved();now=dt.datetime.now(dt.timezone.utc).isoformat()
    for label in ['normal','optimized']:
        ck(load(HERE/('canonical_controls_'+label)/'SUMMARY.json')['all2971_passed'],'Old2971 not complete')
    for suffix in ['', '_OPTIMIZED']:
        rev=load(HERE/('REVISION_CONTROLS'+suffix+'.json'));doi=load(HERE/('DOI_DESTINATION_CONTROLS'+suffix+'.json'))
        ck(rev['all_passed'] and rev['controls']==38 and doi['all_passed'] and doi['controls']==125,'New operation controls incomplete')
        ck(rev['actual_provider_attempts']==doi['actual_provider_attempts']==0,'Provider attempted')
        ck(rev['helper_sha256']==sha((AUDIT/'repository_integration.py').read_bytes()),'Revision tests stale')
        ck(doi['current_verifier_sha256']==sha((AUDIT/'verify_published_files.py').read_bytes()) and doi['current_appender_sha256']==sha((AUDIT/'record_publication_ledger.py').read_bytes()),'DOI tests stale')
    binding={'timestamp':now,'publication_ready':False,'release_manifest_sha256':RELEASE,'root_lead_sha256':LEAD,
             'files':[entry(AUDIT/n) for n in HELPERS]}
    write('CURRENT_HELPER_BINDING.json',binding)
    write('PRESERVATION_FINAL.json',{'timestamp':now,**preserved,'no_actual_provider_git_ledger_mutations':True})
    write('CURRENT_RELEASE_BINDING.json',{'release_manifest':entry(PUB/'RELEASE_FILES.json'),'files':load(PUB/'RELEASE_FILES.json')['files'],
        'version':'1.1','members':69,'payloads':68,'publication_ready':False})
    (HERE/'CANONICAL_HELPERS.diff').write_text(''.join(''.join(difflib.unified_diff((HERE/'before'/n).read_text().splitlines(True),
       (AUDIT/n).read_text().splitlines(True),fromfile='before/'+n,tofile=n)) for n in HELPERS))
    (HERE/'MANUSCRIPT.diff').write_text(''.join(difflib.unified_diff((HERE/'before/preprint/main.tex').read_text().splitlines(True),
       (AUDIT/'preprint/main.tex').read_text().splitlines(True),fromfile='before/preprint/main.tex',tofile='preprint/main.tex')))
    reviewed=AUDIT/'ops_bibliographic_context_repair_20261021/proposed/ops_binding.py'
    (HERE/'RELEASE_CONSTANTS_ONLY.diff').write_text(''.join(difflib.unified_diff(reviewed.read_text().splitlines(True),(AUDIT/'ops_binding.py').read_text().splitlines(True),
          fromfile='reviewed417f_ops_binding.py',tofile='current_ops_binding.py')))
    write('TEST_SUMMARY.json',{'timestamp':now,'operations_per_mode':3134,'operations_parts':[2971,38,125],'normal_and_optimized_pass':True,
        'archive_guard_controls_total':22,'class3_checks_per_replay':147619,'all_odd_checks_per_replay':46298,'odd_primes':167,
        'class1_primes':80,'class3_primes':87,'pdf_pages_rendered_and_viewed':8,'publication_ready':False,'pending':'NEW COMPLETE history-free whole-package reviewer06 and root reproduction/decision'})
    write('HARNESS_NOTES.json',{'development_failures_retained_as_notes':[
      'The DOI fixture initially had a dictionary-key syntax typo; neither mode executed until corrected.',
      'The first actual verify_live->append positive control detected a production draft variable-name collision: a download-loop destination string replaced the new DOI-resolution object. Renamed the DOI object; all actual-function positive/negative controls then passed.',
      'PDF bbox XML contained a PDF control character; sanitized only the analysis copy for bounding-box extraction. No PDF/source change. Root independently measured the same531.21pt bound.'],
      'actual_provider_attempts':0,'old_counterexamples_preserved':True})
    hashes='\n'.join('| '+e['path']+' | `'+e['sha256']+'` |' for e in binding['files'])
    release_hashes='\n'.join('| '+e['path']+' | '+str(e['bytes'])+' | `'+e['sha256']+'` |' for e in load(PUB/'RELEASE_FILES.json')['files'])
    (HERE/'REPORT.md').write_text(f'''# PR280 final v1.1 robustness and operations repair

Completed {now}; local preparation 100%. **Publication readyfalse.** NEW COMPLETE history-free whole-package reviewer06 plus root reproduction/decision remain required. No provider, Git/index/ref, branch, PR, GWS or actual lifecycle mutation was performed. Current branch still has the parent-reported old five at8aebb819bfac9c12340d2f1469408943549ab530; no new branch outcome is claimed.

## Mathematical scope and package

Version 1.1 prints a separate all-odd-prime proposition. On the invariant regular domain of size p(p-r), r in{{0,2}}, the zero-extended primitive indicator has principal term(p-r)theta. The character/Jacobi proof gives |P/p-theta|<=r theta/p+theta(2^omega-1)/sqrt(p)<=2/p+64p^(-1/4), uniformly through all odd primes. Exact regular CDF/ramp formulas use denominator p(p-r). Uniform-point exceptional deletion or arbitrary finite nonnegative assigned periods only there add mass at most r/p, so [0,1]-valued statistics differ by at most r/p and general bounded statistics by at most2||f||infinity r/p. Measures live on nonnegative reals; assigned periods may exceed p, and the ramp is globally bounded continuous. The credited atomless whole-prime scalar law excludes convergence on every positive-upper-prime-density set under these specified conventions.

The original class 3 full-affine theorem is byte-identical, including its limsup1 and liminf-at-most23/24 bound. Class 1 full-affine maps remain nonpermutations. The manuscript does not claim a unique source convention for nonperiodic points. All priority, unrecovered2011-source, established-input and extensive-AI/unrefereed/no-human-review caveats remain.

The source/archive now supplies separate46,298 exact all-odd controls over167 primes through1000 (80 class 1,87 class 3), including10,178 raw regular graph points and assigned periods beyond p. The original147,619-check receipt remains a separate unchanged checker. Both replay in normal/-O;22 archive guard cases reject source/extension/baseline tampering, missing/extra/symlink/traversal/duplicate entries and boolean/float manifest schema substitutions. An isolated local builder reproduced all five payload bytes exactly. ZIP has69 safe members,68 hashed payloads, exactly17 byte-preserved originals and no third-party full source/account/credential bodies. Exactly two intended uploads remain PDF and ZIP.

All eight revised PDF pages were rendered and individually viewed. No clipping/overlap/missing glyph defect was found. Root independently reviewed all eight. Section5 heading ends at531.21pt inside the540pt column boundary; the apparent overflow was disproved by actual bounding boxes, and no science/release rebuild followed. SOURCE_DATE_EPOCH was fixed for the PDF build; no manual PDF editing occurred.

## Bibliographic and DOI destination controls

Installed the exact reviewed bibliographic body417f78a309c262d63ec0946046c388938a7ae323e9eaf7c3d6681526357e050c first. Its only subsequent changes in ops_binding are the new release hash,1.1 metadata version and69/68 archive inventory constants; see RELEASE_CONSTANTS_ONLY.diff. The bounded same-cell OWR classification, short-alias fail-closed rules and previous DOI/URL/family/directory safeguards remain. All176 cached rows parse in current code; old row96 gather/append false blocks remain preserved in historical-source replay.

The public verifier now requires final HTTPS with authority exactly zenodo.org (ASCII case allowed; optional literal:443), canonical plural path /records/EXPECTED_DECIMAL_ID, and no query/fragment, userinfo, extra slash, encoded path, alternate authority or leading-zero ID. This is deliberately stricter than conservative dedup leads; it does not apply the alias parser to authenticated final destination evidence. Actual canonical DOI destinations pass. Noncanonical destinations require review even if some route could redirect correctly. The appender independently repeats the destination validation using the returned status/URL, so forged True booleans with wrong/missing destination evidence cannot bypass it.

There are 125 DOI controls per mode, including actual zenodo.doi_status -> verify_live -> append with synthetic HTTP/provider interfaces and independent forged-upstream appender controls. Exact metadata/PDF/ZIP plus DOI200 with wrong sibling or foreign final URL are rejected before any synthetic gate/append. The frozen old verifier's acceptance of those two wrong destinations remains reproduced. Missing evidence, unsupported port/transport, lookalike, userinfo, root/API/singular/ambiguous path, nearby IDs and query/fragment forms reject. No real provider calls occur.

## Required safe branch revision

repository_integration.py adds only a narrowly pinned revise action from8aebb819bfac9c12340d2f1469408943549ab530. It verifies sole parent091bdecef6f84154f5d5c205a4b07eeb6391b8f8, original17, exact pinned old five manifest548b7a4ae1f13a92029255fc9ef485002b7c33376b9dd9168ffcdb532fc4c20e, complete QUEUE equality, all unselected sibling tree identities and selected directory inventory. It overlays only the current five, creates a sole-parent child, verifies it, repeats fresh gates/PR/ref/file checks and uses a non-force update. PR branch reference must remain identical and cannot be main.

NEW PUBLICATION_REVISION_INTENT/COMMIT/PUSH_INTENT/OUTCOME/UNCERTAIN receipts use exclusive creation with fsync; preexisting branch push receipts are never overwritten. Once an attempt exists, rerun permits only read-only reconciliation: a known new ref can be verified after REST lag/lost response, while an old/unknown ref or partial/conflicting receipts block all mutation retry.38 revision controls per mode cover old/new file/original/QUEUE/sibling/directory tampering, wrong parent/head/ref, local release changes, concurrency, immutable receipts and uncertain-push recovery. These are synthetic executions; no real revise/commit/merge action occurred.

Future root workflow after reviewer06 and a newly pinned root clearance: run `repository_integration.py revise --expected-pr-head 8aebb819bfac9c12340d2f1469408943549ab530` once; then take the exact child from its immutable verified outcome and run verify-test-merge with that child before the existing exact-head merge/publication gates. Do not rerun the original commit action or guess a new head. An uncertain action is reconciled, never blindly retried. The current false root clearance intentionally blocks live use.

## Testing, history and remaining limits

All 3,134 operation controls pass per mode:2,971 prior obligations+38 revision+125 destination controls, each normal and optimized. Historical frozen helpers mount the exact preserved v1.0 publication so their original548... guards remain meaningful; canonical functions use v1.1/69/68. Previously incomplete synthetic success receipts acquire only the canonical intended resolved_url for synthetic ID999; no helper guards or expected outcomes are weakened. Adapter source hashes/counts are recorded. Some nested historical case names/static proposal labels remain historical labels, not publication authority; outer receipts state the current canonical execution context.

The prior exact five+RELEASE are in preprint/release_history/release02_pre_all_odd_prime_robustness_20261021. Initial root/helper/manuscript and107 support/staging/output files were copied before edits; four old branch receipts were also retained. Historical390 and451 manifests remain byte-identical and are reconstructed against their preserved files where current paths changed. No old current path is falsely described as unchanged. Earlier16/44/122 and all completed reviews/seals remain historical; review05's33 artifacts remain unchanged. Original17 and the whole314-file local state inventory remain byte-identical.

Root alone rebound the unchanged semantic lead decision to new release {RELEASE}; current root lead is {LEAD}. The exact old4db5... body is preserved at publication_clearance_history/lead01_pre_scope_extension.json. Account/row/state semantic projections are unchanged. ROOT_SCOPE_RELEASE_LEAD_REBINDING.json is bound; this agent did not author the adjudication. Root clearance remains its unchanged false body.

Finite checks do not prove the credited analytic scalar law or replace reviewer06. Canonical destination policy may conservatively reject benign noncanonical redirects; no universal alias resolution is claimed. Partial revision attempts can require root reconciliation; there is no automatic blind retry. No worldwide priority/open-status claim is added.

## Exact current bindings

Release manifest SHA256: {RELEASE}. Root lead SHA256: {LEAD}.

| Release file | Bytes | SHA256 |
| --- | ---: | --- |
{release_hashes}

| Helper | SHA256 |
| --- | --- |
{hashes}

Reproduce local checks using package verify.py normal/-O, package_validation.py, revision_controls.py, doi_destination_controls.py and replay_final_operations.py. Preserve output custody when rerunning sealed scripts. seal_final.py --verify performs read-only final custody checks. No scientific clearance or publication outcome is asserted by this manifest.
''')
    (HERE/'RESEARCH_LOG.md').write_text(f'''# Final PR280 repair log

- 2026-10-21T15:12Z — 10%: Root authorized exact bibliographic installation and explicit all-odd robustness scope. Preserved old five+RELEASE and root/helper/manuscript/review inputs before edits; copied107 support/staging/output files before changing them.
- 2026-10-21T15:20Z — 55%: Printed separate proposition, built v1.1 PDF, inspected all eight pages. Added46,298 separate exact all-odd controls; retained147,619 class 3 checker. Built69-member/68-payload deterministic ZIP and consistent metadata/README.
- 2026-10-21T15:30Z — 75%: Safe revision action implemented and synthetic hostile/uncertain-push controls pass. All 2,971 prior operational obligations pass with exact historical-release fixture mounts.
- 2026-10-21T15:36Z — 85%: Root rebound semantic lead decision to new release; root retains false clearance. Root requested strict final DOI destination validation in both verifier and appender.
- 2026-10-21T15:45Z — 95%:125 DOI controls and38 revision controls pass normal/-O; all2,971 regressions pass with truthful destination-field fixture additions. Positive actual-function controls caught and corrected a draft variable collision; no provider was contacted. Root independently confirmed the heading's531.21pt bound; no release change.
- {now} — 100% local preparation: Exact current seven/release/root bindings, historical reconstruction and package/visual receipts complete. Pending final local seal, NEW COMPLETE reviewer06/root reproduction. Publication readyfalse; no Git/provider/ledger mutation.
''')
    print(json.dumps({'operations_per_mode':3134,'release_sha256':RELEASE,'root_lead_sha256':LEAD,'helper_binding':binding,'publication_ready':False},indent=2))


if __name__=='__main__':main()
