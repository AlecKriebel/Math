# Finite dyadic-set stabilizers in Thompson's circle group

## Status and attribution

This is a self-contained verification of a theorem already announced by Alper Ferudun in *Maximal Finite-Set Stabilizers in Thompson's Group T*, manuscript dated 4 September 2026, online 5 September 2026, [EulerSolve record](https://eulersolve.org/papers/aim-dynamical-systems-0011/), DOI [10.5281/zenodo.22324898](https://doi.org/10.5281/zenodo.22324898). That record explicitly marks the work as an AI-assisted, unrefereed preprint. The abstract, attribution, date, and theorem statement were accessible; its linked PDF and verification report were not retrievable in this investigation. Accordingly, the proof below is an independent reconstruction, **not a claim to have audited the inaccessible manuscript or its verification report**. No novelty or priority is claimed.

The exact recovered AIM question is: “Find new maximal subgroups of infinite index in Thompson groups.” It is an open-ended request for examples, not a demand for a classification, nor a conjecture restricted to dyadic pairs. The theorem below supplies a countably infinite family of examples, but does not close the broader research programme. The source-access and interpretation limits are recorded separately in SOURCE_GATE.md.

## 1. Definitions and theorem

Let D = Z[1/2]/Z be the dyadic subset of S¹ = R/Z. Thompson's group T consists of orientation-preserving, piecewise-affine circle homeomorphisms preserving D, with finitely many dyadic breakpoints and slopes integral powers of 2. Preservation of D is required explicitly: the breakpoint and slope conditions alone would not exclude arbitrary irrational rotations. Let F be the subgroup fixing 0, viewed as the analogous interval group on [0,1].

For a nonempty finite A ⊂ D, write

H_A = {g ∈ T : g(A) = A},

P_A = {g ∈ T : g(a) = a for every a ∈ A}.

The first is the **setwise** stabilizer; the second is the **pointwise** stabilizer. Maximal means maximal proper among all subgroups of T: H_A < K ≤ T implies K = T. Infinite index means that the set of left cosets T/H_A is infinite.

**Theorem.** For every k ≥ 1 and every k-element subset A of D:

1. H_A is a maximal proper subgroup of T.
2. [T : H_A] = aleph_0.
3. H_A ≅ F^k ⋊ C_k, where C_k cyclically permutes the k factors; equivalently H_A ≅ F wr C_k with the regular cyclic permutation action.
4. All H_A with the same k are conjugate in T.
5. Stabilizers with different k are pairwise nonisomorphic.

For k = 1, C_1 is trivial. For k = 2, this gives the earlier dyadic-pair example F wr C_2. For k > 1 the pointwise subgroup P_A is not maximal in T, because P_A < H_A < T.

## 2. Finite circular extension

**Lemma 1.** Every cyclic-order-preserving bijection between nonempty finite dyadic subsets of the circle extends to an element of T.

**Proof.** Choose corresponding starting points p_0 and q_0, and choose increasing real lifts

p_0 < p_1 < ... < p_m = p_0 + 1,
q_0 < q_1 < ... < q_m = q_0 + 1.

On each paired pair of arcs [p_i,p_{i+1}] and [q_i,q_{i+1}], choose finite partitions into intervals of lengths powers of 2 with dyadic endpoints. This is possible by taking a sufficiently fine uniform dyadic grid. If the two partitions have different numbers of pieces, bisect a piece in the smaller partition until the counts agree. A bisection increases the count by exactly one, so this terminates.

Match the resulting pieces in increasing order and map corresponding pieces affinely. Each slope is a ratio of powers of 2; all endpoints and their images are dyadic. These maps fit at endpoints. Assemble them on [p_0,p_0+1] and extend by f(x+n)=f(x)+n. The induced circle map belongs to T and realizes the prescribed finite bijection. This also proves dyadic preservation, since every affine intercept is dyadic, and the same is true for the inverse. ∎

Consequently, T acts transitively on Ω_k, the set of k-element subsets of D.

## 3. A connected elementary-slide graph

For k ≥ 2, put an undirected edge between A,B ∈ Ω_k if A∩B has k−1 elements and the two distinct points in A△B lie in the same connected component of S¹\(A∩B). For k=1, declare all distinct singletons adjacent. Call this graph L_k.

**Lemma 2.** All edges of L_k lie in a single T-orbit on unordered pairs of vertices.

**Proof.** For k≥2, in the circularly ordered union of the two configurations, the two noncommon points are consecutive, and every remaining point belongs to both configurations. All such unlabelled edge patterns are circularly isomorphic. If the two noncommon points appear in the opposite order, interchange the endpoints A,B of the undirected edge. Lemma 1 realizes the resulting circular bijection. For k=1, any bijection between two distinct circle points preserves circular order, so Lemma 1 again applies. ∎

**Lemma 3.** L_k is connected; its diameter is at most 2k.

**Proof.** Given U,V ∈ Ω_k, choose a cut point q ∈ D\(U∪V), and list the configurations in increasing order on the cut-open interval (q,q+1):

