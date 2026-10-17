# Source-scope adjudication: percolation on graphs coarsely equivalent to lattices

14 October 2026 UTC. Identifier: 10000037 / AMR-099-0037.

## Decision

**The source supports a general-graph, Bernoulli-bond, full-supercritical target. It does not supply a transitivity hypothesis. The parameter quantifier is contextual rather than explicit in the problem sentence.** A separate all-parameter interpretation must retain the critical parameter. None of the inspected later statements certifies an exact-target resolution. In particular, high-density uniqueness and rough-isometry invariance of a nontrivial uniqueness phase must not be promoted to uniqueness throughout the supercritical regime.

This is a source audit, not a mathematical solution or proof audit. No new example, theorem application, construction, experiment, or resolution claim is supplied.

## 1. Primary-source identity

The relevant item is Open Problem 9.6, printed/PDF page 64 of Itai Benjamini's *Coarse Geometry and Randomness*, author manuscript dated 30 October 2013. The complete retained manuscript has 115 pages. The [preserved author-hosted PDF](https://arquivo.pt/noFrame/replay/20201231041548id_/http://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf) is 1,101,523 bytes, SHA-256 aaab65b3acf65f4d21657da94464e9d5edb93969a4c353805099a220a0717cfe. Its archival capture date is not a manuscript revision date.

