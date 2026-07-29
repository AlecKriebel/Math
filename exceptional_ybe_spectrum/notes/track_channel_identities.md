# Track A3: canonical completely positive channels

**Date:** 2026-07-28

**Scope:** arbitrary exceptional projection unless a subsection is explicitly
labelled exact \(d=4\), numerical, or an abstract channel countermodel
**Status:** several universal identities proved; channel commutation remains
an audited conjecture, not a theorem

## Executive conclusion

Let \(P\in\operatorname{End}(V\otimes V)\) be an arbitrary exceptional
projection, \(\dim V=d\).  Automatic standardness gives

\[
\operatorname{Tr}_1P=\operatorname{Tr}_2P=\frac d2I.
\tag{1}
\]

Define

\[
\mathcal E_R(X)=\frac2d\operatorname{Tr}_2
 \bigl(P(X\otimes I)P\bigr),\qquad
\mathcal E_L(X)=\frac2d\operatorname{Tr}_1
 \bigl(P(I\otimes X)P\bigr).
\tag{2}
\]

The following statements are exact and universal:

1. \(\mathcal E_R,\mathcal E_L\) are completely positive, unital,
   trace-preserving, Hilbert--Schmidt self-adjoint, and positive as
   superoperators.  Their spectra lie in \([0,1]\).
2. Their fixed algebras are exactly the one-leg commutants of \(P\).
3. Their superoperator traces are both \(d^2/2\).
4. They satisfy the crossed tensor eigen-relations
   \[
   (\operatorname{id}\otimes\mathcal E_R)(H)=\frac13H,\qquad
   (\mathcal E_L\otimes\operatorname{id})(H)=\frac13H,
   \tag{3}
   \]
   where \(H=I-2P\).
5. Every right operator-Schmidt vector of \(H\) is a \(1/3\)-eigenvector
   of \(\mathcal E_R\), and every left operator-Schmidt vector is a
   \(1/3\)-eigenvector of \(\mathcal E_L\).
6. If \(r\) is the operator-Schmidt rank of \(H\), then
   \[
   r\leq\frac{3d^2}{4}.
   \tag{4}
   \]
7. The stronger affine transforms
   \[
   \mathcal F_R=2\mathcal E_R-\operatorname{id},\qquad
   \mathcal F_L=2\mathcal E_L-\operatorname{id}
   \]
   are completely positive, bistochastic, and Hilbert--Schmidt
   self-adjoint.  They have superoperator trace zero and admit Kraus
   representations by traceless Hermitian Hilbert--Schmidt orthogonal
   operators.

The consequences that can be formulated solely in terms of the one-site
channels do **not** force \(4\mid d\).  There is an exact abstract \(d=6\)
pair satisfying all of those scalar, spectral, affine-CP, and
Schmidt-support constraints, as well as every stronger joint-channel pattern
observed in the \(d=4\) data, with spectrum

\[
\{1^{\,1},(2/3)^{\,16},(1/3)^{\,19}\}.
\tag{5}
\]

This abstract channel pair is not claimed to come from a projection.
It also satisfies the two universal affine complete-positivity constraints
\(2\mathcal E-I\) and \((3\mathcal E-I)/2\).  It proves that channel spectral
multiplicities, commutation, left/right isospectrality, ergodicity, these
affine CP constraints, and the observed paired polynomial alone cannot
exclude \(d=6\).

More sharply, its canonical identity Schmidt pairing produces an exact
Hermitian trace-zero matrix \(H_0\) satisfying the target three-site cubic,
but

\[
3H_0^2+2\sqrt3\,H_0-3I=0,
\qquad
\sigma(H_0)=\{(-\sqrt3)^9,(1/\sqrt3)^{27}\}.
\]

Thus the strengthened channel route reaches the cubic variety in dimension
six and fails precisely at involutivity.  No affine transformation repairs
this while preserving trace zero.

