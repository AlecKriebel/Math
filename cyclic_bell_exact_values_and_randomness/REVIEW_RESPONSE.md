# Response to the author-ready dominating-merge review

Date: 9 August 2026

The review was treated as a set of hypotheses. Each requested change was
checked against the three preserved TeX sources, the current canonical proof,
and fresh deterministic replays. The pre-revision release is frozen in
`audit/PRE_REVISION_BASELINE.md`; the complete source-result inventory is
`audit/THEOREM_CROSSWALK.md`.

## Item-by-item disposition

| Review item | Verdict | Applied revision and qualification |
|---|---|---|
| 1. Restore equal supported multiplicities | **Accepted** | Restored as `thm:support-rigidity`, with the reflection-rank lemma and full support proof in Appendix `app:rigidity-proof`. The relative unitary is $U=A_0^\dagger A_1$; the polar operators are $V_y$. Scope is attained finite-dimensional tensor-product exact maximizers of the first augmented family only, not $qa$, $qc$, the unaugmented family, or the second family. |
| 2. Harden the commuting polar argument | **Accepted** | Added $\mathcal A''$, the two strong limits for the support and canonical partial isometry, $\mathcal B\subseteq\mathcal A'$, and commutation with $\mathcal A''$. The $qc$ theorem survives. No tensor factor, trace, or finite-dimensional step remains in the upper bound. |
| 3. Restore private-MUB composition | **Accepted narrowly** | Restored as a sufficient finite-dimensional operator criterion, with exact subnormalized Eve states, $1/d^2$ Fourier inversion, and a test-operator proof. It is not necessary and does not construct a low-setting Bell score. |
| 4. Restore the binary benchmark | **Accepted and credited as prior art** | Restored the exact $3\sqrt3$ SOS, all three operator-valued Fourier cancellations, two private bits, and componentwise $(2,2)$ setting minimality for DI forcing against all compatible realizations. All auxiliary anticommutation identities are explicitly on-state. |
| 5. Identify source observables | **Accepted** | Added the source coefficient expansion, its Fourier selection rule, the two source sums, the polar-equality identification, transpose/conjugation convention, and exact $d=3$ formula. |
| 6. Derive coefficient normalization | **Accepted** | Derived the general cosecant-square identity by differentiating the cotangent sum and specialized at $x=-\pi/(2d)$ to prove $\sum_\ell|\lambda_\ell|^2=1$. |
| 7. Correct first-family prior art | **Accepted** | The introduction and contribution table now credit the proved source bound $d\sqrt2$, the all-dimensional lower strategy, and NPA agreement through $d=6$. The review’s phrase “asymptotically close” was narrowed: the ratio tends to $\pi/(2\sqrt2)=1.1107207\ldots$, so the bound is same-order but not asymptotically tight. |
| 8. Restore the $d=2,\ldots,6$ table | **Accepted** | Restored exact radicals, decimals, and the tight source NPA level. Every radical was replayed algebraically. |
| 9. State the refuted source claim | **Accepted with normalization explanation** | The paper now identifies Conjecture 2 by number and says plainly that its intended scalar-value implication is refuted for $d\ge4$ after reconciling the isolated printed factor-$d$ discrepancy with the operator definition and source qutrit value. The canonical full-behavior computation is not challenged. |
| 10. Add a non-self-testing consequence | **Accepted only at behavior level** | Added a corollary that the maximal scalar value does not determine the behavior even modulo local output relabelings. A uniform target table cannot be relabeled into a nonuniform one. No complete strategy-level classification under every isometry, ancilla, and transposition convention is claimed. |
| 11. Define the guessing model | **Accepted** | Defined finite tensor $q$, extended-correlation closure $qa$, and tripartite commuting $qc$ adversarial models, then introduced $G_{\mathrm{val}}^\mu(d;\mathcal B)$. The finite witness supplies a lower bound in every containing model; it does not determine the supremum. |
| 12. Convert the four-outcome witness to bits | **Accepted** | Added $-\log_2(3/32)=5-\log_2 3=3.415037\ldots<4$ and identified it as an upper bound on value-only worst-case min-entropy, not the exact optimized value. |
| 13. Keep the all-dimensional result central | **Accepted** | The abstract, contribution list, and section order continue to lead with the all-dimensional exact value, equality results, permutation orbit, and two-family biased maximizers. The $d=4$ table remains a worked certificate. |
| 14. Avoid a complete equality classification | **Accepted** | The manuscript distinguishes scalar phases, necessary finite-dimensional support rigidity, and a sufficient permutation orbit. The sharper open problem asks whether those pieces, direct sums, and ancillary systems exhaust finite-dimensional maximizers. |
| Low-setting reorganization | **Accepted** | The main low-setting section now contains the standard one-input baseline, full binary benchmark, positive private-MUB criterion, and an updated status table. The standard-qudit and fixed-MUB obstruction algebra remains in an appendix. |
| Abstract and introduction rewrite | **Accepted** | Reordered both around exact value, $qc$ scope, support rigidity, permutation orbit, two-family bias, and the precise scalar-value randomness consequence. No peripheral low-setting claim leads or closes the abstract. |
| Preserve earlier repairs | **Accepted** | Kernel sensitivity, vector/operator distinction, source adjoint conventions, second-family SOS attribution, deficit-at-most quantifier, trivial-Eve lower-bound scope, and one-input demotion are retained. |
| 15. NPA bibliography | **Accepted** | The formerly uncited NPA-2007 item is now cited where the source numerical hierarchy evidence is discussed. |
| 16. Coccia–Padovan–Vallone names | **Audited; current canonical form retained** | The official record lists Lorenzo Coccia, Matteo Padovan, and Giuseppe Vallone, so `L. Coccia, M. Padovan, G. Vallone` is correct. The preserved historical third manuscript’s `E./S.` initials are not copied and are not altered in the immutable source package. |
| 17. Contact and disclosure statements | **Accepted** | Removed the categorical manuscript and merge-report claim that no originating author had ever been contacted, because repository history records earlier author contact about the companion result. The disclosure now makes only the verifiable claims that no external review, collaboration, or endorsement is asserted and describes AI assistance and author responsibility. No contact was initiated during this revision. |
| 18. Cross-references and notation | **Accepted** | Rebuilt theorem dependencies, model-indexed guessing notation, source coefficients, Fourier labels, and scope references. Clean build, duplicate-label, bibliography, and page-layout checks are part of `reproduce.sh`. |

