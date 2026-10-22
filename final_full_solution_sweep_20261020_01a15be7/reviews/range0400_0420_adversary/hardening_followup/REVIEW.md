# Independent follow-up: pinned scope helper hardening

Completed2026-10-21 UTC. Completion estimate: **100% of this narrow helper review**.

**Verdict: the advertised hardening is verified; no blocker was found within the helper's stated path/added-row observational scope.** The previous range classification and all164 prior sealed outputs remain unchanged. This follow-up makes no publication, scientific, eligibility, or novelty decision.

## Bound source and method

The reviewed current helper has SHA-256 `ee41b085d1dfa224f4ae7c40fccdb1b59cc3a0481e81df93f696bd951f23830c`. Its preserved predecessor has SHA-256 `2ba3115b4102bc0afedafed1d6d203a6f6b94a01869246f74ffe21526a9e3169`. Both exact sources, required imported helpers, root hardening receipt, relevant inventory records and all21 eligibility inputs are preserved in this follow-up. `HARDENING.diff` records the actual source change.

The new code independently retains the real complete pinned path list, rejects duplicate or non-string cached paths, requires `type(file_count) is int` with the exact actual count, and checks cached file-list length and filename multiset. It does not replace actual pinned Git comparisons with cached metadata assertions.

I wrote an independent challenge harness. It loads the copied helper with Python bytecode disabled, replaces its optional fetch routine with an existing-object read assertion, runs Git only against immutable objects with `GIT_OPTIONAL_LOCKS=0`, and redirects the receipt writer to in-memory capture. Fixture and result writes stay within this new subfolder. No provider API or GWS call, Git status/index/ref operation, Git fetch, branch change, PR write, publication action, or root receipt write occurred.

## Actual cases and malformed-cache controls

Both normal Python and `python -O` pass all21 actual PR400–420 helper cases. These are execution checks of the helper against fixed inputs; they do not reopen the range's scientific or publication review.

Each execution mode runs **51 additional controls**, with exactly matching outcomes, errors, and receipt-write counts between modes. Forty-one malformed cases reject without writing a receipt. Ten cases pass for order-insensitive or intentionally limited-scope reasons.

| Control family | Cases per mode | Rejected | Accepted | Coverage |
| --- | ---: | ---: | ---: | --- |
| Cached paths | 8 | 7 | 1 | Appended duplicate; same-count duplicate replacement; mapping/null; nested list, integer and boolean elements; valid reordering |
| File count | 12 | 12 | 0 | True/False, equal float, numeric string, null, negative, zero, smaller/larger counts, absent field; one-file bool/equal-float boundary |
| Cached files | 11 | 10 | 1 | Missing/extra entry; same-count duplicate filename; foreign filename; missing/null/list filename; string entry; null/mapping container; valid reordering |
| QUEUE scope and added rows | 12 | 12 | 0 | Absent/duplicate/wrong-path/null queue change; missing/duplicate row; changed status, ID, source line, path; null rows and malformed row object |
| Intended scope behavior | 4 | 0 | 4 | Disclosed differing queue SHA; actual411 context difference; unchanged filename with altered cached file SHA; altered unused cached patch |
| Additional schema boundaries | 4 | 0 | 4 | Extra unrelated queue-change entry; empty row mapping for header-only415; numerically equal PR float; conflicting later duplicate inventory entry |

The exact-integer check was tested at the critical one-file boundary: `True == 1` and `1.0 == 1` do not bypass validation on415. The filename check was tested with the same list length and one duplicated name replacing a real name, so length equality alone cannot explain the rejection. Path and file order are correctly irrelevant to their set/multiset contracts.

Some malformed container/field cases reject through `TypeError` or `KeyError` rather than the custom `RuntimeError`. This remains fail-closed: no success receipt is emitted, and optimized Python does not bypass the rejection. The actual hardening checks are ordinary conditionals, not removable assertions.

## PR411's intentional context difference remains explicit

Both modes accept the unchanged actual411 inputs with100 actual paths and equal added rows, while preserving this queue observation:

