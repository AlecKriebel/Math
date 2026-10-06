# Independent exact-target and primary-source audit of PR 22

**Verdict: PASS for the published negative answer to the literal target, with one current PR-description correction required before promotion.** No mathematical or source-attribution repair is required by this family. The checked head is `5dff69d1f25ac585a87bd8c71bc9d9c136e8c13c`; the checked mathematical document is `SOURCE_STATUS.md`, SHA-256 `b6d39596acb84613b15c43c5a9f6d2382bbd4826348638398d793fab4cbc7463`.

This family independently checked the exact original source, positive published prior, theorem-scope adapters, imported provenance, and historical hash bindings. It did not take an old PASS as evidence. It is an AI audit, not human peer review or a formal proof-assistant certificate. Numerical/jet reproduction belongs to the separately assigned mathematical families; this family does not claim it ran those scripts.

## Independence and immutable input

`CRITERION_AND_FIRST_PASS.md` and `FIRST_PASS_SEAL.json` were saved at 19:01:39 UTC before detailed primary proof inspection, historical audits, reviews, code, or outputs. The allowed candidate and source records had been read, so this is independence from prior certification rather than ignorance of the candidate. The subsequent actual-source assessment was sealed at 19:04:59 UTC, still before historical material. No root or sibling mathematical result was read before either seal.

All 15 frozen files were checked against both the snapshot SHA-256/size entries and exact Git-head blobs. Both imported records are byte-identical to the canonical serialization at the cited upstream revision. The full pinned prior reports, not just the imported summaries, were read after the source seal. The old review's source and report hash links are consistent; its PASS was only reconciled after independent evidence existed. No frozen input or historical review was changed. The one original attempt remains 1/5 and is shared with the duplicate.

## Exact original target

The original AIM document is dated 15 October 2003. Its complete preceding discussion distinguishes a general functional on a conformal class from a primitive obtained by the integral of a single-metric local natural invariant. Conjecture 1 on printed p. 17 uses the latter condition for the residual. Problem 30 on p. 28 repeats the same mathematical antecedent and conclusion. Their labels, surrounding explanation, OCR page-number artifacts, and imported titles do not produce two targets.

The statement imposes conformal invariance of the integral, with no formal-self-adjointness antecedent. The nearby independent divergence assertions are Conjectures 2–3 and Problems 31–32. The natural-density and critical polynomial context is confirmed by the density conversion and invariant filtration on pp. 16–18. The six-dimensional, parity-even polynomial counterexample lies inside that context, so its force does not depend on expanding “natural” to ratios, smooth nonpolynomial jet functions, orientation-sensitive constructions, or noncritical homogeneity.

The spectral determinant motivates the question, but the displayed universal implication does not require S to arise as a determinant's conformal gradient. Adding that condition would change the target and remove precisely the obstruction under review. A valid known counterexample at one allowed dimension refutes the universal original statement; it need not refute the restricted surface or four-dimensional results in the imported reports.

## Published prior and explicit adapter

The DML publication cover and institutional metadata identify Branson's article as published in 2005; the 2004 workshop/filename is not its publication year. The inspected mathematical passage is the full printed pp. 31–40, with direct images for ambiguous notation on pp. 32, 34, and 40. The definitions, Proposition 13, repaired Conjecture 14, and explicit nonsymmetric six-dimensional calculation support the attribution. The decisive paragraph is a proof calculation, not an abstract or unsupported dimension count.

Here is the independent adapter. Write

\[
V=\nabla^c(P_{ab|c}P^{ab}),\qquad B=|P|^2.
\]

Metric compatibility gives

\[
\nabla_c B=2P^{ab}\nabla_cP_{ab},\qquad
V=\tfrac12\nabla^c\nabla_c B.
\]

Thus, with the candidate's positive-contraction convention \(\Delta=\nabla^c\nabla_c\), its density \(S=(\Delta B)dV\) is exactly \(2VdV\). Branson's opposite spectral Laplacian convention changes the notation for Delta, not the nonzero obstruction. His printed calculation for V gives minus the skew expression for the other displayed divergence. Its leading specialization has a nonzero contraction of \(\nabla P\) with the test function's third derivatives even in conformally flat geometry. The candidate's cut-off harmonic cubic is a valid realization: at the selected point, \(P=0\), \(dJ=0\), and \(\nabla P=-\partial^3f\); the contraction has six unit terms. The V skew value is 12 with the candidate conventions, and multiplication by two gives the candidate's 24. This uses the explicit local proof mechanism rather than inferring a counterexample from a dimension count.

