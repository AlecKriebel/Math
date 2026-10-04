# Function Theory 5.70: componentwise obstructions and construction controls

Problem ID: **2305070 / AMR-022-5070**. Status: **unsolved**. This is a partial-results report, not a solution or a novelty claim.

## 1. Exact target and conventions

Hayman–Lingham, Problem 5.70, asks: “Can one construct a bounded analytic function with an unbranched level set component of infinite length?” The domain is the open unit disc D. The background example of Barth and Clunie has branching. The 2018 update reports no progress. See SOURCE_GATE.md for the dated, limited literature check.

We require a nonconstant holomorphic function F on D, a positive number c, and a connected component C of {z in D: |F(z)|=c}, such that C is unbranched and its Euclidean one-dimensional Hausdorff measure is infinite. Zero-level sets are discrete for nonconstant F, and constant functions are excluded. Length of the whole level set, hyperbolic length, length counting repeated traversal, and length of a union of components do not satisfy the target.

All statements proved below are auxiliary results. None proves existence or nonexistence of the required C.

## 2. Local branching and regular levels

**Lemma 1.** At a point p with |F(p)|=c>0, the level set is unbranched if and only if F'(p) is nonzero. Every positive level is locally of finite length. Except for at most countably many c, every component of the positive level c is unbranched.

**Proof.** Choose a local holomorphic logarithm h of F. Write

    h(z)-h(p) = (z-p)^m a(z),  a(p) != 0.

After choosing an analytic m-th root of a in a small disc, the coordinate w=(z-p)a(z)^(1/m) is conformal at p. The level is exactly Re(w^m)=0. It consists of 2m rays, paired into m analytic arcs. There is branching precisely when m>1, equivalently h'(p)=F'(p)/F(p)=0. In a sufficiently small closed coordinate disc these arcs have finite Euclidean length, because the derivative of the inverse coordinate is bounded. Compact subsets of D admit finite covers of such neighborhoods; neighborhoods disjoint from the level contribute nothing. Thus the level is locally of finite length. Finally, the zeros of F' are a discrete, at most countable set, unless F is constant. Their positive |F|-values form an at most countable exceptional set. Outside it the first assertion applies everywhere. QED.

At a simple critical point the normal form is Re(w^2)=0. Changing the level to Re(w^2)=epsilon reconnects the four local arms in one pairing for epsilon>0 and the other pairing for epsilon<0. This removes the crossing locally. It does not preserve which remote arms lie in the same connected component.

**Consequence.** No infinite-length component can be contained in a compact subset of D. A compact unbranched component is a smooth circle and has finite length. If F is zero-free in D, no compact unbranched component can occur: a global logarithm exists, and its real part would be constant on a Jordan curve and therefore throughout its bounded interior by the maximum principle, forcing F to be constant by analytic continuation.

## 3. Explicit regular infinite-total-length countercontrol

**Proposition 2.** There is a bounded zero-free F, with bounded reciprocal and F' nowhere zero, such that {|F|=1} has infinite total Euclidean length, but every connected component has finite length.

**Construction and proof.** Put

    W(z)=(1+z)/(1-z),   G(z)=exp(-W(z)),   F(z)=exp(G(z)).

The map W is a conformal bijection from D onto {x+iy:x>0}. Hence 0<|G|<1 and e^(-1)<|F|<e. Also

    F'(z)=-F(z)G(z) * 2/(1-z)^2 != 0.

The equation |F|=1 is Re(G)=0, which in W-coordinates is

    e^(-x) cos(y)=0,  x>0.

Consequently the components are exactly the inverse images of the horizontal half-lines y=b_k, where b_k=pi(k+1/2), k an integer. To see that these are components rather than merely subsets, the continuous y-coordinate sends every connected subset of their union into the discrete set {b_k}; its image is a singleton. Each individual half-line is connected.

The inverse Cayley map is Z(w)=(w-1)/(w+1). The length of component k is

    L_k = integral_(0,infinity) 2/((x+1)^2+b_k^2) dx
        = 2 arctan(|b_k|)/|b_k| < infinity.

For k>=0 we have b_k>=pi/2>1, so arctan(b_k)>=pi/4 and

    L_k >= 1/(2k+1).

The sum over k>=0 diverges. The components are disjoint Borel sets, so countable additivity of Hausdorff measure gives infinite length of the full level. Individual lengths are finite. Their common limiting boundary point 1 is not in D and does not join them. QED.

This example refutes the proposed inference “remove critical levels, then use infinite total length.” It does not refute the original existence question.

## 4. Algebraic length bound: finite rational mechanisms cannot work

**Lemma 3 (elementary Crofton bound).** If P(x,y) is a nonzero real polynomial of total degree d, the one-dimensional length of {P=0} intersected with D is at most pi*d.

