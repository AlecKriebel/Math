# Source audit and bibliographic corrections

Checked 2026-10-08 UTC. Retrieved-byte SHA-256 values and sizes are in
SOURCE_MANIFEST.json. Source documents were retained separately for inspection
and are excluded from this packet. No external researchers were contacted.

## Target and definitions

[Open Problem Garden, Generalised Empty Hexagon Conjecture](https://www.openproblemgarden.org/op/generalised_empty_hexagon_conjecture)
was inspected for the full statement, discussion, and bibliography. Its
emptiness condition excludes every additional point in the closed convex hull.
The word “convex” there is normalized to strict convexity using the same target
in the primary sources below, not weakened to six boundary points.

[Abel et al., Every Large Point Set contains Many Collinear Points or an Empty Pentagon](https://arxiv.org/abs/0904.0262)
was inspected at §1.1 (strict/weak convexity and closed-hull holes), §3 Lemma 7
(perturbation preserves only weak convexity), and the final open-problem
paragraph (the exact bounded-collinearity hexagon extension). The author-hosted
PDF identifies itself as arXiv:0904.0262v2. The paper's full pentagon proof was
not independently reconstructed here. The limiting argument in this packet is
an elementary adaptation of the standard perturbation mechanism, not a new
perturbation discovery.

## Known adjacent theorem

[Barát et al., Empty Pentagons in Point Sets with Collinearities](https://doi.org/10.1137/130950422)
is published in SIAM Journal on Discrete Mathematics 29(1), 198–209 (2015).
The inspected author-hosted manuscript is arXiv:1207.3633v1 (2012), pages 1–3,
including definitions, Theorem 1, the grid lower-bound discussion, and the
explicit unresolved hexagon case. The publisher abstract independently agrees
with the 328 ell^2 pentagon threshold. It is not a hexagon theorem. Its proof
was not rerun or formalized.

## General-position hexagons and correct Gerken DOI

[Gerken, Empty Convex Hexagons in Planar Point Sets](https://doi.org/10.1007/s00454-007-9018-x),
Discrete & Computational Geometry 39, 239–272 (2008): the publisher page and
Crossref record agree on **10.1007/s00454-007-9018-x** and the article title.
The conflicting inherited variant **10.1007/s00454-007-9008-x** returned HTTP
404 through Crossref and is not used. The publisher abstract explicitly assumes
general position. Gerken's complete article proof was not inspected in this
attempt, so it is not described as independently verified.

[Heule and Scheucher, Happy Ending: An Empty Hexagon in Every Set of 30 Points](https://arxiv.org/abs/2403.00737),
Theorem 1 and introduction, were inspected in the downloaded PDF, including
the no-three-collinear hypothesis and the equality h(6)=30. We use that theorem
as prior literature. We did not download or verify their full SAT certificates
or separately check the coordinates of the 29-point lower-bound example.

## Formal-verification scope and a second metadata correction

[Subercaseaux et al., Formal Verification of the Empty Hexagon Number](https://doi.org/10.4230/LIPIcs.ITP.2024.35),
ITP 2024, LIPIcs 309, 35:1–35:19, is the final published article. The official
publisher PDF was inspected at the theorem in §2, definitions in §3, §6.1's
computation description, §7's trust discussion, and §8's conclusion.

The Lean part verifies the geometry-to-CNF reduction. The paper describes
external LRAT checking with cake_lpr and a cube-and-conquer computation. It
also explicitly discusses the trust boundary between the generated CNF and
its checked external unsatisfiability, which is assumed as an axiom on the Lean
side. Therefore “formally verified” here must not be read as a claim that we
replayed an end-to-end kernel check of all computations.

An author-hosted copy at https://www.cs.cmu.edu/~mheule/publications/ITP24.pdf
was retrieved first and bears a stale **10.4230/LIPIcs.ITP.2024.24** on its
first page. The publisher confirms that .24 identifies a different paper;
**.35** is the correct final DOI for this title. Both retrieved PDFs have their
own hashes in the manifest; neither has been silently relabeled or overwritten.
The final published PDF is authoritative for bibliographic metadata.

## Search coverage and limits

Primary-source searches included the exact British and American spellings of
“generalised/generalized empty hexagon,” “empty hexagon collinearities,” and
bounded-collinearity variants with 2024–2026 terms. Results were checked against
the original problem, the pentagon papers, the sharp general-position result,
and its formal-verification paper. No inspected primary source resolves the
full all-ell statement. This is a bounded search finding, not a claim that
unindexed, inaccessible, or later work does not exist.

The inherited gate's public dataset hashes were freshly matched, and the exact
numeric target's absence of a substantive joined report was checked. The gate
is bounded by its repository/index/corpus coverage. It is not literature proof.
Source triage consumes none of the five mathematical approach slots.

## Publication boundary

This packet contains authored mathematical exposition, authored fixtures/code,
and public-source verification metadata only. Source HTML, PDFs, extracted
text, and full dataset bodies are excluded. The source hashes identify the
exact bytes inspected without distributing those bytes.