The two channels commute for the published sparse witness and for the exact
one-parameter color/face family.  Three independently retained numerical
\(d=4\) points also commute to errors around \(10^{-12}\) and have matching
left/right spectra.  All these examples also satisfy a stronger
joint-channel polynomial displayed in Section 7.  Nevertheless, no general
proof from the cubic relation has been obtained.  Standardness by itself is
insufficient: an exact rational standard projection with noncommuting
channels is given in Section 8.  Accordingly,

\[
[\mathcal E_L,\mathcal E_R]=0
\tag{6}
\]

and the stronger isospectral/polynomial patterns are recorded as
**SPECULATION supported by exact families and numerical evidence**, not as
universal theorems.

## 1. Positivity, self-adjointness, and the Dirichlet identity

Equip \(M_d\) with

\[
\langle X,Y\rangle=\operatorname{Tr}(X^*Y).
\]

Complete positivity of (2) follows by composing the completely positive
maps

\[
X\longmapsto X\otimes I,\qquad
A\longmapsto PAP,\qquad
A\longmapsto\operatorname{Tr}_i A.
\]

Equation (1) and \(P^2=P\) give

\[
\mathcal E_R(I)=\mathcal E_L(I)=I.
\]

Cyclicity of the full trace gives, for example,

\[
\begin{aligned}
\operatorname{Tr}\mathcal E_R(X)
&=\frac2d\operatorname{Tr}\bigl(P(X\otimes I)P\bigr)\\
&=\frac2d\operatorname{Tr}\bigl((X\otimes I)P\bigr)
=\operatorname{Tr}X.
\end{aligned}
\]

Thus both channels are bistochastic.

For \(A=X\otimes I\),

\[
\begin{aligned}
\langle Y,\mathcal E_R(X)\rangle
&=\frac2d\operatorname{Tr}\bigl((Y^*\otimes I)PAP\bigr)\\
&=\frac2d\operatorname{Tr}\bigl(P(Y^*\otimes I)PA\bigr)
=\langle\mathcal E_R(Y),X\rangle.
\end{aligned}
\tag{7}
\]

Hence \(\mathcal E_R\) is Hilbert--Schmidt self-adjoint.  Moreover,

\[
\langle X,\mathcal E_R(X)\rangle
=\frac2d\left\|P(X\otimes I)P\right\|_2^2\geq0.
\tag{8}
\]

The same argument applies to \(\mathcal E_L\).  A bistochastic completely
positive map is a Hilbert--Schmidt contraction by the Schwarz inequality.
Together with (7)--(8), this proves

\[
\sigma(\mathcal E_R),\sigma(\mathcal E_L)\subset[0,1].
\tag{9}
\]

There is also an exact Dirichlet-form identity:

\[
\boxed{
\left\|[P,X\otimes I]\right\|_2^2
=d\langle X,(I-\mathcal E_R)X\rangle.
}
\tag{10}
\]

It follows by expanding the squared commutator, using (1), and recognizing
the two cross terms through (2).  Similarly,

\[
\left\|[P,I\otimes X]\right\|_2^2
=d\langle X,(I-\mathcal E_L)X\rangle.
\tag{11}
\]

Consequently,

\[
\operatorname{Fix}(\mathcal E_R)
=\{X:[P,X\otimes I]=0\},
\tag{12}
\]

\[
\operatorname{Fix}(\mathcal E_L)
=\{X:[P,I\otimes X]=0\}.
\tag{13}
\]

In particular, the fixed spaces are finite-dimensional \(C^*\)-algebras,
not merely operator systems.  This recovers the fixed-reflection observation
used in the color/face search and removes the restriction to reflections.

## 2. Forced superoperator trace

Write \(P\) as a \(d\times d\) block matrix with respect to the second
tensor factor, and put

\[
(K_{bv})_{au}=P_{ab,uv}.
\]

Then

\[
\mathcal E_R(X)=\frac2d\sum_{b,v}K_{bv}XK_{bv}^*.
\tag{14}
\]

For a Kraus map \(X\mapsto KXK^*\), its superoperator trace is
\(\lvert\operatorname{Tr}K\rvert^2\).  Therefore

