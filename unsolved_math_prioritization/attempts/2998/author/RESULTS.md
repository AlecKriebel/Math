# Necessary conditions for the fixed branch-surface problem

## 1. Target and scope

The target asks whether a single surface embedded in the four-sphere can be the branch locus of finite coverings with every closed orientable four-manifold as total space. The surface is fixed; the degree and monodromy may depend on the total space. This is modern K3 Problem 4.122, discussed on pages 291–292 of [K3].

We use the smooth or locally flat PL interpretation supplied by the originating papers. In the smooth setting, the maps have the standard transverse power-map models. The invariant arguments below also apply to locally flat topological branch surfaces using [GKS, Theorem 1]. We do not allow cone singularities, nodes, wild embeddings, or arbitrary two-complexes as substitutes for an embedded branch surface. We do not assert that the catalog's abbreviated wording settles every categorical convention.

Let S be a finite disjoint union of closed connected embedded surfaces S_i in the oriented S^4. Write chi_i = chi(S_i) and e_i for the normal Euler number in S^4, defined with the orientation local system when S_i is nonorientable. A cover f: W -> S^4 has finite degree d and **exact** branch locus S. In particular each component is genuinely branched somewhere, hence everywhere at some sheet. Unbranched sheets over a branch component are allowed. The cover need not be regular, cyclic, or simple.

For connected W, choose its orientation to make the covering positive away from S. Nothing in the nonexistence tests requires the problem to prescribe this orientation in advance: the test manifolds have signature zero or nonzero regardless of orientation. All test manifolds below are closed, connected, smooth and orientable.

The classical source results used here are:

- [IP] gives a simple degree-five representation of each closed orientable PL four-manifold using a branch surface that can vary with the manifold.
- [PZ] supplies a fixed orientable ribbon surface in B^4 for compact orientable four-dimensional 0/1/2-handlebodies. Its reduced version has an annulus and two discs. This is a relative-boundary problem, not the present closed one.
- [Viro] supplies the smooth branched-cover signature formula. [GKS, Theorem 1] extends that formula to closed topological four-manifolds with a locally flat embedded branch surface.

These results are imported, not reproved or claimed as new. The following deductions and proofs are authored for this packet.

## 2. Cycle data, Euler characteristic and signature

Choose a meridian of each S_i. Its permutation on the d sheets has c_{i,k} cycles of length k, including fixed points as length-one cycles. These cycle counts are well-defined: changing paths conjugates the permutation, and reversing a meridian replaces it by its inverse. Neither operation changes the cycle type.

Define

    c_i = sum_k c_{i,k},
    r_i = d - c_i = sum_k (k-1)c_{i,k},
    a_i = sum_k ((k^2-1)/(3k))c_{i,k}.

Then sum_k k c_{i,k}=d. Exact branching implies 1 <= r_i <= d-1 and a_i>0. In particular d>=2 if S is nonempty.

### Proposition 2.1: Euler formula

For every cover in the stated category,

    chi(W) = 2d - sum_i r_i chi_i.                    (E)

Proof. Cut S^4 into its surface stratum and complement, or use a tubular neighborhood and additivity of Euler characteristic. Over the complement the map is d-to-one. Over S_i, its full inverse image is an unbranched c_i-sheeted covering of S_i: a length-k meridian cycle supplies one local point over the branch stratum, and motion along S_i can permute these points. Thus this inverse image has Euler characteristic c_i chi_i. Additivity, with compactly supported Euler characteristic on the open complement, gives

    chi(W) = d(2 - sum_i chi_i) + sum_i c_i chi_i,

which is (E). Equivalently the same calculation uses compact exteriors and disc bundles; their three-dimensional common boundaries have Euler characteristic zero. This also avoids interpreting ordinary Euler characteristic of an arbitrary open stratum. QED.

### Proposition 2.2: signature formula in downstairs cycle data

Under compatible orientations,

    sigma(W) = -sum_i e_i a_i.                       (S)

