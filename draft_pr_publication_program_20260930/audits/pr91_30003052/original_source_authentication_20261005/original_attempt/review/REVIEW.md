# Independent review: spectrum of a linear-map Koopman operator

**Verdict: PASS_COMPLETE_CLASSIFICATION.** The proof establishes both spectral formulas for complex C(U), where U is the closed unit ball of an arbitrary finite-dimensional complex norm and A is a contraction in that norm. The submitted classification covers the exact OWR example, including mixed stable/peripheral and singular cases. Historical priority remains unestablished.

This is a separate adversarial AI review (gpt-6-astra, xhigh), completed on 2026-09-30, not human peer review or a novelty certificate. A requested prior-credit clarification is incorporated in the final snapshot; no mathematical repair was needed.

## Frozen material and validation

Reviewed `CLASSIFICATION.md` SHA-256:

`0abd5dd0918905b3a6c1e9c62a57097645bba6334cb625a4a4e88f2c12c4416b`.

Final submitted `verify.py` SHA-256:

`da82ae1c261411994bfd4068b50bb4bdc47c7716bc0d26864374c19dc1480be4`.

The final proof differs from the initial reviewed snapshot `3e87fdf9c2c08a8ab5d68116c29c251ab147f2f37a9f538c629159e8c16fb3cc` only by two explicit nilpotent-case attribution insertions; reversing those insertions reproduced that earlier hash. The final checker uses exact SymPy integer bases throughout.

The submitted checker passed all **473 exact assertions**, with a byte-identical replay receipt. A separate checker passed **907 exact controls**, using a different nonnormal matrix and adapted ℓ¹ norm, signed peripheral characters, fifth-root Cesàro averages, a nilpotent ideal, and radial eigenfunction/range diagnostics. No author mathematics was edited by the reviewer.

## 1. Exact primary formulation and attribution

