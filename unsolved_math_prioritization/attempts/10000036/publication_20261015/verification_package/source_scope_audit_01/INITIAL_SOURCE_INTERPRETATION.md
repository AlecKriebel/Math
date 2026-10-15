Saved 2026-10-15T06:20:56.789163+00:00

# Initial source interpretation (saved before old audit verdicts)

Frozen PR head: ed2de7249953ba0c1afad253adca9b820d7297c5. Problem 10000036. This memo was saved before reading either frozen old independent-review verdict. It records source reconstruction, not a proof acceptance or a current-priority conclusion.

## Authenticated historical question

Saint-Flour author notes, printed/PDF p.61, item 8.15 asks:

> Is there an invariant finite energy percolation X on Z^d, which a.s. percolates and satisfies p_c(X) = 1?

The archive bytes inspected here have 1,101,523 bytes and SHA-256 aaab65b3acf65f4d21657da94464e9d5edb93969a4c353805099a220a0717cfe. Current author URL returned 404; my archive GET timed out; the parent independently retrieved the exact pinned archive over normal public HTTP. This audit verified that file's hash and inspected pages 59, 61, and 33 as rendered PNGs, alongside extracted pages 32-33 and 59-61. Provenance must remain transparent: no successful current-author retrieval is claimed.

## Scope reconstructed from checked primary material

- The process is an edge process on the nearest-neighbor lattice. Section 8.2, p.59 and Definition 8.9 explicitly place invariant percolation on {0,1}^E and require all graph automorphisms. The nearby Exercise 8.17 explicitly specifies site percolation, reinforcing the distinction. A site example alone does not settle this bond question.
- The notes do not give a local definition of finite energy. Full extracted-text search found the term near item 8.5, item 8.15, and a uniqueness discussion, with no uniform conditional bound. The exact earlier question is BHS Question 1.1, arXiv math/9906002v1 p.2: there finite energy means both insertion and deletion tolerance, with strict positivity of each edge's conditional probability given all other edges. BT arXiv 1505.06069v1 p.3, Question 1 and the next paragraph explicitly repeat the same convention. This is ordinary nonuniform finite energy, not uniform finite energy. That interpretation is supported jointly by these sources; the Saint-Flour line in isolation leaves the term undefined.
- The dimension range is implicit in the Saint-Flour sentence. The BHS surrounding criticality discussion and BT's explicitly stated lattice framework identify the substantive range d >= 2. The author claim for every integer d >= 2 therefore covers either an existence-in-some-d reading or a dimension-by-dimension reading. Do not silently include d=1, where this construction has no one-ended spanning-tree input.
- Almost-sure percolation means existence of at least one infinite component in almost every realized graph. It does not mean the origin, or every vertex, lies in an infinite component a.s. BHS explicitly permits finite components in the motivating insertion-tolerant example. The question imposes no everywhere-percolating hypothesis. The notes' earlier root-event discussion must not be used to make an incompatible root-a.s. strengthening.
- p_c(X) is the Bernoulli bond threshold of the realized graph, with fresh independent edge thinning. BHS p.1 defines p_c for arbitrary infinite G by positive probability of any infinite cluster. This resolves the extension needed when X is disconnected; Saint-Flour Definition 4.2 p.33 by itself is rooted and then restricted to connected graphs. The correct claim is quenched for almost every X, at every p<1, plus percolation at p=1. Finite components are harmless and the unique infinite component asserted by the candidate has the same threshold.
- Neither uniqueness, ergodicity nor mixing appears as a target hypothesis in item 8.15. The author asserts these additional properties.

## Dependencies and relation to other results

BHS's everywhere-percolating fixed-density sprinkling conjecture and BT Theorem 1 concern preserving all original edges and adding independent Bernoulli edges of one fixed positive density. BT p.2, item (ii), gives p_c<1 in that class and p.3 still poses the general finite-energy threshold-one question. Thus this theorem does not rule out an arbitrary ordinary finite-energy process. The author kernel deletes tree edges and gives non-tree edges environment-dependent probabilities; it does not satisfy the stated sprinkled-base hypothesis merely by being conditionally independent given T.

HM is a 2009 published site paper (arXiv deposit 2010). The published EMIS PDF was retrieved normally and inspected on printed pp.43,45,46. Its Section 2 gives the relevant antecedent mechanism: one-ended UST geometry and summable environment-dependent flips preserve infinite tails. Its printed p.46 explicitly attributes p_c=1 to the pre-flip graph X-hat, not automatically to the finite-energy post-flip X-bar. No full-target resolution can be quoted directly from that passage. No firstness conclusion is made; a fresh mathematical reduction of HM's site example is outside this audit and deep priority work is deferred.

Timar arXiv 1805.10690v1 pp.1-2, Theorem 1 and the factor definition, supply a measurable isomorphism-equivariant factor-of-iid one-ended spanning tree under the stated ergodic amenable unimodular one-ended assumptions; deterministic rooted Z^d, d>=2, meets them. Pemantle math/0404043v1 Theorems 2.3 and 4.3 give a separate low-dimensional (2<=d<=4) tree input; the high-dimensional USF cannot be substituted for a connected tree. These are established-existence inputs; the candidate's subsequent perturbation and all its claims still require mathematical audit.

## Initial conclusion

No exact-source scope mismatch is found between the historical ordinary finite-energy bond question and the author's Section 1 theorem. Conditional on independent validation of that theorem, ordinary nonuniform finite energy would answer the full historical question. This memo does not certify that the theorem is correct, new, first, or currently open. Published BT PDF routes tried so far returned HTML, 404, or tool failure, so exact BT wording is certified here for its pinned arXiv v1 rather than silently attributed to the inaccessible final.
