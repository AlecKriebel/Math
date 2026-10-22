# Independent audit of the finite-measure estimate for three-dimensional Klein sails

Date: 2026-10-11. Scope: Aggarwal--Andritsch, arXiv:2608.05853v1, Theorem 3.3's finiteness assertion, Proposition 5.1's upper bound, Proposition 6.2, and the upper-bound dependencies in Sections 6--11. This authored report is AI-assisted. The cross-section construction and the connection to Karpenkov's relative frequencies are established in the companion [REDUCTION_AUDIT.md](REDUCTION_AUDIT.md). This measure report does not audit the lower bound.

## Result

The displayed argument in Sections 9--11 contains real errors, including an impossible step in Lemma 9.5 and a false inclusion (11.6) for the sets as literally defined. These are not merely extraction artifacts: the relevant PDF pages were rendered and inspected.

Nevertheless, the upper-bound mechanism can be reconstructed. With the level-k set defined by the first-contact conditions and with the right-Haar disintegration explained below, the following bound holds for almost every unimodular planar lattice L:

    integral_{r>0} Leb(F^{(k)}_{sqrt(r)L}) dr/r
        <= 1080 sqrt(3) H_{k-1}/[k(k-1)]       (k >= 2).

The constant is smaller than the constant printed in Proposition 6.2. For k=1 the same integral is at most 3 sqrt(3). Therefore the sum over all k is finite. The derivation below replaces the defective steps; it does not certify the printed proof word for word.

The non-elementary import still used is White's 1964 Theorem 2. Its statement and the precise parameter substitution were checked in the original publisher PDF, including visual inspection of p.390. White's proof itself was not independently re-proved. The primitive-triangle and reduced-basis facts are proved below by elementary fundamental-parallelogram arguments; Haar disintegration is justified explicitly. The all-lattices exceptional-boundary part of Lemma 9.2 is not needed and is not certified here.

The required identification of the cross-sectional measure mu_C with a fixed positive multiple of right-Haar measure restricted to the affine-lattice first-contact set is established in [REDUCTION_AUDIT.md](REDUCTION_AUDIT.md), Sections 3--5, including the explicit group isomorphism and slice calculation in Section 4. That accompanying AI-assisted reduction audit checks the geometric dependency. The combined target reconstruction is complete relative to the stated established White theorem and standard Haar facts; White's full proof and the entire source manuscript are not certified here.

## Inputs and evidence

Frozen main input:

- Title: Generalised Gauss--Kuzmin Distribution for Klein sails in R^3.
- Authors: Gaurav Aggarwal and Konstantin Andritsch.
- Version: arXiv:2608.05853v1, 50 pages.
- Public identifier: https://arxiv.org/abs/2608.05853v1
- PDF bytes: 677535.
- PDF SHA-256: b8ef367b1561fff377b7678c81547ab4201dd74888bd1a0f8b4b80cef3e41ef1.
- The supplied PDF and extraction were read without modification.
- Rendered and inspected main-paper pages: 37, 40, 44; pages 39--45 also rendered for equation review.

External theorem input:

- G. K. White, Lattice Tetrahedra, Canadian Journal of Mathematics 16 (1964), 389--396, Theorem 2 on p.390.
- DOI: https://doi.org/10.4153/CJM-1964-040-2
- Publisher PDF: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/636DC00E906DE4E640AB27580B9E90D3/S0008414X00035495a.pdf/lattice_tetrahedra.pdf
- Retrieved on 2026-10-11; 569338 bytes; SHA-256 4efca38f39c3f2b95035e900337265d30df6cc0cd941615d8c7f65815cef9d00.
- The publisher PDF was downloaded after the web-open route timed out. Page 2, printed p.390, was rendered and inspected. This is a primary-source theorem check, not reliance on a search-result paraphrase.
- The White PDF and all source-page renderings are excluded source inputs; only their public identifiers, sizes, hashes and inspection metadata accompany this packet.

The Kannan--Lovasz covering-radius import in Section 7 was located bibliographically but its PDF could not be read through the web tool. It is NOT used in the reconstructed proof: the level-one determinant bound below eliminates that dependency entirely.

