# Independent review of the Giroux-torsion partial results

**Verdict: PASS_SCOPED_VOLUME_DEGENERATION_AND_QUANTIFIER_DIAGNOSTICS.** The contact-volume bound, inverse-derivative consequence, and local fixed-point conformal collapse are correct. The closed-manifold torsion problem remains **unsolved, 2/5**. No mandatory correction is required. This is an independent adversarial AI review, not human peer review or a priority claim.

The reviewed `PARTIAL.md` has SHA-256 `1eb9f52ebab0c3a6357bba18343266020053e5c8a40fcfaa200d8f5bf7c58def`. All 372 submitted assertions reproduce byte for byte under SymPy 1.14.0. A separate standard-library program passes 13,569 exact controls.

## 1. The original quantifiers and normalization

I inspected the rendered K3 manuscript pp.160 and 162. The contact-topology section starts with closed three-manifolds and normally assumes coorientability. Problem 3.42 concerns finite Giroux torsion for each fixed tight contact structure. Its definition uses contact **embeddings** of the closed domain T²×[0,1], with both torus coordinates of period one, and the kernel of

\[
\beta_n=\cos(2\pi nz)\,dx-\sin(2\pi nz)\,dy.
\]

The manuscript takes the supremum over positive integral n and assigns zero when there are no embeddings. The candidate retains the closed and fixed-structure scope. Neither varying the contact structure on one closed manifold nor choosing a single noncompact target answers that question. [Primary K3 manuscript, pp.160–162](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).

## 2. Volume and inverse-derivative bounds

The minus sign in beta_n and the order dx∧dy∧dz give the **positive** density 2πn. I recalculated this independently. If phi is a contact embedding, equality of the two plane kernels gives phi*alpha=f beta_n for a smooth nowhere-zero real f. No coorientation-preservation assumption is needed for the volume calculation, since its factor is f².

The exterior product cancels the df term:

\[
\phi^*(\alpha\wedge d\alpha)
=f^2\beta_n\wedge d\beta_n
=2\pi n f^2\,dx\wedge dy\wedge dz.
\]

This also proves that the embedding preserves the induced contact orientation. Change of variables identifies the integral with the volume of its image, at most the fixed finite total V_alpha. Injectivity is essential: an immersion with overlapping image or a covering would count volume with multiplicity and would not justify this upper bound.

The model domain has volume one, so min|f|≤sqrt(V_alpha/(2πn)); the superlevel estimate is the elementary inequality epsilon²·vol{|f|≥epsilon}≤integral f². Along a hypothetical sequence n→infinity the functions therefore converge to zero in L² and in measure, in this fixed domain/contact-form normalization. This does not assert uniform convergence or a pointwise limit for an arbitrary sequence.

For the metric consequence, let A=Dphi and eta=alpha at the image point. Since eta=(A^{-1})*A*eta,

\[
\lVert A^*\eta\rVert\ge
\frac{\lVert\eta\rVert}{\lVert A^{-1}\rVert}.
\]

The model covector beta_n has norm one. Compactness and nonvanishing of alpha give m_alpha>0, and the smooth embedding gives a finite maximum L_phi of the inverse norm. Thus |f|≥m_alpha/L_phi everywhere, yielding L_phi≥m_alpha sqrt(2πn/V_alpha). Boundary points cause no failure: a smooth same-dimensional embedding has an invertible tangent map there as well. These estimates depend on the fixed choices of form and metric and do not define a new contact invariant.

## 3. Local collapse really occurs in a fixed closed tight structure

The Darboux argument needs only equality of kernels: alpha=b(dq+p dt) with b nowhere zero. For gamma=dq+p dt, Cartan's formula gives

\[
X_H=(H-pH_p)\partial_q+(pH_q-H_t)\partial_p+H_p\partial_t,
\qquad \mathcal L_{X_H}\gamma=H_q\gamma.
\]

Indeed gamma(X_H)=H and dH+i_(X_H)(dp∧dt)=H_q(dq+p dt). This confirms the sign and coordinate conventions in the candidate. Near the origin, H0=2q+pt gives the linear vector field (2q,p,t). A cutoff equal to one in a neighborhood of the origin changes neither the field nor its derivative there and produces a smooth contact vector field supported inside the chart. Its extension by zero is complete on the closed manifold.

