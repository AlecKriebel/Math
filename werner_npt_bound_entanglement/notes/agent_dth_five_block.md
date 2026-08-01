# Five-replica DTH block audit: the support-kernel map does not exist

## Status

This note gives an exact audit of the proposed constrained five-replica
question in the local block

\[
[4,1]\otimes[4,1]\otimes[3,2].
\]

There are two conclusions.

1. The cloud obstruction \(\xi\) is reconstructed exactly.  It survives the
   Pluecker and Omega constraints and has minimal-witness quotient \(-1/4\).
2. The requested complex-linear support map on
   \(\operatorname{Sym}^2(\wedge^2\mathcal H)\otimes\mathcal H\) cannot
   exist.  The support equation is mixed holomorphic--antiholomorphic, not a
   complex-linear kernel condition on the stated holomorphic monomial space.

Consequently the proposed common-kernel operator

\[
P_{\mathscr K_{\rm DTH}}\widetilde{\mathcal O}_0
P_{\mathscr K_{\rm DTH}}
\]

is not defined as stated.  A corrected scalar Hermitian support localizer is
available.  Even that corrected scalar first-level relaxation is indefinite;
an exact algebraic obstruction is given below.  This is a certificate-level
obstruction, not a physical DTH counterexample.

## 1. Exact reconstruction of \(\xi\)

Realize \([4,1]\) as the sum-zero part of the point module on five symbols,
with

\[
f_i=e_i-e_4,\qquad 0\le i\le3,
\]

and realize \([3,2]\) inside the two-subset module by

\[
r_{ab\mid cd}=e_{\{a,c\}}-e_{\{a,d\}}-e_{\{b,c\}}+e_{\{b,d\}}.
\]

Set

\[
\begin{aligned}
\xi={}&-
 (f_1\otimes f_1+f_3\otimes f_3)\otimes r_{01\mid23}\\
&+(f_3\otimes f_3-f_2\otimes f_2)\otimes r_{01\mid24}\\
&+(f_1\otimes f_1-f_0\otimes f_0)\otimes r_{04\mid23}.
\end{aligned}
\]

Dependency-free rational arithmetic verifies

\[
\|\xi\|^2=64,
\]

\[
F_{12}\xi=-\xi,\qquad F_{34}\xi=-\xi,
\qquad F_{(13)(24)}\xi=\xi,
\]

and

\[
\mathcal A_4\xi=0.
\]

For each half of the lift,

\[
\langle\xi,(\mathcal O_0)_{125}\xi\rangle
=
\langle\xi,(\mathcal O_0)_{345}\xi\rangle=-16.
\]

The full three-local-site antisymmetrizer in either triple also annihilates
\(\xi\).  Hence the coherent Omega maps vanish separately and the strong and
minimal witnesses agree on \(\xi\):

\[
\langle\xi,\widetilde{\mathcal O}_0\xi\rangle=-16,
\qquad
\frac{\langle\xi,\widetilde{\mathcal O}_0\xi\rangle}{\|\xi\|^2}
=-\frac14.
\]

## 2. No-go theorem for the claimed support map

Let

\[
\eta(w,z)=w\otimes w\otimes z
\]

and let \(W\) be the skew coefficient matrix of \(w\).  There is no
complex-linear map \(\mathcal C_{\rm supp}\) on the stated monomial space
such that, for every physical monomial,

\[
\mathcal C_{\rm supp}\eta(w,z)
=w\otimes(W^\dagger z)
\]

up to a fixed nonzero normalization and fixed linear tensor identification.

Indeed, replace \(w\) by \(e^{i\theta}w\).  Complex linearity would give

\[
\mathcal C_{\rm supp}\eta(e^{i\theta}w,z)
=e^{2i\theta}\mathcal C_{\rm supp}\eta(w,z).
\]

But the proposed right side is phase invariant:

\[
(e^{i\theta}w)\otimes((e^{i\theta}W)^\dagger z)
=w\otimes(W^\dagger z).
\]

Taking, for example, \(\theta=\pi/2\) contradicts the claimed identity at
every point for which \(w\otimes W^\dagger z\ne0\).

This is not a normalization problem.  The left side is holomorphic of degree
two in \(w\); the support vector is of bidegree \((1,1)\) in \(w,\bar w\).

The literal holomorphic replica contraction of replicas 3 and 5 instead gives

\[
w_{12}\otimes(W^{\mathsf T}z)_4,
\]

which is not \(w\otimes W^\dagger z\) for a general complex \(w\).  On the
real binary realization of the block its squared norm on \(\xi\) is exactly
\(6\), so even this incorrect substitute does not annihilate the known
obstruction.

## 3. Correct scalar Hermitian support localizer

Define the global cross Jucys--Murphy operator

\[
J_5=F_{15}+F_{25}+F_{35}+F_{45},
\]

where each \(F_{r5}\) swaps the full three-qutrit replicas \(r\) and \(5\).
For every skew \(w\), not only decomposable ones,

