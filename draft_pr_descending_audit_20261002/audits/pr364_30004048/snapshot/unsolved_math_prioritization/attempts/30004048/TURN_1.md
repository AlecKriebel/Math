# Turn 1: exact rational reduction and uniform finite certificates with slack

Substantive author turn **1/5**. This turn does not prove ψ symmetry. It shows that a genuine asymmetry can always be witnessed at rational parameters, and gives an explicit finite-size approximation/certificate theorem with degree slack. The slack cannot silently be removed at the source's known discontinuities.

Use the exact finite biconstrained graph definition in SOURCE_SCOPE.md. For an admissible tripartite graph G put

 F(G)=max_(c in C)|N_A²(c)|/|A|,
 R(G)=max_(a in A)|N_C²(a)|/|C|.

Thus ψ(x,y)=inf F(G) over the (x,y)-biconstrained graphs. All edge and reachability densities of a particular finite graph are rational.

## 1. The universal symmetry problem is exactly reducible to rational pairs

For each finite graph with all four positive minimum degrees define

 a(G)=min{min_(a in A)deg_B(a)/|B|, min_(b in B)deg_A(b)/|A|},
 b(G)=min{min_(b in B)deg_C(b)/|C|, min_(c in C)deg_B(c)/|B|}.

These are rational numbers in(0,1]. The graph is (a(G),b(G))-biconstrained, and if it is (x,y)-biconstrained then a(G)>=x and b(G)>=y. Therefore

 ψ(x,y)=inf{ψ(r,s):r,s rational, x<=r<=1, y<=s<=1}.              (1)

For the inequality from right to left, use monotonicity of ψ in both constraints. For the other direction, let η>0 and choose a finite admissible G with F(G)<ψ(x,y)+η; this uses only the definition of an infimum. Set r=a(G),s=b(G). Then ψ(r,s)<=F(G)<ψ(x,y)+η. Let η decrease to zero. No extremal graph attaining ψ is assumed.

Consequently ψ is symmetric for all real pairs in(0,1] if and only if it is symmetric for all rational pairs. Equivalently, if ψ(x,y)<ψ(y,x), choose G with

                      F(G)<ψ(y,x).

Its rational pair (r,s) above satisfies

                 ψ(r,s)<=F(G)<ψ(y,x)<=ψ(s,r).                    (2)

This is an exact reduction, with no continuity assumption. It does not bound the denominator of the rational witness. It also does not say that reversing this particular G produces an optimal graph in the other direction.

One related consequence is right continuity along the northeast diagonal at a pair whose two coordinates are irrational. For any near-optimal finite G, both a(G)>x and b(G)>y strictly, so G remains admissible at(x+δ,y+δ) for some δ>0. This and monotonicity prove

                  lim_(δ↓0)ψ(x+δ,y+δ)=ψ(x,y)                    (3)

at such a pair. No analogous assertion at rational thresholds follows. In particular the credited formula ψ(t,t)=1/floor(1/t) has right jumps at t=1/k for k>=2.

## 2. A uniform simultaneous sampling lemma

Let G be any (x,y)-biconstrained graph, let0<ε<min(x,y), and put

                  n=ceil[ε^(−2) log(10/ε²)].                    (4)

There exists a tripartite graph H with **exactly n vertices in each part**, which is (x−ε,y−ε)-biconstrained and satisfies

                       F(H)<=F(G)+ε,
                       R(H)<=R(G)+ε.                            (5)

Its order3n is independent of the order of G. Multiple selections of the same original vertex will become distinct twin vertices in H, so H is still a finite simple graph.

Proof. Independently sample n vertices uniformly with replacement from each of A,B,C. Label the resulting copies A_1,...,A_n, B_1,...,B_n and C_1,...,C_n. Join copies in consecutive parts exactly when their original vertices are adjacent. There are no other edges.

For a fixed selected A_i, conditional on its original vertex, its n adjacency indicators to the sampled B copies are independent Bernoulli variables with mean at least x. Hence the probability its degree is below(x−ε)n is at most exp(−2nε²). The same reasoning, conditioning separately on the selected endpoint, works for each of the other three directed degree families B→A, B→C and C→B. A union bound over these **4n** events suffices; the events need not be independent.

