# Finite-volume Palm cells and obstructions for infinite-volume cells

Problem 30006510 / OWR-14299586-001. Research date: 3 October 2026.

## Disposition and scope

**The original problem remains unsolved after five substantive approaches.** This note gives rigorous partial results and identifies what several plausible extensions actually define. It does not claim a natural scalar cell intensity and a count-typical full-dimensional cell for arbitrary invariant tessellations with infinite-volume cells. No historical novelty is asserted.

The source is Anna Gusakova's contribution to *Mini-Workshop: Hyperbolic meets Stochastic Geometry*, Oberwolfach Report 57/2025, p. 3046, DOI [10.4171/OWR/2025/57](https://doi.org/10.4171/owr/2025/57). Its question is to extend cell intensity and typical cells to unbounded cells. Its surrounding discussion already identifies an obstruction for **infinite-volume** cells. These two adjectives must not be interchanged.

Our conclusions are:

1. Every full-dimensional closed convex finite-volume hyperbolic cell has a measurable, isometry-equivariant center, with no moment assumption. This includes unbounded cells. The ordinary center/Palm construction therefore applies when the inverse-volume intensity is positive and finite.
2. Infinite-volume cells admit no equivariant assignment of a probability measure on the ambient hyperbolic space. Randomizing the center cannot repair the known mass-transport obstruction.
3. Window-hit counts and fully-contained-cell counts do not generally recover center intensity, even for regular bounded-cell tessellations. Ideal triangles give an explicit unbounded finite-volume test.
4. Boundary rooting requires extra structure. There is no nonzero finite invariant measure on the ideal boundary; the known ideal Voronoi corona-Palm construction is model-specific and is not contradicted by this fact.
5. The mean cell-counting measure is always a canonical sigma-finite invariant measure on the space of cells. It has a precise incidence identity, but is measure-valued rather than the requested scalar-intensity/typical-cell pair.

The inverse-volume identity is standard Palm theory; the center obstruction is already in the cited literature. The self-contained formulations and countertests below are not a claim to have discovered those principles.

## 1. Framework and the mass-transport input

Let X = H^d, d >= 2, with curvature -1 and hyperbolic volume m. Let G = Isom(X) be the full isometry group. Fix o in X, and let K be its compact stabilizer. We use the standard Borel space of closed convex subsets of X with nonempty interior, inherited from the Effros/Fell measurable structure.

A tessellation T is a countable, locally finite collection of such cells, with disjoint interiors and union X. Local finiteness means that every compact set meets finitely many cells. Its law is G-invariant. The cell-counting measure is assumed measurable, as in the standard random-tessellation definition. All optional auxiliary randomness must have a jointly G-invariant law. We do not replace G by a nonunimodular subgroup fixing a point at infinity.

The boundary of a full-dimensional convex cell has m-measure zero. Countability and Fubini imply that the cell containing a fixed o is unique almost surely: the invariant random union of boundaries has expected volume zero in every bounded set. Denote this cell by C_o and write V(C) = m(C).

We use the following standard hyperbolic mass-transport principle (MTP). If M is a diagonally G-invariant Borel measure on X x X and its first marginal is finite on one nonempty bounded open set, then

    M(A x X) = M(X x A) = c m(A)

for some finite c and every Borel A. It follows from the unimodularity of G and compactness of K. A directly applicable statement is [BGR25, Theorem 2.1]. We apply it only after establishing the finite-marginal hypothesis; truncations below are essential when intensities may be infinite.

For x in X, kappa_x is normalized Haar measure on the fiber {rho in G: rho o = x}. Precisely, choose any g_x with g_x o = x and push normalized Haar measure on K forward by k -> g_x k. This is independent of the choice of g_x and satisfies

    kappa_(g x) = (rho -> g rho)_* kappa_x.

No uniform probability measure on the noncompact group G is used.

## 2. Approach 1: finite-volume cells without boundedness or moments

### Proposition 1: a moment-free canonical center

For every full-dimensional closed convex C with 0 < V(C) < infinity, there is a measurable center z(C) in C such that z(gC) = g z(C). In particular, boundedness is unnecessary.

**Proof.** Put mu_C = m restricted to C, divided by V(C). For a reference point a define

    F_(C,a)(x) = integral_C [d(x,y) - d(a,y)] mu_C(dy).

The bracket, rather than the two terms separately, is integrated. Its absolute value is bounded by d(x,a), so F is finite without a first-distance moment. The triangle inequality also makes F 1-Lipschitz in x. It is geodesically convex.

