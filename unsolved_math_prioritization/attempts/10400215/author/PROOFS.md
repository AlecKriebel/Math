# Shadow number and Gromov norm: scoped deductions

## Scope and notation

The target is Dylan Thurston's Conjecture 12.10 in Ohtsuki's problem collection, printed page 536 (PDF page 164). Its full heading is `Conjecture 12.10 (D. Thurston)`; the catalog title is truncated. In our notation it asks for universal positive a,b with a G(M) <= s(M) <= b G(M). Here s is the minimum number of true vertices of an ordinary shadow, and G is simplicial volume, not the Thurston norm of a second-homology class. No additive constant occurs.

We work with compact connected oriented 3-manifolds whose boundary is empty or a union of tori, the domain of the cited shadow-complexity theorems. The closed case is contained in the source context. We do not extend any theorem here to arbitrary nonorientable manifolds or arbitrary boundary. Write v3 and v8 for regular ideal tetrahedron and octahedron volumes, respectively, and a=v3/(2v8). Hyperbolic interiors have Vol(M)=v3 G(M). Ordinary, special, branched, stable-map, and four-dimensional shadow complexities must not be interchanged.

## Credited inputs

Costantino--Thurston [CT], Lemma 3.22, Corollary 3.28, Proposition 3.31, and Theorems 3.37 and 5.5 supply: subadditivity for connected sums and torus gluings; zero shadow complexity for graph pieces; and a G <= s <= C G^2 for a universal C>0 in the geometric class. Their definition of geometric uses decomposition into geometric pieces. All subsequent decomposition statements explicitly assume such a decomposition; no independent proof of geometrization is offered. Standard simplicial-volume additivity gives G(M)=sum G(H_i) over its hyperbolic pieces, as used in [CT, proof of Theorem 5.5].

For a closed oriented manifold with a branched special shadow P, n=c(P)>=1, Ishikawa--Koda [IK, v1 Proposition 5.1 and Lemma 5.3] give, when the minimum specified filling slope length L exceeds 2 pi,

    2 v8 n (1-(2 pi/L)^2)^(3/2) <= Vol(M).

Here L=min_R sqrt((2g_R)^2+k_R^2), g_R is the half-integral gleam, and k_R counts vertex passages with multiplicity. The cusps and lengths are exactly their octahedral-shadow construction. Hyperbolicity follows in this setting. These published/primary-preprint results are inputs, not results proved afresh here.

## 1. Decomposition-sensitive upper bound

Let H_1,...,H_r be the hyperbolic pieces after prime and JSJ decomposition of M. Set g_i=G(H_i), G=sum g_i, and B=max g_i, with B=0 for r=0. Then

    a G <= s(M) <= C sum_i g_i^2 <= C B G.

Proof. Build M from the pieces using connected sums and torus gluings. Subadditivity bounds its shadow number by the sum of those of its pieces. Each nonhyperbolic graph piece has shadow number zero; apply the quadratic bound separately to each H_i. Finally, g_i^2<=B g_i, and sum. The lower inequality is the credited universal lower bound. If there are no hyperbolic pieces, both the upper bound and s(M) are zero. No additivity of shadow complexity is assumed or proved.

Consequently, all manifolds with every hyperbolic piece of norm at most B0 obey s(M)<=C B0 G(M), regardless of the number of pieces, the gluing maps, or the size of the graph-manifold parts. In volume units, B0=V0/v3. This is a deduction from the credited proof, not a claim of historical novelty.

## 2. Exact reduction of the universal upper question

Within the above geometric class, a universal linear bound for finite-volume hyperbolic pieces, including both closed and torus-cusped cases, is equivalent to the universal linear bound for all M in the class.

Proof. Necessity is restriction to hyperbolic M. For sufficiency, suppose s(H)<=K G(H) for every hyperbolic piece H with the same K. Subadditivity and zero graph contributions yield s(M)<=sum s(H_i)<=K sum G(H_i)=K G(M). A theorem for closed hyperbolic manifolds alone is not silently substituted for the required cusped statement.

More quantitatively, when G(M)>0,

    s(M)/G(M) <= sum_i [g_i/G(M)] [s(H_i)/g_i]
                 <= max_i s(H_i)/g_i.

Thus if a sequence M_j had unbounded ratios, select a subsequence with ratios tending to infinity and choose H_j whose ratio is at least that of M_j. Since s(H_j)/G(H_j)<=C G(H_j), the selected hyperbolic norms, and hence volumes, tend to infinity. Merely increasing the number of bounded-volume pieces cannot produce this behavior. This is a necessary condition for a counterexample sequence, not construction of one.

## 3. Bounded families, fillings, and additive constants

On the subclass G(M)<=V, the quadratic theorem gives s(M)<=C V G(M). In particular, any family of Dehn fillings of finitely many fixed parents N_i has such a bound, taking V=max_i G(N_i), because simplicial volume does not increase under torus filling. This remains valid for exceptional nonhyperbolic fillings; if the norm becomes zero, the quadratic bound forces s=0. We assume the parents and fillings lie in the geometric domain above. Large surgery coefficients by themselves therefore cannot produce unbounded s/G in a fixed-parent family.

