# Acceptance: EP195 / 1986 partial research

Accepted scope: corrected partial mathematical research. The all-integer four-term problem remains unresolved in this edition. The target is an omega-bijection from N0 onto all Z, avoiding nonconsecutive subsequences with any nonzero common difference, positive or negative. The universally forced threshold remains 3 or 4. Arbitrary total orders and doubly infinite enumerations are different targets.

This is an AI-assisted, unrefereed research edition. The independent check described here is an internal AI audit, not external human peer review or formal proof-assistant certification. Source results retain their named attribution. No novelty claim is made. This prose-and-metadata edition is not a computational reproduction package: code, raw result files, copied source documents, source text, and images are not distributed. Historical execution and inspection statements describe the authenticated research and audit records; no mathematical code or formalization was rerun during publication preparation. Hashes authenticate bytes, not mathematical truth. The complete written mathematics is retained below, with the single safe-prefix orientation correction disclosed in ACCEPTANCE.md and nonmathematical publication edits.

## Required correction and exact application

The audit identified one required correction in the first paragraph of report section 3. The finite safe list must be in the reverse of Ho's fixed tail order. The same orientation is insufficient: the fixed tail puts 1 before 2 and 3 before 4, so prefix (1,2) admits (1,2,3,4); prefix (2,1) is safe by the opposite-orders lemma.

Exact original sentence:

A reverse-binary finite listing is safe by the preceding two-order argument.

Exact corrected sentence:

A finite set listed in the reverse of `triangleleft` is safe by the preceding two-order argument; listing it in the same order as the tail is not sufficient.

The exact audit patch was applied to a separate publication working copy, never to the frozen original. No other mathematical claim, formula, proof, explicit finite sequence, counterexample, or scope boundary was changed. Editorial changes remove private coordination, replace unavailable local links and run commands with historical-distribution wording, and add review-status notices. The full corrected research report is PROOF.md; the full independent mathematical audit, including the complete reconstruction of Ho's N0 proof and Adenwalla's all-Z five-term construction, is AUDIT.md. Neither is replaced by a summary.

## Accepted mathematical ledger

1. Binary-tree total orders are three-term-free and obey the four-term pair identity. Opposite prefix/tail orientations give finite safe completions; this alone does not give order type omega.
2. Ho's September 2026 manuscript proves four-term avoidance on N0 and N. Its complete written proof and exhaustion argument are reconstructed in AUDIT.md. Its inequalities use nonnegativity essentially; the result is not transferred to Z.
3. A fixed reverse-binary safe-tail invariant cannot exhaust Z. The record witness is (-1,M,2M+1,3M+2). This excludes the specified invariant, not all integer permutations or adaptive tails.
4. The signed parity-splice residual is exactly: for every u in U and v in V, either 2v-u lies in P union U or 3v-2u lies in P union V. The stated hypotheses are essential. The (1,0,-1,-2) example and the symmetric-buffer extremal obstruction are retained completely.
5. Missing-continuation and directed-demand-cycle certificates are necessary for arbitrary future enumerations, and the stated tests become sufficient only for a specified three-term-free tail. Both dead prefixes, their two- and three-cycles, and the six-term two-cycle geometry remain explicit.
6. The residue-grouped shell obstruction retains its support, chronology, ratio and modulus hypotheses. It does not rule out arbitrary shell orders or the gapped density construction.
7. The predecessor-bound compactness equivalence is exact. The missing ingredient is one uniform bound function B valid across all finite intervals, not isolated finite avoidance. No such family is constructed here.
8. Every omega-enumeration of Z contains three-term progressions. Adenwalla's known five-term-free construction is reconstructed with endpoint, residue-list, and intervening -1 exposition repairs. It contains infinitely many negative-difference four-term progressions (0,-8^n,-2*8^n,-3*8^n), including positions (0,1,119,123) at n=1.
9. Geneson's density supremum-one result does not imply a full-support avoiding enumeration. The inspected scopes and source publication statuses are preserved, with no claim to comprehensive current literature coverage.

## Verification and limits

The independent audit did not execute candidate code, source-author code, Lean, or builds. Its separately authored finite checker ran in normal, -O, and -OO modes with byte-identical recorded results. Those finite checks are corroborative; global deductions rest on the written arguments. Publication preparation rechecked identities, exact patch application, editorial replay, strict additions-only Git replay and native tree identities. It did not rerun mathematical code, redownload sources, renew source-body inspection, or perform a new literature survey.

The audit is internal AI review, not an external expert referee report. No formal replay, novelty, priority, peer-review acceptance, or solution of the original target is claimed. The source-author repositories' formalization claims are attributed and were not certified here. Public hashes and sizes authenticate source and authored-artifact bytes only. Copied sources, extracted source text, images, datasets, raw output files and code are excluded.

## Authenticated authored identities

- Original REPORT.md: 24826 bytes; SHA-256 `7aa97201b795f0d2b43caa6a78ba2174ffe608de0c06d88a33736ef5e5b88aeb`.
- Original AUDIT.md: 30658 bytes; SHA-256 `b627d14c5f1f38b860fc26b45c9ba3128ad349bac756bff033cc8f8ca12a654f`.
- Corrected report before editorial edits: 24907 bytes; SHA-256 `a6e4e132832f5a0fe0838a26dac01cd5a6aeeb1150453453de62b83bd163556b`.
- Exact audit correction patch: 1473 bytes; SHA-256 `ab437cf4c22193d02f1b2960a6a45aa0b672925742ea0374e0d8625d35b28d12`.
