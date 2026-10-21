# Erdős 734: five approaches and a reconstructed partial bound

Date: 2026-10-21. Target: every sufficiently large integer n admits a nontrivial pairwise balanced design (PBD), with all block sizes between 2 and n−1, such that every size multiplicity is O(sqrt(n)). **Target remains unresolved here.** The argument below independently supplies a complete existence proof of the historical O(n^(3/4)) partial bound, not the conjectured bound. It does not reproduce the stronger high-probability assertion in the original outline.

Write F(n) for the minimum, over these designs, of max_t M_t. All asymptotic constants below are absolute unless explicitly indexed by a density parameter.

## Approach 1: reconstruct the fixed-cardinality random upper bound

### A sampling lemma, including its proof

Let a uniformly chosen n-subset of a v-set have density p=n/v, with 0<p<1. Inspect membership on m specified distinct coordinates. Write P for that binary-vector distribution and Q for m independent Bernoulli(p) variables. If m≤v/2 and v≥2, then

TV(P,Q) ≤ m/v.

Indeed, after j coordinates, let S_j be the number selected. The next success probability is r_j=(n−S_j)/(v−j). The chain rule for relative entropy and the binary chi-square upper bound give

D(P||Q) ≤ sum_{j=0}^{m−1} E[(r_j−p)^2]/[p(1−p)].

The hypergeometric variance is Var(S_j)=j p(1−p)(v−j)/(v−1). Consequently

D(P||Q) ≤ sum_{j=0}^{m−1} j/[(v−1)(v−j)]
           ≤ m(m−1)/[2(v−1)(v−m+1)].

Pinsker's inequality, TV≤sqrt(D/2), proves the assertion: both factors in the denominator are at least v/2. This argument concerns the full membership vector, not merely its total. Therefore it applies simultaneously to the two intersecting lines used below. The ingredients are elementary probability inequalities; no omitted conditioning-on-exact-n step remains.

### Binomial atoms

For a Bin(r,p) mass function a_t, let A=max_t a_t. Uniformly for p in [1/10,1/2], A=O(r^(−1/2)). One direct proof uses Fourier inversion and

|1−p+p exp(iθ)|^r ≤ exp(−2r p(1−p)θ²/π²), for |θ|≤π.

Integrating the Gaussian over the real line gives A≤sqrt(π)/(2 sqrt(2r p(1−p))). Also a_t is unimodal, so, taking a_t=0 outside its support,

sum_t |a_t−a_{t−1}|=2A,
max_t |a_t−a_{t−1}|≤A,
sum_t (a_t−a_{t−1})²≤2A²=O(1/r).

### Apply to a projective plane

Choose a prime power q which is the smallest power of two at least sqrt(2n). Then 2n≤q²<8n. Let v=q²+q+1 and k=q+1, and use the projective plane of order q. For n≥10, q≥4, n>k, p=n/v belongs to [1/10,1/2], and 2q+1≤v/2. Select exactly n points uniformly. For every original line L put Y_L=|L intersect S| and, temporarily including sizes zero and one, X_t=#{L:Y_L=t}.

The sampling lemma for a single line and the binomial atom estimate give

max_t E X_t ≤ v [O(q^(−1/2))+k/v]=O(v/sqrt(q)).

We next control all sizes at once using the trace of the covariance matrix rather than a separate union bound. For two distinct lines L,H let

c = sum_t Cov(1_{Y_L=t},1_{Y_H=t}).

In the iid Bernoulli model their unique common point has indicator B, and their disjoint q-point remainders have independent Bin(q,p) counts U,W. If a is the Bin(q,p) mass function, elementary conditioning on B gives

Cov(1_{U+B=t},1_{W+B=t})=p(1−p)(a_{t−1}−a_t)².

Thus the iid trace covariance is O(1/q). To transfer to the exact-n model, express the trace covariance as

Pr(Y_L=Y_H) − sum_t Pr(Y_L=t)Pr(Y_H=t).

The first term changes by at most the total variation on the union of the lines, at most (2q+1)/v. The second changes by at most the total variation between the product marginal distributions, at most 2(q+1)/v. Hence c≤O(1/q). Absolute-value control of the entire covariance matrix is unnecessary.

For one line, sum_t Var(1_{Y_L=t})≤1. Summing over the ordered pairs of lines now yields

E sum_t (X_t−E X_t)² = sum_t Var(X_t)
                          ≤ v+O(v²/q)=O(v²/q).