\[
\begin{aligned}
\operatorname{Tr}_{\mathrm{sup}}(\mathcal E_R)
&=\frac2d\sum_{b,v}\left|\sum_aP_{ab,av}\right|^2\\
&=\frac2d\left\|\operatorname{Tr}_1P\right\|_2^2
=\frac{d^2}{2}.
\end{aligned}
\tag{15}
\]

The other leg gives the same result:

\[
\boxed{
\operatorname{Tr}_{\mathrm{sup}}(\mathcal E_R)
=\operatorname{Tr}_{\mathrm{sup}}(\mathcal E_L)
=\frac{d^2}{2}.
}
\tag{16}
\]

This is the only equality of spectral moments proved here.  Equality of all
moments, or equality of the two characteristic polynomials, is observed in
the exact and numerical \(d=4\) data but has not been proved universally.

## 3. Tensor eigen-relations

Taking the third and first partial traces of

\[
P_{12}P_{23}P_{12}-P_{23}P_{12}P_{23}
=\frac13(P_{12}-P_{23})
\tag{17}
\]

and then inserting (1) gives

\[
\boxed{
(\operatorname{id}\otimes\mathcal E_R)(P)
=(\mathcal E_L\otimes\operatorname{id})(P)
=\frac13(I+P).
}
\tag{18}
\]

Since both channels are unital and \(H=I-2P\), this is equivalent to (3).
Iteration gives, for every \(n\geq0\),

\[
(\operatorname{id}\otimes\mathcal E_R^n)(H)=3^{-n}H,
\qquad
(\mathcal E_L^n\otimes\operatorname{id})(H)=3^{-n}H,
\tag{19}
\]

or, in projection form,

\[
(\operatorname{id}\otimes\mathcal E_R^n)(P)
=\frac12I+3^{-n}\left(P-\frac12I\right),
\tag{20}
\]

with the analogous left formula.

There is a useful exact audit of a tempting isospectrality argument.  In the
row-major matrix-unit basis, define the reshuffling matrix

\[
(\mathscr K_P)_{(b,d),(a,c)}=P_{(a,b),(c,d)}
\]

and define \(\mathscr K_I\) by the same reshuffling of
\(I_{V\otimes V}\).  Reading the two sides of (18) in indices gives

\[
\boxed{
\mathcal E_R\mathscr K_P
=\mathscr K_P\mathcal E_L^{\mathsf T}
=\frac13(\mathscr K_I+\mathscr K_P).
}
\tag{20a}
\]

Thus \(\mathscr K_P\) is indeed an intertwiner between the right channel and
the transpose of the left channel.  It is not, however, an invertible
intertwiner.  If \(r\) is the operator-Schmidt rank of \(H\), then the
vanishing partial traces make the identity Schmidt term orthogonal to all
terms of \(H\), and hence

\[
\operatorname{rank}\mathscr K_P=1+r.
\tag{20b}
\]

The bound (4) makes this strictly smaller than \(d^2\) for every \(d\geq4\).
Equivalently, (20a) controls only the identity and the operator-Schmidt
support already forced into eigenvalues \(1\) and \(1/3\); it cannot by
itself compare the complementary spectra.  This pinpoints why the crossed
tensor relation does not prove the observed full left/right isospectrality.

## 4. Operator-Schmidt consequences

Because both partial traces of \(H\) vanish, \(H\) has a Hermitian
operator-Schmidt decomposition

\[
H=\sum_{\alpha=1}^{r}
\sigma_\alpha A_\alpha\otimes B_\alpha,
\tag{21}
\]

where the \(A_\alpha\) and \(B_\alpha\) are traceless Hermitian
Hilbert--Schmidt orthonormal families and \(\sigma_\alpha>0\).  Equation (3)
and linear independence give

\[
\boxed{
\mathcal E_L(A_\alpha)=\frac13A_\alpha,\qquad
\mathcal E_R(B_\alpha)=\frac13B_\alpha.
}
\tag{22}
\]

Thus

\[
\dim\ker(3\mathcal E_L-I)\geq r,\qquad
\dim\ker(3\mathcal E_R-I)\geq r.
\tag{23}
\]

