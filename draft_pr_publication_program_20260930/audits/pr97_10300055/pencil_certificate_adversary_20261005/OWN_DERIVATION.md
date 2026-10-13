# Independent global-pencil obligations and derivation

Recorded 2026-10-05 23:50:33 UTC before reading any prior or other fresh review report. This reviewer has read the complete incoming CANDIDATE.md and both diagnostic sources. No central proof search, priority judgment, publication authority, or human peer review is asserted.

## Exact conditional target

On a closed oriented smooth three-manifold, assume a cooriented taut C2 foliation without spherical leaves, global C1 forms alpha and omega with alpha nowhere zero, d alpha = alpha wedge omega, and omega wedge d omega nowhere zero. The target is tightness of ker omega. It does not assert existence of such omega, solve the neighboring weak-sign/existence question, or establish historical priority.

## Independent derivation

1. Distributionally, d squared alpha is zero. Because alpha wedge omega is C1 and equals d alpha, the distributional product calculation is legitimate and its resulting continuous form vanishes pointwise: alpha wedge d omega = 0. The other mixed term omega wedge d alpha is omega wedge alpha wedge omega = 0, and alpha wedge d alpha = 0. Therefore for every spatially constant real s, (omega+s alpha) wedge d(omega+s alpha) equals omega wedge d omega. A nowhere-zero three-form implies omega+s alpha itself has no zeros. The calculation is insensitive to orientation convention or negative s.

2. On compact M, a0=min |alpha| is positive and W=max |omega| is finite. For s>2W/a0, alpha+omega/s is nonzero and converges uniformly to alpha. Normalization is uniformly continuous away from zero; more quantitatively, the normalized covectors differ by at most 2W/(s a0). Thus their cooriented kernels converge uniformly. The target plane field is reached only as a limit; it is never an endpoint to which Gray stability is applied.

3. For smooth inputs, choose one finite S for which the endpoint lies in the tight-contact neighborhood of the foliation. The entire finite interval [0,S] consists of smooth contact forms with unchanged contact volume. Smooth Gray stability connects the endpoint to omega, so the endpoint's tightness transfers. The neighborhood must constrain every sufficiently close contact structure; existence of one tight approximation alone would not suffice.

4. For C1 inputs, first choose finite S using the original pencil. Let a and eta be smooth approximations to alpha and omega in C1, respectively. On M times [0,S], eta+s a differs in form and exterior-derivative norm by at most (1+S) times the approximation error. If the original form and derivative norms are bounded by B and its positive volume is at least c0 after orienting components, the volume perturbation is at most 2B delta+delta squared. Choosing this less than c0/2 gives a smooth contact path. Endpoint plane-field closeness is an additional open condition. Smooth Gray makes every sufficiently C1-close smooth eta tight. No equation or integrability is required for a.

5. Suppose an overtwisted disk has smooth Legendrian boundary gamma and tangent disk planes uniformly distinct from the contact planes there. In a fixed smooth tubular chart (t,u,v), write q_j(t)=theta_j(gamma prime(t)). C1 convergence of theta_j makes q_j and its t derivative tend uniformly to zero. Subtract q_j(t) chi(u,v) dt. The correction is smooth, supported inside the chart, tends to zero in C1, and annihilates gamma prime exactly. Contactness and boundary-plane distinction persist. For a C2 disk, smooth approximating embeddings converge in C2; gamma_j are graphs over a fixed smooth nearby curve and q_j=theta_j(gamma_j prime) tends to zero in C1 by the chain rule. Moving the cutoff with the graph has bounded first derivatives and gives the same result. This is the appropriate contradiction to the smooth-neighbor claim; it uses no C1 version of Gray.

## Adversarial boundary tests

- Disconnected M: each component's contact sign is constant. A compact manifold has finitely many components, so their neighborhoods and minima admit common finite bounds. Reorient negative components for the positive-contact theorem. Disk existence/tightness is orientation-independent.
- Removing nowhere-zero alpha invalidates the uniform normalized convergence argument. Removing compactness invalidates uniform minima, a common finite S, and the stated closed-manifold Gray application.
- Allowing variable h gives the additional volume term omega wedge d h wedge alpha. This can cancel the contact volume, so variable shifts are not a valid Gray route.
- A local formal coframe example is not evidence of global tautness or a closed-manifold example. General pointwise jets are useful algebra controls only. The imported contact-neighborhood and Gray theorems need primary-source checking, not symbolic diagnostics.
- The theorem assumes global coorientation and forms. A local gauge computation cannot substitute for those hypotheses. No extension to boundary, noncompact, noncooriented, merely continuous, or non-taut settings is claimed.
- The alternative disk definition must be equivalent to the usual smooth overtwisted criterion (Legendrian boundary with zero relative contact twisting); direct primary-source confirmation is still required. For a C1 definition with a smooth or C2 disk, the provided approximation lemma is checkable as above.

Current estimate: 45% of this bounded independent audit. No substantive pencil/finite-path defect found; computational guard enforcement and primary contact statements remain to be checked.
