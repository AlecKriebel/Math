# Independent adversarial priority audit: PR1118

Problem 30004231 / OWR-17135-028. Audited claim pinned to head `8592fb7297d3c4973f2778c47cfa8972cba896a6`. This report concerns priority and scope; the independent mathematical audits are separate. No PR, Git reference, input manuscript, publication, or external correspondence was changed.

## Verdict

**NO_IDENTIFIED_FULL_TARGET_PRIORITY_BLOCK — bounded audit, not a novelty certification.**

The searched and inspected primary literature did not supply a previous counterexample, or an established theorem plus a verified bridge, that already settles **both** of the exact printed unrestricted assertions. The decisive remaining test is any prior nonshellability result for the exact positive-plus-additive poset: together with the classical homology antecedent, that would complete an earlier full negative resolution. The two assertions may be resolved by different examples or sources; no earlier identical prism construction or joint example is required. No such prior exact-poset nonshellability result was identified. Consequently this audit does not support an “already solved” exclusion for the full target. It also does not justify an unqualified worldwide-first claim.

There is a material inspection limit: Adiprasito’s closest related note was published in 2024 under a changed title. Its public 2020 author manuscript was fully available and its exact definition was inspected; the actual 2024 article body is paywalled and was not read. The published abstract is about stable complete intersections. It is evidence for the article’s advertised scope, not proof that its uninspected body contains no further observation.

The contribution candidate is a small, explicit counterexample to the **printed exact face-poset question**. It is not a negative solution of the stable/generic tropical complete-intersection shellability program. Classical simplex-difference geometry, exact-decomposition terminology, and the six-point homology control must not be advertised as new.

## Exact claim tested

