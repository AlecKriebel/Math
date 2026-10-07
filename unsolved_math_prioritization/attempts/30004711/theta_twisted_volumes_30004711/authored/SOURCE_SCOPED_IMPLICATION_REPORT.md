# Theta-twisted volumes: prior theorem and normalization audit

Problem 30004711 (OWR-7155449-015). Checked 7 October 2026.

## Conclusion

The natural Euler-form extension and the resulting volume/intersection-number identity already have a proof credited to **Paul Norbury**. The exact coefficient-one formula requires a normalization convention. It is incorrect for the unscaled canonical Euler-form integral: the smallest positive-genus stable case gives 1/16 versus 1/8. The later normalized definition gives precisely the coefficient-one identity.

The original Oberwolfach report does **not** define an additional operation called “completion.” That adjective in the catalog is not a license to insert a missing scalar. Its displayed normalization and dual/orientation conventions must be corrected or explicitly clarified before describing the unqualified catalog formula as proved. This report is a source-scoped implication and statement audit, not a new proof of Norbury's theorem and not a final five-turn unsuccessful research result.

## 1. What the original source actually specifies

Paul Norbury's contribution, “Volume of the moduli space of super Riemann surfaces,” occupies printed pp. 1507–1510 of [Oberwolfach Report 28/2021](https://ems.press/content/serial-article-files/46907). The relevant PDF pages are 46–47, printed pp. 1508–1509. These pages were inspected as rendered images as well as extracted text.

Writing S for the spin moduli space, the report displays:

- Vol(Mhat) = integral of the torsion measure mu = integral over S of e(nu) exp(omega_WP).
- E = -R pi_* of the dual universal spin line, with fibre H^1(C,L^dual), and a natural extension nu -> E.
- Theta_(g,n) = (-1)^n 2^(g-1+n) p_* c_(2g-2+n)(E).
- Vhat_(g,n)(L) = integral of mu over the bordered super moduli space.
- V^Theta_(g,n)(L) = integral over Mbar_(g,n) of Theta_(g,n) exp(2 pi^2 kappa_1 + (1/2) sum L_i^2 psi_i).
- Conjecture 2: Vhat_(g,n)(L) = V^Theta_(g,n)(L).

No scalar multiplier is displayed in the definition of Vhat, and the contribution does not define “completed volume.” The source itself asks whether the natural Euler representative has the required extension. Its symbol nu and the later dual-bundle convention should not be identified without tracking orientation. In particular the formulas alone do not establish that the torsion measure in the report has the normalization of the later normalized Euler measure.

## 2. Precise modern formulation

Use g,n >= 0 with 2g-2+n > 0, all external markings/boundaries Neveu–Schwarz, and L_i >= 0. The geometric interpretation uses these real nonnegative lengths; the resulting polynomial can subsequently be evaluated at arbitrary complex arguments. The n=0 case is included when g>=2. The unstable disk and annulus are not part of this assertion.

Let p:Sbar -> Mbar_(g,n) forget spin and orbifold structures. A point of Sbar is a stable twisted curve C with isotropy Z/2 at markings and nodes, and a spin line theta satisfying theta^2 = omega_C^log. The representation at every external marking is nontrivial. Nodes may have either spin type.

Put r=2g-2+n and F=R^1 pi_*(theta^dual), a rank-r bundle. Negativity of theta^dual on each stable irreducible component makes H^0 vanish. Thus this derived pushforward is a genuine bundle, not merely a K-theory class. Define

A(L)=2 pi^2 kappa_1 + (1/2) sum_i L_i^2 psi_i,

T(L)= integral_(Mbar) Theta exp(A(L)),

W(L)= integral_(S(L)) e(F^dual, canonical Chern connection) exp(omega_WP),

N(L)=2^(g-1+n) W(L).

The classes psi_i here live on the coarse pointed-curve moduli space. If psi_tilde denotes the cotangent class at the orbifold marking, then psi_tilde_i=(1/2)p^*psi_i. Consequently the two exponents (1/2)sum L_i^2 p^*psi_i and sum L_i^2 psi_tilde_i agree; no extra factor of two in the boundary lengths is allowed.

The spin labels in the two later papers differ: the all-NS locus is denoted o=(0,...,0) in arXiv:2005.04378v4 and sigma=(1,...,1) in arXiv:2312.14558v3. They describe the same NS condition, not different components to be summed.

## 3. The theorem-level bridge

