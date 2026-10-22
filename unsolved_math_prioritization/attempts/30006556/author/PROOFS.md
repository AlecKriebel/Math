# Two low-multiplicity distances: scoped partial results

## Target and conventions

For a finite set P of n distinct Euclidean planar points, let μ_P(d) count
unordered pairs at positive distance d. Write D=max d. The target asks, for
n≥5, whether two distinct occurring distances always have μ_P(d)≤n.
The Hopf–Pannwitz diameter theorem, a credited classical input, gives μ_P(D)≤n.
Thus a counterexample would have μ_P(d)≥n+1 for every occurring d<D.
The universal target remains unresolved here. No novelty is claimed.

## 1. Pair count and a collinear-subset consequence

Let M be the number of occurring distances and t=μ_P(D). In a counterexample,

  binom(n,2) ≥ t+(M−1)(n+1),
  M ≤ 1+floor((binom(n,2)−t)/(n+1)).                       (1)

In particular M≥floor(n/2)+1 is sufficient for the desired conclusion:
its right-hand pair lower bound is at least 1+floor(n/2)(n+1)>binom(n,2).
These are integer pair counts, not assumptions about distinct-distance growth.

**Proposition 1.** If P contains at least floor(n/2)+1 collinear points, then
P satisfies the target.

If P is collinear, every fixed positive distance gives a graph of maximum
degree two with no cycle (orient its edges along the line), so its multiplicity
is at most n−1; n≥5 ensures at least two distances. Otherwise let l≥floor(n/2)+1
be the number in a chosen line subset Q, and put its left endpoint at 0.
Its endpoint distances already give l−1 values. Suppose P had only l−1 values.
Then Q has exactly these values, and its coordinate set S, including 0, is
closed under nonnegative differences. If a is its least positive coordinate,
repeated subtraction shows that every member is an integer multiple of a;
closure under subtraction from the largest one then implies
S={0,a,...,(l−1)a}. Any point p of P outside the line must consequently have
its distances to consecutive points of Q in {a,2a,...,(l−1)a}. Strict triangle
inequality makes the difference between two such consecutive distances
strictly less than a. They must therefore be equal. Since l≥3, p would lie on
two different parallel perpendicular bisectors, impossible. Hence M≥l,
and (1) applies. This is an elementary consequence, without a priority claim.

## 2. A credited hull-layer consequence

Let L1 be the convex-hull vertices of P, L2 those remaining after deleting L1,
and h_i=|L_i|. Clemen–Dumitrescu–Liu (CDL), Theorem 1.3, supplies the bound

 μ_P(D2) ≤ min{3(h1+h2)/2, 4h1/3+2h2, 2h1+h2},            (2)

where D2 is the second-largest occurring distance. This bound is imported,
not re-proved here. A sufficient special case is h1+h2≤2n/3.

**Corollary 2.** If a line contains l points of P and l≥n/3+4, the target holds.

There are k=n−l points off that line. Each convex layer has at most two
vertices on the line, including degenerate line-segment layers. Thus
h1+h2≤k+4≤2n/3. Apply (2) and the diameter theorem. Interior occurrences are
controlled by the cited theorem, not discarded. This corollary is credited
as a direct application of CDL. It does not cover all almost-convex sets.

## 3. An exact 61-point obstruction to the extrema shortcut

The following finite specialization is inspired by and credited to CDL,
Proposition 1.5. It refutes only the proposed shortcut
min{μ_P(min distance), μ_P(D2)}≤n, not the target.

Set m=21, α=π/21,

 D=2 cos(α/2), d=2 cos(3α/2),
 r=−cos α+sqrt(cos²α+d²−1), δ=1−r.

Take the 21 vertices v_j=(cos(2jα),sin(2jα)) and their scaled copies r v_j.
Add the nineteen points

 δ(i+j/2, sqrt(3)j/2),
 i,j integers with max{|i|,|j|,|i+j|}≤2.                    (3)