In [Payne’s printed Problem 3](https://ems.press/content/serial-article-files/46818), OWR39/2019, printed 2464 / physical 70, a qualifying face has canonical summands satisfying
$$
\dim F_1,\dim F_2>0,\qquad \dim(F_1+F_2)=\dim F_1+\dim F_2.
$$
The questions ask shellability of their inclusion poset and rational homology of a wedge of $(n-2)$-spheres. The page states no genericity, facets-only, simplicial, or relative-general-position hypothesis.

The pinned proof uses $P_1=D_4\times[0,1]$, $P_2=(-D_4)\times[0,1]$ in $\mathbb R^5$. The ordinary order complex is $K\sqcup K$, with each $K$ a connected pure graph having 50 vertices and 60 edges; ordinary rational Betti numbers are $(2,22,0,\ldots)$. Thus both printed assertions fail. No adjoined extremum, empty-complex convention, dimension-zero shellability convention, or lower-dimensional embedding is used. The $\mathbb R^3$ control has six points and refutes only the homology assertion.

The main example also fails the superficially corrected sphere dimension $n-3$: it has nonzero reduced $H_0$ and $H_1$. This is useful because any qualifying proper face has dimension at least 2, so its chains have order-complex dimension at most $n-3$. It does not establish what unprinted question the speaker intended.

## Decisive definition comparison

[Adiprasito’s author manuscript dated 27 July 2020](https://webusers.imj-prg.fr/~karim.adiprasito/cint.pdf), Theorem 1.2 and Corollary 1.3, gives a positive homotopy Cohen–Macaulay result for stable complete intersections and the associated mixed-face poset. On p 2 its mixed condition is
$$
\dim\Bigl(\sum_{i\in J}F_i\Bigr)\ge |J| \quad\text{for every subset }J.
$$
For two summands this asks positive individual dimensions and sum dimension at least 2. It does **not** ask full dimension additivity. These conditions agree in suitably exact situations, but they differ in the pinned example.

For a proper simplex-difference face $F(A,B)$ with $|A|=|B|=2$, the vertical prism face $F(A,B)\times[0,2]$ has canonical summands of dimensions 2 and 2, while its own dimension is 3. It is retained by the subset condition and removed by the printed equality. In the larger poset it contains both endpoint copies of $F(A,B)$, producing a path between them in its order complex. Thus one cannot identify the disconnected exact-filtered poset with the stable mixed-face poset.

The note appeared as [A note on the topology of Minkowski sums and complete intersections](https://doi.org/10.4310/pamq.2024.v20.n1.a2), *Pure and Applied Mathematics Quarterly* 20(1)(2024),17–28. Public publisher metadata inspected independently by the parent gives received 2 July 2022, accepted 2 February 2023, published 26 March 2024. The author’s homepage and [institutional article record](https://cris.huji.ac.il/en/publications/a-note-on-the-topology-of-minkowski-sums-and-complete-intersectio/) establish the title/publication connection. Cite this published work explicitly, while identifying the accessible earlier manuscript as the source actually inspected for the displayed definition.

## Prior results and direct-consequence checks

[Sturmfels–Tevelev, Elimination Theory for Tropical Varieties](https://arxiv.org/abs/0704.3471), submitted 26 April 2007 and published *Math. Res. Lett.*15(2008),543–562, is especially relevant. Theorem 4.3 gives the same subset-dimension support criterion for a generic complete intersection. Example 1.3, with scaled opposite tetrahedra, explicitly gives a six-ray tropical curve; Example 4.10 records the 12 vertices,24 edges,14 facets of their sum. Thus the geometry behind the small six-point control is classical. Their Example 5.2 concerns a projected tropical variety and absence of a coarsest supported fan; it supplies no exact two-summand face-poset representation or non-shellability result for the target.

[Fukuda–Weibel, On f-vectors of Minkowski additions of convex polytopes](https://arxiv.org/abs/math/0510470), v1(2005), v4(2006), published *Discrete Comput. Geom.*37(2007),503–516, already uses “exact decomposition” for the printed dimension equality. Theorems 1 and 6 describe the face structure of a perfectly centered simplex plus its polar, which includes the classical combinatorics underlying simplex differences after the usual affine/scaling identification. [Their later exact-decomposition paper](https://arxiv.org/abs/0712.0027), v1(2007),v2(2008), published *European J. Combin.*31(2010),565–573, studies face numbers and general position. Neither inspected body supplied the exact-filter/shared-interval non-shellability observation. The elementary classification in the pinned proof is a convenient rederivation of classical structure, not a new face-lattice theorem.

[Adiprasito–Sanyal 2016](https://www.numdam.org/item/10.1007/s10240-016-0083-7.pdf) treats relative Cayley complexes, mixed face numbers and general-position families. It supplies neither the required nongeneric filtered-poset counterexample nor a contradiction to it. [Frick–Sanyal’s universality of Minkowski complexes](https://arxiv.org/abs/1607.07814) concerns a different complex: subsets of summand labels whose sums avoid a fixed point. Universality there cannot be transferred to this two-summand face poset without an additional realizability theorem; none was established.

[Hacking 2008](https://arxiv.org/abs/0711.1847), Theorem 2.5, includes the smoothness and connectedness requirements on torus strata and concerns the tropical link of dimension $\dim X-1$. [Markwig–Yu 2009](https://arxiv.org/abs/0711.0944) proves shellability for a particular tropical moduli space; its historical discussion of generic complete intersections is not an exact negative answer here. [Wang 2023](https://arxiv.org/abs/2306.15147) explicitly assumes generic independently sampled coefficients for its bend-locus connectivity result.

The recent [Hiatt–Simpson–Wang–Wu preprint](https://arxiv.org/abs/2606.10817),9 June 2026, §8, gives a tropical fan with lower link homology using a monomial projection of an arrangement tropicalization. The section does not provide two polytopes whose positive/exact mixed-face poset realizes it. A general tropical fan is not automatically such a filtered poset. The absent bridge is a substantive realizability claim; treating it as automatic would transfer the problem to an unsupported assertion. No particular numerical Betti table from that paper is needed for this comparison.

## Cited paper: versions must not be conflated

The original cited [ABPPS arXiv 1607.00347 v 1](https://arxiv.org/abs/1607.00347) was submitted 1 July 2016; the current arXiv record still lists onlyv 1. Its §1.2 definition of totally mixed requires **summand facets**, unlike the printed positive-dimension/exact-additivity condition.

The actual [published PDF](https://academic.oup.com/imrn/article-pdf/2019/6/1894/28707272/rnx184.pdf) was opened and read. It appeared online 19 August 2017 and in *IMRN*2019(6),1894–1919, DOI 10.1093/imrn/rnx 184. It retains the summand-facet definition, renumbers Lemma 3.7 to Lemma 3.8, and corrects Theorem 1.4’s ambient-dimension formula from the arXiv presentation. The published theorem uses $D=\sum d_i-s$. Record this version difference; do not copy the v1 ambient formula into a comparison with the published theorem.

The full [earlier Payne conference abstract](https://sci-tech.ksc.kwansei.ac.jp/~hohsugi/CREST/abstract%28ver0%29.pdf) was freshly fetched and its page 24 read. It describes positive-dimensional summand faces without stating additivity, and announces topological discussion rather than supplying a proof. Its PDF metadata suggests 2012, but an exact public posting/conference date was not conclusively verified.

## Framing and disposition recommendation

Under the user’s strict “skip already solved” rule, the present evidence does **not** trigger SKIP_ALREADY_SOLVED for the full two-question target. Retain the candidate for the parent’s decision, with the recorded scope and access limitations. No stronger generic/stable claim is present in the pinned proof.

A defensible title/framing is **Counterexamples to the printed totally mixed face-poset questions**. State that the summands deliberately share an interval factor and that the result concerns the literal 2019 definition. The strongest verified content is the explicit full-dimensional lattice-polytopal counterexample and exact homology calculation. The candidate observation beyond the classical components is the loss of the vertical faces under the exact filter, producing a disconnected pure graph and hence non-shellability.

Before promotion, add prominent Adiprasito 2020/2024 and Sturmfels–Tevelev citations, credit the classical simplex-difference/exact-decomposition structure to the older literature, and retain the distinction from stable/generic questions. The current proof’s “no novelty claim” language remains appropriate. Do not claim that the abstract, a genericity theorem, an unrelated universality theorem, or a general tropical counterexample already proves or disproves this exact claim.

The audit used 105 fresh query executions, with 105 distinct query strings, across exact terminology, synonymous conditions, construction components, older exact-face theory, later topology results, and current citation trails, in addition to the inherited five-query audit. The machine-readable ledgers preserve exact strings, source identities, version dates, hashes, and access limitations. Search engines, public sources and finite reading cannot exclude unindexed or unpublished prior work. Reading the paywalled 2024 body through lawful access would reduce the most concrete remaining coverage gap; no outreach or purchase was initiated.