## 1. Precise planar problem and measure

Let v_1,v_2,v_3 be the unit normals in Section 9, so v_1+v_2+v_3=0 and distinct normals have scalar product -1/2. Put

    T = {x : v_i.x > -1/sqrt(2), i=1,2,3}.

This is an open equilateral triangle of area A_T=3 sqrt(3)/2. Let L be a full planar lattice and b a class modulo L. The relevant level-k condition is:

1. For every integer 1 <= ell < k, (L+ell b) has no point in ell * closure(T).
2. (L+k b) intersect kT contains three affinely independent points.

Condition 2 implies that a primitive lattice triangle can be selected from these points. In particular, its two edge differences form a basis of L. Thus no ambiguous use of the phrase 'generates the lattice' is needed. Conversely, a witnessing basis triangle certainly gives affine rank two. Boundary distinctions in condition 1 do not obstruct the upper bound: excluding the closed triangles is stronger than excluding their interiors.

For H=GL_2(R) semidirect R^2 with multiplication (A,b)(C,d)=(AC,b+Ad), right Haar measure in matrix-and-translation coordinates is

    dA / |det A|^2 times db.

Indeed, right multiplication scales four-dimensional matrix Lebesgue measure by |det C|^2 and leaves the translation Jacobian equal to one, up to a triangular shear. The denominator cancels exactly. This checks that the translation fiber uses ordinary Lebesgue measure, not probability-normalized db/det A.

After restricting to positive determinant representatives and quotienting by SL_2(Z), write A=sqrt(r) A_0 with det A_0=1. Haar measure on GL_2^+(R) disintegrates, up to a fixed normalization, as

    dr/r times dm_X2(A_0).

Consequently, if F^{(k)}_L is the level-k subset of a measurable fundamental domain for L,

    m_Y2(C_H^{(k)})
       = integral_X2 integral_{r>0} Leb(F^{(k)}_{sqrt(r)L}) dr/r dm_X2(L),

after choosing compatible normalizations. An unspecified fixed multiplicative normalization does not affect finiteness or the asymptotic upper bound.

## 2. Level one: avoid the Section 7 import

Suppose b has level one for sqrt(r)L, with covolume(L)=1. Choose three noncollinear points of sqrt(r)L+b inside T. The determinant of their difference vectors is a nonzero integer multiple of r. On the other hand, the triangle they span lies in T, so that determinant is at most 2 area(T)=3 sqrt(3). Hence

    r <= 3 sqrt(3).

The entire translation fiber has Lebesgue measure r. Therefore

    integral Leb(F^{(1)}_{sqrt(r)L}) dr/r
       <= integral_0^{3 sqrt(3)} r dr/r = 3 sqrt(3).

This is uniform in L and uses neither Lemma 7.2 nor Kannan--Lovasz. The paper's displayed final numerical bound '<=4' on p.29 does not follow from its preceding statement lambda_2 >> 1; only an unspecified absolute bound follows there.

## 3. Primitive triangles and generic reduced minima

### 3.1 Primitive triangles in convex lattice sets

A bounded convex set containing three noncollinear lattice points contains a primitive lattice triangle. Choose a lattice triangle of minimum positive area inside the set. If its two difference vectors generated a sublattice of index greater than one, their fundamental parallelogram would contain another lattice point. Either that point or its reflection in the parallelogram center lies in the triangle and produces a strictly smaller positive-area lattice triangle. This is a contradiction.

A useful strengthened form is: if a convex set contains a primitive lattice segment [P,P+x] and a point Q off its line, it contains a point R such that (x,R-P) is a lattice basis. In coordinates with x=(1,0), write Q-P=(a,m), m>0. At height one, the triangle's horizontal interval is [a/m, 1+(a-1)/m]. It contains an integer: this follows immediately on reducing a modulo m. That point gives determinant one. The case m<0 is obtained by reversing the transverse coordinate.

### 3.2 Work on a full-measure set of lattices

