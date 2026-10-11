# Audit of the equivariant quotient counterexample

Audit date: 11 October 2026.

## Review and distribution status

This is an AI-assisted, unrefereed authored reconstruction of an already published example. The review consists of one independent reconstruction plus review of that reconstruction, not a second independent mathematical audit. The internal AI mathematical audit is not external human peer review or formal proof-assistant certification. This eight-file prose edition is not a computational reproduction package. No source-author code, executable checker, copied source document, dataset contents, raw output, or private coordination material is distributed. File hashes authenticate bytes, not mathematical truth.

## Verdict

Accepted as a prior negative resolution of problem 30000663, OWR-1452-027, titled *Unramified Quotients of Equivariant Endomorphisms*. The exact map on the exact smooth affine complex surface satisfies every stated hypothesis and induces a ramified quotient map. The construction is credited to Dubouloz–Palka, Theorem D and Example 4.3. No novelty is claimed.

## Checks completed

- The original report's question and surrounding hypotheses were read and visually inspected. Surjectivity, properness, factoriality, and Euler characteristic one are not assumptions of this question.
- Integrality, dimension two, global smoothness, and normality of the surface were checked algebraically.
- The algebraic group action is effective and the map commutes with exactly the same action, without a group homomorphism twist.
- Polynomial preservation of the surface equation and global regularity were checked.
- Two explicit rank-two finite étale algebra presentations cover every source point and establish algebraic étaleness, including flatness.
- A separate tangent-space computation checks both the generic locus and the exceptional locus z=0. Points with x=0 are covered because z=±1.
- The invariant ring was computed directly from the grading. It is C[z].
- The quotient map is z↦2z²−1. Its relative differential module has nonzero fiber at zero, and its ramification index there is two.
- The exact image was computed: it is the complement of the entire line y=0, z=−1. All nonempty fibers have two points. Surjectivity is not claimed.
- The polynomial and scalar parameters were substituted into Theorem D, checking equations (4.3)–(4.7), in addition to the Chebyshev specialization in Example 4.3.
- Degenerate-fiber multiplicities were matched with the relation in Lemma 2.18. The proof does not depend on unverified general steps of that lemma.

## Inspected sources and version limits

Original source: Miyanishi's contribution in *Affine Algebraic Geometry*, Oberwolfach Report 01/2007, printed p. 74, PDF p. 70; [report PDF](https://ems.press/content/serial-article-files/46087?nt=1), [DOI](https://doi.org/10.4171/owr/2007/01). The full PDF has 78 pages, 641506 bytes, SHA-256 a9b3fa5ac48466165296f9825711a2fb3e05e142e0585bc969d19005c9157ca7. The relevant page was read as text and visually inspected; the other pages were not mathematically audited.

Later source: Adrien Dubouloz and Karol Palka, *The Jacobian Conjecture fails for pseudo-planes*, Advances in Mathematics 339 (2018), 248–284, [DOI](https://doi.org/10.1016/j.aim.2018.09.020). The inspected full text is [arXiv:1701.01425v2](https://arxiv.org/pdf/1701.01425v2), dated 5 September 2018, with 26 pages. A fresh retrieval of that explicit version on 11 October 2026 was byte-identical to the retained unversioned retrieval: 597765 bytes, SHA-256 41150cfda4fdf477efefc7d2ce55bc5fb49941705620b567b3333df5fe84281e. The current arXiv landing page independently confirms v2 and the journal reference. A publisher-formatted PDF was not inspected, and byte identity with the publisher PDF is not asserted.

Text read in the later paper: pp. 1–2, 8–10, 17–21. Visually inspected: pp. 18–21. The decisive passages are the definition and action in (1.1), the étale discussion in §2D, Lemma 2.18 and its proof, Theorem D including its converse and proof, and Example 4.3. The complete published theorem classification, all bibliography, other examples, and the ordinary Jacobian Conjecture were outside this audit. The displayed construction has been reconstructed independently, so neither the example's wording nor the theorem's citation is treated as a substitute for proof.

## The old reductive assertion

The original report prints a positive assertion for connected reductive groups. The direct counterexample uses G=C*, which is connected and reductive, so that unrestricted assertion does not survive. The source does not state the extra surjectivity condition that would exclude this example. The audit does not infer an unstated condition or claim to settle any strengthened formulation.

The map sends a point with z=0, whose stabilizer is trivial, to a point with x=0 and y≠0, whose stabilizer is the group of square roots of unity. Thus same-action equivariance does not force preservation of stabilizers here. This is consistent with, rather than an obstruction to, the direct calculation.

## Verification boundaries

The written proof is the mathematical certificate. Symbolic polynomial checks are supplemental and do not alone establish smoothness, étaleness, invariant-ring universality, or the original hypotheses. File hashes certify retained bytes and closed inventory only; they do not certify theorem truth. No mathematical source-author code was executed.

The external input records and complete corpora were authenticated before mathematical reliance. The literature searches were bounded and do not establish an exhaustive present-day or unpublished-literature survey. This audit is a verification of an already complete published example rather than a new search for a counterexample.