**Proof.** Replace P by its square-free part, which does not change the zero set and cannot increase degree. Away from finitely many singular/intersection points its one-dimensional part consists of smooth algebraic arcs. Exhaust these arcs by compact regular subarcs. For such a finite disjoint collection E, the planar Crofton formula is

    length(E) = (1/2) integral_(0,pi) integral_R N_E(theta,t) dt dtheta,

where N counts intersections with the line x cos(theta)+y sin(theta)=t. The formula follows by integrating the variation of orthogonal projections along the arcs: the integral of |cos(theta-alpha)| over theta in [0,pi] is 2. For almost every line, the restriction of P to that line is a nonzero univariate polynomial of degree at most d, hence has at most d zeros. Lines contained in the algebraic set form a measure-zero exceptional family. Lines meeting D have |t|<1. Thus length(E)<=pi*d. Monotone exhaustion gives the claimed bound for all regular arcs; isolated and singular points have zero length. QED.

**Corollary 4.** If R=P/Q is a nonconstant rational function, holomorphic on D, and max(deg P,deg Q)<=n, then for every c>0,

    length({|R|=c} intersect D) <= 2*pi*n.

The same bound holds for {Re R=c}, for every real c, and therefore for each modulus level of exp(R).

**Proof.** The first level lies in the real polynomial zero set |P|^2-c^2|Q|^2=0. The second lies in Re(P conjugate(Q))-c|Q|^2=0. Each polynomial has degree at most 2n. Neither vanishes identically, by the open mapping theorem and nonconstancy of R. Apply Lemma 3. QED.

The conclusion includes exp(R) with essential boundary singularities caused by boundary poles of R. Essential singularities alone are therefore not a construction mechanism.

## 5. Conformal and covering routes

The theorem of Hayman and Wu [HW81, Theorem 1, p. 366] gives a universal finite length bound for the inverse image of a line or circle under a univalent function on D. It is a cited theorem, not reproved here.

Thus the following approaches cannot produce the target:

- taking F itself univalent;
- taking F=exp(h) with h univalent and Re h bounded above, since {|F|=c}=h^(-1)({Re w=log c});
- the analogous exp(i h) construction with h univalent.

“Locally univalent” cannot replace “univalent” in this invocation; Proposition 2 has F' nowhere zero but infinite total level length.

The simplest infinite covering also fails explicitly. For a>0 set S_a(z)=exp(-a W(z)). For 0<c<1, set s=-log(c)/a>0. Its modulus-level component is the inverse image of the entire vertical line Re w=s. Its Euclidean length equals

    integral_R 2/((s+1)^2+y^2) dy = 2*pi/(s+1).

It is a circle minus its boundary point 1, and S_a' never vanishes. The covering winds infinitely often in its image while the Euclidean length remains finite. In particular, infinite covering degree or infinite hyperbolic length does not settle the target.

## 6. Infinite Herglotz superpositions: exact tail controls, missing connectivity

Let zeta_j be points of the unit circle and a_j>0 with A=sum_j a_j<infinity. Define

    H(z)=sum_j a_j (zeta_j+z)/(zeta_j-z),
    H_N(z)=sum_(j<=N) a_j (zeta_j+z)/(zeta_j-z),
    S(z)=exp(-H(z)).

These formulas provide a bounded zero-free analytic S. Indeed,

    Re H(z)=sum_j a_j (1-|z|^2)/|zeta_j-z|^2 > 0,

and the series is locally uniformly convergent. With T_N=sum_(j>N) a_j, for 0<r<1,

    sup_(|z|<=r) |H-H_N| <= ((1+r)/(1-r)) T_N,
    sup_(|z|<=r) |H'-H_N'| <= 2 T_N/(1-r)^2.

**Proof.** Use |zeta+z|<=1+r, |zeta-z|>=1-r, and

    d/dz ((zeta+z)/(zeta-z)) = 2*zeta/(zeta-z)^2.

The Weierstrass convergence theorem justifies differentiation on compact subsets. The displayed real-part identity follows by multiplication by conjugate(zeta-z). QED.

For a fixed s>0, {|S|=exp(-s)} is exactly {Re H=s}. At any point of this level where H' is nonzero it is unbranched. Except for countably many s, this holds for the full level (unless H is constant, which must separately be excluded). For finitely many distinct atoms H_N is rational of degree at most N, so Corollary 4 gives total length at most 2*pi*N.

The tail estimates make persistence of each fixed compact regular arc accessible to the implicit-function theorem. They do not prove that a selected arc can be extended into arbitrarily many outer shells at the same level s, with divergent accumulated length. Adding atoms can change remote pairings and can create new components instead of lengthening the old one. No sequence (a_j,zeta_j) with the required single-component property has been constructed in this attempt. This is the exact remaining gap in this route.