Exclude lattices with a nonzero lattice vector perpendicular to one of v_i. This is a countable union of codimension-one conditions in lattice coordinates and is Haar null. Scaling preserves this exclusion. On the remaining set every nonzero lattice vector has nonzero scalar products with all v_i, so it belongs to exactly one of the six open sign cones.

This is the appropriate condition for uniqueness of the maxima in (9.7). The condition written in Remark 9.3, L intersect R v_i={0}, does not itself express uniqueness of the support projections; perpendicular lines are the relevant ones. Both conditions are generic, but they should not be conflated.

Let K_i be the cone where the i-th scalar product is negative and the other two are positive. A lattice meets each K_i; for example, approximate points going far out along an interior ray by points in a bounded lattice fundamental domain. The portion of K_i with its i-th scalar product bounded below is bounded. Hence there is a unique lattice vector rho_i in K_i maximizing that negative scalar product.

### 3.3 The zero-sum identity

Consider rho_1+rho_2. Its third scalar product is positive. It cannot lie in K_1, since its first scalar product would be strictly greater than that of rho_1, contradicting maximality. It cannot lie in K_2 for the analogous reason. Thus it lies in -K_3, and -(rho_1+rho_2) is a candidate in K_3.

If rho_1+rho_2+rho_3 were nonzero, uniqueness would give three strict cyclic inequalities

    v_i.rho_i > v_i.(-rho_j-rho_l).

Summing them gives a quantity strictly greater than itself, because v_1+v_2+v_3=0. Therefore rho_1+rho_2+rho_3=0.

### 3.4 The missing basis justification

Every rho_i is primitive, since a proper positive fraction of it in L would be a better candidate in K_i. More importantly, any two rho_i form a basis, a fact used without a proof in Lemma 9.5.

Write the three support coordinates of rho_1 as (-A,B,C) and of rho_2 as (D,-E,F), with A,B,C,D,E,F all positive. Then rho_3=(A-D,E-B,-C-F). If rho_1,rho_2 generated a proper sublattice, their half-open fundamental parallelogram would contain a nonzero point w=t rho_1+u rho_2 of L with 0<=t,u<1. Its third support coordinate is tC+uF, strictly between zero and C+F. If w is in K_1, its first coordinate -tA+uD is greater than -A, contradicting rho_1's maximality. If w is in K_2, its second coordinate tB-uE is greater than -E, contradicting rho_2's maximality. The remaining possibility is w in -K_3; then -w has third coordinate greater than -C-F, contradicting rho_3's maximality. The genericity assumption excludes zero support coordinates. This proves that rho_1,rho_2 form a basis, and the zero-sum relation gives the other pairs. No Minkowski theorem is required.

There are at most 12 unordered bases selected from the six signed vectors: choose any two and discard the three opposite pairs.

## 4. Repaired witness-selection lemma

Let D be a translate and positive homothety of T and suppose D intersect L contains three affinely independent points. We prove it contains a basis triangle whose two edges are signed reduced minima.

Start with any primitive triangle P_1,P_2,P_3 in D. Reorder two vertices so P_2-P_1 belongs to K_i. Put x=rho_i. The point P_1+x is in D: for the i-th inequality its projection is no smaller than that of P_2; for each other inequality its projection is no smaller than that of P_1.

Use the primitive-segment result in Section 3.1 to obtain, inside D, a basis triangle P,P+x,P+w. Choose another reduced minimum y. Since (x,w) and (x,y) are both bases, replacing y by the third reduced minimum if necessary gives

    w=n x-y,  n an integer.

There are only three coefficient cases:

- n=0: the original edges x,-y are already reduced.
- n>=1: B=P+n x lies in D. For the i-th normal its value is at least that of P+w, since v_i.y>=0. For either other normal it is at least that of P, since those projections of x are nonnegative. Also B-x lies on [P,B] and is in D. The triangle B, B-x, P+w has edges -x,-y.
- n<=-1: C=P-y lies in D. For either normal other than i, C=(P+w)-n x has projection at least that of P+w. For the i-th normal, -v_i.y >= v_i.x, because x+y+z=0 with v_i.z>=0; hence C has projection at least that of P+x. The triangle P,P+x,C has reduced edges x,-y.

