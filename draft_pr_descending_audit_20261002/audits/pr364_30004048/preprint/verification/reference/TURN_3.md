# Turn 3: a boundary formula and a counterexample to symmetry

Substantive author turn **3/5**. This is a complete negative candidate for the exact source question, submitted for independent review:

     |ψ(13/27,14/27)−ψ(14/27,13/27)| >= 1/108 >0.                (1)

The proof does not infer different universal values from two example graphs. It first proves an exact formula for **all** admissible finite graphs on the boundary x+y=1, then uses a credited explicit regular matrix to place the two universal values in disjoint finite rational sets. The actual two values and their order need not be determined to prove(1), and are not claimed evaluated here.

## 1. A finite incidence invariant

For rational θ in(0,1), let R_θ be the following class. An element consists of a finite binary matrix M, with nonempty row set B and nonempty column set I, and strictly positive rational probability vectors b on B and q on I, such that

                    M q=θ1_B,       M^T b=θ1_I.                 (2)

The columns of M are required to be pairwise distinct. Set

                 Δ(M)=max_(v in B)Σ_(i in I) M_vi,
                 d(θ)=min{Δ(M):(M,b,q) in R_θ}.                  (3)

The degree Δ is the number of distinct column types incident with a row; it is **unweighted**. The probabilities in(2) remain part of the regularity condition. Rows may be repeated. All weights are strictly positive, so no discarded zero-weight row or column is being counted.

This class is nonempty. If θ=p/r in lowest terms with0<p<r, take the r-by-r cyclic incidence matrix whose columns are p consecutive positions, with both weight vectors uniform1/r. Its columns are distinct and Δ=p. Therefore

                              1<=d(θ)<=p.                        (4)

In particular the minimum in(3) is attained: a nonempty set of positive integers has a least member, which by definition comes from a finite template. We do not assume that a graph attaining ψ exists in order to obtain this minimum.

Rationality in the definition causes no loss if one instead starts with positive real vectors satisfying(2) for rational θ. For a fixed rational matrix, each of the two systems in(2), together with the corresponding sum-one equation, is an affine linear system with rational coefficients. Gaussian elimination expresses its solutions as a rational particular solution plus a rational basis of free directions. Rational free coordinates can approximate a given strictly positive solution closely enough to preserve positivity. Thus positive rational solutions exist on exactly the same incidence pattern, retaining Δ and distinct columns.

## 2. Exact boundary formula

For every rational θ in(0,1),

                         ψ(1−θ,θ)=1−θ/d(θ).                    (5)

We prove the universal lower bound and a finite blow-up attaining the upper bound separately.

### 2.1. Universal lower bound, including full-reach vertices

Let G be **any** finite (1−θ,θ)-biconstrained graph via nonempty parts(A,B,C). Put m=|B| and F=max_c |N_A²(c)|/|A|. If F=1, the desired inequality F>=1−θ/d(θ) is immediate. Suppose F<1. Then for every c in C there exists some a in A with no common neighbor in B. Thus N_B(a) and N_B(c) are disjoint, while

 |N_B(a)|>=(1−θ)m,       |N_B(c)|>=θm.

Their size lower bounds sum to m. Equality is forced in both, and their union is B. In particular **every c in C has exactly θm neighbors in B**. Summing B–C edges now gives

 Σ_(v in B)deg_C(v)=θm|C|.

Every summand is at least θ|C| by the fourth biconstraint on this pair. Hence every v in B has exactly θ|C| neighbors in C as well. This is the boundary rigidity that is absent away from x+y=1.

Group the C vertices by their identical B-neighborhoods T_1,...,T_n. These sets are pairwise distinct and have size θm. Define M_vi=1 precisely when v is in T_i, set b_v=1/m, and let q_i be the size of C-class i divided by|C|. All these weights are positive rational numbers. The just-proved degree equalities give(2), so Δ(M)>=d(θ).