The full [OWR 7/2016 contribution, “Pure Koopmanism”](https://ems.press/journals/owr/articles/14215), printed pp.320–322, was read; p.321 was also visually inspected. Example 4 explicitly specifies the closed ball, the induced norm bound, and all complex continuous observables. It imposes no invariant measure, holomorphy, diagonalizability, or matrix invertibility. The candidate matches these hypotheses exactly.

I also read the relevant portion of Küster's [2015 thesis](https://homepages.laas.fr/henrion/mfo16/kari-kuester.pdf), including Section 3.1 and the later discussion in 4.1.7–4.1.9. The all-peripheral formula, the interior-eigenvalue construction, the strictly stable case and the nilpotent-only point spectrum are prior results. Proposition 3.1.7 states the nilpotent case. Printed p.43 explicitly leaves the mixed reverse inclusion open; this page was visually checked. Chapter 4's special decomposition observations do not supply that mixed inclusion. These facts establish the source's historical scope, not present-day novelty.

A bounded independent search did not identify an earlier complete statement of the two formulas. That is not an exhaustive priority search. The local primary-file hashes and exact inspected sections are recorded in `source_verification.json`.

## 2. Norm-preserving peripheral reduction

Power boundedness excludes a nontrivial Jordan block at a unit-modulus eigenvalue: its polynomially growing powers contradict the uniform norm bound, independently of the choice of finite-dimensional norm. The remaining spectral summand has powers tending to zero, including nontrivial Jordan blocks strictly inside the disk.

Simultaneous recurrence of the finitely many peripheral phases produces integers tending to infinity along which every phase tends to one. This follows from the torus pigeonhole argument; if the possible return integers stay bounded, an exact common return occurs and its multiples give the required unbounded sequence. Thus a subsequence of A's powers converges in norm to the commuting spectral projection P. Since each power is contractive, P is contractive in the **original given norm**. Consequently P(U) lies inside U and equals U∩E. No Euclidean orthogonality or unjustified projection of the ball is assumed.

The same recurrent subsequence, shifted by one, gives B⁻¹ as a limit of contractive nonnegative powers of B on E. Hence both B and B⁻¹ are contractive and B is an isometry of E mapping V=U∩E onto itself. When E={0}, V is one point; its continuous-function space is still the nonzero one-dimensional space of constants.

## 3. Every unimodular eigenfunction factors through P

For a Koopman eigenfunction f with multiplier ζ of modulus one, iteration at both x and Px is legitimate because P(U)⊆U. It yields

`|f(x)−f(Px)|=|f(Aⁿx)−f(AⁿPx)|`.

The two arguments approach one another uniformly on U, because their difference is the stable power applied to (I−P)x. Both arguments remain in the same compact ball. Uniform continuity therefore forces f=f∘P, including boundary points and points with nonzero stable component. This proves the reverse inclusion missing from the mixed source case, rather than merely constructing some peripheral eigenfunctions.

Conversely, pullback through P preserves a B-eigenfunction and its eigenvalue, using PA=AP and A|E=B. It preserves nonzeroness because P is onto V. The peripheral eigenvalues of the full Koopman operator are therefore exactly those of the reversible-ball operator.

## 4. Reversible-ball eigenvalues and full spectrum

Diagonal coordinates for B exist by peripheral semisimplicity. For each integer character of its eigenvalues, nonnegative powers of coordinates and their complex conjugates give an eigenfunction. Negative character exponents are supplied by conjugates because the matrix eigenvalues are unimodular. Each such monomial is nonzero on V: V contains a neighborhood of zero in E, which a finite union of coordinate hyperplanes cannot cover. This realizes every element of Γ, including 1.

The coordinate-conjugate polynomial algebra is unital, conjugation-closed and point-separating on V. Complex Stone–Weierstrass therefore gives uniform density on this actual compact ball, without changing observable spaces or invoking an unverified measure model.

For ζ outside Γ, the twisted Cesàro means have norm at most one. They tend to zero on each monomial by the elementary geometric-sum formula and thus on each finite polynomial. If f were a ζ-eigenfunction, every mean would fix f. Uniform polynomial approximation and the common norm bound force f=0. Crucially, this argument excludes ζ even when it is a limit of Γ; it does not confuse the group with its closure.

Since the reversible Koopman operator and its inverse both have norm one, its full spectrum lies on the circle. It contains the closure of Γ. An infinite subgroup of the circle is dense, giving the entire circle in that case. If Γ has finite order q, B^q=I and thus K_B^q=I; spectral mapping places the full spectrum among the qth roots, all already realized as eigenvalues. The one-point case gives {1}. Hence the point spectrum is Γ and the full spectrum is its closure, exactly as claimed.

## 5. Stable nonzero eigenvalue: every point in the open disk

For any nonzero stable eigenvalue α, a nonzero **left** complex-linear eigenfunctional exists whether or not its Jordan block is semisimple. Its norm maximum R on U is attained, finite, and positive because U is compact and contains a neighborhood of zero. Writing r=|α| gives |ℓ(Ax)|=r|ℓ(x)|.

For 0<|μ|<1, the chosen complex exponent z has r^z=μ and positive real part. The definition uses only the real logarithm of |ℓ(x)|/R. Its modulus is (|ℓ(x)|/R)^(Re z), which tends to zero at every point of ker ℓ, so oscillation from the imaginary part causes no continuity problem there. The scaling identity holds both on and off that hyperplane. The function is nonzero, indeed equal to one at a point where |ℓ|=R.

Zero is treated separately and correctly: `( |ℓ(x)|/R−r )_+` is a nonzero continuous function vanishing on A(U). Thus zero is a Koopman eigenvalue even when A is an invertible matrix. The argument does not confuse matrix invertibility with surjectivity of A on its closed unit ball.

All open-disk points are now eigenvalues; no eigenvalue can lie outside the closed disk because the Koopman norm is one. The peripheral factorization excludes any further boundary eigenvalues. Finally, spectral closedness supplies the entire closed disk as the full spectrum. This does not claim every boundary point is an eigenvalue.

## 6. Zero plus peripheral matrix eigenvalues: no hidden disk

When there are no nonzero stable eigenvalues, the stable matrix restriction is nilpotent. The bounded operator Qf=f∘P is an idempotent commuting with K_A. Its range is isometrically C(V), because P maps U onto V. Its kernel is exactly the closed ideal of functions vanishing on V.

If N^d=0, then A^d(U)⊆V, so K_A^d vanishes on ker Q for **all continuous functions**, not merely polynomials. This is the decisive stronger statement distinguishing a nilpotent matrix part from a stable nonzero part. When the stable summand is present, ker Q is nonzero, as witnessed by a linear functional annihilating E. A nilpotent operator on a nonzero vector space has nontrivial kernel and no nonzero spectral value. If the stable summand is absent, ker Q={0} and contributes no zero eigenvalue.

The finite topological direct sum of the two invariant closed spaces makes the resolvent block diagonal; it exists precisely when both block resolvents exist. Eigenvectors obey the corresponding blockwise equations. Thus both full spectrum and point spectrum are the stated unions. In this case the stable summand is nonzero exactly when zero is a matrix eigenvalue. The formulas cover A=0, arbitrary nilpotent matrices, the identity, finite-order and irrational peripheral rotations, and every peripheral/nilpotent mixture.

## 7. Boundary cases and reproducibility

No positive-dimensional peripheral space, nonempty J, nonzero stable eigenvalue, or invertibility hypothesis is silently imposed. The convention Γ={1} for empty peripheral set is necessary and correct. The conclusion concerns spectral **sets** only; it does not classify eigenspace multiplicities, smooth or holomorphic eigenfunctions, generalized eigenvectors, or observable spaces on an open ball. Changing the norm is not used to modify the source domain.

From this review directory:

```sh
python independent_checks.py
python author_replay/verify.py > author_replay/replayed_verification.json
cmp author_replay/verification.json author_replay/replayed_verification.json
```

Both scripts require SymPy. The computations support the finite algebra but do not infer an infinite-dimensional spectrum from a truncated matrix. Recurrence, compactness, uniform continuity, polynomial density, the nilpotent ideal, and the full resolvent argument were checked analytically above.

The exact source question is answered by the complete candidate proof. Recommended campaign disposition: **claimed_solved, 1/5**, subject to the usual unrefereed/AI-reviewed status and unestablished historical priority. Preserve all attribution to Küster's earlier cases. No further mathematical correction is required for this snapshot.
