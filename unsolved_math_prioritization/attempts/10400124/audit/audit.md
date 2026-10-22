# Independent audit: flat-connection growth exponents

Problem 10400124, AMR-103-0124; catalog rank 846. Audited 2026-10-06.

## Verdict and accepted scope

**ACCEPTED AS A PARTIAL RESULT AND FORMULATION AUDIT. No correction patch is required.**

The acceptance applies to the immutable author archive with SHA-256 `232a49f83dd1fc6f79cf82c09a2d8d50fba28a02a716d26ae06f361672b1a172` and size 10,575 bytes. Its four members were checked individually. The author files were not edited.

The package correctly proves an identically absent grouped Chern-Simons sector for the stated lens spaces, verifies the growth exponent for every connected sum of copies of S1 x S2, and isolates the missing noncancellation hypothesis in a componentwise argument. The lens-space example obstructs the interpretation of the original Conjecture 7.7 requiring a **nonzero amplitude at every classical phase**. It is not a counterexample to Conjecture 7.9 read as a conditional statement about stipulated nonzero-sector expansions. It also does not contradict a convention allowing zero series and assigning them formal exponents.

No general proof, general counterexample to that conditional assertion, new literature result, or exhaustive status search is accepted or claimed.

## 1. Identity and provenance

The catalog and the complete problem corpus identify the same problem number and source. The catalog ID is the string `10400124`; the complete problem ID is the integer `10400124`. Matching explicitly across these representations gives exactly one record in each corpus, with catalog rank 846.

The UTF-8 statement hash is `f7cf3043e312b046a890c1d6aac0262d9b1682f2e3a55c59eaa0f01fd7a8b8ca`. The complete review-pair hash is `4c0437f83e25796ad7bad90a5ca0a3e3ec1459caf845d4a254cd1e712947b393`. The latter was recomputed from the full problem record and its full associated report using default `json.dumps`, with `sort_keys=True`, followed by UTF-8 encoding. It was not computed from a hand-selected projection, compact serialization, or only the review text. The stored author pair equals that complete pair.

Full corpus byte counts and hashes are recorded in the verification metadata; corpus contents are excluded. The author reports a blocked live problem-page retrieval. This audit does not substitute search snippets for a verified live problem statement.

## 2. Source formula, conventions, and all levels

Jeffrey's Theorem 3.4 on printed page 577 was checked visually against the PDF, not inferred from its OCR. The author's prefactor, Dedekind-sum arguments, signed factor, quadratic term, and linear term agree with the scan. In the author's notation the exact expression is

Z = (-i/sqrt(2rp)) exp(2 pi i 12s(q,p)/(4r))
    sum over epsilon = +/-1 of epsilon exp(2 pi i epsilon/(2rp))
    sum over n mod p of exp(2 pi i (qr n^2 + n(q+epsilon))/p).

The source uses coprime p,q with 0 < |q| < p; q=2,p=25 meets this directly. General-family q can be represented modulo p within this range. The beginning of Section 3 expressly separates the general-level formula from its later coprime-level specialization. Thus applying Theorem 3.4 when 5 divides r is legitimate. All integers r=k+2 >= 2 are retained.

The source's phase labeling is q-star m^2/p in equation (5.3), printed page 588. For q=2 and p=25, q-star=13 and m=2n is a bijection modulo 25 satisfying 13(2n)^2 = 2n^2 modulo 25. There is no interchange of p and q, no missing inverse, and no mixture of lens-space orientation conventions.

The common prefactor in the canonical framing, apart from r^(-1/2), is an analytic unit in 1/r. A fixed change of two-framing multiplies by a fixed integer power of exp(2 pi i(3-6/r)/24), also a nonzero constant times an analytic unit. It cannot create an absent sector, alter a nonzero leading power, or introduce a new oscillatory factor linear in r. Orientation reversal conjugates phases and leaves the zero phase fixed.

Source: [Jeffrey (1992)](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/jeffrey.pdf), pp. 566, 574, 577, 588.

## 3. Exact cancellation, not only leading cancellation

For p=25,q=2, the congruence 2n^2=0 modulo 25 has precisely n=0,5,10,15,20. At this phase the quadratic exponential is exactly 1 for every integral r. For either sign, the remaining sum is

sum over a=0,...,4 of exp(2 pi i(2+epsilon)a/5).

The exponents 1 and 3 both permute the residues modulo 5. Each signed inner sum therefore vanishes separately. The factors depending on epsilon and 1/r multiply an exact zero before any Taylor expansion is taken. All orders consequently vanish; this conclusion does not follow merely from the cancellation of leading stationary-phase terms.

