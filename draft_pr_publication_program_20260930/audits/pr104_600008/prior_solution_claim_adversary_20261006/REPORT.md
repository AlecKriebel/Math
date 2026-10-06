# PR104 / problem600008: adversarial audit of the prior-solution claim

Audit date: 2026-10-06 UTC. Scope: historical disclosure and reconstruction of the stated degeneration, not a new central proof search. The candidate's mathematics is accepted by the parent task; this audit independently checks the competing primary source and the mapping needed to compare it.

## Bounded result

A prior explicit claim of solving this problem exists in Dragovic-Radnovic (DR), arXiv1909.08154v1, dated 18 September 2019. The paper does not display a counted surface-chain theorem or the candidate's mean formula. Nevertheless, its printed quadratures, together with its expressly indicated surface degeneration, admit a verified analytic reconstruction that is necessary and sufficient and is equivalent to the accepted candidate. This is materially stronger evidence than the bare remark. It supports an `already_solved` disposition **for the analytic parameter classification**, with the reconstruction and count convention attached. It does not certify a finite algebraic Cayley determinant in the axes, a printed proof of the entire surface statement, or priority of the exact mean presentation.

The first, independent checkpoint was saved before reading the candidate. It correctly rejected the naive fixed-total-reflection limit and left the rescaled quadrature route open. The subsequent reconstruction resolves that route rather than converting the fixed-period failure into a verdict against every possible prior solution.

## What the original sources say

The original GKT Problem 5.2 asks for necessary and sufficient axis conditions for its equator map T to return after k iterations with winding r; Section 4 supplies an invariant density, and Section 5 proves the porism. Tabachnikov's 2015 Section 7 instead describes chains of full alternating tropic-to-tropic arcs. These are distinct counting conventions. [GKT primary source](https://arxiv.org/pdf/0705.0188v1), [Tabachnikov primary source](https://amj.math.stonybrook.edu/pdf-Springer-final/014-0001-3.pdf).

DR's introduction expressly identifies both problems as solved. Theorem 3.1 defines N=m1+n1 as total ambient reflections. Theorem 3.2 concerns distinct nondegenerate caustics and a nonsingular curve; Lemma 3.3 gives Taylor rank tests. Proposition 3.5 and Proposition 4.2(b) state analytic and polynomial criteria for lightlike ambient billiards with a finite caustic. Remark 4.4 directs the reader to send the ellipsoidal caustic parameter to zero for surface null geodesics, but prints neither the resulting axes relation nor the period/winding conversion. [DR primary source](https://arxiv.org/pdf/1909.08154v1), printed pp.2,5-6,8-10,12-13.

These descriptions are source facts. The calculations and two-way reconstruction below are this audit's deductions; they should not be attributed to a displayed surface theorem in DR.

## The correct degeneration of the counts

Use a=a1>b=a2>0, c=a3>0 and a positive ellipsoidal caustic gamma in (0,b). After the lightlike limit of the second caustic, set

    G(x)=(a-x)(b-x)(c+x),
    R_gamma(x)=G(x)(gamma-x).

The three coordinate intervals are [-c,0], [0,gamma], [b,a]. Up to the common positive scale removed in the lightlike limit, DR's equation (3.2) becomes

    m1 C_k(gamma)+n1 B_k(gamma)-n2 A_k(gamma)=0,  k=0,1,

where C_k is the integral from 0 to -c, B_k from 0 to gamma, and A_k from b to a of x^k dx/sqrt(R_gamma(x)). The cap integral C_0 is negative; C_1 and A_0,A_1 are positive. Direct substitution x=gamma u gives

    B_0(gamma)=2 sqrt(gamma)/sqrt(abc)+O(gamma^(3/2)),
    B_1(gamma)=4 gamma^(3/2)/(3 sqrt(abc))+O(gamma^(5/2)).

The noncollapsed endpoint singularities are integrable. For finite nonzero m1,n2, the k=0 equation therefore forces n1 to grow as gamma^(-1/2), with positive leading coefficient. The product n1 B_1 tends to zero. The k=1 relation survives as

    m1 I_v=n2 I_u,                                         (A)

    I_v=integral_0^c sqrt(v/((a+v)(b+v)(c-v))) dv,
    I_u=integral_b^a sqrt(w/((a-w)(w-b)(c+w))) dw.

Consequently N=m1+n1 is unbounded. Holding DR's N equal to the finite surface-chain length is invalid. This is not a claim that every closed surface chain is approximated, at fixed axes, by periodic ambient billiards having fixed m1,n2. Such approximants are unnecessary for the sufficiency proof below; closure loci cannot be passed to a limit merely by continuity.

For a closed positively advancing surface chain of n full arcs and winding r, the surviving counts are

    m1=n,  n2=2r.

