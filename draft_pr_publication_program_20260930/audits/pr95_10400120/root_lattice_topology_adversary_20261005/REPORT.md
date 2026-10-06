# PR95 / 10400120 fresh root-lattice and topology adversarial audit

**Verdict: PASS for the exact mathematical counterexample and printed conjecture scope.** Incoming head supplied by the parent audit: `6534ad01e519c719628a18984b108e73cf2e8ead`. Incoming proof SHA-256: `9e412983afbec39f2db103b38e771c0e45d2f5c30b433bd6a92459e9aeb4b6a6`. No author original, Git state, PR, external service, or publication state was changed.

The strongest verified result is

\[
|\widehat\tau^{SU(5)}_{10}(L(5,1))|^2=3475+1550\sqrt5,
\qquad |\widehat\tau^{SU(5)}_{10}(L(5,2))|^2=4025+1800\sqrt5,
\]

where the WZW level is k=5, shifted level is κ=r=10, and \(\widehat\tau(S^3)=1\). The difference is 550+250√5>0, both values are positive, and both fundamental groups are Z/5. This disproves Conjecture 7.5 as printed in Ohtsuki (editor), 2002, p.474. **Exact remaining mathematical gap for this narrow claim: none found**, conditional on the established Hansen–Takata RT theorem used as an imported input. This does not establish novelty, historical priority, human peer review, or publication readiness.

## Independent mechanism and evidence

[INDEPENDENT_DERIVATION.md](INDEPENDENT_DERIVATION.md) is a self-contained checkable derivation. It was frozen before author proof/code and historical review/checker reads. The initial obligations are in [OBLIGATIONS.md](OBLIGATIONS.md); the chronology is in [READ_ORDER.md](READ_ORDER.md) and the UTC log.

The independent input is [Hansen–Takata, arXiv:math/0209403v2](https://arxiv.org/pdf/math/0209403v2), Theorem 5.1. The source was downloaded afresh, complete relevant hypotheses/conventions read, and printed p.39 rendered and visually checked. The derivation uses the A₄ root-lattice quotient Y/5Y and character orthogonality. The quadratic Gauss phase becomes 1, and only five Weyl permutations survive. Their norm sums are 11+2√5 and 9+4√5; the S³ Weyl denominator square is 225−100√5. Cancelling the explicit level/covolume prefactors yields 625 times those norms divided by the S³ denominator square, giving the boxed values. The 5X versus 5Y character condition is checked explicitly, so the weight-lattice duality is retained even though the computational quotient is a root-lattice quotient.

The fresh verifier [root_lattice_check.py](root_lattice_check.py) uses only the Python standard library, integer vectors modulo Φ₅₀, all 625 root-lattice representatives, and all 120 Weyl permutations. It constructs all character sums for q=1,2,3,4,6,7,−1,−2, verifies the exact result by cross-multiplication, and uses no author matrices, integrable-weight enumeration, author polynomial coefficients, or imported old checker. Its final normal and optimized executions have identical stdout and exit 0. Both deliberately false guard executions exit 1 under explicit `RuntimeError`, including under `python -O`. See `executions/sealed_exact.*`, `sealed_optimized.*`, `sealed_false_normal.*`, and `sealed_false_optimized.*`; these receipts record actual process IDs, argv, cwd, UTC start/end, exit codes, full streams, and input hashes at execution.

The real embedding is established analytically: √5=1+4cos72°>0. The numerical amplitude and squared magnitude fields in the output are ordinary double-precision diagnostics only, approximately 6940.905365 and 8049.922359. No exact identity, sign, inequality, nonzero decision, or verdict depends on those decimals.

## Falsification and boundary results

| Challenge | Result / exact control |
|---|---|
| Level shift or factor of two | HT r=mκ, m=1, κ=k+h∨=10; theorem permits κ≥5 and does not require gcd(κ,5)=1. |
| Wrong lattice covolume | Gram determinant 5, vol(Y)=√5, vol(X)=1/√5; normalization prefactors explicitly cancel. |
| Missing weight-lattice duality | Trivial character iff qρ−wρ∈5X, equivalently all five coordinates congruent; precisely five permutations. |
| S³ denominator or vacuum zero | Weyl product 5√5−10>0, denominator square 225−100√5>0; p=1 gives normalized value 1. |
| Surgery sign | HT −p/q versus author +p/q reverses orientation; exact full Dedekind-plus-Weyl conjugation controls pass. |
| Denominator inversion | q=2 and q=3 (inverse mod5) produce equal exact norms and phase sum; q=1 and q=4 have equal norms. |
| q periodicity | q=6 agrees with1 and q=7 with2. |
| Nonvanishing exception | Both exact squares positive, so the conjecture's exception cannot apply. |
| Same fundamental group but different manifolds | Van Kampen kills μ⁵ in unknot exterior; both groups Z/5. Connected closed oriented scope satisfied. |
| General formula used outside hypotheses | p=0 handled separately; noncoprime p,q excluded; coprime-level Proposition 5.2 not used. |
| Circular computation | Primary root-lattice formula and exact judgment recorded before original/history reads; no author input imported by verifier. |
| Optimization drops validation | Fresh explicit guard fails in both normal and -O executions. |

The submitted author proof's shifted-coordinate exponents, S magnitude −1/(100√5), powers of 50000 in normalized squared ratios, and orientation statements match the independent derivation. The author proof and verifier were read and copied into this audit for a closed input record, without executing a writer in the original directory. The old historical review/checker was read only after the independent judgment. Its root-lattice mechanism agrees with the fresh result; the freshness here is independent read order and reconstruction, not a claim that this mechanism differs from the historical checker.

## Limitations and source hazards

The incoming author verifier and historical checker use Python `assert`, which optimization disables. Their existing `all_pass` receipts should therefore be interpreted as normal-Python receipts, not proof of safe guard behavior under `-O`. This audit's fresh checker provides an optimization-resistant exact certificate. No changes to incoming code were made.

The freshly fetched HT PDF SHA-256 is `a00c189a481c1c7f5ccb14968e4d3b29abe7e560d3bb416f13ba56ae795e609e`, independently matching the author source manifest. The Ohtsuki publisher's `024p` PDF was used afresh rather than inheriting the author's `024s` bytes; the pertinent printed Chapter 7 definition and conjecture match. Its SHA-256 is `cf7c5e29b818e647496e888378db7a8620be5386f357691c4c48b51f1ca1f5fe`.

An obvious later-priority-audit lead is HT Remark 5.3(a), printed p.44, where sl₄ invariants separate L(64,9) and L(64,25). Separation of complex values alone does not establish unequal magnitudes, so it is a lead, not a demonstrated historical counterexample. Ohtsuki attributes Conjecture 7.5 to Guadagnini–Pilo (1998), [158]. No global priority/status audit or external individual communication was undertaken. Source PDFs and renders are internal audit evidence and have no redistribution/publication approval from this task.

## Closed packet and status

`EVIDENCE_MANIFEST.json` enumerates and hashes the complete internal packet, including primary PDFs/text/render, frozen derivation, checker, incoming byte snapshots, per-process receipts, full output streams, chronology, and report. It excludes only itself and its detached `SHA256SUMS` self-authentication to avoid a circular hash. The manifest declares its own actual generation process and its empty streams; source/input snapshots are closed within this directory. Early provisional receipts are retained with their original streams; only the `sealed_*` receipts are authoritative for the final checker version.

Audit completion estimate: **100%** after packet seal. Historical author search budget remains **2/5**, with **zero new central proof-search turns**. No authority to publish was granted or exercised. Remaining gap beyond this audit: novelty/current literature priority and any separate release/package checks requested by the parent.
