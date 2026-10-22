# Independent audit: integral skyline partial results

Problem 30001525 / OWR-4413-009, rank 977. Audit date: October 7, 2026.

## Verdict

**Accept the claimed mathematical partial results, with a verifier-hardening patch and clarifications supplied. Do not mark the unrestricted conjecture solved.**

The all-degree cyclic-basis property for S_n with n<=7, the single-skyline third-Bockstein family of exact order eight on S8, and the artificial preferred-basis obstruction all withstand this independent audit. Their logical scope is as stated in the frozen packet. The S8 result does not prove a complete S8 basis. Its detected target can generate an abstract order-eight direct summand, but no allowable skyline basis of the complement is established. No novelty claim is established.

The main actionable defect is computational: all 20 guards in the frozen verifier use Python assert, so optimized execution removes them. Four genuine mathematical mutants falsely print PASS under both -O and -OO. This is a validation robustness defect, not a counterexample to the theorem. The supplied explicit-check replacement preserves every original check expression and reproduces the original JSON byte-for-byte while rejecting every tested mutant in normal, -O and -OO execution.

## Frozen target and independence

- Pinned MANIFEST.json SHA-256: b1af9079189bd88ba892e682dc848de46448237539e68b5f624cab2aaab253fa.
- Seven payload files, 82,741 bytes: every size and hash verified.
- All six public source PDFs already accompanying the work: recorded sizes and hashes independently matched.
- The frozen directory is preserved byte-for-byte. Executable reruns use temporary copies; patches and corrected manifests are separate.
- No remote write, publication, third-party contact or additional worker was used for this audit.

## Mathematical review

Every proof section was read. The exact Sinha conjecture and coefficient context were inspected in the primary OWR report. The relevant primary Hopf-ring, Fox–Neuwirth, extended-power and Curtis–Wellington source sections were inspected. A further primary reference, May–Ponto's coefficient Bockstein treatment, was checked for cyclic-factor accounting and multiplicativity.

The detailed derivations are in MATHEMATICAL_SUPPLEMENT.md. Particularly important conclusions are:

1. An individual skyline source is a mod-2 cohomology class. Even corrections to an integral lift preserve that source. Explicit corrections through page three are provided. The audit does not certify division of the unmodified canonical Fox–Neuwirth representative.
2. The S4 monomial pairing argument is exhaustive in all degrees. C4 restriction forces d2(z)=y^2. The coefficient exact sequence and finite cyclic-factor counts justify actual integral generation and independence, not just page dimensions.
3. The S5–S7 odd-index argument gives injectivity on all Bockstein pages. Primitive single-skyline classes give odd-degree E2 surjectivity, and their d2 images give even-degree surjectivity. The field Kunneth step is legitimate and is not an integral tensor-product assertion.
4. The S8 equal-profile cancellation is valid. In the cited convention the columns are supported on four letters but have combinatorial width two; coefficient 6 is correct. The correction patch clarifies this terminology.
5. All ten C8 Mackey orbits and all 70 cosets are accounted for. The sole C2 orbit contributes zero because z vanishes on two disjoint transpositions. The sole C4 orbit contributes once. Corestriction sends s4 to s8 even though restriction sends s8 to zero.
6. Naturality rules out earlier boundaries for U_a and detects d3. A compatible integral lift produces an actual class killed by eight, whose restriction has order eight; thus its order is exactly eight.
7. The abstract free-complex example genuinely defeats unrestricted preferred-basis Smith reduction, while remaining explicitly outside the class of symmetric-group examples.

## Exact independent computation

Run python3 audit_verify.py from this directory. The verifier uses only the standard library and leaves the frozen packet untouched. It needs the sibling frozen packet and the separate patched verifier. Source PDFs are optional: available PDFs are checked, while absent PDFs are explicitly marked unverified on that rerun. Use --source-bytes to require the public PDFs. The recorded full audit verified all six PDFs; none is included in this audit.

The independent implementation reconstructs the S4 differential from generator values using a polynomial Leibniz rule, uses a separate row-elimination procedure, and constructs Q(i,j) by a closed symmetric-polynomial coefficient formula rather than the submitted recurrence. It checks degrees 0–100 and exactly reproduces all submitted degree-0–80 dimensions, factor counts and primary/secondary source selections.

Other checks include integral cyclic carry cocycles for C2, C4, C8 and C16; the distinction between restriction and corestriction in degree one; every C8 subset orbit with permutation cycle types on both blocks; transfer parity; odd indices and the power-of-two barrier; and the artificial complex by an independent determinant/gcd computation of its invariant factors.

AUDIT_RESULTS.json records 6,486 explicit checks, 101 independently checked S4 degrees, and 30 actual child-process baseline/mutation runs. Every baseline regenerates the original test JSON hash 1ba096cb9b60933759ef2b80ba0bbd9c95dfd5d00b0265c10d2c5c176476d98a. Original optimized baselines are recorded only as output reproducibility, never as successful validation.

The four mutations are loss of the y contribution in d1, loss of its z contribution, an incorrect C8 stabilizer assertion and reversal of the transfer-square parity claim. Normal original execution rejects all four. Original -O and -OO falsely accept all four. The hardened replacement rejects all four in all three modes.

Integrity controls reject both a changed payload byte and a changed payload accompanied by a newly self-consistent but unpinned manifest. The independent audit itself is also run normally and under -O/-OO; the separate execution record reports byte-identical audit results.

## Deliverables and corrections

- MATHEMATICAL_SUPPLEMENT.md: full mathematical audit and lift/order/generation details.
- audit_verify.py and AUDIT_RESULTS.json: independent exact checks and mutation evidence.
- PATCHES.diff: reviewable changes to PROOF.md and verify.py.
- patched/: a separate corrected packet with a regenerated manifest. Other original payload files remain unchanged; TEST_RESULTS.json remains byte-identical.
- SOURCE_VERIFICATION.json: public source metadata and precise inspection/dependency record.
- EXECUTION_VALIDATION.json: normal/-O/-OO reproducibility of the independent audit.
- AUDIT_MANIFEST.json: hash manifest for this audit and its corrected packet.

The proof patch is clarification, not an alteration of theorem scope. The verifier patch is a real implementation correction: explicit runtime checks replace assertions. The patch generator verifies each assertion has exactly the same condition after translation; no mathematical condition is removed or weakened.

## Limitations

This is a mathematical referee-style audit supported by exact finite checks, not a formal proof-assistant verification. It does not independently reprove the published full Hopf-ring theorem or directly calculate all integral Fox–Neuwirth differentials. Those are accurately identified dependencies. Infinite-degree claims are established by the written arguments, not by the finite run.

The inspected sources and targeted searches did not provide a complete integral skyline basis result. This remains a bounded literature observation; it does not certify the absence of unpublished or unindexed results. General conjecture status in the packet remains unresolved, and all five approach descriptions are consistent with their stated partial outcomes. The recorded chronology is a provenance claim, not something mathematical checking can independently reconstruct.
