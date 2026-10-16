# Source and scope audit

## Exact target

The full, 25-page publisher PDF of Dmitry Fuchs's 2021 article was retrieved from the Arnold Mathematical Journal's site. Printed pp.502–505 (Definition 2.1 and tables), p.506 (elementary lattice descriptions), and p.512 (Conjecture 2.7) were rendered and visually checked. The first source section supplies the dihedral meaning of parallelism. The complete source was available; no workshop summary was substituted.

The upstream description calls the source a 2020 work under an earlier title. The retrieved final article is *Billiard Trajectories in Regular Polygons and Geodesics on Regular Polyhedra*, published online 7 January 2021, Arnold Math. J. 7, 493–517. The target itself is unchanged.

“Short” means vertex to first subsequent vertex, and does not impose a small Euclidean length. The types are those of oriented paths, with indices modulo \(n-2\). The sine expression uses the canonical representative, since the numerical sine is not itself periodic modulo \(n-2\). The source's paragraph immediately before Definition 2.1 selects the sum or difference of endpoint angles by segment parity. The candidate retains that selection, including at directions where both numerical integrality conditions happen to hold. Reading the displayed branches without that convention would create spurious overlapping labels.

The pinned paraphrase says \(A_0\) is characterized by one difference equation. That is only one branch of the actual definition; the candidate uses the full primary definition. The original odd-polygon first branch prints a loose bound \(k\le m+1\); its additional labels are excluded by its angle bound. The exact verifier retains that printed inequality.

## Imported theorems and their access

The proof credits Veech's classical group computation and saddle-connection/cusp theorem. The publisher page for [Veech 1989](https://doi.org/10.1007/BF01388890) was checked, but the full original article was not retrieved. No independent reconstruction of that theorem is claimed.

The complete 25-page [Finster arXiv v3](https://arxiv.org/pdf/1005.4588) was retrieved. Sections 3.1–3.2 reproduce the odd and even group calculations, explicitly attributing them to Veech's Theorem 5.8. In particular, §3.2 explicitly says that the even double polygon is a degree-two cover and has the same Veech group as the opposite-side single-polygon quotient; it is not merely an inference from that quotient. Remark 3.5 gives signature \((n/2,\infty,\infty)\). Printed p.20 gives the two cusp representatives. The even formula and cusp paragraph were visually checked. The candidate uses this only for even \(n\ge8\), and handles \(n=6\) directly.

The complete published [Boulanger–Lanneau–Massart paper](https://www.numdam.org/item/10.5802/ahl.211.pdf), Ann. H. Lebesgue 7 (2024), 787–821, was retrieved. Its §1.4, printed p.791, explicitly states the saddle-connection/cusp correspondence for Veech surfaces and credits Veech. Its particular double-polygon family and one-cusp model are odd; the candidate does not apply that one-cusp assertion to even polygons.

Uniqueness of the hyperelliptic involution in genus at least two and Riemann–Hurwitz are standard compact-Riemann-surface facts. The candidate proves that its specific polygon involution has the requisite fixed-point count and explains why conjugation by any affine map remains a holomorphic hyperelliptic involution.

## Prior work, related targets and novelty

The current queue, full pinned record and keyed prior report, existing attempt history, reset/assessment records, related-target groups, all-state problem-specific PR list and remote branch were checked before proof work. No earlier campaign attempt or problem-specific branch/PR was found. The imported report was literature triage, not an earlier proof attempt by this campaign.

The neighbouring record 5000005 / AMR-049-0005 concerns Conjecture 2.6's assignment of types to parallel angles. It is distinct. This proof does not assume it, the reachable-polygon conjectures, or a currently unproved affine reconstruction. The candidate's elementary affine-invariance lemma is stated and proved within its own scope.

A bounded current literature search using the article title, the exact conjecture number, and short-trajectory length-ratio terminology recovered the original source, classical regular-polygon papers and related pentagon work. No later resolution of this exact labelled assertion was located. This is not an exhaustive bibliography or a historical-priority certificate. Fuchs himself credits the Veech framework and points toward proofs using it; all such credit is retained.

No source PDFs or rendered pages are redistributed in this repository. The local source cache and hashes serve verification only. Upstream problem metadata comes from [ulamai/UnsolvedMath](https://huggingface.co/datasets/ulamai/UnsolvedMath), pinned revision 37e53eabe540fb458758e198be61634bd02ee008, with its CC BY 4.0 attribution.

