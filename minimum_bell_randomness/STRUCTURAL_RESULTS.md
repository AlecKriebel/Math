# Structural results under audit

These statements are written in proof-ready form but remain provisional until
the independent verification track is complete.

## 1. Exact one-wing one-input impossibility

Let \(p(a,b|y)\) be any finite-dimensional quantum behavior in which Alice
has exactly one \(d\)-outcome projective input and Bob has any finite number
of \(d\)-outcome projective inputs.  Fix a target \(y_*\).  Then the same full
behavior has a compatible pure realization for which

\[
G(AB|0,y_*,E)
\geq
\sum_a\max_b p(a,b|y_*)
\geq \frac1d.
\]

To prove this, start from any realization
\(\rho_{AB},\{P_a\},\{Q_{b|y}\}\) and define the subnormalized states

\[
\rho_B^a
=
\operatorname{Tr}_A\!\left[
(P_a\otimes I)\rho_{AB}(P_a\otimes I)
\right].
\]

Choose subnormalized purifications
\(|\phi_a\rangle_{BE_0}\) of the \(\rho_B^a\), all in one finite-dimensional
space, and set

\[
|\Psi'\rangle
=
\sum_a
|a\rangle_{A'}|\phi_a\rangle_{BE_0}|a\rangle_{E_1}.
\]

Alice uses the computational rank-one PVM and Bob retains every
\(Q_{b|y}\).  This reproduces every probability \(p(a,b|y)\), while

\[
\sigma_{E_0E_1}^{ab|y}
=
\operatorname{Tr}_B\!\left[
(Q_{b|y}\otimes I)|\phi_a\rangle\langle\phi_a|
\right]\otimes |a\rangle\langle a|_{E_1}.
\]

The Eve supports for distinct \(a\) are orthogonal.  After reading \(a\),
Eve guesses a value \(b_a\) maximizing \(p(a,b|y_*)\), which gives the first
bound.  The second follows from
\(\max_b p(a,b|y_*)\geq p(a)/d\).  If \(p(a)=0\), take
\(|\phi_a\rangle=0\); zero-probability outcomes and zero projectors cause no
difficulty.

The symmetric statement holds if Bob has one input and Alice has arbitrarily
many:

\[
G(AB|x_*,0,E)
\geq
\sum_b\max_a p(a,b|x_*,0)
\geq\frac1d.
\]

Thus \(m_A,m_B\geq2\) is necessary even when the complete behavior, rather
than only one score, is known.  This must not be confused with using one
designated generation setting per party inside a larger Bell test.

## 2. Private-MUB composition lemma

Let \(P_b\) be Alice's reference projectors, \(R_a\) Alice's target
projectors, and \(Q_{\pi(b)}\) Bob's added-setting projectors. Suppose, on the
tested state and its purification:

1. \(P_b\) produces a uniform outcome independent of Eve;
2. \(Q_{\pi(b)}|\Psi\rangle=P_b|\Psi\rangle\);
3. \(P_bR_aP_b|\Psi\rangle=d^{-1}P_b|\Psi\rangle\).

Then

\[
\sigma_E^{a,\pi(b)}=\rho_E/d^2
\]

for every \(a,b\).

A purification-stable projector-level self-test of a maximally entangled
qudit with branchwise mutually unbiased \(P\) and \(R\) implies hypotheses
1 and 3. A separately bounded perfect-correlation term implies hypothesis 2.
State extraction alone, scalar overlap averages, and observed uniformity do
not suffice.

## 3. Exact and setting-optimal binary construction

For binary Hermitian unitary observables define

\[
\mathcal W_2
=
A_0\otimes B_0-2A_0\otimes B_1
+2A_1\otimes B_0+2A_1\otimes B_1.
\]

There is an exact sum-of-squares identity

\[
\begin{aligned}
3\sqrt3 I-\mathcal W_2
={}&
\frac1{2\sqrt3}
\bigl(\sqrt3 A_0\otimes I-I\otimes B_0+2I\otimes B_1\bigr)^2\\
&+
\frac1{\sqrt3}
\bigl(\sqrt3 A_1\otimes I-I\otimes B_0-I\otimes B_1\bigr)^2.
\end{aligned}
\]

Consequently the quantum maximum is at most \(3\sqrt3\).  Equality on a
purification \(|\Psi\rangle\) gives

\[
(B_0-2B_1)|\Psi\rangle=\sqrt3 A_0|\Psi\rangle,
\qquad
(B_0+B_1)|\Psi\rangle=\sqrt3 A_1|\Psi\rangle.
\]

Put

\[
X_A=\frac{A_0+2A_1}{\sqrt3},
\qquad
Z_B=\frac{B_0-2B_1}{\sqrt3}.
\]

The equality relations imply

\[
B_0|\Psi\rangle=X_A|\Psi\rangle,\qquad
Z_B|\Psi\rangle=A_0|\Psi\rangle,
\]

\[
X_A^2|\Psi\rangle=Z_B^2|\Psi\rangle=|\Psi\rangle,
\qquad
\{A_0,X_A\}|\Psi\rangle
=
\{Z_B,B_0\}|\Psi\rangle=0.
\]

The Hermitian operators \(S_A=X_A\otimes B_0\) and
\(S_B=A_0\otimes Z_B\) stabilize \(|\Psi\rangle\).  For every Hermitian
operator \(R\) on Eve, inserting these stabilizers on both sides gives

\[
\langle A_0R\rangle=0,\qquad
\langle B_0R\rangle=0.
\]

Moreover,
\(\langle A_0B_0R\rangle=\langle A_0X_AR\rangle\).  The former is real,
whereas state-supported anticommutation makes the latter purely imaginary;
hence it also vanishes.  These are all three nontrivial operator-valued
binary Fourier coefficients, so

\[
\sigma_E^{ab}=\rho_E/4
\]

at the target \((A_0,B_0)\).

The maximally entangled qubit strategy

\[
A_0=Z,\quad
A_1=-\tfrac12Z+\tfrac{\sqrt3}{2}X,\quad
B_0=X,\quad
B_1=-\tfrac{\sqrt3}{2}Z+\tfrac12X
\]

attains \(3\sqrt3\).  Together with Section 1, this proves that
\((2,2)\) is setting-minimal for \(d=2\).

For comparison, the simpler binary \(2\times3\) composition

For Hermitian binary observables,

\[
\mathcal S
=
A_0(B_0+B_1)+A_1(B_0-B_1)+A_1B_2
\leq 2\sqrt2+1.
\]

The CHSH sum-of-squares identity and the bound \(A_1B_2\leq I\) prove the
upper bound. Equality gives the CHSH stabilizers, state-dependent
anticommutation of \(A_0,A_1\), and \(B_2|\Psi\rangle=A_1|\Psi\rangle\).
All three nontrivial operator-valued Fourier coefficients of the target
\((A_0,B_2)\) vanish, so

\[
\sigma_E^{ab}=\rho_E/4.
\]

The EPR strategy with \(A_0=Z,A_1=X\),
\(B_{0,1}=(Z\pm X)/\sqrt2\), and \(B_2=X\) attains equality.

## 4. Exact audit of the standard two-input qudit strategy

For the standard Fourier-phase maximally entangled strategy, all four joint
tables have the form

\[
p(a,b|x,y)
=
\frac{\sin^2(\pi\delta_{xy})}
{d^3\sin^2\!\left(\pi(a-b+\delta_{xy})/d\right)},
\]

where, up to input swaps, transposition, conjugation, and outcome
relabeling,

\[
(\delta_{xy})=
\begin{pmatrix}
1/4&3/4\\
-1/4&1/4
\end{pmatrix}.
\]

Thus every table has

\[
p_{\max}
=
\frac1{2d^3\sin^2(\pi/(4d))},
\qquad
p_{\min}
=
\frac1{2d^3\cos^2(\pi/(4d))}.
\]

No table is uniform for any \(d\geq2\), although both marginals are uniform.
Its ideal joint min-entropy is

\[
H_{\min}
=
\log_2\!\left(2d^3\sin^2\frac{\pi}{4d}\right)
=
\log_2d+\log_2\frac{\pi^2}{8}+o(1).
\]

Now anchor a third Bob setting perfectly to either one of Alice's two ideal
measurements by adding a separately bounded correlation term.  The aligned
pair has only \(d\) possible joint outcomes.  For the cross pair,

\[
p_{\max}^{\mathrm{cross}}
=
\frac1{d^3\sin^2(\pi/(2d))}
>
\frac1{d^2}
\qquad(d\geq3).
\]

The ideal strategy already saturates both separately bounded terms, so this
single nonuniform maximizing realization disproves maximal-global-randomness
certification by that augmentation.  The unique exception is \(d=2\), where
the two Alice bases are mutually unbiased and the cross table is uniform.

## 5. A stronger obstruction to the computational-MUB repair

Let \(F\) be the \(d\)-dimensional Fourier matrix, put
\(\rho=e^{\pi i/d}\), and let

\[
R=\operatorname{diag}(1,\rho,\ldots,\rho^{d-1}).
\]

The real Hermitian operator system generated by the two standard Alice PVMs
is

\[
\mathcal S
=
\operatorname{span}_{\mathbb R}
\left\{
F\operatorname{diag}(x)F^\dagger,\,
RF\operatorname{diag}(y)F^\dagger R^\dagger:
x,y\in\mathbb R^d
\right\}.
\]

If \(K\in\mathcal S\) has a computational vector \(e_r\) as an eigenvector
with eigenvalue \(\kappa\), put \(s=\min(r,d-1-r)\).  Then, after grouping
the first \(s\), middle \(d-2s\), and last \(s\) coordinates,

\[
K-\kappa I
=
\begin{pmatrix}
0&0&T\\
0&0&0\\
T^\dagger&0&0
\end{pmatrix},
\]

where \(T\) is an \(s\times s\) upper-triangular Toeplitz matrix.  Hence
either \(K=\kappa I\), or the spectrum of \(K-\kappa I\) contains a nonzero
pair \(\pm\sigma\).  In the latter case \(\kappa\) is neither a maximal nor
a minimal eigenvalue.

For completeness, write \(K=C+RC'R^\dagger\), with \(C,C'\) Hermitian
circulants and

\[
C_{jk}=c_{[j-k]},\qquad C'_{jk}=c'_{[j-k]}.
\]

The eigenvector equations in column \(r\) are

\[
c_m+\rho^{\nu_r(m)}c'_m=0,
\]

where \(\nu_r(m)\in[-r,d-1-r]\) is congruent to \(m\pmod d\).  Comparing
this equation with its Hermitian conjugate forces

\[
c_m=c'_m=0
\quad\text{unless}\quad
m\in\{1,\ldots,s\}\cup\{d-s,\ldots,d-1\}.
\]

For the surviving modes, the ordinary and wrapped matrix diagonals cancel
except in the upper-right and lower-left \(s\times s\) corners, giving the
displayed block form.  Its nonzero eigenvalues are the pairs
\(\pm\sigma_j(T)\).

Now consider any separately bounded third-setting term

\[
\mathcal L=\sum_bK_b\otimes Q_b,
\qquad K_b\in\mathcal S,
\]

where \(\{Q_b\}\) is Bob's third PVM.  To attain a coefficientwise spectral
bound with the maximally entangled state and the computational Bob basis,
the corresponding computational vector would have to be a maximal
eigenvector of every \(K_b\).  The theorem makes this impossible unless all
relevant \(K_b\) are scalar, in which case the term imposes no measurement
constraint.  Since the computational basis is mutually unbiased to both
standard Alice bases, this rules out the most natural MUB repair even when
arbitrary real coefficients from both original Alice PVMs are allowed.

This is a no-go only for the separately bounded local-spectral route.  It
does not rule out a genuinely joint SOS, a different mutually unbiased
third basis, or a different two-input self-test.

## 6. Polar-linear permutation-blindness theorem

Fix complex coefficients \(\alpha_r,\beta_r\) and put

\[
g_r(z)=\alpha_r+\beta_rz,\qquad
f(z)=\sum_r|g_r(z)|,\qquad
M=\max_{|z|=1}f(z).
\]

Assume unit phases \(z_0,\ldots,z_{d-1}\) satisfy:

- \(f(z_j)=M\) for every \(j\);
- \(\prod_jz_j=1\);
- for each \(r\), phases \(s_r(z_j)\) can be chosen with
  \(s_r(z_j)|g_r(z_j)|=g_r(z_j)\) and
  \(\prod_js_r(z_j)=1\).

The last formulation includes singular values \(g_r(z_j)=0\), where the
unitary polar-extension phase is free.

For the score

\[
\mathcal J
=
\sum_r\operatorname{Re}
\bigl[(\alpha_rA_0+\beta_rA_1)\otimes B_r\bigr]
+\operatorname{Re}(A_0\otimes B_*),
\]

the arbitrary-unitary upper bound is \(M+1\). Every permutation \(\kappa\)
of the \(z_j\) gives an order-\(d\) maximizer by setting

\[
A_0=X,\quad
A_1=X\operatorname{diag}(z_{\kappa_j}),\quad
B_r=\overline{X\operatorname{diag}(s_r(z_{\kappa_j}))},\quad
B_*=X.
\]

All first-harmonic data used by the score are permutation invariant. For the
target \((A_1,B_*)\), put \(q_0=1\),
\(q_{j+1}=z_{\kappa_j}q_j\), and
\(\widehat q_m=\sum_jq_j\omega^{mj}\). Then

\[
p_\kappa(a,b|1,*)
=
\frac{|\widehat q_{-(a+b)}|^2}{d^3}.
\]

Therefore the score cannot certify maximal global randomness whenever an
admissible permutation has nonconstant Fourier magnitudes. Permutation
freedom alone is insufficient: special cases can remain Fourier-flat.
