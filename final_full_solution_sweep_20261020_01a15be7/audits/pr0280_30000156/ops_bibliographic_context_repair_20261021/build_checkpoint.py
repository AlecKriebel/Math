#!/usr/bin/env python3
"""Local proposal evidence, exact bindings and preservation; never installation."""
import datetime as dt
import difflib
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
ROOT=AUDIT.parents[1]
REPO=ROOT.parent
FROZEN=HERE/'pre_bibliographic_binding'
PROPOSED=HERE/'proposed'
HELPERS=['ops_binding.py','prepublication_check.py','publication_live_gates.py','repository_integration.py',
         'publication_lifecycle.py','record_publication_ledger.py','verify_published_files.py']
OLD='b12e7262026d780029a7eeee1fb8d0c8a514c4a2ab382faadebad40a84dba55d'


def sha(b):return hashlib.sha256(b).hexdigest()
def load(name):return json.loads((HERE/name).read_text())
def write(name,value):(HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def check(value,message):
    if not value:raise RuntimeError(message)
def entries(base):return [{'path':n,'bytes':(base/n).stat().st_size,'sha256':sha((base/n).read_bytes())} for n in HELPERS]
def verify(root,files):
    check(len(files)==len({e['path'] for e in files}),'Duplicate binding')
    for e in files:
        p=root/e['path'];b=p.read_bytes()
        check(not p.is_symlink() and len(b)==e['bytes'] and sha(b)==e['sha256'],'Changed binding '+str(p))


def check_inputs():
    prior=load('INPUT_PRESERVATION.json');check(len(prior['files'])==392,'Preserved392 inventory changed')
    verify(FROZEN,prior['files']);verify(AUDIT,prior['files'])
    manifest=AUDIT/'ops_record_url_repair_20261021/MANIFEST.json'
    check(sha(manifest.read_bytes())==OLD,'Canonical390 seal changed')
    check(json.loads((AUDIT/'ROOT_PUBLICATION_CLEARANCE.json').read_text())['publication_ready'] is False,'Clearance unexpectedly changed')
    state=REPO/'.zenodo-state'
    check(not any(p.is_symlink() for p in state.rglob('*')),'Unexpected state symlink')
    inventory=[{'path':p.relative_to(REPO).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(p for p in state.rglob('*') if p.is_file())]
    before=json.loads((FROZEN/'ops_record_url_repair_20261021/STATE_BEFORE.json').read_text())
    check(len(inventory)==before['files'] and sha(json.dumps(inventory,sort_keys=True,separators=(',',':')).encode())==before['inventory_sha256'],'Local state changed')
    return {'files':len(inventory),'inventory_sha256':before['inventory_sha256']}


def main():
    state=check_inputs();now=dt.datetime.now(dt.timezone.utc).isoformat()
    binding={'proposal_only':True,'publication_ready':False,'canonical_current':entries(AUDIT),'proposed':entries(PROPOSED),
             'changed_proposed_helpers':[n for n in HELPERS if (AUDIT/n).read_bytes()!=(PROPOSED/n).read_bytes()]}
    check(binding['changed_proposed_helpers']==['ops_binding.py'],'Proposal change scope exceeded')
    write('PROPOSED_HELPER_BINDING.json',binding)
    (HERE/'PROPOSED.diff').write_text(''.join(''.join(difflib.unified_diff((AUDIT/n).read_text().splitlines(True),
        (PROPOSED/n).read_text().splitlines(True),fromfile='frozen_canonical/'+n,tofile='proposed/'+n)) for n in HELPERS))
    summary=[]
    for optimized in [False,True]:
        current=load('BIBLIOGRAPHIC_CONTROLS_OPTIMIZED.json' if optimized else 'BIBLIOGRAPHIC_CONTROLS.json')
        frozen=load('FROZEN_COMPATIBILITY_OPTIMIZED.json' if optimized else 'FROZEN_COMPATIBILITY.json')
        old=load('regression1704_'+('optimized' if optimized else 'normal')+'/SUMMARY.json')
        root=load('regression1704_'+('optimized' if optimized else 'normal')+'/ROOT_METAMORPHIC.json')
        check(current['all_controls_passed'] and current['controls']==1267 and current['provider_access_attempts']==0,'New controls incomplete')
        check(current['proposed_ops_binding_sha256']==binding['proposed'][0]['sha256'],'New controls stale')
        check(old['all1704_passed'] and old['controls']==1704 and old['actual_provider_access_attempts']==0,'1704 replay incomplete')
        check(root['source_sha256']==binding['proposed'][0]['sha256'],'Root benchmark stale')
        check(frozen['false_block_rows']==[96] and frozen['actual_frozen_gather_false_block'] and frozen['actual_frozen_append_false_block'],'Old actual false block not preserved')
        summary.append({'optimization':int(optimized),'new_controls':1267,'prior_controls':1704,'total':2971,
                        'actual_cached_rows_parse':176,'old_false_block_row':96,'providers':0,'new_case_counts':current['case_counts']})
    write('TEST_SUMMARY.json',{'timestamp':now,'proposal_only':True,'publication_ready':False,'modes':summary,
          'no_canonical_installation':True,'pending':'Root explicit authorization after complete sealed review05; then consistent installation evidence and fresh reviewer06'})
    write('PRESERVATION_FINAL.json',{'timestamp':now,'old390_all_current_and_frozen_verified':True,'manifest_and_checksum_unchanged':True,
          'preserved392_verified':True,'all_seven_canonical_helpers_unchanged':True,'scientific5_RELEASE_original17_root_inputs_unchanged':True,
          'local_state_unchanged':state,'provider_git_ledger_mutations':0,'publication_ready':False,'proposal_only':True})
    private=ROOT/'private/record_route_retrospective/ledger.json';raw=private.read_bytes();sheet=json.loads(raw)['values']
    write('CACHED_SHEET_READ_RECEIPT.json',{'path':private.relative_to(ROOT).as_posix(),'bytes':len(raw),'sha256':sha(raw),'rows_including_header':len(sheet),
          'cells_present_including_header':sum(len(r) for r in sheet),'row96_values_sha256':sha(json.dumps(sheet[95],sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()),
          'row_bodies_copied_to_public_evidence':False,'account_credentials_or_bodies':False,'source':'Root14:21cached full four-column sheet; no new GWS request'})
    report=f'''# PR280 bibliographic-context proposal checkpoint

Completed {now}. **Proposal only; publication readyfalse.** Canonical390, root inputs and review05 remain frozen. No installation or lifecycle action is authorized by this checkpoint. Root explicit authorization after COMPLETE sealed review05 is required before any canonical installation; a consistent final binding and fresh whole-package reviewer06 would then be required.

## Verified false block and preservation

Before any proposal work, verified every one of the390 files under manifest SHA256 `{OLD}` and copied all390 plus manifest/checksum audit-relative under `pre_bibliographic_binding/`. `INPUT_PRESERVATION.json` records392 verified copies. Both actual canonical390 and the392 preserved files remain byte-identical; `PRESERVATION_FINAL.json` also confirms all seven canonical helpers, science5/RELEASE, original17, root inputs and all314 local-state files unchanged.

The exact cached sheet has176 rows including header, SHA256 `d513b4cfef1ca47f654a6f677693ae7186f3f193f6d892c5e043ad318c0061b3`. Frozen actual390 parsing accepts175 rows and rejects only row96. Actual frozen gather and independently bypassed-gate append also reproduce the row96 false block in normal and optimized Python. `FROZEN_COMPATIBILITY*.json` retains these failures. The cached full row is read privately; public results contain its digest, not the unrelated ledger notes or full sheet bodies.

Row96's source cell explicitly uses the bibliography “OWR 10/2016” with the full literal source DOI `10.4171/OWR/2016/10`. MFO's [primary catalog metadata](https://publications.mfo.de/handle/mfo/3513?show=full) identifies report2016,10 and that publisher DOI; [EMS Press](https://ems.press/journals/owr/articles/14218) confirms the DOI for the2016 report. Only bibliographic metadata was assessed; no PR826 mathematical audit or outreach occurred. Direct DOI web-tool open failed and is not claimed read. `PRIMARY_BIBLIOGRAPHIC_EVIDENCE.json` records actual successful primary metadata reads.

## Exact proposed rule

Only the proposed copy of `ops_binding.py` changes. The other six proposed helper copies equal frozen canonical files. `PROPOSED.diff` and `PROPOSED_HELPER_BINDING.json` give exact code and hashes.

For each cell, without Unicode folding, find literal ASCII-case-insensitive `OWR` followed by spaces/tabs and the bounded token `10/YYYY` with exactly four ASCII year digits. Qualifying bibliographic context requires exactly one such context, exactly one literal bounded full DOI `10.4171/OWR/YYYY/R` with canonical positive ASCII report digits, exactly one literal OWR-source hint, and exactly one hint after the existing bounded recursive percent-decoding review. The year strings must match and the source report string must be exactly `10`. Duplicate, mismatched, encoded-only or malformed source contexts do not qualify. The report/year classification is a literal bibliographic relationship, not an assertion that all syntactically matching source DOIs resolve or that numeric shortDOIs are impossible.

When qualified, mask **only that one literal report token** for the short-code ambiguity decision. The original cell still undergoes all DOI/Zenodo URL/family recognition. All other bounded `10/` prefixes are conservative unresolved-code leads, regardless of an imagined shortDOI alphabet; isolated numeric codes, dates/fractions, explicit `doi:10/2016`, extra or nested encoded codes remain review-required. No numeric code is globally whitelisted. No root row-digest exemption is consulted by this classification, and a potential target identity cannot be exempted by it.

Known shortDOI resolver references remain unresolved aliases. The proposal conservatively recognizes protocol-relative/default-port/dot-segment resolver variants and malformed single-slash official resolver forms, plus bounded bare shortdoi.org references. Known shortdoi.org URLs always require review; doi.org/dx.doi.org paths without a complete lexical `10.<ASCII digits>/<suffix>` shape require review. This is a conservative blocker, not an alias-resolution or DOI-validity oracle. Existing resolver/encoding guards remain active. No claims of global URI equivalence, arbitrary Unicode normalization or universal redirect discovery are made.

All four cells are still evaluated before allocation/model shortcuts and independently by append/readback. Root non-target digest entries do not bypass unresolved aliases or target identities. Exact desired literal row idempotence remains unchanged. DOI ASCII case/unreserved handling, leading-zero suffixes, record-URL conservatism, concept/version-family leads and directory inventory preservation are retained.

## Actual-function offline evidence

Normal and optimized Python each pass **2,971 controls**:1,267 new bibliography/cached-row controls plus all1,704 previous controls. The new suite includes176 actual cached rows,64 valid-context full pipelines across four cells with/without root digests,2 exact original row96 full pipelines,384 independent append rejection checks,384 collector/gate-before-allocation rejection checks,24 later-cell short-alias append checks,24 later-cell before-allocation checks,16 adjacent/later target-identity pipelines,192 readback ambiguity checks across all four cells and literal idempotence. Thus all176 cached rows parse in the proposal. Actual provider attempts arezero; test providers are synthetic, with socket/subprocess/provider traps. Public bibliography reads above were read-only and separate from the offline service simulations.

The1,704 replay retains994 route controls,404 historical controls,303 root finite lexical obligations and3 already-pushed resume controls. The test adapter changes source selection and output custody only; prior directory fixtures and expected outcomes remain unchanged. Nested legacy120 output still carries old static `proposal_only:false`/`canonical_edits_authorized:true` labels from its untouched historical runner. Those labels describe that runner's original mode, not this execution: the outer replay receipt identifies isolated proposed sources and no authorization or canonical mutation. Root benchmark source SHA binds this exact proposed body. Finite overlapping controls do not prove universal parser correctness.

Reproduce with `PYTHONDONTWRITEBYTECODE=1 python3 bibliographic_controls.py` and `replay1704_proposed.py`, then each with `-O`; their temporary full-sheet fixtures stay in the ignored private scratch folder. `seal_proposal.py --verify` verifies this proposal and the unchanged390/392 inputs locally.

## Remaining limits and handoff

The exception deliberately accepts a single explicit literal OWR bibliography context; duplicate references or encoded-only source citations conservatively block. It does not verify every future source DOI against a registry or establish mathematical truth. Arbitrary disguised text, unrecognized external redirect domains and universal shortDOI alias discovery remain outside a finite lexical recognizer. Potentially ambiguous recognized forms require review; no automatic metadata-only exemption is introduced.

No canonical helper, root clearance/reconciliation, old seal/review, source payload, original file, GWS row, provider object or Git state was changed. Already-pushed head remains a parent-owned fact; no integration action was rerun. Await root's explicit next authorization before canonical installation. Proposal preparation is100% complete; publication remains pending.

Proposed ops_binding SHA256: `{binding['proposed'][0]['sha256']}`. Current canonical SHA256 remains `{binding['canonical_current'][0]['sha256']}`.
'''
    (HERE/'REPORT.md').write_text(report)
    (HERE/'RESEARCH_LOG.md').write_text(f'''# PR280 bibliographic proposal log

- 2026-10-21T14:46Z — 10%: Preserved all390 bound artifacts and manifest/checksum before proposal work. Canonical installation forbidden while review05 continues.
- 2026-10-21T14:49Z — 25%: Verified exact cached row96 false block and obtained primary MFO/EMS bibliographic metadata. No unrelated mathematics audit or outreach.
- 2026-10-21T14:56Z — 65%: Initial same-cell literal context proposal passes actual cached176 rows and synthetic full pipelines. Tightened duplicate/encoded-source rejection and added all-cell readback checks.
- 2026-10-21T15:03Z through15:05Z — 95%: Bounded unresolved resolver/code fallback retained and strengthened; final1,267 new controls and1,704 prior controls pass normal and optimized. Frozen gather and independent append false blocks preserved.
- {now} — 100% proposal checkpoint: Exact proposed seven binding/diff and preservation receipts complete. Current390 and392 copies unchanged; no canonical install/provider/Git mutation. Proposal seal pending creation; await root authorization after sealed05 before installation/fresh06.
''')
    print(json.dumps({'proposed_sha256':binding['proposed'][0]['sha256'],'controls_per_mode':2971,'canonical390_unchanged':True,'proposal_only':True,'publication_ready':False}))


if __name__=='__main__':main()
