# Independent analytic review — Zenodo 23422055

**Verdict: PASS for the published Theorem 1 and its stated counterexample consequence.** No substantive mathematical defect or unresolved load-bearing gap was identified. This is AI mathematical review, not external human peer review, formal verification, journal acceptance, or certification of novelty.

Work reviewed: Alec Kriebel, *Three anti-invariant classes on a nonintegrable four-manifold*, October 16, 2026, version 1.0. All five published pages, the full TeX source, the original author construction, the three mathematical checkers used by the portable verifier, and the verifier were read. Historical reviewer reports and current sibling opinions were not read.

## Immutable bindings

- Published PDF: SHA256 `14063ce9fef470a6a3875dc429a1c3d34372d60cbd73eb7e22e77b46b1639f60`.
- Published verification ZIP: SHA256 `ae7d51ded2f03cd307ec394728a94f3e2e6e568903905713da8bfdf0007a24d6`.
- Fresh acquisition receipt: SHA256 `fefedf8ff304b01c45a07f95feb667e21239f930964e724f4dd86b25f67934f6`.

`source_bindings.json` also records metadata and byte counts. The PDF inside the archive is byte-identical to the separately published PDF. The verdict applies to these bytes, not a later editable file.

## Exact claim and scope

On the specific closed connected smooth four-manifold M=Σ₂×E, with Σ₂ the smooth compact completion of y²=z⁶−1 and E=C/(Z+iZ), there is a jointly smooth family of almost-complex structures Jε for sufficiently small |ε|. They equal the product complex structure outside one fixed coordinate ball and converge to it in C∞. Three fixed linearly independent real de Rham classes have closed Jε-anti-invariant representatives. Every nonzero sufficiently small ε gives a nonintegrable structure. Consequently h⁻(Jε)≥3, contradicting the unrestricted compact-four-manifold integrability conjecture as actually stated in DLZ Conjecture 2.5.

This does not compute the exact dimension for ε≠0, establish generic nonvanishing, impose a common compatible metric or fixed symplectic form, give a spatially real-analytic construction, or assert any priority claim. It does not concern only three pointwise independent forms: those would be impossible in the real anti-invariant plane. The independence here is in real cohomology.

## Reconstructed proof

**1. Compact starting manifold and holomorphic forms.** The sextic has no repeated root, since it is relatively prime to 6z⁵. The double cover of CP¹ has six simple finite branch points and two unramified points over infinity. Its Euler characteristic is 2·2−6=−2, hence genus two. The cover is connected because z⁶−1 is not a square in C(z). The affine chart is smooth: simultaneous vanishing of 2y and 6z⁵ cannot occur on y²=z⁶−1.

At a finite branch point z≠0, y is a coordinate and dz/y=dy/(3z⁵). At infinity s=1/z and q=y/z³ satisfy q²=1−s⁶ with q(0)=±1, giving η₀=−s ds/q and η₁=−ds/q. Thus both forms are global holomorphic differentials. They are independent because their ratio is the nonconstant function z wherever η₀ is nonzero. The global form dw on E is translation invariant. Therefore Ωj=ηj∧dw are closed holomorphic two-forms on the compact product. Their real/imaginary parts are anti-invariant for the product complex structure.

**2. Cohomological independence, not just form independence.** A real linear combination F=aα+bβ+cγ is the real part of H=(a−ib)Ω₀+cΩ₁. Since the complex dimension is two, H²=0, and F²=(1/2)H∧conjugate(H) is nonnegative in the complex orientation. If H is not identically zero, it is nonzero on an open set, so the integral is strictly positive. If F is exact, F² is exact because F is closed, and compactness without boundary makes its integral zero. Thus H vanishes identically. On the selected chart H=(a−ib+cz)Ω₀, so a=b=c=0. This proof supplies genuine independent de Rham classes and does not depend on an imported Hodge-theoretic classification.

