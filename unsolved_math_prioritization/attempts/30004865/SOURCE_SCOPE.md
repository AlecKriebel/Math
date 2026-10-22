# Source gate: local Hilbert-space entanglement testers

Problem 30004865 / OWR-8415352-007, rank416. This is a source and prior-attempt checkpoint, **0/5 author turns**. The imported expanded title is not the mathematical statement.

## Exact source question

Cécilia Lancien's contribution, with Maria Anastasia Jivulescu and Ion Nechita, occupies printed pages2696–2698 of [OWR49/2021](https://ems.press/journals/owr/articles/8415352), published26 November2022. Its central question on p2697 concerns completeness of the whole local-contraction tester family without reordering input indices. Separate questions concern mixed multipartite states detected by realignment or SIC testers, comparison of those two fixed tests, and output-dimension efficiency. It is not a claim that those two particular testers already constitute the entire family.

A state rho is a positive semidefinite, trace-one matrix on the tensor product of m finite-dimensional complex Hilbert spaces, m>=2. Separable means fully separable: a convex combination of tensor products of local density matrices. Failure of full separability need not be genuine multipartite entanglement.

The main question, with the notation made explicit, is:

    For every non-fully-separable rho on tensor_i C^(d_i), do there exist
    finite n_i and complex-linear E_i:M_(d_i)(C)->C^(n_i),
    ||E_i||_(S1->l2)<=1,
    such that ||(tensor_i E_i)(rho)||_(tensor_pi,i l2^(n_i))>1?

No partial transpose, swap of individual bra/ket indices, or regrouping of input tensor legs is allowed before these local maps. The output projective norm is the infimum over sums of simple tensors of the sum of products of Euclidean norms. For two factors it is the matrix nuclear norm. Using norm at most1 rather than exactly1 does not enlarge the detected-state set: nonzero maps can be normalized upwards.

## Detailed primary paper and credited earlier results

[Jivulescu–Lancien–Nechita, arXiv:2010.06365v1](https://arxiv.org/abs/2010.06365), dated13 October2020, is the retrieved full text. Definition3.1 and Corollary3.3 specify the tester and detection condition; Section13 p35 states the unanswered general question. Sections10–12 already prove the bipartite fixed-test dominance, a completeness theorem after a specific index permutation, and detection of every entangled multipartite pure state. These are prior results, not targets to relabel as new progress. Section8.2 already computes the fixed-test Werner thresholds. Its failure examples for fixed testers alone do not establish failure of all possible testers.

The [journal version](https://link.springer.com/article/10.1007/s00023-022-01187-9) was published7 May2022, Annales Henri Poincaré23,3791–3838. Its metadata and abstract are accessible; its full subscription PDF was not retrieved. No assertion of byte-identical editions is made.

The fixed realignment tester is vectorization, with Euclidean output equal to the Hilbert–Schmidt norm. For a SIC of d² unit vectors, the normalized SIC tester has entries sqrt((d+1)/(2d)) times the corresponding quadratic matrix evaluations. These normalizations agree with [Shang–Asadian–Zhu–Gühne, 2018](https://arxiv.org/abs/1805.03955v3) and the detailed paper's definitions. A SIC is not assumed to exist in every dimension. Any replacement by an abstract map with the same Gram form must be stated explicitly.

## Norm and logical caveats

The primary paper discusses both complex-linear testers on all matrices and real-linear testers on Hermitian matrices. The main explicit problem uses complex Schatten spaces. A proof may establish a bound under the weaker condition that every pure-state projector is mapped into the Hilbert unit ball, but must say why that includes all required complex testers.

Some ancillary displayed claims in the retrieved preprint require care. In Section4.1, for the deformed canonical basis map G_x with x<1, an off-diagonal rank-one matrix has output norm sqrt(d/(d-1+x²))>1 although its trace norm is1. Thus that normalization cannot be used as a complex S1-contraction in that range. We do not assume the general real-to-complex extension assertion of Lemma3.2. This observation limits which source formulas may be imported; it is not a resolution of the original question, and no claim about a correction in the inaccessible journal text is made.

Section13 attributes an obstruction to norm-one Hilbert factorization of arbitrary witnesses to Aubrun's 2020 personal communication. It explicitly distinguishes that obstruction from the existence of a state with no suitable witness. We have no separate proof from that communication and will not use it as a counterexample.

## Later literature and eligibility

The bounded search, checked2 October2026, covered the exact title, tester terminology, completeness, factorization, Werner states, SIC/realignment comparisons, and the authors' current publication pages. [Shi–Sun's 2023 paper](https://arxiv.org/abs/2211.04868) studies a revised realignment family and its relation to enhanced realignment; its primary abstract and main theorem scopes do not assert all-tester completeness. [Nechita's 2025 lectures](https://nechita.net/assets/pages/teaching/icts-2025-tensor-norms-for-quantum-entanglement.html) retain the local-contraction framework and discuss pure-state detection. Neither is a universal resolution. Search snippets dating old2020 slides as recent were not treated as new results. No general resolution was located; this is not a novelty certification.

The direct UnsolvedMath page failed. The pinned imported record was used only to locate the primary source. All-reference local commit-message/path checks and live repository searches found no prior proof attempt; PRIOR_GATE.json records the exact coverage. Related SIC-existence imports concern Zauner's conjecture and do not duplicate tester completeness. Source PDFs and the lecture HTML are locally hash-bound in SOURCE_MANIFEST.json; raw sources and raw imported records are excluded from the public checkpoint.
