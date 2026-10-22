# Tree-action closure audit

Checkpoint: **2026-10-17 21:30 UTC**. Discovery estimate toward 21.140: **10%**.
This is a checked structural lemma, not a solution or a novelty claim.
The parent proposed the mechanism; this file independently checks its cases.

## Statement

**Lemma T.** For every action of standard Thompson `F` on a nonempty simplicial
tree, there is a subgroup `F_0 <= F` isomorphic to `F` that fixes a vertex after
barycentric subdivision. If the action has no edge inversions, it fixes an
original vertex.

**Corollary.** If a group acts without inversions on a tree and every vertex
stabilizer contains no copy of `F`, then the group contains no copy of `F`.
In particular, the fundamental group of any abstract graph of groups whose
vertex groups all exclude `F` also excludes `F`. This includes arbitrary
amalgamated free products and HNN extensions with injective edge maps and
vertex groups excluding `F`; no finiteness assumptions on the graph or edge
groups are required for this implication.

## Primary inputs verified

1. Brin–Squier, *Groups of piecewise linear homeomorphisms of the real line*,
   Invent. Math. 79 (1985), Theorem (3.1), printed p.494, proves that the finite
   piecewise-linear group contains no nonabelian free subgroup. It applies to
   `F` by extension by the identity outside `[0,1]`.
   [Primary paper](https://pi.math.cornell.edu/~justin/Limited2Cornell/PLoI.pdf).
2. Culler–Morgan, *Group actions on R-trees*, Proc. London Math. Soc. 55 (1987),
   define reducible actions on printed p.573 as: every element elliptic, an
   invariant line, or a fixed end. Their Theorem 2.7, pp.582–583, proves that
   an irreducible action with nonzero translation length function contains a
   rank-two free group. Their Lemma 1.5, p.577, says that disjoint characteristic
   sets force a positive translation length for the product; Corollary 2.3,
   p.580, identifies the length in the fixed-end case with the absolute value
   of a real character.
   [Primary paper](https://marc-culler.info/static/home/papers/RTrees.pdf).
3. Cannon–Floyd–Parry, Theorems 4.1 and 4.5 and Lemma 4.4: `F'` is simple,
   consists of elements trivial near 0 and 1, and contains a copy of `F`
   supported in `[1/4,1/2]`. In particular `F'` is nonabelian and perfect.
   [Primary paper](https://www.imo.universite-paris-saclay.fr/~emmanuel.breuillard/Cannon.pdf).

For the last perfectness deduction: the embedded interval copy of nonabelian
`F` ensures `[F',F'] != 1`; this is a normal subgroup of simple `F'`, so
`[F',F']=F'`.

## Proof and adversarial case audit

Replace the tree by its barycentric subdivision so that the action has no edge
inversions. Give every edge length one. The action of `F` has no nonabelian
free subgroup by input 1. If it has a nonzero translation length function,
input 2 rules out an irreducible action. Thus the following cases cover every
action.

**All elements elliptic.** Let `a,b` be the usual generating pair of `F`.
If their fixed subtrees were disjoint, input 2's Lemma 1.5 would make `ab`
hyperbolic, contrary to the present case. Therefore they fix a common point.
For a simplicial action without inversions, they then fix a common vertex.
Here one can take `F_0=F`.

**Invariant line.** The induced map to the isometry group of the line kills
`F'`: its image on `F'` is perfect, whereas the line isometry group is soluble
(translations form an abelian normal subgroup with quotient of order at most
two). Every perfect subgroup of a soluble group is trivial. Thus `F'` fixes
the line pointwise, and the interval copy `F_0` from input 3 fixes any vertex
of that line. If the invariant metric line were first described in a geometric
realization, it is a union of simplicial edges, so it contains vertices.

**Fixed end.** Let `e` be the end. Fix a simplicial ray `R=(v_0,v_1,...)`
tending to `e`. For each `g` preserving `e`, the rays `R` and `gR` have a
common tail, so there is an integer `chi(g)` such that, for sufficiently large
`i`, `g v_i = v_(i+chi(g))`. Comparing tails shows
`chi(gh)=chi(g)+chi(h)`. Thus `chi:F -> Z` is a homomorphism. In particular,
`chi(g)=0` for `g in F'`, and such a `g` fixes a tail of `R` pointwise.

Take the **finitely generated interval copy** `F_0 <= F'` from input 3, and
let `u,v` be its two generators. Each fixes a tail of the same `R`. The two
tails intersect in a tail, and any vertex on that intersection is fixed by
both `u,v`, hence by `F_0`.

This argument does **not** assert that `F'` is finitely generated or that the
whole `F'` fixes a vertex in the fixed-end case. Neither assertion is needed.
It also does not assert property `FA` for `F`: the quotient `F -> Z` supplies
an action on a line without a global fixed vertex. The conclusion concerns a
subcopy of `F` in a stabilizer.

These cases prove Lemma T. For the corollary, restrict a group action to a
purported embedded `F`; Lemma T supplies a subcopy contained in a vertex
stabilizer, contrary to its hypothesis. For a graph of groups, use the usual
Bass–Serre tree, whose vertex stabilizers are conjugate to the vertex groups.
QED.

## Consequence for the research program

Combining Lemma T with the product, extension, and directed-union closure
lemmas in `approach_structure.md` shows that the absence of `F` survives many
standard embedding constructions. This is useful for screening an explicit
construction; it does **not** furnish geometric `F_infinity` for its output.
The classical rope-trick obstruction in the main structural note explains one
specific failure of that missing finiteness step.

Parent review is required before promotion. The lemma has not been claimed as
novel, and no external communication or publication action has occurred.
