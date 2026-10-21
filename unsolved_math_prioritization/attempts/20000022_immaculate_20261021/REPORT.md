# Row 1895 / ID 20000022: scoped mathematical analysis

## Decision and source boundary

**Partial progress only; no complete solution; no publication or QUEUE edit.** The exact private corpus record and recovery gate were inspected. The actual AIM task asks for the symplectic interpretation of toric fan criteria and consequences of suitable subspace generalizations. It does not ask merely for an abstract Hom-vanishing translation. The original live page was not newly recovered here; identity relies on the recovery gate's matched corpus fields.

Primary sources inspected on 2026-10-21:

- Borisov–Duncan, arXiv:2312.02885v3, https://arxiv.org/html/2312.02885v3, Theorems 1.1–1.2 and Remark 4.5. The forbidden-cone infinitude theorem is already proved; necessity of deficient slope hulls is explicitly separate and unresolved there. No independently verified 2026 journal-status claim is made.
- Borisov–Wang, arXiv:1904.00799v3, https://arxiv.org/html/1904.00799v3, Proposition 3.8, Theorem 2.14 and Theorem 4.12. In particular, the annihilator of a deficient slope hull can be chosen to be a fan ray. This existing theorem materially simplifies the computational approach below.
- AIM workshop report, https://aimath.org/pastworkshops/syzygymsrep.pdf, pp. 4–5. It already discusses vanishing Floer cohomology for Lagrangian sections and a possible matroid perspective.
- Altmann–Buczynski–Kastner–Winz, https://www.intlpress.com/site/pub/files/_fulltext/journals/pamq/2020/0016/0004/PAMQ-2020-0016-0004-a012.pdf. Search-visible primary text Figure 4 explicitly treats the Hirzebruch example; this report does not claim its elementary classification below is new.

The five approaches below contain proofs or explicit obstruction calculations, not five claimed solutions. Approaches 2–4 develop precise versions of the proposed generalization. Approach 5 excludes a tempting but incorrect mirror model. None supplies a new general brane construction.

## 1. Exact slope-kernel test, with a wall obstruction

Let Sigma be a complete simplicial rational fan of dimension d, with n rays v_i and maximal cones sigma. Values a=(a_i) specify a continuous Sigma-piecewise-linear function uniquely. For each maximal cone, form the invertible d-by-d matrix V_sigma with its ray vectors as rows, and the d-by-n selector S_sigma. Its slope is m_sigma=P_sigma a, where P_sigma=V_sigma^{-1} S_sigma. Fix sigma_0. For each ray w define the rational matrix

A_w = stack over sigma != sigma_0 of [w^T (P_sigma-P_sigma_0)].

Here w^T denotes the row vector evaluating a dual slope; vectors v_i are understood as coordinate columns when used in this formula. Every global linear function lies in ker A_w, providing a d-dimensional subspace G. Consequently

ker A_w/G != 0 iff n-rank(A_w)>d.

By Borisov–Wang Proposition 3.8, there exists a support function with 0 < dim(conv slopes) < d if and only if this strict inequality holds for at least one ray w. The backward implication follows immediately because all slopes have the same value on w and the function is not globally linear. The forward implication is exactly where Proposition 3.8 is used, not something newly proved here. All matrices are rational: a positive test admits a rational nonglobal solution and, after clearing denominators, integral slopes. Thus a finite exact certificate is available without enumerating tempting subsets. A negative test excludes this sufficient mechanism, NOT infinitude in dimensions where its necessity is open.

A second independently elementary certificate helps explain the matrix. Let G_w have maximal cones as vertices and join adjacent cones across a codimension-one wall tau whenever w is not in span(tau). Across a wall, continuity implies that the difference of slopes is a scalar multiple of a wall normal u_tau. If the slopes all evaluate equally on w and u_tau(w)!=0, their difference is zero. Therefore slopes are identical on each component of G_w. If G_w is connected, the only solution is globally linear. If G_w is disconnected this is only a necessary opportunity, not a sufficient certificate: compatibility across the omitted walls must still be checked by A_w.