If x_0 != x_1, distance to y is strictly convex on the segment [x_0,x_1] whenever y is outside the complete geodesic through these points. A geodesic has d-dimensional volume zero. Thus integration against mu_C makes F strictly convex.

Choose R with p = mu_C(B(a,R)) > 1/2. For y in that ball,

    d(x,y) - d(a,y) >= d(x,a) - 2R;

for other y it is at least -d(x,a). Consequently

    F_(C,a)(x) >= (2p-1)d(x,a) - 2pR.

Hence F is coercive. Hyperbolic space is proper, so F has a unique minimizer z(C). Metric projection to a closed convex subset of a Hadamard manifold weakly decreases the distance to every point of that subset, and strictly decreases it when the original point is outside the subset. Therefore a minimizer outside C is impossible, and z(C) belongs to C.

Changing a to b changes F by the finite constant

    integral_C [d(a,y)-d(b,y)] mu_C(dy).

Thus the minimizer does not depend on a. Changing C,x,a by an isometry preserves the objective, which proves equivariance.

For completeness, measurability does not require an unproved choice of minimizer. Fix a countable dense sequence (q_j) in X. For each q_j the objective is a measurable function of C, by measurable integration of the Borel incidence relation y in C; V(C) is measurable too. The infimum over all x equals inf_j F(q_j), by continuity. For each n choose the first q_j whose value is less than this infimum plus 1/n. These choices are measurable, and for each C they stay in a compact sublevel set eventually. Strict convexity and uniqueness imply that the sequence converges to z(C). Thus z is measurable. QED.

This is a geometric-median construction. It is not the Lorentz-coordinate centroid, whose defining coordinate integrals would require separate justification on an unbounded body.

### Proposition 2: exact intensity and Palm inversion

Let T_f be the finite-volume subcollection of T, and use the center from Proposition 1. Define

    xi_z = sum_(C in T_f) delta_(z(C)),
    gamma_f = E[1_{V(C_o)<infinity}/V(C_o)],
    p_f = P(V(C_o)<infinity).

The counting measure xi_z is locally finite, with multiplicity allowed, since z(C) in C. Its intensity is exactly gamma_f, allowing the values 0 and infinity. If 0 < gamma_f < infinity, its center-Palm typical-cell distribution exists. For every nonnegative isometry-invariant measurable function F of a cell,

    gamma_f E_typ[F(C)]
      = E[1_{V(C_o)<infinity} F(C_o)/V(C_o)].                 (2.1)

In particular,

    gamma_f E_typ[V(C)] = p_f.                             (2.2)

When every cell has finite volume, p_f = 1. Formula (2.1), including the scalar intensity, is independent of the selected equivariant center. The *embedded, centered* distribution may depend on that center.

**Proof.** For each integer n >= 1 and bounded nonnegative invariant F, send mass from x in a finite cell C with V(C) >= 1/n to z(C), at density F(C)/V(C). The expected transport is

    M_n(A x B) = E sum_C [F(C)/V(C)] m(C intersect A)
                              1_{V(C)>=1/n, V(C)<infinity, z(C) in B}.

Its first marginal has density at most n ||F||_infinity relative to m. Invariance is immediate. MTP therefore equates its marginals. In particular, for m(B)=1,

    E sum_C F(C) 1_{V(C)>=1/n, V(C)<infinity, z(C) in B}
      = E[F(C_o)/V(C_o) 1_{V(C_o)>=1/n, V(C_o)<infinity}].

First let n increase, then truncate and increase F. Monotone convergence proves the corresponding identity with extended values. F=1 gives the center intensity. Dividing by finite positive gamma_f yields (2.1), and F=V gives (2.2). QED.

Here is also an explicit embedded law, avoiding any ambiguity in the word "typical." For a measurable nonnegative f on cell space, define

    S_z f(C) = integral_G f(rho^(-1) C) kappa_(z(C))(d rho).

By the covariance of kappa and z, S_z f is G-invariant. The centered probability Q_z is

    Q_z f = gamma_f^(-1) E[1_{V(C_o)<infinity} S_z f(C_o)/V(C_o)].

The transport proof identifies this with the cell mark of xi_z selected per unit volume. It agrees with the source's center-based construction on bounded cells and extends it to all finite-volume cells. Its law is independent of the unit-volume observation set.

By contrast,

    Q_vol f = gamma_f^(-1) E[1_{V(C_o)<infinity} f(C_o)/V(C_o)]