There is a useful integer gap requiring no numerical minimum-volume theorem. If G>0, then s>=aG>0 and s is integral, so 1<=s<=CG^2. Hence G>=C^(-1/2). Suppose one could establish s<=A G+D for universal nonnegative A,D. For G>0, D<=D sqrt(C) G, whence s<=(A+D sqrt(C))G. For G=0, already s=0. Therefore a universal affine upper bound is equivalent here to the desired homogeneous upper bound. This deduction does not establish either bound.

## 4. Long slopes: linear comparison and an exact integer threshold

Retain ALL the [IK] hypotheses above, and put f(L)=(1-(2 pi/L)^2)^(3/2). Since P is an ordinary shadow after forgetting its branching, s(M)<=n. Combining the credited lower volume estimate with the credited universal bound gives

    n f(L) <= Vol(M)/(2v8) <= s(M) <= n.

For a fixed L0>2 pi and every such P with L>=L0, this yields

    a G(M) <= s(M) <= [a/f(L0)] G(M).

The upper constant is independent of n and M, but depends on the imposed uniform slope lower bound. Existence of such a shadow for every hyperbolic manifold is not established.

Define, for each integer n>=1,

    L_*(n)=2 pi / sqrt(1-(1-1/n)^(2/3)).

If L>L_*(n), then f(L)>1-1/n. The displayed inequalities imply s(M)>n-1. Since s(M) is an integer and s(M)<=n, we get s(M)=n. The same argument, using s<=bsc=smc<=n from [IK, Theorem 2.2], gives bsc(M)=smc(M)=n. The conclusion thus concerns this explicitly restricted long-slope family.

A simpler sufficient condition is

    L >= 2 pi sqrt(3n/2).

Indeed, q=(2 pi/L)^2<=2/(3n)<1. Direct expansion gives

    (1-2/(3n))^3 - (1-1/n)^2 = (9n-8)/(27n^3) > 0.

Taking positive square roots shows f(L)>1-1/n, including n=1. This improves algebraically the convenient sufficient condition L>2 pi sqrt(2n) printed in [IK, v1 Theorem 5.2]. It is a consequence of their own volume estimate and integrality, not a new volume estimate or a novelty assertion. Moreover L_*(n)/(2 pi sqrt(n)) tends to sqrt(3/2), because [1-(1-x)^(2/3)]/x tends to 2/3 at x=0. Thus sqrt(3/2) is the asymptotic constant for this particular integer-rounding argument. We make no optimality claim about actual manifolds or endpoint equality L=L_*(n).

## 5. Two insufficient routes to the universal result

Theorem 5.4 of [CT] drills a suitable link from a hyperbolic M and supplies O(Vol(M)) tetrahedra. Their Theorem 4.2/Corollary 4.3 converts that triangulation to a shadow with O(t^2) vertices; filling adds no vertices. Composing these estimates is quadratic, not linear. A linear converter for the relevant triangulations would suffice. The existing converter does not provide one, and changing a surgery coefficient does not repair this exponent gap.

A different temptation comes from the quantum bounds in Belletti--Detcherry--Kalfagianni--Yang [BDKY, Corollary 3.11 and Remark 3.12]. Bounds Q<=K s and Q<=B G do not imply an upper bound on s/G, even if one adds Q=G. As an abstract logical countermodel, take G=m, s=m^2, Q=m for integers m>=1 and K=B=1. These inequalities, nonnegative integral s, a linear lower bound, and a quadratic upper bound all hold, yet s/G=m is unbounded. These are numerical symbols, not realizable 3-manifolds or a topological counterexample. A reverse estimate controlling s by Q, or another new construction, would be required.

## Remaining gap and disposition

Five bounded approaches produce the scoped deductions above and no universal upper constant, no topological counterexample, and no proof of present global openness. The target is UNSOLVED BY THIS ATTEMPT. The lower bound and several classes are already covered by prior literature. Our strongest explicit extra calculation is the sharpened long-slope integer threshold, under its full branchable-special-shadow hypotheses. The fresh independent audit is pending at author freeze.

## References

[O] T. Ohtsuki (editor), Problems on invariants of knots and 3-manifolds, Geometry & Topology Monographs 4, 377--572, published 2004 in the 2002 volume. https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf

[CT] F. Costantino and D. Thurston, 3-manifolds efficiently bound 4-manifolds, Journal of Topology 1 (2008), 703--745. Inspected author preprint arXiv:math/0506577v3, 17 July 2007. https://arxiv.org/abs/math/0506577 ; https://doi.org/10.1112/jtopol/jtn017

[IK] M. Ishikawa and Y. Koda, Stable maps and branched shadows of 3-manifolds, arXiv:1403.0596v1, 3 March 2014; later Math. Ann. 367 (2017), 1819--1863. Numbering above refers to the inspected v1, not a purported inspection of the published version. https://arxiv.org/abs/1403.0596 ; https://doi.org/10.1007/s00208-016-1403-4

[BDKY] G. Belletti, R. Detcherry, E. Kalfagianni and T. Yang, Growth of quantum 6j-symbols and applications to the volume conjecture, J. Differential Geometry 120 (2022), 199--229. https://par.nsf.gov/servlets/purl/10323860
