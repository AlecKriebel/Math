# Independent adversarial audit: type-A clasp prior-formula dossier

Problem 30004222 / OWR-17135-015; queue rank 718. Audit date: 2026-10-05 UTC.

## Verdict

REVISE REQUIRED for the frozen dossier. Its normalization assertion is mathematically false under the published definition it cites: the multiplicative factor N' of Eq. (5.15) has inverse square, not square, equal to the local intersection scalar. The dossier's statement that this is merely an omitted-square abbreviation in Theorem 5.11's prose understates the actual inconsistency.

The repair is explicit and noncircular. `REPLACEMENT_PROOF.md` derives the fixed-step q-binomial quotient B=(N')^(-2), proves B=K for every admissible strip, and identifies the representation-theoretic inputs that imply kappa=B. No unresolved normalization assumption remains in that reconstruction. It is a dependency-aware reconstruction of the cited prior theorem, not an assertion that the printed proof is literally consistent or a claim to a new theorem.

The correct final substantive disposition remains qualified: prior all-rank type-A formula, with a representation-theoretic argument containing tableau combinatorics. Neither an unqualified purely combinatorial solution nor a result for other Lie types or arbitrary roots of unity is certified. If the larger workflow records substantive attempts, 1/5 with qualified partial/prior-formula status is appropriate; no five-approach completion or `verified_solved` decision follows from this audit.

## Exact binding and preservation

The input is the frozen release manifest whose SHA-256 is

    975d9a7f2d13ab2564defe4d9965fb7e62586d71fa6f80760b4410047af243bb

All seven listed files match their recorded byte counts and SHA-256 hashes. The exact directory allowlist was checked. The release verifier passes and its mathematical replay equals the recorded JSON. Originals were not modified. The audit is a separate tree; only its `safe` directory is a candidate release. Source PDFs, text extracts and rendered images remain outside it.

See `FROZEN_BINDING.json` for exact file-level binding and source-PDF hashes, `AUDIT_RESULTS.json` for structured findings, and the audit `MANIFEST.json` for the safe output allowlist. The audit manifest excludes itself from its content list; its external hash is reported separately.

## What was independently inspected

1. Elias's 2019 Oberwolfach contribution, printed pp. 2426-2429. The final formula and request on pp. 2428-2429 were freshly rendered and visually inspected. The statement uses gl_n, an exterior-power weight, two dominant endpoints, a preferred basis, and precisely the roots whose denominator pairing is smaller by one. The earlier sl_2 sign difference is expressly distinguished in the original report.
2. Elias's *Light ladders and clasp conjectures*, especially Definition 3.13, Claims 3.14-3.15 and Conjecture 3.16 on pp. 53-54, with the Weyl-dimension discussion thereafter. The permutation convention and selected 01 roots were checked against the later paper.
3. Martin-Spencer's published 36-page PDF, including its first-page publication metadata, Def. 2.11 and Conjecture 1, Eq. (2.15), Eq. (4.4), Section 5's skew Howe map, Section 5.1 form compatibility, Lemma 5.4, Eqs. (5.10)-(5.16), Lemma 5.7, the divided-power/light-ladder comparison, Lemma 5.10 and Theorem 5.11. Fresh visual inspection covered pp. 8, 11, 27, 31-32 and 34-35. The normalization mismatch is visible in the PDF pixels, not inferred from a damaged text extraction.
4. Matching arXiv v4 text, including the same inverse-half-power normalizer and contrary square label. Version history was independently checked on arXiv: v1 18 October 2022; v4 11 February 2026. The publisher's article page and first PDF page agree on publication on 26 March 2026, DOI 10.1007/s00209-026-03990-0.

This is targeted primary-source verification and a full audit of the dossier's elementary mathematics. It is not a line-by-line independent reconstruction of every external representation-theory theorem or every diagram reduction in the paper. In particular, the foundational Cautis-Kamnitzer-Morrison and Tolstoy/Quesne results are named dependencies, not secretly treated as independently reproved results.

The exact UnsolvedMath live page and upstream raw statement/AI report remain uninspected. The original dossier's HTTP 403 report is preserved; this audit did not retry or work around that access restriction. The ID/title/code binding comes from the frozen descriptor, while the mathematical scope is independently checked against the original 2019 report. Neither dataset hashes nor the old catalog state substitute for content inspection. Historical repository-search observations were not re-executed and are not used to prove novelty.

## Findings and precise corrections

### F1. Substantive: reciprocal normalization is wrong in the frozen dossier

Affected frozen locations:

- `RESULT.md`, the paragraph following elementary bridge proof 5, which identifies kappa with N'^2;
- `RESULT.md`, the dependency/notation-hazard paragraph, which presents Lemma 5.10 as an unambiguous square fix;
- `RESEARCH_LOG.md`, the claim to have checked the normalization square;
- `EXACT_CHECKS.json` and `verify_clasp_bridge.py`, whose norm-versus-square negative control does not test the actual source normalizer and consequently misses this defect;
- the overall verification status insofar as it relies on the inaccurate normalization bridge.

Source location map:

- Eq. (5.10), published p. 25: the original norm constant is used inversely;
- Eq. (5.13), p. 27: rewriting with divided powers yields factorials times the square root of a q-binomial quotient;
- Eqs. (5.14)-(5.16), p. 27: the divided-power multiplicative normalizer N' is that quotient to power -1/2;
- Lemma 5.10, p. 31, and its conclusion on p. 34: the printed N'^2 label instead identifies the direct quotient with kappa;
- Eq. (5.38), p. 32: the direct quotient is labeled N'^2 and includes an all-j product although the left side is a single parent/child step;
- Theorem 5.11, pp. 34-35: its prose identifies the normalizer itself with the desired scalar, conflating normalizer, squared normalizer and unnormalized squared norm.

Exact minimal witness: T=[1,2], T'=[1]; old gl_2 weight (1,0), increment (0,1), new weight (1,1). Here kappa=[2] but N'^2=1/[2]. Values are 2 versus 1/2 at q=1 and 5/2 versus 2/5 at q=2. This also follows directly from the split-merge coefficient and from the highest-weight-two quantum sl_2 norm, so it does not assume the all-rank conjecture.

Correction: define B=(N')^(-2) using fixed j=s in Eq. (5.15). The independent proof establishes B=K by q-factorial cancellation, then uses the actual form compatibility and norm recursion to obtain 1=N'^2*kappa. Therefore kappa=B=K. The printed Lemma 5.10 cannot be quoted literally as its justification.

The all-j issue also has an exact witness: T=[1,2,3], T'=[1,2], q=1. The last-step B is 3; the product over all steps is 6. A parent quotient is required if that global product is used. The replacement avoids it entirely by fixing the final step, and verifies earlier-step cancellation explicitly when presenting the equivalent path argument.

### F2. Confirmed: Eq. (2.15) really has inconsistent priming

Fresh pixels on published p. 11 confirm both defects: lambda' is declared the smaller partition, but a selected index is required to satisfy lambda'_k=lambda_k+1; the displayed distance uses the larger partition. The frozen warning about impossible priming was justified, unlike a merely suspected extraction error. It should be sharpened to mention both parts.

For old alpha=(1,0), new beta=(1,1), the literal selected set is empty, yielding 1 instead of [2]. Reversing only the increment condition while retaining the outer distance yields [1]/[0]. The replacement must use beta_b=alpha_b+1 and distances alpha_a-alpha_b+b-a, as in the original root statement and the starting product on p. 31. No formula is silently repaired.

### F3. Additional root-direction hazard in the source

Under the standard left action, Conjecture 1's prose on p. 8 sends mu to a dominant weight while retaining w_mu^(-1) in its root-set definition. Elias's Definition 3.13 instead sends the dominant weight to mu. The paper's own coordinate description on p. 9 selects the intended 01 pairs.

Example mu=(0,1,1): the minimum permutation sending mu to (1,1,0) is [3,1,2]. Taking its inverse-root inversion set gives {(1,3),(2,3)}, whereas the intended 01 set is {(1,2),(1,3)}. Thus simply repeating the published w sentence without a convention check is unsafe. The frozen dossier's direct coordinate definition avoids this defect, and the replacement retains that safer definition. This issue is convention-qualified and does not affect the independently specified coordinate product.

### F4. Elementary claims otherwise pass

The root-coordinate calculation, dominance/zero-denominator equivalence, characteristic-zero q=1 specialization, central-shift invariance, horizontal-strip telescoping with the final row group, and t^2 rescaling of a bilinear preferred-basis pairing are sound. The elementary tableau identity does not itself identify a local intersection form; the dossier correctly treats that as a separate representation-theoretic step. The false N'^2 identification must be removed from the otherwise correct rescaling discussion.

## Independent diagnostics

Two distinct checks were done: an exact replay of the frozen standard-library script, and a separately authored script importing none of the frozen code. The independent script enumerates vertical weights directly from binary vectors and selects horizontal strips by testing distinct new-box columns among all bounded partition pairs.

Reproduced counts:

- 7,085 admissible vertical strips;
- 10,935 failures of endpoint dominance, each detected by a zero denominator index;
- 7,085 central-shift checks;
- 12,173 horizontal strips, with exact factor-multiset equality between the column-root formula and row telescope;
- all six advertised negative controls rejected.

Stronger checks added:

- all 12,173 horizontal cases also match the fixed-step inverse-square lowering quotient B;
- 36,519 exact rational evaluations for horizontal formulas at q=1, 2 and 3/2;
- 14,170 exact checks of q-to-minus-q parity;
- 25 low-rank endpoint-weight/parity checks and the gl_2 ratio (m+1)/m;
- explicit reciprocal-normalizer, all-j-product, partial-priming-fix and permutation-direction negative witnesses;
- a roots-of-unity obstruction: lambda=(2,0), mu=(0,1) gives [3]/[2], whose denominator is zero and numerator is -1 at q=i;
- q=1 values of the finite Laurent q-integer for m=1,...,40.

These computations compare algebraic formulas; they do not construct or evaluate arbitrary-rank web diagrams. Exact factor-multiset equality is a sufficient identity check in Q(q), and the unrestricted identities are proved separately in `REPLACEMENT_PROOF.md`. The horizontal diagnostics include harmless empty/full strips beyond the nontrivial exterior-power claim, clearly as product identities.

The original six controls were useful but insufficient: its sixth control established only that a positive scalar need not equal its square root. It never read or evaluated N' from the cited paper, which is why it could pass while the normalization bridge was false. The original q=1 loop likewise checked the number of monomials, not the full normalization inference.

## Scope and release decision

The corrected proof is type A at generic q, with characteristic-zero q=1 obtained through nonzero denominators. The rank convention is gl_n/sl_n versus root type A_(n-1); the increment is a weight of an exterior power and must have 0<k<n; both endpoints must be dominant. A determinant shift preserves the formula. No extra parity restriction is justified. No arbitrary nonfundamental weight, other Lie type, positive-characteristic theorem, or unrestricted root-of-unity result is supplied.

A formula theorem is relevant to the 2019 request but does not, by itself, satisfy every meaning of a combinatorial explanation. Here the explicitly corrected bridge still uses quantum skew Howe duality, extremal projectors and an external orthonormal basis theorem. The qualitative qualification is essential. Do not call the formula open; equally, do not turn this into an unqualified purely combinatorial resolution.

No remote writes, branch changes, contacts, queue changes or publication were performed. The safe output is authored audit analysis, code and public verification metadata only. A revised candidate should incorporate the explicit reciprocal correction, source notation caveats and strengthened controls, then receive a delta check against its own manifest before it is described as audit-passed.