The exact SymPy checker in check.py constructs A_w over QQ, not floating point. It checks P2, P3, F_0,F_1,F_2,F_5, (P1)^3, and the blowup of (P1)^3 at a torus fixed point. The raw fan and rank data are in results.json. These are validation fixtures, not a search across all threefolds. Completeness and smoothness of the fixtures follow from the standard simplex/product/Hirzebruch constructions and one stellar subdivision at a smooth maximal cone.

**Outcome:** a rigorous implementable reduction and obstruction, largely a corollary of existing work. The missing theorem is that a Borisov–Duncan safe direction forces one of these nonzero kernels. This report does not prove it.

## 2. Full non-product test case: Hirzebruch surfaces

Let F_n, n>=0, have negative section S with S^2=-n and fiber F, and write L(a,b)=O(aS+bF). For n>0 the entire immaculate locus is

{(-1,b): b in Z} union {(0,-1),(-2,-n-1)}.

For n=0 it is {a=-1} union {b=-1}.

Proof: if a>=0, the projection p:F_n->P1 has no higher direct images and

p_*L(a,b) = direct sum over j=0,...,a of O_P1(b-jn).

A sum of line bundles on P1 has all cohomology zero exactly when each summand has degree -1. For n>0 this forces a=0,b=-1. For n=0 it forces b=-1. For a=-1, all relative cohomology vanishes. For a<=-2 use Serre duality and K_Fn=-2S-(n+2)F: the dual coordinates are (-2-a,-n-2-b), which reduce to the already solved a>=0 case. This proves both directions, including all endpoints.

This is a genuine non-product classification for n>0 and a controlled target for any explicit mirror construction. It is not novel: it belongs to the established Picard-rank-two theory. The sequence b maps to a fixed relative immaculate window, whereas the two isolated classes do not form extra asymptotic directions.

**Outcome:** exact classification benchmark; no new general theorem or mirror construction.

## 3. Birational generalization with a sharp exceptional strip

Let f:X'->X be the blowup of a smooth variety along a smooth center Z of codimension c>=2, with exceptional divisor E. For any line bundle L on X and integer 0<=k<=c-1,