Justification of the conversion. Let A be a connected ramification component over S_i, with transverse local degree k and degree m as an ordinary covering A -> S_i. Its normal disc bundle maps to the pullback of the normal disc bundle of S_i with fiber degree k. The Euler obstruction of an oriented circle bundle multiplies by k under this fiber map. The same statement holds with the orientation local system. Pairing on A therefore gives

    k e(A in W) = m e_i.

The sign is positive because the ambient orientations are compatible; equivalently this identity follows by counting the pulled-back normal-section zeros with their local indices. Sum m over ramification components of index k above S_i. It equals c_{i,k}, the number of points of this index over one point of S_i. Thus their aggregate upstairs normal Euler number is c_{i,k} e_i/k.

The imported formula is

    sigma(W) = d sigma(S^4) - sum_{k>=2} ((k^2-1)/3)e(A_k in W).

Since sigma(S^4)=0, substitution gives (S). In the smooth category, this is also directly [Viro, formulas (17)–(18)]: the denominator is 3 for upstairs embedded normal Euler numbers and 3k for the downstairs immersed normal Euler numbers. These two quantities must not be conflated. QED, conditional only on the cited signature theorem.

Checks: simple branching has cycle type (2,1,...,1), so r_i=1 and a_i=1/2. A meridian which is a product of two disjoint transpositions has r_i=2 and a_i=1. It is not simple even though every nontrivial local index is two.

## 3. Opposite normal-Euler signs are necessary

### Theorem 3.1

If S is universal, some component has positive normal Euler number and another has negative normal Euler number. Consequently at least two components are nonorientable.

Proof. If every e_i vanishes, (S) makes the signature of every total space zero. This excludes CP^2, whose signature in either orientation is nonzero.

Suppose at least one e_i is nonzero but all nonzero e_i have the same sign. Since each a_i is strictly positive for exact branching, sum_i e_i a_i is nonzero for every such cover. Then (S) excludes S^4, whose signature is zero. This argument does not require both orientations of CP^2 as separate target objects.

Therefore there must be nonzero normal Euler numbers of opposite signs. An orientable closed surface in S^4 has normal Euler number equal to its self-intersection. Its homology class is zero because H_2(S^4;Z)=0, so its normal Euler number vanishes. The two components with nonzero e_i are nonorientable. QED.

This sharpens the elementary connected-locus obstruction into a useful sign test. It does not assert an optimal lower bound on the number of components.

The exact-locus hypothesis matters. If one silently allows S_i to be a dummy, everywhere unbranched component for an individual covering, a_i may vanish and the same-sign exclusion of S^4 does not follow. That altered formulation is not used here.

## 4. Positive Euler mass and a three-component lower bound

Set

    P(S) = sum_i max(chi_i,0).

For a closed connected surface positive Euler characteristic means either S^2, contributing two, or RP^2, contributing one.

### Proposition 4.1

For every cover with exact branch locus S,

    chi(W) >= (2-P(S))d + P(S).                     (B)

Proof. For chi_i>0 use r_i<=d-1 in (E). For chi_i<=0 the contribution -r_i chi_i is nonnegative and may be discarded for a lower bound. Hence

    chi(W) >= 2d - (d-1)P(S).

QED.

### Corollary 4.2

Universality implies P(S)>=3.

Proof. If P=0, (B) gives chi(W)>=2d>=4. If P=1, it gives chi(W)>=d+1>=3. If P=2, it gives chi(W)>=2. Each case excludes S^1 x S^3, whose Euler characteristic is zero. QED.

### Corollary 4.3

Universality implies that S has at least three connected components.

Proof. Theorem 3.1 requires at least two nonorientable components. If there were exactly two, each would have Euler characteristic at most one, yielding P<=2, contrary to Corollary 4.2. Zero or one component is already excluded. QED.

### Corollary 4.4: explicit growth of degree

Suppose P>2 and W_g is the connected sum of g copies of S^1 x S^3, with g>=1. Any covering of W_g over this fixed S satisfies

    d >= ceil(1 + 2g/(P-2)).

Proof. A connected sum of closed four-manifolds subtracts two from the sum of their Euler characteristics. Thus chi(W_g)=2-2g. Substitution in (B) and rearrangement gives the result. QED.

