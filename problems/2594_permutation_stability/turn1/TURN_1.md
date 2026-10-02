# Turn 1: exact deletion modulus and the first repair obstruction

**2594 / KOU-21.85. Substantive author turn 1/5. Original implication remains unresolved.**

The source gate pins finitely generated groups, pointwise asymptotic multiplicativity, normalized Hamming distance, and an asymptotically negligible enlargement of the finite set. This turn develops an exact reduction to deleting points from genuine finite actions, proves a conditional repair result, and excludes a tempting uniform-metric shortcut. It does not claim these elementary mechanisms are historically new.

## 1. Canonical compression and a sharp defect bound

Let Y be a finite set, X⊂Y nonempty, n=|X|, k=|Y\X|. For a permutation p of Y, define c_X(p) on X by following the p-cycle from x until its first return to X. Thus c_X(p) is a permutation: it is obtained by erasing Y\X from each cycle. It preserves inverses and the identity:

    c_X(p⁻¹)=c_X(p)⁻¹,       c_X(1)=1.

Whenever p(x)∈X, c_X(p)(x)=p(x). Hence the two maps disagree on X in at most k places. More precisely, the exceptional set is X∩p⁻¹(Y\X), whose cardinality is at most k.

For two permutations p,q of Y,

    |{x∈X : c_X(p)c_X(q)(x) ≠ c_X(pq)(x)}| ≤ 2k.             (1)

Indeed, outside q⁻¹(Y\X)∪(pq)⁻¹(Y\X), both q(x) and pq(x) lie in X; both sides then equal pq(x). Intersecting with X and bounding the two exceptional sets proves (1). No commutativity is used.

The constant 2 is sharp. Take Y={0,1,2}, X={0,1}, p=(0 2), q=(1 2). Both individual compressions are identities, whereas c_X(pq) interchanges 0 and 1. Thus exactly 2k=2 discrepancies occur.

If ρ:G→Sym(Y) is a genuine action, the maps

    c(g)=c_X(ρ(g))

satisfy, for every g,h∈G at once,

    d_X(c(g)c(h),c(gh)) ≤ 2k/n.                              (2)

In particular, if k/n→0 in a sequence, these maps form a source-admissible almost-homomorphism. Restoring the erased points is a flexible repair for **every group**: the disagreement on X is at most k and the added-point penalty is k, so its flexible distance is at most 2k/n.

There is also a useful one-sided comparison with an arbitrary permutation a of X:

    |{x∈X : a(x) ≠ c_X(p)(x)}|
       ≤ |{x∈X : a(x) ≠ p(x)}|.                             (3)

Where p(x)∈X, the comparisons are identical; where p(x)∉X, the right side already counts x and the left side counts it at most once. Thus replacing the restriction of a flexible repair by its canonical compression does not increase its disagreement with the original approximate permutation.

## 2. The exact remaining modulus

Fix a nonempty finite symmetric generating set S for G. For δ≥0 let D_{G,S}(δ) be the supremum, over all finite genuine actions ρ:G→Sym(Y) and nonempty X⊂Y with |Y\X|≤δ|X|, of

    min_{τ∈Hom(G,Sym(X))} max_{s∈S} d_X(c_X(ρ(s)), τ(s)).    (4)

The minimum exists because there are finitely many homomorphisms into a fixed finite symmetric group and the trivial action is among them. The supremum exists in [0,1]. D is nondecreasing and D(0)=0.

### Proposition 1

For a flexibly permutation-stable finitely generated group G,

    G is permutation-stable  ⇔  lim_{δ↓0} D_{G,S}(δ)=0.       (5)

The forward implication holds without assuming flexible stability.

**Proof of the forward implication.** If the limit were not zero, choose ε>0, δ_j→0, finite actions ρ_j and subsets X_j so that every action on X_j has generator error at least ε. Supremum attainment is unnecessary: lower the positive limsup threshold by a factor of two. Put n_j=|X_j| and k_j=|Y_j\X_j|. Since a counterexample has k_j≥1 and k_j/n_j≤δ_j, n_j→∞. The compressed maps c_j have multiplicativity defect bounded by 2δ_j for every pair, by (2). Permutation stability would supply actions τ_j with generator errors tending to zero, a contradiction.

To apply the source convention indexing a challenge by every integer n, first take a subsequence with strictly increasing n_j, relabel X_j=[n_j], and use the trivial action for other values of n. The resulting sequence is a source challenge. Thus arbitrary increasing dimensions have not strengthened the hypothesis.

**Proof of the reverse implication.** Let f_n:G→Sym(X_n) be a source challenge and use flexible stability to obtain genuine actions ρ_n on Y_n⊃X_n with δ_n=|Y_n\X_n|/|X_n|→0 and pointwise discrepancy on X_n tending to zero. Define c_n(g)=c_{X_n}(ρ_n(g)). By (3), d_X(f_n(g),c_n(g))→0 for each g. By (4), choose genuine τ_n on X_n whose generator error from c_n is at most D(δ_n), hence tends to zero. It follows that τ_n and f_n are close on S.

Generator closeness implies pointwise closeness because the maps f_n are asymptotically multiplicative. For a fixed word g=s_1⋯s_ℓ, telescoping in the bi-invariant Hamming metric gives

    d_X(f_n(g), τ_n(g))
      ≤ d_X(f_n(g), f_n(s_1)⋯f_n(s_ℓ))
           + Σ_i d_X(f_n(s_i), τ_n(s_i)) → 0.

The first term tends to zero by induction on the fixed word length, using the finitely many multiplication pairs along that word. This proves source permutation stability. ∎

