# Independent final derivations and scope falsifiers

Checked 2026-10-01 04:54:09 UTC. These certify the accepted input-dependent bound and falsify tempting weakenings. They are audit artifacts, not new results or additions to the canonical candidate.

## 1. Complete threshold certificate, including arbitrary real coefficients

Let S be a normal finite-type complex algebraic klt surface and D1,...,Dr actual effective Cartier divisors. Let w,fj be nonnegative and set aj=integral(w fj), assumed finite. Finite linearity gives

    I(F)=sum_j aj ord_F(Dj)=ord_F(B),  B=sum_j aj Dj.

Choose a log resolution pi:Y->S of S and the finite union of the supports of all Dj. Include every exceptional component and every strict transform in a finite list Ei. Write Ai=A_S(Ei)>0 and mi=ord_Ei(B)>=0. If B is nonzero, some strict transform has mi>0. Thus

    c=min_{mi>0} Ai/mi

is finite and positive, even when the aj and mi are arbitrary real numbers. At this c, the crepant boundary on Y has coefficients 1-Ai+c mi<=1. Its support is SNC. A further point blowup at q<=2 boundary components produces coefficient sum gamma_i-1<=1; away from the boundary it produces -1. Every further surface prime valuation is obtained by finitely many point blowups, so all log discrepancies remain nonnegative. Negative crepant coefficients cause no failure. Hence (S,cB) is lc. An Ei realizing the minimum has zero discrepancy at c and negative discrepancy at every larger parameter, so c is exactly lct(S;B). Consequently

    Kopt=max_i mi/Ai=1/c,

and the global supremum is attained. Applying the same argument to each nonzero Dj gives ord_F(Dj)<=A_S(F)/cj. Nonnegative aj permit summation, yielding K0=sum aj/cj. No threshold-addition rule is involved.

If B=0, the least nonnegative constant is 0. When the problem asks for K>0, 1+K0 is valid; a least strictly positive constant need not exist in that zero case. The candidate correctly calls Kopt the least nonnegative constant.

## 2. Compact chamber and endpoint certificate

Put H=-K_X and tau=sup{u>=0:H-uS is pseudo-effective}. The openness of ampleness gives tau>0. Intersecting with H^2 gives

    0<=H^3-u(S.H^2),  hence tau<=H^3/(S.H^2)<infinity.

BCHM's published Corollary 1.3.2 applies to the smooth Fano pair (X,0), so X is Mori dream. A finite closed rational-polyhedral cone is described by finitely many rational linear inequalities. Its intersection with the rational affine line H-uS therefore has a rational finite endpoint. On a smooth Fano variety Pic_Q=N1_Q; a rational point of the effective rational-generator cone is a nonnegative rational combination of its effective generator classes. This constructs a Q-effective G with G~_Q H-tau S. This is genuine Q-linear effectivity, not merely a numerical limiting assertion.

If G=bS+G' with b>0, then G'~_Q H-(tau+b)S is effective, a contradiction. Choose A~_Q H effective and avoiding S. For u in [0,tau], (1-u/tau)A+(u/tau)G is effective and avoids S. At rational u, clearing denominators gives a member of a multiple of the complete system avoiding S, so its normalized fixed coefficient along S vanishes. Okawa's finite closed chambers and Q-linear negative maps extend this to every real u in the interval.

On each chamber, N is an effective divisor supported on finitely many exceptional primes of the associated contraction. Finitely many contractions yield a finite support union on X. Uniqueness of the normalized fixed part makes the maps agree on rational overlaps; the overlaps are rational polyhedral, so real extensions agree as well. Compactness then gives bounded piecewise affine coefficients, including every wall and the endpoint. P=H-uS-N is likewise piecewise affine as a numerical class. Its fixed intersection square with S is piecewise quadratic and bounded. All aj are finite.

For a negative prime E different from integral S, smoothness of X makes E Cartier, and its local defining equation has a nonzero image in the local domain of S. This is a nonzerodivisor. It therefore defines the actual effective Cartier divisor E|S; reducibility and multiplicity of that restriction must be retained. A disjoint E gives zero, which may be discarded.

## 3. Fresh geometry check of the nonzero Fano example

Let L=(x0=x1=0) in P3. The blowup X is the closure of the graph of [x0:x1], realized by the incidence equation t1 x0=t0 x1 in P3×P1. This gives the combined closed embedding underlying ampleness: if H is the first projection's hyperplane pullback and F=H-E the second projection's fiber class, then -K_X=3H+F is the restriction of ample O(3,1). Hence X is smooth Fano. The exceptional-fiber curve and a strict transform of a line meeting L impose respectively the nef inequalities b>=0 and a-b>=0 for aH-bE, confirming that H and H-E generate the nef cone.

The exceptional divisor E=P(N_L/P3)=P1×P1 has H|E=O(1,0) and E|E=O(1,-1); consequently H3=1, H2E=0, HE2=-1, E3=-2, and (4H-E)^3=54. A fiber S is the strict transform of a plane through L. Blowing up the plane along its Cartier line changes no plane, so S=P2. Restricting gives H|S=h and E|S=C, an actual reduced line.

Every nonexceptional prime comes from a degree-d hypersurface with multiplicity m along L, where 0<=m<=d. Its class is d(H-E)+(d-m)E. Thus the effective cone has generators E,H-E and

    D(u)=(4-u)H+(u-1)E=(4-u)(H-E)+3E,
    tau=4.

