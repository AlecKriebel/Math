# Independent audit: lifting, integral logarithms, finite count, and Lazard

**Checkpoint:** 2026-09-15T04:26:41Z.  
**Scoped audit completion estimate:** 100%.  
**Source examined:** `/Users/alec/Downloads/kourovka_16_63/report/kourovka_16_63.tex`.  
**Method:** independent derivation of the analytic and lattice arguments, including all precision losses, plus inspection of a primary source for the correspondence. Attached instructions were not treated as authorization. No external communication, commit, or push was performed.

## Verdict and scope

I found no gap in Lemmas `lift`, `logexp`, `tensor`, Proposition `full-count`, the conversion of the claimed Smith invariants into the count, or Lemma `class` and the application of Lazard. These conclusions are conditional on the independently auditable inputs from earlier sections: the integral Lie structure, generation of B by x,y, trivial full and infinitesimal flag stabilizers, and the stated Smith invariants. This report does **not** certify that those inputs or their computational implementations are correct; they are separate audit assignments.

In particular, the argument actually counts the full automorphism group once those inputs hold. It does not silently restrict to inner automorphisms or a chosen congruence subgroup: the lifting lemma forces every finite automorphism into the analytic domain before logarithms are used.

## 1. Lifting argument, rederived

Write E = End(A), E0 = End(B), with p²B ⊆ A ⊆ B. All maps on A extend uniquely to the common rational vector space. An automorphism of the additive group A/p^iA is automatically Z/p^i-linear and lifts to Q in GL(A), because an integral lift of an invertible matrix modulo p has unit determinant. Thus there is no extra linearity hypothesis on finite Lie-ring automorphisms.

The scaled bracket is ν = p²μ. Its bracket-preservation congruence yields

    E_Q(A,A) ⊆ p^(i−2) A,
    E_Q(u,v) = Qμ(u,v) − μ(Qu,Qv).

Applying this to p²u,p²v, with u,v in B, and dividing by p⁴ gives

    E_Q(B,B) ⊆ p^(i−6) A ⊆ p^(i−6) B.

This calculation does not assume beforehand that Q preserves B. Bilinearity on the rational vector space suffices.

For i ≥ 6, Qx,Qy lie in A ⊆ B. If Q sends two Lie words into B, the displayed error identity shows it sends their bracket into B. Induction therefore sends every Lie word in x,y into B. The input generation lemma says finitely many such words span B over Z_p, so Q(B) ⊆ B. Its determinant is a unit in either basis, hence Q(B)=B. For i ≥ 7 the error is zero modulo p, giving a genuine automorphism of B/pB.

Preservation of both lattices forces preservation of the plane (A+pB)/pB and of ((p^−1A∩B)+pB)/pB. With weights 0,0,1,2,…,2 these are exactly the asserted flag. Triviality of its full stabilizer gives Q−I in pE0; Q−I also lies in E. Hence Q belongs to 1+J.

For a derivation congruence the same argument uses

    Dμ(u,v) = μ(Du,v) + μ(u,Dv) + δμ(D)(u,v).

The word induction is valid without assuming D preserves B. The reduced derivation preserves both flag spaces, and the infinitesimal stabilizer input forces D in J. The proof therefore applies to arbitrary representatives, not only carefully selected ones.

## 2. Integral logarithm and exponential

From the lattice inclusions,

    p²E0 ⊆ E ⊆ p^−2E0.

For X in J, multiplication shows X^r belongs both to E and to p^rE0; consequently it lies in p^(r−2)E. At degrees r<p, the denominators r! and r are units. At r≥p=1009, both valuations are at most r/1008, so

    r − 2 − v_p(r!) > 0,
    r − 2 − v_p(r) > 0.

These bounds tend to infinity. The series converge in E, and their nonconstant terms lie in pE0. Formal inverse identities are legitimate in the complete rational matrix algebra, so exp and log are inverse maps between J and 1+J. The geometric inverse of I+X also preserves A because its powers converge in E.

### Precision, including noncommuting matrices

Suppose X−Y belongs to p^iE. Each telescoping term

    X^a (X−Y) Y^b,  a+b=r−1,

lies in p^iE by multiplicative closure. Since X,Y belong to pE0 and E ⊆ p^−2E0, it also lies in

    p^(i+r−3)E0 ⊆ p^(i+r−5)E.

For r<p no division loses precision. For r≥1009,

    r−5 > r/1008 ≥ max(v_p(r!), v_p(r)),

so divided terms still belong to p^iE. The proof works for arbitrary noncommuting matrices, since telescoping powers does not use commutativity. The same estimate handles logarithms of I+X and I+Y.

Finally p^iE ⊆ J when i≥3. Thus the two series give well-defined inverse bijections on the relevant congruence classes. No hidden reduction in i is needed.

