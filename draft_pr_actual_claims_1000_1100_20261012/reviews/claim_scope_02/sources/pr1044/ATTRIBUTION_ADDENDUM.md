# Prior-work attribution: ordinary logarithmic GE tensorization

Problem 30004587 / OWR-4990370-005. Checked 2026-10-09.

## Classification

**Verified consequence of prior work, with an explicit direct certificate. No novelty or priority claim.**

The accepted proof remains mathematically valid. The identity-amplification obstruction is already explicit in Brannan–Gao–Junge (2020 preprint; 2022 publication). Combining that obstruction with the qubit factor estimate of Münch–Wirth–Zhang (2024) gives the same-constant ordinary logarithmic GE tensorization failure. The present rational positive-time calculation provides a self-contained certificate of this consequence.

## Exact antecedent

Michael Brannan, Li Gao, and Marius Junge, *Complete logarithmic Sobolev inequalities via Ricci curvature bounded below*, Advances in Mathematics **394** (2022), 108129, §4.4, p. 51, immediately before Proposition 4.21, explicitly gives

GE((I−τ₂)⊗id_M₂) ≤ MLSI((I−τ₂)⊗id_M₂) < 1.

This statement is already present in arXiv:2007.06138v2 (27 August 2020), pp. 46–47, with the inequality on p. 47. Their example uses Bell-projector weights 5/8, 1/8, 1/8, 1/8 in ordinary-trace normalization. Proposition 4.21 itself states the MLSI/CLSI separation; the preceding paragraph also explicitly states the GE obstruction. Therefore the amplification failure must be attributed to these authors, rather than described as a new discovery here.

Their Definition 3.11 uses the same exp(−2λt) convention; Proposition 3.14 identifies the logarithmic weighted norm, and Proposition 3.15 with Proposition 3.3 gives GE ⇒ MLSI, including the nonergodic setting.

Sources: [published DOI](https://doi.org/10.1016/j.aim.2021.108129), [published PDF](https://par.nsf.gov/servlets/purl/10355667), [2020 manuscript](https://arxiv.org/abs/2007.06138v2).

## Factor estimate and the resulting inference

Florentin Münch, Melchior Wirth, and Haonan Zhang, *Intertwining Curvature Bounds for Graphs and Quantum Markov Semigroups*, arXiv:2401.05179v1, Theorem 3.23 and Remark 3.24, pp. 26–28, prove GE_Λ(1/2+1/n,∞) for the normalized depolarizing generator A−τ_n(A)I. For symmetric means, Remark 3.24 permits arbitrary complex observables. Thus the logarithmic qubit estimate is GE(1,∞).

Together with the preceding amplification obstruction and the zero gradient of the identity semigroup, this proves failure of ordinary same-K tensorization. **This combination is an inference from the two sources, not a claim that either paper explicitly announces that combined conclusion.** No separate later explicit announcement was established in this bounded check.

The 2024 paper's separation of intertwining curvature from entropic curvature is a different statement. Its Example 3.15 gives the optimal intertwining constant 1/2+1/(n+1); that is not an optimal complete logarithmic-GE constant.

Source: [2024 manuscript](https://arxiv.org/abs/2401.05179v1).

## Convention checks and direct-certificate contribution

The following observations are independent algebraic checks of compatibility:

- A trace-one matrix r on M₄ corresponds to ρ=4r for τ₄=Tr/4. Homogeneity of the logarithmic mean cancels the factor four from the trace, so this change does not alter the GE constant.
- Centering the observable is immaterial: δE(a)=0, hence a and a−E(a) have the same gradients before and after the semigroup.
- The existing certificate uses normalized eigenvalues 2,2/3,2/3,2/3, rather than the earlier example's 5/2,1/2,1/2,1/2. Its exact time log 2 and strict rational comparison 81>75 are checked directly in the full tensor calculus.
- The direct Bell-algebra weighted-form calculation remains useful; the literature obstruction does not replace that calculation in the accepted self-contained proof.

These checks do not establish that the particular choice of rational parameters or presentation has never appeared elsewhere.

## Complete estimates remain distinct

Melchior Wirth and Haonan Zhang, *Complete gradient estimates of quantum Markov semigroups*, arXiv:2007.13506v2, Definition 2.5 and Theorem 4.1, define CGE by all identity amplifications and prove its tensor stability. The introduction says ordinary GE tensorization was unknown at the time. The inspected article does not supply the Bell counterexample. The present consequence leaves its complete-GE theorem unaffected.

Sources: [manuscript](https://arxiv.org/abs/2007.13506v2), [published article](https://doi.org/10.1007/s00220-021-04199-4).

## Classical complete-graph connection: lower bounds are not optima

All constants here are for Lf=f−average(f).

- Erbar–Maas, *Ricci curvature of finite Markov chains via convexity of the entropy*, Example 5.1, gives the lower bound 1/2+1/(2n). [Author PDF](https://www.janmaas.org/papers/Ricci.pdf)
- Mielke, *Geodesic convexity of the relative entropy in reversible Markov chains*, Example 3.4, gives (n+2)/2 for transition rates one. Dividing the generator by n gives 1/2+1/n. The same passage expressly expects nonoptimality for n≥3 and only concludes equality in the two-state case. [Accepted manuscript, p. 11](https://www.wias-berlin.de/people/mielke/preprints/Mielke_GCM120613_acc.pdf)
- Münch–Wirth–Zhang, Example 2.13, attributes that entropic lower bound to Mielke. Its optimality claim is for Bakry–Émery and intertwining curvature, not for logarithmic entropic curvature.

Consequently, 3/4 is an established lower bound for the normalized K₄ entropic curvature, not an established exact value from these citations. The accepted witness independently gives the upper bound (1+1/log 3)/2<1 by differentiating its GE inequality. It does not determine the optimum.

## Bounded-search limits

The check covered the above primary texts, Wirth–Zhang's curvature-dimension paper (arXiv:2105.08303v2 and the published §4.3/§6.3), and targeted primary-manuscript screening through 9 October 2026. Two 2026 hits, arXiv:2606.17729v3 and arXiv:2609.20753v2, concern hypercontractivity/entropy tensorization; no ordinary logarithmic-GE counterexample was identified in the inspected passages. Their different tensorization questions are not evidence for or against this GE statement.

Search scope and retrieval/inspection metadata are recorded separately. This is not an exhaustive bibliography, proof of absence, or novelty determination. Both the original certificate and the prior obstruction use a nonergodic identity factor; no assertion about a requirement that both factors be ergodic is made.
