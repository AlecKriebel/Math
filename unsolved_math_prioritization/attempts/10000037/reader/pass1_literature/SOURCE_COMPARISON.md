# Bounded source and prior-art comparison: deterministic angular subdivisions

14 October 2026 UTC. Subject: bounded-degree lattice-coarse graphs with iid bond percolation. This is a bibliographic and scope report, not certification of the proposed construction or of its novelty.

## Findings

1. No hidden transitivity or homogeneity hypothesis was found in the inspected Benjamini manuscript conventions or immediately surrounding Problem 9.6. Fixed nonperiodic bounded subdivisions are not excluded by those conventions.
2. The problem sentence omits its parameter quantifier. Its full-supercritical interpretation is supported by the chapter introduction and adjacent lattice-uniqueness theorem, but is an interpretation rather than a verbatim quantified statement.
3. This bounded search did not authenticate a prior publication giving the exact proposed counterexample: two supercritical angular regions, a widening subcritical separating region, and uniformly bounded edge subdivisions restoring a common iid bond parameter on a graph quasi-isometric to a Euclidean lattice.
4. Closely related primary literature confirms the series-path probability transformation and explains why some superficially similar uniqueness theorems require additional symmetry or uniformity. None of the inspected statements rules out the proposed construction.

The negative retrieval result establishes neither originality nor current openness. The construction must stand on its own proof. A sound result may be called a counterexample to the explicitly stated full-supercritical formulation without claiming to have identified the author's intended missing quantifier or to have found an error in a published theorem.

## 1. The original scope

Benjamini, *Coarse Geometry and Randomness*, author manuscript dated 30 October 2013: graph conventions p.5, rough-isometry Definition 1.25 p.9, bond model pp.32–33, and Chapter 9 pp.63–65 were re-read. The graph convention is simple, undirected, countable and locally finite; the percolation chapter uses infinite connected graphs. Rough isometry permits multiplicative and additive distortion. Transitivity is defined separately and explicitly imposed in Theorems 9.1 and 9.3. It is absent from Problem 9.6. The preceding exercise concerns half and quarter spaces.

The Chapter 9 introduction explicitly sets the regime above the critical probability. The publisher's chapter abstract independently preserves that supercritical context. There is no inspected text expressly restricting Problem 9.6 to parameters sufficiently near one. Conversely, the short problem sentence itself supplies no parameter quantifier. A hidden periodicity, stationarity, quasi-transitivity, or additive-only metric convention would be an unsupported insertion. [Preserved author manuscript](https://arquivo.pt/noFrame/replay/20201231041548id_/http://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf); [published chapter record and abstract](https://doi.org/10.1007/978-3-319-02576-6_9).

## 2. Series-path reduction is established methodology

Hilário, Sá, Sanchis and Teixeira, *Percolation on stretched lattices: a static renormalization approach*, PTRF 195 (2026), 451–496, §2, pp.456–457, explicitly gives equivalent descriptions: uniform iid bond percolation on a stretched graph and conditionally independent lattice edges with probabilities equal to powers of the common bond parameter. The exponent is the corresponding path length.

Remark 5 obtains full-supercritical uniqueness for that paper's random environment under its annealed law, using translation invariance, ergodicity and finite energy. This is not a theorem about every deterministic stretching pattern. In particular, the cited passage supplies no uniqueness conclusion for a fixed nonstationary angular pattern. The path reduction itself is a precedent, not a novelty of the proposed example. [Published article](https://doi.org/10.1007/s00440-026-01470-4).

## 3. The uniformity gap is explicit in earlier uniqueness work

Häggström, Peres and Schonmann, *Percolation on transitive graphs as a coalescent process: relentless merging followed by simultaneous uniqueness* (1999), author PDF dated 8 July 1999, defines uniform percolation in Definition 2.1, p.8: large balls meet infinite clusters with probability tending to one uniformly over their centers. Theorem 8.2, p.22, assumes a uniform two-ball connection condition at a parameter and concludes uniqueness at larger parameters. Theorem 1.9, p.7, concerns actual Cartesian products; coarse equivalence to a product is not its hypothesis.

