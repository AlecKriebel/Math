# Independent review of the matrix complete-intersection criterion

**Target:** UnsolvedMath 30002867, OWR-13678-008 (Shekhtman, Problem 2).  
**Review date:** 30 September 2026.  
**Reviewer model:** gpt-6-astra, xhigh.  
**Reviewed artifact:** `CANDIDATE.md`, SHA-256 `1a52d5d0fb983266d723416586cbcb709042691390fbbe77d6b608c0d1e9ffde`.

## Verdict

**PASS on mathematical correctness and coverage of the stated nonzero finite-dimensional target.** I found no substantive gap in the Koszul-rank characterization or in the stronger minimum-generator formula. The crucial global step uses an established stable-range theorem with hypotheses satisfied here. It does not use the discredited broad 2016 claims about Murthy's conjecture.

**Novelty and first-resolution status remain unverified.** This is a short application of classical homological algebra and classical efficient generation. Correctness of the explicit criterion does not establish that its formulation is new, that the source problem remained open, or that it merits a new-result claim.

The 1978 theorem was independently checked through its exact restatement in a later primary research paper, not through a newly obtained copy of the original 1978 proof. This bibliographic limitation is disclosed below; it is not an identified mathematical gap.

## 1. Original scope

The requested [UnsolvedMath page](https://www.unsolvedmath.com/problems/30002867) was tried first and was inaccessible through the web reader. I then checked the complete Shekhtman contribution in the [official Oberwolfach report](https://ems.press/content/serial-article-files/46567), pp. 1182–1184.

- The discussion restricts ideal projectors to finite-dimensional range
- Equation (1) is coordinate multiplication on the quotient by the kernel
- Definition 5 uses global generation of a zero-dimensional ideal by exactly the number of variables
- Problem 2 asks for the associated matrix characterization
- The nearby Hermite-approximation conjecture and absence of roots at infinity are separate statements

Thus the candidate has not replaced the requested global affine condition by the weaker local condition or by a stricter homogeneous/projective one. The proper positive-colength convention is explicit. If the zero projector is included under a nonstandard interpretation, its unit ideal needs a separately stated trivial convention; it is not covered by the displayed formula with an empty spectrum.

## 2. Algebraic audit

### Support and rank of the first differential

For the regular quotient representation, the cokernel of the row of shifted multiplication maps is the quotient of the finite algebra by the corresponding coordinate maximal ideal. Over the specified field \(\mathbb C\), this quotient is one-dimensional exactly at a support point and zero otherwise. Hence the claimed support test and rank \(N-1\) are correct, including nonreduced and multiple-support algebras.

### First Koszul homology

The shifted coordinates form a regular sequence in the ambient polynomial ring. Their Koszul complex resolves the residue field at the support point. Tensoring with the quotient algebra therefore computes the required Tor group. The proposed signs in the second differential satisfy \(D_1D_2=0\).

The long exact sequence of Tor identifies this first homology with \(I/\mathfrak m I\), because the map from \(I\otimes R/\mathfrak m\) to \(R/\mathfrak m\) is zero when \(I\subseteq\mathfrak m\). Localizing does not change this residue-vector-space quotient. Nakayama then gives the local minimal number of equations. Taking the dimension of the kernel of \(D_1\), subtracting the rank of \(D_2\), yields exactly

\[
\mu(I_{\mathfrak m})=(d-1)N+1-\operatorname{rank}D_2(\lambda).
\]

The use of the total length \(N\), not the length of one local factor, is correct. The other support factors contribute exact Koszul summands, whose ranks cancel in the homology calculation.

### Local complete intersections

At each support point the ambient local ring is regular of dimension \(d\), and the localized ideal is maximal-ideal-primary. The height theorem gives a lower bound of \(d\) generators. Equality means that a generating list is a system of parameters in a Cohen–Macaulay regular local ring, hence a regular sequence. This is exactly the stated local rank threshold.

### The global step

For \(Q=I/I^2\), the decomposition of the finite quotient algebra into its Artinian local factors makes its global generator number the maximum of the local generator numbers: combine padded local generating lists componentwise. The identity \(I^2\subseteq\mathfrak m I\) makes those residue dimensions equal to the local counts already computed.

The remaining equality between the generator numbers of \(I\) and its conormal module is **not** a consequence of Nakayama alone. The candidate correctly invokes efficient generation. With \(r=\mu(I/I^2)\), its hypotheses here read

\[
r\ge d\ge2=\dim(R/I)+2
\]

when \(d\ge2\). The stable-range theorem therefore applies. The univariate case is handled independently by the principal-ideal property, and the empty-column matrix \(D_2\) has the stated rank zero.

No step assumes radicality, diagonalizability, freeness of the conormal module in the non-CI case, or the ability to lift a prescribed generating list.

## 3. Efficient-generation source and errata

I checked [M. K. Das, *On two conjectures of Murthy*, Theorem 1.2](https://arxiv.org/pdf/1710.04281), which expressly attributes the following result to Mohan Kumar's 1978 Theorem 5: for a polynomial ring over a field, equality of the ideal and conormal generator numbers holds when the latter is at least two more than the quotient's Krull dimension. This is exactly the statement used by the candidate, including for non-CI ideals.

The [original publisher record](https://link.springer.com/article/10.1007/BF01390276) verifies author, title, journal, volume, pages, and 1978 date. Its accessible page contains metadata rather than the full original theorem proof. The author's available preprint index did not supply this old paper. A [2024 primary research article](https://www.sciencedirect.com/science/article/pii/S002186932300577X) continues to discuss Theorem 5 as the classical bound underlying later efficient-generation results.

I also read [Fasel's 2017 erratum](https://annals.math.princeton.edu/wp-content/uploads/annals-v186-n2-p07-p.pdf). It invalidates a stronger lifting argument used in the 2016 claimed proof of Murthy's conjecture. The candidate needs neither that argument nor the ability to lift an arbitrary chosen conormal basis. The erratum does not invalidate the 1978 stable-range theorem used here.

## 4. Independent exact stress tests

I wrote `independent_checks.py` without reading or reusing the candidate author's checking code. It uses only Python's standard library and exact rational Gaussian elimination.

All **20 examples** passed, including:

- Univariate quotients of lengths 1, 2, and 5
- Seven different plane monomial staircase ideals, whose minimal generators are counted directly as the minimal excluded monomials
- Box complete intersections and square-zero maximal-ideal quotients in dimensions 2, 3, and 4
- A nonmonomial length-five Gorenstein algebra with five minimal quadratic equations in three variables
- A length-fourteen product of a non-CI local algebra, a complete-intersection local algebra, and a reduced point at three distinct support points

For the last example the ranks of \(D_2\) are 24, 26, and 26, giving local counts 5, 3, and 3 by the full-size formula. This checks the potentially troublesome contribution from support components away from the tested point.

Every example also checks \(D_1D_2=0\) and the expected acyclic ranks at a point outside the support. An intentionally noncyclic commuting tuple fails the required \(N-1\) rank property, confirming the importance of the regular-representation hypothesis. These finite checks support the algebraic audit; they do not prove the global efficient-generation theorem.

Reproduction (from this review directory):

```sh
python3 independent_checks.py
```

The full exact output is recorded in `independent_results.json`.

## 5. Recommended presentation refinements

These are clarifications, not mathematical repairs:

1. Distinguish an exact structural criterion over arbitrary complex coefficients from an executable algorithm. For an algorithm, specify an effective coefficient field or exact arithmetic/root access. With that access, one may list eigenvalues of each coordinate matrix, test their finite Cartesian product with \(D_1\), and then compute the ranks of \(D_2\); no primary decomposition is needed.
2. Preserve the proper positive-colength and regular quotient-representation hypotheses prominently.
3. Keep novelty explicitly unresolved. The [Kreuzer–Long–Robbiano paper](https://arxiv.org/pdf/1903.09563) already gives zero-dimensional local complete-intersection algorithms through classical Fitting-ideal criteria. The present rank formulation is compatible with this literature; this review has not established priority for it.
4. Record 30002868 as the already-identified duplicate source extraction, without treating it as an independent discovery.

## Final disposition

The candidate is suitable to retain as a **mathematically checked characterization, with classical dependencies and unresolved novelty**. It should not be promoted to a novel independently verified research discovery merely because the finite checks and this review passed. No external contact or repository write was performed during this review.

## Follow-up check of the final additions (03:43 UTC)

The revised artifact adds the effective-coefficient-field qualification and the finite Cartesian-product spectral procedure; both are correct and resolve recommendation 1. I also independently checked both new diagnostic examples. The algebra with relations x²=y²=xz=yz=0 and z²=xy has basis 1,x,y,z,xy, one-dimensional socle, and five minimal quadratic equations; its second Koszul rank is 6. The tuple of multiplication by t,t²,t³ on C[t]/(t⁴) has rank 6 and defines an affine CI. Since 1,t,t²,t³ are all represented by degree-at-most-one polynomials, its associated graded algebra has Hilbert function (1,3), so its degree-form ideal is the homogeneous maximal ideal squared. It is not a strict CI. The main proof is unchanged. PASS verdict is retained for the refreshed hash above. The independent test suite now includes these two additions, for 20 examples total.

The final formatting-only conversion to GitHub math delimiters was checked at 03:44 UTC; the refreshed hash identifies that version.

Formatting-only hash refresh: the final candidate uses GitHub dollar-sign math delimiters. The reviewed mathematical content is unchanged. Run the reproduction command from the directory containing this review and its checking script.
