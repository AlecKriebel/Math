# PR1241 publication workflow adaptation

Prepared 17 October 2026. Scope is the eight workflow scripts only, adapted after reading the complete PR1225 hardened templates and the relevant PR1241 original/current math, source-question, fresh adversary, diagnostic and priority records. No mathematical edition, manuscript, deposit metadata, release PDF/ZIP, review gate, upload, tracker row or PR update was created by this adaptation. No branch, shared index or remote was changed. The scripts are prepared for later root-authored inputs and separate whole-package review; this record is not a clean whole-package verdict.

## Fixed identity and attribution

PR1241; problem11000082; AMR-109-0082; Farb Question7.6. The pinned original head is `493a764dec034b7b645be76a284c4e6edc0583eb`, branch `audit/11000082-johnson-multiplicities-20261011`, and original eight-file prefix `unsolved_math_prioritization/attempts/11000082`. The title is *Equal dilatations deep in the Johnson filtration: a convex-core proof*. Release filenames are `Johnson_Filtration_Multiplicity_Note_v1.0.pdf` and `Johnson_Filtration_Multiplicity_Verification_v1.0.zip`.

The paper's result is an attributed alternative proof of unbounded exact dilatation multiplicity for every fixed genus g>=2 and fixed finite Johnson depth k>=3, counting ambient orientation-preserving mapping-class conjugacy. The explicit printed theorem of Alper Ferudun, DOI10.5281/zenodo.23301731, must be credited. No firstness, new existence, new mechanism, current openness, ambient primitivity, simple-loop, single-value infinite multiplicity or intersection-of-all-depths result is promoted by these scripts. Historical public visibility and disclosure genealogy remain distinct from dated Git/PR and Zenodo creation facts. The tracker and final PR prose state this scope and the extensive-AI/unrefereed disclosures.

## Required root-authored context

`prepare_package.py` requires both `PRIORITY_ADJUDICATION.json` and `CURRENT_PR1241_CONTEXT.json` in the audit root. It also requires the exact original-target `MATH_GATE.json` to have a `PASS` status. It does not compose final mathematical or priority findings from an earlier PR template.

The priority object must explicitly contain these fields:

```json
{
  "novelty_clearance": false,
  "firstness_claim": false,
  "current_openness_claim": false,
  "new_existence_claim": false,
  "matching_publication_doi": "10.5281/zenodo.23301731"
}
```

Additional adjudication fields are retained verbatim. The current context contract is:

```json
{
  "schema": "math-pr1241-current-context-v1",
  "pr": 1241,
  "problem_id": 11000082,
  "original_head": "493a764dec034b7b645be76a284c4e6edc0583eb",
  "title": "Equal dilatations deep in the Johnson filtration: a convex-core proof",
  "edition_text": {
    "PROOF.md": "Root-supplied current proof and explicitly marked historical material",
    "AUDIT.md": "Root-supplied current audit",
    "README.md": "Root-supplied current scope and use instructions",
    "ACCEPTANCE.md": "Root-supplied exact current acceptance"
  },
  "acceptance": {"root_supplied": "Actual final structured acceptance"},
  "sources": {"root_supplied": "Actual final source/priority scope"},
  "verification": {"root_supplied": "Actual final verification acts and limits"},
  "authored_freezes": [
    {
      "path": "reviews/analytic_adversary/FINAL_AUTHORED_FREEZE.json",
      "base": "reviews/analytic_adversary",
      "entries_key": "entries",
      "path_key": "file",
      "sha256": "fda107bc74f9af2eb5ba235a897c43b8de09cc7d9185437069c0d29ec572c52f"
    }
  ]
}
```

This is a schema example, not a usable completed context. The registry must include all seven actual initial/cross-challenge family freezes after sealing. Every `path` and `base` is relative to the audit root and retains the identical relative meaning in the extracted archive. Every `sha256` is the outside-anchored digest of the manifest itself. The original-submitted and current-edition `MANIFEST.json` files are handled automatically and **must not** be in this family registry.

Five required initial schemas are checked explicitly:

| Manifest | Base | Entry array | Member path key |
|---|---|---|---|
| reviews/analytic_adversary/FINAL_AUTHORED_FREEZE.json | reviews/analytic_adversary | entries | file |
| reviews/source_question_family/FREEZE_MANIFEST.json | reviews/source_question_family | authored_files | path |
| reviews/convex_core_adversary/FREEZE_MANIFEST.json | reviews/convex_core_adversary | authored_files | path |
| priority/independent/FREEZE_MANIFEST.json | priority/independent | all_authored_content_files | path_relative_to_authored_root |
| priority/adversary/FREEZE_MANIFEST.json | priority/adversary | authored_files | path |

The two later cross-challenge schemas must be registered explicitly with their actual names, bases, keys and outside hashes. The portable verifier rejects recognized authored freeze/manifest files that are unregistered, missing manifests, changed outside anchors, duplicate members, unsafe paths, wrong sizes and digests. It treats raw/source inventories as authored **receipts** only: their omitted source-body entries are never treated as portable members to reauthenticate. Absolute historical paths retained inside a receipt are descriptive and do not control portable lookup.

