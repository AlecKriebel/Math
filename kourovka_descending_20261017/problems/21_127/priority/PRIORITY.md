# Kourovka 21.127 — preliminary priority audit

As of October 24, 2026 UTC. Future-candidate source preparation only. **Provisionally open: no complete proof of rationality for all RAAG elements, and no irrational counterexample in a RAAG, was located.** This is a bounded primary-source audit, not a proof that no solution exists and not a novelty claim.

## Exact question and official status

For every right-angled Artin group \(G\) and every \(g\in[G, G]\), must \(\operatorname{scl}_G(g)\) be rational? The [official October 20 main Notebook](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-3.pdf), printed p.198, 21.127, attributes the question to I. Soroko and mentions the known free-group case. Its definition is in 18.40, printed p.129: the limit of \(\operatorname{cl}(g^n)/n\), with commutator length defined using products of commutators. The downloaded hash matches `f133b4547caae29822fb65455b2115c4af075aa168983996a2aac1c2b21bc118`.

The exact domain and finite-graph issue are recorded in `SOURCE_CONTRACT.md`. The statement does not explicitly impose finite generation. Every individual element lies in a finite induced RAAG retract, and inclusion plus retraction preserves its commutator length and scl, so finite graphs suffice without changing the target. No unstated finite-graph convention is needed.

The current official question remains; the [changes PDF](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21upd-3.pdf) contains no 21.127 entry. Its cover says November 2026 even though retrieved October 24 and linked from the October update. That future-label anomaly and the actual hash are preserved; it is not represented as an authenticated November publication. An absent solution mark alone is not status evidence sufficient for this audit.

