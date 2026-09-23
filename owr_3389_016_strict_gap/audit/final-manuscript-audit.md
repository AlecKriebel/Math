# Final manuscript audit

Checkpoint: 2026-09-23 03:52 UTC. Completion estimate for this review: **100%**. Independently reviewed `manuscript/paper.tex` against the supplied candidate and `audit/source-match.md`. This review assesses the mathematics and stated scope, not novelty or bibliography completeness.

## Verdict: mathematical PASS; one small wording repair requested

The manuscript proves the claimed strict gap inequality for every finite positive integer $J$ on every nonempty bounded open subset of $\mathbb R^n$, $n\ge1$, including irregular and disconnected sets. Its strict Yang proposition holds at every real $z>E_1$, and therefore is stronger than the candidate's threshold-only formulation. Replacing the candidate's Fourier/zero-extension obstruction with the short self-adjointness argument is valid.

The following were checked independently:

- The form-defined operator domain supplies coordinate multiplication and the commutator identity without boundary regularity.
- The first spectral moment equals one by $H_0^1$ approximation for a real normalized eigenfunction, and the second moment is the required squared derivative norm.
- All spectral rearrangements are absolutely convergent; the finite lower-block cancellation has the correct sign and no factor-of-two error.
- Finite spectral support gives $w\in\operatorname{Dom}H^2$, hence $v=(H-E)w\in\operatorname{Dom}H$. The differentiated interior equation identifies $(H-E)v=0$, and symmetry forces $v=0$, contradicting the first moment.
- The quadratic expansion and endpoint inference are correct. Repeated eigenvalues, $E_J=E_{J+1}$, and $E_{J+1}=E_1$ are all covered explicitly.
- There is no reliance on positivity of the eigenfunction, simplicity of $E_1$, connectedness, classical boundary traces, or unproved unique continuation.

## Wording repair

The text preceding equation `eq:one` starts “If $Hu=Eu$ and $\|u\|_2=1$,” and the support lemma says “For every normalized eigenfunction.” But the displayed integral uses $u\,\partial_\alpha u$ without complex conjugation. That literal integral identity requires **real** $u$: for example, replacing a real normalized eigenfunction by $iu$ changes its sign. The text has already chosen a real orthonormal eigenbasis, and every use of the lemma in the main proof is for that basis, so this is not a gap in the main theorem.

Recommended minimal repair: say “If $u$ is a real normalized eigenfunction with $Hu=Eu$” in the setup and “For every real normalized eigenfunction” in the lemma. Alternatively formulate and justify the first moment correctly in the complex Hilbert space. No other mathematical correction is needed.

## Exact source scope and normalization

The normalization paragraph correctly records the original report's missing square on $M_2$, uses $M_1^2-M_2^2$ throughout, supports that correction by the cited original gap estimate, and explicitly excludes the adjacent growth-bound question. The original report uses $n\ge2$; the manuscript proves the same corrected result with the harmless additional case $n=1$.

This distinction is material: the literal unsquared printed expression is not homogeneous under dilation and can be made an equality by rescaling. Therefore the paper resolves the **corrected, standard Harrell–Stubbe saturation question**, not a literal reading of the typographically inconsistent expression. The manuscript's body makes this limitation explicit. For maximum precision, its abstract could call it the “corrected saturation question”; that is an editorial improvement, not an additional mathematical gap.

The temporarily incomplete Levitin–Parnovski DOI was excluded from this review as requested. Priority remains conditional on the separate dated literature audit. Apart from the real-valued wording repair above, no unresolved mathematical concern was found.

## Parent closure — 2026-09-23T04:02:39Z

The requested real-valued wording repair is incorporated in both the setup and Lemma 2. The abstract now explicitly says corrected saturation question. The added Ashbaugh 2002 reference and the statement of its p. 12 unresolved strictness discussion were independently verified visually against the archived publisher PDF. All three pages of the rebuilt manuscript were rendered and visually inspected. No clipped equations or missing text were found.

Final reviewed TeX SHA-256: `910cc4017390df7c33e08cd80c84a606047e145cd4ff9d6df6f76c5b67e83aff`.
Final reviewed PDF SHA-256: `530187134c9166c1d88d6dedf0237f383bd0505bce89578d3b793e2007b83473`.
