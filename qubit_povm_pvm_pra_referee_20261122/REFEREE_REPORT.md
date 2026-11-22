# Independent referee report on *Minimum Bell-Setting Complexity for Qubit POVM–PVM Separation*

**Date.** 22 November 2026. **Version reviewed.** The PRA revision in pull request 1451, commit `6af1a90588125ad69bb7718f2d259984adc63f1b`, built to a 33-page PDF. **Reviewer.** Claude Fable 5.2 (Anthropic), working in Claude Code with four independent sub-reviews. No person outside the project was contacted.

**Recommendation.** Merge the revision with the changes listed below, then submit. I found no error in any theorem, proposition or numerical claim. The changes repair two derivations that the prose asserted without proof, correct one inaccurate description of prior work, and state the open questions that the main theorem answers.

Acceptance cannot be guaranteed by any pre-submission review. The remaining risks are listed at the end.

## What was checked, and how

| Check | Method | Result |
| --- | --- | --- |
| Every proof in the main text and appendices | Line-by-line reading by me, and a second independent adversarial reading that did not see my notes or the earlier review | No false statement. Two missing derivations and a list of smaller imprecisions, all fixed |
| Lean statements against the paper's claims | Read-only audit of the definitions and every declaration named in the verification appendix, a scan for `sorry`, added axioms, `native_decide` and similar constructs, and a comparison with the verification appendix | Statements match the paper. No vacuity or weakening. Three wording errors in the appendix, fixed |
| Sum-of-squares certificate | The 12 × 12 matrix parsed from `appendices.tex`; exact leading minors by two methods; the operator identity reduced in a free algebra with only involutivity and cross-party commutation; 1200 random involution tuples in local dimensions 2, 3, 4 | Identity exact. All twelve minors positive. Printed pivot floors reproduced |
| Both POVM strategies and all scalar comparisons | Exact recomputation from the Born rule | 20√2 + 16/25 and (16 + 8√7813)/25 confirmed. Gap above 289/10 is 0.0251763 |
| Projective bound 289/10 | About 260,000 qubit-PVM optimizations over all 1,944 labelled rank patterns and by direct optimization | Largest value found 28.887740069934, below 28.9 |
| Two-setting equality | 7,845 Bell functionals in eight two-setting output architectures, about 619,000 POVM see-saw runs, compared with the two-angle projective bound | Largest POVM minus PVM value +8.5 × 10⁻¹⁴. No counterexample |
| Positive control for the search | The same POVM search on the paper's three-setting functional | Exceeds 28.9 in about 64% of restarts and converges to (16 + 8√7813)/25 |
| Bibliography | Every entry checked against Crossref or arXiv; cited claims checked against the sources' text | No fabricated or misattributed entry. One inaccurate description and several omissions, fixed |
| Prior art | Search for earlier proofs, conjectures or counterexamples at two settings | No earlier proof and no claimed two-setting qubit advantage |
| Build | Tectonic 0.16.9, warning-free; exact artifact suite and the earlier review's checker rerun | Pass |

The numerical searches are evidence and not proof. Random functionals rarely reach the binary-against-ternary case that the proof treats last, so the informative tests are the 4,367 functionals with a genuine quantum advantage and the structured families built around trine, tetrahedral and discrimination terms.

## Findings and changes

### Positioning against the literature

1. Navascués, Feix, Araújo and Vértesi (Phys. Rev. A 92, 042117) state the conjecture that general measurements do not improve the projective qubit bound of the two-setting CGLMP inequality, and report that their hierarchy could not confirm it. The manuscript cited this paper only for context. The introduction now says that the main theorem proves this for every two-setting functional.
2. The manuscript described Cerf and Ollivier (arXiv:2603.26875) as a study of dichotomic strategies. Their paper treats two settings with any number of outcomes and parties, and proposes two-setting functionals as a route to a POVM advantage at fixed local dimension. Zhu et al. (arXiv:2608.01317v2) state that their three-setting construction does not settle that program. The introduction and related-work paragraph now say this, and say that the equality excludes such a functional for two parties and qubits.
3. Added references: Collins et al. for the CGLMP inequality; Cleve et al. and Liang–Doherty for the binary-outcome fact; Donohue–Wolfe for nonconvexity; Ramanathan for the one-binary-party quantum set; Tavakoli et al. and Steinberg et al. for prepare-and-measure certification, whose minimal scheme also uses three against two; Hirsch–Huber for device-independent Schmidt-number certification; Cai et al. for the qutrit analogue. Six entries that were in the bibliography but never cited are now cited where they belong. Issue numbers and arXiv identifiers were added to three entries.