u_1 < ... < u_k and v_1 < ... < v_k.

Choose k distinct dyadic points b_1 < ... < b_k in (q,min(u_1,v_1)). Starting from U, replace u_1 by b_1, then u_2 by b_2, and so on. At step i, the point b_i and the old point u_i lie in the same complementary interval of the other k−1 points: the points b_j already inserted have j<i and lie to their left, while the remaining u_j have j>i and lie to their right. Thus every step is an edge of L_k. This gives a length-k path from U to B={b_1,...,b_k}. Repeat with V and reverse that second path. For k=1 the same argument applies directly. ∎

## 4. Primitivity from one moved point

**Lemma 4.** The action of T on Ω_k has no invariant equivalence relations other than equality and the universal relation.

**Proof.** Let ~ be an invariant equivalence relation and suppose A~B with A≠B. Since A,B have equal finite size, choose a∈A\B. Choose a different dyadic point a' sufficiently close to a that moving a to a' while fixing every other point of A∪B preserves circular order. In particular, a' is not in A∪B, and a,a' lie in the same component of S¹\(A\{a}). Such a choice is possible because D is dense and A∪B is finite.

By Lemma 1 there exists g∈T fixing (A∪B)\{a} pointwise and taking a to a'. Since a∉B, gB=B. Invariance gives gA~gB=B; together with A~B this gives A~gA. The vertices A and gA form an edge of L_k. Lemma 2 and invariance imply that every edge of L_k joins equivalent vertices. Lemma 3 and transitivity of ~ then imply that all vertices are equivalent. ∎

**Lemma 5.** H_A is maximal proper in T.

**Proof.** Transitivity identifies Ω_k with the left-coset action T/H_A through gH_A↦gA. If H_A≤K≤T, then

gH_A ~ hH_A if and only if gK=hK

is a T-invariant equivalence relation. Lemma 4 says that it is equality or universal. In the equality case, for every k∈K the equality kK=K forces kH_A=H_A, hence K=H_A. In the universal case every gK equals K, hence K=T. Finally H_A is proper because Ω_k has more than one element and the action is transitive. ∎

The coset bijection also computes [T:H_A]=|Ω_k|=aleph_0, since D is countably infinite and k is fixed and positive. No inference from simplicity, finite generation, or a finite numerical experiment is needed.

## 5. Structure and distinct isomorphism types

**Lemma 6.** H_A ≅ F^k ⋊ C_k, and H_A and H_B are conjugate whenever |A|=|B|=k.

**Proof.** Lemma 1 gives t∈T with tA=B, whence tH_At^{-1}=H_B. It therefore suffices to compute one representative.

Partition [0,1] into exactly k standard dyadic intervals I_0,...,I_{k−1}. Such a partition exists for every k≥1: start with [0,1] and repeatedly bisect a current interval. Let A_0 be their k left endpoints modulo 1. Every orientation-preserving circle map preserving A_0 induces a cyclic rotation of its k ordered points; the image of H_{A_0} in Sym(A_0) is therefore contained in C_k.

The kernel P_{A_0} consists of independent allowed interval maps on the k arcs. Affine normalization of each I_i to [0,1] has power-of-two slope and dyadic intercept, so each factor is exactly F. Restrictions glue continuously at the fixed endpoints, giving P_{A_0}≅F^k.

Define r by mapping I_i affinely onto I_{i+1}, with indices modulo k. The interval lengths are powers of 2, so r∈T. In normalized coordinates r preserves the position within an interval and moves the interval index forward by one. Thus r has order exactly k (order 1 when k=1), its image generates C_k, and conjugation by r cyclically permutes the normalized F-factors. The sequence with kernel P_{A_0} therefore splits with the stated action. ∎

**Lemma 7.** H_A has maximum finite element order exactly k. Consequently the groups for different k are nonisomorphic.

**Proof.** Every orientation-preserving interval homeomorphism of finite order is the identity. Indeed, if f(x)>x then x<f(x)<f²(x)<... contradicts finite order; the case f(x)<x is analogous. Hence F and F^k are torsion-free.

If u∈F^k⋊C_k has finite order, its finite cyclic subgroup intersects the torsion-free kernel F^k trivially. It injects into C_k, so the order of u divides k. Lemma 6 constructs an element of order k. Thus the maximum finite element order is k, an abstract group invariant. This separates every two different k, including k=1. ∎

## 6. Scope of the answer

The family is countably infinite even up to abstract isomorphism, and each member is maximal among **all** proper subgroups, not merely among infinite-index subgroups. It answers the requested construction task in the sense of supplying examples. It does not classify maximal subgroups of F, T, V, or generalized Thompson groups. The literature already contains the same all-k claim; this reconstruction is not a new mathematical discovery. The theorem's full proof above is logically independent of the inaccessible EulerSolve PDF.

The finite exact checks accompanying this note verify representative dyadic extensions, cyclic splittings and local-slide paths. They do not replace the universal proofs.