An independent integer-polynomial check reduced both coefficient polynomials modulo Phi_25(x)=1+x^5+x^10+x^15+x^20 and obtained zero remainders. This is an exact diagnostic, with no floating-point tolerance.

The ten nonzero phase numerators are 2,3,7,8,12,13,17,18,22,23 modulo 25. Each arises from one pair n,-n with n a unit. Its leading coefficient inside the signed sum is

2 cos(6 pi n/25) - 2 cos(2 pi n/25)
= -4 sin(4 pi n/25) sin(2 pi n/25),

which is nonzero because 25 cannot divide 2n or n for a unit n. Exact polynomial remainders independently confirm all ten. The invariant is therefore not the zero sequence, even though the zero-phase series vanishes. Cancellation between different phases may still occur on particular level subsequences.

As an additional check, the two complete signed Gauss coefficients vanish on all residues r=0,5,10,15,20 modulo 25. For such r, shifting n by 5 multiplies each summand by exp(2 pi i(q+epsilon)/5), a nontrivial fifth root, while leaving its quadratic part unchanged. Hence the full invariant vanishes on those levels. This is consistent with, and does not weaken, the all-level phasewise assertion.

For prime ell >= 5, p=ell^2, q nonzero and different from +/-1 modulo ell, the zero indices are precisely n=ell a. The same proof gives two zero sums of all ell-th roots of unity. The infinite-family proof is algebraic; finite checks of 284 admissible q-classes over 13 primes from 5 through 47 were only supplemental diagnostics. The excluded q=+/-1 controls correctly leave one nonvanishing signed sum.

## 4. Why regrouping cannot restore the missing phase

All classical phases in the example have denominator 25. Suppose two finite-sector asymptotic expansions with rational leading powers and integer-step corrections represent the sequence at all integral levels. Subtract the expansions, choose the largest remaining power alpha, and take sufficiently deep truncations that both error bounds are o(r^alpha).

For each residue a modulo 25, divide by r^alpha and let r=25j+a tend to infinity. The resulting equations are the discrete Fourier transform of the coefficients at power alpha, with zeros at unused frequencies. The 25-character Fourier matrix is invertible, so every coefficient at that power vanishes. Finitely many integer-step ladders of rational powers form a discrete set bounded above; induction then removes every coefficient at every fixed order.

Thus a nonzero zero-phase amplitude cannot be inserted into the exact expansion and hidden among the other phases. The use of all 25 residues is essential. A restriction to levels prime to 25 would not supply these 25 Fourier equations and must not be silently substituted for the original all-level statement.

## 5. Twisted cohomology and the generic maximum

The lens-space calculation uses H1 of the adjoint local system, not an assumption that the manifold is aspherical. For a connected manifold with simply connected universal cover, its degree-one local-system cohomology agrees with group cohomology; higher homotopy does not affect this identification.

For the cyclic group, T^25=1. Over characteristic zero, V=su(2) splits into the T-fixed subspace and its complementary eigenspaces. The norm N=1+T+...+T^24 is 25 on the fixed part and zero on the complement, while T-1 is invertible on the complement. Hence ker N=im(T-1), proving h1=0.

The zero-phase conjugacy classes have representatives m=0,5,10. Their invariant dimensions h0 are 3,1,1, respectively. The resulting h1-h0 values are -3,-1,-1. Since this character space is finite, each point is Zariski open as well as closed; one can also separate its distinct trace values polynomially. The generic maximum is -1, so the predicted half-value is -1/2. The missing analytic sector has no nonzero leading exponent with that value or any other finite value.

This finite-fiber argument does not license maximizing over special points of a positive-dimensional singular fiber. The original source uses the generic maximum and explicitly warns that a special-point maximum fails for a torus mapping-torus example. The author preserves this distinction.

Source: [Ohtsuki, Section 7.2](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf), pp. 478-479.

## 6. Connected sums, including reducible loci

For g>=1, a crossed homomorphism from the free group F_g to the adjoint module is determined by arbitrary values on the g generators, so Z1 has dimension 3g. The coboundary map has kernel H0 and rank 3-h0. Therefore h1=3g-3+h0 and h1-h0=3(g-1) for every representation. No smoothness, irreducibility, or generic-stratum restriction is being used. For g=0, the trivial representation on S3 gives h1=0,h0=3 separately.

