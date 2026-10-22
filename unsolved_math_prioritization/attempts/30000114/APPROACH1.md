# Approach 1: lattice hull, slicing, and the Ehrhart boundary deficit

Status: **partial progress; no proof or counterexample to the unrestricted question**.
Problem: rank 1217, corpus 30000114, OWR-741-008.
Prepared 10 October 2026 (UTC).

## 1. Exact target and conventions

For each fixed n, the question asks whether there is a finite c(n) such that every compact convex body K in R^n satisfies

    G(K) <= V_n(K) + V_{n-1}(K) + c(n) L_n(K),
    L_n(K) := sum_{i=0}^{n-2} V_i(K),
    G(K) := #(K intersect Z^n).

Both displayed leading coefficients must be 1. Intrinsic volumes have their usual Euclidean normalization: V_0=1 on a nonempty convex set, V_n is n-volume, and V_{n-1} is half the surface area for a full-dimensional body. Intrinsic volumes are unchanged by embedding in a larger Euclidean space. The coefficient c(n) may be assumed nonnegative. There is no symmetry, centering, or full-dimensional-lattice-hull assumption.

The source is Martin Henk's contribution to OWR 39/2004, printed p.2089, PDF p.23. Its question has been checked visually. The report records the full Wills inequality as established for n<=3 and false in sufficiently high dimensions. We do not claim those earlier results as new.

For n=1 the sum is empty and the target is simply G([a,b])<=b-a+1, which follows from the spacing of distinct integers. A singleton has the same bound. The remaining discussion concerns n>=2.

## 2. Exact reduction to lattice polytopes

Let K intersect Z^n be nonempty, and set P=conv(K intersect Z^n). Then P is a lattice polytope, P is a subset of K, and

    P intersect Z^n = K intersect Z^n.

The forward inclusion follows from P subset K; the reverse follows from the definition of the convex hull. Monotonicity of each intrinsic volume gives V_i(P)<=V_i(K). Thus an estimate with nonnegative coefficients for every lattice polytope P, including lower-dimensional ones, implies the target for every K. Bodies with no lattice points satisfy it trivially.

This is not a reduction to a centered polytope, nor is translating by an arbitrary nonlattice vector allowed in the lattice-polytope subproblem. The original translation freedom is already retained by taking the hull of the actual lattice points of K.

### 2.1 Lower-dimensional lattice hulls are controlled

We use the following established input from Henk--Wills, arXiv:0705.2088v1, Corollary 4.2, printed p.8. In every dimension d>=2 there is a finite beta_d, depending only on d, such that for every d-dimensional Euclidean lattice Lambda and convex Q whose Lambda-points span its ambient d-space,

    #(Q intersect Lambda)
      <= vol_d(Q)/det(Lambda)
         + beta_d V_{d-1}(Q)/D_{d-1}(Lambda),                 (2.1)

where D_{d-1}(Lambda) is the smallest covolume of a rank-(d-1) sublattice. Their surface-area coefficient has been absorbed into beta_d. Their published coefficient is not 1, so (2.1) alone does not resolve the n-dimensional target.

For any independent integer vectors b_1,...,b_r in R^n, the square of their r-dimensional parallelepiped volume is the positive integer det((b_i dot b_j)_{i,j}). Consequently every positive-rank sublattice of Z^n has covolume at least 1 in its span.

Suppose dim P=d<n. Translate by a lattice vertex and use Lambda=lin(P-P) intersect Z^n. If d>=2, (2.1) yields

    G(P) <= V_d(P) + beta_d V_{d-1}(P).                    (2.2)

If d=1, points on the induced lattice line have spacing at least 1, so G(P)<=V_1(P)+1. If d=0 then G(P)=1. When d=n-1, the leading V_d term in (2.2) is exactly the permitted V_{n-1} term; everything else has degree at most n-2. When d<=n-2, all terms are among L_n. Taking the maximum of the finitely many constants gives a constant depending only on n.

Therefore the remaining question is exactly a uniform estimate over **full-dimensional lattice polytopes**. No lower-dimensional-lattice-point case has been discarded.

## 3. A uniform result for bounded lattice width

This section proves a useful restricted theorem, with an explicit dependence on the allowed lattice width. It is a deduction using (2.1) and elementary slicing, not a claim of historical novelty.