For each type i let A_i consist of the A vertices whose B-neighborhood is exactly B\T_i. A vertex a is missed by a c of type i if and only if N_B(a) is disjoint from T_i. Since |N_B(a)|>=(1−θ)m and |B\T_i|=(1−θ)m, disjointness is equivalent to that exact equality of neighborhoods. Thus the missed A set is **exactly A_i**. Different A_i are disjoint because their neighborhoods are different. Put

 p_i=|A_i|/|A|>0,      t=min_i p_i.

The strict positivity follows from F<1, and

                                F=1−t.                          (6)

For any middle vertex v, all A_i with v in T_i are nonneighbors of v. The B→A lower degree constraint says that at most a θ fraction of A are nonneighbors. Consequently

                    Σ_(i:M_vi=1) p_i <= θ.

There may be additional A vertices outside the union of the A_i; they only make this inequality stronger and are not discarded. It follows that t times each row degree of M is at most θ, and therefore

 t<=θ/Δ(M)<=θ/d(θ),       F>=1−θ/d(θ).                           (7)

This proves the lower bound for every finite graph, with repeated C-neighborhoods correctly grouped and full-reach graphs already handled.

### 2.2. A finite upper construction from a minimizing template

Take (M,b,q) in R_θ with Δ(M)=d=d(θ), and let n be its number of columns. Write T_i for column i's row support. By(2), every T_i has b-weight θ. Since b is strictly positive and the columns are distinct, these supports are pairwise incomparable: T_i⊆T_j would force equality from their equal positive weights.

Set

                             t=θ/d,
                             δ=1−nt.

These are rational and δ>=0, because

 nθ=Σ_i b(T_i)=Σ_v b_v deg_M(v)<=d.                             (8)

Construct a weighted tripartite graph as follows:

- Its middle part has one vertex per row, of weight b_v
- Its C part has one vertex c_i per column, of weight q_i, adjacent exactly to T_i
- Its A part has one vertex a_i of weight t for each column, adjacent exactly to B\T_i
- If δ>0, add an A vertex a_* of weight δ adjacent to all of B; if δ=0, omit it

Each part has positive total weight1, and every retained vertex has strictly positive weight. For every a_i its B-neighbor weight is1−θ; for a_* it is1. For each middle vertex v its A-neighbor weight is

                         1−t deg_M(v)>=1−θ.

Both directions of the B–C pair have neighbor weight exactly θ by(2). Thus all **four** biconstraints hold.

For c_i, the vertex a_i is not reachable. If j≠i, incomparability gives T_i\T_j nonempty, so a_j is reachable through a middle row in that difference. The universal vertex a_*, when present, is reachable because θ>0 makes T_i nonempty. Therefore every c_i reaches A-weight exactly1−t.

All weights are rational. Replace every weighted vertex in each part by a positive integer number of twins proportional to its weight, using a common denominator for that part; join complete or empty type pairs according to the weighted graph. Each original middle row has at least one copy, so the reachability statements are preserved exactly. This gives an ordinary finite simple graph with all three parts nonempty, all four degree fractions unchanged, and F=1−t. Zero-mass a_* was omitted before this blow-up. Therefore ψ(1−θ,θ)<=1−θ/d, completing(5).

No compactness limit or attainment of the original infimum was assumed. The construction proves attainment on this rational boundary as a consequence of the integer minimum(3).

For comparison, if θ is irrational, the first equality |N_B(c)|=θm is impossible in a finite graph. Hence every admissible graph has a full-reach C vertex, and ψ(1−θ,θ)=1. This is consistent with the credited irrational-boundary phenomenon in the source; it is not used to prove the counterexample.

## 3. The credited seven-type regular matrix

