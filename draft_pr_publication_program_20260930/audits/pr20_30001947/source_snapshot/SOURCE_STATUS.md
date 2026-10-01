# 30001947: the requested Witt pairing is already known not to exist

**Classification:** already solved in the literature; source-status correction, not a new mathematical discovery. Prepared 2026-09-30 with gpt-6-astra at xhigh reasoning. A separate source audit should precede any PR.

## Answer and exact scope

The answer is **no**, for every \(j\ge0\). For a compact, integrally oriented \(\mathbb F_2\)-Witt PL pseudomanifold \(X^{4j+2}\), the middle-dimensional pairing represents zero in \(W(\mathbb F_2)\).

The target is Question 2 in Friedman's problem discussion in [OWR 56/2011](https://www.mathi.uni-heidelberg.de/~banagl/pdfdocs/OWR_2011_56.pdf), report pages 63–64 (the available author-hosted report uses local pagination). The conventional spaces have no codimension-one strata and no boundary. “Oriented” refers to integral orientation of the regular stratum. Merely mod-two orientation is insufficient: the even-dimensional real projective spaces give nonzero unoriented examples.

## The apparent literature conflict is explicitly resolved by the original proposer

Friedman's [2012/2013 characteristic-two paper](https://faculty.tcu.edu/gfriedman/papers/2-Witt3.pdf), Theorem 1(4), leaves the oriented \(4j+2\) case ambiguous. That source alone would therefore support an open status.

However, in [*Stratified and unstratified bordism of pseudomanifolds*](https://faculty.tcu.edu/gfriedman/papers/stratwitt.pdf), §5.2.1, manuscript pp. 27–29, especially footnote 14 on p. 28, Friedman explains that Goresky–Pardon had already computed this case. He explicitly identifies his earlier correction's unresolved case as having an existing solution. This is an author-confirmed status correction, rather than an inference from superficially similar theorem statements.

The later [*Singular Intersection Homology* manuscript](https://faculty.tcu.edu/gfriedman/ihbook.pdf), printed p. 676, repeats the complete oriented bordism computation:
\[
\Omega_n^{\mathbb F_2\text{-Witt}}\cong
\begin{cases}
\mathbb Z,&n=0,\\
\mathbb Z_2,&n>0,\ n\equiv0\pmod4,\\
0,&\text{otherwise}.
\end{cases}
\]
Thus \(\Omega_{4j+2}^{\mathbb F_2\text{-Witt}}=0\). The middle pairing is a bordism-invariant Witt class, so it vanishes on every such \(X\).

## Direct theorem and hypothesis audit

The original result is Mark Goresky and William Pardon, [*Wu numbers of singular spaces*](https://www.math.ias.edu/~goresky/pdf/Wu.jour.pdf), *Topology* 28 (1989), 325–367, DOI [10.1016/0040-9383(89)90012-8](https://doi.org/10.1016/0040-9383(89)90012-8).

Their §10.1 uses the same mod-two, lower-middle-perversity link-vanishing condition. Their §8.1 defines local orientability by orientability of links, and the corollary in §8.3 explicitly proves that an oriented pseudomanifold is locally orientable. No choice of globally coherent orientations of link bundles is additionally required.

Their §10.2 corollary says the odd middle Steenrod square vanishes for orientable locally orientable Witt spaces. This is an intersection-homology operation, not a claim transferred without justification from ordinary cohomology. Consequently every middle self-pairing is zero. A nonsingular alternating bilinear form over \(\mathbb F_2\) has a symplectic basis and is Witt trivial. Section 10.5, Theorem A, and its proof in §10.7 give the bordism formulation directly. These statements settle the exact requested pairing, not merely a manifold or isolated-singularity special case.

For a local geometric check of the orientation implication: in a distinguished neighborhood \(\mathbb R^s\times cL\), restrict the orientation of the regular stratum to \(\mathbb R^s\times(0,1)\times L_{\mathrm{reg}}\). Orienting the first two factors induces an orientation of \(L_{\mathrm{reg}}\). This only asserts orientability of each link; no orientation of the whole singular stratum is necessary.

## What was checked

- Read the full seven-page 2012 characteristic-two paper, the exact OWR question, and the relevant original Goresky–Pardon sections, including the proof of the odd-square relation on pp. 339–340.
- Read the complete later historical footnote and its surrounding definitions; visually inspected the original formula on p. 339 and Friedman's footnote on manuscript p. 28.
- Checked the later book's exact coefficient-group formula and attribution. This was a targeted page inspection, not a cover-to-cover review of the book.
- Main queue: queued, 0/5; no source research report; no related-target match, matching attempt path, or matching earlier PR found. Source record and checksums are preserved separately.

No new proof search is needed. The upstream 2026 “open” label is stale because it misses the proposer's later correction. The proper queue outcome is **already_solved**, with credit to Goresky–Pardon, rather than a new verified-solution claim.
