# Independent prior-proof scope audit

UTC: 2026-10-24 23:04:25. Completion estimate: 100% of this narrow source challenge; no estimate of a new discovery.

Source: Natanael Wildner Fraga, *Protected p-Division and the Extended Agrachev–Gamkrelidze Construction for Finite Pre-Lie Rings*, v1, posted 28 August 2026, DOI [10.20944/preprints202608.2109.v1](https://doi.org/10.20944/preprints202608.2109.v1). Read primary HTML Sections 2–8 and the publisher-served PDF text, independently of other agents' preparation.

**Verdict: no substantive gap or counterexample found in the checked protected calculus and affine BCH closure. Treat this as prior art for its explicit corrected prescription.** The preprint is expressly unrefereed. This is a human-readable independent mathematical check, not formal verification or a human peer-review certificate.

The source's algebraic hypotheses match Definition 59 of [2410.20440v2](https://arxiv.org/html/2410.20440v2): finite additive p-group, pre-Lie identity, p>3, m=floor((p−1)/4), and both Property 3 inclusions. No homocyclicity, independent nilpotence assumption, or fixed globally iterable arbitrary section was needed. Formula-level comparisons are explicitly with that arXiv version; this audit does not compare the accepted JPAA text.

The critical checks were the local annihilation of section defects, preservation of protected markings under substitution, and affine closure. For a degree-d right-comb coefficient with p-denominator t, d≥4mt+1 leaves an inner bracket of degree ℓ=d−2mt≥2mt+1. Its value has a p^t-root. The chosen affine lift and the protected divided operator differ by p^t-torsion. Expanding 2mt outer commutators leaves at least mt letters on one side of that defect, which annihilate it. This establishes actual return to the affine image. The finite group action then has trivial unit stabilizer and |A| elements, establishing the orbit bijection and transported brace law. The integral Lyndon-basis theorem remains an identified external dependency, rather than being independently reproved here.

## Presentation caveat and exact identities used

The web display of (12), (14), and (27) loses the necessary exponent grouping. Equation (14), visually inspected in the live HTML, reads −s+t rather than −(s+t). The extracted PDF text has the same ambiguity. Remark 1 and the accompanying proofs explicitly prescribe reducing the number of divisions by one under multiplication by p, and adding division counts under products. The identities independently checked here are

\[
p\langle p^{-s}w\rangle=\langle p^{-(s-1)}w\rangle,
\quad
\langle p^{-s}u\rangle\langle p^{-t}v\rangle
=\langle p^{-(s+t)}uv\rangle,
\]

with total division count s0+Σsi after flattening. These follow directly from cancelling a section or concatenating protected markings. Thus the printed/extracted signs must not be quoted as correct. Their repair does not replace the central closure mechanism with an unsupported claim. Original PDF equation typography was **not visually verified**: its text was readable but the available viewer could not navigate to the relevant page. No claim that the mismatch is definitely a conversion artifact is made.

## Independent falsification checks

`check_operator_words.py` uses no external packages. On Z/27⊕Z/9, p=3, m=2, it tests a jointly contractive noncommuting operator family and three nonadditive, nonnormalized local sections. These are tests of the abstract operator lemmas, which allow arbitrary p and m; they are not examples for the p>3 exponential theorem.

Results: 3,888 contraction-point checks, 864 protected marked maps, 2,834,352 input-additivity comparisons, 11,664 division-cancellation checks, 144 operator-slot comparisons, and 240,000 exponential/logarithm denominator inequalities. All pass. Finite tests supplement the unbounded proof reasoning and do not prove the general theorem by themselves.

A second internal reviewer, `shield_budget`, independently read the primary source and found no gap in flattening, endpoint-factor cases, denominator-preserving right-comb rewriting, or the affine torsion-defect argument. That reviewer likewise did not independently reprove the integral Lyndon theorem or inspect original PDF typography.

## Priority consequence and limits

This establishes a concrete prior proof mechanism, rather than merely a prior abstract assertion. It does **not** establish that every possible clarification of the original displayed formulas is equivalent, or that the literally uncorrected string defines a group operation. It gives no basis for an original-solution claim or new upload from this project. A claimed relevant preprint remains prior art even before peer review.

Source receipts hash the web-tool-rendered snapshots actually obtained. Direct HTTP download returned 403, so neither raw HTML nor PDF bytes are claimed to have been archived or hashed. No outside communication, git mutation, upload, or heavy dependency installation occurred.
