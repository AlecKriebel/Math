# A four-strand obstruction to restrictable exceptional solutions

**Date:** 2026-07-29

**Status:** PROVED

**Scope:** arbitrary solutions in the balanced exceptional class; no
Pauli, sparsity, scalar-cross, irreducibility, or separate preservation of
the two mixed-color cells is assumed

## 1. Main result

Put
\[
q=e^{i\pi/3},\qquad
R=qI-(1+q)P,
\]
where \(P\) is an orthogonal projection of rank \(d^2/2\), and suppose
that \(R\) satisfies the braid-form Yang--Baxter equation.  Thus the
tensor-space representation has Markov parameter
\[
\eta=\frac{\operatorname{rank}P}{d^2}=\frac12.
\]
Here the Markov conclusion is not being inferred from the two-strand
rank alone: it is the automatic Markov theorem for unitary
two-eigenvalue \(R\)-matrices with no opposite eigenvalues (Lechner,
Proposition 2.4 and Lemma 3.1), already audited for the full matrix
class in `notes/track_hecke_multiplicity.md`.

Call a subspace \(0\ne W\subseteq V\) **square-invariant** when
\[
R(W\otimes W)\subseteq W\otimes W. \tag{1}
\]
Since \(R\) is unitary, this invariant subspace is automatically
reducing.  Let
\[
R_W=R|_{W\otimes W},\qquad r=\dim W.
\]

> **Theorem 1 (automatic balance of square restrictions).**
> Every square-invariant subspace has even dimension, and
> \[
> R_W\in[e^{i\pi/3},1/2,r].
> \]
> In particular, \(R_W\) is non-scalar and the \((-1)\)-spectral
> projection of \(R_W\) has rank \(r^2/2\).

The theorem uses a four-strand obstruction.  It does not inspect the
mixed sector
\[
(W\otimes W^\perp)\oplus(W^\perp\otimes W)
\]
at all.

Recall that an \(R\)-matrix is restrictable in the sense of
Conti--Lechner when there is a proper nonzero \(W\subset V\) for which
both \(W^{\otimes2}\) and \((W^\perp)^{\otimes2}\) are invariant.
Theorem 1 gives the following consequences.

> **Corollary 2 (restrictable descent).**
> If an exceptional solution of dimension \(d\equiv2\pmod4\) is
> restrictable, both diagonal restrictions are smaller balanced
> exceptional solutions of even dimensions \(r\) and \(d-r\).  Exactly
> one of these dimensions is congruent to \(2\pmod4\).
>
> Consequently, a least-dimensional solution in the unresolved
> congruence class \(d\equiv2\pmod4\) must be non-restrictable.

> **Corollary 3 (dimension-six no-go).**
> No dimension-six exceptional solution is restrictable.

Indeed, a restrictable split of dimension six would have two even
parts.  Up to order it must be \(2+4\), and the balanced exceptional
class in dimension two is empty.  In particular, the genuine
\(3+3\) qutrit-gluing branch is impossible even if the operator on
\[
(A\otimes B)\oplus(B\otimes A)
\]
is completely arbitrary and mixes the two displayed summands.

This is not an unrestricted dimension-six nonexistence theorem.
It proves that any hypothetical dimension-six witness must be
non-restrictable.

## 2. Generator convention and the two four-strand projectors