is the volume-rooted version, with the origin at a uniform volume location within a count-typical cell. It should not be confused with Q_z. Both give (2.1) for invariant F.

A sufficient condition for gamma_f < infinity is E N_hit(B(o,1)) < infinity, because centers in that ball are bounded by cells hitting it. Almost-sure local finiteness alone does **not** imply finite expectation. Positivity is automatic if p_f > 0.

**Outcome.** The unbounded finite-volume subclass is handled, subject to the explicit finite-intensity hypothesis. If infinite-volume cells occur, this construction counts only T_f. Equation (2.2) displays the missing spatial mass p_f rather than silently replacing it by 1. If p_f=0, gamma_f=0 and neither normalization above is a probability law.

## 3. Approach 2: randomized centers do not repair the obstruction

### Proposition 3: no ambient probability kernel for infinite-volume cells

Suppose T contains an infinite-volume cell with positive probability. There is no jointly G-invariant assignment

    C -> q_(T,C)

to every infinite-volume cell of a Borel probability measure on X. The assignment may depend on all of T and additional invariant randomness. No assumption that q is supported inside C is needed.

**Proof.** If such kernels existed, define the expected transport

    M(A x B) = E sum_(C:V(C)=infinity) m(C intersect A) q_(T,C)(B).

It is diagonally invariant. Since interiors are disjoint and q(X)=1,

    M(A x X) <= m(A).

MTP applies and implies M(X x B(o,n)) <= m(B(o,n)) < infinity for each n.

On the other hand, the incoming mass from an infinite-volume cell is infinite whenever q_(T,C)(B(o,n))>0. Each probability q has positive mass in some B(o,n). On the event that an infinite-volume cell exists, at least one such cell and one n have this property. This event is a countable union over n, so some n has positive probability of receiving infinite mass. Then M(X x B(o,n))=infinity, a contradiction. All products with infinite volume are interpreted via the displayed iterated nonnegative integral, so there is no undefined "0 times infinity" manipulation. QED.

The same conclusion holds for equivariant nonzero finite measures per infinite-volume cell: normalize each by its total mass. It includes deterministic centers, randomized interior points, and attempts to assign a finite cloud of points with total mass one.

[BGR25, Lemma 2.2] already proves the one-point obstruction. Proposition 3 is its direct probability-kernel formulation, not a refutation of the source problem or a novelty claim.

A related unavoidable constraint is the volume-bias identity. Any proposed *finite-intensity ambient-root Palm* law that reconstructs volume by the usual cell allocation satisfies gamma E_typ[V] = 1 (or p_f for a selected subcollection). For gamma>0, it cannot charge cells with V=infinity. This does not rule out an alternative boundary-rooted or non-Palm meaning of "typical."

**Outcome.** This approach closes a tempting loophole, but only for a precisely stated class of extensions. It is not an impossibility theorem for every conceivable answer to the OWR question.

## 4. Approach 3: explicit window-count countertests

### Proposition 4: boundary effects remain of order volume

Suppose an invariant tessellation has an equivariant center z with finite positive intensity gamma and, for a fixed r>0, every cell contains B(z(C),r). Let N_hit(R) count cells meeting B(o,R), and N_in(R) cells contained in B(o,R). Then for R>r,

    E N_hit(R) >= gamma m(B(o,R+r)),
    E N_in(R) <= gamma m(B(o,R-r)).                        (4.1)

Consequently,

    liminf_(R->infinity) E N_hit(R)/m(B(o,R))
        >= gamma exp((d-1)r) > gamma,
    limsup_(R->infinity) E N_in(R)/m(B(o,R))
        <= gamma exp(-(d-1)r) < gamma.                    (4.2)

The first inequality is meaningful even if an expected hit count is infinite.

**Proof.** A center in B(o,R+r) has its radius-r ball meeting B(o,R), so its cell is hit. A contained cell has its entire radius-r ball inside B(o,R), which forces d(o,z(C)) <= R-r by extending the geodesic from o through z(C). These yield deterministic counting inequalities. Taking expectations gives (4.1) by the definition of center intensity. Finally,

    m(B(o,R)) = omega_(d-1) integral_0^R sinh(t)^(d-1) dt,

so the ratios m(B_(R+s))/m(B_R) tend to exp((d-1)s) for fixed s. QED.

A regular compact hyperbolic polygon tiling, randomized by normalized Haar measure on the finite-volume quotient of G by its reflection lattice, supplies an example with r>0 and bounded cells. Thus (4.2) is a real counterexample to identifying the large-ball *expected* hit or containment density with ordinary cell intensity. We make no unsupported almost-sure ergodic-limit assertion for these balls.