## 7. Prescribed geometry and limits

### 7.1 An embedded infinite-length analytic arc exists geometrically

For t>=2 put

    gamma(t)=1-1/t + i*sin(t^2)/t.

Its real coordinate is strictly increasing, so it is injective. Its derivative has real part 1/t^2>0, so it is regular. Moreover

    |gamma(t)|^2 = 1-2/t+(1+sin(t^2)^2)/t^2 < 1,

and gamma(t) tends to 1. The arc has infinite length. To prove this, take t_n=sqrt(pi/2+n*pi), n>=1. Then the imaginary coordinates alternate between +1/t_n and -1/t_n. The sum of the lengths of successive chords is at least

    sum_(n>=1) (1/t_n+1/t_(n+1)) = infinity,

since t_n is of order sqrt(n).

Around every finite parameter t_0, the holomorphic function gamma(w)=1-1/w+i*sin(w^2)/w has nonzero derivative. A local holomorphic inverse psi exists. The function exp(i psi(z)) has nonzero derivative there and its modulus-one level contains the corresponding piece of the arc. On a sufficiently small relatively compact neighborhood it is bounded.

This proves local analytic realizability, not realizability by one bounded analytic function on all of D. The local inverses do not supply the necessary global bounded analytic continuation. No global harmonic function with bounded real part, zero set containing the whole arc, and nonzero gradient along it is provided here.

For clarity, bounded harmonic functions do furnish a sufficient subclass: if u is real harmonic and bounded on D, choose its harmonic conjugate v and put F=exp(u+i v). Then F and 1/F are bounded, {|F|=1}={u=0}, and F' vanishes precisely where grad u vanishes. The converse holds for zero-free F with bounded reciprocal. This equivalence does not establish the needed harmonic function for gamma.

### 7.2 Compact convergence can lose arbitrarily large regular level length

Put a_n=exp(-n^2) and

    F_n(z)=exp(z^n-a_n).

The functions are uniformly bounded by e on D and converge locally uniformly to the constant 1. Yet their modulus-one levels are regular and have total lengths tending to infinity.

Indeed, {|F_n|=1} is Re(z^n)=a_n. The vertical open chord {a_n+i t: |t|<sqrt(1-a_n^2)} in the w-disc avoids zero. Its inverse image under z^n consists of n disjoint analytic arcs. On each, F_n' is nonzero, since its only possible critical point is z=0, which is not on the level. The arc passes through radius a_n^(1/n)=exp(-n), and both ends tend to radius 1. Its length is at least 2(1-exp(-n)), by total radial variation. Thus total length is at least 2n(1-exp(-n)), tending to infinity. Every finite-stage level has finite length by Corollary 4.

The limiting constant has no admissible one-dimensional level component. Therefore neither Montel compactness nor finite-stage length growth, even with finite-stage regularity, is enough. An actual construction must preserve a nonconstant normalized limit and the membership of all length-forcing pieces in one selected regular component.

## 8. Exact unresolved obligation

No complete solution is asserted. To obtain a positive answer one must construct a single nonconstant bounded F and one fixed positive c, prove that one maximal connected component of {|F|=c} contains a sequence of disjoint or ordered pieces whose lengths force divergence, and prove absence of critical points on that entire component. The controls above each isolate a failure mode, but none supplies those simultaneous global properties. A negative answer would require a componentwise rectifiability theorem for all bounded analytic functions, beyond the univalent and finite rational cases addressed here.

## References

- [HL18] W. K. Hayman and E. F. Lingham, Research Problems in Function Theory (New Edition), arXiv:1809.07200, Problem and Update 5.70, printed p. 111. https://arxiv.org/abs/1809.07200
- [BC82] K. F. Barth and J. G. Clunie, A bounded analytic function in the unit disk with a level set component of infinite length, Proc. Amer. Math. Soc. 85 (1982), 562–566. DOI: https://doi.org/10.1090/S0002-9939-1982-0660605-9 . The full proof was not accessible in this check; no reconstruction of it is claimed.
- [HW81] W. K. Hayman and J.-M. G. Wu, Level sets of univalent functions, Comment. Math. Helv. 56 (1981), 366–403. Theorem 1. https://doi.org/10.1007/BF02566219 . Author-uploaded text: https://www.researchgate.net/publication/226448362_Level_sets_of_univalent_functions
- [NR21] A. Nicolau and A. Reijonen, A characterization of one-component inner functions, Bull. London Math. Soc. 53 (2021), 42–52, first online 2020, final discussion. https://doi.org/10.1112/blms.12395
