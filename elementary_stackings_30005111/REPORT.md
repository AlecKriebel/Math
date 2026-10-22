# Row 1840: closed-walk stackings

## Outcome
The unrestricted statement in Oberwolfach Report 22/2022, p. 1225, is false under the standard projection-preserving continuous-embedding definition when immediate backtracking is permitted. A ten-edge counterexample on the three-vertex path is given below. This does not contradict Louder–Wilton: their stacking existence theorem assumes an immersion. For that actual scope, `immersed_elementary_proof.md` gives a finite elementary proof using integer edge weights and a strictly increasing vertex count, avoiding an appeal to the maximal cyclic tower theorem. No claim of novelty or literature priority is made.

## Exact counterexample
Let G be the path a—v—b. Set

W = v a v b v a v b v a v.

Label the five visits to v by 0,1,2,3,4 in domain cyclic order. The five leaf excursions are a,b,a,b,a. Each edge occurrence maps homeomorphically onto its edge; heights may be arbitrary continuous functions. The question is whether there exists h on the domain circle such that (W,h) is an embedding.

### Nonperiodicity
Any period of the edge walk must send a visit to v to a visit to v, so its length is even. A proper period dividing the total length 10 must consequently be 2. That would make all five excursions identical, whereas both leaves a and b occur. Thus W is not a proper repetition. This argument concerns combinatorial repetition, not the homotopy class: all walks in this tree are null-homotopic.

### Same-leaf interval lemma
Suppose an embedding exists. Consider two distinct excursions to the same leaf. Each excursion has two continuous height strands over the open leaf edge, and both strands converge at the leaf to the height of its own leaf visit. The two leaf visits have distinct heights. If the first leaf height is lower, both of its strands lie below both strands of the second excursion sufficiently near the leaf. A pair of strands cannot change vertical order anywhere in the open edge, since equality would violate injectivity. Taking limits at v shows that the entire closed interval between the first excursion's central endpoint heights lies below that of the second. Equality between their interval endpoints is possible only for a shared domain central visit. In particular, the intervals have disjoint interiors.

This is a statement about continuous embeddings. It does not assume affine strands on the original edges, differentiability, or a drawing perturbation.

### Contradiction
Write h_i for the five distinct central heights. The a-excursions connect pairs (0,1), (2,3), and (4,0). The intervals [h_0,h_1] and [h_4,h_0] have disjoint interiors, so h_4,h_0,h_1 are strictly monotone (in either direction). Their union is the interval spanned by those three heights. The interval [h_2,h_3] must have disjoint interior from both, hence it lies wholly below or wholly above that union; all five heights are distinct. Therefore the sets of heights indexed by {4,0,1} and by {2,3} are separated by a nonempty open gap.

The two b-excursions connect (1,2) and (3,4). Both of their height intervals contain that same gap. This contradicts the same-leaf interval lemma. No continuous stacking exists.

## Five substantive approaches

1. **Strand-order constraints.** Derived the same-leaf interval lemma directly from arbitrary continuous strands. It yields the exact obstruction above. General graph edge tests must allow endpoint ties when two traversals share one domain vertex; disallowing these falsely rejects the stackable one-edge out-and-back.
2. **Cyclic-word primitivity and lexicographic heights.** Repetition is ruled out by the continuous difference h(τt)-h(t), whose sign is constant but whose cyclic sum telescopes to zero. Lexicographic ordering of forward cyclic tails works for positive directed words, because shifting equal first letters preserves order, but does not directly handle inverses. For the reduced commutator a b A B with alphabet order a<b<A<B, the forward-tail ranks are 0,1,2,3; the two b-strands have opposite endpoint order, so this naive assignment fails. The actual counterexample is combinatorially primitive despite representing the identity in the tree's fundamental group.
3. **Graph-cover/tower elimination.** Produced a finite elementary proof for primitive immersions: choose a non-gradient integral edge cochain with zero walk sum, split visited vertices by cumulative level, and iterate. Every step strictly increases the number of visited vertices, bounded by domain length. Minimum degree at least two forces the terminal rank-one graph to be a circle; nonperiodicity makes its lift a homeomorphism. Explicit small height perturbations descend the stacking. See the companion proof.
4. **Small exact search.** Independent auditor enumerated all 5!=120 central-height orders for the excursion word ababa; none satisfy same-color interval disjointness. Shorter primitive binary excursion words have feasible orders. This finite search supports but is not needed for the analytic proof. The auditor supplies reproducible standard-library scripts and results in audit/. In addition, check_cochain.py implements the constructive proof with a spanning-tree chord basis and exact rational heights. It passes all cyclically reduced two-generator rose words through length seven: 3,228 primitive cases and 64 proper-power negative controls. It also passes 372 subdivided-loop cases, which include parallel edges and reverse traversals. Each positive certificate is checked for distinct vertex heights and unchanged strict ordering along every pair of occurrences of a common original edge. The commutator a b A B receives heights (0,1,4/3,1/3). Full output is cochain_results.json. These tests corroborate the proof but do not replace it.
5. **Spur/backtracking scope.** The walk v a v is nonimmersed but does admit an oval-shaped stacking, so missing immersion is not itself a disproof. The length-ten example is a genuine obstruction. The immersive theorem remains valid and is treated separately, rather than conflated with the broader printed statement.

## Source and priority checks
- Oberwolfach Report 22/2022, p. 1225, Pokrovskiy's Problem 3: https://publications.mfo.de/bitstream/handle/mfo/3964/OWR_2022_22.pdf . The printed statement uses closed walks with no explicit no-backtracking hypothesis; its attribution says “Louder and Witten,” while the cited relevant work is by Louder and Wilton.
- Louder–Wilton, *Stackings and the W-cycles conjecture*, accepted manuscript, May 26, 2016: https://discovery.ucl.ac.uk/1493364/1/elevations-cmb-2016-05-26.pdf . Definition 8 requires a projection-preserving embedding. The manuscript's Lemma 17 proves existence for primitive immersions, using cyclic towers; numbering differs from the published Lemma 3.4.
- Published DOI: https://doi.org/10.4153/CMB-2016-078-3 . Repository metadata: https://www.repository.cam.ac.uk/handle/1810/262356 . Original preprint: https://arxiv.org/abs/1410.2540 .
- Targeted searches for elementary stacking proofs, the exact closed-walk phrase, and maximal cyclic towers found the source proof and later thesis expositions, but did not establish a prior publication of the counterexample or this finite reformulation. A negative search is not proof of novelty. No stronger literature claim is warranted.

## Interpretation boundary
If the intended convention silently restricts “closed walk” to cyclically reduced walks, the counterexample is outside that convention and the correct deliverable is the elementary immersed proof. If all graph-theoretic closed walks are intended, the printed equivalence needs correction. Neither result should be represented as a disproof of Louder–Wilton.