A particularly useful proposer source is [Soroko’s questions/comments sheet](https://sites.math.unt.edu/~soroko/questions2.pdf), dated October 19, 2021. Questions 2.1 and 2.2 separately ask whether scl in RAAGs is computable and whether it is rational, with a positive expectation. The [current proposer publication listing](https://ignatsoroko.com/publications/), including 2026 papers, still links this comments sheet under the genus-bounds paper; no later full answer is listed. That is corroboration, not an exhaustive guarantee.

## What the strongest relevant graph-product paper proves

[Chen–Heuer, *Stable commutator length in right-angled Artin and Coxeter groups*](https://arxiv.org/abs/2012.04088), latest arXiv v3 August 10, 2022; [published online September 26, 2022](https://doi.org/10.1112/jlms.12680), J. London Math. Soc. 107 (2023), 1–60:

- Theorems 6.3/7.4 compute **vertex chains** by a linear program when the needed scl data in vertex groups are known. Rationality is conditional on rational vertex data. This does not cover arbitrary words in a graph product.
- Under the standard RAAG decomposition with cyclic vertex groups, null-homologous vertex chains have zero scl; nonzero double-chain examples instead use a decomposition with free-group vertex groups.
- Theorem 7.11 gives the exact value \(\frac12\operatorname{fsn}(\Gamma)\) for the special double chain in its double RAAG. Theorem 7.13 realizes every rational \(q\ge1\) by a chain in some RAAG. Neither says all elements have rational values.
- Theorem 7.14 proves NP-hardness of the threshold problem with graph, word, and rational threshold as input. It does not prove uncomputability or irrationality. Theorem 6.2 supplies a gap for chains outside the vertex-chain exception, rather than a general exact formula.

These are inspected theorem scopes, not deductions from the title or abstract.

## Other primary results and their boundaries

| Primary source | Exact useful scope | What it leaves out |
|---|---|---|
| [Calegari, *Stable commutator length is rational in free groups*](https://arxiv.org/abs/0802.1352), v3 March 14, 2009; JAMS 22 (2009), 941–961, Rationality Theorem | Free groups: rationality, extremal surfaces, piecewise rational linearity, exact algorithm on finite-dimensional rational chain subspaces. | General commutation graphs. |
| [Calegari, *Scl, sails and surgery*](https://arxiv.org/abs/0907.3541), v3 November 23, 2010; J. Topology 4 (2011), 305–326, Theorem 3.14 | Free products of finitely many finitely generated free abelian groups have piecewise rational linear scl and an exact algorithm. This covers RAAG graphs that are disjoint unions of complete graphs. | Arbitrary overlapping commutation relations. |
| [Susse, *Stable Commutator Length in Amalgamated Free Products*](https://arxiv.org/abs/1310.2254), v3 May 12, 2014; J. Topology Anal. 7 (2015), Theorems 3.4/3.5 | Free abelian factors amalgamated over \(\mathbb Z^k\), including multiple factors over one common shared subgroup: piecewise rational linearity and computability. | No theorem permitting unrestricted iterated amalgamation of arbitrary RAAG factors. In particular one cannot iterate it after the factors cease to be free abelian. |
| [Chen, *Scl in graphs of groups*](https://arxiv.org/abs/1904.08360), v2 January 15, 2020; Invent. Math., DOI 10.1007/s00222-020-00951-0, Theorem 5.10 | Vertex scl identically zero; edge images in each vertex group central **and mutually commensurable**. Exact rational linear programming under these hypotheses. Includes generalized Baumslag–Solitar groups. | An arbitrary RAAG splitting need not satisfy either the centrality or mutual-commensurability requirements. “Acts on a tree” alone is insufficient. |
| [Clay–Forester–Louwsma, *Stable commutator length in Baumslag–Solitar groups and quasimorphisms for tree actions*](https://arxiv.org/abs/1310.3861), v2 July 14, 2014; Trans. AMS 368 (2016), 4751–4785, DOI 10.1090/tran/6510 | Theorem 1.1/5.2 and Corollary 5.3 give exact rational LP values for alternating t-shape elements. For general t-exponent-zero input, Theorem 4.3 gives a lower bound. | The authors explicitly identify realization of the LP solution by surfaces as the missing matching upper bound in that generality. These tree-action results are not full RAAG rationality. Chen later settles all Baumslag–Solitar groups under his own hypotheses. |
| [Heuer, *Gaps in scl for Amalgamated Free Products and RAAGs*](https://arxiv.org/abs/1802.01107), v3 September 14, 2018; GAFA 29 (2019), 198–237, Theorem 7.3 | Every nonidentity commutator-subgroup element in a RAAG has scl at least 1/2, sharply. | A lower spectral gap places no rationality restriction on values above it. The quasimorphisms certify that bound, not the exact value for every input. |
| [Forester–Soroko–Tao, *Genus bounds in right-angled Artin groups*](https://arxiv.org/abs/1710.10542), v2 March 8, 2018; Publ. Mat. 64 (2020), 233–253 | Earlier bounds 1/(6k) for chromatic number k and 1/20 for triangle-free graphs. | Bounds, not rationality. |

## Updates through the audit date

The [Chen–Heuer graphs-of-groups paper](https://arxiv.org/abs/1910.14146) is now v3, September 10, 2024; the current author page lists it as to appear in American Journal of Mathematics. TheoremD/5.5 is an explicit graph-product gap statement, with an exact formula only in its complete-support exception. The arXiv revision notes preserve its gap results and identify a corrected lemma; no general rationality theorem is claimed.

The new [Chen–Heuer *Uniform spectral gap of scl in 2-orbifolds*](https://arxiv.org/abs/2604.21059), v2 May 27, 2026, concerns relative spectral gaps for hyperbolic 2-orbifolds. It was separated from the older long paper’s appendix and does not solve RAAG rationality. [Marchand’s *From letter-quasimorphisms to angle structures and spectral gaps for scl*](https://arxiv.org/abs/2402.13856), v2 August 5, 2024 and listed as an Israel Journal of Mathematics 2026 publication, gives a geometric proof of the sharp 1/2 gap, not exact scl on arbitrary RAAG words.

Current primary author listings for [Chen](https://lvzhouchen.github.io/research.html), [Soroko](https://ignatsoroko.com/publications/), [Heuer](https://www.nicolausheuer.com/), [Forester](https://math.ou.edu/~forester/), [Louwsma](https://www.joellouwsma.com/research), and [Marchand](https://alexis-marchand.github.io/) were checked. No complete target solution was located. A direct MattClay research-page/PDF attempt failed; the joint paper’s full arXiv copy was read instead. Heuer’s direct page download failed, while its primary web rendering and linked arXiv listing were accessible. Search-service snapshots and finite author lists can miss material; they do not prove completeness.

## Safeguards for a later research effort

The remaining question concerns an arbitrary commutator-subgroup word in an arbitrary finite commutation graph. Neither positivity nor a sharp gap is an arithmetic discreteness theorem. Rational lower and upper estimates converging to a real value do not establish that the limit is rational. A finite rational LP answers rationality only after proving it computes the exact scl, including the matching construction/asymptotic realization. A result for selected chains or vertex-chain decompositions cannot be promoted to all elements without a scope reduction. Conversely, a chain irrationality result would need an appropriate valid chain-to-element transfer before serving as an elementwise counterexample. Mere subgroup embeddings need not preserve scl; the finite-support reduction works because it has a retraction.

All cached source URLs, hashes, versions, theorem locators, failed accesses, and search families appear in `SOURCE_MANIFEST.json`. No QUEUE/PR/other-agent material was read; no outreach, git action, publication, or original-solution effort was performed. The assigned audit is complete, while the mathematical target remains unresolved by this work. Renew the priority check before promoting a future result.