\[
\boxed{
\langle\eta(w,z),J_5\eta(w,z)\rangle
=4\|w\|^2\|W^\dagger z\|^2.
}
\]

To prove this, the expectation of each of the four swaps is

\[
\|w\|^2\,z^\dagger WW^\dagger z.
\]

The equality of the first- and second-leg reduced matrices follows from
\(W^{\mathsf T}=-W\).  Summing the four identical terms proves the formula.

Thus physical support implies a zero expectation of \(J_5\).  It does not
imply that the five-replica monomial lies in \(\ker J_5\): on the Pluecker
kernel, \(J_5\) is indefinite.

For the exact obstruction,

\[
\langle\xi,J_5\xi\rangle=-40.
\]

On the first-four-replica \([2,2]\) sector, induction to \(S_5\) gives the
two branches

\[
[3,2]\quad(J_5=+2),
\qquad
[2,2,1]\quad(J_5=-2).
\]

Put

\[
\xi_+=\frac12\left(I+\frac{J_5}{2}\right)\xi,
\qquad
\xi_-=\frac12\left(I-\frac{J_5}{2}\right)\xi.
\]

Then exact arithmetic gives

\[
\|\xi_+\|^2=22,qquad \|\xi_-\|^2=42.
\]

This identifies precisely how the support equation excludes the original
\(\xi\): a physical supported monomial has equal \(+2\) and \(-2\) branch
mass, whereas \(\xi\) has masses \(22\) and \(42\).

## 4. Exact obstruction to the corrected scalar first lift

Although \(\xi\) is not \(J_5\)-isotropic, define

\[
\boxed{
\zeta=\sqrt{21}\,\xi_+ + \sqrt{11}\,\xi_-.
}
\]

Both branches remain in the source symmetry space and in the kernels of
\(\mathcal A_4\) and both Omega maps.  Moreover,

\[
\|\zeta\|^2=21\cdot22+11\cdot42=924
\]

and

\[
\langle\zeta,J_5\zeta\rangle
=21(2\cdot22)+11(-2\cdot42)=0.
\]

The minimal witness Gram matrix on \((\xi_+,\xi_-)\) is

\[
\begin{pmatrix}
55/32&-231/32\\
-231/32&-105/32
\end{pmatrix}.
\]

Consequently

\[
\langle\zeta,\widetilde{\mathcal O}_0\zeta\rangle
=-\frac{231\sqrt{231}}{16}
\]

and

\[
\boxed{
\frac{
\langle\zeta,\widetilde{\mathcal O}_0\zeta\rangle
}{\|\zeta\|^2}
=-\frac{\sqrt{231}}{64}<0.
}
\]

The separation from the physical Segre locus is already visible in the
simplest flattening.  Up to a nonzero scalar, write

\[
\zeta'=\sqrt{231}\,\xi_+ + 11\xi_-.
\]

Exact Gaussian elimination over \(\mathbb Q(\sqrt{231})\) gives

\[
\boxed{
\operatorname{rank}_{1234:5}(\zeta')=7.
}
\]

A physical vector \((w\otimes w)\otimes z\) has rank one across this cut.
Thus \(\zeta\) violates a basic Segre-minor family very strongly; it is not a
near miss caused only by the Pluecker relations.

Therefore no certificate consisting of positivity on the Pluecker/Omega
kernel plus an arbitrary scalar multiple of the Hermitian support localizer
\(J_5\) can prove DTH at this level.

This does **not** yet exclude every correctly formulated first-degree support
ideal certificate.  Componentwise equations \(W^\dagger z=0\) have mixed
bidegree and require a mixed moment/localizing module, not a common kernel in
the holomorphic space \(\mathscr X\).  A natural enlarged monomial is

\[
w\otimes\bar w\otimes z,
\]

on which contraction to \(w\otimes W^\dagger z\) is linear.  A valid finite
relaxation must also impose the rank-one consistency relations tying this
mixed monomial to \(w\otimes w\otimes z\).  Those data are absent from the
proposed five-replica common-kernel question.

## 5. Logical scope

Exact conclusions:

- the original \(\xi\) survives Pluecker and Omega but fails physical support;
- the claimed complex-linear \(\mathcal C_{\rm supp}\) does not exist;
- support acts as an equal-mass condition between the \([3,2]\) and
  \([2,2,1]\) branches;
- the corrected scalar-support relaxation has the exact negative algebraic
  pseudomoment \(\zeta\).

Not proved:

- \(\zeta\) is not asserted to be a physical Veronese--Segre monomial;
- the full mixed-bidegree support ideal has not been classified;
- DTH, square-zero positivity, unrestricted three-copy positivity, and the
  all-copy problem remain open.

Completion estimate for the stated holomorphic common-kernel decision: 100%,
because the support map required to define it is impossible.  Completion
estimate for a correctly reformulated mixed-moment first-level DTH decision:
25%.

The independent exact checker is
`verification/agent_dth_five_block.py`.
