# Independent source and mathematical review: the conformal-primitive statement

**Verdict: PASS as a source-status correction for an already known counterexample.** The literal 2003 AIM implication is false, and the nonvariational six-dimensional divergence used in the note is explicitly identified in Branson's 2005 publication. The closed-torus calculation correctly realizes that published obstruction. No new discovery or resolution of a repaired variational conjecture is supported or claimed.

**Target:** 20002011 / AIM-GEOMETRY-0349.  
**Duplicate:** 20002052 / AIM-GEOMETRY-0390.  
**Reviewed document:** SOURCE_STATUS.md.  
**Reviewed SHA-256:** b6d39596acb84613b15c43c5a9f6d2382bbd4826348638398d793fab4cbc7463.  
**Date:** 30 September 2026. **Reviewer model:** gpt-6-astra, xhigh.

This is an independent AI review, not human peer review or formal verification. No substantive mathematical correction is required.

## What the original source actually says

The [AIM workshop notes](https://aimath.org/WWN/confstruct/confstruct.pdf) are dated 15 October 2003. On printed p. 17, Conjecture 1 assumes only that the integral of a natural top-degree density is conformally invariant. It concludes that the density is a constant multiple of the standard critical Q-curvature density, plus a pointwise conformal invariant density, plus a density with a local conformal primitive. The preceding discussion defines the last term by variation of an integral of a single-metric local invariant. There is no formal-self-adjointness assumption in the conjecture.

Problem 30 on printed p. 28 repeats the same statement and definition. The two stored records reproduce these two occurrences, so the duplicate identification is exact. Different record titles do not create different mathematical questions. The adjacent divergence decompositions are separately numbered conjectures/problems and do not allow replacing the primitive condition by an arbitrary divergence in this target.

## The decisive published obstruction

[Branson, Q-curvature and spectral invariants](https://www.dml.cz/bitstream/handle/10338.dmlcz/701742/WSGP_24-2004-1_3.pdf), was published in 2005; the digitized volume's title page confirms the year. Proposition 13 and Conjecture 14 on printed p. 34 distinguish conformally invariant integrals from densities with formally self-adjoint conformal linearization.

Printed p. 40, equations (53)–(54), gives a nonzero skew part of that linearization in dimension six. The following paragraph explicitly identifies the divergence
$\nabla^c(P_{ab|c}P^{ab})$ as another representative, with a nonzero proportional skew part. Metric compatibility makes this divergence $\frac12\Delta|P|^2$ under the note's Laplacian convention. Branson also explicitly observes the obstruction in the conformally flat setting. The review inspected the typeset pages 34 and 40, including their displayed formulas.

Thus the literature does contain the needed counterexample mechanism, rather than merely a related conjecture or an abstract dimension count.

## Variational necessity

Use affine coordinates on a conformal class, so a metric is written $e^{2u}g$. If a density $H$ is the conformal gradient of a twice differentiable functional, the two mixed variations in arbitrary directions $\varphi,\psi$ commute. Consequently its density-valued conformal linearization satisfies
\[
\int_M\varphi\,D_gH(\psi)=\int_M\psi\,D_gH(\varphi).
\]
There is no additional derivative of either test function: these are fixed affine directions in the conformal factor.

The linearization of the critical Q-curvature density is the formally self-adjoint critical GJMS operator. A pointwise conformal invariant density has zero linearization. A local conformal gradient has the symmetry just derived. Hence the proposed decomposition forces formal self-adjointness. This is a necessary condition, so the note needs no general converse or inverse-variational theorem.

It is essential that the volume-form variation is included. Symmetry of the Hessian of the integral of the proposed density would be a different assertion and would not establish the required condition. The note uses the correct density-valued variation.

## Audit of the six-dimensional calculation

The proposed density is polynomial and natural, of critical weight, and its integral vanishes on every closed manifold by the divergence theorem. It therefore satisfies the literal hypothesis.

With $B=|P|^2$ and $T\psi=P^{ij}\nabla_i\nabla_j\psi$, the variations in the note give
\[
\begin{aligned}
D_g\bigl((\Delta B)dV\bigr)(\psi)/dV
&=4\psi\Delta B+4\langle d\psi,dB\rangle
  +\Delta(-4\psi B-2T\psi)\\
&=-4\operatorname{div}(B\nabla\psi)-2\Delta T\psi.
\end{aligned}
\]
The coefficient $4$ uses dimension six and includes the volume variation. The first term is symmetric. Integration by parts twice gives
$T^*h=\nabla_j\nabla_i(P^{ij}h)$, so the skew part is exactly
$-2(\Delta T-T^*\Delta)$.

For the cubic $f=x_1x_2x_3$ and $g=e^{2f}\delta$ near the origin, $f$, its first derivatives and its second derivatives vanish there. Hence $P=0$ and $\nabla_kP_{ij}=-f_{ijk}$ at that point. The cubic is harmonic and $|df|^2$ is quartic, so the asserted vanishing of $J$ through order three is correct. Thus $\operatorname{div}P=dJ=0$ at the point.

For $\psi=f$ near the origin, the product rule leaves precisely
\[
\Delta(T\psi)(0)=2\sum_{i,j,k}(-f_{ijk})f_{ijk}=-12.
\]
There are six nonzero third-derivative entries, all equal to one. The covariant third derivatives equal ordinary derivatives at this point because the lower jets of the conformal factor and test function vanish appropriately. Also $\Delta_g\psi$ has zero two-jet at the origin: it equals $4e^{-2f}|df|^2$ near that point. This independently proves $T^*(\Delta_g\psi)(0)=0$. It follows that the skew operator applied to $\psi$ has value $24$, with the stated conventions.

A smooth cutoff equal to one on a smaller coordinate ball transports these exact jets to a smooth function on the flat six-torus. The conformal metric remains smooth and positive definite everywhere. The operator and test function are smooth, so the nonzero positive value persists in a neighborhood. A nonnegative test function supported in that neighborhood gives the strict integral asymmetry claimed in the note. This supplies a closed-manifold witness and justifies the integration by parts; no periodic polynomial or globally flat coordinate chart is assumed.

The Ricci conversion is correct:
$|4P+Jg|^2=16|P|^2+(8+6)J^2$.
At critical dimension six, varying $\int J^3dV$ gives the density
$-3\Delta(J^2)dV$ with these conventions. That contribution is conformally variational, so the Ricci-norm version has the same obstruction multiplied by sixteen, namely the value $384$ at the displayed jet.

## Computational verification

The author's script was copied to an isolated review directory and rerun without modifying the submitted files. All 25 assertions passed, and its JSON receipt reproduced byte for byte.

The separate independent_checks.py reconstructs the relevant covariant Hessian and Laplace–Beltrami jets from the conformal Christoffel symbols, using all six tensor indices. Its 21 exact assertions also passed under SymPy 1.14.0. These include the value $-12$ for $\Delta T\psi$, the zero two-jet of $\Delta\psi$, the final skew value $24$, and four harmonic-cubic leading-jet checks. No numerical tolerance or sample-based inference is used. Reproduce from the review directory with python independent_checks.py.

The author's full-density calculation uses three active coordinate variables but six-dimensional Schouten contractions. That restriction is valid for this witness, which is independent of the other coordinates in the neighborhood used for the jets. Derivatives in inactive coordinates give no missing contribution to the displayed value.

The finite calculations validate the local identities; the preceding argument supplies variational necessity, closed-manifold localization, and the integral witness.

## Scope of the disposition

[Alexakis's divergence decomposition](https://sigma-journal.com/2011/019/sigma11-019.pdf), Theorem 1.1, permits a natural divergence. The example is itself such a divergence and is compatible with that theorem. It does not refute the divergence decomposition.

[Case–Lin–Yuan](https://arxiv.org/pdf/1711.05579), Section 2, uses formal self-adjointness in its conformally variational framework. Branson's later formulation likewise imposes variational symmetry and uses a space of generalized Q-type densities. The note does not prove or disprove that repaired statement in general dimensions, and the present review makes no claim about its current global status.

The defensible disposition is therefore: the literal imported 2003 claim has a known published negative answer; 20002052 is the same target; no new solution should be counted. The source qualification and separation from any repaired conjecture should remain in the published package.