- Actual branch-head QUEUE blob: `b0a1bc47a4a6d2c5ed94981154338739af15a7bb`.
- Cached merged-context blob: `7ba6ce11defb9da24b3a53fd33a3ef8e4a186dc3`.
- Receipt field: `equal: false`.
- Actual pinned QUEUE patch SHA-256: `41b364188b04a99f89f281bd13e1c28e45ef0d4aa1d8769ccd252bca299c24c6`.

The hardening therefore does not turn a legitimate, previously explained whole-QUEUE context difference into a file-inventory rejection, and it does not hide the difference. The already completed range review supplies the separate branch/merge provenance explanation; this follow-up does not replace or repeat that scientific/publication work.

An arbitrary syntactically valid differing cached queue SHA also passes with `equal:false`, as in the previous helper. Thus success still means actual path/added-row agreement plus disclosed queue-byte comparison; it is not proof that every differing cached SHA came from a genuine merge. Likewise, changing cached per-file blob SHA fields or the unused cached patch does not defeat the actual path/row check, because those cached fields are outside its attested byte-identity scope.

## Reproduced permissive schema boundaries

Four additional malformed or ambiguous schema cases remain accepted. They are explicit limits of this helper rather than blockers to the tested path/row hardening:

1. **Extra unrelated `queue_changes` entry:** a valid actual canonical queue change plus an entry for `foreign/QUEUE.md` passes. The helper checks the actual canonical path and corresponding entry; it does not validate the entire cached queue-change list against the complete changed-path list. It does not emit a successful binding for the foreign entry.
2. **Empty mapping in place of the row list on415:** `added_queue_rows={}` passes when the actual added-row set is empty. Iteration over the empty mapping is vacuous, so this does not manufacture or omit an actual added problem row. It shows that the helper is not a strict cache-schema validator.
3. **Numerically equal PR float:** evidence `pr=400.0` passes comparison with requested integer400. The actual requested PR, refs, paths and rows remain the same. The PR identity field does not have the new strict integer-type rule used for `file_count`.
4. **Later conflicting duplicate inventory entry:** a second entry for400 with a different head is ignored because selection uses the first matching entry. Inventory uniqueness and live freshness remain upstream responsibilities; the helper's returned pins still describe the selected first entry.

If strict validation of the entire inventory/cache schema is desired later, these four checks are concrete additional boundaries to tighten. The present source claims pinned scope only and continues to state that it makes no live-head, publication, mathematical or priority decision. None of these accepted fixtures falsifies the actual path/row statement of the emitted receipt, and none appears in the actual21 inputs tested here.

## Seal preservation and strongest verified result

`PRIOR_SEAL_RECHECK.json` rehashes every one of the prior164 sealed outputs and confirms all are unchanged. It also separately confirms that the previous `OUTPUT_MANIFEST.json` itself remains byte-identical. `FINAL_RECHECK.json` confirms the live current helper still equals the reviewed source snapshot and that normal/optimized control result records are exactly equal.

The strongest verified result is that the two previously reported metadata gaps are closed by the reviewed change, together with broader malformed filename/container/row rejection, in both execution modes and without losing legitimate411 disclosure. No new blocker remains for using this helper according to its stated observational scope. Full cache-schema validity, inventory uniqueness, live metadata, file-byte identity beyond its queue observation, problem correspondence, and mathematical/publication conclusions remain separate responsibilities.

## Evidence

- `INPUT_MANIFEST.json`, `inputs/`, `HARDENING.diff`: exact bound source and metadata inputs.
- `challenge_helper.py`: independently written, reproducible controls with bytecode/fetch/root-write safeguards.
- `actual_range_normal.json`, `actual_range_optimized.json`:21 actual observations in each mode.
- `controls_normal.json`, `controls_optimized.json`, stdout/stderr files: all51 cases per mode and receipt-write counts.
- `PRIOR_SEAL_RECHECK.json`, `FINAL_RECHECK.json`: unchanged original164 outputs and source/mode correspondence.
- `VERDICT.json`, `RESEARCH_LOG.md`, `OUTPUT_MANIFEST.json`: narrow decision, timestamped checkpoints, and new follow-up checksum seal.