## 3. Tensor argument and exact equivalence

Let T = Hom(Λ²A,A), T0 = Hom(Λ²B,B). A tensor preserving A can lose at most four powers on its two B inputs; a factor p² suffices for a B-integral tensor to land in A. Hence

    p²T0 ⊆ T ⊆ p^−4T0.

It follows by applying endomorphisms to these lattices that

    p⁶End(T0) ⊆ End(T) ⊆ p^−6End(T0).

For D in J its differential action X is integral on T and divisible by p on T0. Thus X^r belongs to p^(r−6)End(T) when r≥6, and X^7 is zero modulo p on T.

The output action and two input actions commute with each other on the rational tensor space. Their exponential therefore equals the natural tensor action of exp(D). In particular, with Q=exp(D),

    ρ_T(Q)−I = exp(X)−I = X U(X),
    U(X) = Σ_(r≥0) X^r/(r+1)!.

For r<p−1 the denominators are units. For r≥p−1=1008,

    r−6−v_p((r+1)!) ≥ r−6−(r+1)/1008 > 0.

Consequently U(X) is integral on T. Modulo p, only terms r≤6 survive; this is a polynomial in the nilpotent operator X with constant coefficient 1. It is therefore invertible modulo p and over Z_p. It commutes with X. Hence

    (ρ_T(Q)−I)ν ∈ p^iT  ⇔  Xν ∈ p^iT.

For completeness, the usual bracket error and this tensor error differ only by precomposition on both inputs with Q^−1, an integral invertible transformation of T. Thus they define exactly the same bracket-preservation congruence. The argument preserves the full p^i precision.

## 4. Full count, conditional on the Smith data

For i≥7 every finite automorphism has a representative in 1+J and every derivation solution has a representative in J, by Section 1. Sections 2–3 then produce mutually inverse maps on all finite classes satisfying the respective equations. This proves the asserted full-set bijection, not merely a subgroup inclusion.

For an integral matrix of rank 931 on 961 columns with 30 zero invariants and nonzero valuations

    0 × 87, 1 × 55, 2 × 758, 3 × 6, 4 × 25,

the kernel modulo p^i has order p^(30i+1689) for i>4. This follows coordinate by coordinate from the Smith normal form; a nonzero diagonal entry p^v has exactly p^v solutions to p^v z=0 modulo p^i. The multiplicities sum to 931 and their weighted sum is 55+1516+18+100=1689.

The manuscript's strategy for excluding invariants hidden beyond computation precision is logically sound: 931 verified pivots give rank at least 931, while 30 independent rational inner derivations give rank at most 931. Therefore no further nonzero invariant can exist at a larger valuation. This statement does not replace checking the implementation or those 30 independent vectors.

## 5. Nilpotence and correspondence

The quotient L/p^1689L has exactly p^(31·1689)=p^52359 elements. Since L ⊆ p²B and B is a Lie lattice, induction gives γ_m(L) ⊆ p^(2m)B. Also

    p^1689L = p^1691A ⊇ p^1693B.

Thus γ_847(L) ⊆ p^1694B ⊆ p^1689L; the quotient has class at most 846. This is strictly below 1009.

I independently inspected the primary paper by Cicalò, de Graaf and Vaughan-Lee, *An effective version of the Lazard correspondence*, Journal of Algebra 352 (2012), 430–450. Its introduction states the correspondence for finite Lie rings of p-power order and class below p; pages 433–434 explain invertibility of the needed denominators and explicitly identify the automorphism groups. These statements do not require additive exponent p. Source: [author manuscript](https://iris.unitn.it/retrieve/e3835192-3015-72ef-e053-3705fe0ad821/lazard.pdf), inspected 2026-09-15 UTC.

Independently, the degree-n associative expansion of log(exp(X)exp(Y)) uses factorials and logarithm denominators with prime divisors at most n; the Dynkin conversion divides by n and introduces no larger prime. Truncation at n=846 is therefore well-defined modulo p^1689. The class bound makes all longer Lie terms zero.

The resulting group has the same full automorphism group as its Lie ring, and the conditional count gives

    |Aut(G)| = p^(30·1689+1689) = p^52359 = |G|.

## Publication recommendation for these sections

No mathematical correction is required in the sections audited here. Two short additions would improve readability: explicitly observe that finite additive automorphisms are Z/p^i-linear before lifting, and spell out the equivalence between the ordinary bracket error and the natural tensor-action error. These are clarifications of valid steps, not missing hypotheses.

**Exact remaining verification boundary:** establish the upstream algebra/flag claims and independently reproduce the Smith certificate. Subject to those inputs, the analytic and finite-group deductions are verified.