**Exact gap.** The difficult assertion in (5) is the vanishing of D. This reduction does not establish it for general flexibly stable groups. Applying flexible stability again to the compressed challenge adds no information: the original ρ already provides the flexible repair by restoring the k removed points. That attempted iteration simply returns the starting action.

## 3. A sufficient orbit-tail condition

For a finite action ρ on Y and an integer K≥1, let

    t_K(ρ) = |{y∈Y : the G-orbit of y has size >K}| / |Y|.

Let U be the union of the ρ-orbits meeting B=Y\X, and Z=Y\U. Then Z⊂X is invariant. Define an action τ on X by keeping ρ on Z and fixing every point of X\Z. Its disagreement with the compression is bounded, uniformly over g∈G, by

    d_X(c_X(ρ(g)),τ(g)) ≤ |U∩X|/n
                       ≤ (K−1)k/n + (1+k/n)t_K(ρ).          (6)

For the second inequality, every touched orbit of size at most K has at most K−1 retained points per deleted point. Their total retained mass is therefore at most (K−1)k. All remaining retained points of U lie in the union of large orbits, of mass at most |Y|t_K. This proves (6); subtracting deleted points in the large orbits would only improve it.

### Proposition 2

Suppose a source challenge has flexible repairs ρ_n with δ_n→0 whose orbit distributions are tight, in the precise sense

    lim_{K→∞} limsup_{n→∞} t_K(ρ_n)=0.

Then that challenge has strict repairs on its original sets. In particular, if every source challenge of a flexibly stable G admits such repairs, G is permutation-stable.

**Proof.** The action τ_n just defined does not depend on K. Inequality (6), first with any fixed K and then letting K→∞, gives limsup_n d_X(c_n(g),τ_n(g))=0 uniformly in g. Combine with (3) and the pointwise closeness of the given flexible repairs. ∎

For example, if all finite G-orbits have size at most a common K, then

    D_{G,S}(δ) ≤ min{1,(K−1)δ}.                              (7)

Thus flexible stability implies strict stability for this class, which includes groups whose finite actions all factor through one fixed finite quotient. No amenability is required for this conditional argument. This does not settle the unbounded-orbit case.

## 4. Why the untouched-core method and a uniform shortcut both fail

Let G=Z=⟨t⟩, let ρ(t) be a single cycle of length M, and delete one point. No nonempty G-invariant subset of the original action remains inside X, so Z in Section 3 is empty. Nevertheless strict repair is easy: let τ(t) be the cycle on the M−1 surviving points, in their inherited cyclic order.

For every fixed integer a,

    d_X(c_X(ρ(t^a)), τ(t)^a) ≤ |a|/(M−1).                  (8)

For a≥1, exclude the starting points whose original orbit segment of a steps meets the deleted point; there are at most a such points. For the remaining points, both maps follow the same segment and agree. For a<0 use the inverse cycle; a=0 is exact. Thus the canonical compressions are strictly repairable pointwise even though the largest untouched invariant core is empty.

However, (2)'s **uniform** multiplicativity bound does not license replacing pointwise closeness by uniform closeness over all g. This already fails for Z. Here is a self-contained diagnostic, consistent with the stronger known result of Becker–Chapman (Theorem 1.1, cited below).

Take M=p prime, n=p−1, let ρ be the p-cycle, and delete one point. For every action τ of Z on n points, put β=τ(t) and r=|Fix(β)|/n. The permutation c_X(ρ(t)) is an n-cycle. For n≥2, its distance from β is at least r. Also c_X(ρ(t^{pj}))=1 for all integers j. Since every cycle length of β is <p, exponentiation by p is coprime to every such length. Averaging over j through a full period of β, a β-cycle of length L≥2 has mean moved fraction 1−1/L≥1/2. Consequently some j satisfies

    d_X(1,β^{pj}) ≥ (1−r)/2.

Therefore every exact τ satisfies

    sup_{g∈Z} d_X(c_X(ρ(g)),τ(g))
       ≥ max{r,(1−r)/2} ≥ 1/3.                              (9)

Meanwhile the uniform multiplicativity defect tends to zero by (2), and the pointwise strict corrections in (8) still exist. The group element witnessing (9) may depend on p and τ. This is not a counterexample to KOU-21.85.

## 5. Literature credit and control scope

Deleting a point and bypassing it in permutation cycles is an established mechanism in Becker–Lubotzky's instability work and Becker–Chapman's *Stability of approximate group actions: uniform and probabilistic*, JEMS 25 (2023), 3599–3632, [DOI 10.4171/JEMS/1267](https://doi.org/10.4171/JEMS/1267), [primary full PDF](https://ems.press/content/serial-article-files/32932), Theorem 1.1 and Section 4. Their theorem is stronger than the elementary uniform Z diagnostic (9). This turn claims no novelty for that separation, for the compression method, or for the already known amenable implication from Ioana's Lemma 3.2.

The exact verifier checks compression and (1) on all permutation pairs and all nonempty retained subsets through |Y|=5, the no-loss bound (3), orbit-tail bounds on finite cycle partitions, and the explicit prime-cycle diagnostics. These are finite controls of the formulas, not a proof of vanishing of D or a graph/group-realized counterexample to the original implication.

**Turn outcome:** a complete exact reduction, a tight-orbit sufficient condition, and two rigorously identified failed mechanisms. **Unresolved:** whether every flexibly stable finitely generated group has D_{G,S}(δ)→0. Next work must add a mechanism for unbounded touched orbits or construct a genuinely flexibly stable group where that modulus fails.