Each tropic encounter is one cap event in m1. The concurrent belt event is part of the divergent n1 count; a tropic's two-reflection convention does not double m1. The number n2 is a complete coordinate excursion/crossing count, not the number of individual monotone half-traversals. DR's proof counts it by crossings of x2=0. On the surface, its angular coordinate has two such crossings per turn; four quadrant traversals would overcount by two. This distinction fixes the factor in (A).

## Independent sufficiency check of the surface equation

Here is an explicit check that (A) is an actual two-way surface closure condition, rather than merely a necessary relation for possible ambient limits.

Let w(t)=a sin^2(t)+b cos^2(t), D=(a+c)(b+c). On the northern belt use 0<=v<=c and

    x=sqrt(a(a+v)/(a+c)) cos(t),
    y=sqrt(b(b+v)/(b+c)) sin(t),
    z=sqrt(c(c+w(t))(c-v)/D).

The southern formula uses -z. Substitution gives x^2/a+y^2/b+z^2/c=1. The two nonzero DR confocal coordinates are lambda1=-v and lambda3=w; their remaining surface coordinate is lambda2=0. This verifies the exact sign convention, including the opposite caustic-parameter sign in GKT.

The metric obtained by differentiation is

    g=(v+w)[ w/(c+w) dt^2
             -v/(4(a+v)(b+v)(c-v)) dv^2 ].                 (B)

The accompanying standard-library checker verifies the cleared polynomial identities for both diagonal terms, the zero cross term, and the squared scalar angular differential. These are generic identities, not checks restricted to samples.

Define

    S(t)=integral_0^t sqrt(w(s)/(c+w(s))) ds,
    tau(v)=1/2 integral_0^v sqrt(u/((a+u)(b+u)(c-u))) du,
    H=tau(c)=I_v/2,   L=S(2pi)=2 I_u.

For the equality L=2 I_u, w(t) runs between b and a once in each quadrant and dw/sqrt((a-w)(w-b)) has magnitude 2 dt. Set Y=H-tau(v) in the northern half and Y=-H+tau(v) in the southern half. Equation (B) is then a positive conformal multiple of dS^2-dY^2. The open belt is the cylinder (R/LZ) x (-H,H): uniqueness of v follows from strict monotonicity in v of

    (a+c)x^2/[a(a+v)] + (b+c)y^2/[b(b+v)]=1.

The coordinate glues across the equator because both signed z and Y have first-order dependence on sqrt(c-v). It extends continuously to the tropics, with tau(v)=O(v^(3/2)) there. Thus the prescribed switch between null families at a tropic is the reflected continuation of a line of slope dS/dY=+1 or -1. This does not extend a nonsingular Lorentz metric into the caps.

The surviving scalar differential in the DR quadrature is precisely x dx/sqrt(-xG(x)). Its magnitudes on lambda1=-v and lambda3=w(t) are 2 d tau and 2 dS respectively. Hence the scalar surface relation is the null equation dS=+/-dY, not an extra condition that could discard solutions.

Every positively advancing tropic-to-tropic arc traverses a vertical distance 2H and advances S by I_v. The angular period is L=2 I_u. A chain returns after n arcs with winding r if and only if

    n I_v=2r I_u,    n even.                              (C)

The parity is required to return to the same tropic and null-family state. Conversely these conditions close the reflected straight line for every starting point, proving sufficiency and the porism at once. No unverified ambient periodic approximants or elliptic torsion identification enters this argument.

GKT's equator-to-North-to-equator T also advances S by I_v. Thus T^k returns with winding r if and only if k I_v=2r I_u, with no full-arc parity requirement. To compare an odd k with the even m1 in an ambient or full-chain convention, use 2k full arcs and winding 2r; the scalar condition is unchanged. Least T-period further requires gcd(k,r)=1. For a full chain with rho=I_v/(2 I_u)=p/q in lowest terms, its least arc count is lcm(2,q).

## Comparison with the accepted candidate

The candidate uses the mean

    M=L/(2pi)=1/(2pi) integral_0^(2pi) sqrt(w(t)/(c+w(t))) dt.

Its verified contour identity is I_u+I_v=pi. The reconstruction above therefore has

    rho=I_v/(2 I_u)=1/(2M)-1/2,
    M=n/(n+2r).

The two parameter classifications coincide, including ordinary winding and the full-arc parity. Even before the contour simplification, (C) is already an explicit parameter-only, necessary-and-sufficient relation between finite integrals. The mean formula is a more economical presentation, not a different analytic classification. The candidate's literature section should acknowledge DR's express earlier claim and explain the reconstructed equivalence before any novelty promotion.

DR assumes a>b. Swapping a,b covers the other unequal ordering. The axial case a=b=A follows by the nonsingular metric/density formulas or their continuous limit: I_u=pi sqrt(A/(A+c)), I_v=pi(1-sqrt(A/(A+c))). The interval defining I_u collapses while its integrand becomes singular, so treating it as an integral over a zero-length interval would again be wrong. The criterion becomes c=A[(1+2r/n)^2-1]. This is a routine extension audited here, not a theorem explicitly covering equal axes in DR.

