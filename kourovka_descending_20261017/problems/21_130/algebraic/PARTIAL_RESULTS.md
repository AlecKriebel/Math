# Checkable algebraic and probabilistic partial results

Status at 2026-10-24T19:43Z: **partial results only; no solution of Kourovka 21.130**. Best-guess completion toward the full research goal: **12%**. None of these claims is asserted novel.

Let `A` be an `n`-element subset of an additive abelian group. Its complete simple graph is colored by `c({a,b})=a+b`. This is a proper edge coloring: equal colors on two edges sharing a vertex force the other two vertices to be equal.

## 1. Exact first moment

For each sum `s`, let `m_s` be the number of unordered distinct-element pairs `{a,b}⊂A` of sum `s`, and put

`T(A) = sum_s binom(m_s,2)`.

Every pair counted by `T(A)` consists of disjoint edges. For `n≥4`, a uniformly random undirected Hamiltonian cycle contains any specified two disjoint edges with probability

`p = 4/((n−1)(n−2))`.

Proof: there are `(n−1)!/2` unoriented cycles. Contract the two specified edges, retain their two orientations independently, and count cycles on the resulting `n−2` blocks. Equivalently use directed cycles, giving `4(n−3)!/(n−1)!`. This also gives the correct value `2/3` when `n=4`.

If `X` counts pairs of equal-colored edges within the cycle, linearity gives

`E X = 4T(A)/((n−1)(n−2))`.

Consequently, if `4T(A)<(n−1)(n−2)`, some Hamiltonian cycle has no repeated sum. This conclusion applies to abelian groups of any order. It does not handle typical high-energy subsets: if `A=G` has odd cardinality `n`, then every `m_s=(n−1)/2`, so `E X=n(n−3)/(2(n−2))`.

## 2. A standard local-lemma consequence

For completeness, the random-injection local lemma yields a broader sparse-color condition. Write `r=max_s m_s`. For `n≥4`, a sufficient condition is

`32 e (r−1) < n−2`.

No novelty is claimed. The imported fact is the canonical-event negative-dependency theorem for uniform random injections (Lu–Székely, Theorem 1) together with its local lemma (Lemma 3): [primary paper](https://people.math.sc.edu/lu/papers/randinj.pdf), [published record](https://doi.org/10.37236/981).

Here is the complete event count. Uniformly map the vertices of a fixed cyclic template `C_n` bijectively to `A`. A bad canonical event prescribes a bijection from the endpoints of a disjoint template-edge pair to the endpoints of a same-colored edge pair in `A`, mapping edges to edges. There are `Q=n(n−3)/2` template-edge pairs and eight such maps per pair-pair. Each event has probability `p=1/(n)_4`.

Let `R_a=sum_(b≠a)(m_(a+b)−1)` and `R=max_a R_a`. For a fixed template vertex there are at most `16(n−3)T` events using it; for a fixed target vertex there are `8QR_a` events using it. The graph joining any two events whose domain supports or image supports intersect contains the canonical-event conflict graph, so remains a valid negative-dependency graph. Any closed neighborhood has size at most

`D+1 ≤ 64(n−3)T + 32 Q R`.

The bound is valid although the event itself is counted several times. Thus the sharper sufficient inequality is

`e[64T+16nR] < n(n−1)(n−2)`.

Finally `T≤n(n−1)(r−1)/4` and `R≤(n−1)(r−1)` give the stated condition. Avoiding every canonical event is precisely avoiding every color repetition in the single template cycle.

This proof does not use odd order. Its exact universal gap is the large color-class regime; in odd groups one can have `r=(n−1)/2`, far beyond the bound.

## 3. Large least-prime-factor rectification

**Proposition.** If every prime divisor of the finite abelian group order `|G|` is greater than `2^(n−1)`, every `n`-element subset of `G`, `n>2`, has the required cyclic ordering.

**Proof.** Label `A={a_1,...,a_n}`. Form an integer matrix `M` with one row `e_i+e_j−e_k−e_l` for each equality `a_i+a_j=a_k+a_l` between distinct unordered pairs. A nontrivial row has four distinct indices by cancellation, has Euclidean norm `2`, and has coordinate sum zero. Let its rational row rank be `q≤n−1`.

We claim `e_i−e_j` is outside the rational row space for every `i≠j`. If it were inside, choose `q` independent rows and `q` pivot columns, with nonzero integer determinant `d`. Cramer's rule implies `d(e_i−e_j)` is an integer combination of those rows. Applying the homomorphism `Z^n→G`, `e_t↦a_t`, yields `d(a_i−a_j)=0`. Hadamard's inequality gives `1≤|d|≤2^q≤2^(n−1)`. By the assumption on `|G|`, multiplication by `d` is injective on `G`, so `a_i=a_j`, a contradiction. If `q=0`, the claim is immediate without a determinant.

Therefore the rational nullspace of `M` contains a vector `x=(x_1,...,x_n)` with pairwise distinct coordinates: each equality `x_i=x_j` is a proper hyperplane in the nullspace, and finitely many proper hyperplanes cannot cover a vector space over the infinite field `Q`. Every original equal-sum relation is preserved by `a_i↦x_i`.

Sort these rational coordinates as `b_1<...<b_n`. The simple graph with edges `{i,i+2}` for `1≤i≤n−2`, together with `{1,2}` and `{n−1,n}`, is one Hamiltonian cycle (its parity chains are joined at both ends). Its edge sums satisfy

`b_1+b_2 < b_1+b_3 < b_2+b_4 < ... < b_(n−2)+b_n < b_(n−1)+b_n`.

They are all distinct. The corresponding cycle in `A` also has all sums distinct, since an equality in `G` would have been preserved in the rational coordinates. QED.

The determinant bound is deliberately elementary and not optimized. This proposition leaves all small-prime primary groups, including arbitrarily large elementary `3`-groups, unresolved. The same relation-space mechanism becomes an equivalent reformulation if one simply assumes that all vertex differences survive over the rationals; proving that for every odd group would be false. For example, for `A=G=Z/5Z` the edge-only relation matrix has rational rank `4`, so its nullspace consists only of constant vectors and every vertex difference lies in its rational row space. The proposition uses the explicit determinant bound to justify rectification in its restricted regime.

## Route status

- Exact first moment: proved, sparse additive collisions only.
- Random-injection local lemma: proved consequence of a cited primary theorem, sparse maximal multiplicity only.
- Rational rectification: elementary proof above, large least prime factor only.
- Universal extension of these conditions: **blocked**; none controls arbitrary high-multiplicity small-prime subsets.
- Natural polynomial/exterior-algebra invariants: tracked separately in `polynomial/`.