Use Hecke generators \(g_i\) with
\[
(g_i-q)(g_i+1)=0,
\qquad
g_i^2=(q-1)g_i+q. \tag{2}
\]
For \(w\in S_4\), let \(g_w\) be the product along any reduced word and
let \(\ell(w)\) be its Coxeter length.  Define
\[
\begin{aligned}
A_+&=\sum_{w\in S_4}g_w,
&
c_+&=\sum_{w\in S_4}q^{\ell(w)},\\
A_-&=\sum_{w\in S_4}(-q^{-1})^{\ell(w)}g_w,
&
c_-&=\sum_{w\in S_4}q^{-\ell(w)}.
\end{aligned} \tag{3}
\]
Because \(q\) has order six and the largest relevant quantum factorial
is the fourth, \(c_+\) and \(c_-\) are nonzero.  The multiplication rule
in (2) gives
\[
g_iA_+=A_+g_i=qA_+,\qquad
g_iA_-=A_-g_i=-A_-. \tag{4}
\]
It follows that
\[
e_+=c_+^{-1}A_+,\qquad e_-=c_-^{-1}A_- \tag{5}
\]
are the central idempotents for the one-dimensional representations
\[
g_i\longmapsto q,\qquad g_i\longmapsto-1, \tag{6}
\]
respectively.  In every unitary Hecke representation, their images are
the orthogonal projections onto the simultaneous \(q\)- and
\((-1)\)-eigenspaces of \(g_1,g_2,g_3\).

The idempotent \(e_+\) is the four-strand \(q\)-symmetrizer and \(e_-\)
is the four-strand \(q\)-antisymmetrizer.

## 3. Exact Markov-trace calculation

Let \(\mu_\eta\) be the normalized tensor-space Markov trace with
\[
\mu_\eta(P_i)=\eta.
\]
In the convention (2), its generator parameter is
\[
z:=\mu_\eta(g_i)=q-(1+q)\eta. \tag{7}
\]
Repeated use of cyclicity and the Markov rule, or a direct reduction of
the 24 basis elements in (3), gives
\[
\mu_\eta(e_+)
=
\frac{
(z+1)((q+1)z+1)((q^2+q+1)z+1)}
{(q+1)^2(q^2+1)(q^2+q+1)}, \tag{8}
\]
and
\[
\mu_\eta(e_-)
=-
\frac{
(z-q)((q+1)z-q^2)((q^2+q+1)z-q^3)}
{(q+1)^2(q^2+1)(q^2+q+1)}. \tag{9}
\]
Using
\[
q^2-q+1=0 \tag{10}
\]
and substituting \(z=q-(1+q)\eta\) reduces the two traces for arbitrary
\(\eta\) to
\[
\boxed{
\mu_\eta(e_+)
=\frac{(1-\eta)(2-3\eta)(1-2\eta)}2,
\qquad
\mu_\eta(e_-)
=\frac{\eta(3\eta-1)(2\eta-1)}2.
} \tag{11}
\]
In particular,
\[
\begin{array}{c|cc}
\eta&\mu_\eta(e_+)&\mu_\eta(e_-)\\ \hline
0&1&0\\
\frac13&\frac19&0\\
\frac12&0&0\\
\frac23&0&\frac19\\
1&0&1.
\end{array} \tag{12}
\]

Thus the balanced exceptional quotient kills both one-dimensional
four-strand blocks:
\[
\rho^{(1/2)}_4(e_+)=\rho^{(1/2)}_4(e_-)=0. \tag{13}
\]
This conclusion follows directly from (12): the images are orthogonal
projections, the normalized matrix trace is faithful, and both traces
vanish.

More strongly, the two polynomials in (11) have the unique common zero
\[
\eta=\frac12. \tag{14}
\]
Thus simultaneous annihilation of both idempotents forces balance
without first invoking the classification of positive Hecke Markov
traces.  For reference, a positive Markov trace with parameter \(1/3\)
sees a nonzero \(q\)-symmetrizer, while parameter \(2/3\) sees a nonzero
\(q\)-antisymmetrizer.  In a local dimension-three realization, their
ordinary ranks are
\[
3^4\cdot\frac19=9. \tag{15}
\]
The scalar parameters \(0\) and \(1\) see the full trivial and sign
representations, respectively.

In Wenzl's notation, four strands is the first level giving the
simultaneous separation needed here:

- \(H_4(3,6)\) excludes both \((4)\) and \((1^4)\);
- \(H_4(2,6)\) retains \((4)\);
- \(H_4(4,6)\) retains \((1^4)\).

Equations (8)--(11) make the needed separation independent of this
diagrammatic description.