Thus ordinary supercriticality at a root cannot simply replace the uniform connection assumption. The paper's p.26 two-cluster example glues two copies of a tree-product graph through a finite connection. It is not a Euclidean-lattice-coarse bounded-subdivision example. [Author-hosted paper](https://www.math.ucla.edu/~rhs/papers/hps.pdf).

## 4. Defect-plane uniqueness is geometry-specific

De Lima, Martineau, Sanna and Valesin, *Approximation on slabs and uniqueness for Bernoulli percolation with a sublattice of defects*, ALEA 19 (2022), 1767–1797, Theorem 1.1, printed p.1769, concerns one coordinate sublattice with one probability and all other lattice edges with another. It gives uniqueness away from the ambient critical parameter, plus a codimension-one critical case. Its discussion explicitly explains why the usual transitive argument cannot be imported unchanged.

Its more general §3.5 still assumes a connected distinguished subgraph on which a subgroup of graph automorphisms acts transitively. Neither that hypothesis nor the coordinate-sublattice geometry describes two opposite cones. This is a useful comparison, not a prohibition of arbitrary deterministic two-probability fields. The 2021 arXiv v2 and published theorem statements were compared; the original arXiv title uses “plane of defects,” whereas v2 and the journal use “sublattice of defects.” [Published paper](https://alea.impa.br/articles/v19/19-67.pdf); [arXiv v2](https://arxiv.org/abs/2010.06736v2).

## 5. Other comparisons remain restricted

The source audit's earlier high-density conclusions remain unchanged: Teixeira's Theorem 1.4, Candellero–Teixeira's Theorem 1.8, and Hutchcroft–Tointon's Theorem 1.8 do not identify the lower endpoint of uniqueness with the critical parameter. A counterexample at an intermediate parameter would not contradict their stated high-density conclusions. [Teixeira](https://arxiv.org/abs/1409.5923v1); [Candellero–Teixeira](https://arxiv.org/abs/1507.07765v3); [Hutchcroft–Tointon](https://doi.org/10.4171/JEMS/1453).

Benjamini–Kozma's Theorem 1 constructs critical nonuniqueness on a subexponential-growth product, without asserting lattice quasi-isometry. It is not being relabeled as the desired supercritical angular-subdivision example. [Published paper](https://alea.math.cnrs.fr/articles/v10/10-02.pdf).

## 6. Interpretation and acceptance limits

- The inspected sources justify continuing a proof attempt under the declared full-supercritical contract. They do not justify a novelty announcement.
- Do not insert transitivity merely to explain why the construction appears elementary. Conversely, a mathematical counterexample does not reveal which weaker formulation an author might have intended.
- Do not confuse rough transitivity with quasi-transitivity. The former is a coarse metric notion and should not be presented as an automatic exclusion of a lattice-coarse graph.
- The final proof must verify the common iid parameter, global metric bounds, an actually supercritical parameter, and positive-probability nonuniqueness. This report certifies none of those construction-specific steps.
- The chapter's contextual supercritical reading and the dataset's stronger all-parameter normalization remain distinct. A valid supercritical counterexample would refute both explicitly normalized universal assertions.

## Inspection limits

Relevant full statements and surrounding hypotheses were inspected, not the complete proofs of all cited papers. New local PDFs were retained for HPS1999, de Lima et al. arXiv v2, and Hilário et al.2026. The published de Lima paper was inspected through web PDF extraction; direct byte retrieval failed, so no local hash is assigned to it. Attempts to retrieve Babson–Benjamini1999 and Benjamini–Schramm1996 did not yield a newly inspected full text; no conclusion above depends on those failed routes. Primary-source copies, extracted text and rendered pages are excluded from this authored report.