The same decomposition gives explicit Kraus formulas:

\[
\mathcal E_R(X)
=\frac12X+\frac1{2d}\sum_{\alpha=1}^r
\sigma_\alpha^2A_\alpha XA_\alpha,
\tag{24}
\]

\[
\mathcal E_L(X)
=\frac12X+\frac1{2d}\sum_{\alpha=1}^r
\sigma_\alpha^2B_\alpha XB_\alpha.
\tag{25}
\]

Here \(\sum_\alpha\sigma_\alpha^2=\|H\|_2^2=d^2\).
In particular, the affine transforms

\[
\boxed{
\begin{aligned}
\mathcal F_R&:=2\mathcal E_R-\operatorname{id}
=\frac1d\sum_{\alpha=1}^r
\sigma_\alpha^2A_\alpha(\,\cdot\,)A_\alpha,\\
\mathcal F_L&:=2\mathcal E_L-\operatorname{id}
=\frac1d\sum_{\alpha=1}^r
\sigma_\alpha^2B_\alpha(\,\cdot\,)B_\alpha
\end{aligned}
}
\tag{25a}
\]

are completely positive.  Since the Schmidt operators are traceless
Hermitian and Hilbert--Schmidt orthonormal, (25a) is stronger than merely
requiring an arbitrary CP realization.  Unitality and trace preservation
follow from those properties of \(\mathcal E_R,\mathcal E_L\), and
self-adjointness is immediate from the Hermitian Kraus operators.  Finally,
(16) gives

\[
\operatorname{Tr}_{\rm sup}\mathcal F_R
=\operatorname{Tr}_{\rm sup}\mathcal F_L=0.
\tag{25b}
\]

Let \(n=d^2\).  At least \(r\) of the \(n\) eigenvalues of either channel
equal \(1/3\), all remaining eigenvalues are at most \(1\), and their sum is
\(n/2\).  Hence

\[
\frac n2\leq\frac r3+(n-r),
\]

which proves (4).

## 5. Relation to the reduced unitary channel of \(R\)

Let

\[
q=e^{i\pi/3},\qquad
R=qI-(1+q)P.
\]

The scalar partial trace is

\[
\frac1d\operatorname{Tr}_2R=\frac{q-1}{2}I.
\]

Expanding \(P=(qI-R)/(1+q)\), using
\(\lvert1+q\rvert^2=3\), and taking a partial trace gives

\[
\boxed{
\mathcal E_R
=\frac13\operatorname{id}+\frac23\mathcal U_R,
}
\tag{26}
\]

where

\[
\mathcal U_R(X)=\frac1d\operatorname{Tr}_2
\bigl(R(X\otimes I)R^*\bigr).
\tag{27}
\]

There is an analogous formula on the left.  Thus the reduced dynamics of
the braid gate is Hilbert--Schmidt self-adjoint in this exceptional class,
and

\[
\sigma(\mathcal U_R)\subset[-1/2,1],
\qquad
\operatorname{Tr}_{\mathrm{sup}}(\mathcal U_R)=\frac{d^2}{4}.
\tag{28}
\]

Equation (22) says that \(\mathcal U_R\) annihilates every right
operator-Schmidt vector of \(H\); the left reduced channel annihilates every
left vector.

## 6. Exact \(d=4\) channel spectra

### Published sparse witness

Exact arithmetic gives

\[
[\mathcal E_L,\mathcal E_R]=0
\tag{29}
\]

and

\[
\chi_{\mathcal E_L}(x)=\chi_{\mathcal E_R}(x)
=(x-1)^4(x-1/3)^{12}.
\tag{30}
\]

The operator-Schmidt rank of \(H\) is \(3\).  The two fixed algebras both
have vector-space dimension four, although the separate exact commutant
audit identifies different algebra types:

\[
\operatorname{Fix}(\mathcal E_R)\cong M_2(\mathbb C),\qquad
\operatorname{Fix}(\mathcal E_L)\cong\mathbb C^4
\]

up to the left/right convention used there.

### Exact color/face family

For the family in `scripts/verify_color_face_d4_family.py`, with parameters

