# Credited resolution of the standard physical class

Let (M,g) be a smooth, complete, one-ended asymptotically flat Riemannian3-manifold of orderτ>1/2, with two-derivative decay and integrable scalar curvature as in Jauregui Definition9. Assume scalar curvature nonnegative everywhere and compact boundary empty or minimal. The full paper's conjecture follows from prior theorems:

    m_ADM ≤ m_CV ≤ m_iso = m_ADM.

The first inequality is Jauregui Theorem5. The middle is Benatti–Fogagnolo–Mazzieri, SIGMA19(2023)091, Theorem5.6 atp=2. The last is the established Huisken isoperimetric-mass theorem, proved by Jauregui–Lee and independently by Chodosh–Eichmair–Shi–Yu; Jauregui Theorem2 states its exact boundary scope. The sharper C¹ framework is also covered by Benatti–Fogagnolo–Mazzieri, CPAM78(2025), Theorem1.4. Only the original two-derivative class is needed here.

## Topology and normalization

Published SIGMA Theorem1.3 explicitly assumes H₂(M,∂M;Z)=0. We do not drop that assumption. Instead, its Theorem5.6 independently assumes only C⁰ asymptotic flatness and compact boundary; combining this upper bound with the other two prior results gives the chain without a topology restriction.

SIGMA Definition1.1 uses c_p=(4π)^−1((p−1)/(3−p))^(p−1) inf∫|Dv|^p. Atp=2 it is exactly Jauregui capacity via v=1−φ. Its mass becomes [vol(Ω)−(4π/3)cap(Ω)^3]/[4πcap(Ω)^2]. Jauregui Lemma10 and SIGMA Proposition5.2 identify the exhaustion supremum with the radius-minus-capacity formula.

Smooth compact supersets suffice: outer regularity of Dirichlet capacity gives smooth bounded supersets with capacity arbitrarily close from above, while volume cannot decrease. Choosing the capacity error tending to0 loses at most that error in the deficit. Such supersets exhaust. For nestedness, first select a sufficiently late original exhaustion member containing the previous smooth set, then approximate it. Conversely these are allowable compact competitors. Capacities diverge along exhaustions by monotonicity and the coordinate-ball comparison.

## Proof-chain qualification

SIGMA's upper comparison applies the asymptotic isoperimetric inequality to capacitary superlevel sets, Hölder/coarea and spherical symmetrization. At(5.9)–(5.11), multiplying an upper integral estimate needs a nonnegative isoperimetric mass. Here m_iso=m_ADM≥0 by the positive mass theorem; taking m>m_iso handles zero. Thus the needed sign holds in the claimed physical class.

Benatti arXiv2511.11155v2 §3 explicitly identifies the sign issue and proves a corrected broader comparison using inclusion-large sets and separate signs. It also cites Jauregui–Lee–Unger2024 for AF nonnegativity. We do not use its all-p equivalence theorem to erase its additional assumptions. This is a qualified prior-proof-chain verification, not a new analytic theorem.

Primary references:
- Jauregui, equations(3)–(5), Theorems2,5,6, Lemma10: https://arxiv.org/pdf/2002.08941
- Benatti–Fogagnolo–Mazzieri, SIGMA19(2023)091, Definition1.1, Theorems1.3,5.6, pp20–21: https://sigma-journal.com/2023/091/ ; final version https://arxiv.org/pdf/2305.01453v2
- Jauregui–Lee, Crelle756(2019)227–257, Theorem3: https://arxiv.org/pdf/1602.00732
- Benatti–Fogagnolo–Mazzieri, CPAM78(2025)1042–1085, Theorem1.4: https://doi.org/10.1002/cpa.22239
- Benatti, §3: https://arxiv.org/pdf/2511.11155v2
- Jauregui–Lee–Unger: https://arxiv.org/pdf/2408.08871

The literal all-AF statement is treated separately in TURN_1.md; its example does not contradict the credited physical-class resolution.
