# Independent early seal: recovered primary target

Stage: PARTIAL-RESULT REVIEW ONLY. This is a source and scope adversary, not a new proof search.

Before this seal I read only the fresh recovered author PDF (and PDF tooling instructions), pages 5, 32–33, and 75–76. I have not read prior reviews, author code/results, readiness, package history, root findings, or sibling findings.

## Literal source and inherited hypotheses
The fresh PDF has 115 pages, 1,101,523 bytes, SHA-256 aaab65b3acf65f4d21657da94464e9d5edb93969a4c353805099a220a0717cfe. Direct requested retrieval: https://arquivo.pt/noFrame/replay/20201231041548id_/http://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf . The web extraction tool failed; a literal HTTP retrieval succeeded and the page 76 image was inspected.

Problem 9.49 is the infinite-fiber-intersection question on G × Z under pc(G)=1. Inherited conventions: G is simple, undirected, countable, locally finite (p.5), infinite and connected unless explicitly stated (p.33); Bernoulli independent bond percolation with p∈[0,1] (p.32); pc is the threshold for positive probability of an infinite component and is independent of root on connected G (p.33). Product adjacency is Cartesian, not strong/direct product (p.33).

Operational universal reading: for each p∈[0,1], a.s. every infinite open cluster C and every base vertex v have |C∩({v}×Z)|=∞. The sentence does not separately formalize the quantifier on v; a weaker possible reading is that every nonempty fiber intersection is infinite. A valid proof for the operational reading settles the weaker reading too. A review must disclose which assertion is established and must not silently weaken to one fixed fiber, one selected cluster, existence of some repeated fiber, or a conditional finite-visit exclusion for special G. Countability allows conversion from fixed v statements to all v, only after each fixed-v assertion is proved.

## Boundary checks and partial mechanisms fixed before package comparison
* p=0 is vacuous. At p=1 connected G × Z has one component containing each entire fiber, so the claim holds deterministically.
* If a separate valid theorem establishes uniqueness of the infinite cluster at the chosen p, independence and vertical shift ergodicity give positive frequency of cluster hits on each fixed fiber (positive membership probability propagates through finite paths by finite energy). This is a conditional partial mechanism; importing uniqueness for arbitrary pc(G)=1 is an unsupported transfer of the central difficulty.
* Uniform finite separators/recurring bounded cutsets may supply a closure argument, but pc(G)=1 alone is not a supplied uniform-cutset condition. Such a theorem is only a subclass result unless that implication is proved.
* pc(G)=1 is a base-graph hypothesis, not pc(G × Z)=1. The neighboring subexponential-growth construction on pp.75–76 does not prove Problem 9.49 and is not a universal counterexample: its copies of Z^d already require checking the base threshold.
* Stationarity of the environment under vertical shifts cannot alone turn finite intersection of a particular random cluster into a contradiction. A stationary selection of that cluster, or an event tied to a fixed vertex, must be justified; infinitely many translated clusters can invalidate naive counting.

## Falsifiable success criteria
A full solution needs either a proof covering every G above and every p, with its quantifiers and all imported hypotheses checked, or a graph G satisfying pc(G)=1 and positive-probability infinite cluster with finite intersection with a fiber (identify whether nonempty) that falsifies the exact reading. Finite experiments or subclass proofs are partial evidence. Check G=Z, finite-width or one-ended separators, highly nonuniform degrees, p endpoints, and bases with pc<1 as condition controls. For pc<1 controls, failure cannot refute the actual pc=1 target. No novelty/open-status conclusion follows from this reading alone; the PDF marks the problem open at its historical date.

Completion estimate at seal: 15% of the assigned audit; 0% independent progress toward a full universal solution is claimed.