By Markov's inequality, with probability at least 1/2 the sum of squares is at most twice this upper bound. On that event every coordinate satisfies

X_t ≤ E X_t + sqrt(sum_s (X_s−E X_s)²)
    = O(v/sqrt(q))=O(q^(3/2))=O(n^(3/4)).

Discard the intersections of size zero or one. Every remaining pair lies on exactly one retained original line; two retained blocks cannot coincide, because two original lines share at most one point. All blocks have size at most q+1<n. This is a valid nontrivial PBD with the asserted uniform multiplicity bound, for **every n≥10**, up to an absolute constant. Small orders are irrelevant to the target.

**Outcome:** complete existence-level reconstruction of the published exponent, with all-n order selection and fixed-cardinality sampling explicitly addressed. Not a new exponent and not a solution to the sqrt(n) question. The proof gives a positive fraction of successful selections for a sufficiently large constant; it does not assert the original outline's 1−o(1) success probability.

## Approach 2: exact obstruction to dense projective-plane truncation

This argument is deterministic; randomness and typicality are unnecessary. Fix any n-point subset of a plane of order q. Choose a line uniformly from its v lines and put Z=|L intersect S|, p=n/v. Point and pair incidence counts give

E Z=(q+1)n/v=(q+1)p,
E[Z(Z−1)]=n(n−1)/v,
Var(Z)=q p(1−p).

The last equality follows by substitution and (q+1)²=v+q. In particular Var(Z)≤q/4. Chebyshev shows that at least 3v/4 lines have intersection size within sqrt(q) of the mean. There are at most 2sqrt(q)+1 integer sizes in this interval. If p≥δ>0, then for sufficiently large q its lower endpoint is at least two. Therefore the induced PBD has

max_{t≥2} M_t ≥ (3v/4)/(2sqrt(q)+1)=Ω(q^(3/2))=Ω(n^(3/4)).

No upper bound p≤1−δ is needed for this coarser bound. If variance is smaller, an interval of radius proportional to sqrt(qp(1−p)) can give a stronger obstruction, with a separate zero-variance case. Dense deterministic subsets, clever derandomization, and improved concentration cannot beat the 3/4 exponent within this construction family.

**Outcome:** exact method barrier, not a lower bound for arbitrary PBDs. Sparse subsets are not covered uniformly by the density hypothesis.

## Approach 3: distinct-size counting and the sqrt(n) lower obstruction

Here is the short core of the corrected distinct-size upper bound, rather than an appeal to block count alone. Distinct blocks meet in at most one point. If selected blocks have strictly increasing sizes s_1<...<s_r and s_1≥a, their union has at least ar points: when block i is added, at most i−1 of its points are old, while its size is at least a+i−1. Thus there are at most floor(n/a) distinct occurring sizes at least a, and at most a−2 smaller sizes. The number D of distinct sizes satisfies

D≤a−2+floor(n/a).

Set h=floor(sqrt(n)). If h²≤n<h²+h, choose a=h to get D≤2h−2. If h²+h≤n<(h+1)², choose a=h+1 to get D≤2h−1. These are the corrected sharp distinct-size counts in Gyárfás (2002); only the upper bounds are needed here.

The de Bruijn–Erdős theorem gives at least n blocks in a nontrivial PBD. Hence

F(n)≥ceil(n/D), and in particular F(n)>sqrt(n)/2.

This does not establish an optimal leading constant for F(n): equality in the separate block-count and distinct-size inequalities need not occur simultaneously. Trying to maximize the number of distinct sizes can produce designs with many repeated 2-blocks. Thus the corrected distinct-size theorem settles a necessary palette-size constraint, not realizability of a balanced profile.

**Outcome:** rigorous matching-order lower bound; no stronger asymptotic constant claimed.

## Approach 4: line refinement and weighted-inflation tests

### Arbitrary independent refinements of a complete projective plane fail strongly

Start with the complete plane on v=q²+q+1 points, and replace each original k=q+1 block by a PBD on those same k points, allowing the unchanged block. The resulting blocks still cover each pair once. Let U be the number of unchanged original lines and M the largest final size multiplicity. An altered line requires at least k blocks by de Bruijn–Erdős. Consequently the final block count b obeys

b≥U+k(v−U)=kv−qU.