The following matrix is the top bipartite part of **Figure1, printed6** of Chudnovsky–Hompe–Scott–Seymour–Spirkl, *Concatenating Bipartite Graphs*, EJC29(2)(2022),P2.47. The same regular example is discussed in §12, printed71. The figure was visually checked and the weights and every row/column sum were independently verified.

 M = [1 0 1 1 1 0 0]
     [0 1 1 1 1 0 0]
     [0 0 1 0 0 1 1]
     [0 0 0 1 0 1 1]
     [0 0 0 0 1 1 1]
     [1 1 0 0 0 1 0]
     [1 1 0 0 0 0 1],

 b=(5,5,3,3,3,4,4)/27,
 q=(4,4,3,3,3,5,5)/27.                                         (9)

Direct multiplication gives Mq=(13/27)1 and M^T b=(13/27)1. Its seven columns are distinct. Its row degrees are4,4,3,3,3,3,3, so Δ(M)=4. The complementary matrix J−M has the same positive weights and is14/27-regular, again with distinct columns; its row degrees are3,3,4,4,4,4,4. Therefore

                         1<=d(13/27)<=4,
                         1<=d(14/27)<=4.                        (10)

The regular matrix is an existing source example, not a new matrix attributed to this attempt. The global boundary formula(5) and the deduction from it are the mathematical claims being submitted for review.

## 4. The two universal values cannot be equal

Let d=d(13/27) and e=d(14/27). Equation(5) gives

 ψ(14/27,13/27)=1−13/(27d),
 ψ(13/27,14/27)=1−14/(27e),       d,e integers in{1,2,3,4}.        (11)

Equality would imply13e=14d. Since13 and14 are coprime, this requires d to be a positive multiple of13 and e a positive multiple of14, contradicting(10). Thus the displayed rational pair is an actual counterexample to universal symmetry.

There is also the explicit gap in(1). If d=e, the difference in(11) is1/(27d)>=1/108. If e>d, then13e−14d=13(e−d)−d>=10, while27de<=324. If d>e, then14d−13e=14(d−e)+e>=15 and again27de<=324. Both latter bounds exceed1/108. This proves(1) without computing d or e, and without claiming the sign of the difference.

## 5. Two explicit upper-bound graphs, with their scope marked

The source matrix and its complement each have Δ=4, so the construction of §2.2 is completely explicit even if those templates do not minimize d. For θ=13/27, use A-type sizes

                    (13,13,13,13,13,13,13,17),

B-type sizes(5,5,3,3,3,4,4), and C-type sizes(4,4,3,3,3,5,5). Each A_i is joined to the complement of column i of M; the eighth A type is universal to B. Use M for B–C. The part orders are108,27,27, so the graph has162 vertices. Its minimum directed degrees in the four directions A→B, B→A, B→C, C→B are14,56,13,13, respectively. Every C vertex reaches95 A vertices. This verifies

                         ψ(14/27,13/27)<=95/108.                 (12)

For θ=14/27 use J−M, the same B,C class sizes, and A sizes

                    (14,14,14,14,14,14,14,10).

Again the graph has162 vertices. Its corresponding minimum directed degrees are13,52,14,14, and every C vertex reaches94 A vertices, giving

                         ψ(13/27,14/27)<=47/54.                  (13)

These are **upper bounds**, not asserted exact evaluations. Their unequal values alone would not prove asymmetry. The universal lower reduction and integer quantization(5),(11) are indispensable. The attached certificate and checker verify both ordinary graphs as well as the regular matrix and the integer gap.

## 6. Final candidate status

This resolves the exact symmetry question negatively, contingent on full independent review of the proof. It respects finite simple graphs, distinct reached vertices, all four constraints, arbitrary positive part sizes, repeated neighborhood types and ordinary rational blow-ups. It neither relies on the fixed-template discrepancy from turn2 nor substitutes φ for ψ.

No novelty certification is made. The seven-type source example and classical elementary tools are credited. The third substantive turn supplies a complete negative candidate, so author research stops here under the campaign's “complete earlier” exception. Full independent source/proof review is required before a solved-status publication or user resolution claim.