For 0<=u<=1 the divisor is 3H+(1-u)(H-E), nef and basepoint free after clearing rational denominators. For 1<=u<=4, the exceptional-fiber intersection forces (u-1)E as a fixed coefficient. A section of the residual multiple of (4-u)H avoiding L has no extra E component, so the coefficient is exactly u-1. Thus N=(u-1)E, P=(4-u)H on that piece, and N=0 before the wall. At tau, G=3E avoids S. The wall restrictions agree at 3h; the endpoint has P=0 and weight zero, while N is finite.

The nonzero integral is

    a=integral_1^4 (4-u)^2(u-1)/18 du=3/8.

Since C is smooth, lct(S;C)=1 and lct(S;(3/8)C)=8/3. K0=Kopt=3/8, attained by the surface prime C. At a point outside C the local constant is zero for every admitted center containing that point; the same zero constant fails globally at C. This confirms both endpoint and local/global conventions.

`verification/check_exact_examples.py` ran successfully. Its arithmetic results are reproduced in the final report; the geometric argument above, not the script alone, verifies the Fano test.

## 4. Scope falsifiers and limiting cases

| Tempting weakening or mistaken inference | Checkable failure / boundary test | Candidate status |
| --- | --- | --- |
| Replace actual divisor equality by linear or numerical equivalence | On P2, two lines are linearly equivalent. A line through P has order 1 at the blowup of P; a line avoiding P has order 0. | Explicit actual-divisor equality prevents this. |
| Use point-local thresholds at every center | A smooth line C in P2 and P outside C have local threshold infinity. Global F=C has order 1 and discrepancy 1, so the local zero contribution cannot bound it. | Local-center condition is explicit. |
| Admit only centers equal to P while assuming curve attainment | For B=C through P, repeated blowups along C yield order n and discrepancy n+1, approaching ratio 1 without any such valuation attaining it. C itself attains 1 and its center contains P. | Candidate uses centers containing P and global attainment. |
| Drop klt to lc | The cubic elliptic cone x3+y3+z3=0 has vertex blowup discrepancy 2-3=-1, log discrepancy 0. The Cartier section x=0 has exceptional order 1. No finite K can bound 1 by K*0. | Du Val/klt hypothesis restored. |
| Ignore restriction multiplicity | On xy=z2, x=0 is Cartier but equals 2L for L=(x=z=0). Vertex blowup yields exceptional order 1, log discrepancy 1; strict L has order 2, log discrepancy 1, so lct=1/2. | Cartier divisor, including multiplicities, is retained. |
| Exclude strict transforms from the resolution minimum | A smooth curve D on a smooth surface has lct 1, realized by D. The single point blowup has ratio 2 and gives the wrong answer if used alone. | Strict transforms are explicitly included. |
| Multiply the threshold inequality by negative integrated weights | With w=-1, f=1, D a smooth curve and interval length 1, proposed K0=-1. At a point blowup on D, I=-1 but K0*A=-2, so the asserted inequality fails. Clipping w to 0 repairs it. | Nonnegative setup and signed clipping are distinguished. |
| Assume finite support can be omitted | Let Ln=(x=n) on A2. On disjoint intervals of lengths 2^-n totaling 1, take N(u)=2^(2n)Ln and w=1. F=Ln has integrated order 2^n and discrepancy 1. No finite K works. | MDS finite-support mechanism supplies the missing premise. |
| Require rational real-boundary thresholds | B=sqrt(2)C for smooth C has threshold 1/sqrt(2), attained at C. | Candidate correctly permits real coefficients and claims no rationality. |
| Let E=S or let S be reducible | E=S restricts its defining equation to zero, giving no effective Cartier divisor. For reducible S, E unequal to the total S may still contain a component. | Prime/integral S and endpoint exclusion close this gap. |
| Extend S-exclusion to negative u | On Bl_p P3, with S=E, D(u)=4H-(2+u)E has fixed E coefficient -2-u for u<-2. | Candidate restricts every claim to [0,tau]. |
| Infer a universally useful K-stability bound | The finite K depends on the weighted actual divisor B; finiteness does not force K below any stability criterion. | Candidate expressly disclaims this inference. |

Additional zero/limit checks: empty family, D_j=0, a_j=0, N identically zero, and weights vanishing almost everywhere yield B=0. Scaling B by t>0 scales Kopt by t and divides the threshold by t. Letting t decrease to zero gives Kopt to zero and lct to infinity; the zero convention is consistent. For transverse half-weight smooth curves B=(C1+C2)/2, SNC gives lct=2 and Kopt=1/2, whereas K0=1. For two tangent unit-weight curves y=0 and y=x2, the two blowups give (A,m)=(2,2),(3,4), so lct=3/4 and Kopt=4/3 while K0=2. These tests falsify threshold additivity and verify that interaction terms are recognized by the common resolution.

## Primary references for geometric bridges

- BCHM, published Corollary 1.3.2: https://www.ams.org/journals/jams/2010-23-02/S0894-0347-09-00649-3/S0894-0347-09-00649-3.pdf . The indexed published primary text was verified; direct PDF retrieval returns 403. The early arXiv version numbers the same Fano/MDS corollary 1.3.1: https://arxiv.org/pdf/math/0610203 . This does not impeach the candidate's published numbering.
- Okawa, https://arxiv.org/pdf/1104.1326v2 , Lemma 2.7, Proposition 2.8, Remark 2.12 and Proposition 2.13, printed pp.5–7: finite closed chambers; exceptional support; fixed-part uniqueness; Q-linear decomposition, including chamber boundaries.