## 4. Proof of Theorem 1

Condition (1) implies
\[
R_i(W^{\otimes n})\subseteq W^{\otimes n}
\qquad(1\le i<n) \tag{16}
\]
for every \(n\).  Hence the entire tensor-space Hecke representation on
\(W^{\otimes n}\) is the restriction of the ambient representation.
In particular, the ambient relations (13) remain true after restriction:
\[
\rho^W_4(e_+)=\rho^W_4(e_-)=0. \tag{17}
\]

The matrix \(R_W\) is unitary, satisfies (2), and satisfies the
Yang--Baxter equation on \(W^{\otimes3}\).  Lechner's
no-opposite-eigenvalue theorem makes its normalized tensor-space trace
a Markov trace, including in either scalar case.  Put
\[
\eta_W
:=
\frac{\dim\ker(R_W+I)}{r^2}
\in[0,1]. \tag{18}
\]
Because both idempotents vanish as operators in (17), their faithful
normalized matrix traces vanish.  Applying the arbitrary-parameter
factorizations (11), their unique common zero (14) gives
\[
\eta_W=\frac12. \tag{19}
\]
Its negative spectral multiplicity is \(r^2/2\), which is integral only
if \(r\) is even.  In particular, \(R_W\) is non-scalar.  This proves
Theorem 1.

Notice that no trace-propagation assumption was made from the two-strand
rank alone.  The Markov property for \(R_W\) is supplied independently
by the unitary no-opposite-eigenvalue theorem, and the ambient
four-strand annihilation is inherited because \(W^{\otimes n}\) is an
actual invariant tensor subspace at every level.

## 5. The dimension-six \(3+3\) branches before the obstruction

This section records the complete branch bookkeeping, to guard against
silently assuming that the mixed block preserves \(A\otimes B\) and
\(B\otimes A\) separately.

Let
\[
V=A\oplus B,\qquad \dim A=\dim B=3,
\]
and suppose \(R\) preserves \(A^{\otimes2}\), \(B^{\otimes2}\), and
\[
\mathcal M=(A\otimes B)\oplus(B\otimes A). \tag{20}
\]
Let \(P=(qI-R)/(1+q)\), and write
\[
a=\operatorname{rank}(P|_{A^{\otimes2}}),\qquad
b=\operatorname{rank}(P|_{B^{\otimes2}}).
\]
The scalar cases and Lechner's rank list give
\[
a,b\in\{0,3,6,9\}. \tag{21}
\]

Write the mixed projection relative to (20) as
\[
P_{\mathcal M}
=
\begin{pmatrix}
X&Y\\
Y^*&Z
\end{pmatrix}, \tag{22}
\]
where no condition makes \(Y\) vanish.  Automatic standardness of the
ambient solution gives
\[
\operatorname{Tr}_1P=\operatorname{Tr}_2P=3I_6. \tag{23}
\]
The off-diagonal block \(Y\) has zero partial trace because its input and
output have orthogonal colors on the contracted leg.  Taking the traces
of the four diagonal color compressions of (23) gives
\[
a+\operatorname{Tr}X=9,\qquad
b+\operatorname{Tr}Z=9,\qquad
a+\operatorname{Tr}Z=9,\qquad
b+\operatorname{Tr}X=9. \tag{24}
\]
Consequently
\[
a=b,\qquad
\operatorname{rank}P_{\mathcal M}=18-2a. \tag{25}
\]
The four branches are therefore
\[
\begin{array}{c|c}
a=b&\operatorname{rank}P_{\mathcal M}\\ \hline
0&18\\
3&12\\
6&6\\
9&0.
\end{array} \tag{26}
\]

The middle two rows are precisely the genuine qutrit \(1/3\) and
\(2/3\) diagonal branches, with an arbitrary rank-12 or rank-6
projection on the full 18-dimensional mixed sum.  Theorem 1 eliminates
all four rows from the diagonal restriction alone.  In particular, it
does not matter whether \(Y\) in (22) is zero.

