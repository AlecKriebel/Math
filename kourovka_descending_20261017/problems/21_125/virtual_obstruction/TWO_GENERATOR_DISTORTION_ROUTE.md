# A stronger metric route and its remaining gap

October24,2026. This is a reduction of a possible negative strategy, not a virtual nonembedding proof.

## A necessary property of any positive answer

**Proposition.** If a finitely generated group \(G\) has a finite-index subgroup that embeds in a RAAG, then it has a finite-index normal subgroup \(K\) such that every nonabelian two-generator subgroup of \(K\) is undistorted in \(G\). In particular there is one positive integer \(N\) such that, for every pair \(x,y\in G\), the subgroup \(\langle x^N,y^N\rangle\), whenever nonabelian, is undistorted in \(G\).

**Proof.** Take the normal core \(K\) of the given RAAG-embedding finite-index subgroup. Let \(\iota:K\hookrightarrow A\) denote the resulting embedding; its image lies in a finite induced RAAG since \(K\) is finitely generated. For \(L=\langle u,v\rangle\le K\), Carr's theorem says that a nonabelian \(L\) is a free group quasi-isometrically embedded in \(A\). Thus for its word metric there are constants depending on this pair such that
\[
|w|_L\le c\,|\iota(w)|_A+c\quad(w\in L).
\]
The homomorphism \(\iota\) is Lipschitz on the finitely generated group \(K\), and the finite-index inclusion \(K\le G\) is a quasi-isometry. Consequently \(|w|_L\le c'|w|_G+c'\), which proves undistortion. Conversely inclusion of any finitely generated subgroup is Lipschitz, giving the other inequality. Take \(N\) to be the exponent of the finite group \(G/K\); then \(x^N,y^N\in K\) for every \(x,y\). The quasi-isometry constants may depend on the pair, and no uniform constants over all pairs are asserted. \(\square\)

The full quasi-isometry conclusion is established prior work: Mike Carr, *Two-generator subgroups of right-angled Artin groups are quasi-isometrically embedded*, arXiv:1412.0642. The reduction to ambient \(G\) does not require the embedding \(K\to A\) itself to be quasi-isometric; only its automatic upper Lipschitz bound is used.

## Why ordinary Hydra distortion does not complete this route

Dison–Riley construct free \(H_m=\langle a_1t,\ldots,a_mt\rangle\le G_m\) with Ackermannian distortion. Already \(H_2\) is a distorted free two-generator subgroup. However, **\(G_2\) is known virtually special**, so the existence of that subgroup cannot contradict virtual specialness. A finite-index subgroup intersects \(H_2\) in a finite-index subgroup of a free group, whose rank can exceed two; Carr's two-generator theorem gives no distortion bound for that intersection. Likewise \(H_m\), for \(m\ge3\), has too many generators for this theorem.

To obtain a negative solution by this method, one would need to prove, for some fixed \(m\ge5\), that for **every** \(N\ge1\) there are \(x_N,y_N\in G_m\) such that \(\langle x_N^N,y_N^N\rangle\) is nonabelian and distorted in \(G_m\). A single distorted subgroup, or experiments for a bounded list of \(N\), would not suffice. No such family has been proved. Replacing the Hydra generators by powers without proving persistence of their distortion is exactly the missing step; the known rank2 positive result is a falsification check.

The uniformly passing finite permutation covers in `CENTRALIZER_COSET_FILTER.md` settle only the algebraic centralizer-coset test. They do not prove this stronger metric property, either positively or negatively.

## A relevant recent theorem, checked in primary form

Andrew–Bering–Kapovich–Vidussi, with an appendix by Shalen, *On two-generator subgroups of mapping torus groups*, Journal of the London Mathematical Society112(2025), no.1, e70226, DOI10.1112/jlms.70226, arXiv:2405.08985v2 (June23,2025), **TheoremA and CorollaryB**, classify two-generator subgroups of a free-by-cyclic group: they are free, or finitary sub-mapping tori; in the finite-rank automorphism case the latter are undistorted. This theorem does not exclude distorted free two-generator subgroups and does not assert a finite cover eliminating them for reducible Hydra monodromy. Its separate CorollaryF concerns fully irreducible monodromy, a hypothesis the Hydra triangular automorphism fails. The primary PDF was read and cached; no abstract-only extrapolation was used.

The route is therefore recorded with an explicit quantitative obstruction target, but remains **unsolved**. Neither large distortion of \(H_m\) nor this reduction establishes an intrinsic Dehn-function statement or a virtual-specialness answer.