For a primitive vector a in Z^n, define

    w_a(K) := max_{x in K} a dot x - min_{x in K} a dot x.

The units here are lattice layers: consecutive planes a dot x=j have Euclidean separation h=1/||a||. For n>=2 there is a constant A_n, independent of a and K, such that

    G(K) <= V_n(K) + V_{n-1}(K)/||a||
            + A_n (floor(w_a(K))+1) L_n(K).               (3.1)

In particular, for every fixed H<infinity, all convex bodies of lattice width at most H satisfy the requested inequality with

    c(n,H) = A_n (floor(H)+1).                            (3.2)

Because ||a||>=1, the surface coefficient in (3.1) is at most 1. Notice that (3.2) still depends on H; it is not the unrestricted c(n).

### 3.1 Uniform estimate inside one lattice layer

Set d=n-1, and let H_j={x:a dot x=j}, for an integer j. Primitivity of a ensures that H_j intersect Z^n is nonempty, and its difference lattice is

    Lambda_a = a-perp intersect Z^n,
    det(Lambda_a) = ||a||.                               (3.3)

For completeness, extend a basis b_1,...,b_d of the kernel of a:Z^n->Z by a vector z with a dot z=1. This is a Z-basis of Z^n, so its n-dimensional determinant has absolute value 1. The distance of z from a-perp is 1/||a||. Computing the determinant as base times height gives (3.3).

For any nonempty compact convex S in H_j, there is a constant A_n with

    #(S intersect Z^n)
       <= vol_d(S)/||a|| + A_n sum_{i=0}^{d-1} V_i(S).    (3.4)

If its lattice hull Q has dimension d>=2, use (2.1), (3.3), the fact D_{d-1}(Lambda_a)>=1, and monotonicity from Q to S. If d=1, the exact one-dimensional interval estimate gives (3.4) with A_2=1. If dim Q=q<d, Blichfeldt's classical estimate applied in the lattice span gives

    G(Q) <= q! V_q(Q)/det(Lambda_Q)+q <= q! V_q(S)+q

for q>=1. These are all lower-degree terms in (3.4). If q=0 there is at most one lattice point, covered by V_0(S); if Q is empty the count is zero.

For example, when n>=3 we may take

    A_n = max(1, beta_{n-1}, max_{1<=q<=n-2} q!,
                    max_{1<=q<=n-2} q),

with an empty maximum omitted. No numerical value of beta_d is required for the existence statement.

### 3.2 The one-dimensional quadrature fact

If f:R->[0,infinity) is compactly supported and all its strict superlevel sets are intervals, then for every h>0 and t_0 in R,

    h sum_{j in Z} f(t_0+jh) <= integral_R f(t) dt + h sup f. (3.5)

Proof: an interval I of length ell contains at most ell/h+1 points of the arithmetic progression t_0+hZ. Apply this to {f>u}, multiply by h, and integrate in u from 0 to sup f. Layer cake gives the integral and sum in (3.5). This proof allows closed endpoints and intervals of zero length, so lattice planes on the boundary are counted correctly.

### 3.3 Slicing proof

Write u=a/||a|| and

    f(t) = vol_{n-1}(K intersect {x:u dot x=t}).

For a full-dimensional K, the Brunn--Minkowski theorem in the section planes makes f^(1/(n-1)) concave on its support, so its superlevel sets are intervals. Also

    integral f = V_n(K),      sup f <= V_{n-1}(K),        (3.6)

where the second statement follows by intrinsic-volume monotonicity for each section. Apply (3.4) to the N lattice layers meeting K and use V_i(S)<=V_i(K). Summing and then using (3.5) with h=1/||a|| yields

    G(K) <= h sum_j f(jh) + A_n N L_n(K)
         <= V_n(K) + V_{n-1}(K)/||a|| + A_n N L_n(K).

Since N<=floor(w_a(K))+1, this is (3.1). For lower-dimensional K the same argument applies to the section superlevel sets. If dim K<n-1, every section has (n-1)-volume zero. If dim K=n-1 and its affine hull is not parallel to the section planes, every section again has (n-1)-volume zero. If K lies in one section plane, each nonempty positive superlevel set is a singleton. Thus the sharper coefficient 1/||a|| is retained in (3.1) in every case.

### 3.4 Hollow bodies and a necessary condition for failure

