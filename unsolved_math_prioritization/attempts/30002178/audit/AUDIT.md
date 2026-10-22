# Independent audit: 30002178 / OWR-12014-013

## Disposition

**PASS for the frozen package's scoped mathematical claims and its explicitly unresolved disposition. NOT a complete proof or counterexample.** The correct research status remains **unsolved, 5/5 approaches used**. No verified complete prior resolution, novelty claim, or global-openness claim is warranted by this audit.

This audit is separate from the author archive. The original archive was not modified. Its SHA-256 is `24f88fd09d1f753306be377bcb96e17a0dd85d2ccb674975873a6046ddcbe02d`, its size is 29,040 bytes, and it contains 13 files. The independently verified SHA-256 of its manifest is `12236b07d02cdc19409631ce6b56ae41d6509876a3c7fa200e2aafda1df329b6`. The machine-readable binding records the complete per-file comparison.

No substantive mathematical error was found in the five restricted proof routes. The missing conductor-uniform estimate is not supplied by their combination. Acceptance of these restricted deductions must not be relabeled acceptance of Conjecture 7.

## Target and source binding

The publisher PDF of Oberwolfach Report 42/2012 was freshly retrieved; its relevant extracted text and rendered printed page 2574 were independently inspected. Conjecture 7 fixes a positive number of summands m. Each summand's order divides the same integer d, repetitions are permitted, zero sums are omitted, and the quantity is ordinary complex modulus. The requested exponent depends only on m, with the inequality required eventually for every d. [Primary source](https://ems.press/content/serial-article-files/46413).

The archive's use of N in place of d is harmless. A least common multiple is not required: a larger common conductor remains a valid instance. Replacing a bound on each separate order by a common conductor needs an explicit least-common-multiple step. For fixed m this least common multiple is at most the product of the orders and therefore at most d^m; this preserves polynomial form but changes the exponent.

The identity labels ID 30002178, rank 716, OWR-12014-013 and the descriptor DOI are consistent with the supplied package and the directly inspected primary mathematical target. Raw dataset records, raw research reports and the numerical problem website were not inspected in this audit. No claim of equality to a raw row or prior AI answer is made. In particular, the descriptor's statement and review hashes remain declarations rather than independently verified content hashes.

A lower estimate c_m N^(-e_m), valid at all N, implies the eventual strict target after increasing the exponent, e.g. to e_m+1 and choosing N>1/c_m. Conversely, finitely many positive minima at small N absorb into c_m. The strict inequality is not obtained by silently replacing a non-strict inequality at the same exponent. Signs require positive coefficient mass sum |c_a|, and odd conductors may need enlargement to 2N.

## Route 1: algebraic norms and energy

For N>=3, complex conjugation pairs the phi(N) embeddings of the full cyclotomic field. The product of the squared moduli over the phi(N)/2 pairs is a positive integer. Isolating the pair containing the target value and bounding every other modulus by m yields |S|^2 >= m^(2-phi(N)). This argument uses field embeddings, including repeated values when S lies in a subfield. It does not confuse the number of summands with field degree. N=1,2 and m=1 are correctly treated separately.

For an odd prime p, summing |P(zeta_p^t)|^2 over nonzero t gives p H-m^2, where H is the sum of squared multiplicities. Thus the sum over conjugate pairs is (p H-m^2)/2. Applying AM-GM to the remaining (p-3)/2 positive squared moduli gives exactly the published prime-energy bound. Dropping the target summand from the available sum only weakens the result. For p=3 there are no remaining pairs and the norm directly bounds |S|^2 below by 1.

**Scope accepted. Gap remains:** phi(N) and p appear in the exponent. A bounded average and an integral product allow an exceptionally small factor as the number of factors grows. For example, the positive scalar list 2^(-k),2,...,2 with k copies of 2 has product 1 and bounded mean. This is a logical obstruction to that inference, not a claimed roots-of-unity counterexample.

## Route 2: geometry through four terms

The pair decomposition is valid with a nonnegative magnitude 2 cos(j pi/N), with 0<=j pi/N<=pi/2, and phase in mu_(2N). Absolute values and a possible sign in the half-angle formula are accounted for by the larger phase group.

For two terms, the smallest nonzero distance from opposition gives the conservative bound 2/N. For three terms, if the pair magnitude differs from 1, the integer 3j-N gives angular separation at least pi/(3N). The difference-of-cosines identity and the elementary chord inequality give the stated 2/(3N) bound. If the pair magnitude equals 1, the residual two-phase sum has the stronger lower bound 1/N; if the pair cancels exactly, the third root has modulus 1.

