# The AIM conformal-primitive statement needs a variational hypothesis

**Disposition:** the literal 2003 statement is false by a six-dimensional obstruction already exhibited by Branson in 2005. This is a source-status correction, with a direct verification of the known counterexample mechanism. **No new resolution of a current open conjecture is claimed.**

**Records:** 20002011 / AIM-GEOMETRY-0349 and its duplicate 20002052 / AIM-GEOMETRY-0390.  
**Date:** 30 September 2026. **Model and effort:** gpt-6-astra, xhigh.  
**Review:** separate source and mathematical verification pending.

## 1. Exact source and duplicate

In [the 2003 AIM workshop notes](https://aimath.org/WWN/confstruct/confstruct.pdf), Conjecture 1 on printed p. 17 assumes that a natural top-degree form $S_g$ has conformally invariant integral and concludes

$$S_g=aQ_g+L_g+G_g,$$

where $L_g$ is a pointwise conformal invariant density and $G_g$ is the conformal gradient of an integral of a natural local density. Explicitly, for some local $F$ and every smooth $\omega$,

$$\left.\frac{d}{dt}\right|_{0}\int_M F_{e^{2t\omega}g}=\int_M\omega G_g.$$

The preceding discussion, pp. 16–17, distinguishes this single-metric local primitive from a two-metric conformal cocycle. The conjecture is repeated as **Problem 30 on p. 28**, with the same hypothesis and conclusion. Thus the two records are one mathematical target; their different titles describe different prior partial calculations. They must not receive separate proof budgets or be counted as two discoveries.

The original source also states different divergence decompositions in Conjectures 2 and 3 on p. 18, repeated as Problems 31 and 32 on p. 28. Those are not the local-primitive assertion. The obstruction below is a parity-even polynomial natural density of exactly the critical weight, so it does not exploit any ambiguity about allowing nonpolynomial invariants or noncritical weights.

## 2. The decisive published correction

Thomas Branson, [*Q-curvature and spectral invariants*](https://www.dml.cz/bitstream/handle/10338.dmlcz/701742/WSGP_24-2004-1_3.pdf), *Rendiconti del Circolo Matematico di Palermo*, Series II, Supplement 75 (2005), pp. 11–55, makes the variational restriction explicit. In Proposition 13 and Conjecture 14 on p. 34, the relevant space is the space of densities with formally self-adjoint conformal linearization. It is contained in the larger space of densities having conformally invariant integrals.

On **p. 40, equations (53)–(54)** and the following discussion, Branson proves the containment is strict in dimension six, including on conformally flat metrics. He gives a nonzero skew-adjoint conformal linearization and identifies the divergence $\nabla^c(P_{ab|c}P^{ab})$, proportional to $\Delta|P|^2$, as another representative of the same obstruction. Both p. 34 and p. 40 were inspected as typeset pages, rather than relying only on OCR. The publication year is **2005**; “2004” in the repository filename denotes the Winter School volume, not its publication year.

This already contradicts the literal AIM hypothesis-to-conclusion implication. The calculation below supplies a short explicit realization of that published obstruction. It does not claim priority for it.

## 3. Necessary variational symmetry

For a density $H_g$, define its conformal linearization by

$$D_gH(\psi)=\left.\frac{d}{dt}\right|_0H_{e^{2t\psi}g}.$$

If $H$ is the conformal gradient of a twice differentiable functional $\mathcal F$ on the conformal class, then symmetry of mixed variations gives

$$\int_M\varphi D_gH(\psi)=\int_M\psi D_gH(\varphi) \qquad\text{for all }\varphi,\psi.$$

Indeed, apply equality of mixed partial derivatives to $\mathcal F(e^{2(s\varphi+t\psi)}g)$. In particular every local primitive required in the AIM statement has this property. The standard critical $Q$-curvature density also has formally self-adjoint conformal linearization, the critical GJMS operator. A pointwise conformal invariant density has zero conformal linearization. Consequently **every density admitting the asserted decomposition must have formally self-adjoint conformal linearization**.

This test concerns the linearization of the density, including the volume-form variation. It is not the assertion that the integral of the density has a symmetric second variation, which by itself would provide no such conclusion.

## 4. A six-dimensional counterexample

Let $M$ be any closed oriented six-manifold, and use the conventions

$$\Delta=\nabla^i\nabla_i,\qquad J=\frac{R}{10},\qquad P=\frac14(\operatorname{Ric}-Jg).$$

Thus $P$ is the Schouten tensor. Consider the universal natural density

$$\boxed{\;S_g=(\Delta_g|P_g|_g^2)\,dV_g.\;}$$

Its scalar factor has weight $-6$. By the divergence theorem, $\int_M S_g=0$ for every metric. Thus it satisfies the AIM hypothesis for every conformal change, and even for arbitrary changes of metric.

We show that it fails the necessary symmetry. Put $B=|P|^2$ and write

$$D_gS(\psi)=(\mathcal D_g\psi)\,dV_g.$$

The elementary conformal variation formulas in dimension six are

$$\dot{dV}=6\psi\,dV,\qquad \dot P_{ij}=-\nabla_i\nabla_j\psi,\qquad
\dot B=-4\psi B-2P^{ij}\nabla_i\nabla_j\psi,$$

and, for a varying scalar $b$,

$$\frac{d}{dt}\Big|_0\Delta_{e^{2t\psi}g}b_t
=-2\psi\Delta b+4\langle d\psi,db\rangle+\Delta\dot b.$$

Substitution, including the variation of $dV$, yields

$$\mathcal D_g\psi=-4\operatorname{div}(B\nabla\psi)-2\Delta\bigl(P^{ij}\nabla_i\nabla_j\psi\bigr). \tag{1}$$

Let $T\psi=P^{ij}\nabla_i\nabla_j\psi$. The first summand of (1) is formally self-adjoint and $\Delta$ is self-adjoint. Hence

$$\mathcal D_g-\mathcal D_g^*=-2(\Delta T-T^*\Delta),\qquad
T^*h=\nabla_j\nabla_i(P^{ij}h). \tag{2}$$

### Explicit local jets on a closed manifold

Take the flat six-torus, choose a small Euclidean coordinate ball around $p=0$, and let $f$ be a smooth cutoff of $x_1x_2x_3$, equal to that cubic near $p$. Set $g=e^{2f}g_{\rm flat}$ and choose a smooth $\psi$ equal to the same cubic near $p$.

At $p$, $f=df=\partial^2f=0$. The formula

$$P_{ij}=-f_{ij}+f_if_j-\tfrac12|df|^2\delta_{ij}$$

therefore gives

$$P(p)=0,\qquad \nabla_kP_{ij}(p)=-f_{ijk}(p).$$

Also $J=-e^{-2f}(\Delta_0f+2|df|^2)$ vanishes to order four near $p$, so $dJ(p)=0$. The contracted Bianchi identity gives $\nabla_iP^{ij}=\nabla^jJ$.

Because $\psi(p)=d\psi(p)=\nabla^2\psi(p)=0$, the product rule gives

$$\Delta(T\psi)(p)
=2\sum_{i,j,k}(\nabla_kP_{ij})(\nabla_k\nabla_i\nabla_j\psi)(p)
=-2\sum_{i,j,k}f_{ijk}(p)^2=-12.$$

There are six nonzero third derivatives, one for each permutation of $(1,2,3)$, and each equals one. On the other hand,

$$T^*(\Delta\psi)(p)=0.$$

To see this last equality, expand the double divergence: its terms contain respectively $P(p)$, $\operatorname{div}P(p)=dJ(p)$, or $\Delta\psi(p)$, all of which vanish. Equation (2) now gives the exact nonzero value

$$\boxed{\;((\mathcal D_g-\mathcal D_g^*)\psi)(p)=24.\;} \tag{3}$$

Thus the operator is not formally self-adjoint. For an explicit integral witness, the left side of (3) is positive on a sufficiently small neighborhood. Choose a nonnegative nonzero smooth $\varphi$ supported there. Then

$$\int_M\varphi\mathcal D_g\psi\,dV_g-\int_M\psi\mathcal D_g\varphi\,dV_g
=\int_M\varphi(\mathcal D_g-\mathcal D_g^*)\psi\,dV_g>0.$$

Therefore $S$ cannot have the AIM decomposition. This is a counterexample on a closed manifold, within a conformally flat class, using a universal polynomial curvature density of the intended critical weight. Changing the sign convention for the Laplacian only changes the nonzero witness's sign.

For comparison with Ricci-tensor notation, $|\operatorname{Ric}|^2=16|P|^2+14J^2$ in dimension six. The $\Delta J^2$ term is conformally variational, as follows directly from varying $\int J^3dV$. Thus $\Delta|\operatorname{Ric}|^2dV$ has the same obstruction, with witness value $384$ under these conventions.

## 5. Exact checks and the remaining boundary

`check_jets.py` verifies the cubic jets and independently differentiates the exact coordinate density. For $g=e^{2f}\delta$ in dimension six, put $C=\sum P_{ij}^2$, using Euclidean component contractions. Then

$$S_g=\operatorname{div}_0\bigl(e^{4f}\nabla_0(e^{-4f}C)\bigr)\,dx
=\bigl(\Delta_0C-4\langle df,dC\rangle-4C\Delta_0f\bigr)\,dx.$$

The script differentiates this polynomial expression, constructs its formal adjoint by coefficient differentiation, and obtains $\mathcal D\psi(p)=24$ and $\mathcal D^*\psi(p)=0$. All **25 exact checks** pass; no sampling or numerical tolerance is used. The closed-manifold localization and variational argument are proved above, not inferred from computation.

The distinction from Alexakis's established decomposition is substantive: his theorem allows an arbitrary natural divergence. The displayed $S$ is already such a divergence, so it is entirely compatible with that theorem. See [Alexakis, Theorem 1.1](https://sigma-journal.com/2011/019/sigma11-019.pdf).

[Case–Lin–Yuan](https://arxiv.org/pdf/1711.05579), Section 2 and Section 8.4, provides the modern conformally variational framework and the weight-six calculations. Branson's later Conjecture 14 uses a formally self-adjoint hypothesis and a space of generalized $Q$-type densities. The present note neither proves nor disproves that repaired conjecture in general dimensions, and does not identify its modern status with that of the literal 2003 sentence.

**Recommended queue action:** exclude the literal target from new-proof research as already refuted in published literature; mark 20002052 as a duplicate of 20002011. Any repaired variational target requires its own precise statement and current source audit, rather than a silent change of hypothesis.