\[
s^2+2t^2=1,
\tag{31}
\]

the channels commute identically even before imposing (31).  They have the
same symbolic characteristic polynomial

\[
\frac{(3x-1)^8
(-s^2-2t^2+3x-2)^4
(s^2+2t^2+3x-2)^4}{3^{16}}.
\tag{32}
\]

On (31), equation (32) reduces exactly to (30).

## 7. The unresolved commutation question

Composition of the two channels has a useful three-site expression.  With
\(p=P_{12}\), \(q_0=P_{23}\), and \(X_2=I\otimes X\otimes I\),

\[
(\mathcal E_L\mathcal E_R)(X)
=\frac4{d^2}\operatorname{Tr}_{1,3}
\bigl(pq_0X_2q_0p\bigr),
\tag{33}
\]

\[
(\mathcal E_R\mathcal E_L)(X)
=\frac4{d^2}\operatorname{Tr}_{1,3}
\bigl(q_0pX_2pq_0\bigr).
\tag{34}
\]

Therefore universal commutation is exactly the quartic, rotated-square
identity

\[
\operatorname{Tr}_{1,3}(pq_0X_2q_0p)
=\operatorname{Tr}_{1,3}(q_0pX_2pq_0)
\quad\text{for every }X.
\tag{35}
\]

The cubic relation proves (18), but the current audit did not find a valid
algebraic reduction from (17) to (35).  Since the channels are individually
self-adjoint, (35) is equivalently the statement that
\(\mathcal E_L\mathcal E_R\) is positive/self-adjoint.

The retained numerical candidates have:

\[
\begin{array}{c|c|c|c}
\text{candidate}
&\|{\rm YBE\ residual}\|_F
&\|[\mathcal E_L,\mathcal E_R]\|_F
&\|\sigma(\mathcal E_L)-\sigma(\mathcal E_R)\|_2\\ \hline
\text{unconstrained seed 26072804}
&8.73\cdot10^{-11}&9.59\cdot10^{-13}&1.13\cdot10^{-13}\\
\text{crossed-face calibration}
&1.10\cdot10^{-10}&2.67\cdot10^{-12}&1.95\cdot10^{-12}\\
\text{mixed-face calibration}
&9.84\cdot10^{-11}&2.25\cdot10^{-12}&2.65\cdot10^{-13}
\end{array}
\]

These data support (6) and left/right isospectrality, but they do not prove
either statement.

There is a still sharper pattern.  Let

\[
\Omega(X)=\frac{\operatorname{Tr}X}{d}I
\]

be the rank-one completely depolarizing projection.  Every retained
candidate satisfies, to the same numerical precision,

\[
\boxed{
\left(\mathcal E_R+\mathcal E_L-\frac43I\right)
\left(\mathcal E_R-\frac13I\right)
\left(\mathcal E_L-\frac13I\right)
=\frac8{27}\Omega.
}
\tag{36}
\]

The exact sparse verifier proves (36) for the published witness.  The exact
symbolic verifier proves it on the full color/face solution circle.  For the
three numerical candidates, the Frobenius residuals of (36) are respectively

\[
3.64\cdot10^{-13},\qquad
6.36\cdot10^{-13},\qquad
1.39\cdot10^{-13}.
\]

If commutation and (36) were universal, their simultaneous eigenvalue pairs
\((x,y)\) on the traceless operator space would obey

\[
(x-1/3)(y-1/3)(x+y-4/3)=0.
\tag{37}
\]

Thus every joint eigenvector would either lie in a \(1/3\)-eigenspace of
one channel or have paired eigenvalues summing to \(4/3\).  This exactly
explains the two moving \(d=4\) eigenvalues:

\[
0.4583843459+0.8749489875=\frac43
\]

and

\[
0.3364537238+0.9968796095=\frac43
\]

to the retained precision.  Each appears with multiplicity two in the
individual channel spectra.

In terms of the reduced braid-gate channels from (26),

\[
\mathcal U_R=\frac{3\mathcal E_R-I}{2},\qquad
\mathcal U_L=\frac{3\mathcal E_L-I}{2},
\]

