# Focused acceptance: source correction and boundary-transgression approach

Problem 30004711. Independently checked 7 October 2026.

## Pinned artifacts and outcome

- Frozen source-scoped report: `fe38b9dac323407637721620afbad4e31eaca28ab373dd9b6f557a6810eaa506`. Its bytes remain unchanged.
- CORRECTIVE_ADDENDUM.md: `85fcfeace146127e2261e1060078e55d6304ddbefbc9d69317f9b5a3bdafc3cb`.
- AUTHOR_APPROACH_1_BOUNDARY_TRANSGRESSION.md: `46e5dae728acc840bdfda1be780ec1d188a06e15251b663b461ea0ba47c2bdd1`.

**Accept the correction and the mathematical approach at these hashes, with the scope limits below.** The earlier version of Approach 1 needed an explicit dimension restriction for its factorial formula; this has been corrected to d>=r>=1, and the all-NS formula is restricted to g>=1. Stable genus zero is separately disposed of by degree.

This acceptance certifies a transgression identity and an explicit counterexample to an unrestricted invariance lemma. It does not certify a counterexample to the original OWR problem, a value of its actual torsion boundary residue, or a solved-as-written classification.

## 1. Source-correction check

The addendum correctly distinguishes the original OWR display from the explicit Stanford-Witten torsion normalization. The latter is present in [1907.03363v5](https://arxiv.org/abs/1907.03363v5), Appendix A.3, (A.18), printed p.113 / PDF p.114. Its spin weighting and torus conventions cannot be transplanted into the canonical oriented stack calculation without comparison.

I reread Appendix A.2, printed p.111 / PDF p.112, including (A.9)-(A.11). It chooses an arbitrary SO(m) connection after invoking exact-deformation invariance. Its subsequent fixed-connection local integration formula is logically separate from the noncompact invariance step being tested.

I also reread [2608.25237v2](https://arxiv.org/abs/2608.25237v2), pp.27-29. Section 4.1.3 proposes a hyperbolic harmonic-projection construction. Exercise 7 on p.28 asks for its comparison with the holomorphic Euler construction; the boundary analogue is described on p.29. The addendum appropriately does not identify this harmonic connection with an actual torsion-induced connection. Exactness of the characteristic forms, once they are well-defined connections on the same oriented bundle, is not itself a proof that their improper total integrals agree.

The other corrections (Remark 3.20 locator, dual distinction, Pfaffian normalization/invariance) accurately describe the source-scoped convention risks already found in the independent audit.

## 2. Chern-Simons formula and degree

For a real oriented rank-2r bundle with a fixed fiber metric and invariant polarized Pfaffian P normalized by P(X,...,X)=Pf(X), the form

CS_e = r/(2 pi)^r integral_0^1 P(a,F_t,...,F_t) dt

has degree 1+2(r-1)=2r-1. The curvature derivative is d_(A_t)a; invariance and Bianchi give d CS_e=e(A_1)-e(A_0), using the artifact's consistent curvature/orientation convention. Multiplying by the closed form omega^(d-r)/(d-r)! gives degree 2d-1 on the boundary and degree 2d after differentiation. The Stokes identity therefore has exactly the correct degrees and coefficient.

The same argument applies to orbifolds with their ordinary finite-stabilizer integration weights. For the NS ranks, d-r=g-1. No factorial expression is used when r>d.

The artifact correctly conditions its application on a prior identification of both actual connections on the same oriented bundle. Here “metric connections” is read relative to one fixed fiber metric, so their affine interpolation is an SO connection. If the initial metrics differ, their orthonormal reductions must first be identified. The artifact does not derive the needed connection identification from notation alone.

## 3. The explicit cylinder example

For q(t)=exp(2t)/(1+exp(2t)), q'(t)>0, q(-infinity)=0, and q(+infinity)=1. Thus omega=q'(t)dt wedge dtheta is symplectic on R times S^1 and has total area 2 pi.

The connection A_s=scq(t)Jdtheta is globally defined on the trivial rank-two bundle: dtheta is a global circle one-form, and J is a fixed element of so(2). Its metric compatibility is immediate. Since so(2) is abelian, its curvature is scq'(t)Jdt wedge dtheta. With Pf(J)=1,

e(A_s)=scq'(t)dt wedge dtheta/(2 pi).

Its integral is sc and the integral of its absolute coefficient is |sc|. It is globally exact. On [-R,R] times S^1, the boundary integral is

sc(q(R)-q(-R))=sc(exp(2R)-1)/(exp(2R)+1),

which tends to sc. Therefore the example has finite Euler integrals, fixed bundle/metric/orientation, and nonzero arbitrary boundary transgression. The formula does not require c to be integral because no extension of these arbitrary connections across the ends is asserted.

This directly verifies the general obstruction. It is not evidence that the actual moduli-space residue is nonzero.

## 4. Fixed-retraction split-supermanifold interpretation

On Pi F with dimension 2|2, the connection expression (A.10) gives a globally defined lambda_(A_s), so Omega_s=pi^*omega+d lambda_(A_s) is closed. Its reduced even block is omega and its reduced odd block is the fixed negative Euclidean metric. Both are invertible everywhere, which makes the full supermatrix invertible by a finite nilpotent inverse expansion. Uniform nondegeneracy at infinity is not needed for this pointwise assertion and is not claimed.

All Omega_s have the same body restriction and differ by exact forms. With the same split retraction and a consistent Berezin orientation, the fixed-connection Gaussian/Berezin calculation in (A.14)-(A.17) gives the normalized volume integral integral e(A_s)exp(omega). In body dimension two, only e(A_s) contributes, hence Vol_s=sc. Its top Berezin coefficient is absolutely integrable.

The artifact correctly limits the example to fixed-retraction integration. It does not assume unrestricted noncompact retraction independence, nor pretend that the connections are all Chern connections for a single fixed holomorphic structure.

## 5. Conditional genus-one consequence

If a fully verified convention/connection comparison gives V_tau=epsilon W+B_tau with W=1/16 and epsilon=+1 or -1, then V_tau=1/8 requires

B_tau=1/8-epsilon/16.

The two values 1/16 and 3/16 are correct. A proof of B_tau=0 in those conventions would instead refute that strengthened coefficient-one statement. The authored approach proves neither actual value; it identifies the residual calculation required.

## Limits of acceptance

- The normalized canonical identity remains a cited prior theorem.
- The authored example invalidates a proposed unrestricted noncompact invariance principle; it does not invalidate a version with suitable boundary assumptions.
- The explicit model is neither the spin moduli space nor its torsion connection.
- No actual OWR convention map or cusp asymptotics have been certified.
- Counting this as a targeted mathematical approach does not turn it into a new theorem about the original problem or a final unsuccessful outcome.
- No publication was performed by this audit.