The classical flatness theorem says that, in fixed dimension n, every full-dimensional convex body with no interior lattice point has lattice width at most a finite flatness constant Flt(n). Applying (3.2) with H=Flt(n) proves the desired form uniformly for this hollow class. The original input can also be used in its strictly lattice-point-free formulation: Banaszczyk--Litvak--Pajor--Szarek, Proposition 2.3 and the first part of Theorem 2.4 (preprint pp.8--9), bound that width by a finite dimension-dependent constant. If K has no interior lattice points, choose x_0 in int K and apply the bound to K_epsilon=x_0+(1-epsilon)(K-x_0), which is contained in int K. Its lattice width is exactly (1-epsilon)lw(K), so letting epsilon decrease to zero proves the hollow formulation. This works for arbitrary translations. Lower-dimensional lattice hulls are covered separately by Section 2.1; no full-dimensional flatness theorem is being applied to an irrational lower-dimensional set. No assertion about the optimal value of Flt(n) is needed.

Consequently, if the unrestricted inequality fails in a fixed dimension, there must be a sequence of full-dimensional lattice polytopes P_m for which

    [G(P_m)-V_n(P_m)-V_{n-1}(P_m)] / L_n(P_m) -> +infinity

and their minimum lattice widths tend to infinity. Otherwise a bounded-width subsequence would contradict (3.2). More directly, (3.1) bounds the positive quotient by A_n(lw(P_m)+1).

## 4. What the Ehrhart boundary term does and does not prove

For a full-dimensional lattice polytope P, write

    G(kP)=sum_{i=0}^n g_i(P) k^i,  k in Z_{>=0}.

The leading terms are

    g_n(P)=V_n(P),
    g_{n-1}(P)= (1/2) sum_{facets F} vol_{n-1}(F)/||a_F||,  (4.1)

where a_F is the primitive outward integer normal. Thus

    Delta(P):=V_{n-1}(P)-g_{n-1}(P)
       = (1/2) sum_F (1-1/||a_F||) vol_{n-1}(F) >=0.       (4.2)

These are classical Ehrhart facts, present in the retained Henk--Wills and Betke--Boroczky sources. The exact target on P is equivalent to

    sum_{i=0}^{n-2} g_i(P) <= Delta(P)+c(n)L_n(P).          (4.3)

The nonnegative Delta must not simply be thrown away.

For each **fixed** P, putting

    c(P)=max(0, max_{0<=i<=n-2} g_i(P)/V_i(P))

gives a finite bound along all integer dilates. This does not make c(P) independent of P. If Delta(P)>0, the negative term -Delta(P)k^{n-1} eventually dominates all terms of lower degree, so sufficiently large integer dilates even satisfy the full Wills bound with coefficient 1 on every intrinsic volume. If Delta(P)=0, every facet normal is one of the signed coordinate vectors, so P is an axis-aligned lattice box. Such boxes satisfy equality in the full Wills bound. Thus testing larger dilates of a single fixed polytope cannot establish the needed uniformity or disprove the weakened statement.

## 5. An exact obstruction to coefficientwise lower-order control

A tempting strengthening would be g_i(P)<=C(n)V_i(P) for each i<=n-2. It is false even in dimensions where the full Wills inequality holds.

For n>=3, put d=n-1 and let L be a positive integer. Consider the height-one pyramid

    P_L = conv( ([0,L]^d x {0}) union {e_n} ).

It has the inequality description

    z>=0,  x_i>=0,  x_i+Lz<=L   (1<=i<=d).

The condition z<=1 follows from the displayed inequalities. At integer height z in kP_L, the x-section is [0,L(k-z)]^d. Therefore, exactly,

    G(kP_L)=sum_{j=0}^k (Lj+1)^d.                         (5.1)

Faulhaber's identity gives

    g_n(P_L)     = L^d/n,
    g_{n-1}(P_L) = L^d/2 + L^{d-1},
    g_{n-2}(P_L) = (d/12)L^d + (d/2)L^{d-1}
                                + (d/2)L^{d-2}.         (5.2)

The enclosing orthotope [0,L]^d x [0,1] has

    V_{n-2} = d L^{d-1} + binom(d,2)L^{d-2}.

