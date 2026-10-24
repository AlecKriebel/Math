# Preliminary priority audit: Kourovka 21.129

**Status as of 24 October 2026: no complete resolution found; provisionally open.** This is a finite primary-literature audit, not a certificate that no unpublished or overlooked solution exists. No novelty claim, outreach, upload, or publication was made.

## Exact target

If two Artin groups of spherical type are quasi-isometric, must they be abstractly commensurable? Here spherical means their associated Coxeter groups are finite; abstract commensurability means isomorphic finite-index subgroups. Reducible Coxeter diagrams and the resulting direct products are included. An affirmative answer must cover every such product; a negative answer needs an eligible quasi-isometric, noncommensurable pair. A counterexample among nonspherical right-angled Artin groups does not suffice.

The [official 21st Notebook PDF](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-3.pdf), printed p.198, gives precisely this question and attributes it to I. Soroko. It has no solution text, star, or sharp marker. The downloaded SHA-256 matches the research contract: `f133b4547caae29822fb65455b2115c4af075aa168983996a2aac1c2b21bc118`. The [latest official announcement](https://kourovkanotebookorg.wordpress.com/2026/10/06/october-2026-update-2-for-the-21st-edition/) is modified 20 October 2026. This is current editorial corroboration, not the sole basis of the assessment.

## Primary sources inspected

| Source | Date/version and relevant location | Exact scope and priority finding |
|---|---|---|
| Cumplido–Paris, [*Commensurability in Artin groups of spherical type*](https://doi.org/10.4171/RMI/1282), [published PDF](https://ems.press/content/serial-article-files/39000?nt=1) | Online 29 June 2021; *Rev. Mat. Iberoam.* 38(2) (2022), 503–526. Theorems 2.2–2.4, Proposition 3.1, Corollary 3.2, Remark 5.2 | Almost complete **commensurability** classification. It does not state a complete quasi-isometry classification. The product-related nuance is addressed below. |
| Soroko, [*Artin groups of types F4 and H4 are not commensurable with that of type D4*](https://arxiv.org/abs/2009.10471), [PDF](https://arxiv.org/pdf/2009.10471v4) | First arXiv submission 22 September 2020; v4 7 July 2021; *Topology Appl.* 300 (2021), 107770. Theorems 1 and 5 | Resolves the two named noncommensurability comparisons; identifies the D4 central quotient with the pure mapping class group of a three-punctured torus. Neither F4 versus H4 nor the whole question is resolved here. |
| Soroko, [2021 World of GroupCraft handout](https://sites.math.unt.edu/~soroko/presentation-WOG-handout.pdf) | Actual title-page date 25–26 August 2021; slides 4 and 8 | Proposer explicitly labels quasi-isometry classification mostly open and lists four outstanding commensurability pairs. The search renderer's recent crawl/publication display is not the document date. |
| Soroko, [current publications page](https://ignatsoroko.com/publications) | Retrieved 24 October 2026; includes 2026 preprints | Latest spherical D5 work classifies automorphisms, and other recent work concerns endomorphisms or Reidemeister numbers. No complete 21.129 theorem is listed. A current bibliography is useful corroboration, not proof of absence. |
| Kapovich–Kleiner–Leeb, [*Quasi-isometries and the de Rham decomposition*](https://math.nyu.edu/~bkleiner/kkl.pdf) | Author-hosted manuscript 3 October 1996; *Topology* 37(6) (1998), 1193–1211; Theorem B | Product rigidity for factors of coarse type I/II and Euclidean-cone factors. The required spherical-Artin application is explicitly identified in Cumplido–Paris Remark 5.2. |
| Sauer, [*Homological invariants and quasi-isometry*](https://arxiv.org/abs/math/0312129), [PDF v2](https://arxiv.org/pdf/math/0312129v2) | v2 18 October 2004; *GAFA* 16 (2006), 476–515; Theorem 1.2(i) | Uniform embeddings preserve the indicated inequality of finite cohomological dimensions. Applied in both directions, quasi-isometric groups with finite cohomological dimension have equal dimension. |
| Behrstock–Kleiner–Minsky–Mosher, [*Geometry and rigidity of mapping class groups*](https://msp.org/gt/2012/16-2/gt-v16-n2-p05-s.pdf) | *Geom. Topol.* 16 (2012), 781–888; complete Theorem 1.2 in Section 10, p.875 | A group quasi-isometric to a mapping class group has a finite-index subgroup mapping to the latter modulo its finite center, with finite kernel and finite-index image. The complete statement handles complexity 2, unlike the shortened introductory version. |
| Ragosta, [*A marking graph for finite-type Artin groups*](https://arxiv.org/abs/2508.10394), [PDF v1](https://arxiv.org/pdf/2508.10394v1) | Submitted 14 August 2025; Theorem A and introduction | Constructs a geometric marking-graph model for each irreducible spherical Artin group modulo center. It does not identify graphs for different types or prove quasi-isometry rigidity. The introduction still distinguishes this model from the unresolved mapping-class-style machinery. |
| Huang–Osajda–Vaskou, [*Rigidity and classification results for large-type Artin groups*](https://arxiv.org/html/2407.19940) | v1 29 July 2024; introduction, Theorems 1.8–1.9 | Strong rigidity results require large type and specified graph hypotheses. Large type forbids commuting relations; irreducible spherical diagrams of rank at least three include such relations and are outside that hypothesis. Rank-two overlap is already covered by the dihedral commensurability class. |

## Existing results reduce the gap, but do not close it

The following is a synthesis of established results, recorded to prevent a false new-solution claim. It is not presented as a novel theorem or an independently refereed proof.

Write \(P_T\) for the pure Artin subgroup of an irreducible spherical type \(T\), and \(Q_T=P_T/Z(P_T)\). For a diagram with \(p\) components, \(k\) non-singleton, the existing finite-index model is

\[
\left(\prod_{i=1}^{k}Q_{T_i}\right)\times\mathbb Z^{p}.
\]

Here \(Q_{A_1}=1\); the other \(Q_T\) embed in torsion-free Artin groups. See Cumplido–Paris Proposition 3.1/Corollary 3.2. Their Remark 5.2 supplies coarse type I and invokes product rigidity. **Its subsequent algebraic conclusion assumes a finite-index isomorphism:** it cannot be read as deriving commensurability from an arbitrary quasi-isometry.

1. KKL Theorem B therefore supplies equal Euclidean dimensions, equal numbers of nontrivial factors, and a matching of the \(Q_T\)'s up to quasi-isometry. It need not make the entire map a product map: Euclidean shearing is allowed. Singleton-component counts are recovered by \(p-k\).
2. Matched factors can be multiplied by \(\mathbb Z\), giving quasi-isometric irreducible Artin groups. Their cohomological dimensions equal their Artin ranks; applying Sauer in both directions gives equal ranks. Thus cross-rank pairs are excluded without assuming that rank alone classifies geometry.
3. For types \(A_n,B_n\) with \(n\ge3\), the central quotients are virtually punctured-sphere mapping class groups. For \(D_4\), use the three-punctured torus. Their relevant centers are trivial and complexities are at least 2. Apply BKMM to a torsion-free \(Q_T\); its finite kernel is trivial. This yields commensurability with the mapping-class-type factor, then with the corresponding original Artin group after adjoining the cyclic factor. Hence a known noncommensurability comparison involving one of these types cannot yield a counterexample.
4. Once every matched irreducible pair is commensurable, finite-index isomorphisms can be multiplied, establishing the same for the original products. This is the product criterion in Cumplido–Paris Theorem 2.2.

The low-rank and exceptional bookkeeping is:

| Rank/types | Disposition under the above existing results |
|---|---|
| Rank 1: \(A_1\cong\mathbb Z\) | Euclidean factors; their multiplicity is retained. If the empty diagram is admitted, its trivial group is an immediate separate case. |
| Rank 2: \(A_2,B_2,I_2(m),m\ge5\) | One commensurability class. This includes aliases \(I_2(3)=A_2\), \(I_2(4)=B_2\). No rigidity theorem for high-complexity surfaces is needed. |
| Rank 3: \(A_3,B_3,H_3\) | \(A_3\sim B_3\); comparison with \(H_3\) is excluded by the mapping-class argument plus established noncommensurability. Do not omit the complexity-2 case. |
| Rank 4: \(A_4,B_4,D_4,F_4,H_4\) | Comparisons involving the mapping-class-type entries are accounted for; **\((F_4,H_4)\)** remains an eligible gap. |
| Rank 5 or rank \(n\ge9\): \(A_n,B_n,D_n\) | \(A_n\sim B_n\); comparisons with \(D_n\) are excluded by the mapping-class argument. |
| Ranks 6, 7, 8: \(A_n,B_n,D_n,E_n\) | Mapping-class-type comparisons are accounted for; **\((D_6,E_6),(D_7,E_7),(D_8,E_8)\)** remain eligible gaps. |

Thus, **on the cited product/rigidity inputs, the precise remaining task is four implications**

\[
 A[X]\simeq_{qi}A[Y]\quad\Longrightarrow\quad A[X]\sim_{comm}A[Y],
 \qquad
 (X,Y)\in\{(F_4,H_4),(D_6,E_6),(D_7,E_7),(D_8,E_8)\}.
\]

A positive commensurability result for a pair would establish its implication immediately; a noncommensurability result alone would not. For a negative resolution of 21.129 one still needs both quasi-isometry and noncommensurability for the same eligible pair. No such pair was found in this audit. The four commensurability comparisons were explicitly open in the inspected 2021/2022 sources; no later primary resolution was located. Their current unresolved status is therefore an audit finding, not a claim that those old sources alone authenticate 2026 status.

## Provenance, coverage, and limits

Searches covered the exact question/number, spherical and finite-type terminology, quasi-isometry rigidity, products, central quotients, mapping class groups, recent Soroko work, and each exceptional comparison. Primary manuscripts and author/editor pages were inspected; aggregator labels and summaries were not used as authority. No QUEUE, PR, unrelated local effort, or other independent research agent was consulted.

The official updates-only URL `21upd-3.pdf` returned a file headed **November 2026 update** on the October 24 audit date. It contains no 21.129 entry; SHA-256 `3371fa96766d35e18256af9eeac299785d95fb211b31d5e1b31bfab6da2beb71`. Preserve this as an observed mutable retrieval, not a historically authenticated publication dated before the audit. The main Notebook matches the contract's previously frozen hash.

Source PDFs and exact retrieval hashes are cached locally in `sources/`; `SOURCE_MANIFEST.json` records dates, scope, theorem locations, and search families. This audit checks theorem statements and the logical use of their hypotheses, not all proofs or computation in the cited papers. Literature indexing can miss sources and author bibliographies may lag. Renew the priority audit before promoting any solution. The four-pair synthesis should receive independent adversarial verification before publication as a research result.
