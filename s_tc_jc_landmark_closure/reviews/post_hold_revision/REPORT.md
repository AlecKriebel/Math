# Post-HOLD adversarial revision report

Status: **VERIFIED — REPAIRED, INDEPENDENT ADVERSARIAL RE-REVIEW PASSED**

The external adversarial report supplied on 2026-08-14 has SHA-256
`106155f3e918f343ea79091d250a44edbc870f2f1c3afdf9179d396a4535da9e`.
The Figure 4 screenshot has SHA-256
`c3ef4e4a5eae3fd4ba53b7ce92fce1be8ef8d8a303b7e0ad2a5fd245da9ff9a5`.

## Disposition of findings

| Finding | Disposition | Active repair |
|---|---|---|
| Primitive-core degree count | **VALID LOAD-BEARING DEFECT; REPAIRED** | The false `3v<=2e` step was removed.  The proof now uses `sum(deg_B-2)=2(r-1)` on the unsuppressed biconnected subcubic blob, then records source/sink events and ordered port words. |
| Public repository mismatch | **VALID RELEASE DEFECT; REPAIR PENDING FINAL TAG** | The manuscript now names immutable tag `stc-jc-sharp-boundary-v1.0.0`; the tag is created and pushed only after all revised bytes pass clean replay. |
| Crossing-quartet reduction | **VALID LOAD-BEARING OMISSION; REPAIRED** | A graph-theoretic lemma now exhausts one-active and two-active quartet marginals and states the submatrix rank transfer. |
| Complete bridge fibre | **EXPOSITION GAP; HARDENED** | The manuscript now gives sector scales, the leaf-peeling induction, the incidence assignment, anchor exponent matrices, stabilizer exclusion, and no-holonomy argument. |
| Root reduction | **EXPOSITION GAP; HARDENED** | The proof now treats directed cycles, retained reticulation arrowheads, literal one-step suppression, LSA validity, parent complementation, and open edge splitting. |
| Omega rank-nine upper bound | **EXPOSITION GAP; HARDENED AND EXACTLY REPLAYED** | Edge/parameter order, the `14 x 10` core Jacobian, rank six, determinant `-723/8589934592`, and the Euler tangent identity are explicit.  `omega_audit/independent/verify_omega_rank_readability.py` regenerates them. |
| Observational relations and blob definition | **EDITORIAL AMBIGUITY; REPAIRED** | The source-regular neighborhood definition and maximal nontrivial biconnected-block definition are now explicit. |
| Real-algebraic citations | **EDITORIAL GAP; REPAIRED** | Exact Bochnak--Coste--Roy proposition/theorem numbers replace broad section citations. |
| Authorship and AI disclosure | **VALID DISCLOSURE ISSUE; REPAIRED** | The text no longer claims sole implementation/validation and explains that an independent replay is code-independent, not a human review. |
| Figure 4 overlap | **VALID VISUAL DEFECT; REPAIRED** | Panel spacing was increased and the figure rescaled; the revised page is included in the final two-renderer audit. |
| ORCID in title block | **OPTIONAL STYLE CHOICE; REMOVED** | ORCID remains in bioRxiv metadata and upload instructions, but not in the printed author block. |

No reported issue supplied a counterexample to the classification theorem or
the Omega/Theta sharpness theorems.  The submission HOLD is lifted only after
the revised clean-clone, mutation, PDF, archive, and public-tag gates pass.

## Fail-closed bootstrap record

Two clean-clone attempts failed before release sealing, and neither failure
is being erased from the audit record.

1. At source commit `703b2c604838f0e1bbde238441962bd5ae986057`, the
   default package index did not provide the historical pins
   `networkx==3.6.1` and `numpy==2.3.5`.  The verifier stopped during
   environment creation, before any theorem check.  The active lock now
   contains only packages imported by the release gates and uses the
   available exact pin `networkx==3.2.1`.
2. At source commit `90106057bfdd6ccff3896d96292a4289926e2d0f`, the
   quick suite passed, but the full suite exposed that macOS's system
   Python 3.9 lacks `int.bit_count`; the first failing file was
   `reviews/root_probe/verify_parameter_submersion.py` at the expression
   `sink_mask.bit_count()`.  The active bootstrap now locates and enforces
   Python 3.10 or newer, recreating an older virtual environment rather than
   silently continuing.
3. At source commit `13d8395d992c18d549811c6537ed4f1905e6e5bd`, the
   full suite completed the root, bridge, and clean-room n3 relation checks,
   then stopped because the two active base-gate referees still locked the
   pre-revision hash of `docs/DEFINITIONS_LOCK.md`.  Their 225 and 44 exact
   symbolic bodies had no failures; only `locked_input_hashes` failed.  The
   changed definitions bytes are the intentional blob and observational-
   relation clarifications documented above.  Both active locks were updated
   to that exact hash, their certificates were regenerated, and both
   byte-for-byte referee replays now pass.  Historical reviews retain their
   original hashes.
4. At source commit `82329310342134cb4e12e4e91703da4edc2e168f`, every
   classification, restoration, and bridge gate passed, but the full command
   stopped when the historical Omega verifier imported `python-flint` through
   a discovery-only module.  The proof script uses only that module's literal
   15-element `JC_REPRESENTATIVES` tuple; it never calls the finite-field
   matrix routines.  The frozen historical source remains unchanged.  An
   import-only compatibility module now supplies the tuple, and a separate
   AST-based verifier first extracts the literal from the frozen source and
   checks exact equality, uniqueness, zero-sum status, and both file hashes.
   The historical SymPy proof and the independent standard-library and direct
   displayed-tree implementations remain unchanged and all pass.

These are release-engineering failures, not mathematical certificate
failures.  Final clean-clone transcripts are accepted only if they record the
supported interpreter, exit status zero, and clean tracked state before and
after every advertised command.

## Independent theorem-level re-review

A code-independent adversarial reviewer first classified the primitive-core
degree count and crossing-quartet omission as the only two load-bearing
defects among the mathematical findings.  After the revisions, the same
reviewer re-read the current source and returned `PASS`: the unsuppressed
degree-excess proof correctly retains source/sink events and port words; the
quartet alternatives are exhaustive and rank transfers through a genuine
Fourier-flattening submatrix; and no new false statement was found in the
expanded bridge, root, Omega, observational-relation, or blob passages.

This was an AI-assisted adversarial mathematical review, not a human
specialist review.  The clean replay and public-tag conditions are tracked by
the release envelope rather than asserted by this pre-seal report.
