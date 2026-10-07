# Independent source and normalization audit: problem 30004711

Checked 7 October 2026. Scope: the all-Neveu-Schwarz (NS), stable volume/intersection identity associated with Norbury's contribution to OWR 28/2021. This is a source-scoped mathematical audit, not a new proof or an exhaustive priority search.

## Disposition

**Accept the normalized canonical Euler-volume identity as a prior theorem of Paul Norbury, subject to the explicit conventions below. Do not certify the literal OWR coefficient-one identity as written.**

The frozen candidate report, SHA-256 `fe38b9dac323407637721620afbad4e31eaca28ab373dd9b6f557a6810eaa506`, has the correct main projection-formula calculation and correctly limits its genus-one countercheck to the canonical Euler integral. Its public presentation should receive a separate correction/addendum for the historical torsion conventions, the source typographical issues, and the page locator identified below. Its frozen bytes need not be changed.

Recommended queue status: **Prior theorem; normalization clarification required**. Recommended finding: **Norbury's canonical Euler extension yields W=2^(1-g-n)V^Theta; the explicitly normalized N=2^(g-1+n)W equals V^Theta. At (1,1), W=1/16 and V^Theta=1/8 on the same spin-stack convention. OWR's literal torsion-measure/orientation identification is not certified; no new proof and no solved-as-written claim.**

A finding that an exact source comparison is not certified by this audit is not a claim that it is a newly discovered open problem or has never been proved elsewhere.

## 1. Original OWR statement