## Why the fixed-N Taylor/Pell limit does not supply (C)

For fixed j, with G(0)=abc,

    A_j(gamma)=[x^j] sqrt(G(x)(gamma-x))
       ~sqrt(abc) a_j gamma^(1/2-j),
    B_j(gamma)=[x^j] sqrt(G(x)/(gamma-x))
       ~sqrt(abc) b_j gamma^(-1/2-j).

For j>=1,

    a_j=-binom(2j,j)/((2j-1)4^j),
    b_j= binom(2j,j)/4^j.

These coefficients diverge at the Taylor center. For N=2m, the top square minor of the published even rank matrix uses indices 4+i+j, with size m-2. Diagonal row/column scaling has limiting matrix a_(4+i+j). For N=2m+1 the odd square minor uses b_(3+i+j), with size m-1. Their negatives/positives respectively are strictly positive moment matrices:

    -a_j=(1/pi) integral_0^1 t^(j-3/2)(1-t)^(1/2) dt,
     b_j=(1/pi) integral_0^1 t^(j-1/2)(1-t)^(-1/2) dt.

For every nonzero vector, the associated quadratic form integrates the square of a nonzero polynomial against a positive weight. Therefore both minors are nonsingular. For every fixed admissible finite N, the required rank defect is absent at sufficiently small positive gamma. The checker also confirms exact positive minors for sizes 1 through 10; the moment proof establishes all sizes.

The polynomial formulation exhibits the same obstruction. Write D3(s)=(s-1/a)(s-1/b)(s+1/c). Multiplying the even equation by gamma gives

    gamma p^2+(1-gamma s)s^2 D3 q^2=gamma;

a bounded-coefficient limit forces q to vanish. The odd equation becomes

    (gamma s-1)p^2-gamma s^2 D3 q^2=-gamma;

a bounded-coefficient limit forces p to vanish. Changing coefficient scales and degrees is essential, and N itself diverges. The vanishing caustic is Q0=E, a nondegenerate quadric but no genuine interior chord can be tangent to the strictly convex boundary. The quartic R_0=-xG(x) has four distinct roots 0,-c,b,a: its normalization is not singular. The broken assumptions concern the admissible billiard phase, the marked Taylor point, and the reflection count. They do not invalidate the separately checked scalar surface reconstruction.

## Evidence limits and disposition

- Printed fact: an explicit 2019 solution claim, ambient billiard criteria, and the indicated surface limit.
- Independently verified reconstruction: criterion (C), exact arc/winding conversion, necessity and sufficiency, equality with the accepted analytic candidate.
- Not recovered: a displayed n/r surface theorem in DR, the exact mean formula in that paper, a finite algebraic Cayley condition in a,b,c, or a global historical search proving who first wrote the exact mean presentation.
- Not asserted: that fixed-N rank tests survive gamma=0, that all closed surface chains arise as fixed-count periodic ambient approximants, or that the relevant third-kind periods are ordinary elliptic-group torsion.

A bare `already_solved` supported only by Remark 4.4 would not meet this project's verification policy. The full evidence bundle now supports `already_solved_analytic_via_verified_reconstruction`, with the explicit-printing limits stated. This rules out an unqualified claim of a new analytic solution mechanism on the present evidence. It leaves possible expository value and a stronger algebraic interpretation separate.

## Access, independence and reproducibility

Before candidate access, I read the DR primary source's introduction and Sections 2-4 through Remark 4.4, GKT introduction and Sections 4-5, and Tabachnikov Section 7. DR bibliography was also checked. After the independent checkpoint I read only the accepted ANALYTIC_CRITERION.md candidate and additional GKT Sections 2-3 excerpts for geometry checks. I did not open sibling reports, other-family conclusions, Wustholz/Tejada/Garcia/Bialy texts, or any queue/PR/editor/service state. A parent message subsequently requested that the independently identified quadrature route receive a sufficiency audit; it supplied no outside-family proof.

The three public URLs opened successfully. The local PDF and extraction inputs are hashed in MANIFEST.json. Broad first reads had extraction-output truncation; relevant formulas were reread in bounded ranges and visually checked. Visual QA inspected DR printed pp.5,6,10,12,13; GKT pp.16-18; and Tabachnikov p.62. An initial Tabachnikov render selected p.63 and was corrected. Temporary source-page images were deleted after inspection. No full source or source-page image is included in this audit's deliverables.

Run `python3 validate_reconstruction.py` from this folder. VALIDATION.json records its output. The first two execution attempts encountered unavailable SymPy in both system and bundled Python; the final checker was rewritten to use only the standard library and passed. The checker supplements the arguments; it does not replace the topology, parity, limiting estimates, or historical limits stated in this report.

Publication recommendation: close this candidate without a new research paper. This bounded audit demonstrates no novel mathematical contribution beyond the prior disclosed, now verified analytic mechanism. Retain the accepted derivation as an expository/audit artifact; do not create an immutable release on this evidence.