The origin is fixed for every time. The derivative of the flow at that point is diag(e^(2s),e^s,e^s). The covector gamma there therefore scales by e^(2s); since the point is fixed, the value of b cancels, so alpha has the same scaling factor there. Taking s=−T and composing with the original embedding gives exactly the claimed factor e^(−2T) at the selected domain point. The flow is a global contactomorphism isotopic to the identity, so the target contact structure and embeddedness are preserved.

The closed universally tight example in the next section admits a one-turn domain. Consequently this disproves an automatic positive lower bound on min|f| **over all** such embeddings in a fixed tight example. It does not show that their L² masses can be made small, that a large torsion layer can be inserted by dilation, or that suitably selected representatives cannot have useful normalization. The candidate explicitly preserves each distinction.

## 4. The two standard models do not resolve the closed target

For alpha_k on T³, the displayed change of universal-cover coordinates has determinant 2πk and inverse obtained by the inverse planar rotation and scale. Direct differentiation gives dQ+P dZ=alpha_k. The universal cover is thus contactomorphic to the standard tight model. Tightness of standard contact R³ is the classical Bennequin input, explicitly recalled for these torus structures by Colin on printed p.270. An overtwisted disk in any cover would lift to an embedded overtwisted disk in the universal cover, so universal tightness follows. This uses an established theorem; the finite checker is not a proof of tightness. [Colin's primary paper, p.270](https://www.numdam.org/item/ASENS_2001_4_34_2_267_0.pdf).

When 1≤n<k, z↦(n/k)z modulo one is injective on the closed interval because its range has length less than one. Together with the identity on T², this gives the stated contact embedding and lower bound GT(T³,xi_k)≥k−1. At n=k the two boundary tori coincide. When n>k, points separated by k/n in the domain coordinate coincide. The degree-k periodic map is likewise a covering rather than an embedding for k>1. These failures correctly prevent a false infinite-torsion conclusion for one fixed xi_k.

On T²×R there is no periodic identification in the final coordinate; z↦nz embeds every finite layer. The same universal-cover calculation establishes universal tightness, and the total contact volume is infinite. This is a valid noncompact infinite-torsion example, explicitly outside the source's closed class. The varying closed examples rule out only a bound depending on the underlying manifold alone, while the noncompact example shows why the ambient compactness convention matters.

## 5. Existing theorems and the residual gap

Colin's Theorem 1.4 on p.268 assumes irreducibility, universal tightness and a normal isotopy class, where normality involves persistent intersection with an incompressible torus. Theorem 1.7 on p.269 gives finiteness of the number of isotopy classes containing a torsion-one submanifold under closedness, irreducibility and universal tightness. The candidate correctly declines to remove normality or universal tightness or infer a finite total supremum from merely finitely many classes.

I also checked Gay's Corollary 2.2 and its proof on printed p.1751 in the complete primary PDF. The proof assumes a strongly convex boundary of a compact symplectic filling; the result is the vanishing of Giroux torsion for strongly fillable structures. It does not assert that every tight structure is strongly fillable. [Gay's primary paper, Corollary 2.2](https://arxiv.org/pdf/math/0606402).

The full proofs of these deep imported theorems are not recertified here. Their precise hypotheses and applications have been checked. The unresolved step is an appropriate global control or normalization that excludes unbounded embedded layers in every fixed closed tight structure, or a genuine fixed closed tight counterexample. The partial volume argument supplies neither.

## 6. Reproduction and finite evidence

The submitted checker uses SymPy 1.14.0 for symbolic identities and rational controls. Its 372 assertions and frozen receipt were reproduced. The separate checker uses only the Python standard library: it verifies exterior-volume densities at arbitrary rational one-form jets, Cartan's Hamiltonian identity, the global rotating-coordinate inverse, exact dilation factors, diagonal covector inequalities and interval-wrapping diagnostics. All 13,569 assertions pass.

```
python author_replay/verify.py
python independent_checks.py
```

These tests supplement the geometric proofs. They certify neither a new tightness theorem nor finite/infinite torsion for an arbitrary fixed closed tight contact manifold. Publish the package as scoped partial results, retaining unsolved 2/5 and no novelty claim.