**3. Simultaneous local coordinates and full-cutoff identities.** At z=0,y=i and a local elliptic lift w=0, the coordinate change ζ=z, ξ=w/y(z) has Jacobian determinant 1/y(z)≠0. Wedging its derivatives gives Ω₀=dζ∧dξ and Ω₁=ζΩ₀ exactly. In real coordinates (u,v,x,t), the displayed α, β and γ=uα−vβ follow with the published signs. The ball lies in this chart where Ω₀ never vanishes.

For the fixed smooth compactly supported cutoff, the one-forms R dv and Rv dv extend smoothly by zero. Hence βε−β and γε−γ are globally exact. The identity d(Rv dv)=v d(R dv) holds for arbitrary smooth R, including the transition region: the extra term R dv∧dv is zero. It gives γε=uα−vβε exactly. The derivatives Ru and Rt in that transition region cannot be discarded; they are retained in the full algebra below. Rv disappears for the valid algebraic reason dv∧dv=0.

**4. Positive plane and an explicit almost-complex matrix.** The wedge Gram matrix is

\[
\begin{pmatrix}2&R_t\\R_t&2(1-R_x)\end{pmatrix}\mathrm{vol}.
\]

Its determinant is 4D, where D=1−Rx−Rt²/4. The fixed cutoff has bounded derivatives, so one ε₀ makes |Rx|≤1/4 and |Rt|≤1 everywhere; D≥1/2 follows. Orthogonalizing and normalizing βε gives Bε=(βε−(Rt/2)α)/√D with α∧Bε=0 and Bε²=α². Thus Ψε=α+iBε is decomposable and has nonzero product with its conjugate. Its contraction kernel and conjugate are complementary rank-two complex bundles, defining a real almost-complex structure with the stated choice of (0,1) kernel.

Independently of the kernel argument, the same structure has the following real matrix, with columns the images of (∂u,∂v,∂x,∂t):

\[
J_\varepsilon=\frac1{\sqrt D}
\begin{pmatrix}
R_t/2&R_x-1&0&0\\
1&-R_t/2&0&0\\
0&-R_u&R_t/2&-1\\
-R_u&0&1-R_x&-R_t/2
\end{pmatrix}.
\]

Direct exact identities show J²=−I, J*α=−α, J*βε=−βε, and Ψ(X,JY)=iΨ(X,Y). The third anti-invariance identity follows from the retained pointwise relation, and was checked separately. The matrix reduces to J₀ at zero jet. This reconstructs the realization through a distinct matrix/Pfaffian route, without assuming the cited positive-plane theorem.

**5. Global gluing and smooth dependence.** The support is compactly contained in B, so R and every derivative are identically zero on a collar, not merely small there. On that collar the local matrix equals J₀ exactly. Extension by J₀ is consequently smooth on the closed product. All coefficients depend jointly smoothly on (ε,p); the denominator stays uniformly positive. Every derivative converges as ε→0 on the fixed compact set, proving C∞ convergence. Zeros of Ω₀ on the remote infinity fibers do not enter this construction: there J is defined directly as J₀. Exact perturbations preserve the already independent classes globally, completing the lower bound.

**6. Nonintegrability for every nonzero small parameter.** On the open core with ρ=1, let k=1−εx. The coframe is φ₁=du+i√k dv, φ₂=dx+i/√k dt. Expanding gives the stated Ψ. Exterior differentiation yields dφ₁∧φ₁∧φ₂=k′/(2k) vol. At the origin k=1 and k′=−ε, so this obstruction is already nonzero there whenever ε≠0. Integrability would force the (0,2) component of dφ₁ to vanish, and therefore that wedge to vanish. This uses only the necessary local consequence of integrability, not an unproved converse.

As a separate check, all six coordinate pairs of the Nijenhuis tensor were computed from the real matrix. In the paper's convention, N(∂u,∂x)=k′/(2k)∂u, hence −ε∂u/2 at the origin. At ε=0 the family returns to the integrable product, as required.

## Actual primary-source audit

Fresh primary PDFs and hashes are saved in `primary-sources/receipt.json`. The following are the exact reading scopes; the entire upstream papers were not claimed as independently verified.