equation (36) becomes the particularly simple relation

\[
(\mathcal U_R+\mathcal U_L-I)\mathcal U_R\mathcal U_L=\Omega.
\tag{38}
\]

Equations (36)--(38) are **not promoted to universal identities** here.
The current derivation of (18) only forces the left and right
operator-Schmidt supports into the \(1/3\)-eigenspaces.  It does not control
the complementary operator space on which the moving paired eigenvalues
live.  A proof would need a new contraction of the cubic relation (or an
operator-algebraic commuting-square theorem) covering that complement.

## 8. Standardness does not imply commutation

Here is an exact rational guard example.  Put

\[
A=\operatorname{diag}(1,1,-1,-1),
\]

\[
Q=
\begin{pmatrix}
3/5&0&-4/5&0\\
0&1&0&0\\
4/5&0&3/5&0\\
0&0&0&1
\end{pmatrix},
\qquad C=QAQ^T,
\]

and define the controlled reflection

\[
H=\sum_{i=0}^3|i\rangle\langle i|\otimes B_i,
\qquad
(B_0,B_1,B_2,B_3)=(A,-A,C,-C).
\tag{39}
\]

Then

\[
H=H^*,\quad H^2=I,\quad
\operatorname{Tr}_1H=\operatorname{Tr}_2H=0.
\]

Thus \(P=(I-H)/2\) is a rank-half standard projection.  Exact arithmetic
nevertheless gives

\[
\left\|[\mathcal E_L,\mathcal E_R]\right\|_F^2
=\frac{12423168}{244140625}>0.
\tag{40}
\]

The channels are not even isospectral: their first unequal power sum occurs
at degree four,

\[
\operatorname{Tr}_{\rm sup}(\mathcal E_R^4)
-\operatorname{Tr}_{\rm sup}(\mathcal E_L^4)
=\frac{26496}{390625}.
\tag{40a}
\]

The paired polynomial also fails, with exact squared Frobenius residual

\[
\frac{114672636256}{494384765625}>0.
\tag{40b}
\]

This \(H\) does not satisfy the exceptional cubic relation.  It proves that
any proof of (6), or of full left/right isospectrality, must use the
Yang--Baxter relation essentially; positivity, standardness, and
involutivity are not enough.

## 9. Even the stronger observed pattern does not force \(4\mid d\)

The conjectural identities in Section 7 still have no spectral-multiplicity
parity capable of excluding \(d=6\), even after imposing the stronger
complete-positivity consequence (25a).  The following exact Weyl-diagonal
countermodel is designed to include that constraint.

Write \(\mathbb C^6=\mathbb C^2\otimes\mathbb C^3\), and label its Weyl
operators by

\[
G=\mathbb Z_2^2\times\mathbb Z_3^2.
\]

On the dual group, let \(S\) consist of the sixteen nonzero labels

\[
\begin{aligned}
S={}&\{(0,0,c,e):(c,e)\ne(0,0)\}\\
&{}\cup\{(1,1,c,e):(c,e)\ne(0,0)\}.
\end{aligned}
\]

Prescribe Fourier eigenvalues

\[
\widehat p(0)=1,\qquad
\widehat p(z)=
\begin{cases}
1/3,&z\in S,\\
-1/3,&z\notin S\cup\{0\}.
\end{cases}
\tag{41}
\]

The inverse Fourier transform is nonnegative.  Explicitly, for a nonzero
group element \(g\), let

\[
A(g)=\sum_{z\in S}\chi_z(g).
\]

The character sum is \(16\) once, \(0\) eighteen times, and \(-2\) sixteen
times.  Consequently,

\[
p(0)=0,\qquad p(g)=\frac{2+A(g)}{54},
\]

so the probability multiset is

\[
\{(1/3)^1,(1/27)^{18},0^{17}\}.
\tag{42}
\]

Define the random-unitary Weyl channel

\[
\mathcal F(X)=\sum_{g\in G}p(g)W_gXW_g^*.
\tag{43}
\]

