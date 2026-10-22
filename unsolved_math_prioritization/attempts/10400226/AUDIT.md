# Independent mathematical acceptance audit

Audit date: 11 October 2026 (UTC).

## Verdict

**PASS for the exact frozen candidate and the original unrestricted-knot existence question.** No mathematical correction to the frozen reconstruction is required. This is an independent AI-assisted mathematical audit, not human peer review, external refereeing, or a novelty determination.

Audited candidate: `CANDIDATE.md`, 5,108 bytes, SHA-256 `a6a32909a92496a5f2da3136ddbd722512447250d5b2bd2c86d8e4f456440065`. The content is an unchanged copy of the frozen input. Its complete argument is expanded in `PROOF.md`.

The accepted conclusion is: every integer n = 4k + 1 with k > 0 occurs as the determinant of a tame knot in S³ of signature four. Genus at most two is established outside the remaining square case; genus at most three is established in that case.

## Original hypotheses and prior attribution

The actual problem was read in the pinned Ohtsuki PDF, both extracted text and rendered physical p. 168 (printed p. 540). Problem 12.21 attributes the question to Y. Shinohara and asks precisely for a knot of determinant n and signature four when n = 4k + 1, k > 0. It imposes no genus, primeness, alternating, two-bridge, or hyperbolicity condition. In particular, use of a connected sum or a genus-three surface does not weaken the requested answer.

Stoimenow's pinned PDF, physical p. 21 (printed p. 383), was also checked as text and image. Its §5.1 / Question 5.1 asks the equivalent determinant-set question, and Proposition 5.1(1)–(2) records the relevant divisor and multiplicative closure phenomena. This audit does not rely on any assertion that the 2007 state of the literature remains current.

The construction was previously stated by Alper Ferudun on 2 October 2026, Theorem 1.1 and Lemmas 3.1–3.2, DOI https://doi.org/10.5281/zenodo.23111900. The frozen preprint's central proof page was independently read in text and image. Its front matter says unrefereed; p. 8 discloses AI-assisted work. The publicly accessible manuscript page also states these facts. The author and prior construction are attributed prominently. Publication or DOI registration is not treated as mathematical validation.

## Proof obligations checked independently

1. **Integer entries.** The even-y requirement makes y/2 integral. The arithmetic argument explicitly enforces this parity; it is not a dropped hypothesis.
2. **Knot realization.** The four-dimensional matrix has skew part J ⊕ J and the final six-dimensional matrix has skew part J ⊕ J ⊕ J, each determinant one. These satisfy the ordinary classical knot realization criterion. Friedl's introduction independently states realization for every integral matrix with skew determinant one. The exact one-boundary-component and genus conditions also agree with Theorem 7.6 in the Kyushu-hosted lecture slides. No higher-dimensional-knot theorem, stabilization, or merely S-equivalent realization is substituted.
3. **Invariant conventions.** The knot determinant is the absolute value of the symmetric determinant. In the last case that determinant is negative, so retaining the absolute value is essential and correctly done. Signature is symmetric-form signature. Mirroring resolves any opposite convention in the problem's convention without changing determinant.
4. **Principal minors.** Direct tridiagonal expansion gives the four listed determinants. The identity 2D₃ = D₄ + D₂ is exact. The assumptions b ≥ 1 and D₄ > 0 force all four leading determinants positive. This is enough for positive definiteness by Sylvester's criterion; no missing additional condition on c or y is needed.
5. **Squarefree reduction.** For odd nonsquare n ≡ 1 (mod 4), n = s²m has m > 1 odd squarefree and m ≡ 1 (mod 4). Thus a prime r dividing m exists and is odd.
6. **CRT and reduced progression.** The chosen moduli 4, r, and m/r are pairwise coprime. The m/r = 1 case is harmless. The resulting t is a unit modulo 4m and has exactly one negative local quadratic character, giving Jacobi symbol −1.
7. **Unbounded prime existence.** Dirichlet applies to the reduced progression. Excluding the finitely many primes dividing s leaves an admissible prime. The progression already excludes primes dividing m. Consequently the Legendre symbols in the next step never vanish. Finite search is not used as proof of this step.
8. **Reciprocity.** The sign in reciprocity is +1 because m ≡ 1 (mod 4), including when m is composite. Squareness of s modulo ℓ then gives (n/ℓ) = −1. Since ℓ ≡ 3 (mod 4), the factor (−1/ℓ) reverses the sign. The eventual square-root conclusion has prime denominator ℓ, so there is no invalid inference from a Jacobi symbol with composite denominator.
9. **Parity and positivity.** Inverting 2 modulo the odd prime ℓ and adding ℓ when needed preserves the congruence and fixes y's parity. The quotient h is positive, congruent to 3 modulo 4, and therefore at least three. Both b and c are positive integers.
10. **Prime-divisor branch.** Whenever a prime ℓ ≡ 3 (mod 4) divides n, the quotient n/ℓ is again congruent to 3 modulo 4. The y = 0 construction works even for squares. This branch is distinct from the nonsquare existence argument and remains available when that argument's m would equal one.
11. **Remaining squares.** In the remaining case every prime p dividing s is at least five and congruent to 1 modulo 4. Applying the nonsquare result to p is valid and noncircular. The quotient h = n/p is congruent to 1 modulo 4. The block W has skew determinant one and symmetric determinant −h < 0, hence inertia (1,1,0). Direct sum gives inertia (5,1,0), signature four, and absolute determinant n.
12. **Exhaustiveness and exclusions.** Every admissible n is nonsquare, is a square possessing a 3-mod-4 prime divisor, or is a square whose prime divisors are all 1 modulo 4. The excluded value n = 1 is never used. There is no claim of a genus-two construction for every square.

