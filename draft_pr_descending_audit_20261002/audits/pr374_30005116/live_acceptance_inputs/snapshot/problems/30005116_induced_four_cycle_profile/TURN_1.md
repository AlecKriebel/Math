# Turn 1: exact optimization within the complete multipartite class

**30005116 / OWR-10252930-028. Original unresolved; substantive author turn 1 of 5.**

The target is the full induced-C4 profile at edge density x>1/2, not merely optimization over the proposed host family. This turn proves the latter for every number of parts, gives its explicit value and finite-size control, and identifies the exact missing reduction. The clique-density construction is credited to the source literature. The moment argument is an elementary reconstruction; no historical novelty is claimed.

## 1. Precise normalization and the restricted problem

For a graph G on n vertices, write

    x(G)=e(G)/binom(n,2),      ρ(C4,G)=N(C4,G)/binom(n,4),

where N counts four-element vertex sets inducing C4. It does not count labeled embeddings or arbitrary four-cycles with possible chords.

A complete multipartite graphon with part masses a_1,...,a_m≥0, ∑a_i=1, has

    q=∑a_i²,       x=1−q,
    F(a)=6∑_{i<j} a_i² a_j² = 3(q²−∑a_i⁴).             (1)

Indeed an induced four-cycle must have two sampled vertices in each of two different parts; the multinomial coefficient is 6. Thus at fixed x the entire restricted problem is to minimize the fourth moment under fixed first and second moments.

## 2. The finite-dimensional moment theorem

Let 0<q≤1. Among all finite nonnegative vectors a with ∑a_i=1 and ∑a_i²=q, the minimum of ∑a_i⁴ is attained by the following vector, up to permutation and zero entries. Put

    r=floor(1/q),
    d=((r+1)q−1)/r,
    a=(1+√d)/(r+1),       b=(1−r√d)/(r+1).              (2)

The minimizing positive masses consist of r copies of a and, when b>0, one copy of b. In particular

    L(q)=r a⁴+b⁴.                                      (3)

At q=1/r, formula (2) has b=0 and a=1/r, and the minimizer is the uniform r-part vector. The formula at q=1 is interpreted the same way. For q→0, L(q)→0.

**Proof for fixed dimension.** Fix any dimension m for which the constraint set is nonempty. It is compact, so a minimum exists. Delete its zero coordinates and write s for its positive support size.

If all positive coordinates are equal, q=1/s and their fourth moment is 1/s³=q³. For every feasible vector, Hölder's inequality gives

    ∑a_i² ≤ (∑a_i⁴)^(1/3) (∑a_i)^(2/3),

so ∑a_i⁴≥q³, with equality only when the positive coordinates are equal. Thus reciprocal-integer q is settled, including the equality case.

Suppose q is not a reciprocal integer. The positive coordinates of a minimizer are not all equal. The gradients of ∑a_i and ∑a_i² are therefore linearly independent. The Lagrange multiplier theorem applies in the relative interior of this positive support. For some real λ,μ, every positive coordinate z satisfies

    4z³−2λz−μ=0.                                      (4)

This cubic has no quadratic term and therefore cannot have three distinct positive roots: their sum would be zero if all three roots were positive. It has at most two distinct positive roots. A single positive value was already excluded, so denote these values by t<u.

Subtracting equation (4) at t and u gives

    2λ=4(t²+tu+u²).                                   (5)

We claim t occurs only once. If it occurred twice, take a vector v supported on those two coordinates with entries 1 and −1. It satisfies

    ∑v_i=0,       ∑a_i v_i=0,

so it is tangent to both constraints. Their gradients are independent, hence their common level set is a smooth manifold near this minimizer. In particular there is a twice differentiable feasible curve with derivative v. The second derivative of the objective on this curve is the Lagrangian Hessian evaluated on v:

    ∑(12a_i²−2λ)v_i²
      =2(12t²−2λ)
      =8(t−u)(2t+u)<0.                                (6)

The first derivative is zero at a constrained minimum. A negative second derivative is impossible. This proves the claim. Notice that the relevant tangent direction exists only when there are at least two small coordinates and one large coordinate, so there is no two-variable dimension exception in this step.

Consequently the minimizer has r copies of a larger value a and one smaller positive value b. The constraints read

    r a+b=1,       r a²+b²=q,       0<b<a.

The first relation yields 1/(r+1)<a<1/r; the second increases strictly with a on this interval and ranges from 1/(r+1) to 1/r. Hence

    1/(r+1)<q<1/r,