It is CP and bistochastic.  Since \(p(g)=p(-g)\), it is Hilbert--Schmidt
self-adjoint.  The identity Weyl has zero probability, so every displayed
Kraus operator is traceless, and Fourier diagonalization gives

\[
\sigma(\mathcal F)
=\{1^{\,1},(1/3)^{\,16},(-1/3)^{\,19}\},
\qquad
\operatorname{Tr}_{\rm sup}\mathcal F=0.
\tag{44}
\]

This model also matches the Hermitian-Kraus geometry in (25a), not merely
abstract complete positivity.  Pairing \(g\) with \(-g\) replaces each
equal-weight pair \(W_g,W_g^*\) by the traceless Hermitian operators

\[
\frac{W_g+W_g^*}{\sqrt{2d}},\qquad
\frac{W_g-W_g^*}{i\sqrt{2d}}.
\]

Together with Hermitian phase choices for the three self-inverse supported
Weyls, these form nineteen Hilbert--Schmidt orthonormal traceless Hermitian
directions \(A_\alpha\).  With \(\sigma_\alpha^2=d^2p(g)\) on the
corresponding direction, they satisfy

\[
\mathcal F(X)=\frac1d\sum_\alpha
\sigma_\alpha^2A_\alpha X A_\alpha,
\qquad
\sum_\alpha\sigma_\alpha^2=d^2.
\tag{45}
\]

Moreover, these nineteen Hermitian directions span exactly the
\(1/3\)-eigenspace of the channel \(\mathcal E\) below.  Thus, after taking
\(\mathcal E_L=\mathcal E_R\), the model also obeys the crossed
Schmidt-support requirement (22), with \(r=19\).

Now put

\[
\mathcal E=\frac12(\operatorname{id}+\mathcal F).
\tag{46}
\]

Then

\[
\sigma(\mathcal E)
=\{1^{\,1},(2/3)^{\,16},(1/3)^{\,19}\},
\qquad
\operatorname{Tr}_{\rm sup}\mathcal E=18.
\tag{47}
\]

The second universal affine channel is CP as well:

\[
\mathcal U=\frac{3\mathcal E-I}{2}
=\frac14(\operatorname{id}+3\mathcal F).
\tag{48}
\]

At the Weyl probability level, this is
\(\frac14\delta_0+\frac34p\), hence is manifestly random unitary.  Its
spectrum is \(\{1^{\,1},(1/2)^{\,16},0^{\,19}\}\) and its superoperator
trace is \(9=d^2/4\).

Taking \(\mathcal E_L=\mathcal E_R=\mathcal E\) enforces commutation,
left/right isospectrality, and a scalar common fixed space.  It also
satisfies the observed joint polynomial exactly:

\[
\left(\mathcal E_R+\mathcal E_L-\frac43I\right)
\left(\mathcal E_R-\frac13I\right)
\left(\mathcal E_L-\frac13I\right)
=\frac8{27}\Omega.
\tag{49}
\]

### The identity Schmidt pairing is an exact unbalanced cubic solution

The preceding channel model comes unexpectedly close to an actual
exceptional witness.  Let \(T=\{g:p(g)>0\}\), let \(T_0\) be its three
self-inverse elements, and choose one representative \(T_+\) from each of
the eight remaining inverse pairs.  Choose a Hermitian phase
\(\widetilde W_g\) for \(g\in T_0\).  The identity pairing of the two
Hermitian Schmidt bases is

\[
\begin{aligned}
H_0={}&\sum_{g\in T_0}\sqrt{p(g)}\,
\widetilde W_g\otimes\widetilde W_g\\
&+\sum_{g\in T_+}\sqrt{p(g)}
\left(W_g\otimes W_g^*+W_g^*\otimes W_g\right).
\end{aligned}
\tag{50}
\]

This is exactly the matrix
\(\sum_\alpha\sigma_\alpha A_\alpha\otimes A_\alpha\) associated with
(45).  It has a much simpler closed form.  After regrouping tensor factors
as