Primary source: [OWR 28/2021, DOI 10.4171/OWR/2021/28](https://ems.press/content/serial-article-files/46907), contribution by Paul Norbury, printed pp.1507-1510. I inspected the extracted contribution and rendered PDF pp.46-47, printed pp.1508-1509.

The source displays a torsion-defined measure mu on the super moduli space, an equality of its integral with the spin-space integral of e(nu) exp(omega_WP), an extension of nu to the algebraic bundle with fibre H^1(C,L^dual), and

Theta_(g,n) = (-1)^n 2^(g-1+n) p_* c_(2g-2+n)(E).

It then defines the bordered Vhat as the integral of mu and conjectures Vhat=V^Theta, where V^Theta uses the exponent 2 pi^2 kappa_1 + (1/2) sum L_i^2 psi_i. The contribution neither displays the factor 2^(g-1+n) in Vhat's definition nor defines an operation called completion. Its following discussion identifies the natural Hermitian Euler representative as the comparison it hopes to establish.

This supports a statement-level normalization warning. It does **not** authorize equating the original mu with the later normalized N, nor prove the original torsion measure has the value 1/16.

## 2. Exact stable geometric scope

Fix g,n nonnegative integers with 2g-2+n>0. Let Sbar be the compactified stack of stable twisted spin curves with order-two stabilizers at markings and nodes, a line theta satisfying theta^2=omega^log, and nontrivial representation at every external marking. The all-NS locus includes its even and odd parity components. No extra parity weight is inserted into the algebraic pushforward below. Nodes of either spin type occur in the compactification.

Let p:Sbar -> Mbar_(g,n) be the spin/orbifold-forgetting morphism, and let pi be the universal curve. Put

r=2g-2+n, F=R^1 pi_*(theta^dual).

On every irreducible component X, stability gives deg(omega^log|X)>0 and therefore deg(theta^dual|X)<0. A global section vanishes on every component, so H^0(C,theta^dual)=0. Cohomology and base change together with orbifold Riemann-Roch produce a bundle F of rank r. This verifies the use of an ordinary top Chern class rather than a formal virtual rank alone.

Use the ordinary complex orientation, e(F^dual)=c_r(F^dual), and the standard Chern-Weil normalization. The canonical Hermitian form on F^dual over the smooth locus is obtained by integrating the product of its 3/2-differentials against the reciprocal square root of the complete hyperbolic metric. Write e_can(F^dual) for its top Chern form. Boundary-length transport is the one specified in Norbury's Remark 3.20; it does not vary the Euler representative independently of that transport.

Set

A(L)=2 pi^2 kappa_1+(1/2) sum_i L_i^2 psi_i,
T(L)=integral_(Mbar) Theta_(g,n) exp(A(L)),
W(L)=integral_(S(L)) e_can(F^dual) exp(omega_WP),
N(L)=2^(g-1+n) W(L).

The geometric lengths lie in R_>=0; zero denotes cusps. Polynomial evaluation at other arguments is algebraic continuation, not a claim about hyperbolic surfaces of those lengths. The case n=0 is included for g>=2; unstable disk/annulus values are excluded. Ramond external markings and parity-refined identities are not added to this assertion.

The psi_i in A are the coarse moduli-space cotangent classes. On the twisted spin space psi_tilde_i=(1/2)p^*psi_i, so sum L_i^2 psi_tilde_i=(1/2)sum L_i^2 p^*psi_i. There is no permitted extra rescaling of the lengths. The all-NS labels are o=0^n in 2005.04378v4 and sigma=1^n in 2312.14558v3.

## 3. The theorem actually used and the complete formal implication

Primary source: [Norbury, Enumerative geometry via the moduli space of super Riemann surfaces, 2005.04378v4](https://arxiv.org/abs/2005.04378v4).

The dependency is the algebraic extension (Definition 2.3, p.10), the NS flat/holomorphic comparison (Theorem 3.18 and discussion, pp.34-35), the natural metric construction (p.36), its compactified Euler-class extension (Theorem 6, pp.37-38), boundary-length transport (Remark 3.20, **p.37**), and the Weil-Petersson extension/symplectic-reduction class. The resulting integral statement is Theorem 1, p.5, with the projection-formula proof on p.39.

The mathematical consequence, keeping F and F^dual distinct, is

c_r(F^dual)=(-1)^r c_r(F)=(-1)^n c_r(F),
Theta_(g,n)=2^(g-1+n) p_* e(F^dual).

The cited extension and integration theorem gives

W(L)=integral_(Sbar) e(F^dual) exp(p^*A(L))
    =integral_(Mbar) p_*e(F^dual) exp(A(L))
    =2^(1-g-n) T(L).

Consequently N(L)=T(L). This proves the implication from the cited geometric theorem; it does not reproduce an independent proof of that analytic theorem.

The equality must hold on the compactification. Equality after restriction to the open locus alone does not exclude boundary-supported discrepancies. Likewise, local pole integrability at a fixed nodal curve alone does not prove smooth dependence in plumbing parameters, and is not used here as a substitute for Theorem 6.

For genus zero, r=n-2 is greater than dim_C(Mbar_(0,n))=n-3, so the relevant forms/classes and both volumes vanish by degree. For g>=1, the remaining complex degree is (3g-3+n)-r=g-1. Thus the polynomial degree in the variables L_i^2 is at most g-1, consistent with the source.

A second clean normalization source is [Norbury, Super Weil-Petersson measures on the moduli space of curves, 2312.14558v3](https://arxiv.org/abs/2312.14558v3). Equation (3), p.3, inserts epsilon_(g,sigma)=2^(g-1+(n+|sigma|)/2), which equals 2^(g-1+n) for all NS. Definition 3.2, Theorem 3.3, and Corollary 3.5, pp.10-12, supply the matching extension and compactified integral. Only the m=0 specialization is used here, avoiding unrelated Ramond-index conventions.

## 4. Genus-one check, with stack convention held fixed

Primary source: [Norbury, A new cohomology class on the moduli space of curves, 1712.03662v4](https://arxiv.org/abs/1712.03662v4), Proposition 2.9, PDF p.11.

The displayed orbifold GRR evaluation is

integral p_*c_1(F) = -2[11/24^2 + 1/24^2 + (1/2)(1/24)(1/2)] = -1/16.

The same proposition gives p_*c_1(F)=-(3/2)psi_1 and Theta_(1,1)=3psi_1. With integral psi_1=1/24 this yields

integral p_*e(F^dual)=1/16,
T_(1,1)=1/8,
N_(1,1)=2W_(1,1)=1/8.

There are no positive-degree exponential terms in this case. The rational calculation was rerun with exact fractions; the accompanying check file records it.

Both 1/16 and 1/8 here use **the same p, same stack integral, same bundle, and same complex orientation**. The distinction is the factor 2 in the definition of Theta, not a change of rigidification between the two computations. An orientation reversal can change a sign, not remove this factor. Replacing the stack with a rigidification and retaining the old pushforward without a degree correction is not a valid argument.

Additional current check: [Norbury, Spin structures and measures on the moduli space of curves, 2608.25237v2](https://arxiv.org/abs/2608.25237v2), pp.39-40, repeats the total -1/16 and computes the odd part as -1/32, hence the even part as -1/32. Page 35 records the degree 2^(2g-1) stack-forgetting convention. Its explicitly scaled volumes are consistent with the normalization distinction; its bundle names are not used to override the F/F^dual definitions above.

This is a countercheck to W=T. It is **not** a counterexample to a differently oriented, parity-weighted, rigidified, or rescaled super torsion measure unless the missing exact identification is separately proved.

## 5. Historical torsion conventions: what is specified and what is not

OWR cites [Stanford and Witten, JT Gravity and the Ensembles of Random Matrix Theory, 1907.03363v5](https://arxiv.org/abs/1907.03363v5). It is incorrect to describe the cited torsion literature as having no specified normalization.

Appendix A, equations (A.17)-(A.18), printed pp.112-113 / PDF pp.113-114, states the Euler-integral convention and explicitly rescales the torsion tau by

mu_SW=(2 pi)^chi tau, chi=2-2g-n.

The bosonic restriction is the standard Weil-Petersson normalization. Appendix A.3 also discusses the sign change (-1)^n from reversing the complex orientation, and fixes its choice through disk/pants conventions. Appendix D, equations (D.40)-(D.41), printed p.136 / PDF p.137, applies the torsion rescaling to pants.

There are further bookkeeping differences. Section 5.2.2, equation (5.37) and footnote 58, printed p.98 / PDF p.99, uses a spin sum weighted by (-1)^zeta. Its equation (5.40) gives V_1(b)=-1/8. Footnote 56, printed p.93 / PDF p.94, specifies a one-holed-torus half-volume convention. These facts prevent using that -1/8 as a direct contradiction to the unweighted oriented algebraic stack calculation without tracing all conventions.

The current 2608.25237v2 source says the two NS parity contributions are added, explicitly normalizes its measure (Definition 4.2, p.27), and presents general parity equality as Exercise 9 on p.34 rather than proving it. In genus one the equal -1/32 algebraic contributions would cancel under a naive extra parity sign. Thus merely inserting the SW parity weight in the same complex-oriented algebraic integral cannot be the full comparison. This audit has not identified and verified a complete term-by-term orientation/rigidification/boundary convention map for OWR's original mu.

Nor is a missing scalar a new discovery of the latest version:

- 2005.04378v1 (9 May 2020), pp.3-4 and 44, already displays a factor-bearing Euler/intersection relation, with an older sign/dual convention, and a separate relation to the SW volumes. Its argument on p.44 chooses an extension connection; this is not itself a proof about the required natural connection on a noncompact space.
- v2 (20 April 2023), Theorem 1, p.5, already gives 2^(1-g-n), and introduces a natural-Euler extension theorem.
- v3 (25 May 2023), Theorems 1 and 6, pp.5 and 36-37, uses the explicit compactified extension formulation.
- v4 retains the factor. Its p.50 explicitly writes V_SW=(-2)^n W=(-1)^n2^(1-g)T.

The latter equation is a source-stated comparison of volume conventions; it does not by itself prove that OWR's symbol mu is the later normalized N, particularly in light of the different displayed definitions. No inspected source supplied an OWR erratum making that exact identification.

## 6. Source-level slips and acceptance limits

1. The candidate's locator for Remark 3.20 should be p.37, not p.36.
2. In 2005.04378v4, the line preceding Corollary 3.19 identifies H^1(theta^dual)^dual with the flat cohomology, while Definition 2.3 defines the compact bundle by H^1(theta^dual); the corollary's printed bundle equation suppresses this dual distinction. Do not certify it as an orientation-preserving identification without qualification. The class calculation above fixes the dual explicitly, and 2312.14558v3 provides the clean algebraic definition.
3. In rendered v4 p.35, equation (39) prints (1/(4 pi))^N pf(F_A) for real rank N, alongside the claim that its Pfaffian is O(N)-invariant. Under the given ordinary Pfaffian/curvature conventions the Euler normalization is Pf(F_A/(2 pi)) (with the chosen orientation), and invariance is under SO(N). The printed prefactor is inconsistent with the adjoining assertion e=c_(N/2). This audit uses that declared standard characteristic-class normalization, not the literal erroneous prefactor. The same prefactor appears in 2312.14558v3 p.9 and 2608.25237v2 equation (16). These source slips are not a new route to a coefficient-one raw-volume identity.
4. The smooth-extension argument is cited, not independently rebuilt. Neither the numerical GRR check nor a check of pole integrability supplies the missing global analytic work.
5. The later Ramond statements, supergeometry foundations, parity-refined all-genus identities, and an exact theorem for the original OWR torsion measure remain outside this acceptance.

## 7. Acceptance/failure checklist

Accepted:

- Stable all-NS range, including stable n=0; all NS parity components retained.
- Rank, dual sign, standard Euler/top-Chern normalization, and psi factor.
- The compactification-dependent projection formula W=2^(1-g-n)T and N=T, invoking Norbury's named extension/integration theorem.
- Exact genus-one GRR arithmetic and its same-stack interpretation.
- The existence of explicit historical torsion and volume conventions; no hidden completion.
- A bounded current-source check through 2608.25237v2, with no novelty assertion.

Fails / is not certified:

- Literal OWR solved-as-written label.
- Identifying OWR mu with N only by renaming it.
- Calling 1/16 versus 1/8 a literal OWR counterexample without a measure comparison.
- Treating equality of open-locus classes or an arbitrary connection as sufficient.
- Importing the printed Pfaffian prefactor as the standard Euler normalization.
- Claiming a complete independent proof of the analytic extension theorem.

A correction/addendum satisfying these items, while preserving the frozen report and distinguishing its scope, is an appropriate acceptance artifact. No publication was performed by this audit.
