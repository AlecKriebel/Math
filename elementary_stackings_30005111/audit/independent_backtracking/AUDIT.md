# Independent adversarial audit: the backtracking walk ababa

Date: 2026-10-21 UTC.

## Verdict and scope

**PASS:** The length-ten combinatorial closed walk

    v a v b v a v b v a v

on the path a—v—b is not a nontrivial repetition of a shorter closed walk, even after cyclic rotation or reversal, and has no continuous projection-preserving embedding into G × R. No piecewise-linearity, affine interpolation, differentiability, or monotonicity of the height function is assumed.

This disproves the assertion “every nonpower closed walk stacks” if “closed walk” permits immediate backtracking and “nonpower” means nonrepetition of the actual parametrized/combinatorial walk. It does **not** disprove the primitive-immersion stacking theorem. Nor is it a counterexample with a nonpower fundamental-group element: the graph is a tree, so the represented element is the identity. The term “primitive” here must not be read as “belongs to a free basis.” Any application to a source statement must establish which meaning that source uses.

## Formal setup

Regard the domain as a circle with ten consecutive edges, mapped homeomorphically on each open edge to the indicated target edge. Label its five distinct visits to v by c0,...,c4, in their cyclic order, and its five distinct leaf visits by t0,...,t4. Excursion i runs from ci to ti to c(i+1), with indices modulo 5. Excursions 0,2,4 visit a; excursions 1,3 visit b.

A proposed stacking is a continuous function H on the domain circle such that F(s) = (W(s),H(s)) is an embedding. In particular, hi = H(ci) are pairwise distinct. Heights of distinct visits to the same leaf are also pairwise distinct. Since the domain is compact and G × R is Hausdorff, injectivity would already imply embedding.

## Arbitrary-continuous-height interval lemma

Take two different excursions E and E' to the same leaf. Parametrize their common target edge by x in [0,1], with x=0 at v and x=1 at the leaf. Each excursion has an outgoing and an incoming branch. Composing H with the inverse target-edge parametrization gives continuous real functions f0,f1 for E and g0,g1 for E' on [0,1]. These functions are not assumed monotone or linear.

At x=1, f0(1)=f1(1)=u and g0(1)=g1(1)=u', where u≠u', because the two leaf visits are distinct domain points. Suppose u<u'; reverse the labels otherwise. Continuity gives fα(x)<gβ(x) for x sufficiently close to 1, simultaneously for α,β in {0,1}.

For every x in (0,1), the four branch points are distinct domain points. Injectivity of F therefore implies fα(x)≠gβ(x). Each continuous difference fα−gβ is nonzero on the connected interval (0,1), and hence has constant sign. Its negative sign near 1 consequently holds throughout (0,1). Taking limits at 0 gives

    max(f0(0),f1(0)) ≤ min(g0(0),g1(0)).

Thus the intervals spanned by the central endpoint heights of the two excursions have disjoint interiors. A common endpoint height can occur only when the excursions share the very same domain visit to v. This is exactly the allowed equality for excursions 4 and 0; it does not invalidate the lemma.

There is no appeal to planar intuition or to strand-height monotonicity. The only monotonicity used is the fixed topological parametrization of an individual traversal of a graph edge.

## Contradiction for ababa

Let Iij denote the closed real interval with endpoints hi and hj. The three a-excursion intervals are I01, I23, I40.

I01 and I40 share h0 and have disjoint interiors. Their other endpoints are distinct from h0 and each other. It follows that either h4<h0<h1 or h1<h0<h4. Their union J is the single interval between h1 and h4.

I23 must have interior disjoint from both I01 and I40. Because h2 and h3 are distinct from h0,h1,h4, neither endpoint can be in J: an endpoint in the interior of either of its two subintervals would force an open overlap, while equality with their endpoints is excluded. Also h2,h3 cannot be on opposite sides of J, as then I23 would contain the interior of J. Thus I23 is strictly above J or strictly below J.

The b-excursion intervals are I12 and I34. If I23 is above J, both I12 and I34 contain the nonempty open gap

    (max(h1,h4), min(h2,h3)).

If I23 is below J, both contain the nonempty open gap

    (max(h2,h3), min(h1,h4)).

Either case contradicts the same-leaf interval lemma for the two b excursions. Therefore no such continuous H exists.

## Nonpower under cyclic rotation and inversion

Orient the target edges from v toward their leaves. In the directed-edge word, v→a occurs exactly three times and v→b exactly twice. If the word were U repeated k times for k≥2, each directed-edge count would be divisible by k. This would require k to divide both 3 and 2, impossible.

Cyclic rotation preserves these counts. Reversal replaces directed edges by their inverses, but the inverse counts are also 3 and 2. Hence the same argument excludes proper powers after any cyclic rotation or inversion. An actual factorization of this parametrized walk through a degree-|k| circle covering, |k|≥2, likewise repeats all regular edge-point preimages |k| times and is excluded by the counts. This is a statement about the actual map, not its homotopy class.

## Independent exhaustive corroboration

The accompanying standard-library script does not import the original checker. It performs two exact tests:

1. Enumerate all 5! = 120 strict orders of the central heights. For each, list every pair of same-leaf excursions whose endpoint intervals have intersecting interiors. Every order has at least one violation; zero orders pass.
2. Independently enumerate all 5!·3!·2! = 1,440 strict vertex-fiber orders, including the three a-leaf visits and two b-leaf visits. For every target edge, orient every traversal from v toward its leaf. If two strands have endpoint pairs (x1,y1),(x2,y2), the necessary noncrossing inequality is (x1−x2)(y1−y2)≥0. Zero complete orders satisfy all inequalities. For each central order, the existence/nonexistence of an accepted leaf order agrees with the interval test.

The script also checks all ten directed-edge cyclic rotations and all ten cyclic rotations of the inverse word for every proper word period dividing length ten. No proper period occurs.

The 120-order test is corroboration, not a replacement for the arbitrary-continuous-height proof. Ranks suffice because the necessary conditions depend only on strict ordering within each vertex fiber.

## Reproduction and receipt

Run from this package root:

    python audit/independent_backtracking/verify_ababa.py

Expected counts: central_orders_checked=120; accepted_central_orders=0; complete_vertex_orders_checked=1440; accepted_complete_vertex_orders=0; rotation_and_inverse_variants_checked=20.

The full receipt records all 120 central orders, every overlapping same-leaf excursion pair, and all 20 nonpower checks.

- Original pre-hardening script SHA-256: 8a1383503d36f4a14b2f1c620c1e9e40e75db4e88072b2a24631da8525477260
- Receipt SHA-256: 3e495f1ba9aec0aa7c85e68b353b1eaab330951a6b9c4c61954a6442bf762693

No repository publication, queue change, or external mutation was performed.

The publication script replaces optimization-removable assertions with explicit guards. See provenance/guard_transformation.json and the corresponding patch. The receipt is unchanged; the current script hash is recorded in MANIFEST.json.