R Gamma(X',f^*L tensor O(kE)) = R Gamma(X,L).

Hence f^*L(kE) is immaculate if and only if L is immaculate in this entire strip. For smooth toric centers this yields non-product toric families; the statement is not contingent on a literal product decomposition.

Proof: Rf_*O_X'=O_X for a blowup of a smooth center. Induct using

0 -> O((k-1)E) -> O(kE) -> O_E(-k) -> 0.

The exceptional divisor is a P^{c-1}-bundle over Z, and its relative cohomology of O_E(-k) vanishes for 1<=k<=c-1. Thus Rf_*O(kE)=O_X throughout the strip. Projection formula and derived global sections prove the assertion.

For a concrete threefold, blow up a torus fixed point of X=(P1)^3. With H_i pulled back from its factors, all classes

-H_1 + a H_2 + b H_3 + kE, a,b in Z, k=0,1,2,

are immaculate. More generally the whole pullback-product locus is characterized exactly for each of these three k values. This fan has three opposite ray pairs, so it lies outside the at-most-one-pair hypothesis in BW's necessity theorem, but it already satisfies their sufficient condition and is not evidence resolving the remaining necessity question.

The k-window is sharp uniformly. Put L=O(-1,0,0), which is immaculate. At k=3, the exact sequence has quotient L|_p tensor O_P2(-3) with nonzero H^2; since the k=2 term is acyclic, f^*L(3E) has nonzero H^2. At k=-1, the sequence 0->f^*L(-E)->f^*L->L|_p->0 yields nonzero H^1. These exclude extending the strip on either side for this L.

The support-function mechanism also survives any fan refinement: an old piecewise-linear function remains linear on every new cone, with the same slope set (every old maximal cone has a full-dimensional subdivision). Therefore a pre-existing deficient nonzero slope hull persists. This explains why arbitrary sequences of toric blowups starting from products cannot find a counterexample to BW necessity: they retain its sufficient mechanism.

**Outcome:** exact elementary birational propagation and sharp boundary calculation; standard derived/projective-bundle facts, no novelty claim.

## 4. Numerical obstruction to arithmetic families, and its failure as a criterion

Let X be smooth projective of dimension d over characteristic zero, and suppose L tensor M^t is immaculate for infinitely many distinct integers t. Hirzebruch–Riemann–Roch says

P(t)=integral_X exp(c1(L)) exp(t c1(M)) td(X)

is a polynomial of degree at most d. Infinitely many zeros force P=0, so for every j=0,...,d,

integral_X c1(M)^j/j! [exp(c1(L)) td(X)]_{d-j}=0.

In particular c1(M)^d=0. Thus no arithmetic family in an ample direction can be immaculate at infinitely many integers. For a surface the three exact conditions are M^2=0, M.(2L-K_X)=0, and chi(L)=0.

The conditions are NOT sufficient, even for a toric surface. On F_2, L=O(S) has chi(L)=0 but the direct image is O_P1 plus O_P1(-2), so h^0(L)=h^1(L)=1. Euler cancellation does not imply cohomological vanishing. More strongly, set M=O(S+F), a nonzero Picard class. Then M^2=0 and M.(2L-K)=0, so chi(L tensor M^t)=0 for every integer t. Yet Approach 2 shows that (a,b)=(t+1,t) is immaculate exactly for t=-3,-2,-1. Thus all three numerical family conditions hold while only three members of the progression are immaculate. This is an explicit falsification of the whole proposed numerical shortcut, not merely of its constant term.

The obstruction concerns an arithmetic progression with fixed direction, not every arbitrary infinite subset of Pic(X). It should not be substituted for the forbidden-cone theorem or the unknown slope implication. Since the product/blowup examples above vary in fiber-type directions, their top self-intersection is zero as expected.

**Outcome:** exact rejection test and explicit false-positive example; standard Riemann–Roch consequence.

## 5. Direct mirror model obstruction: compact periodic exact graphs cannot work

A naive attempt is to represent both the unit and every toric line bundle by compact exact graph sections of T^*T, with T a real torus, and infer immaculate vanishing by removing their intersections. This model fails before any fan computation.

For smooth globally defined functions f,g:T->R, graph(df) meets graph(dg) wherever d(f-g)=0. Since T is compact, f-g attains a maximum and minimum, so an intersection always exists. More strongly, with the usual compatible trivial rank-one brane data, the ordinary compact exact Floer theory of these Hamiltonian-isotopic sections is modeled by the Morse cohomology of f-g and is H^*(T), not zero. The second assertion refers to ordinary compact exact Floer theory, not a stopped-category computation with altered objects. Nontrivial local systems, noncompact representatives, stops, and admissibility data must not be erased.

This excludes a concrete proposed explanation of the original question: deficient slope hulls cannot simply make globally periodic exact graphs disjoint from the zero section. To advance the actual mirror question one needs explicit appropriate noncompact/stopped representatives, plus a boundary-sensitive Morse/Floer differential or a valid comparison theorem. The existing abstract unit-orthogonality statement supplies neither.

**Outcome:** rigorous obstruction to a wrong model; no construction of the desired geometric mirror. The original broad task remains open in the sense that this work does not resolve it.

## Acceptance boundaries

Accept only: the exact matrix reduction with its cited Proposition 3.8 dependency; the wall-connectivity obstruction; the fully proved Hirzebruch classification; the sharp blowup strip; the numerical necessary conditions and counterexample; and the compact-graph obstruction under stated brane assumptions.

Reject: novelty claims for known classifications, calling the matrix test a proof of necessity, counting the blowup examples as resolving all multiple-collinearity threefolds, treating chi=0 as immaculacy, replacing stopped/noncompact branes by periodic exact graphs, or marking the AIM problem solved.