All comparisons preserve the strict inequalities defining D. This proves the generic version of Lemma 9.5 sufficient for integration.

### Why this is a repair, not a restatement

Lemma 9.5's printed Case 4 asks for 1<=n'<=n so that

    -y+(n-n')x belongs to K_j union K_l,  j,l different from i.

For generic reduced minima this is impossible: its i-th projection is strictly negative, and its y-index projection is strictly positive. It can lie only in K_i or -K_y, never either of the requested positive cones. For a concrete check in projection coordinates, take x=(-2,1,1), y=(1,-2,1), P=0 and w=2x-y. Then w belongs to K_1, but w-x=(-3,3,0) and w-2x=(-1,2,-1) belong to neither K_2 nor K_3. A sufficiently large translated T contains 0,x,w. The preceding three-case argument replaces the defective step.

## 5. Arithmetic restrictions: checked application of White

Let the level-k witnesses be

    P_1=c_1 a+c_2 b, P_2=P_1+a, P_3=P_1+b,

where (a,b) is a basis. If nonnegative integers d_1,d_2,d_3 have positive sum ell<k and satisfy

    ell c_1+d_2 = 0 mod k,
    ell c_2+d_3 = 0 mod k,

then (d_1P_1+d_2P_2+d_3P_3)/k belongs to L intersect (-ell b_translation+ell T). Indeed, after adding ell b_translation it is ell/k times a convex combination of the three level-k interior witnesses. This contradicts first contact.

If m=gcd(c_1,k)>1 and q=k/m, choose

    ell=k-q,
    d_2=0,
    d_3=(q c_2 mod k),
    d_1=ell-d_3.

Since d_3 is a multiple of q at most k-q, these are nonnegative and give an obstruction. Thus c_1 is a unit modulo k; similarly c_2 is a unit. The paper writes m>=1 when it needs m>1 here.

Suppose also that none of c_1+1,c_2+1,c_1+c_2 vanishes modulo k. Apply White's Theorem 2 with parameters (a,b,c,d)=(1,c_1,c_2,k). All three required pair sums are nonzero modulo k. It gives u with

    0 < {u/k}+{u c_1/k}+{u c_2/k} <= 1.

Choose u in {1,...,k-1}; the strict lower inequality excludes u=0 mod k. Put r_i=(u c_i mod k), and set

    ell=k-u,
    d_2=r_1, d_3=r_2,
    d_1=k-u-r_1-r_2.

These are a forbidden obstruction. This also clarifies a variable-name collision in the paper: the sum of the displayed d_i is k-u, not u. Consequently

    gcd(c_1,k)=gcd(c_2,k)=1,
    c_1=-1 or c_2=-1 or c_1+c_2=0  (mod k).

White's theorem is correctly applicable. Its proof is an imported published result, not something certified by the finite computational checks.

## 6. A valid finite configuration cover

For each of the at most 12 original reduced bases, the arithmetic condition gives three ordered-basis families. They may be taken as

    (a,b), (b,a), (b-a,-a).

For the third family relabel P_2 as the origin witness: its coefficients in (b-a,-a) are (c_2,-c_1-c_2-1). Hence the second coefficient is -1 modulo k. The transformed pairs need not themselves be reduced; the analytic estimate below works for any basis, so this causes no problem.

Reduce the first coefficient modulo k to a unit c in {1,...,k-1}, and the second to -1. If the original witness differs from the normalized one by kq with q in L, replace the translation by b_translation+q. This preserves level and represents the same translation class.

For each ordered pair (a,b) and unit c, define the normalized witness points

    P_1=(c a-b)/k,
    P_2=((c+1)a-b)/k,
    P_3=c a/k.

Use the set of translations satisfying BOTH the normalized witness conditions and the first-contact exclusions. Call this set B_tilde. It is bounded. The projection of all such sets to the torus covers the actual level-k fiber. Quotient projection cannot increase their Lebesgue measure. All covering statements used for an upper bound are inequalities, not disjoint-union equalities.

This corrects two printed problems: the B and B-bar definitions omit the level restriction later invoked, and p.40 changes the witness coefficient -1 to k-1 without simultaneously translating the Q-points. The normalized formula above is used consistently throughout this reconstruction.

## 7. Farey competitors and three separate support cuts

Choose q in {1,...,k-1} to be the inverse of c modulo k, and put

    p=(q c-1)/k,
    q'=k-q,
    p'=c-p.

Then p/q<c/k<p'/q', with differences 1/(kq) and 1/(kq') respectively. These are the adjacent fractions in order k; only the displayed identities and denominators below k are needed. Define

    Q_R=(p'/q') a,
    Q_L=(p/q) a,
    Q_3=(c a-b)/(k-1).

Each competitor is in (1/ell)L for an ell<k and is therefore forbidden at a level-k translation. Set

    D(S)=intersection_{s in S}(-s+T),
    nu_i(S)=max_{s in S}(-v_i.s).

Then

    B_tilde subset D(P) minus union_j D(P union {Q_j}).

Let x_i=v_i.a and y_i=v_i.b. If Q_R strictly increases the i-th support threshold, direct subtraction from the three P_j gives

    x_i<0, -x_i>q' y_i, (q'-1)x_i>q' y_i.

In particular y_i<0. If Q_L increases it, then

    x_i>0, x_i>q y_i.

If Q_3 increases it, then

    y_i>c x_i, y_i>(c-k+1)x_i,

so y_i>0. Thus a right cut and a left cut cannot affect the same normal; a right cut and the third cut cannot affect the same normal. A left and third cut at the same normal would give y_i>c x_i>c q y_i with y_i>0 and cq>=1, an impossibility.

If any competitor increases no normal, its triangle already contains D(P) and the remainder is empty. Otherwise each of the three cuts increases exactly one normal and the three normals are distinct. Let their positive increases be delta_R,delta_L,delta_3. The same subtractions give

    delta_R <= -x_{j_R}/(kq'),
    delta_L <=  x_{j_L}/(kq),
    delta_3 <=  y_{j_3}/[k(k-1)].

These denominators correct the interchange of k' and k'' in the printed Lemma 11.1/11.2. Their product is unchanged, but individual inequalities as printed need not hold.

## 8. A stronger normalization bound

Put

    alpha = sum_i nu_i(P)
          = (1/k) sum_i max(0,-x_i,-y_i),
    M=max_i(max(|x_i|,|y_i|)).

Since sum_i x_i=sum_i y_i=0,

    sum_i max(0,-x_i) >= max_i |x_i|,
    sum_i max(0,-y_i) >= max_i |y_i|.

Consequently alpha>=M/k>0. With beta_j=delta_j/alpha, the support bounds imply

    0<beta_R<=1/q',
    0<beta_L<=1/q,
    0<beta_3<=1/(k-1).

This improves the factors 2 in the paper. It is useful because it more than compensates for the factor 2 missing in the paper's harmonic summation.

## 9. Radial integration, independently recomputed

For any finite S,

    Leb(D(S))=A_T [1-(sqrt(2)/3) sum_i nu_i(S)]_+^2.

To check this directly, its defining thresholds are v_i.z>nu_i(S)-1/sqrt(2). Their sum determines the homothety ratio; the center has projections nu_i(S)-(1/3)sum_j nu_j(S). The area formula then follows. This avoids the shifted-vertex mistakes in the proof of Lemma 10.1.

Under radial scaling by t=sqrt(r), all support values scale by t. Three distinct cuts give, by inclusion-exclusion, the area factor

    A_T * [ (1-C alpha t)_+^2
            - sum_i (1-C(alpha+delta_i)t)_+^2
            + sum_{i<j}(1-C(alpha+delta_i+delta_j)t)_+^2
            - (1-C(alpha+delta_1+delta_2+delta_3)t)_+^2 ],

where C=sqrt(2)/3. The pairs are unordered. The expression vanishes for t below 1/[C(alpha+sum delta_i)] and above 1/(C alpha). At the lower range the three removed triangles cover the original triangle; equivalently the coordinate upper bounds imposed by avoiding all three cuts have negative sum.

Using dr/r=2 dt/t, integrate the displayed expression. The antiderivative after substituting u=1-C a t is

    -u(u+2)/2 - log(1-u).

The polynomial terms cancel in the alternating sum. This gives exactly

    integral Leb(remainder_{sqrt(r)}) dr/r
      = -3 sqrt(3) log R,

    R = [(1+beta_1+beta_2)(1+beta_2+beta_3)(1+beta_3+beta_1)]
        /[(1+beta_1+beta_2+beta_3)(1+beta_1)(1+beta_2)(1+beta_3)].

The identity

    1-R = beta_1 beta_2 beta_3 (2+beta_1+beta_2+beta_3)
          /[(1+sum beta_i) product_i(1+beta_i)]

was checked by exact symbolic expansion. In particular 0<R<1. Applying -log(1-z)<=z/(1-z), and using that each beta_i<=1, gives

    integral Leb(B_tilde_{sqrt(r)}) dr/r
       <= 3 sqrt(3) beta_1 beta_2 beta_3 (2+sum beta_i)
       <= 15 sqrt(3) / [(k-1)q(k-q)].

This computation validates the intended cancellation mechanism. The p.44 sums written i!=j must be i<j; otherwise every pair is counted twice and the displayed product/log expression does not follow.

## 10. Summation and finiteness

As c runs over units modulo k, q=c^{-1} does also. Thus

    sum_{c unit} 1/[q(k-q)]
       <= sum_{q=1}^{k-1} 1/[q(k-q)]
       = 2 H_{k-1}/k.

The factor 2 is essential. For k=2 the left sum is 1, whereas H_1/2=1/2, so the paper's displayed step on p.45 is false as stated.

There are at most 12 reduced bases and three ordered configurations for each. Therefore

    integral Leb(F^{(k)}_{sqrt(r)L}) dr/r
       <= 12 * 3 * 15 sqrt(3) * 2 H_{k-1}/[k(k-1)]
       = 1080 sqrt(3) H_{k-1}/[k(k-1)].

Since 1080<12*9*64=6912 and H_{k-1}<=log(k)+1, this is stronger than the numerical constant printed in Proposition 6.2, on the full-measure set of lattices under consideration. Integrating over the probability space X2 and using k(k-1)>=k^2/2 gives

    m_Y2(C_H^{(k)}) <= 2160 sqrt(3) (log(k)+1)/k^2,

up to the fixed Haar normalization. Together with the k=1 estimate and convergence of sum_k (log(k)+1)/k^2, this establishes the required planar finite measure.

Exceptional lattices were excluded on a Haar-null subset of X2, invariant under radial scaling. Their product with the radial and translation variables is null by Tonelli on countable bounded boxes. No conclusion about their pointwise radial bound is needed. Thus this proves the almost-everywhere estimate sufficient for Proposition 5.1's upper-bound/finiteness use, without certifying the stated all-A pointwise scope of Proposition 6.2.

## 11. Defect ledger and disposition

1. Section 6.3, k=1, p.29: the stated numerical <=4 does not follow from lambda_2 >>1. Replaced by the uniform determinant bound 3 sqrt(3).
2. Lemma 8.1, pp.31--32: a mistyped P_3 expression, m>=1 instead of m>1 in the contradiction, and reuse of ell where the new coefficient sum is k-ell. Application and conclusion checked after explicit variable correction.
3. Remark 9.3, p.34: the genericity condition for unique support maxima concerns perpendiculars to v_i. Replaced by an explicit Haar-full set.
4. Lemma 9.5, p.36: the basis property of pairs of reduced minima is used without justification. Supplied by the fundamental-parallelogram contradiction in Section 3.4.
5. Lemma 9.5, p.37, Case 4: the claimed cone membership after subtracting a reduced vector is impossible in the generic sign configuration. Replaced by the three integer-coefficient cases in Section 4 of this report.
6. Section 10.1, pp.37--38: the translation-equivariance sign for C(S-p) and the displayed vertex thresholds are inconsistent with D(S). The center formula and area statement can be checked directly from support inequalities; only the corrected area statement is used.
7. Section 11.1, pp.39--40: witness-set definitions omit the first-contact restriction later asserted. As written (11.6) is false: take a tiny basis and translation zero, so the three witnesses fit inside kT although the level is one, while the competitor zero removes that translation. Replaced by B_tilde including the missing restriction.
8. Section 11.1: inconsistent normalization shifts/signs, including -1 versus k-1 and different relabeled basis pairs. Replaced by a consistent torus projection cover and explicit ordered pairs.
9. Lemma 11.1 and 11.2: denominators for the right/left Farey competitors are interchanged. Corrected individually; their symmetric product is unaffected.
10. Section 11.3, p.43: the sign displayed for the forbidden-point scalar product does not match the defining inequalities. Corrected via the sum of the three coordinate upper bounds.
11. Section 11.3, p.44: the pair sums must be over i<j, not i!=j, and (11.21) is reused as notation for its radial integral. Integral recomputed independently.
12. Section 11.3, p.45: the harmonic sum loses a factor 2, and set-cover inequalities are written as equalities. Both corrected. A stronger normalization estimate absorbs the constant loss and proves a bound below the printed constant.

These defects do not constitute a counterexample to the asserted finite measure. They do mean that treating the paper's upper estimate as already audited merely because its final series converges would be unjustified.

## 12. Exact audit boundary

Checked or reconstructed:

- Right-Haar density and radial/translation disintegration on the affine-lattice side.
- The first-contact planar interpretation, with the required geometric identification established by the accompanying AI-assisted reduction audit in REDUCTION_AUDIT.md, Section 4.
- A uniform level-one bound independent of covering-radius theory.
- Generic reduced minima, their zero-sum relation and basis property.
- Generic reduced witness selection, replacing the faulty printed Case 4.
- White theorem parameter substitution and the entire residue-obstruction argument.
- Configuration count and normalization modulo the lattice.
- Three-competitor support inequalities and their distinct-normal property.
- The radial integral, algebraic cancellation, stronger beta bounds, harmonic summation, and convergence.

Imported rather than re-proved in full:

- White, Theorem 2; original statement inspected and hypotheses checked.
- Standard Haar measure on the finite-volume unimodular lattice space X2 and its normalization to a probability measure.

Not certified by this report:

- The source's Sections 2--4 as a whole. The required cross-section existence, local embeddedness, local Haar disintegration and face stabilizer/comparison factors are reconstructed in REDUCTION_AUDIT.md, Sections 3--5. Generic ergodic frequency identification remains outside this packet's acceptance scope.
- The exceptional all-lattices version of Lemma 9.2 or Proposition 6.2.
- Any lower bound in Proposition 5.1, Proposition 6.3 or Theorem 3.3.
- The full proof of White's theorem or the Kannan--Lovasz import, which was avoided.
- An exact canonical multiplicative normalization for mu_C versus m_Y2.

## 13. Verification checks

The independently authored verification code uses exact rational/symbolic arithmetic where indicated. Every logical check uses an always-active `require` function, not Python `assert`. Normal, -O and -OO runs give identical outputs; a deliberate failing-check control exits nonzero in all three modes. The code and failure controls are excluded from this public packet; [VERIFICATION_METADATA.json](VERIFICATION_METADATA.json) records their aggregate results:

- Exact symbolic product/log identity and antiderivative checks.
- Farey identities for 3043 unit residues with 2<=k<=100.
- Harmonic identity for 2<=k<=100.
- 73809 residue pairs through k=60 checked against the no-earlier-level obstruction.
- 11931 random integer-coordinate basis configurations, including 882 with all three active support cuts, checked with exact rational arithmetic against the corrected support inequalities and beta bounds.
- Four high-precision numerical radial-integral checks, with absolute discrepancies below 1.2e-46.

These tests are useful error detectors; the general proof is the argument above, not an extrapolation from finite tests. No source-author code was used. The mathematical review was AI-assisted, with no independent human referee review or proof-assistant formal verification.
