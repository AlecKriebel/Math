# Verification and publication verdict

Version 1.0.1, 23 September 2026 UTC. Unrefereed, AI-assisted mathematical audit.

**PASS for the exact printed limit-existence question.** The proof establishes the claimed limit for every nonzero nonnegative multiplicative function under F(2x)/F(x) -> 1. The all-dilations condition in the source implies this, and monotonicity also proves the converse. There is no remaining mathematical gap in that theorem identified by the audits.

**Qualified priority result.** No exact earlier resolution was located. Close predecessors in Yeats (2002, 2003) were checked and do not immediately imply the theorem in its full generality. Bell (2004) and other broad sources could not be fully inspected. Earlier published or folklore appearances of this elementary principle remain possible. The package does not claim certified originality.

**Source limitation.** The original report's proposed weighted Euler-factor value contradicts its printed hypothesis. The explicit example f(n)=1/n has actual limit 1/2 and the printed prediction 3/4. The package resolves the printed question and corrects that constant; it does not resolve the possible intended index-one variation problem or establish the proposer's intent.

## Proof obligations

| Obligation | Evidence | Status |
|---|---|---|
| Positive denominators | Nonzero multiplicativity forces f(1)=1 | Pass |
| Correct decomposition | Unique n=2^k m, m odd; coprime multiplicativity | Pass |
| Finite-sum upper estimate | A_K F2(x) <= F(2^K x), K fixed before the limit | Pass |
| Infinite local sum | Upper estimates and nonnegativity force zero | Pass |
| Finite local sum | F(x) <= A F2(x) supplies matching lower bound | Pass |
| No hidden growth premise | Bounded F allowed, no infinite limit/sum interchange | Pass |
| Independent mechanism | Vanishing boundary increments and tail domination; probability formulation | Pass |
| Original source | Visually inspected EMS PDF p.3066; browser inspected catalogue | Pass |
| Correct publication scope | Source mismatch explicit in title context, abstract, text, site and metadata | Pass |

## Computational evidence

`python3 verification/verify.py` and `python3 -O verification/verify.py` passed with identical results. Runtime dependencies: Python 3.9+ standard library. Explicit checks remain active under optimization.

- 243 nonnegative multiplicative fixtures, including functions that are not completely multiplicative.
- 15,552 exact prime-power decomposition checks.
- 62,208 exact fixed-dilation inequalities.
- 15,552 finite-local-sum inequalities.
- 34,992 checks of the separately derived convolution increment bound.
- 1,024 example checks, including harmonic sums, finite and infinite local sums, and an index-one control.

All arithmetic is integer or rational; there is no floating-point tolerance. These are finite diagnostics, not a universal proof or proof-assistant certification. The general proof is the short analytic argument in the manuscript.

## Independent audits

The original proof and final-review records below refer to version 1.0.0 and retain their historical hashes. Version 1.0.1 changes access information and PDF metadata only; its theorem, proof and verifier are unchanged. Two fresh sequential preprint reviews were completed, with the two access findings corrected between rounds; the second review found no actionable issues. Full disposition and exact final manuscript/PDF/verifier hashes are recorded in `preprint-readiness.md`.

- `adversarial-proof.md`: detailed line-by-line check, second proof, eight boundary cases.
- `independent-derivation.md`: weighted-probability derivation, quantitative bound and scope tests.
- `priority-independent.md`: queries, closest predecessors, precise differences and access limits.
- `final-review.md`: independent final manuscript and verifier audit.
- `source-match.md`: primary and secondary statement comparison.

The final wording makes the nonzero standing assumption explicit and names the precise Yeats theorem and proposition. This is an AI audit, not external human peer review. No individual was contacted.

## Artifact checks

The paper compiles with Tectonic and is three pages. Every page is visually reviewed at publication time. Source, metadata, scripts, audit reports and paper are included in the deterministic source archive; full third-party source publications are excluded. The package builder verifies local site links, mirror hashes, ZIP contents and SHA-256 manifests. Version-specific public deployment evidence is recorded separately in the repository; it is operational history outside the research archive.