### Example 5: all cells unbounded, ordinary intensity positive

Take the reflection tiling of H^2 by an ideal triangle. The reflection group is a cofinite hyperbolic lattice. If g is sampled using the invariant probability on G/Gamma, gT is a G-invariant locally finite tessellation. An ideal triangle has area pi, by the hyperbolic polygon area formula, and is unbounded. Proposition 2 gives

    gamma = 1/pi,          E_typ[area] = pi.

Nevertheless N_in(R)=0 for every finite R. There is no paradox: unboundedness does not imply infinite hyperbolic volume. The count-typical unrooted shape is the ideal triangle; its canonical center is the geometric median from Proposition 1 (also its symmetry center).

A second elementary test distinguishes the zero cell from the typical cell. Mix, with probabilities 1/2 and 1/2, invariant ideal-triangle and regular ideal-quadrilateral tilings. Their cell areas are pi and 2pi. The zero-cell shape probabilities are 1/2 and 1/2. Equation (2.1) instead gives

    gamma = 3/(4pi),
    P_typ(triangle) = 2/3,     P_typ(quadrilateral) = 1/3.

This nonergodic example is permitted by the source assumptions. It shows concretely why simply renaming C_o the typical cell does not preserve the usual count-based meaning.

**Outcome.** Euclidean negligible-boundary intuition fails, including before infinite-volume cells enter. A chosen window or rooting convention must be specified and justified.

## 5. Approach 4: ideal-boundary roots and existing special models

### Proposition 6: no invariant finite boundary measure

For d>=2 there is no nonzero finite G-invariant Borel measure on the ideal boundary partial X.

**Proof.** Normalize such a measure to a probability nu. Choose a loxodromic isometry h with attracting point a and repelling point b. For every boundary point xi != b, h^n xi -> a; h^n b=b. For any continuous f on the compact boundary, invariance and dominated convergence imply

    integral f dnu = (1-nu({b})) f(a) + nu({b}) f(b).

Thus nu is supported on {a,b}. Choose another loxodromic isometry with both fixed points disjoint from {a,b}. The same reasoning forces disjoint support, impossible for a probability. QED.

This rules out a naive replacement of hyperbolic volume by a finite invariant measure on the bare boundary. It does not rule out infinite intensity, conformally covariant measures, a chosen boundary point, or an enlarged boundary state space. Any of those changes the normalization problem.

The ideal Poisson--Voronoi tessellation is an important existing positive example with extra structure. [DCE+25, Section 5.3] constructs a typical ideal cell by inserting an ideal nucleus into a Poisson process on a corona. That space carries a transitive invariant measure, and disintegration/Mecke supplies the relevant Palm law despite noncompact isotropy. The embedding depends on the chosen ideal nucleus; the paper compares the resulting cells on the isometry-invariant sigma-field. This is neither a finite probability on the bare boundary nor a center in H^d.

The distinction remains present in recent literature: [DT26, Section 2] uses ordinary typical lower-dimensional IPVT faces, whose boundedness permits ambient centers, while distinguishing them from a usual full-cell Palm law. [BGT26] concerns a chosen horoball and a projected Euclidean tessellation, so its typical projected cells do not provide a general G-invariant full-dimensional construction.

**Outcome.** Corona-Palm is a valid model-specific route already known. No canonical corona or marked ideal-nucleus process has been constructed here for an arbitrary tessellation, especially for cells with many ideal endpoints. Extending that model-specific construction is a remaining problem, not a theorem of this packet.

## 6. Approach 5: a canonical sigma-finite measure-valued alternative

### Proposition 7: mean cell measure and incidence identity

On the measurable cell space define

    nu(A) = E sum_(C in T) 1_{C in A}.

Then nu is a G-invariant sigma-finite measure, even without E N_hit(K)<infinity. For nonnegative measurable h on X x cell-space,

    integral nu(dC) integral_C h(x,C) m(dx)
      = integral_X E[h(x,C_x)] m(dx).                    (6.1)

Here C_x denotes the almost surely unique cell at each deterministic x; a version on the null boundary set does not affect the integral.

**Proof.** Countable additivity follows by monotone convergence, and invariance follows from the law of T. For integers n,k>=1 let

    A_(n,k) = {C : m(C intersect B(o,n)) >= 1/k}.

Disjoint interiors give, deterministically,

    # (T intersect A_(n,k)) <= k m(B(o,n)).

