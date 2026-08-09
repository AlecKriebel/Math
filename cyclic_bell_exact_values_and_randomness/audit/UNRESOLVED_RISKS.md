# Unresolved risks

Audit date: 2026-08-09

The revised mathematical verdict is positive. The following are remaining
specialist-review or release risks; none authorizes a stronger claim than the
claims ledger.

| Priority | Risk | Present evidence | Required closure |
|---|---|---|---|
| High | The restored support-rigidity proof is technically dense and could hide a support or invariance slip. | The proof separately checks residual saturation, Schmidt support cancellation, bad-kernel exclusion, $A_0K=K$, $V_yK=K$, adjacent reflections, and the finite-rank count. **verify_rigidity.py** passes 89,439 phase/reflection triples, 840 hostile rank products, and 16,128 dimension cases. | Obtain specialist scrutiny of Appendix **app:rigidity-proof**, especially the passage from vector stabilizers to $K$, kernel-safe cancellation, and the supported $d$-th-power step. Preserve the finite-dimensional tensor-product first-augmented scope. |
| High | Convention drift could reintroduce a missing adjoint, transpose, or conjugation. | The source has adjacent no-adjoint and all-adjoint Bob conventions and briefly omits Alice's conjugation near the second construction. The revised appendix identifies the source and polar observables, including $d=3$. | Keep Appendix **app:conventions**; rerun source/polar, first-family, and second-family verifiers after any formula edit. Never mix conventions termwise. |
| High | The second-family phases are algebraically dense and easy to damage during copyediting. | The coefficient norm, geometric sum, parity exponent, and independent exact $d=4$ SOS currently agree. | Freeze **eq:lambda**, **eq:second-A**, and **eq:Fourier-compression**; rerun the $d\leq100$ normalization tests and both second-family replays after edits. |
| Medium | The arbitrary-$qc$ polar argument may be summarized too loosely. | The revised proof displays $\mathcal B\subseteq\mathcal A'$, the strong limits placing the support and $V$ in $\mathcal A''$, and the canonical support identities. | Preserve the bicommutant and strong-limit paragraphs. Do not replace them by “the polar operator is in Alice's algebra” or present $qc$ as numerically validated. |
| Medium | Model-indexed guessing notation could be collapsed back into one ambiguous quantity. | The framework defines $\mathfrak S_q,\mathfrak S_{qa},\mathfrak S_{qc}$, and **eq:gval-model** states a separate supremum for each. | Keep the model index in manuscript, website, and summary. State only the common lower bound supplied by the finite witness; do not claim the suprema are equal. |
| Medium | The guessing lower bound or $d=4$ entropy could be mistaken for an exact optimization. | The text calls the bound a lower bound on $G_{\mathrm{val}}^\mu$, says the swap need not be worst, and calls $5-\log_2 3$ an upper bound on value-only worst-case entropy. | Keep those qualifications adjacent to every numerical statement. |
| Medium | Behavior-level nonuniqueness could be promoted into an overbroad self-testing claim. | Uniform and nonuniform target tables are inequivalent under output relabeling, but no complete strategy-equivalence formalism is used. | Use “the scalar maximum does not determine the behavior, even modulo output relabelings”; avoid a full realization-level non-self-test claim unless separately formalized. |
| Medium | Binary value scope and privacy scope could be conflated. | The SOS proves $q=qa=qc=3\sqrt3$; the Eve-decoupling proof treats attaining finite-dimensional tensor-product strategies. | Retain both clauses in Theorem **thm:binary-benchmark**; do not infer $qa/qc$ privacy from the value statement. |
| Medium | The private-MUB criterion could be marketed as an achieved low-setting construction. | The theorem expressly calls its hypotheses sufficient and says it neither proves necessity nor constructs a Bell functional. Three deleted-hypothesis hostile controls fail as intended. | Keep the lemma in its design-criterion role and the $2\times3$, $d\geq3$ entry open. Require an independent score or SOS enforcement theorem before changing that status. |
| Medium | One-input minimality could again be worded as a claim about intrinsic randomness. | The proposition says “DI-force against all compatible realizations,” and the binary corollary specifies the finite-dimensional projective certification task. | Preserve “certify/force,” “compatible realizations,” and “total test-input alphabets” in summaries. |
| Medium | Endpoint robustness could again acquire an exact-deficit interpretation. | The corollary quantifies every strategy whose deficit is at most $\varepsilon$. | Preserve that tolerance convention verbatim. |
| Medium | Priority may have shifted in a later source version or contemporaneous preprint. | A dated primary-source audit checks the source $d\sqrt2$ bound, NPA through $d=6$, binary prior art, and recent related work. | Refresh the search log at release freeze and revise novelty wording immediately if a conflict appears. |
| Medium | Verification implementations are not fully independent. | The $d=4$ certificate has two routes; new rigidity, benchmark, and MUB verifiers use independent finite calculations; some historical unit tests still call shared routines. | Preserve independent $d=4$ and exact-$\mathbb Q(\sqrt3)$ paths. Never present finite replay as proof of an analytic theorem. |
| Release | The manuscript and package are still changing after the earlier released baseline. | This audit is keyed to the revised 2026-08-09 **main.tex**; new theorem labels and verifiers have been added. | After content freeze, rerun **reproduce.sh**, rebuild and inspect both PDFs, regenerate hashes and reports, and compare all seventeen named environments to **CLAIMS_LEDGER.md**. |
| Release | Website, redirects, historical URLs, hashes, and metadata may lag the revision. | These are outside the analytic theorem audit. | Rebuild the canonical assets and run local and live link, metadata, and hash checks after the revised PDF is copied to the site. |
| Release | No external specialist has reviewed the revision. | All reviews described here are internal AI-assisted adversarial reconstructions. | Continue to mark the paper unrefereed; present focused questions without implying endorsement or collaboration. |

## Closed during the 2026-08-09 restoration audit

- The formerly omitted equal-supported-multiplicity theorem is restored with
  an explicit finite-dimensional tensor-product first-augmented scope and an
  independently replayed reflection-rank lemma.
- The private-MUB lemma is restored as a sufficient operator criterion, with
  exact conditional-state and Fourier normalizations and no existence claim.
- The full binary $3\sqrt3$ benchmark is restored; its $qc$ value and finite-
  dimensional privacy scopes are separated, and its prior-art origin is
  explicit.
- The one-input conclusion is now stated as DI certification or forcing
  against compatible realizations, not as an intrinsic-randomness claim.
- The value-conditioned guessing quantity is model-indexed, and the common
  statement is only a finite-witness lower bound.
- The polar proof no longer hides the von Neumann closure step: support and
  canonical partial isometry are placed in $\mathcal A''$ by strong limits.
- The source's $d\sqrt2$ bound, NPA range through $d=6$, exact radical table,
  source-observable identification, and coefficient normalization are
  restored and independently checked.
- The endpoint ambiguity remains closed by the “deficit at most
  $\varepsilon$” quantifier.
