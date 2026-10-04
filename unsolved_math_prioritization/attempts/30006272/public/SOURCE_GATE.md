# Source, identity, and scope gate

Checked 2026-10-04 UTC. The exact primary mathematical question is recovered.
**No full resolution is claimed.** Recommended status: unsolved, 5/5
substantive approaches. This gate concerns source identity and honest scope;
it is not an independent mathematical audit.

## Primary target and catalogue mismatch

- Catalogue ID: 30006272; code: OWR-14299283-013; rank: 554.
- The requested [catalogue endpoint](https://www.unsolvedmath.com/problems/30006272)
  was attempted directly and by web retrieval. Direct retrieval returned
  HTTP 403; web retrieval failed. Its current text was not recovered.
- The repository queue identifies this ID with “Catalan Formulas for
  Ekedahl-Oort Intersection Cohomology”. The linked primary report instead
  concerns orbit closures of complexes of vector spaces. The notation on
  printed p.1316 is a calligraphic E indexed by an orbit O, not
  “Ekedahl–Oort”. The whole report has no Ekedahl occurrence.
- Primary source: Markus Reineke, joint work with Xin Fang, “Local
  intersection cohomology of varieties of complexes,” in *Enveloping Algebras
  and Geometric Representation Theory*, Oberwolfach Report 25/2025,
  pp.1315–1316. [Publisher](https://ems.press/journals/owr/articles/14299283),
  [PDF](https://ems.press/content/serial-article-files/51851),
  [DOI](https://doi.org/10.4171/OWR/2025/25).

Both pages were read, and p.1316 was visually inspected. The question asks
for an explicit Catalan-combinatorial extension of the construction to all
canonical-basis elements indexed by complexes' orbits. The preceding
theorem only covers irreducible components, characterized by nonadjacent
positive homology dimensions. Neither a particular Catalan model nor
specific conjectural coefficients are stated. The recovered primary
question, rather than the erroneous catalogue title, is the target here.

For differential f_i:V_i -> V_{i+1}, the correct dimension convention is
d_i=h_i+r_{i-1}+r_i, as in the cited preprint §2. The report's displayed
r_{i+1} is an indexing typo. The boundary ranks are zero. These conventions
are explicit in this packet and its checker.

## Proof sources read and used

1. **Xin Fang and Markus Reineke**, *Local intersection cohomology of
   varieties of complexes*, [arXiv:2502.07688v1](https://arxiv.org/abs/2502.07688v1),
   11 February 2025; journal DOI
   [10.1093/imrn/rnaf241](https://doi.org/10.1093/imrn/rnaf241).
   All nine preprint pages were read, including the full proofs of
   Theorems 4.1 and 5.1, the quantum-binomial transformation and degree
   estimate, and the coefficient normalization in §3, equation (1).
   Their sparse-support theorem is prior work, not a resolution of the
   report's all-orbits extension. This packet uses its standard
   quiver IC/canonical-basis comparison; restricted new calculations
   here carry no novelty claim. The journal full text was not retrieved.

2. **Mark Andrea de Cataldo and Luca Migliorini**, *The Decomposition
   Theorem and the topology of algebraic maps*,
   [arXiv:0712.0349](https://arxiv.org/abs/0712.0349).
   Read §4.2 through §4.2.1 (preprint pp.55–59), including Proposition
   4.2.1, Remark 4.2.4, Theorems 4.2.7 and 4.2.9, and the explanation
   of component-monodromy local systems and intersection-form splitting.
   These supply the standard small and semismall decomposition results.
   Their general Hodge-theoretic foundations are treated as established
   theorems, not re-proved or machine-verified here. The hypotheses needed
   for the constructed incidence maps are checked in PROOF.md.

## Update and previous-attempt checks

The arXiv abstract/history retrieved in this pass lists only v1. The
[author's current bibliography](https://math.ruhr-uni-bochum.de/en/fakultaet/arbeitsbereiche/algebra/research-team-reineke/team/prof-dr-markus-reineke/)
identifies the 2025 IMRN publication. Searches for the exact title,
Fang–Reineke with Catalan and complexes, and varieties of complexes with
semismallness did not locate a subsequent all-orbits formula. This is a
bounded literature check, not proof that no such result exists.

The live repository queue was fetched before research; its row was queued
at 0/5. Separate GitHub searches checked PRs by ID, “Ekedahl”, the quoted
Catalan title, and “complexes”, plus commits, branches and default-branch
code by ID. No matching earlier attempt was located; the sole “complexes”
PR result was unrelated Hudson subdivision work (#54). The queue label
alone was not treated as evidence of no previous attempt. Search indexing
and unindexed history remain limitations. The full queue and remote search
responses are not part of the public mathematical packet.

## What this packet does and does not establish

- Proven: local cancellation/slice reduction; image/kernel incidence
  smallness criteria; Gaussian-product IC formulas in their chambers;
  exact image-semismallness and relevant-path criteria; a semismall
  decomposition relation; a fully evaluated non-sparse three-vertex case.
- Refuted: dropping sparse support unchanged from the existing formula;
  a rank-one 2 by 2 determinant already contradicts that extrapolation.
- Open here: an explicit uniform Catalan formula for all orbit closures.
  The chosen incidence maps fail outside specified chambers; this is no
  nonexistence theorem for other methods.
- The checker is bounded exact arithmetic. It does not compute IC
  independently, certify novelty, or resolve the original general question.

Only authored mathematical documents, the checker, its results, and hashes
belong in the public packet. Source PDFs, page images, extracted source
text, HTML, repository snapshots and raw search results stay local.
