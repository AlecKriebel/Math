# 30006395: planted random-tree detection, exact source gate

**Historical source gate at 08:06 UTC: no substantive author turn had begun. Original transition unresolved.** Rank 251 / OWR-14299518-013. Checked 2026-10-01. No novelty claim.

## Original question and information model

The primary source is Nina Kamčev's contribution, joint with Nicolas Broutin, Gábor Lugosi, Bruce Reed and Liana Yepremyan, OWR 42/2025, pp.2267–2269: https://ems.press/content/serial-article-files/52246. The workshop ran 14–19 September 2025; the catalog's 2026 report citation does not change the 2025 workshop/question date. Relevant formula pages were visually checked.

The baseline is G(n,c/n), fixed c>0. Plant a uniformly embedded tree by forcing its edges; all others retain probability c/n. The target's logarithm-squared discussion concerns an **unknown uniform labelled Cayley tree** on k vertices. Detection means vanishing testing error, without a polynomial-time requirement.

The source distinguishes:
- Typical tree **revealed** beforehand: detection for c<1.2, k>C log n
- **Unrevealed** random tree: detection for c<1.1, k≥C(log n)²
- For c>500 and k=o(sqrt(n)), impossibility even with the shape revealed

The maximum c admitting polylogarithmic detection and the transition are open. Even O(log n) detection for an unknown tree at c<1.1 is separately open. Therefore log² n is a supplied sufficient scale, not an established sharp lower endpoint. Known-shape and mixture experiments must remain distinct.

## Formal convention for subsequent research

Let P_(n,c) be the null law on labelled simple graphs. The unknown-shape alternative Q_(n,k,c) first selects a uniform k-subset S and a uniform labelled tree on S, forces its k−1 edges, and generates all other potential edges independently with probability c/n. Equivalently one may choose a uniform Cayley tree on [k] and an independent uniform injection into [n]. A test sees only the graph and parameters, not the tree realization or embedding. We use the sum of type-I and type-II errors; its optimum is 1−TV(P,Q). Equal-prior average error is half that number. A known-template experiment instead conditions on/reveals the abstract tree T and must be labeled separately.

The original question asks for the statistical detection scale as the fixed mean-degree constant changes. A result for paths, fixed-degree regular trees, a noisy planting model, a low-degree algorithm class, or one endpoint alone is not full resolution. A c(n)-dependent critical window would require its own explicit limiting regime rather than being silently substituted for fixed c.

## Known primary results and limitations

**Massoulié–Stephan–Towsley (2019)**, *Planting trees in graphs, and finding them back*, COLT/PMLR 99, pp.2341–2371: https://proceedings.mlr.press/v99/massoulie19a.html. Complete PDF retrieved. Setup, Lemma 5, Theorems 6 and 10 and the path/D-ary discussion were read. Lemma 5 gives the usual copy-count likelihood ratio for a known fixed template. Theorem 6 supplies detection of any connected planted graph with k=omega(sqrt(n)). The path and regular D-ary analyses do not resolve unknown uniform Cayley trees.

**Elimelech–Huleihel (2025)**, *Detecting Arbitrary Planted Subgraphs in Random Graphs*, COLT/PMLR 291, pp.1691–1798: https://proceedings.mlr.press/v291/elimelech25a.html. Complete 108-page PDF retrieved; setup, Definition 1, critical-regime Theorem 7, Definition 14, and corresponding discussion inspected. Its background parameter q corresponds to our c/n; template-edge p=1 corresponds to forced planting. Theorem 7's alpha=1 branches concern polynomially growing maximum degree or uniformly bounded degree. Neither is an automatic theorem for typical Cayley-tree sequences with unbounded subpolynomial maximum degree. Its known deterministic template model also differs from the unknown-shape mixture. General overlap bounds may be useful, but no exact transition is imported from its broad title or abstract.

**Current-source check:** targeted title/coauthor searches and Kamčev's primary website https://sites.google.com/view/ninakamcev/about confirmed the 2025 talks. No complete Broutin–Kamčev–Lugosi–Reed–Yepremyan manuscript or later resolution was located in this bounded pass. The OWR endpoints are credited as announced primary-source results; their omitted proofs are not claimed to have been independently verified here. The original problem statement itself is available, so this is not a missing-statement blocker.

The August 2026 preprint Chen–Li, https://arxiv.org/abs/2608.06279, was checked at abstract level only: it conditions on low-degree indistinguishability and concludes indistinguishability after noise. It is not used as an unnoised unknown-tree transition theorem.

## Prior-work gate

Read both AGENTS files, queue/README, complete pinned record and its embedded literature assessment. The separate research-results cache has no OWR-14299518-013 entry. Live all-state searches for numeric ID and planted-tree title, exact branch query, and default-branch attempt-path history found no prior attempt. Recovered campaign inventory also marks this exact target unattempted; the stale queue alone is not treated as conclusive. No related-target group matching this ID was found.

No queue generator was used, no other row was changed, and no external outreach was attempted. Full source PDFs, text, images, and imported record are local reading aids outside the public attempt directory. This checkpoint counts zero author proof turns; the next substantive derivation must be recorded as turn 1.
