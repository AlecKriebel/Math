# Source gate: differential criteria for low-genus curves on surfaces

Checked 20 October 2026. Queue row 1830; ID 30003253; source key OWR-15170-020.

## Verdict

**The original source is recovered, but the catalogue's purportedly verified reformulation is not an equivalent statement.** The authentic problem is an open-ended request for hypotheses making the branched-cover/symmetric-differential method work. Existing results already establish the ramification and degree-negativity mechanism, and later work gives substantial sufficient conditions for cyclic-cover families. No complete general low-twist existence criterion was verified in this search.

This is a source/status gate, not a proof attempt or an audit of the cited proofs. It makes no queue change and publishes nothing. Do not claim a solution by reproving the existing pullback argument, disproving the catalogue rewrite, or substituting a general hyperbolicity conjecture.

## Authentic target

Natalia Garcia-Fritz, *Curves of Low Genus on Surfaces and Some Extensions of Büchi's Problem*, printed pp. 2839–2842, especially Question 1 on p. 2841, in *Definability and Decidability Problems in Number Theory*, Oberwolfach Reports 13 (2016), no. 4, 2793–2866, DOI 10.4171/OWR/2016/49. Workshop: 23–29 October 2016; publication: 21 December 2017. [Official record](https://ems.press/journals/owr/articles/15170); [official PDF](https://ems.press/content/serial-article-files/46652).

The question asks for conditions on a complex algebraic surface and a morphism \(\pi:X\to\mathbf P^2\), relating its branch divisor \(B\) to a low-degree twist \(L\), so that a useful symmetric differential
\[
\omega\in H^0(\mathbf P^2,L\otimes\operatorname{Sym}^r\Omega^1_{\mathbf P^2})
\]
makes **every irreducible component of \(B\)** integral. Degree is to be controlled against curves upstairs of **geometric genus at most a fixed \(g\)**. The motivating examples concern genus 0 and 1. The request is for hypotheses, not a universal implication with a fixed numerical bound. No value of \(r\), formal minimization procedure, or explicit finiteness assumption on \(\pi\) is stated. Smooth projective surfaces are the method's setting; Question 1 itself does not repeat all those assumptions. Higher-dimensional completeness is separate Question 2. The relevant object is a symmetric power of ordinary cotangent differentials, not a higher-jet bundle.

## Catalogue discrepancy and scope lock

The recovered catalogue record adds a different premise: a minimum-degree line bundle having a scalar section that vanishes on images of all low-genus curves. It then asks for a differential integral both on those images and on the branch components. Its `corrected_verified` label should not be treated as evidence that these additions were checked correctly.

For future work, distinguish three tasks:

1. **Existence:** obtain an appropriate nonzero branch-integral symmetric differential with sufficiently favorable twist. Nonzero is indispensable for an effective method, even though the informal question does not separately write that predicate.
2. **Transfer:** use ramification to improve the upstairs twist and force genus-bounded curves to be integral. This has established theorems below.
3. **Completeness:** determine all integral curves for the chosen differential. This is an additional computation, not automatic from genus vanishing.

A formal research theorem must declare the surface and morphism class, the positive integer \(r\), the twist being optimized, and its claimed coverage. Merely saying that the branch divisor is large is insufficient. The source does not promise that every smooth projective surface has the desired differential or that all low-genus curves form a finite set.

## The established mechanism predates the question

