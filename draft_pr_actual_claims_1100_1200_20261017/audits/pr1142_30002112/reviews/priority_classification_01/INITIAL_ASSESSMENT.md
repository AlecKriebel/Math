# Independent initial classification

Recorded at 2026-10-17 23:23:17 UTC, before reading the candidate proof, any earlier audit, or any other review.

## Finding

An earlier full negative result has been located. Luc Pétiard's arXiv:1706.09189v1 (submitted 2017-06-28 09:53:24 UTC), Theorem 2 on PDF p.2, already rules out bounds consisting of an arbitrary continuous function of the isoperimetric ratio plus a dimensional multiple of the Weyl-order index term, for connected smooth compact embedded hypersurfaces in each dimension at least three. His 2019 Neuchâtel thesis extends the recorded construction and conclusion to boundary dimension two as well: Chapter 2, especially Theorem 2.1.2 on printed p.24, with full construction on printed pp.26–30. I have read the whole six-page 2017 preprint and the complete relevant thesis chapter (printed pp.23–30), together with the thesis's introduction to the same question (printed pp.16–18). The thesis records its successful defense date as 2019-02-05.

This is already a recorded full-target counterexample result, rather than a case in which generic older tools yield the target only after a new deduction. It is stronger on connectedness: the counterexamples can have connected boundary. The construction is recognizably the same spectral mechanism as the assignment's candidate outline: large first-positive-eigenvalue component, a round sphere whose spectrum gives the initial eigenvalues, and enough total area to force an arbitrarily large normalized spectral coefficient. The published/preprint record must be distinguished: the 2017 arXiv theorem is stated for dimension at least three; the 2019 thesis explicitly includes dimension two. I have not yet found a journal version.

## Checkable bridge to the original question

Write the target's one-based eigenvalues as L_k and Pétiard's zero-based eigenvalues as mu_j. Then L_(j+1)=mu_j. Set p=2/m and a=1+p. For any proposed finite target constants A_m,B_m, take a continuous function F(t)=A_m t^a, and choose a prior-theorem spectral coefficient C>2^p max(B_m,0). For arbitrarily large j, the earlier m>=3 theorem supplies a connected Euclidean hypersurface with

    mu_j |Sigma|^p > F(I) + C j^p.

Since (j+1)^p <= 2^p j^p for j>=1, this violates the target at k=j+1. Every compact connected embedded Euclidean hypersurface used here is the smooth boundary of its bounded connected side, so the domain convention does not exclude it.

For m=2, the thesis theorem gives, for an arbitrarily chosen positive coefficient C, a single finite isoperimetric ceiling J and arbitrarily large indices j for which the normalized eigenvalue exceeds 2C j^p. Fix the proposed constants first, choose C large enough that 2C>2^p max(B_m,0), then choose j sufficiently large to absorb max(A_m,0) J^a. This yields the same contradiction. The theorem's fixed J depends on C, not on j; that quantifier order is the decisive distinction from mere unbounded first eigenvalues.

## Provisional assessment and remaining work

Priority classification: earlier full negative answer located, with a dimension-three-and-higher preprint in 2017 and full dimension-at-least-two thesis result in 2019. Completion estimate: 55% of this audit. Remaining checks: render the relevant pages to confirm typography and dimensions; trace bibliographic versions and later primary citers; inspect proof assumptions concerning spectral convergence and two-component volumes; document search limits and pin all material read. The candidate proof remains unread at this checkpoint.

Primary URLs: https://arxiv.org/abs/1706.09189 ; https://arxiv.org/pdf/1706.09189v1 ; https://libra.unine.ch/server/api/core/bitstreams/cb35ac23-61a8-402a-9fdb-a1eb4d47c041/content .