## Fresh adversarial replays added

- `verification/verify_rigidity.py`: equality phases and wraparound through
  $d=64$, 840 exact-rational rank tests, and 16,128 hostile dimension counts.
- `verification/verify_exact_benchmarks.py`: exact radicals, source decimals,
  $d=4$ entropy, cosecant-square normalization through $d=100$, and 77
  independently reconstructed source/polar Bob observables through $d=12$.
- `verification/verify_private_mub_binary.py`: exact
  $\mathbb Q(\sqrt3)$ SOS, binary strategy/Fourier data, 1,980 MUB checks
  through $d=12$, and three dropped-hypothesis hostile controls.

These are regression evidence. The readable proofs remain load-bearing.

## Claims deliberately not made

- No complete maximizing-face classification or exact worst-case guessing
  probability.
- No support-rigidity extension to $qa$, $qc$, approximate maxima, the
  unaugmented first family, or the second family.
- No nonuniform permutation witness for $d=2,3$.
- No general $2\times3$ impossibility or all-dimensional minimum-setting law.
- No strategy-level self-test classification beyond the proved behavior-level
  inequivalence.
- No novelty claim for the binary benchmark or private-MUB design lemma.
- No external review, collaboration, endorsement, contact campaign, DOI,
  release, or submission claim.

## Overall verdict

The review identified genuine omissions and one underexplained $qc$ step. Its
main mathematical recommendations were sound after the scope repairs above.
The revised paper now contains every proved substantive theorem from the
three predecessors while retaining the unified exact-value-to-randomness
narrative.