## Independent finite diagnostics

An independent exact diagnostic program was newly authored for this audit; no source-author code was obtained or run. It follows the literal CRT progression in the nonsquare branch. It uses exact trial-division primality, integer CRT and Legendre/Jacobi calculations, determinant expansion over permutations, and rational congruence elimination for inertia. No floating-point eigenvalue tolerance is used. No correctness check is implemented with a Python assert statement.

It passes for all 2,500 admissible n from 5 through 10,001, plus four distinct additional large cases, for 2,504 distinct n in total. Case counts are 2,453 nonsquares, 35 square cases with a 3-mod-4 prime divisor, and 16 remaining squares. A further 1,427 checks exercise the y = 0 branch whenever applicable, including nonsquares. All constructed matrices have integral entries, skew determinant one, absolute symmetric determinant n, and signature four. Four-dimensional outputs have four positive leading minors.

The largest prime encountered in these finite, literal-CRT tests is 1,342,291. Thirty-five tested n require skipping an initial progression prime dividing s, explicitly exercising that otherwise easy-to-miss condition. This maximum is only a property of this finite test, not a universal prime bound.

The three examples in the frozen candidate were separately verified:

- n = 33,049 with b = 5, c = 437, y = 6: leading minors 2, 19, 16,534, 33,049; inertia (4,0,0).
- n = 5 with b = 1, c = 2, y = 2: leading minors 2, 3, 4, 5; inertia (4,0,0).
- n = 25 from the n = 5 block plus W(5): signed symmetric determinant −25; inertia (5,1,0).

Negative controls reject n = 1, an input in the wrong congruence class, odd y, and a W parameter in the wrong class. A negative-D₄ example is confirmed not to be positive definite. Running the diagnostics under ordinary Python, `-O`, and `-OO` produces byte-identical results. These finite checks corroborate the construction and guard against transcription mistakes; the all-n proof rests on the mathematical argument and named standard theorems.

## Source and integrity audit

The three primary source PDFs match their recorded byte counts and SHA-256 hashes. The additional mathematical-input references were independently retrieved, hashed, and inspected. `SOURCE_PINS.json` identifies sources, public URLs, exact byte pins, and the inspected locations. `RETRIEVALS.json` records successful supplemental downloads and one failed direct HTML request. The latter failure does not become a claimed HTML byte pin: the manuscript's status was independently available in the pinned PDF and through the web reading tool.

`MANIFEST.json` is a closed-world inventory of every public file in this packet other than the manifest itself. The source byte pins identify inspected source artifacts; they do not imply that source copies are distributed here. `CHECK_RESULTS.json` gives aggregate diagnostic results and fresh ordinary, `-O`, and `-OO` execution comparisons. Integrity checking rejects altered, missing, extra, symlinked, or otherwise nonregular entries. The manifest is externally sealed. Integrity seals establish consistency with a frozen packet, not mathematical truth or human authorship.

## Limits of acceptance and publication boundary

This audit accepts the complete proof of the exact existence statement. It does not claim novelty, exhaustive literature coverage, human review, refereed status, or institutional endorsement. It does not audit the source's full classification theorem, lattice-theoretic route, finite knot tables, minimal crossing-number assertions, universal genus-two possibility, or source-author programs. No such ancillary claim is needed here.

This public packet contains the complete authored proof, candidate, mathematical audit, and acceptance report, together with public-source metadata and aggregate checks. It distributes no copied third-party source documents, extracted source text, inspection images, executable scripts, or raw test matrices or witness datasets. The symbolic matrix formulas in the authored proof are part of the mathematics. The public editorial map records presentation-only changes; no mathematical correction, proof step, hypothesis, quantifier, or caveat has been removed.