The [published chapter record](https://doi.org/10.1007/978-3-319-02576-6_9) has different pagination, 69–84. No identity between the publisher's complete chapter bytes and this manuscript is asserted. The prior retrieval record reports HTTP 404 for the live author URL; an indexed search result is not evidence that the URL has resumed serving the file.

## 2. Model and parameter adjudication

The manuscript's conventions and adjacent results establish the following scope:

- Pages 5 and 33: infinite, connected, countable, undirected, simple graphs; the target adds a uniform finite degree bound.
- Page 9, Definition 1.25: coarse surjectivity plus both multiplicative and additive metric distortion. The source identifies this usage with quasi-isometry. Additive-only distortion is not the source convention.
- Pages 32–33 and Theorems 9.2–9.3: independent edge retention at one common parameter; all vertices remain. This is bond percolation.
- Pages 63–65: transitivity is an explicit hypothesis of particular preceding theorems, not a standing hypothesis for Problem 9.6. Periodicity and homogeneity are also absent.
- Page 63 explicitly sets the chapter's focus at p>p_c; page 64 omits a parameter range and dimension restriction in the problem itself. Almost-sure uniqueness is supplied by the surrounding discussion. [Primary manuscript](https://arquivo.pt/noFrame/replay/20201231041548id_/http://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf)

For subsequent acceptance, keep these authored formalizations distinct. Write N∞ for the number of infinite open clusters.

1. **Context-supported target:** for each admissible graph G and each fixed p with p_c(G)<p≤1, P_p^G(N∞=1)=1.
2. **Stronger all-parameter normalization:** for each admissible G and each fixed p in [0,1], P_p^G(N∞≤1)=1, explicitly including p=p_c(G).

Neither formulation asks for simultaneous assertions at every p in one coupled process. Do not silently impose d≥2; any restriction of the work to that range needs an explicit treatment or exclusion of d=1. Do not insert a periodicity, stationarity, unimodularity, quasi-transitivity, or lattice-embedding requirement. A deterministic nonperiodic local modification is not excluded merely because it lacks symmetry; admissibility still depends on the actual graph and metric conditions.

An assertion of p_c=p_u is not an adequate substitute for the first target on an arbitrary nontransitive graph unless the required parameter-wise uniqueness is separately justified. The source's examples and later product-graph literature specifically caution against assuming uniqueness monotonicity outside its stated hypotheses. [Benjamini–Kozma, pp. 15–16](https://alea.math.cnrs.fr/articles/v10/10-02.pdf)

## 3. Exact later-source comparison

### Teixeira: a high-density site theorem

Augusto Teixeira, *Percolation and local isoperimetric inequalities*, PTRF 165 (2016), 963–984, [DOI](https://doi.org/10.1007/s00440-015-0653-5); inspected [arXiv:1409.5923v1](https://arxiv.org/abs/1409.5923v1), pages 2–4.

Theorem 1.4 assumes a local isoperimetric inequality of dimension greater than one and a polynomial volume upper bound. It supplies a threshold p*<1 and uniqueness above p*. Theorem 1.9 supplies a related high-marginal statement for dependent site laws. Page 3 explicitly distinguishes this nontransitive, large-p conclusion from Burton–Keane. The site-to-bond comparison mentioned there concerns p_c<1; it is not stated as a transfer of the entire uniqueness conclusion. Neither theorem identifies p* with p_c. The arXiv margin says v1, 20 September 2014, while the generated title date is 5 July 2021; these are different metadata fields, not evidence of another arXiv version.

### Candellero–Teixeira: also high-density site uniqueness

Elisabetta Candellero and Augusto Teixeira, *Percolation and isoperimetry on roughly transitive graphs*, AIHP 54(4) (2018), 1819–1847, [DOI](https://doi.org/10.1214/17-AIHP857). Theorem 1.8 was inspected in [arXiv v3](https://arxiv.org/abs/1507.07765v3), page 3, and independently compared with the [institutional published-version PDF](https://wrap.warwick.ac.uk/90875/7/WRAP-percolation-isoperimetry-roughly-graphs-Candellero-2018.pdf), printed page 1821 / PDF page 4 including its repository cover.

The theorem requires rough transitivity, polynomial growth, an isoperimetric inequality, and a decoupling condition; its conclusion applies when every site marginal exceeds p*<1. It does not assert p*=p_c. The published statement preserves that restriction. The nearby cited site-to-bond consequence concerns nontriviality of the phase transition. No blanket uniqueness transfer is stated there. The book reference in Remark 2.2 concerns another open question, not an explicit resolution of Problem 9.6.

### Hutchcroft–Tointon: bond model, still a high-p conclusion

Tom Hutchcroft and Matthew Tointon, *Non-triviality of the phase transition for percolation on finite transitive graphs*, JEMS 27 (2025), 4283–4346, [DOI](https://doi.org/10.4171/JEMS/1453). In the [paginated publisher PDF](https://ems.press/content/serial-article-files/51184), printed page 4291 / PDF page 9, Theorem 1.8 gives bond uniqueness for p≥1−ε under a uniform finite-exhaustion isoperimetric condition of dimension greater than 6+2√7. It does not require transitivity. Corollary 1.9 yields p_u<1. Theorem 1.10 requires a separate uniform connection hypothesis at p_0 and concludes uniqueness for p>p_0. These statements do not identify their lower endpoint with p_c for every graph in the target class.

### Sprinkling is a different input model

Benjamini and Tassion's [*Homogenization via sprinkling*](https://arxiv.org/abs/1505.06069v1), Theorem 1 and its adjacent extension, concern a fixed everywhere-percolating or densely-percolating lattice subgraph augmented with independent positive-density bond sprinkling. Their connectivity/uniqueness conclusion is not phrased as Bernoulli-p percolation on every graph quasi-isometric to a lattice. A bridge between those models would require additional mathematics and is not certified here.

### The alleged invariance shortcut is not authenticated

Benjamini–Schramm's [*Percolation in the Hyperbolic Plane*](https://doi.org/10.1090/S0894-0347-00-00362-3), introduction and Theorems 1.1–1.3, printed pages 487–488, concern transitive planar/nonamenable settings. They do not state preservation of full-supercritical uniqueness under arbitrary bounded-degree quasi-isometries.

In Lyons–Peres, [*Probability on Trees and Networks*](https://rdlyons.pages.iu.edu/prbtree/book_pb.pdf), Exercise 7.13, printed page 271 / PDF page 288 of the inspected 19 August 2026 corrected paperback manuscript, the property preserved is p_u<1, and both graphs are quasi-transitive. The adjacent Theorem 7.50 also assumes quasi-transitivity. These are different hypotheses and a weaker conclusion than the target. A citation to this exercise cannot remove either distinction.

## 4. Bounded counterexample search

The search separately looked for published nonuniqueness examples on nontransitive graphs quasi-isometric to Euclidean lattices, including variants of “roughly isometric,” “rough isometric,” “quasi-isometric,” “counterexample,” “non-uniqueness,” and “multiple infinite clusters.” It did not authenticate a primary source stating a counterexample with the exact lattice-coarse and supercritical hypotheses. That negative retrieval result is not a theorem, an openness certificate, or a novelty claim.

A directly relevant cautionary source is Benjamini and Kozma, *Uniqueness of percolation on products with Z*, ALEA 10(1) (2013), 15–25. Their [published paper](https://alea.math.cnrs.fr/articles/v10/10-02.pdf), Theorem 1 on page 16, gives critical nonuniqueness for a subexponential-growth product graph. Its statement does not assert lattice quasi-isometry. The introduction also records nonmonotone uniqueness examples for products. Neither statement is being relabeled as an exact counterexample to Problem 9.6, and no new analysis of those constructions was undertaken.

## 5. Acceptance consequences and inspection limits

A later mathematical deliverable should name its chosen quantifier before claiming completion. A near-one result, an added symmetry assumption, or an unproved model-transfer step remains a restricted result. A negative answer requires an admissible graph and nonuniqueness at the relevant parameter; a critical-only example would address the all-parameter normalization but not automatically the full-supercritical target.

The source conventions and statement pages were checked against rendered images. Full files were retained for identification and keyword searching; this does not mean their proofs were audited. The published Candellero–Teixeira statement was checked through web text extraction; direct PDF retrieval timed out and the web screenshot failed, so no retained-byte hash or visual-inspection claim is made for that version. The companion metadata file records successful PDF hashes, sizes, and the actual scope of inspection. All conclusions here are bibliographic or source-scope adjudications.