In particular, for g=1 both central and noncentral representations have h1=h0. For g>=2, central, reducible noncentral, and irreducible holonomies have h0 equal to 3,1,0 respectively, with compensating changes in h1. This verifies that no reducible locus was dropped.

The author's connectedness argument for the Chern-Simons value is sound. A second justification avoids any concern about choosing paths through singular quotient strata: every representation extends over the four-dimensional 1-handlebody with boundary #^g(S1 x S2). Its associated flat SU(2) connection extends there. The Chern-Weil integral of its curvature is zero, so the boundary Chern-Simons value is zero modulo integers.

In the stated TQFT normalization, S11=sqrt(2/r) sin(pi/r), Z(S1 x S2)=1, and gluing along the one-dimensional S2 state space gives Z(M#N)=Z(M)Z(N)/Z(S3). It follows exactly that

Z(#^g(S1 x S2)) = (pi sqrt(2))^(1-g) r^(3(g-1)/2)
                  (sin(pi/r)/(pi/r))^(1-g).

For each fixed g>=0, the last factor is analytic near 1/r=0, has constant term 1, and is even in 1/r. Thus the sole sector has a genuine nonzero leading power 3(g-1)/2 and a full expansion. Dividing by Z(S3) would add 3/2 to that exponent; the author correctly warns against mixing the two normalizations.

## 7. Logical target and existing literature

The implication in Conjecture 7.9 and the existence/nonzero-amplitude requirement in Conjecture 7.7 must remain distinct. In the lens-space example the latter strict hypothesis fails. Assigning a formal exponent to a zero coefficient can retain a formula by convention but does not produce an exponent observable from the invariant. The package is careful on both points.

The componentwise lemma is correct under its explicit assumptions: at the largest component exponent a, the grouped coefficient is the sum of leading coefficients of components with exponent a. The grouped exponent remains a exactly when that sum is nonzero. This lemma proves neither a general stationary-phase theorem at singular strata nor general noncancellation.

The literature descriptions were checked at the cited theorem scope:

- [Andersen, arXiv:1104.5576v1](https://arxiv.org/abs/1104.5576v1), Theorems 1.1-1.2, establishes finite-order mapping-torus results in the stated gauge-theoretic construction. The introduction separates that construction from its identification with combinatorial WRT theory.
- [Andersen-Jorgensen, arXiv:1206.2552v2](https://arxiv.org/abs/1206.2552v2), Theorem 3.3.2, proves the SU(2) growth formula for the studied trace-two family. Theorem 3.4.2 gives all-torus-bundle AEC formulas. Those are not interchangeable theorem scopes.
- [Andersen et al., arXiv:2510.10678v1](https://arxiv.org/abs/2510.10678v1), Theorem 1.1 and equation (1.10), gives a Seifert integral-homology-sphere AEC and a degree upper bound. It does not establish the general topological equality. Its S3-normalized invariant requires the 3/2 exponent adjustment above.

The public arXiv records still identify these cited versions. A small independent repository search returned no relevant earlier attempt for the checked problem-ID and phrase queries. This is bounded evidence, not coverage of every branch, past commit, paper, or formulation. The package makes no novelty claim.

## 8. Inventory and adversarial diagnostics

The author archive is data-only: checks.json, proof.md, source_metadata.json, status.md. Every ZIP member is a regular, non-executable UTF-8 file, and every byte count and SHA-256 equals the external manifest. No archive code was imported or executed.

An audit-owned validation utility read the archive as data under Python -I -S. Its output was byte-identical under normal execution, -O, a relocated utility and input, a hostile working directory/PYTHONPATH containing shadow modules, and that hostile setup combined with -O. The utility uses explicit checks rather than assertions. It is not part of the accepted author package or the distributable audit bundle.

Ten negative controls were rejected: extra executable-language payload, duplicate member, missing member, traversal name, symlink mode, executable mode, changed content, oversized member, trailing archive bytes, and changed archive identity. These are integrity diagnostics, not a formal proof checker or sandbox certification. Since the mathematical deliverable contains no runner, runner-specific execution guarantees are not claimed for it.

The separate public audit bundle contains only this authored report, an acceptance record, diagnostic results, and public-source/integrity metadata. It contains no source PDFs, scans, extracted source prose, corpus entries, private sources, or coordination material.

## Final disposition

Accept the original immutable author package without a correction patch, solely under its stated partial-result scope. Preserve the missing-sector/conditional-conjecture distinction in every summary or later publication. The general conjecture is not resolved by this package.
