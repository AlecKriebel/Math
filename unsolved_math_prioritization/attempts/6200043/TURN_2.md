# Recovery proof turn 2: coarse subgroup models and finite algebraic covers

2026-10-03. Recovery turn 2/5; historical count unknown. Original unresolved. Completion estimate 15% (subjective approach coverage).

The first turn leaves arbitrary nonporous images open. This turn tests whether a quasi-isometric self-embedding can be reduced to a subgroup, including embeddings that are not homomorphisms. The outcome is a precise positive class and an explicit missing reduction.

## Theorem A: subgroup-like images

Let G be a non-elementary hyperbolic group whose boundary attains its finite Ahlfors regular conformal dimension. Let F:G→G be a quasi-isometric embedding. If F(G) is at finite Hausdorff distance from a subgroup H≤G, then F is coarsely onto.

Proof. A quasi-isometric embedding of a geodesic hyperbolic Cayley graph has quasiconvex image: join any two preimages by a geodesic; its image is a uniform quasi-geodesic, and the hyperbolic stability theorem places the target geodesic within a uniform neighborhood of that image. Mapping vertices only is sufficient after interpolating consecutive images by uniformly bounded geodesics. The assumed Hausdorff bound then makes H quasiconvex. Quasiconvex subgroups of finitely generated hyperbolic groups are finitely generated, and their intrinsic word metrics are quasi-isometric to their induced ambient metrics. Thus H is quasi-isometric to G. The boundary identification is quasisymmetric for visual metrics. If H had infinite index, Carrasco–Mackay Proposition 8.4 would make its limit set porous, while Proposition 8.3 would contradict equality of its attained conformal dimension with that of ∂G. Hence H has finite index, so H and F(G) are both coarsely dense in G. QED.

The core no-quasiconvex-copy statement is already Carrasco–Mackay Corollary 8.5, whose proof even explicitly permits quasi-isometric rather than isomorphic subgroups. The finite-Hausdorff-distance formulation is a routine extension proved above. It is not claimed new.

## Theorem B: finite cover by small quasiconvex algebraic pieces

Assume additionally a chosen Ahlfors Q-regular representative X of ∂G realizes the conformal dimension Q>0. There is no quasi-isometric embedding F:G→G whose image is contained in a fixed-radius neighborhood of a finite union

  g_1 H_1 ∪ ... ∪ g_m H_m,

where all H_i are infinite-index quasiconvex subgroups and g_i∈G.

Proof. Each ΛH_i is porous in a visual boundary by Carrasco–Mackay Proposition 8.4. The boundary action of g_i and the change to X are quasisymmetric; porosity is preserved by their Lemma 8.2. Thus each compact set E_i=g_iΛH_i is porous in X. In an Ahlfors Q-regular space a uniformly porous subset has Assouad dimension strictly below Q (the David–Semmes result used in Proposition 8.3). Elementary subgroups cause no difficulty: empty or at-most-two-point limit sets have Assouad dimension zero, and Q>0.

A finite union E=∪E_i has Assouad dimension max_i dim_A E_i<Q. To verify the finite-union assertion without a hidden common-center assumption, cover each E_i∩B(x,R) using the doubling/Assouad estimate centered at any chosen point of that nonempty intersection, with radius 2R, then sum the finitely many cover bounds. The reverse inequality is monotonicity.

The limit set Y=∂F(∂G) lies in E. Indeed take any sequence F(x_n) tending to a boundary point, choose uniformly close points of the union, then pass to a subsequence with a fixed index i. Bounded-distance sequences have the same boundary limit, which belongs to g_iΛH_i. Compactness of each E_i makes the conclusion valid for every such limit.

Thus dim_A(Y)<Q. Y is uniformly perfect and quasisymmetric to X. The same regularization theorem used by Carrasco–Mackay Proposition 8.3 implies ARCdim(Y)≤dim_A(Y): apply the theorem for every exponent strictly larger than dim_A(Y) and take an infimum. This contradicts ARCdim(Y)=ARCdim(X)=Q. QED.

## Limitations found by this approach

An arbitrary quasi-isometric embedding is not known to be at finite Hausdorff distance from a subgroup, or to admit a finite cover of the stated kind. Quasi-convexity of a subset is not the same as being a quasiconvex subgroup: cocompact group action on its convex hull was essential in Proposition 8.4. Replacing 'subgroup' by 'quasiconvex subset' in that proposition would beg the source problem.

The finite-union hypothesis is substantive. No uniform dimension gap follows for an arbitrary countable union with worsening porosity constants. Nor does the argument address distorted subgroup embeddings that are not quasi-isometric. Abstract co-Hopficity, commensurable co-Hopficity, quasi-isometric co-Hopficity and boundary QS co-Hopficity must remain distinct.

This turn therefore excludes finite algebraic-envelope routes to a counterexample but does not settle arbitrary self-embeddings of the source boundary.