These bounds exclude many surfaces, but they do not exclude all surfaces. In particular, the conditions “at least three components” and “P>=3” are not sufficiency statements.

## 5. Degree and simplicity cannot be fixed

### Proposition 5.1: bounded degree gives only finitely many total spaces

Fix a smooth or locally flat PL S. In any fixed degree d there are finitely many covers up to equivalence, hence finitely many underlying total spaces in the corresponding category.

Proof. Its compact exterior has finitely generated fundamental group G. If G has g generators, a homomorphism G -> Sym(d) is determined by at most g permutations; there are at most (d!)^g possibilities before imposing the relations, transitivity, or peripheral conditions. An ordinary cover of the complement is determined by its monodromy up to conjugacy. Its standard branched completion, when it is in the category under consideration, is determined by that ordinary cover. Thus the finite monodromy list bounds the possible completions. QED.

The same argument applies topologically whenever the compact locally flat exterior has finitely generated fundamental group and one uses the usual unique branched completion. The PL/smooth case is sufficient for the present obstruction.

Consequently no uniform upper degree bound can realize the infinitely many distinct W_g. Distinctness follows already from their first Betti numbers, equal to g. The degree-five theorem [IP] does not contradict this: it changes S with W.

### Proposition 5.2: simple coverings alone cannot be universal

For fixed S, a simple d-fold cover satisfies

    chi(W)=2d-chi(S),   sigma(W)=-e(S)/2.

Proof. Set r_i=1 and a_i=1/2 in (E) and (S). QED.

As d>=2, the Euler characteristics are bounded below by 4-chi(S), excluding W_g for large g. Independently, all simple covers over fixed S have the same signature, so they cannot realize both S^4 and CP^2. Increasing d alone does not repair either restriction. A strategy must vary genuinely nonsimple monodromy.

This does not say that high local ramification index is necessary. Products of multiple disjoint transpositions are nonsimple and can have large defects while keeping every ramification index equal to two. The index-two modification mentioned in [PZ] must not be mistaken for a simple-cover construction.

## 6. The complement group must be large

A group is called large if a finite-index subgroup surjects onto the free group F_2.

### Theorem 6.1

If S is universal, pi_1(S^4 minus S) is large.

Proof. Apply universality to W_2 = (S^1 x S^3)#(S^1 x S^3). Van Kampen gives pi_1(W_2)=Z*Z=F_2. Let A=f^{-1}(S). Removing the closed codimension-two submanifold A from W_2 leaves a connected manifold: paths can be perturbed off A. The ordinary covering

    W_2 minus A -> S^4 minus S

therefore identifies H=pi_1(W_2 minus A) with an index-d subgroup of G=pi_1(S^4 minus S).

Inclusion W_2 minus A -> W_2 induces a surjection on pi_1. To see this directly, represent each loop by a path transverse to A. Since a one-dimensional path and a two-dimensional submanifold in a four-manifold have negative expected intersection dimension, a small perturbation misses A. The same conclusion follows by adjoining the normal disc bundles: this kills meridians rather than creating fundamental-group generators. Thus H surjects onto F_2. QED.

In particular, finite and virtually solvable complement groups are excluded. Subgroups and quotients of virtually solvable groups are virtually solvable, whereas F_2 is not: every finite-index subgroup of F_2 is free of rank at least two and is not solvable. This is stronger than merely checking that the complement group is nonabelian.

Largeness is necessary, not sufficient. A surjection from a finite-index subgroup to a desired group need not arise by killing precisely the ramification meridians of a branched completion; and matching a fundamental group does not identify a four-manifold.

## 7. Doubling the four-ball construction does not solve the problem

Take a proper orientable ribbon branch surface F in B^4 from [PZ]. Reflect B^4 and double along the boundary. The doubled surface D(F) is closed and orientable. For the three-component version, its components are a torus and two spheres.

### Proposition 7.1

Every closed cover of S^4 with exact branch locus D(F), in the stated category, has signature zero. Hence D(F) is not universal.

Proof. Each orientable component in S^4 has e_i=0. Equation (S) applies without any simplicity assumption and yields zero. In particular CP^2 is excluded. QED.