The primary source [Norbury, arXiv:2005.04378v4](https://arxiv.org/abs/2005.04378v4), submitted 23 December 2025, gives the following dependency chain. Its PDF is the authoritative locator for equation numbers here; the generated HTML renumbers some equations.

1. Definition 2.3, PDF p.10: the algebraic extension F is constructed from the universal twisted spin curve. Theorem 3.18 and Corollary 3.19, pp.34–35, establish the flat/holomorphic bundle comparison on the smooth NS locus. This uses Higgs-bundle methods, not equality of recursions.
2. Section 3.4, pp.35–37: the canonical Hermitian pairing on the dual fibre of 3/2-differentials is the integral of conjugate(eta) xi / sqrt(h), with h the complete hyperbolic metric. Its compatible Chern connection defines the Euler form.
3. Theorem 6, pp.37–38: that natural Euler form extends and its extended cohomology class is e(F^dual). This is the substantive geometric theorem used, not inferred here from convergence of a single integral. Finiteness at a node alone would not prove smooth dependence on a plumbing parameter or the absence of boundary correction classes.
4. Remark 3.20, p.36, transports the same Euler form to positive boundary lengths. The Weil–Petersson current extension and symplectic-reduction formula supply the class p^*A(L).
5. Theorem 1, p.5, with proof in section 3.4.2, p.39, gives **W(L)=2^(1-g-n)T(L)**. Its proof passes through the compactified spin integral and the projection formula.

The paper's [publisher record](https://www.sciencedirect.com/science/article/abs/pii/S0393044025003353) identifies publication in Journal of Geometry and Physics 222 (April 2026), article 105750, [DOI 10.1016/j.geomphys.2025.105750](https://doi.org/10.1016/j.geomphys.2025.105750). The arXiv PDF, not an inaccessible publisher full text, was used to inspect the proof.

A second primary source, [Norbury, arXiv:2312.14558v3](https://arxiv.org/abs/2312.14558v3), fixes the normalized convention explicitly. Equation (3), PDF p.3, multiplies the Euler integral by epsilon_(g,sigma)=2^(g-1+(n+|sigma|)/2), which is 2^(g-1+n) on sigma=1^n. Its Definition 3.2 and Theorem 3.3, pp.10–11, give the same algebraic extension and natural Euler-class identification; Corollary 3.5, p.12, converts the volume into compactified intersection numbers. Set the number m of Ramond markings to zero. This gives **N(L)=T(L)**, the desired coefficient-one version, without appealing to any recurrence.

## 4. Explicit implication, including sign and scalar

The rank is r=2g-2+n, so (-1)^r=(-1)^n. Therefore

c_r(F^dual)=(-1)^n c_r(F),

Theta = (-1)^n 2^(g-1+n) p_*c_r(F)
      = 2^(g-1+n) p_*e(F^dual).

Using the geometric extension theorem and its integration result,

W(L) = integral_(Sbar) e(F^dual) exp(p^*A(L))
     = integral_(Mbar) p_*e(F^dual) exp(A(L))
     = 2^(1-g-n) T(L).

Multiplication by 2^(g-1+n) proves N(L)=T(L). This calculation is formal once the cited geometric theorem is available. It is not a new proof of that theorem. It also identifies exactly where the missing factor enters. In genus zero, r=n-2 exceeds dim_C Mbar_(0,n)=n-3, so both sides vanish. For g>=1, the difference of complex degrees is g-1, explaining the degree bound g-1 in the squared boundary lengths.

The class equality used here is an equality on the compactification. Equality of characteristic classes restricted to the open moduli space would not be enough: restriction can discard classes supported on the boundary. Similarly, there is no claim that arbitrary Euler differential-form representatives coincide pointwise.

## 5. Independent low-genus normalization check

[Norbury, A new cohomology class on the moduli space of curves, arXiv:1712.03662v4](https://arxiv.org/abs/1712.03662v4), Proposition 2.9, computes the genus-one pushforward by orbifold Grothendieck–Riemann–Roch. Independently of the volume recursion, it gives p_*c_1(F)=-(3/2)psi_1. Re-evaluating its rational expression gives

-2 [11/24^2 + 1/24^2 + (1/2)(1/24)(1/2)] = -1/16.

Since integral_(Mbar_(1,1)) psi_1=1/24,

T_(1,1)(L)=integral 3psi_1=1/8,

W_(1,1)(L)=integral p_*c_1(F^dual)=1/16,

N_(1,1)(L)=2 W_(1,1)(L)=1/8.

No positive-degree term of exp(A) contributes, because Theta already has top degree. Exact rational arithmetic for these identities is recorded in NORMALIZATION_CHECK.json. This refutes the identification of the **raw canonical Euler volume** with T, not every possible rescaling or orientation convention of a torsion-defined super measure.

## 6. What may and may not be concluded

Supported:

- The claim that no natural Euler-form extension theorem is known is contradicted by the inspected primary results.
- The normalized canonical Euler-measure version of the identity is already proved by Norbury.
- The raw canonical Euler-measure version requires the displayed factor 2^(1-g-n); it is already unequal at (g,n)=(1,1).
- The imported wording does not specify any separate “completion” that repairs its notation.

Not claimed:

- No new theorem or novelty is claimed here.
- We do not silently redefine the original OWR torsion measure mu as N, or call its unqualified printed normalization correct.
- We do not claim an independent reconstruction of every analytic argument proving Theorem 6. In particular, checking pole integrability would not substitute for that theorem.
- We do not claim that all foundational supergeometry is settled: section 4.4 and the conclusion of the current paper still distinguish a fully supergeometric derivation from its established Euler/intersection-theoretic construction.
- No Ramond deformation, unstable value, or equality of full CohFTs is added to the NS problem.

Recommended mathematical disposition after independent review: **prior theorem with a required normalization/statement correction**. A coefficient-one statement is valid if Vhat is explicitly N. If Vhat is explicitly the raw canonical W, replace it by the factor-bearing formula. If a separate literal torsion-measure identity is intended, its measure normalization and comparison to the canonical Euler form must be supplied before that stronger formulation can be certified. This source ambiguity must not be hidden by a “solved as written” label.