Thus nu(A_(n,k))<infinity. Every cell contains an open ball, so belongs to some A_(n,k). This proves sigma-finiteness without a local count-moment assumption. Applying Tonelli to the random cell-counting measure proves (6.1), since exactly one cell contributes at m-almost every x. QED.

The measure nu is recoverable from the location-indexed zero-cell laws. To see this directly, choose any strictly positive integrable Borel weight w on X, for example w(x)=exp(-d*d(o,x)), and define

    Z_w(C) = integral_C w(x) m(dx),

which is strictly positive and finite for every cell. Substitution of

    h(x,C) = w(x) 1_{C in A}/Z_w(C)

in (6.1) gives the exact reconstruction

    nu(A) = integral_X w(x) E[1_{C_x in A}/Z_w(C_x)] m(dx). (6.2)

All integrals may take the value infinity. The intermediate choice w and origin o does not change nu, because (6.2) equals its root-free definition. The zero-cell laws at different locations are themselves related by the G-invariance of T.

In particular, nu restricted to cells containing o is the law of C_o and has total mass one. This illustrates both the strength and limitation of nu. It captures finite- and infinite-volume cells without a center, but restricting it at o produces the spatially sampled zero cell, not a count-typical cell. Example 5 demonstrates that difference even in a finite-volume case.

On the finite-volume sector, a center disintegrates nu into hyperbolic location intensity and the centered typical law; Proposition 2 is the scalar consequence. On the infinite-volume sector, Proposition 3 prevents achieving that disintegration through an equivariant probability kernel on X.

**Outcome.** This is a universal canonical measure-valued extension and a useful organizing object. Mean measures of point/particle processes are standard. A sigma-finite measure on embedded cells is not, by itself, the requested finite scalar intensity plus typical-cell probability, and we do not present it as a complete solution.

## 7. What remains and suggested next step

The genuine remaining case is a full G-invariant locally finite tessellation with infinite-volume cells. One must specify an alternative notion of typicality and a normalization that (i) agrees with ordinary count-Palm on finite-volume cells, (ii) remains informative about infinite-volume cells, and (iii) is intrinsic enough to deserve the source's word "natural."

Our no-go theorem rules out finite ambient probability roots; it does not rule out all such alternatives. The bare-boundary obstruction likewise leaves marked coronas and suitable sigma-finite disintegrations open. A productive next task is to characterize which cell processes admit an intrinsic marked boundary process carrying an invariant locally finite intensity and a Palm disintegration. Such a characterization would have to encompass the existing ideal Voronoi construction and address multiple-ended cells. Nothing here proves that it exists or is unique.

## References and credit

- [OWR25] A. Gusakova, "Random tessellations in hyperbolic space," in *Mini-Workshop: Hyperbolic meets Stochastic Geometry*, Oberwolfach Report 57/2025, 3046--3047. [Report](https://ems.press/content/serial-article-files/52444).
- [Last10] G. Last, "Stationary random measures on homogeneous spaces," *J. Theoret. Probab.* 23 (2010), 478--497. Section 8, especially the proper-partition reciprocal-volume identity. [Author manuscript](https://publikationen.bibliothek.kit.edu/1000012083/1022543).
- [BGR25] T. Bühler, A. Gusakova, K. Recke, "Critical Poisson hyperplane percolation in hyperbolic space has no unbounded cells," arXiv:2512.19425v1, 22 December 2025. Theorem 2.1 and Lemma 2.2. [Paper](https://arxiv.org/abs/2512.19425).
- [DCE+25] M. D'Achille, N. Curien, N. Enriquez, R. Lyons, M. Ünel, "Ideal Poisson--Voronoi tessellations on hyperbolic spaces," arXiv:2303.16831v3, 10 June 2025. Sections 4.1 and 5.3. [Paper](https://arxiv.org/abs/2303.16831).
- [DT26] M. D'Achille, C. Thäle, "Face volume densities of positive-intensity and ideal Poisson--Voronoi tessellations in hyperbolic spaces," arXiv:2606.26049v1, 24 June 2026. Section 2. [Paper](https://arxiv.org/abs/2606.26049).
- [BGT26] F. Besau, A. Gusakova, C. Thäle, "Random hyperbolic polyhedra in horoballs," arXiv:2609.10007, 9 September 2026. [Paper](https://arxiv.org/abs/2609.10007).

OpenAI tools assisted the research, proof writing and finite controls. This is an AI-assisted research note, not formal verification or human peer review. An independent audit was pending at author freeze.
