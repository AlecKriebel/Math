# Independent modular and Kummer derivations

These derivations test the manuscript as a hypothesis. They are independent of candidate scripts and prior audit reports. The exact polynomial checks in `check_primary_arithmetic.py` use only `fractions`, `dataclasses` and `json` from Python's standard library. A successful replay is `python3 check_primary_arithmetic.py`; its current result is recorded in `arithmetic_stdout.json`. The failed exploratory derivative-factor guess is preserved separately as `arithmetic_failed01_stderr.txt`.

## Parameters and signs

Work in Q(r), r²=5, phi=(1+r)/2 and c=phi⁵=(11+5r)/2. Write h=(11−5r)/2. Then ch=−1, so h=−c⁻¹, rather than c⁻¹. The candidate's beta=h lambda/(lambda+5r) therefore gives

* c beta+1=5r/(lambda+5r);
* beta−c=−5r(lambda+c)/(lambda+5r);
* beta+c⁻¹=5r c⁻¹/(lambda+5r).

Consequently

    iota(beta)=(c beta+1)/(beta−c)=−1/(lambda+c),
    (beta−c)/(beta+c⁻¹)=−c(lambda+c),
    (c−beta)/(beta+c⁻¹)=c(lambda+c).

These are exact rational-function equalities; all cross products vanish in the independent program. The four excluded projective values lambda=0,−5r,−c,infinity map respectively to beta=0,infinity,c,−c⁻¹, precisely the Tate cusps. Thus a finite allowed lambda has beta≠0 and beta²−11 beta−1≠0.

Choose zeta with 1+zeta+zeta⁻¹=phi. Verdure's Theorem 5 has alpha5=8+5 zeta+5 zeta⁴=c and beta5=3−5 zeta−5 zeta⁴=−c⁻¹. His criterion is therefore exactly the second ratio above. Morton's b is −beta, so his (2b+11+5r)/(−2b−11+5r) is exactly the third ratio.

For a=lambda+c and theta⁵=a:

    (−1/theta)⁵=−1/a,
    (phi theta)⁵=c a,
    (−phi theta)⁵=−c a.

Thus all three radical *fields* are the same. In a fixed Kummer group, [−1/a]=[a]⁻¹ because −1=(−1)⁵; this is not equality of nontrivial fixed classes. The manuscript makes that distinction explicitly.

## Fisher map and all fibers

Fisher p.179 defines Y(5) as triples (E,P,Q) with e5(P,Q)=zeta and gives the action Q↦Q+P, with quotient X1(5). Lemma 1.1(iii), p.172, rules out automorphisms of (E,P) for a point P of order at least four. Section 2.1 constructs the parameter line X(5), the elliptic families and cusps. Lemma 3.4, p.194, gives the labelled-subgroup-preserving isomorphism and parameter beta=tau f(tau)/g(tau), with the same f and g as the manuscript.

Let N=tau f and D=g. The independent program checks gcd(N,D)=1 and

    N'D−ND'=(tau²−tau−1)⁴.

The map has degree five. Its only ramification points are tau=phi and tau=−phi⁻¹, with respective target beta=c and beta=−c⁻¹. There is no residual ramification over the cusp complement B=P1_beta\{0,infinity,c,−c⁻¹}.

The Mobius maps epsilon(tau)=(phi tau+1)/(tau−phi) and iota(v)=(c v+1)/(v−c) have nonzero determinants and square to scalar matrices. The exact homogeneous cross product verifies

    N/D=iota(epsilon(tau)⁵).

The variable u=epsilon(tau) therefore realizes this degree-five cover as u⁵=−1/(lambda+c). Since a=lambda+c is invertible on the allowed finite lambda base, u is invertible and the derivative 5u⁴ is invertible. This Kummer scheme is finite etale of degree five. Its normality follows from etaleness over a normal smooth base.

Independently, the complementary-basis scheme C={Q∈D_beta[5]:e5(P0,Q)=zeta} is an open and closed subscheme of the finite etale 5-torsion scheme. It has five geometric points in every fiber, all of the form Q+jP0. A point of C determines a full basis, and that basis determines all torsion; the absence of an automorphism fixing P0 eliminates a possible moduli quotient. Fisher identifies the generic function-field cover of C with the cover just computed. Both finite etale normal covers are the integral closure of the same base in that common function-field extension, hence are isomorphic on the entire base. This does not assert generic irreducibility persists after specialization. In split fibers the etale algebra is a product; every selected root still supplies a complete basis. The argument also includes j=0 and j=1728 because the marked point removes their stabilizers.

## Independent field and degree inference

Let F be any characteristic-zero field containing zeta over which D_beta and its marked point are defined. Verdure Proposition 3 and Corollary 1 establish that F(D_beta[5])/F is cyclic of degree one or five, and one complementary abscissa already generates the entire torsion field. Theorem 5, including its polynomial proof on pp.84–88, applies to every t with P5(t)≠0. In particular, its final specialization step notes Delta_T, T, T−alpha5 and T−beta5 stay nonzero. The theorem yields full rational torsion over F(theta), and excludes full rational torsion over F when theta is not already in F. Since the degree is then five, F(D_beta[5])=F(theta). This gives an arithmetic route independent of the finite-etale normalization argument.

For the manuscript's E, take L=K(delta,zeta). The given twist isomorphism supplies L(E[5])=L(theta). Its marked ordinate is −k³ d beta delta/2, with a nonzero coefficient in K on every allowed fiber, so K(E[5]) contains delta. The Weil pairing, by Sutherland Theorem 23.29 and Corollary 23.30, supplies zeta. Thus K(E[5]) already contains L and equals L(theta).

The quadratic facts are elementary: Norm_K/Q(d)=5, so d cannot be a square in K; K(delta) is real; K(zeta)/K is imaginary quadratic. Their intersection is K and [L:K]=4. If v∈L with v⁵=a∈K*, then n=Norm_L/K(v) satisfies n⁵=a⁴ and (a/n)⁵=a. Therefore a is a fifth power in L exactly when it is a fifth power in K. Kummer theory over L gives degree one or five and the total degree four or twenty.

In the degree-twenty case K(zeta,theta)/K has the usual order-ten dihedral group: theta is a real fifth root, zeta conjugation fixes theta, and it conjugates the fifth-root rotation to its inverse. The unique quadratic subfield is K(zeta), distinct from K(delta). Adjoining delta therefore gives D10×C2. In the split case the group is C2×C2. The independent delta involution acts as −I through the twist, so there is no nonzero K-rational fifth torsion. Over K(delta), real points restrict odd fifth torsion to the identity real circle, where the fifth-torsion subgroup has five points; the known five-point subgroup fills it. Generically the valuation of a=lambda+c at lambda=−c is one, forbidding a fifth power and giving degree twenty.

No primary-source or Kummer-sign gap remains in these deductions. Verification of the pentagonal birational bridge itself belongs to the separate geometric review, not this source family.