For four terms, unequal pair magnitudes differ by at least 4/N^2: both sine factors in their cosine difference are at least 1/N. For equal positive pair magnitudes, each magnitude is at least 2/N and the nonzero phase sum is at least 1/N. If both magnitudes vanish, the full sum is zero and is correctly excluded. Therefore the uniform 2/N^2 bound is valid. N=1 does not create a missing case.

These constants are deliberately conservative. The prior exact small-term results and correction to an older three-term value can be checked in Barber's Proposition 3; the five-term results there are upper constructions. [Barber v2](https://arxiv.org/abs/2104.15057v2).

**Scope accepted. Gap remains:** a lower bound on the modulus of a triple is not a lower bound on its distance from an arbitrary pair magnitude. The argument does not induct to unrestricted m=5.

## Route 3: factored constructions

A nonzero difference of N-th roots has modulus at least 2 sin(pi/N)>=4/N for N>=2. Multiplying r such factors gives the claimed restricted-family bound. Expansion contributes exactly 2^r occurrences before cancellation, and antipodes encode negative occurrences in mu_(2N). Coincidences do not lower the count of summands in the represented expression.

For even N, the binomial expansion of (1-zeta_N)^r is an exactly 2^r-term positive-root expression, remains nonzero, and has modulus at most (2pi/N)^r. For fixed r, this rules out any claimed eventual exponent E(2^r)<r. It does not rule out E=r or larger. Varying r with N varies m and does not contradict the fixed-m target.

**Scope accepted. Gap remains:** no universal factorization of arbitrary fixed-length sums, with controlled factors and coefficients, has been established.

## Route 4: exact prime counting

For p prime and 1<=m<p, a positive coefficient polynomial of degree at most p-1 and total m cannot be a nonzero rational multiple of Phi_p: such a multiple would have total coefficient mass divisible by p. Hence all nontrivial prime conjugates are nonzero, including repeated-root inputs. This statement fails without the prime hypothesis.

Evaluation of the full cyclic product R at 1 and at nontrivial p-th roots, followed by Fourier inversion, gives p r_0=m^(p-1)+(p-1)D. Removing the factors indexed by 1 and -1 gives p q_0=m^(p-3)+D T, where T is the sum of inverse squared moduli. The ratio displayed in the author proof follows by substitution. The empty product at p=3 is 1 and is consistently handled.

The inequalities M^(-2)<=T<=(p-1)M^(-2) have the correct directions. Thus a uniform polynomial upper bound on T is equivalent, up to a power of p, to the desired prime-case lower estimate. Positive multiplicities are preserved in the counts. The earlier counting paper's statements distinguish repeated-root and distinct-root variants; the archive derives its repeated-root version rather than silently importing a distinct-root theorem. [Author-hosted 2022 paper](https://qcheng2023.github.io/paper/sum_roots.pdf).

**Scope accepted. Gap remains:** D>=1 alone leaves exponentially large counting quantities. The necessary polynomial bound for the ratio is not proved. Even the prime case alone would not settle composite conductors.

## Route 5: sparse Taylor argument

Distinct integer exponents make the falling-factorial evaluation matrix invertible, since its determinant is the ordinary Vandermonde product. Consequently the multiplicity q at 1 is at most s-1. For a nonzero integer polynomial, division by the monic factor (x-1)^q leaves an integer quotient Q with |Q(1)|>=1.

The partial-sum formula for one division gives an l1 coefficient bound at most A times the original bound; iterating gives ||Q||_1<=L A^q. The derivative is bounded by A||Q||_1 on the closed unit disk. The segment from 1 to a point on the unit circle stays in that disk, so the stated perturbation estimate is uniform on the stated neighborhood. The threshold N>=4pi L A^(q+1) guarantees |Q(zeta_N)|>=1/2. Combining this with the chord bound gives |P(zeta_N)|>=(1/2)(4/N)^q. The argument includes q=0.

This is a complete local estimate with a stated remainder control, not merely a formal leading-term expansion. Large A is the central limitation: arbitrary target tuples may have spread comparable with N, and rotation does not uniformly reduce it. For exponents 0,33,67 modulo 101 the minimum spread over all rotations is 67. No arithmetic approximation theorem controlling arbitrary nearby vanishing configurations is supplied.

**Scope accepted. Gap remains:** the threshold cannot be discarded or made uniform in all target exponent tuples by compactness alone.

## Independent computations and author replay

