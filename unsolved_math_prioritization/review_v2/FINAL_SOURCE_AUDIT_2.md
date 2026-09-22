# Independent final source audit: shard 2

Checkpoint: 2026-09-22 05:20 UTC. Bounded source-audit goal: 100% complete; neither candidate is certified novel or solved. All 2,366 assigned individual desk reviews are complete, and ledger writes have stopped. No exhaustive search or external communication was used.

## 30003169 — kernel level-set second-order bias

**Recommendation: hold until the exact functional I2 is recovered.** The [original OWR 2016 report, printed p.1833](https://ems.press/content/serial-article-files/46636?nt=1) genuinely asks for an h^-2 I2 limit without nh^(d+4)→0. However, it only names variance-related and bias-related pieces; it does not define their integrals. It also discusses several loss weights g, which must be fixed before testing the claim. The [Cadre preprint](https://arxiv.org/pdf/math/0501221) did not expose a matching named I1/I2 definition in this brief inspection. Its proof's two crossing-direction terms must not simply be identified with variance and bias.

[Qiao, Theorem 3.2](https://arxiv.org/pdf/1707.09697) gives, for ordinary measure loss and second-order kernels, a leading boundary integral of E|s_n Z+h²b(x)|/|∇f(x)|, with remainder o(s_n+h²). Here s_n²=c||K||²/(nh^d). Its bandwidth assumptions allow s_n/h² to approach a positive constant; this is already closely relevant literature, not an untouched expansion problem.

**Conditional mechanism, not a solution:** if the actual I2 is risk minus the zero-bias leading risk, accurate to o(h²), then along s_n/h²→r∈(0,∞), its scaled limit would be the boundary integral of

    [E|rZ+b(x)| − r E|Z|] / |∇f(x)|.

For b≠0 this expression changes strictly with r: its r derivative is 2φ(b/r)−2φ(0)<0. Two bandwidth sequences h=a n^(-1/(d+4)) give different finite r and keep the published remainder o(h²). Thus a bandwidth-independent B is doubtful under this natural interpretation. This reasoning deliberately avoids the noise-dominant r→∞ regime, where the published remainder alone is insufficient after division by h².

**Exact gap:** identify I2 and its error terms, specify g and the kernel/density hypotheses, and compare that definition with Qiao. A deterministic displaced-level-set bias term could behave differently. A desk note must not present the conditional mechanism as a verified counterexample to the stated historical question.

## 30001163 — saturation of eigenvalue mean gap bound

**Recommendation: retain as a plausible short proof candidate, with novelty and formulation checks still required.** The [original OWR 2009 report, printed pp.413–415](https://ems.press/content/serial-article-files/46205) concerns bounded Euclidean domains and Dirichlet eigenvalues, with n≥2. It genuinely asks about saturation. Its displayed formula prints M1²−M2 despite defining Mp with a p-th root; the dimensionally consistent correction is D=M1²−M2². Record that repair explicitly. Harmonic oscillator or closed-manifold equality examples do not answer this bounded Dirichlet question.

[Harrell–Stubbe, Corollary 2.3, equation (2.9)](https://arxiv.org/pdf/0808.1133) supplies an exact commutator trace identity. For H=−Δ_D and coordinate multiplication, the associated Yang polynomial is

    Q_J(z)=Σ_{j≤J}(z−E_j)(z−(1+4/n)E_j)
          =J[(z−M1)²−D] ≤ 0,  E_J≤z≤E_(J+1).

**Independent proof route:** equality D=(E_(J+1)−E_J)²/4 forces Q_J(E_(J+1))=0. When E_(J+1)>E1, every spectral-tail summand associated with the first eigenfunction has one sign. Vanishing therefore forces each x_a u1 to have finite spectral support, at energies ≤E_(J+1). This is finite support of these particular functions; claiming an invariant finite-dimensional space would be stronger and unjustified.

Then (H−E1)(x_a u1)=−2∂_a u1 puts every first derivative in H0¹. Extending u1 by zero should consequently give a compactly supported H² function satisfying −Δu1=E1u1 on all of R^n, impossible by Fourier transform. This avoids relying on a smooth-boundary Hopf lemma, but the operator-domain and zero-extension steps deserve explicit independent verification. If E_(J+1)=E1, all first J energies equal E1 and D=4E1²/n²>0, already excluding saturation. Repeated higher eigenvalues remain covered by the first-eigenfunction argument.

**Exact gap:** write and adversarially check these domain arguments, including disconnected or irregular bounded open sets; confirm the intended corrected formula; check whether strictness of Yang's first inequality or this particular gap bound has already been published. The quick literature search did not establish novelty. This is substantially more concrete than the initial invariant-space desk heuristic, but it is not a publication-ready result.
