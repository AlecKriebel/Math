# Structural results

The claims ledger records which statements have received an independent
derivation or finite check.  These results remain unreviewed mathematics.

## 1. Exact one-wing one-input impossibility

Let \(p(a,b|y)\) be any finite-dimensional quantum behavior in which Alice
has exactly one \(d\)-outcome input and Bob has finitely many
\(d\)-outcome inputs.  Nonsignalling makes
\(p(a)=\sum_b p(a,b|y)\) independent of \(y\).  For \(p(a)>0\), put
\[
r_y(b|a)=\frac{p(a,b|y)}{p(a)};
\]
choose an arbitrary distribution for a zero-probability \(a\).  Define
\[
\lambda=(a,b_1,\ldots,b_{m_B}),\qquad
\mu(\lambda)=p(a)\prod_y r_y(b_y|a).
\]
Alice outputs \(a\), while Bob outputs the stored \(b_y\) on input \(y\).
Marginalizing the unused \(b_{y'}\)'s reproduces every \(p(a,b|y)\).

This deterministic local model has a pure projective realization
\[
|\Psi'\rangle
=
\sum_\lambda\sqrt{\mu(\lambda)}
|\lambda\rangle_A|\lambda\rangle_B|\lambda\rangle_E,
\]
with Alice's and Bob's PVMs grouping computational labels according to
\(a\) and \(b_y\).  Eve measures the same label and guesses both outputs
perfectly.  Hence
\[
G(AB|0,y,E)=1
\]
for every \(y\).  The symmetric statement holds if Bob has one input and
Alice has arbitrarily many.

Thus \(m_A,m_B\geq2\) is necessary for any private randomness at all, even
when the complete behavior, rather than only one score, is known.  This is
the standard fact that a bipartite nonsignalling behavior with one input on
one wing is local.  It must not be confused with using one designated
generation setting per party inside a larger Bell test.

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

Fix \(d\geq2\), a finite coefficient index set, and complex numbers
\(\alpha_r,\beta_r\).  Put

\[
g_r(z)=\alpha_r+\beta_rz,\qquad
f(z)=\sum_r|g_r(z)|,\qquad
M=\max_{|z|=1}f(z).
\]

For arbitrary unitaries define

\[
\mathcal J
=
\sum_r\operatorname{Re}
\bigl[(\alpha_rA_0+\beta_rA_1)\otimes B_r\bigr]
+\operatorname{Re}(A_0\otimes B_*).
\]

Let \(U=A_0^\dagger A_1\),
\(C_r=A_0g_r(U)=V_r|C_r|\) be the canonical polar decomposition, and set

\[
\begin{aligned}
P_r&=
|C_r^\dagger|^{1/2}\otimes I
-V_r|C_r|^{1/2}\otimes B_r,\\
G&=MI-f(U),\\
R_*&=I-A_0\otimes B_*.
\end{aligned}
\]

Because \(g_r(U)\) is normal,

\[
|C_r|=|g_r(U)|,\qquad
|C_r^\dagger|=A_0|g_r(U)|A_0^\dagger.
\]

Functional calculus gives \(G\geq0\), and the exact positive-factor
certificate is

\[
\boxed{
(M+1)I-\mathcal J
=
\frac12\sum_rP_r^\dagger P_r
+\frac12R_*^\dagger R_*
+\frac12\bigl(G+A_0GA_0^\dagger\bigr)\otimes I.
}
\]

The polar identity remains valid when \(C_r\) is singular, with \(V_r\) a
partial isometry.  Thus \(\mathcal J\leq(M+1)I\) for arbitrary unitaries,
without finite-order assumptions.

Now let \(\omega=e^{2\pi i/d}\), let
\(X|j\rangle=|j+1\bmod d\rangle\), and suppose there are labeled phases
\(z_j,s_{rj}\in\mathbb T\) such that

\[
f(z_j)=M,\qquad
\prod_jz_j=1,
\]

\[
s_{rj}|g_r(z_j)|=g_r(z_j),\qquad
\prod_js_{rj}=1.
\]

If \(g_r(z_j)=0\), the corresponding \(s_{rj}\) is a freely chosen unitary
polar-extension phase.  The labels matter: a permutation moves each paired
datum \((z_j,(s_{rj})_r)\).

For every permutation \(\kappa\), define

\[
Z_\kappa=\operatorname{diag}(z_{\kappa_j}),\qquad
S_{r,\kappa}=\operatorname{diag}(s_{r,\kappa_j}),
\]

\[
A_0=X,\quad
A_1=XZ_\kappa,\quad
B_r=\overline{XS_{r,\kappa}},\quad
B_*=X,
\]

where the bar is taken in the displayed computational basis.  With

\[
|\Phi_d\rangle=d^{-1/2}\sum_j|j,j\rangle,
\]

this is a maximizing strategy satisfying \(O^d=I\) for every observable.
Indeed,

\[
\bigl(X\operatorname{diag}(t_j)\bigr)^d
=
\left(\prod_jt_j\right)I,
\]

and

\[
C_r
=
X\operatorname{diag}(g_r(z_{\kappa_j}))
=
XS_{r,\kappa}
\operatorname{diag}(|g_r(z_{\kappa_j})|).
\]

The maximally entangled trace identity gives value \(M+1\).

More strongly, the entire first-harmonic correlator matrix is permutation
invariant:

\[
\langle A_0\otimes B_r\rangle
=
\frac1d\sum_j\overline{s_{rj}},
\qquad
\langle A_1\otimes B_r\rangle
=
\frac1d\sum_jz_j\overline{s_{rj}},
\]

\[
\langle A_0\otimes B_*\rangle=1,\qquad
\langle A_1\otimes B_*\rangle=\frac1d\sum_jz_j.
\]

All local first moments vanish.  This invariance does not extend in general
to higher harmonics or the full behavior.

Use the spectral convention
\(O=\sum_a\omega^a\Pi_a\).  At the target \((A_1,B_*)\), set

\[
q_0=1,\qquad
q_{j+1}=z_{\kappa_j}q_j,\qquad
\widehat q_m=\sum_jq_j\omega^{mj}.
\]

The product condition gives \(q_d=q_0\), and a direct eigenvector
calculation yields

\[
p_\kappa(a,b|1,*)
=
\frac{|\widehat q_{-(a+b)}|^2}{d^3}.
\]

Parseval gives \(\sum_m|\widehat q_m|^2=d^2\).  Therefore, if the Fourier
magnitudes are nonconstant, the same trivial-Eve maximizer has

\[
G(AB|1,*,E)
\geq
\frac{\max_m|\widehat q_m|^2}{d^3}
>
\frac1{d^2}.
\]

This is an exact no-go for Bell-value or first-harmonic-conditioned maximal
randomness under the displayed hypotheses.  Permutation freedom alone is
not sufficient: all orderings remain Fourier-flat in some small cases.

The cyclic family is the special case

\[
g_y(z)=1+\omega^yz,\qquad
z_k=\exp\!\left(\frac{\pi i(2k+\delta_d)}d\right),
\quad
\delta_d=
\begin{cases}
0,&d\ \text{odd},\\
1,&d\ \text{even}.
\end{cases}
\]

Here

\[
\prod_kz_k=1,\qquad
\prod_k(1+\omega^yz_k)=2>0,
\]

so every hypothesis holds with the nonsingular polar phases.  Swapping the
last two roots gives nonconstant Fourier magnitudes for every \(d\geq4\);
for \(d=2,3\), every root ordering remains flat.

## 7. The second cyclic family has the same obstruction

The phase permutation also survives the exact SOS of the second family
\(\mathcal F_d\) in arXiv:2606.21362.

Let

\[
\eta=e^{\pi i/d},\qquad
\delta=
\begin{cases}
0,&d\ \text{odd},\\
1,&d\ \text{even},
\end{cases}
\qquad
z_r=\eta^{2r+\delta}.
\]

For a permutation \(\kappa\), retain the first-family Bob observables

\[
B_y
=
\overline{
X\operatorname{diag}
\left(
\frac{1+\omega^yz_{\kappa_j}}
{|1+\omega^yz_{\kappa_j}|}
\right)_j
}.
\]

Define their Fourier transforms

\[
C_\ell=\sum_{y=0}^{d-1}\omega^{\ell y}B_y.
\]

With

\[
\lambda_\ell=\lambda_{0,\ell-1}
\]

in the originating paper's indexing, a finite geometric-sum calculation
gives the exact identity

\[
C_\ell=d\lambda_\ell D_\ell,
\]

where

\[
D_\ell
=
q_\ell X\operatorname{diag}(\omega^{-\ell\kappa_j}),
\qquad
q_\ell=\eta^{-\ell(\ell-1+\delta)}.
\]

One direct derivation uses

\[
s_0(z_r)
=
\varepsilon_r\eta^{r+\delta/2},
\qquad
\varepsilon_r=
\begin{cases}
+1,&2r+\delta<d,\\
-1,&2r+\delta>d,
\end{cases}
\]

and

\[
s_y(z_r)=s_0(z_{r+y\bmod d}).
\]

Hence

\[
\sum_y\omega^{\ell y}\overline{s_y(z_r)}
=
\omega^{-\ell r}
\sum_t\omega^{\ell t}\overline{s_0(z_t)}.
\]

Evaluating the two geometric blocks produces

\[
\sum_t\omega^{\ell t}\overline{s_0(z_t)}
=
d\lambda_\ell q_\ell.
\]

Every \(D_\ell\) is unitary and satisfies the \(d\)-th-power relation.
Indeed, \(\sum_j\kappa_j=d(d-1)/2\), so

\[
D_\ell^d
=
q_\ell^d
\omega^{-\ell\sum_j\kappa_j}I
=
(-1)^{
\ell(\ell-1+\delta)+\ell(d-1)
}I
=I.
\]

The last exponent is even: \(d-2+\delta\) is odd, so
\(\ell(\ell+d-2+\delta)\) is even.

Now define all \(d\) Alice observables by

\[
A_\ell=\overline{D_\ell}.
\]

The second-family Bell functional and SOS factors are

\[
\mathcal F_d
=
\frac12\sum_\ell
\lambda_\ell^*A_\ell\otimes C_\ell+\mathrm{h.c.},
\]

\[
P_\ell=d\lambda_\ell I-A_\ell\otimes C_\ell,
\qquad
dI-\mathcal F_d
=
\frac1{2d}\sum_\ell P_\ell^\dagger P_\ell.
\]

Since

\[
(\overline{D_\ell}\otimes D_\ell)|\Phi_d\rangle
=
|\Phi_d\rangle,
\]

every \(P_\ell\) annihilates \(|\Phi_d\rangle\).  Thus every permutation
attains the exact value

\[
\langle\mathcal F_d\rangle=d.
\]

Adding \(B_d=X=\overline{A_0}\) saturates the extra Hermitian correlation
term and gives the exact augmented value \(d+1\).

Crucially,

\[
A_0=X,\qquad
A_1
=
X\operatorname{diag}(z_{\kappa_j}).
\]

Therefore the target pair \((A_1,B_d)\) is literally the same target pair
as in Section 6, with

\[
p_\kappa(a,b|1,d)
=
\frac{|\widehat q_{-(a+b)}|^2}{d^3}.
\]

For the final-two swap, this table is nonuniform for every \(d\geq4\).
Consequently the augmented second family also fails to certify
\(2\log_2d\) bits from its maximal Bell score in those dimensions, even
with trivial Eve.  This does not challenge the private randomness of the
canonical full behavior, and \(d=3\) remains Fourier-flat, consistently
with the known qutrit self-test.

The quantitative lower bound from Section 6 carries over unchanged:

\[
G(AB|1,d,E)
\geq
\frac1{d^2}
+
\frac{2\sin(\pi/d)\sin(3\pi/d)}{d^2(d-1)}
>
\frac1{d^2}
\qquad(d\geq4).
\]

At \(d=4\), the exact table is

\[
p(a,b|1,4)=
\begin{cases}
1/32,&a+b\ \text{even},\\
3/32,&a+b\ \text{odd},
\end{cases}
\]

so the actual trivial-Eve guessing probability is \(3/32>1/16\).

## 8. Resource-law status

The results above do not determine the minimum all-dimensional setting
pair.  They establish:

\[
m_A\geq2,\qquad m_B\geq2
\]

for every protocol, even one conditioned on the full behavior; exact
attainment by \(2\times2\) when \(d=2\); and no-go results for several
natural all-dimensional constructions when \(d\geq3\).  The targeted
literature audit located a rigorous \(2\times(d^2+1)\) all-dimensional
single-score construction, but no \(2\times2\) or \(2\times3\) construction
and no stronger universal lower bound.

Accordingly, for \(d\geq3\), both

\[
(2,2)\in\mathfrak M_d
\quad\text{and}\quad
(2,3)\in\mathfrak M_d
\]

remain open here.  The exact obstruction in Section 6 is class-specific and
must not be promoted to a universal \(2\times2\) impossibility theorem.