The author checker was inspected before execution. Its exact-zero test via reduction modulo Phi_N is valid, and the rational cosine remainder and outward rounding are sound. Rotation to a multiset containing 0 covers every possible modulus while allowing duplicate representatives of an orbit; the author correctly calls these normalized multisets, not distinct orbits. Minimums of lower and upper endpoints enclose the true minimum. The reported upper witness need not be a unique minimizer.

Author scripts were run from an extracted copy. All 67,380 checks, 46,803 normalized multisets, 21 counting examples, 12 Taylor cases, eight semantic controls and nine integrity corruptions replayed. Normal and Python -O result bytes both match frozen RESULTS.json exactly. The frozen originals were rehashed afterward.

The separate standard-library-only checker imports no author code and uses different mechanisms:

- A Ramanujan-sum trace of |S|^2 gives an exact zero criterion. The trace is a sum of nonnegative conjugate squared moduli; it is zero exactly when S is zero. A separately coded integer cyclotomic construction cross-checks it.
- Real and imaginary coordinate rectangles use pi=8 arctan(1/3)+4 arctan(1/7), independent of the author's Machin identity. Cosine and sine Taylor remainders, argument uncertainty, and all rounding are rational and outward. Their minimum enclosures must lie inside the author's reported enclosures.
- Direct enumeration of the counting choices replaces cyclic-convolution code. Norms are determinants of multiplication matrices, and inverse-square traces are obtained by exact rational matrix inversion, replacing resultants and symbolic polynomial inversion.
- Binomial shift coefficients independently identify Taylor multiplicity. Exact division, derivative coefficient bounds, and certified conductors check the local estimate. Evaluation is factored to avoid losing information through high-order cancellation.

The independent result file contains precise check totals, all 109 finite (m,N) rows, all 21 counting cases, all 12 Taylor cases and 17 semantic/quantifier controls. These are finite corroboration. The infinite deductions were audited as proofs, not inferred from the computations. All runtime checks raise exceptions and remain active under -O.

## Literature quantifiers and limits

Eight public scholarly PDFs were freshly retrieved, and every byte count and SHA-256 matches the frozen source metadata. Relevant sections were inspected, not every proof in those sources. Only public verification metadata and original audit discussion are included here; no PDFs, source extracts or images are distributed.

- Habegger's The Norm of Gaussian Periods, Theorem 3, limits the number of very small conjugates for each fixed prime. It does not exclude every bad embedding. [Version inspected](https://arxiv.org/abs/1611.07287v1).
- Habegger's Diophantine Approximations on Definable Sets, Theorem 7, bounds the number of bad primes up to a cutoff for fixed nonzero coefficients. This is a different paper and a different exceptional set. [Version inspected](https://arxiv.org/abs/1608.04547v1).
- Dimitrov–Habegger Theorem 1.1 controls a Galois average of logarithms under an essentially-atoral hypothesis and a sufficiently large strictness parameter. It is not a uniform individual-modulus bound. [Version inspected](https://arxiv.org/abs/1909.06051v2).
- Nahshon–Shpilka Lemma 3.14 selects a suitable prime from a controlled interval depending on the polynomial. Its universal quantifier over roots applies after that existential prime selection, not at every prescribed conductor. [Publisher statement](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/new-bound-on-cofactors-of-sparse-polynomials/2CADDB77D2E5CBFB7B803CCCAC49D2FD).
- Cornelissen–Hokken–Ringeling study Mahler measure/height for selected Gaussian periods. Kalogirou's Theorems 1–2 provide upper constructions, including a seven-term O(N^(-3/2)) bound. Neither stated result is the universal lower estimate sought here. [Gaussian periods v3](https://arxiv.org/abs/2507.09303v3), [Small sums v1](https://arxiv.org/abs/2607.06098v1).

No older full text was independently audited solely because a later paper cited it. Publication metadata in the author archive beyond the inspected public pages is not an assertion that every journal version was freshly fetched. No exhaustive literature search or historical absence claim is made.

## Publication boundary and conclusion

The audit deliverable contains only authored analysis, independent code, exact test results, hashes, sizes, public links, scope/status data and integrity records. It excludes source PDFs, extracted source text, rendered pages, raw corpus data, and private coordination material. It makes no remote writes.

The package may be represented as an audited unresolved five-route investigation with valid restricted results and reproducible finite checks. It must retain unsolved status, 5/5, and explicit non-claims of a full proof, a counterexample, a verified complete prior resolution, novelty or global openness.