Monotonicity gives the same expression as an upper bound for V_{n-2}(P_L). Hence

    g_{n-2}(P_L)/V_{n-2}(P_L)
      >= [(d/12)L^d+(d/2)L^{d-1}+(d/2)L^{d-2}]
                   /[d L^{d-1}+binom(d,2)L^{d-2}]
      ~ L/12 -> infinity.                               (5.3)

This rules out the coefficientwise route, in every n>=3.

### 5.1 Why this is not a counterexample to the target

The base of P_L has d-volume L^d. Each of its d coordinate side facets has d-volume L^{d-1}/d. Each of the other d facets has d-volume L^{d-1}sqrt(1+L^2)/d. Thus

    V_{n-1}(P_L)= (1/2)[L^d+L^{d-1}(1+sqrt(1+L^2))],
    Delta(P_L)= (1/2)L^{d-1}(sqrt(1+L^2)-1) ~ L^d/2.       (5.4)

The large coefficient in (5.3) is accompanied by a surface deficit of the same high order. Indeed G(P_L)=(L+1)^d+1, and

    [G(P_L)-V_n(P_L)-V_{n-1}(P_L)] / L^d -> -1/n.         (5.5)

So the uncorrected leading two terms alone dominate G(P_L) for large L. In n=4 specifically,

    g_2=L^3/4+3L^2/2+3L/2,      V_2(P_L)<=3L^2+3L,

while sqrt(1+L^2)>=L bounds the target's residual from above by

    -L^3/4+(5/2)L^2+3L+2.

This polynomial is negative for every L>=12: substituting L=12+t gives

    -t^3/4-(13/2)t^2-45t-34.

The example must therefore be labeled a counterexample to an auxiliary coefficient bound, never a counterexample to weakened Wills.

## 6. Relevant prior asymptotics and the remaining gap

Betke--Boroczky, *Asymptotic Formulae for the Lattice Point Enumerator*, Canadian Journal of Mathematics 51 (1999), 225--249, DOI 10.4153/CJM-1999-012-9, proves:

- Theorem A, p.226: the lattice-surface leading error with O(lambda^{n-2}) for dilates of a fixed lattice-facet polytope. Its implied constant may depend on the fixed polytope.
- Theorem B, p.227: the corresponding o(lambda^{n-1}) error for shapes converging to a fixed full-dimensional body.
- Theorem D, p.228: for any family with inradius tending to infinity, a mixed-volume upper bound plus o(surface area). Taking its auxiliary body to be the Euclidean ball of radius 1/2 gives |G(P)-vol(P)|<=V_{n-1}(P)+o(surface(P)).

Theorem D also permits the crosspolytope C=conv{+/-e_i/2}, because h_C(v)=||v||_infinity/2>=1/2 for primitive integer v. Its leading mixed-volume term is

    (1/2) integral_{boundary P} ||u(x)||_infinity dS(x),

which is at most V_{n-1}(P). If the average gap between ||u||_infinity and 1 stays positive, this supplies asymptotic room below the desired surface coefficient. It gives no quantitative O(L_n(P)) remainder, and makes no assertion when the inradius stays bounded. In particular, an o(surface) term cannot be silently replaced by a constant times the lower intrinsic volumes. Unbounded lattice width does not imply that the Euclidean inradius tends to infinity, even for lattice polytopes. For an exact example, let Q_m={(x,y):0<=y<=m, 0<=x-my<=m}. This is the unimodular shear of [0,m]^2, so lw(Q_m)=m. Its two pairs of parallel supporting lines have Euclidean separations m and m/sqrt(1+m^2); hence its inradius is m/(2sqrt(1+m^2))<1/2. In dimension n>=2 the product Q_m x [0,m]^(n-2) has the same inradius and lattice width m. These families must not be discarded on the basis of a large-width argument.

The actual Berg--Henk paper arXiv:1505.06444v1, Proposition 1.1 and Theorems 1.1--1.2, has been inspected. It controls centered bodies through their first successive minimum, with sharper simplex/planar conclusions. It does not give the target estimate for arbitrary translated bodies.

The residual problem is the shape-uniform bound (4.3) in each fixed dimension over full-dimensional lattice polytopes of unbounded lattice width, retaining the compensation Delta(P). Neither the fixed-polytope Ehrhart expansion, the known asymptotic results, nor the bounded-width argument supplies that bound. No rigorous counterexample to (4.3) has been found in this approach.