### Proofs

4. **Stationarity.** Section 7 began from a stationary point without showing that the maximizer is one, and the final proof gave block-wise optimality as the reason. The section now derives the Lagrange identity from local physical completeness and the independence of the six constraint differentials, and reads off both its probability-block and metric components.
5. **Second derivative along feasible curves.** The Hessian was computed along straight lines, while feasible curves are curved. The text now differentiates the constraints twice and uses the Lagrange identity on the acceleration to obtain the second derivative 2q(W). The sub-review confirmed the identity and its sign numerically on curved feasible curves.
6. The roadmap and Section 8 described the manifold and inertia statements as optional explanations. In the written proof they carry the rank-at-least-two case. The text now says the written proof is self-contained and that the Lean proof reaches the same contradiction by a different route.
7. Smaller repairs: positivity of the coefficients in the rank-zero case is now derived from positive marginals; the relabeling that gives P = g is made explicit; the one-dimensional span and the projective second measurement are handled in the right order in the residual reduction; pairwise distinctness of the five rays is justified; the circuit lemma defines its terms; the extreme-point lemma separates a point different from p; the weighted second form states its hypotheses; the one-parameter family in Appendix B is defined.

### Verification appendix

8. The rank cases are combined in `Bell/ResidualClosure.lean`, not `Bell/Assembly.lean`. The row for `main_claims_with_strengthening` now lists what that declaration contains. The two corollaries of Section 3 are now stated to be unformalized.

### Presentation

9. Figure 1 no longer splits the Main Theorem. All three figures are cited in the text. Cross-references are capitalized. The Bell operator has one symbol in the main text and appendix, the CHSH operator replaces an undefined symbol, the score operators no longer reuse G and H, and the discrimination score is defined where it is first used. The abstract and corollary specify finite-dimensional realizations and arbitrary POVMs.
10. A sentence now records that the sum-of-squares bound holds in every dimension for two-outcome projective settings, and that the qubit hypothesis enters only through the support of the ternary measurement.
11. The AI Use Disclosure names this review. The cover letter was rewritten for the current manuscript; the previous letter predated the Lean formalization and the corollaries.

## Remaining risks

- **AI disclosure.** The search summaries of APS's June 2026 policy say authors must name each AI tool and version and say how it assisted. The disclosure names the two review tools but says the records for the earlier research stages do not identify model versions. The author should replace that sentence with the tools actually used. I could not read the APS policy pages directly, because they are behind an automated-access check.
- **Software citation.** The Data Availability statement cites a GitHub commit. APS asks for data and code in a repository, and a DOI-bearing archive is the usual form. A Zenodo release of the verification software would give the statement a persistent identifier.
- **Format.** The manuscript uses the article class. APS accepts this for initial submission and prefers REVTeX.
- **Scope of formal verification.** The corollaries and several auxiliary statements are proved only in prose. The appendix says so.
- **Refereeing depth.** This review did not rebuild the Lean project locally. It relied on the passing continuous-integration build of the pull request and on a reading of the statements.

## Files

- `numerics/` contains the falsification scripts and `numerics/outputs/` their summaries. `claim3_sos.py <appendices.tex> <out.json>` and `claim2_exact.py <out.json>` rerun the exact checks with NumPy and SymPy.
- `proof_checks/` contains the adversarial reader's numerical checks of the Lorentz model, the feasible-curve second derivative, and the one-binary-party construction.

In the first run of the two-setting search, 7 of 7,845 functionals returned a two-angle value below the general projective see-saw. The cause was a truncated shortlist in the search heuristic, not the formula: an uncapped search reproduces the see-saw value to 10⁻¹⁵, and 498 fresh functionals agree to 2 × 10⁻¹⁴. `numerics/outputs/diag_analyze_output.txt` records the diagnosis.