There are only q possible final sizes, 2,...,q+1, so b≤qM. The only size-(q+1) blocks are unchanged originals, so U≤M. Therefore

M≥kv/(2q)=(q+1)v/(2q)=Ω(v).

This excludes arbitrary line-by-line internal PBD replacements of the full plane, not just a particular near-pencil replacement rule. It does not exclude constructions which reorganize pairs across original lines, or a different initial geometry.

### Naive unequal weighting is not an available operation

Replace each point of a parent k-block (k≥3) by a positive-size group of weight w_i. Suppose its cross-group pairs are to be covered using blocks containing exactly one point from **every** group. If there are b such transversal blocks, then for every pair i≠j, b=w_i w_j, because each block covers exactly one pair from those two groups. Positivity and k≥3 imply all w_i are equal. Unequal weights cannot simply be inserted into an ordinary full-transversal design.

For equal weight w, each parent block generates w² transversal blocks of its original size k, while the point count grows by only w. On a uniform parent plane this gives v w² copies of size k before adding any within-group designs; it worsens, rather than spreads, that multiplicity. General weighted group-divisible designs permit smaller supports and are not ruled out, but they require new cross-group pair-covering constructions and explicit bounds on every resulting size. Merely assigning different weights to vertices is not a proof.

**Outcome:** two rigorous barriers to natural geometric modifications, with the wider weighted-design route left genuinely open.

## Approach 5: profile capacity, leftover pairs, and all-n interpolation

The pair-count identity is

sum_t binom(t,2) M_t=binom(n,2).

If M_t≤C sqrt(n) and all sizes are at most K, then

binom(n,2)≤C sqrt(n) sum_{t=2}^K binom(t,2)
          =C sqrt(n) binom(K+1,3).

Thus K≥((3/C)^(1/3)+o(1))sqrt(n). Together with at least n blocks, the multiplicity target requires at least sqrt(n)/C distinct occurring sizes. A bounded palette, or blocks all substantially smaller than sqrt(n), cannot work. These are necessary profile constraints only; satisfying the arithmetic does not construct a design.

An approximate edge-disjoint clique decomposition can be completed by making every uncovered pair a 2-block. If it leaves L uncovered pairs, this adds L to M_2. For this particular repair mechanism the target therefore requires L≤C sqrt(n), even if the starting packing has no 2-blocks. Coverage 1−o(1), or even an o(n²) leftover, is nowhere near sufficient: the permitted leftover fraction is O(n^(−3/2)). Grouped repairs might improve this, but then their full size profile must be proved.

A further exact obstruction concerns interpolation between admissible orders. Keep every old block of an n-point PBD and append one new point. Any block containing the new point and two old points would repeat their already-covered pair. Therefore the n old-new pairs must become n separate 2-blocks. Even adding one point by this keep-all-old-blocks padding rule destroys an O(sqrt(n)) bound. A construction on a subsequence cannot be promoted to every large n by such padding. One must redesign old pairs, use an independently controlled deletion mechanism, or prove a suitable all-order existence theorem.

**Outcome:** exact acceptance conditions for approximate designs and all-n interpolation. No claimed general impossibility of absorption, deletion, or sophisticated repair.

## Sources and status boundaries

- Erdős–Purdy, Some Combinatorial Problems in the Plane (1978), Theorem 2: https://renyi.hu/~p_erdos/1978-42.pdf . The printed result supplies the historical exponent; it explicitly omits probability calculations. Approach 1 above is a separate authored existence proof, not a claim those omitted calculations were recovered verbatim.
- Gyárfás, Erdős Problems on Irregularities of Line Sizes and Point Degrees (2002): https://www.renyi.hu/~gyarfas/Cikkek/101_Gyarfas_ErdosProblemsOnIrregularitiesOfLineSizesAndPointDegrees.pdf . Used for the corrected distinct-size statement and historical context. Approach 2 derives its own exact quantitative barrier, avoiding OCR ambiguity in the historical method-limitation remark.
- de Bruijn–Erdős, On a combinatorial problem (1948): https://www.renyi.hu/~p_erdos/1948-01.pdf . Standard nontrivial-PBD block-count theorem used in Approaches 3 and 4.
- Existing recovered source/status gate: SOURCE_GATE.md. Current tracker status remains subject to that gate; no new claim of live tracker access.

These are mathematical research notes, not a publication or a declaration that Erdős 734 is solved. Independent review is required before accepting the reconstructed upper proof or new barriers.