For a cover M -> B^4, direct doubling gives D(M)=M union_boundary (-M) -> S^4. Its signature is also zero by additivity or by the orientation-reversing involution interchanging the two halves. Thus direct doubling does exactly what the signature calculation predicts; it does not preserve an arbitrary closed W obtained by adding three- and four-handles to M.

Here is the missing relative condition for a gluing strategy. One would need fixed proper surfaces F_+ and F_- in the two balls, with a fixed boundary identification, such that for **every** desired decomposition W=M union_phi C there are equal-degree covers of M and C whose boundary monodromies agree (up to a single sheet conjugacy) under that identification, and whose lifted boundary gluing is the prescribed phi. Their union must remain a fixed embedded surface with the appropriate local models. The maps must genuinely branch along every intended component.

An existential boundary link cover or a boundary diffeomorphism of M does not supply this compatibility. The known four-ball universality statement does not assert the required simultaneous extension over an arbitrarily chosen cap. Furthermore orientable choices on both sides that glue orientably are already excluded by Proposition 7.1. We do not construct a compatible nonorientable cap system, and we do not prove one impossible.

## 8. Exact controls and unresolved work

`controls.py` enumerates every integer partition of degrees 1 through 18, using rational arithmetic to check defects and signature weights. It also exhaustively tests the elementary Euler bound for three-component Euler tuples in {-2,-1,0,1,2} and all defects for degrees 2 through 9; same-sign signature cancellation; the two-nonorientable-component Euler obstruction; and the derived degree growth inequalities in a specified finite box. Its range and counts are in `CONTROL_RESULTS.json`.

The arithmetic relaxation deliberately accepts the formal data

    d=3, (chi_i)=(1,1,2), (e_i)=(2,-2,0),
    meridian cycles (2,1), (2,1), (3),

with chi=0 and sigma=0. This is not an actual cover or an embedded surface construction. It demonstrates why the scalar inequalities alone are not a general nonexistence proof: they forget group relations, peripheral compatibility, transitivity and geometric realization. The controls neither establish nor refute realization of this example.

The unresolved target is still the existence of a single suitable disconnected surface and realizable nonsimple monodromies for every closed orientable four-manifold. No candidate meets that universal requirement here. Conversely, the obstructions do not exhaust all possible embedded surfaces. Five distinct approaches have produced partial results and identified gaps, rather than a proof or counterexample to KP-4.122.

## References

[K3] R. Inanc Baykur, Robion C. Kirby, Daniel Ruberman, *K3: A New Problem List in Low-Dimensional Topology*, April 2026 author version, Problem 4.122, pp. 291–292. https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf

[PZ] Riccardo Piergallini and Daniele Zuddas, *A universal ribbon surface in B^4*, Proc. London Math. Soc. 90 (2005), 763–782. https://doi.org/10.1112/S0024611504015072 ; inspected author preprint: https://arxiv.org/abs/math/0308222

[IP] Massimiliano Iori and Riccardo Piergallini, *4-manifolds as covers of the 4-sphere branched over non-singular surfaces*, Geometry & Topology 6 (2002), 393–401. https://doi.org/10.2140/gt.2002.6.393 ; https://arxiv.org/abs/math/0203087

[Viro] O. Ya. Viro, *Signature of a branched covering*, Mathematical Notes 36 (1984), 772–776, especially formulas (17)–(18). https://doi.org/10.1007/BF01156467 ; inspected public scan: https://www.maths.ed.ac.uk/~v1ranick/papers/viro3.pdf

[GKS] Christian Geske, Alexandra Kjuchukova and Julius L. Shaneson, *Signatures of topological branched covers*, International Mathematics Research Notices 2021, 4605–4624, Theorem 1. https://academic.oup.com/imrn/article/2021/6/4605/5880468 ; inspected v3: https://arxiv.org/abs/1901.05858

[BPZ] Valentina Bais, Riccardo Piergallini and Daniele Zuddas, *Branched coverings of simply connected 4-manifolds*, arXiv:2605.26337v2 (2 July 2026), Theorem A. https://arxiv.org/abs/2605.26337