This gives 61 distinct points. All inequalities used next are certified with
rational enclosing intervals by verify_math.py, using Machin's identity and
alternating Taylor series, not floating-point equality tests:

 0<r<1, δ>0, δ<2r sin α,
 r−2δ>δ, 1−2δ>δ,
 rD<d<D, 4δ<d, 1+2δ<d.                                  (4)

The nineteen-point triangular patch lies in the disk of radius 2δ. Its
minimum distance is δ; exactly 42 unordered pairs have that distance, as
verified by the integer quadratic form (Δi)²+ΔiΔj+(Δj)².

Within either 21-gon the minimum distance exceeds δ. Between the two rings,
the squared distance is 1+r²−2r cos(2kα), minimized uniquely at k=0.
Thus there are precisely 21 radial pairs of length δ. The disk bounds in
(4) exclude any patch-to-ring pair of that length. Therefore μ_P(δ)=42+21=63.

The outer 21-gon has diameter D at 21 pairs, and second-largest length d at
21 pairs. The largest cross-ring distance has angle π−α and square
1+r²+2r cos α=d², by the definition of r. There are exactly 42 such pairs.
All inner-ring and patch-related distances are strictly below d by (4).
Consequently D is the diameter, D2=d, μ_P(D)=21, and μ_P(D2)=21+42=63.

These strict gaps also establish that neither alleged extremum was selected
by approximate sorting. In this construction the short radial ring pairs,
not consecutive inner-polygon vertices, supply the extra 21 occurrences of
δ. The broader CDL obstruction is not a new result of this packet.

## 4. All but one point on a circle

**Theorem 4.** Let n≥5. If n−1 points of P lie on one circle, then P has two
distinct occurring distances of multiplicity at most n.

The proof below is an authored argument. Its novelty has not been established.
The only external mathematical input is the classical diameter theorem.

Write P=Q∪{p}, |Q|=m=n−1≥4, and normalize the circle to the complex unit
circle. If p is on it too, every distance graph has maximum degree two,
so every multiplicity is at most n and the assertion follows. We consider
p off the circle.

### 4.1 The center case

Suppose p=0. Every distance other than 1 occurs only inside Q and has
multiplicity at most m. If the target failed, all distances in Q would lie
in {1,D}, with D>1. Indeed D≤1 would leave an occurring distance below 1
in Q, producing a second sparse value, whereas if 1 never occurs in Q
then all P-distance multiplicities are at most m. Each point has at most
two circle-neighbors at a fixed distance, so a two-distance Q has m≤5.
For m=5 both distance graphs have degree two at every vertex. In particular
Q is invariant under rotation by π/3, because chord length 1 on the unit
circle subtends π/3. Every such orbit has six points, a contradiction.

For m=4, all pairwise chord lengths being 1 or D>1 means each consecutive
angular gap is at least π/3 and at most π. Each is π/3 or the same angle
θ in (π/3,π]. If k gaps are θ, their sum gives θ=π/3+2π/(3k), k=1,2,3,4.
In units π/3 these choices are respectively θ=3,2,5/3,3/2.
For k=1 two consecutive unit gaps give a forbidden chord-angle 2.
For k=2 a boundary between a unit gap and a 2-gap gives forbidden angle 3.
For k=3 a boundary gives forbidden angle 8/3.
For k=4 two successive gaps give forbidden angle 3.
All are the smaller central angles of the indicated two-gap arc (at most π).
Thus no such Q exists. This settles p=0.

### 4.2 Saturation of every non-diameter distance

Suppose p≠0 and the target fails. A circle centered at p intersects the unit
circle in at most two points. Thus at most two p-to-Q pairs have any fixed
length. Within Q every distance graph has degree at most two, hence at most
m edges. Every non-diameter occurring distance must therefore have exactly
m+2=n+1 occurrences: m inside Q and two incident to p. Its graph on Q is
2-regular, and the two neighbors of each q are reflections of one another
in the radial line through q.