- [DLZ, arXiv:1104.2511v1](https://arxiv.org/pdf/1104.2511v1): definitions/context, Conjecture 2.5 and surrounding conjectures, plus Theorem 1.1 and its definition of metric-related structures. Conjecture 2.5 is unrestricted apart from compact real dimension four. Theorem 1.1 concerns a **common compatible metric**, which is an additional hypothesis. On the core, compatibility with both J₀ and Jε would force guu=gvv=gvv/k, impossible at points with k≠1. Therefore the claimed counterexample does not contradict that theorem's hypotheses.
- [Donaldson, arXiv:math/0607083v1](https://arxiv.org/pdf/math/0607083v1), opening background on pp. 1–2: a positive oriented real two-plane of two-forms specifies the almost-complex structure; the stronger complex-symplectic statement includes closed normalized forms. The paper's kernel construction and the independent matrix reconstruction establish the particular realization directly.
- [Bande–Kotschick, arXiv:math/0703348v2](https://arxiv.org/pdf/math/0703348v2), §3.2, Theorem 6, Lemma 7 and the complete proof immediately following: the integrability theorem requires two symplectic forms whose recursion operator squares to −I. Here the normalized Bε is not closed: dBε=−k′/(2k^(3/2)) dx∧du∧dt on the core. The unnormalized closed pair has the wrong normalization to supply that recursion operator. The cited theorem is therefore correctly excluded; it is not a missing input to the proof.
- [Tan–Wang–Zhang–Zhu, arXiv:1112.0768v3](https://arxiv.org/pdf/1112.0768v3), definition of the ambient space and Theorem 1.1: the h⁻=0 set is open and dense among all smooth almost-complex structures on a closed four-manifold. A special non-generic one-parameter family retaining classes is consistent with that statement. The generic-vanishing proof is background and was not independently re-proved.

The comparison bibliography is not needed for the explicit existence theorem. No withdrawn paper is used as a theorem. This review makes no exhaustive historical comparison and does not certify the asserted literature search or first occurrence.

## Checkable evidence

`fresh_symbolic.py` imports no published checker or reviewer verdict. It uses skew matrices, Pfaffians, component exterior differentiation and coordinate Lie brackets. Both normal and optimized runs pass **44 exact symbolic checks**, **75 exact rational jet cases**, and **four negative controls**. These include the full arbitrary-cutoff identities; the complete real J matrix; all six core Nijenhuis components; compactification differential formulas; a local sum-of-squares for real holomorphic combinations; and the product intersection-form sanity check b₂=10, signature (5,5). The latter is compatible with three positive cohomology classes and is not needed to replace the Stokes argument. The two fresh JSON outputs agree exactly. SymPy 1.14.0 was used; no floating-point approximation was needed.

The portable profile was inspected and executed with normal and optimized outer Python. Each run authenticated **258 files**, the **24 original files**, and **7 archive members**, then replayed all three original symbolic checkers with assertions explicitly forced on. Both runs also rejected a deliberately false assertion. This matters because two original checkers use Python `assert`; simply running those raw scripts with `-O` would not validate their assertions. The profile avoids that issue, and the fresh checker uses explicit exceptions. Exact historical checker-output hashes matched. These are local algebra and integrity checks, not global proof certification.

All global reasoning—compactness, class independence, smooth patching and asymptotic smooth convergence—was checked analytically above rather than inferred from the finite computations. No substantive defect was found. The remaining limits are normal review limits: no formal verification, no independent human peer review, and no novelty certification.

## Independence and boundaries

No current sibling review or historical mathematical acceptance report informed this decision. The author proof's introductory candidate-status language was encountered while reading the actual derivation. The portable verifier authenticated historical reports as opaque bytes; their conclusions were not read or adopted. The mathematical checker programs themselves were inspected and rerun as evidence.

The result relies on small |ε|, a smooth cutoff, a closed manifold, the chosen chart and compactification, and the supplied explicit forms. The ε=0 case is integrable; D=0 would invalidate realization; replacing a cohomology claim by pointwise independence would be wrong. No larger-parameter, real-analytic, fixed-metric or exact-dimension extension is being promoted.

No website, spreadsheet, Git, publishing or Zenodo action and no external outreach occurred.