Garcia-Fritz's 2015 Queen's thesis, *Curves of low genus on surfaces and applications to Diophantine problems*, provides the precise background. [Institutional full text](https://qspace.library.queensu.ca/bitstreams/007eb1de-ecf4-4747-a756-f7cac789ba56/download).

For normalization \(\nu:\widetilde C\to X\), integrality means the image of \(\nu^*\omega\) in
\(H^0(\widetilde C,\nu^*L\otimes K_{\widetilde C}^{\otimes r})\) is zero. It does **not** mean all coefficients vanish along \(C\).

- Proposition 3.42, pp. 107–108: for a smooth projective surface, \(r\in\mathbb N\), and \(g(C)\le N\), the inequality \(\deg\nu^*L<2r-2rN\) forces \(C\) to be integral for every such global differential.
- Theorem 3.87, pp. 147–150: for a dominant morphism between smooth integral complex surfaces and a prime divisor \(D\) mapping onto an integral curve, branch integrality implies the pulled-back differential vanishes along \((e_D-1)D\). The theorem does not require the morphism to be finite.
- Theorem 3.76, pp. 138–139: away from the specified local degeneracy/discriminant locus, the sum of multiplicities of integral curves through a point is at most \(r\). This can certify local completeness but is not a blanket algorithm listing every curve.

These are existing ingredients, not a new answer to low-twist existence.

## Later sufficient conditions, and their boundary

Garcia-Fritz–Urzúa, *Families of explicit quasi-hyperbolic and hyperbolic surfaces*, Math. Z. 296 (2020), 573–593, DOI 10.1007/s00209-019-02439-x. The theorem statement inspected is [arXiv:1804.07671v1](https://arxiv.org/abs/1804.07671), Theorem 5.1; publication metadata is confirmed by the [authors' institution](https://www.mat.uc.cl/publicaciones?isipage=35&tpane=isi).

Start with a smooth projective surface \(Y\), a differential \(\omega\in H^0(Y,L\otimes\operatorname{Sym}^r\Omega_Y^1)\), and cyclic-cover data
\[
m_iM_i=\sum_j a_{ij}D_{ij},\qquad
0<a_{ij}<m_i,\quad \gcd(a_{ij},m_i)=1.
\]
Assume the total branch arrangement has simple normal crossings, each \(D_{ij}\) is \(\omega\)-integral, \(a_{ij}\not\equiv-a_{ij'}\pmod{m_i}\) for distinct indices within each stage, and
\[
\sum_i\frac1{m_i}\sum_jD_{ij}-L
\quad\text{is \(\mathbf Q\)-ample.}
\]
Then genus-0/1 curves on the resulting normal cyclic tower lie over integral curves on \(Y\). Resolutions and cyclic quotient singularities enter the proof. The paper also gives explicit branch arrangements and hyperbolic examples.

**Boundary:** the theorem assumes the relevant differential and integral branch arrangement; it does not characterize their existence at optimal twist for arbitrary surfaces or morphisms. It is important published progress on the original program, not a verified complete solution. The abstract's generality should not be enlarged beyond these hypotheses.

## Current literature check

- Bruin–Thomas–Várilly-Alvarado, *Explicit computation of symmetric differentials and its application to quasi-hyperbolicity*, Algebra & Number Theory 16 (2022), 1377–1405, DOI 10.2140/ant.2022.16.1377. [Author manuscript, arXiv:1912.08908v3](https://arxiv.org/abs/1912.08908). Its introduction explicitly treats determination of integral curves as generally difficult. It gives effective constraints for nodal surfaces and dimension estimates, including Barth and cuboid examples, rather than a general branch/minimal-twist criterion.
- Stoll–Testa, *The surface parametrizing cuboids*, author-hosted manuscript dated 24 February 2025. Its current abstract gives a classification of integral curves of degree at most six on that particular surface, not all genus-bounded curves on arbitrary surfaces. [Current manuscript](https://www.mathe2.uni-bayreuth.de/stoll/papers/Cuboidi.pdf).
- [Garcia-Fritz–Pasten, arXiv:2406.00835](https://arxiv.org/abs/2406.00835), and [Chen–Garcia-Fritz–Mathur–Pasten, arXiv:2602.06956](https://arxiv.org/abs/2602.06956), were screened at abstract level. Their stated targets are symmetric-product hyperbolicity and arithmetic integral-point degeneracy, respectively; neither abstract announces the missing criterion. These were not full-text audits.

**Status wording supported by this pass:** source correction required; substantial known sufficient criteria, but no verified general resolution of the original existence/optimal-twist request. This is a bounded negative literature finding, not proof that no later solution exists. The catalogue's higher-dimensional discussion should not be used to redefine this row.

## Verification metadata

Fresh local rehashes, not fresh upstream corpus downloads:

- `problems.json`: 68,931,837 bytes; SHA-256 `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`; 15,458 records; exactly one ID/source-key match.
- `research_results.json`: 80,334,822 bytes; SHA-256 `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`; 6,701 records; no ID/source-key match in keys or serialized values.

The official OWR PDF has 74 pages, 672,899 bytes, SHA-256 `d020cdff122c3b8f91082006f5ba2e07aba536f58072de581fc6facca2f1f2fd`. Printed p. 2841 was visually inspected. Additional public-source hashes, sizes, and inspection scope are in `SOURCE_METADATA.json`; corpus match metadata is in `CORPUS_VERIFICATION.json`. Raw third-party PDFs, extraction text, and the catalogue record are not part of the authored deliverable.

Retrieval limits: the author's homepage and a coauthor paper-list route returned HTTP 502. A publisher-PDF route returned HTML, so the cyclic-cover theorem is attributed to the inspected arXiv version. A guessed MSP article slot was a different paper and was excluded. No inaccessible source was represented as inspected.