Let s be the number of non-diameter values and let t∈{0,1,2} be the number
of p-to-Q pairs of length D. Counting p-to-Q pairs gives m=2s+t.
Every q∈Q has exactly 2s non-diameter neighbors, leaving t−1 diameter
neighbors. Thus t is 1 or 2. If t=1, there are no diameter edges in Q;
if t=2, those edges form a perfect matching.

### 4.3 Radial symmetry forces a regular polygon

Let S=∑_{q∈Q}q. Each of the s non-diameter neighbor pairs at q sums to
2 cos θ_j q, where θ_j depends only on its chord length. Put
c=2∑_{j=1}^s cos θ_j, which is real.
For t=1, S=(1+c)q for all q, so S=0. All noncentral points of Q pair by
radial reflection about every q, and these reflections preserve Q.

For t=2 let f(q) be the diameter partner. Then
S=(1+c)q+f(q). Summing over q, and using that f permutes Q, gives
mS=(2+c)S. Since c<2s=m−2, S=0. Consequently f(q)=−(1+c)q.
Both q and f(q) have modulus one, the scalar is real, and f(q)≠q; hence
f(q)=−q. The leftover neighbor is antipodal and is fixed by radial
reflection. Again every radial reflection through a point of Q preserves Q.

A finite subset of a circle preserved by reflection in the radius through
each of its points is a regular polygon. Here is a direct argument. Choose
a smallest positive gap α0 between consecutive points, rotate one endpoint
to angle 0 and the next to α0. Reflection successively in radii through
already obtained points produces all integer multiples of α0. Finiteness
forces α0/(2π) to be rational. If that rotation orbit had a smaller angular
gap than α0, minimality would be contradicted; therefore the orbit's spacing
is exactly α0. No additional points can lie between its consecutive points.
So Q is exactly a regular m-gon.

### 4.4 Two radial moments contradict m≥4

Put x=|p|² and y=D². For a regular m-gon with m≥3, the first two complex
Fourier sums vanish. Hence

 ∑_{q∈Q}|p−q|² = m(1+x),
 ∑_{q∈Q}|p−q|⁴ = m(1+4x+x²).                             (5)

For any vertex q0 of Q, the corresponding sums over q∈Q (including q0) are
2m and 6m. Each non-diameter length occurs twice in that row and twice in
the p-row. Length D occurs t−1 times in the vertex row and t times in the
p-row. Thus (5) equals 2m+y and 6m+y² respectively. It follows that

 y=m(x−1),    (x−1)((m−1)(x−1)−6)=0.

As y>0, x=1+6/(m−1) and y=6m/(m−1). But the triangle inequality gives
D≤|p|+1, so

 6m/(m−1) ≤ (sqrt(1+6/(m−1))+1)².

Subtracting the rational terms leaves
2≤sqrt(1+6/(m−1)), equivalent to m≤3. This contradicts m≥4 and proves
the theorem. The excluded m=3 is meaningful: the four-point pair of joined
equilateral triangles is a counterexample to the unrestricted n=4 target.

## 5. Why the one-circle argument does not extend immediately

Suppose P consists of m circle points Q and k additional points R, none at
the circle center. For every fixed distance,

 μ_P(d) ≤ m+2k+binom(k,2).                                (6)

If P were a target counterexample, every non-diameter distance would satisfy

 μ_Q(d) ≥ m+1−k−binom(k,2),
 m−μ_Q(d) ≤ k+binom(k,2)−1.                              (7)

Indeed each extra point gives at most two Q-incidences, and there are at
most binom(k,2) pairs within R. For k=1 the defect is zero, which is exactly
the saturation used above. For k=2 the defect can be two; the corresponding
distance graph may have four missing incidences. Radial reflections need no
longer preserve Q, and neither its regularity nor the vanishing Fourier
moments follows. If an outlier is the center, even (6) needs an exceptional
radius term. No stability theorem closing these defects is proved here.
This is the precise remaining gap of this approach, rather than an implicit
assumption that two-circle intersections solve the arbitrary planar case.