which uniquely determines r=floor(1/q). Solving the quadratic gives exactly (2). This proves that every fixed-dimensional minimum has value (3). The proposed vector is feasible in every dimension for which the original constraint is feasible: for nonreciprocal q, Cauchy–Schwarz forces m≥ceil(1/q)=r+1, while at q=1/r it forces m≥r. Thus the conclusion applies to every dimension, with the stated equality classification. ∎

This proof uses both a support-boundary argument and the constrained second-order condition. Merely finding a two-valued stationary vector would not distinguish the wrong branch with many small coordinates and one large coordinate.

## 3. Exact restricted profile and comparison with the credited construction

Let M(C4,x) be the supremum of limiting induced-C4 densities over sequences of complete multipartite graphs with edge densities tending to x, as in the source paper. Then

    M(C4,x)=3[(1−x)²−L(1−x)],        0≤x≤1,             (7)

with endpoint values zero at x=0 and x=1.

For x>1/2, let k=r+1 in (2). The r=k−1 large parts have mass

    a=(1+√(1−kx/(k−1)))/k,

and the remaining part has mass b=1−(k−1)a. This is precisely Liu–Mubayi–Reiher Construction 1.9, which is the credited clique-density construction. The boundary choice b=0 is the same smaller-part-count graph, not a distinct extremizer. At x=1−1/r, (7) gives 3(r−1)/r³, matching their already proved unrestricted values.

For x≤1/2 the same formula reduces to the complete bipartite expression 3x²/2, which is already known to be the unrestricted answer. We do not count that known theorem as new progress.

**Why (7) covers unbounded part counts.** In a finite complete multipartite graph with integer part sizes n_i summing to n, put a_i=n_i/n, q=∑a_i², and p_j=∑a_i^j. Direct counting gives

    N(C4,G)=∑_{i<j} binom(n_i,2)binom(n_j,2),

and therefore the exact identity

    24N(C4,G)/n⁴
       =3(q²−p_4)+6(p_3−q)/n+3(1−q)/n².              (8)

Also x(G)=n(1−q)/(n−1). The error between the right side of (8) and 3(q²−p_4) is at most 6/n+3/n², independently of the number of parts. The weighted moment theorem supplies p_4≥L(q).

On each interval between reciprocal integers, L is continuous by (2). At a junction q=1/r, the vector on one side limits to r equal positive masses and one zero, while on the other side it limits to r equal positive masses. Both give L=q³. Finally 0≤L(q)≤q² gives continuity at 0. Thus every complete multipartite sequence, including one whose number of parts tends to infinity, has limsup bounded by (7). Rounding the masses (2) to integer parts gives a matching sequence at each fixed x. The conversion from n⁴/24 to binom(n,4) has factor tending to 1 and does not change these limits. ∎

## 4. Exact algebraic evaluation and an explicit obstruction to a shortcut

For rational q, one may evaluate (3) in a quadratic field without numerical square roots. Using d from (2),

    L(q)=A−B√d,
    A=[1+6rd+r(r²−r+1)d²]/(r+1)³,
    B=4r(r−1)d/(r+1)³.                               (9)

Here B≥0. To certify a rational fourth moment z satisfies z≥L(q), if z≥A the conclusion is immediate; otherwise it is equivalent to

    B²d ≥ (A−z)²,

with both compared sides nonnegative. This is the exact arithmetic used for the finite controls.

The conclusion M(C4,x)=the proposed profile **does not establish** I(C4,x)=M(C4,x) for arbitrary graphs. The source's Schelp–Thomason symmetrization statement for the Lagrangian C4−cK2 yields an upper bound by the concave envelope of M; it does not keep the edge density fixed during symmetrization. No fixed-density replacement theorem has been proved here. That is the remaining substantive obstacle, rather than optimization of multipartite weights.

The first turn therefore closes the weighted-multipartite search route as a possible counterexample family. Further turns must investigate genuinely non-multipartite hosts or a valid density-preserving reduction; increasing a finite scan of part weights would not address the main gap.

## Checks

`verify_turn1.py` uses exact integer and rational arithmetic. It independently checks the radical moment formulas and the negative constrained-Hessian coefficient, all integer partitions on the declared finite range, and direct induced-vertex-set counting for small multipartite graphs against (8). These checks are not the proof for all weights or all part counts; the preceding compactness and calculus argument provides that proof.

Primary formulation and notation: Liu–Mubayi–Reiher, https://arxiv.org/abs/2106.16203v2 and https://doi.org/10.1016/j.jctb.2022.09.003 . Original source: https://ems.press/journals/owr/articles/10252930 . Current related but distinct semi-induced problem: Balogh–Lidický–Mubayi–Pfender–Volec, https://homepages.math.uic.edu/~mubayi/papers/Semi_Inducibility.pdf .