## Appendix A. Complete operator-valued mixed-color braid equations

Although the four-strand obstruction makes these equations unnecessary
for the no-go theorem, they specify exactly the discarded search space.

Write
\[
T=R|_{A^{\otimes2}},\qquad
S=R|_{B^{\otimes2}},
\]
and decompose the completely arbitrary mixed operator as
\[
C=R|_{\mathcal M}
=
\begin{pmatrix}
X&Y\\ Z&U
\end{pmatrix}
:
\begin{matrix}
A\otimes B\\ \oplus\\ B\otimes A
\end{matrix}
\longrightarrow
\begin{matrix}
A\otimes B\\ \oplus\\ B\otimes A.
\end{matrix} \tag{27}
\]
Rows are output cells and columns are input cells.  Thus, for example,
\(Y:B\otimes A\to A\otimes B\).

The monochromatic braid equations are the Yang--Baxter equations for
\(T\) and \(S\).  On
\[
\mathcal K_A
=(AAB)\oplus(ABA)\oplus(BAA), \tag{28}
\]
the two adjacent generators are
\[
L_A=
\begin{pmatrix}
D&0&0\\
0&A_0&B_0\\
0&C_0&E_0
\end{pmatrix},
\qquad
M_A=
\begin{pmatrix}
x&y&0\\
z&u&0\\
0&0&F
\end{pmatrix}, \tag{29}
\]
where the typed maps are
\[
\begin{array}{lll}
D=T\otimes I_B,&
A_0=X\otimes I_A,&B_0=Y\otimes I_A,\\
C_0=Z\otimes I_A,&E_0=U\otimes I_A,&
F=I_B\otimes T,\\
x=I_A\otimes X,&y=I_A\otimes Y,&
z=I_A\otimes Z,\quad u=I_A\otimes U.
\end{array} \tag{30}
\]
The complete \(AAB\)-orbit equation \(L_AM_AL_A=M_AL_AM_A\)
is the following set of nine operator identities:
\[
\begin{array}{rcl}
DxD&=&xDx+yA_0z,\\
DyA_0&=&xDy+yA_0u,\\
DyB_0&=&yB_0F,\\
A_0zD&=&zDx+uA_0z,\\
A_0uA_0+B_0FC_0&=&zDy+uA_0u,\\
A_0uB_0+B_0FE_0&=&uB_0F,\\
C_0zD&=&FC_0z,\\
C_0uA_0+E_0FC_0&=&FC_0u,\\
C_0uB_0+E_0FE_0&=&FE_0F.
\end{array} \tag{31}
\]
All products in (31) are compositions of the typed maps in (30).

The nine equations on
\[
\mathcal K_B
=(BBA)\oplus(BAB)\oplus(ABB) \tag{32}
\]
are the color-reversed copy of (31), under
\[
A\leftrightarrow B,\qquad
T\leftrightarrow S,\qquad
X\leftrightarrow U,\qquad
Y\leftrightarrow Z. \tag{33}
\]
Together with
\[
C^*C=CC^*=I_{\mathcal M},\qquad
(C+I)(C-qI)=0, \tag{34}
\]
the analogous local conditions for \(T,S\), the two monochromatic braid
equations, and (31) plus its color reversal, these are the full equations.
They allow all operator-valued diagonal and off-diagonal mixed blocks.

## Appendix B. Exact replay

Run

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_restrictable_four_strand_obstruction.py
```

The verifier uses exact arithmetic to:

1. construct the 24-dimensional Hecke algebra \(H_4(q)\);
2. verify the two idempotents (5) and their generator eigenrelations;
3. derive the Markov-trace formulas (8) and (9) from the defining trace
   and Markov equations;
4. derive the arbitrary-parameter factorizations (11), their unique
   common zero, and every entry of (12);
5. verify the nine free operator-word equations (31);
6. replay the dimension-six branch and descent arithmetic.

The verifier does not assume a Gaussian normal form for the qutrit
restrictions.