\[
(\mathbb C^2\otimes\mathbb C^3)^{\otimes2}
\cong(\mathbb C^2)^{\otimes2}\otimes(\mathbb C^3)^{\otimes2},
\]

one has

\[
\boxed{
H_0=\frac1{\sqrt3}\left[
Y\otimes Y\otimes I_9
+(X\otimes X+Z\otimes Z)\otimes F_3
\right],
}
\tag{50a}
\]

where \(F_3\) flips the two qutrits.  Direct cyclotomic arithmetic gives

\[
3H_0^2+2\sqrt3\,H_0-3I=0
\tag{51}
\]

and, on three sites,

\[
(H_{0,1}H_{0,2}H_{0,1}-H_{0,2}H_{0,1}H_{0,2})
=\frac13(H_{0,1}-H_{0,2}).
\tag{52}
\]

Thus \(H_0\) satisfies the target cubic relation exactly.  It fails only
the involution requirement:

\[
\sigma(H_0)
=\{(-\sqrt3)^{\,9},(1/\sqrt3)^{\,27}\}.
\tag{53}
\]

The multiplicities follow from (51), \(\operatorname{Tr}H_0=0\), and the
exact ranks of its two spectral factors.

There is no affine spectral repair.  More generally, if

\[
X^2=uX+vI,\qquad
X_1X_2X_1-X_2X_1X_2=c(X_1-X_2),
\]

then direct expansion for \(Y=aI+bX\) gives

\[
Y_1Y_2Y_1-Y_2Y_1Y_2
=(a^2+abu+b^2c)(Y_1-Y_2).
\tag{54}
\]

For \(X=H_0\), the unique nonconstant affine transform taking the two
eigenvalues to \(\{-1,+1\}\), up to overall sign, is

\[
K=\frac12(I+\sqrt3\,H_0).
\tag{55}
\]

Equations (51) and (54) show exactly that

\[
K^2=I,\qquad K_1K_2K_1=K_2K_1K_2,
\qquad \operatorname{Tr}K=18.
\tag{56}
\]

Hence \(K\) is an unbalanced braid involution with multiplicities \(9\) and
\(27\), not a trace-zero exceptional involution.  The only other affine
involutions are \(-K\) and \(\pm I\), with traces \(-18\) and \(\pm36\).
Formula (50a) makes the imbalance transparent: on the \(+1\) eigenspace of
\(F_3\), \(K\) restricts to the qubit flip

\[
F_2=\frac12(I+X\otimes X+Y\otimes Y+Z\otimes Z),
\]

whereas on the \(-1\) eigenspace it restricts to
\((Y\otimes I)F_2(Y\otimes I)\).
Reaching the exceptional class therefore requires changing the pairing
between the two nineteen-dimensional Schmidt bases, not merely rescaling or
shifting \(H_0\).

This is not a construction of \(P\), because \(H_0\) is not an involution.
Its exact purpose is to eliminate a whole obstruction route: no divisibility
by four follows from the channel spectra even after imposing commutation,
isospectrality, ergodicity, (36), complete positivity of both affine
transforms, the orthonormal traceless-Hermitian Kraus form forced by
(24)--(25), a common Schmidt realization, and even the three-site cubic
equation.  A successful channel obstruction must use the remaining
requirement \(H^2=I\) essentially.  A constructive \(d=6\) route would have
to change the pairing between the two Schmidt bases so as to impose
involutivity without losing the cubic relation.

## 10. Reproduction

Exact sparse witness and exact rational guard:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_channel_identities_d4.py
```

Exact symbolic color/face family:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_channel_color_family.py
```

Exact abstract \(d=6\) channel model:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_channel_d6_abstract_model.py
```

Numerical retained-candidate diagnostics:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  scripts/analyze_channel_d4_candidates.py \
  results/d6_candidates/d4_complex_none_random_seed26072804.npz \
  results/color_face_candidates/color_face_crossed_d4_2x2_complex_fourier_mixopt0_seed26073101.npz \
  results/color_face_candidates/color_face_mixed_d4_2x2_complex_random_mixopt1_seed26073114.npz \
  --output results/channel_d4_candidate_diagnostics.json
```
