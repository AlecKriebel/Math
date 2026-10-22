# Independent mathematical and reproducibility audit

Target: **30005421 / OWR-12697690-001**. Audit date: **8 October 2026**.

## Disposition

**ACCEPT as an application of a prior published result.** The authored `PROOF_APPLICATION.md` proves the complete existence statement in the original source's setting. No mathematical correction to that file is required. The result is credited to **Markus Reineke**, with his acknowledgment of Urban Jezernik's contribution preserved. This audit is verification and clarification, not a novel theorem or a substantive new proof-search turn.

The original numerical checker has an important reproducibility limitation: its ten `assert` statements disappear under Python optimization. Its ordinary execution was independently reproduced byte-for-byte, but optimized `PASS` outputs are not mathematical checks. This audit supplies an independently written, standard-library-only checker with explicit failures, exact arithmetic, and adversarial mutation controls active in all three Python modes. The original packet and its original checker were preserved without modification.

## 1. Sources, attribution, and exact target

The original question was independently inspected in Markus Reineke's contribution *Expander representations*, printed pp.405–406 of [Oberwolfach Report 7/2023](https://ems.press/journals/owr/articles/12697690), [official report PDF](https://ems.press/content/serial-article-files/47001). Printed p.405 was also visually inspected.

The relevant published result is Theorem 2.4 of Reineke, *Expander representations of quivers*, [Forum of Mathematics, Sigma 14 (2026), e132, 1–10](https://doi.org/10.1017/fms.2026.10284). The publisher independently confirms online publication on 29 September 2026. The [author's arXiv v2](https://arxiv.org/abs/2411.15609v2), dated 6 July 2026, was cross-checked in its PDF and public HTML. All three supplied PDFs match their recorded SHA-256 digests and byte lengths. `SOURCE_AUDIT.json` records the independent checks without reproducing source text.

The exact target is: for every finite acyclic wild quiver over an algebraically closed field, there is a fixed rational slope with positive denominator, such that for each cutoff in (0,1) a positive uniform gap holds along an unbounded family. The original weak inequality permits the family to depend on the cutoff. The authored reconstruction establishes the stronger statement with one family for all cutoffs, and also supplies the journal's strict gap convention. Neither change weakens or changes the requested conclusion.

The audit concerns only the forward implication. It does not certify the published converse or statements elsewhere in the paper that are unnecessary for the target. Unboundedness here is total representation dimension: visual inspection of journal Definition 2.3 confirms that its scalar dimension threshold is distinct from the bold dimension-vector notation. Zero extension on a disconnected quiver therefore causes no growth problem.

## 2. Perron–Frobenius and rational perturbation

For a connected finite acyclic wild quiver, its symmetric Cartan matrix is indefinite, and its least eigenvalue is negative. The matrix 2I−C is nonnegative and irreducible. Perron–Frobenius and symmetry give a strictly positive eigenvector v for the simple least eigenvalue λ₁; hence λ₂>λ₁. A connected acyclic wild quiver has at least two vertices, so the second eigenvalue and nontrivial orthogonal hyperplane used here exist.

At v, the vector −Cv is strictly positive. Strict positivity persists on an open neighborhood. The maximum M(d)=max dᵢ/(−Cd)ᵢ is continuous there and equals −1/λ₁ at v. The restricted Rayleigh minimum b(d), on the unit sphere perpendicular to Cd, is also continuous. For completeness: normalized projection of a minimizer onto a nearby hyperplane proves the upper-semicontinuity inequality; compactness and a convergent subsequence of nearby minimizers prove the lower-semicontinuity inequality. The normal remains nonzero throughout this neighborhood.

At v this minimum is λ₂. Thus c(d)=1+min(b(d),0)M(d) is continuous and strictly positive near v. If λ₂≥0 its value at v is 1. If λ₂<0 its value is 1−λ₂/λ₁>0. Rational points are dense in the open positive neighborhood. Clearing denominators preserves the hyperplane, M, b, and c, because positive rescaling multiplies both d and −Cd equally. Consequently an integral d with all required properties exists, and the resulting Euler/skew linear forms have integral coefficients. Their denominator is strictly positive on every nonzero vector in the nonnegative cone.

No numerical eigenvalue approximation, unproved rational eigenvector assumption, or characteristic restriction is hidden in this step. The spectral argument takes place in the real space of dimension vectors, independently of the characteristic of the representation field.

## 3. Uniform inequality and all signs

Writing f=ηd+x with η=κ(f)/κ(d) gives w·x=0. Each coordinate lies between −ηdᵢ and (1−η)dᵢ. Expanding the nonnegative product of its distances to the two endpoints gives the square bound with the **plus** linear term (1−2η)dᵢxᵢ. Multiplication by wᵢ/dᵢ and summation annihilate that linear term. Hence the weighted square sum is at most η(1−η)B, and the ordinary square norm is at most Mη(1−η)B.

When b<0, multiplication of this norm upper bound by b reverses the inequality. The reconstruction has the correct direction. When b≥0 the zero lower bound is sufficient. Combining both cases produces the single constant c fixed before f, η, n, or any subrepresentation is considered.

The Euler/skew identity is

2E(f,d−f)=S(d,f)−A(d,f)−S(f,f).

Thus E(f,d−f)≥0 implies A(d,f)≤−cη(1−η)B. Division is by κ(f)=ηB>0, so the resulting slope gap is at least c(1−η). All signs, factors of two, orientations, and normalizations are correct.

Several compressed source displays need care. The source's weighted sum changes the sign of a linear term, but that summed term is zero; the packet derives the consistent coordinate inequality. More importantly, an arbitrary restricted Rayleigh quotient need not approach λ₂ as d approaches v. The correct claim concerns the **minimum**, as the packet explicitly states and proves. This distinction is real: the exact Cartan example in the independent checker has an integral Perron vector and two vectors perpendicular to that Perron vector with distinct negative quotients −1 and −25/33. The authored reconstruction does not inherit the false stronger inference.

## 4. Generic incidence and the countable-field issue

For each D=nd and integral 0≤e≤D, the incidence space over the product of Grassmannians is the kernel bundle imposing arrow conditions. For an arrow i→j, those conditions have codimension eᵢ(Dⱼ−eⱼ): after fixing subspaces they are exactly the components from the chosen source subspace to the target quotient. Different arrows involve independent matrix coordinates. Local Grassmannian charts show constant rank, so the bundle dimension is exactly dim R_D+E(e,D−e).

Projection of this closed incidence space to R_D has closed image because the Grassmannian factor is projective. If the Euler term is negative, its image has dimension smaller than the affine representation space and is therefore proper. Only finitely many integral e lie in the box 0≤e≤D. Irreducibility excludes their finite union from filling R_D. Its complement is a nonempty open finite-type variety over the algebraically closed field, so it has a point over that same field.

This argument works over countable algebraically closed fields, including algebraic closures of finite fields and of the rationals. There is no intersection over all cutoffs, no appeal to uncountability, and no descent or fixed-field extension claim. For each n a single representation is chosen outside **every** negative-Euler locus. No dependence on δ is introduced.

## 5. Quantifiers, strictness, and disconnected quivers

For every nonzero proper subrepresentation of that chosen representation, f=e/n satisfies the numerical assumptions. The Euler form scales by n², the slope is homogeneous of degree zero, and the cutoff ratio is unchanged. Positivity of all denominator coefficients guarantees 0<η<1 for a proper nonzero subrepresentation, even when e has zero coordinates.

For a fixed cutoff δ<1, the gap is at least c(1−δ). Choosing ε=c(1−δ)/2 makes it strictly larger than ε, which resolves the published strict/weak endpoint discrepancy without claiming an attained maximum under a strict inequality. The positive constant is uniform in n. Dimensions equal n times a positive fixed total dimension and tend to infinity. Stability follows directly because every proper nonzero subrepresentation has η<1; no additional theorem about Schurian representations is necessary.

A finite acyclic wild quiver has a wild connected component. Extending the constructed representations by zero leaves every subrepresentation supported on that component. Extending the numerator by zero and the denominator by positive integer coefficients elsewhere preserves rationality and positivity on the full cone. Slopes, cutoff ratios, and total-dimension growth of the family are unchanged. This handles disconnected quivers without erroneously extending κ by zero.

The proof therefore has no remaining bridge for the stated target. It makes no claim for a prescribed arbitrary slope, oriented cycles, non-algebraically-closed fields, explicit matrices, or a gap uniformly bounded away from zero as δ tends to 1.

## 6. Independent exact tests and adversarial controls

`independent_check.py` is independently written rather than an assert-to-exception transformation of the old checker. It uses only Python's standard library, exact integer/Fraction arithmetic, an independently implemented determinant, and exact Sylvester certificates on an explicit kernel basis. It has no `assert` nodes. It tests four cases, including unequal dimension coordinates, two cases with genuinely negative restricted Rayleigh values, and a nonconstant integral Perron eigenvector.

For each clean run it executes **323,049 explicit checks**, enumerating **16,883** dimension vectors with **1,386** eligible nonzero proper vectors and **7,919** strict-cutoff checks. There are **634** sampled vectors with negative restricted quadratic value. Exact check counts, certified principal minors, slack minima, and arithmetic witnesses appear in `INDEPENDENT_TEST_RESULTS.json`.

The clean output is byte-identical in ordinary Python, `-O`, and `-OO`. Twelve independently designed semantic mutations are each rejected with exit code 1, the expected failing check, and an exact witness in all three modes: **36 substantive rejections**.

1. Reverse the skew-form sign: Euler/skew identity fails.
2. Reverse the negative spectral correction: the numerical estimate fails.
3. Use the minimum weight ratio instead of the maximum: the norm bound fails.
4. Set ε=0: positivity fails.
5. Drop cutoff dependence from ε: a strict-gap witness fails.
6. Transpose the incidence arrow contribution: the dimension identity fails.
7. Reverse which Euler sign is excluded: a negative-Euler case is not excluded.
8. Omit n from the cutoff normalization: weighted orthogonality fails.
9. Omit n from f=e/n: Euler homogeneity fails.
10. Reverse the coordinate linear-term sign: the coordinate square inequality fails.
11. Claim all restricted Rayleigh quotients coincide: exact negative values −1 and −25/33 refute it.
12. Set the off-component denominator coefficient to zero: full-cone positivity fails.

These are finite algebraic controls, not tests of the theorem over all quivers or fields. Geometric existence, continuity, and the universal quantifier conclusions are certified by the written argument above, not by sampling. The avoidance-sign mutation checks the computational sign convention only; it is not a computer proof of nonempty generic loci.

## 7. Original-checker limitation and preservation

The original checker was replayed normally and reproduced its 1,918-byte recorded JSON exactly. Its ten assertions are enabled in that mode. Prepending a deliberate failing assertion causes normal Python to exit with failure, but both optimized modes delete it and still emit the original `PASS` JSON byte-for-byte. `ORIGINAL_CHECKER_LIMITATION.json` records all six executions and hashes.

This is an execution-mode limitation of the old supporting script, not a defect in the mathematical proof or evidence that its ordinary run was false. No optimized pass from that checker is used as audit evidence. No transformation of the old script is presented as an independent verification. All original input files were preserved, and their hashes are recorded in `INPUT_PACKET_MANIFEST.json`.

## 8. Reproduction and publication boundary

Run the independent suite with:

    python -B run_independent_suite.py

The suite launches the checker in all three Python modes and demands identical clean output plus all 36 expected mutation rejections. It uses no source files, network calls, datasets, or third-party modules and writes only to standard output. The read-only replay receipt records actual non-root file-append and directory-create denials, complete suite replay, and before/after hash equality. Read-only status is demonstrated by failed write attempts, not inferred from a mode bit alone.

The source-free packet includes authored analysis, exact checking code, results, and public bibliographic/hash/inspection metadata. It excludes third-party PDFs and extracted source text, datasets, private sources, and private coordination material. No GitHub or queue writes were performed during this audit.

**Final recommendation: retain the disposition “already solved by prior published result,” with zero substantive new proof-search turns and no novelty claim.**
