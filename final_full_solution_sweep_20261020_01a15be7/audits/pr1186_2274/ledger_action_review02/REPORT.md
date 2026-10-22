# Independent adversarial review02: PR1186 existing-publication ledger action

Verdict: no remaining material objection to the exact revised action under the stated execution gates. This is a bounded review of one existing-publication reconciliation. It is not a new-paper publication clearance or a guarantee of cross-service atomicity.

## Exact reviewed action

The entire copied `inputs/reconcile_existing_row.py` was read: 9,105 bytes, SHA256 `0360bb97064000502aa04a38c7f8816229b298fcdcb2295f16acc7f2e53af1a5`. Proposal: 1,809 bytes, SHA256 `09fcd90b9b89a4a54e19a660505990ca861c3b90080a6c954d0a7ea5f70eeac2`. Publication verification: 1,084 bytes, SHA256 `e5b7dd44e20001cd448c9980d1bca786475d4dff289fe0f6de8163dd87ee696f`.

Root must rehash these exact live inputs before execution. The runner was never executed against live providers by this reviewer. Executed copies were isolated and stubbed; all their writable paths were within this review directory. No production case, intent, root receipt, Git/index/ref or CLI setup was changed.

## Independent action tests

`verify_offline.py` was authored independently for this review and executes the complete pinned runner main against explicit provider stubs, with actual exclusive local file creation and file/directory fsync calls. Unknown network URLs and commands are rejected by the stubs. The final suite has40 scenarios, repeated in normal, `-O`, and `-OO`; all120 scenario executions produced expected results (with12 additional guarded-rerun checks). `FINAL_MODE_COMPARISON.json` confirms identical40 scenario outcome vectors. Timestamps and isolated path strings are deliberately not compared byte-for-byte. Earlier37-scenario runs remain identifiable historical evidence.

The two positive scenarios make exactly one synthetic append, with the exact reviewed four literal string cells, blankB, correct book and numeric gid1254632077, a complete43-column data-filter read, and a matching readback. An unrelated concurrent append is permitted; every earlier row stays unchanged. The stub checks that the before snapshots and original-digest intent exist before the synthetic mutation, that the intent request equals the submitted request, and that containing-directory flushes occurred.

Thirteen duplicate scenarios cover canonical EP711 URL, canonical PR1186 URL, version DOI18154085, concept DOI18154084, named Erdős forms (including decomposed Unicode), EP alias, problem2274, author, title fragment, percent-encoded concept DOI, zero-width concept DOI, and a lead in columnAQ. Each makes zero write calls and no success receipt.

Wrong workbook, numeric gid, title, sheet width, echoed data-filter gid, or truncated read extent block before writing. So do formula/value disagreement, third-read ledger changes, proposal/proof drift during preflight and after snapshot creation, live PR head/body drift, unpublished record, checksum inventory change and DOI failure. Proposal drift is rejected using the frozen initial bytes; intent hashes that original buffer. The earlier review's two material findings are closed by these independently reproduced controls.

Simulated directory-fsync and intent-fsync failures produce no append. Both ambiguous transport cases—failure before the provider applies an append and failure after it applies one—leave the intent/case guard and produce no success receipt. Rerunning causes no additional write. Earlier-row drift, target-row drift, unexpected write replies and a post-write duplicate lead each suppress success after the single attempted write. Directory flush calls now occur on the actual local filesystem in positive tests; no power-loss or filesystem-crash persistence guarantee is claimed.

## Paper and row identity

The complete three-page extracted text of the retained article was independently read, including all proof and references. PDF:210,567 bytes, SHA256 `6b76d226c0967e66221eb8e38b46bf06b69c7fd1cf3ad2741cf2900572d6ed5b`, MD5 `21332a60cacff6ee8702ce3a0b80eb0e`. No visual page inspection is claimed.

The paper is Wouter van Doorn, *On the Length of an Interval That Contains Distinct Multiples of the First n Positive Integers*, Integers26(2026),A7, published5January2026. It expressly states the Erdős–Pomerance conjecture that max_m f(n,m)-f(n,n) tends to infinity and identifies this as part of EP711. Theorem1 proves the proposed strict bound0.36n log n/log log n for all sufficiently large positive n. The row credits this existing journal publication and links PR1186 only as an audit; it neither claims project authorship nor calls the paper AI-generated or unrefereed. ColumnB is appropriately blank.

The proof's transfer lemma constructs disjoint multiples for i>n in (kn,k²n] and i≤n in (k²n,k²n+f(n,k²n)], giving kn+f(kn,kn)≤k²n+f(n,k²n). Write s=sqrt(log n/log log n) and k=ceil(0.6s). The cited lower diagonal estimate yields liminf f(kn,kn)/(k²n)≥(2/sqrt(e))/0.6>2.01, while the upper diagonal estimate gives f(n,n)/(k²n)→0. Thus eventually f(kn,kn)>2.01k²n and f(n,n)<0.01k²n, and k²n≥0.36n log n/log log n supplies the claimed strict gap. The argument is sound subject to the explicitly cited1980 diagonal estimates; this review did not independently reprove their source. It resolves this complete original subquestion; the uniform exponent-one upper question remains unproved by this article, exactly as the row states.

## Fresh read-only checks and limits

At2026-10-22T05:07:30.624678UTC a fresh GWS native numeric-sheet read returned182 rows over `'Math Puzzles'!A1:AQ1178`, exact book/gid, with no known relevant alias lead. Its raw205,651-byte response is retained privately, SHA256 `4472a5fe9a01e751fe8c04194e4ba890769de7750b2c738a9b87b673bd34a45b`. Fresh Zenodo metadata matched published state, creator, exact title, version DOI and concept DOI; the version DOI resolved200 to record18154085. `FRESH_READONLY_OBSERVATION.json` pins these observations. No external service write occurred.

This read does not replace the runner's fresh preflight immediately before any action. Root must continue semantic deduplication beyond identifier matching. Another writer can race between a read and append; this action cannot provide a global lock or atomic read-and-append transaction. Post-write conflicts are detected and require inspection rather than automatic rollback or retry. A local file can change after the final equality check; the request and intent nevertheless derive from the same frozen buffer, and root must maintain its exact-input gate. No further material issue was found within this bounded scope.

Own bounded review complete100%; overall sweep remains79%.