For a selected C_i, every sampled A copy reachable from it through a sampled B copy was already reachable in G. Conditional on the original C vertex, the n indicators that sampled A copies belong to its original N_A² set are independent Bernoulli with mean at most F(G). Therefore the probability that the actual reach fraction in H exceeds F(G)+ε is at most exp(−2nε²). This is an upper bound by the original reach set, and does not assume that sampling B preserves every existing path. The reverse reach bound has the same proof with A and C exchanged. These contribute **2n** further events.

For completeness, the Bernoulli bound used here follows from the classical exponential-moment argument: for a Bernoulli variable X of mean p, the second derivative of log E exp(t(X−p)) is the variance of a tilted Bernoulli law and is at most1/4. Its value and first derivative at0 vanish, so the logarithm is at most t²/8. Independence, Markov's inequality and t=4ε give exp(−2nε²) for the upper deviation; apply −t for the lower deviation. Thus no large-sample normal approximation is used.

The probability of any failure is at most6n exp(−2nε²). Let u=ε² in(0,1) and L=log(10/u). Since n>=L/u and n<=L/u+1,

 6n exp(−2nε²) <=(6/100)(uL+u²) <=24/100 <1.                   (6)

For the second inequality, use log10<3 and log(1/u)<=1/u−1, which give uL<=1+2u<=3, and u²<=1. Hence some realization of the samples has all four degree inequalities and both reach bounds simultaneously. This proves (5), including its uniform order and all dependency/duplicate-selection qualifications.

## 3. A finite optimization table and the exact sandwich it provides

For a positive integer n define Ψ_n(x,y) to be the minimum of F(H) over all tripartite graphs H with exactly n vertices in each part that are (x,y)-biconstrained. This is a minimum over a nonempty finite set (the complete graph between consecutive parts is allowed), and its value is a multiple of1/n. At rational inputs it can in principle be found by testing the2^(2n²) binary choices for the two bipartite edge sets. This is a finite exact formulation, **not a claim that such an exhaustive computation was performed or is efficient**.

Always ψ(x,y)<=Ψ_n(x,y), since the latter uses a restricted family. Taking near-optimal G and applying §2, then letting its excess over the infimum vanish, gives

             Ψ_n(x−ε,y−ε)<=ψ(x,y)+ε,                            (7)

where n is as in(4). Equivalently, if x+ε,y+ε<=1,

       ψ(x,y)<=Ψ_n(x,y)<=ψ(x+ε,y+ε)+ε.                           (8)

Equation(8) is a one-sided regularized sandwich. It does not assert uniform approximation at every exact parameter pair, nor replace x+ε by x. At a point with right continuity along the northeast diagonal it does give convergence of these particular finite table values as ε↓0, including the irrational-coordinate points in(3). The diagonal's rational jumps explain why the qualification is necessary.

## 4. A finite sufficient certificate for actual asymmetry

For n from(4), x,y>ε, suppose an exact finite table comparison were to establish

                Ψ_n(x,y)<Ψ_n(y−ε,x−ε)−ε.                       (9)

Then (7) in the reversed order and the trivial lower restriction give

 ψ(x,y)<=Ψ_n(x,y)<Ψ_n(y−ε,x−ε)−ε<=ψ(y,x).                       (10)

Thus (9) is a sufficient finite certificate for an **actual** asymmetric pair of universal values, rather than merely an asymmetric example graph. No instance satisfying(9) is claimed here. A calculation of only a candidate graph supplies an upper bound on Ψ_n, not the exact lower bound on the reversed table required by(9).

If both relevant points are continuity points and ψ(x,y)<ψ(y,x), a sufficiently small ε gives

 ψ(x+ε,y+ε)+2ε<ψ(y−ε,x−ε).

Using (8) on the left and Ψ_n>=ψ on the right proves(9). More generally that strict robust inequality itself suffices, without a continuity claim. A gap confined to a parameter boundary is not certified by this reasoning. The exact rational reduction(1)–(2) and the slackened finite certificate are therefore complementary, not interchangeable.

## 5. Scope of this turn

The proof supplies an exact countable parameter reduction and explicit uniformly small slackened models, together with a correct finite certification target. It does not establish ψ-symmetry or provide an asymmetric pair. The source's known φ symmetry, ψ diagonal formula and minimal-value symmetry are credited rather than counted as results of this attempt.

The remaining difficulty is to prove the relevant global transposition principle or find a finite certificate strong enough to separate universal values, including their boundary behavior. A bounded graph census alone is not such a resolution. Original question unresolved1/5; four substantive turns remain.