The published notation's generalized Q-space itself imposes self-adjointness. Therefore enlarging the allowed Q-representatives to that whole space would still not absorb this nonsymmetric density. No choice of an allowed Q and a pointwise invariant repairs the original implication.

## Why this obstructs the precise conclusion

For a natural local functional \(\mathcal F\), use affine conformal coordinates \(g_u=e^{2u}g\). If its first derivative is \(\int\varphi G_{g_u}\), commuting the mixed derivatives implies

\[
\int\varphi\,D_gG(\psi)=\int\psi\,D_gG(\varphi).
\]

This concerns the density-valued linearization and includes the volume variation. Standard critical Q has the self-adjoint critical GJMS linearization; the original two-metric primitive discussion gives the same symmetry. A pointwise invariant density has zero linearization. A constant linear combination of these terms therefore has symmetric linearization. The exhibited density does not, so it cannot meet the conclusion. This necessary test requires no converse inverse-variational theorem.

Under a constant metric rescaling by \(c^2\), the covariant Schouten tensor is unchanged, its squared norm scales by \(c^{-4}\), the Laplacian by \(c^{-2}\), and the six-dimensional volume by \(c^6\). Hence the example has the intended critical scalar weight minus six and density homogeneity zero. It is constructed by curvature contractions and derivatives, with no parity-odd ingredient or background field. Its integral is zero for every closed metric, stronger than the antecedent's conformal invariance. The smooth cut-off construction on the six-torus respects closedness and introduces no boundary, asymptotic decay, or global polynomial-coordinate assumption. The source's naturality and universal-metric hypotheses are therefore met.

## Adjacent theorems and repaired formulations

Alexakis's actual Theorem 1.1 specifies linear combinations of curvature-derivative complete contractions of weight minus n, with the invariant-integral hypothesis for every closed n-manifold and every smooth conformal factor. Its conclusion includes a natural divergence, with no primitive certificate. Here \(S\) is already such a divergence, so it is compatible with that theorem. The cited SIGMA paper states the result with the other proof-series parts; this family verifies its actual hypotheses/conclusion, not the full proof series anew. The counterexample does not depend on accepting that series.

The checked Case–Lin–Yuan PDF is explicitly arXiv v1, 15 November 2017. Its definitions on pp. 5–8 distinguish a conformal gradient from invariance of an integral; its critical-dimension primitive can depend on a background metric. Its complete weight-six discussion on pp. 30–32 constructs variational combinations, including terms involving Delta of the squared Schouten norm. Such a combination's variationality does not imply that each component divergence is variational. The candidate's separation is correct.

The current Case–Gover survey likewise starts the anomaly discussion from densities that already arise as functional gradients. Its published 2026 passage cites a BRST proof sketch for that variational anomaly classification. This does not change the original AIM antecedent. This family did not verify an equivalence with every natural-local repaired formulation or a complete all-dimensional repaired proof. Consequently the current statement must remain “this PR does not resolve the repaired conjecture”; it must not say that every repaired version is globally open or globally solved. The existing candidate respects that limit.

The original statement is therefore a known refuted conjecture. Within this queue's status convention, `already_solved` denotes this previously settled negative outcome; it is not a claim that the original affirmative formula became true. The duplicate should remain `duplicate` with no separate attempt or discovery credit. There is no new paper, DOI, or preprint package warranted for this source correction.

## Required current metadata correction

**P3: correct the live PR body's scope before accepting it.** It says all changes are confined to the numeric attempt directory and that there are no shared queue edits. The exact head changes `QUEUE.md` for both target and duplicate. Both sentences must be updated to describe that actual scope. This is a factual, readily repairable documentation issue, not a mathematical failure or reason to close the PR.

The frozen historical provenance/log's queue exclusion predates the later queue-update commits. Preserve it as history, with current acceptance metadata explicitly superseding that old isolation statement. Do not silently rewrite old reviews or original source-record status fields. Current records should also preserve the distinction between the actual 2017 preprint inspected and its 2019 journal publication rather than claiming journal pagination was checked.

No required mathematical correction, source-priority gap, positive-prior access hold, or hidden stronger unsolved target was found by this family. Exact mathematical verification and the final merged-candidate gate remain the parent task's responsibility. Family completion: 100%; program completion is not asserted.