`prepare_package.py` authenticates registered original frozen members before writing, includes them even if a global scratch-directory ignore would otherwise omit a registered child, and copies only authored review/priority material beyond those explicit members. Existing package-owned copy trees are regenerated; the portable verifier is retained. All original eight submitted files stay separately immutable. Current structured records retain earlier source and execution statements as historical records, without retroactive authentication. A separately authored manuscript-source derivation folder is not automatically copied merely because it exists: its inclusion requires root adjustment or an explicit registered authored freeze under the allowed trees.

## Compilation, layout and archive

`compile_note.py` sets `SOURCE_DATE_EPOCH=1792267200` in the actual compiler environment. This is the chosen reproducible build stamp **2026-10-17T20:00:00Z**, not the actual compilation or research-completion time. `COMPILE_RECEIPT.json` records that value and meaning, the real `at_utc`, compiler path/version/digest, current source digest, resulting PDF digest and success. Identical cached compiler/input conditions can reproduce bytes; universal cross-environment determinism is not claimed.

Only after actual compilation and all-page rendering/inspection, the root adds a positive integer `expected_pdf_pages` to the context. No page count was invented or hardcoded by this adaptation. Build independently reads the PDF page count with `pdfinfo`, requires an exact page-index inspection list and current source/PDF hashes, and verifies the chosen compile stamp. Context and priority-record hashes are also bound across building. The source/PDF cannot change during compilation or building. Bibliography QA must exist before package preparation.

The ZIP is built in an ignored temporary directory, with fixed member timestamps. It is reopened and every member byte and inventory entry is compared before the final archive and PDF are atomically replaced. Root inventory, all authored nested freezes and original Git blob identities are checked. Exact-artifact whole-package reviews, final review gate and publication receipts remain later required acts.

## Actual diagnostic scope and replay

The archive includes `root_horowitz_checks.py`, `ROOT_EXACT_DIAGNOSTICS.json` and `ROOT_REPLAY_RECEIPT.json` under `diagnostics/`; all corresponding root provenance records are preserved. The portable verifier replays the root's explicit-check diagnostic in normal, `-O` and `-OO` modes and compares results with the saved finite results and receipt bindings.

The source-question `verification.py` and convex-core `adversarial_checks.py` contain essential assertions and write result files beside themselves. They are replayed in a fresh **normal** interpreter on temporary copies only, explicitly clearing inherited `PYTHONOPTIMIZE`. Their generated JSON bytes must match the frozen results. No optimized assertion-based replay is presented as performing the normal checks. Root and family diagnostic inputs remain unchanged. These are finite exact arithmetic/free-word consistency and altered-hypothesis controls; the infinite geometric and ambient-conjugacy results rest on the written proofs and named mathematical imports. The candidate-aware analytic adversary executed no mathematical experiments, and omitted original historical code was not replayed.

## External-operation guards retained

The eight-script exact workflow gate and an actual latest `CLEAN` review report/verdict are bound before the PR helper can mutate anything. The original head, source/body identity, exact current edition, exact reviewed PDF/archive, metadata, canonical production DOI/record links, public downloads and full tracker receipt are checked. Git object creation never changes local branch or the shared index. The publication commit is parented directly to the pinned original; saved commit intent is rechecked against actual parent, all13 changed paths and each blob on every retry. The branch push is non-force and pinned. API lag stops before the final-body mutation. Final body editing is read back, rejects unknown outside edits and reconciles lost responses without duplicate writes.

Public verification compares every supplied metadata field exactly after only the explicit Zenodo legacy/public schema projection and verifies both public downloads. Tracker writes use the Google Workspace CLI, the designated sheet ID/gid/title, exactly four cells with blank solution-chat URL, an intent before one append, duplicate-problem/DOI checks and exact readback. An uncertain append is reconciled from the actual exact row before any retry. Publication/merge itself is not performed by this adaptation and requires root coordination with the repo's Zenodo kit and expected-head merge.

## Checks performed for this adaptation

All eight scripts parsed successfully. The offline guard worker ran in normal, `-O` and `-OO` modes with identical results. It exercised missing/wrong current context and math/priority inputs; custom freeze schemas and an altered member hidden by an updated outer inventory; stale source/PDF, wrong page/compile stamp and missing visual-QA bindings; canonical publication identity; every four-cell tracker position/range and renamed-tab prewrite refusal; saved PR identity, actual commit parent/path/blob guards; all11 public metadata fields; and final-body readback, unknown outside changes, idempotence and lost-response recovery. These were temporary fixtures/mocks and made no external operations. An initial pre-authoring run used an explicitly labeled eleven-field metadata fixture. After the root supplied `zenodo-deposit.json`, the final three-mode run instead compared all11 fields from that actual current local metadata file with offline public-schema fixtures, rejecting corruption of every field. No live deposit is claimed. The final worker enumerated98 negative-control groups, with additional body/idempotence and prewrite mock checks.

All44 authored members in the five actual initial frozen review/priority manifests were also authenticated with their real custom schemas and base paths. The two cross-challenge freezes remain root-supplied later registry inputs. The actual finite diagnostic replay helper was separately run on temporary copies: root normal/`-O`/`-OO` matched the saved result, and both assertion-based family programs matched their frozen result bytes in normal mode. Those copied inputs remained unchanged. No package/release or actual current edition was built. No final workflow regression receipt, final review gate, clean package verdict or sealed authoring freeze is asserted here; the root will generate current receipts after the final context, manuscript, metadata and cross-challenges are ready.
