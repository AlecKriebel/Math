# Determinant-space transport does not supply a parity form

**Date:** 2026-07-29
**Scope:** arbitrary exceptional projection for the transport theorem;
arbitrary balanced projection for the flip-kernel reduction; the
published exact \(d=4\) solution for the spatial-pairing falsifier
**Status:** exact theorem and exact limitation audit; no proof that
\(4\mid d\)

## 1. Conclusion

Write \(d=2s\), let

\[
p=P_{12},\qquad q=P_{23},
\]

and let

\[
e=\frac32pqp-\frac12p
\tag{1}
\]

be their common-one projection.  Its range

\[
W=\operatorname{ran}e
=\operatorname{ran}P_{12}\cap\operatorname{ran}P_{23}
\tag{2}
\]

has dimension

\[
\dim W=\frac{d^3}{8}=s^3.
\tag{3}
\]

The exact four-site relation

\[
e_{123}e_{234}e_{123}=\frac14e_{123}
\tag{4}
\]

does give a canonical unitary transport

\[
\boxed{
U=2e_{234}e_{123}:
W\otimes V\longrightarrow V\otimes W.
}
\tag{5}
\]

After making the source and target tensor orders agree, a second exact
structure appears.  A partial transpose of this transport is a scaled
partial isometry:

\[
\boxed{
\operatorname{rank}T^{\Gamma_V}=\frac{d^2}{2},
\qquad
\text{every nonzero singular value of }T^{\Gamma_V}
\text{ equals }\frac d2.
}
\tag{6}
\]

Here \(T=\Sigma U\in\operatorname{End}(W\otimes V)\), where
\(\Sigma:V\otimes W\to W\otimes V\) is the tensor flip.  Equation (6) is
basis independent even though a basis is used to write the partial
transpose: changing bases conjugates its two support projections
unitarily.

This does **not** give a symplectic or quaternionic structure on \(W\).
The polar part of \(T^{\Gamma_V}\) is a unitary between two generally
different support spaces, each of dimension

\[
\frac{d^2}{2}=2s^2.
\tag{7}
\]

It is not an endomorphism, bilinear form, or antiunitary on the
\(s^3\)-dimensional space \(W\).

The exact published \(d=4\) witness rules out the most direct attempt to
close this gap by spatial reflection.  If \(J_\pi\) permutes the three
tensor sites, then the six compressions \(eJ_\pi e\) have the following
spectra on \(W\):

\[
\begin{array}{c|c|c}
\pi&\text{nonzero spectrum}&\text{rank}\\ \hline
\mathrm{id}&1\ \text{(eight times)}&8\\
\text{a transposition}&1/2\ \text{(four times)}&4\\
\text{a three-cycle}&1\ \text{(two times)}&2.
\end{array}
\tag{8}
\]

The two three-cycle compressions coincide.  Consequently the only
skew-adjoint direction in the real group algebra
\(\mathbb R[S_3]\), namely the difference of the two cycles, compresses
to zero.  Combining a nonidentity spatial permutation with coordinate
conjugation therefore gives a degenerate antilinear map on \(W\).
Coordinate conjugation alone is nondegenerate for this real witness, but
it squares to \(+I\), not \(-I\).

Thus neither the shifted determinant transport, its partial transpose,
bare reversal, nor their shortest five-site closures produces a
parity-bearing form on \(W\).  The odd test value \(s=3\) remains
arithmetically compatible:

\[
\dim W=27,\qquad
\dim(W\otimes V)=162,\qquad
\operatorname{rank}T^{\Gamma_V}=18.
\tag{9}
\]

The abstract odd-\(s\) Hecke model realizes the first of these as a
scalar multiplicity space.  It is not tensor-local, so this audit does
not disprove four-divisibility.  It proves that a parity theorem needs a
new spatial descent beyond the canonical determinant transports audited
here.

The distinct two-site flip product \(K=H\mathsf F\) gives a sharp but
tautological parity reformulation:

\[
\dim\ker(K+I)\equiv s\pmod2.
\]

Its kernel always equals

\[
(\operatorname{ran}P\cap\operatorname{Sym}^2V)
\oplus(\ker P\cap\Lambda^2V),
\]
even when \(H\) does not commute with the flip.  Thus proving this
kernel even would prove \(4\mid d\), but the determinant calculation
itself merely restates the missing parity.  A balanced, fully standard
\(d=2\) limitation projection has odd nullity \(3\) and shows that the
exceptional cubic must be used to obtain any positive result.

## 2. Universal setup and marginals

Automatic standardness gives

\[
\operatorname{Tr}_1P
=\operatorname{Tr}_2P
=\frac d2I_d.
\tag{10}
\]

For the common-one projection (1), the outer contractions are

\[
\operatorname{Tr}_1e=\frac d4P_{23},
\qquad
\operatorname{Tr}_3e=\frac d4P_{12}.
\tag{11}
\]

No scalar middle marginal is used below.  In particular, nothing in the
proof assumes a value for

\[
\operatorname{Tr}_2e\in\operatorname{End}(V_1\otimes V_3).
\tag{12}
\]

On four sites put

\[
E=e_{123},\qquad F=e_{234}.
\tag{13}
\]

The already-proved zero-variance calculation gives

\[
EFE=\frac14E,\qquad FEF=\frac14F.
\tag{14}
\]

Both projections have rank \(d\dim W\).

## 3. Canonical transport

Choose an isometry

\[
i:W\longrightarrow V^{\otimes3},
\qquad ii^*=e.
\tag{15}
\]

Let

\[
L=i\otimes I_V:
W\otimes V\longrightarrow V^{\otimes4},
\]

\[
R=I_V\otimes i:
V\otimes W\longrightarrow V^{\otimes4}.
\tag{16}
\]

Then

\[
LL^*=E,\qquad RR^*=F.
\]

Define

\[
U=2R^*L.
\tag{17}
\]

Using (14),

\[
U^*U
=4L^*RR^*L
=4L^*FL
=4L^*EFE L
=I_{W\otimes V}.
\tag{18}
\]

The source and target have the same finite dimension, so \(U\) is
unitary.  Equivalently, (17) is the coordinate form of (5).

The construction is independent of the chosen basis of \(W\).  Replacing
\(i\) by \(iu\), \(u\in U(W)\), conjugates the source and target of \(U\)
by the corresponding copies of \(u\).

### Why this unitary alone has no determinant parity

Equation (17) is a unitary between **different tensor orders**.  A
determinant of \(U\) requires choosing bases for both orders; changing
either basis changes its displayed phase.  Composing with the canonical
tensor flip gives an honest unitary \(T\) on \(W\otimes V\), but its
determinant is only a phase and has no relation to the parity of
\(\dim W\).

Closing the shifted path immediately gives

\[
(2EF)(2FE)=E.
\tag{19}
\]

More generally, the determinant boundary-corner theorem proves

\[
(e\otimes I_{V^{\otimes m}})
\mathcal A_{m+3}
(e\otimes I_{V^{\otimes m}})
=e\otimes\mathcal A_m.
\tag{20}
\]

Thus every closed four- or five-site word made from the Hecke boundary
operators acts trivially on the \(W\)-factor.  Partial tracing all added
boundary sites leaves only a scalar multiple of \(e\).  The open
transport (17) is genuine, but its Hecke closures do not create an
endomorphism of \(W\).

## 4. Exact partial-transpose theorem

Fix orthonormal bases of \(V\) and \(W\), and write the inclusion (15) as

\[
i_{\;abc,\mu},
\qquad
a,b,c\in\{1,\ldots,d\},
\quad
\mu\in\{1,\ldots,\dim W\}.
\tag{21}
\]

Let

\[
\Sigma:V\otimes W\longrightarrow W\otimes V
\]

be the tensor flip and put

\[
T=\Sigma U\in\operatorname{End}(W\otimes V).
\tag{22}
\]

Its entries are

\[
T_{\nu a,\mu x}
=2\sum_{b,c}
\overline{i_{bcx,\nu}}\,i_{abc,\mu}.
\tag{23}
\]

Partially transpose the \(V\)-indices:

\[
(T^{\Gamma_V})_{\nu x,\mu a}
=T_{\nu a,\mu x}.
\tag{24}
\]

Define two rectangular matrices

\[
\mathsf A_{(\nu,x),(b,c)}
=\overline{i_{bcx,\nu}},
\]

\[
\mathsf B_{(b,c),(\mu,a)}
=i_{abc,\mu}.
\tag{25}
\]

Equation (23) becomes the exact factorization

\[
\boxed{T^{\Gamma_V}=2\mathsf A\mathsf B.}
\tag{26}
\]

The two outer marginal identities (11) say precisely

\[
\mathsf A^*\mathsf A
=\frac d4P,
\qquad
\mathsf B\mathsf B^*
=\frac d4P.
\tag{27}
\]

Put \(a=d/4\).  The range of \(\mathsf B\) is
\(\operatorname{ran}P\), so \(P\mathsf B=\mathsf B\).  Therefore

\[
\begin{aligned}
(T^{\Gamma_V})^*T^{\Gamma_V}
&=4\mathsf B^*\mathsf A^*\mathsf A\mathsf B\\
&=4a\,\mathsf B^*P\mathsf B\\
&=4a\,\mathsf B^*\mathsf B.
\end{aligned}
\tag{28}
\]

The nonzero eigenvalues of
\(\mathsf B^*\mathsf B\) equal those of
\(\mathsf B\mathsf B^*=aP\).  Hence they all equal \(a\), with
multiplicity

\[
\operatorname{rank}P=\frac{d^2}{2}.
\tag{29}
\]

The nonzero eigenvalues in (28) are consequently

\[
4a^2=\frac{d^2}{4},
\tag{30}
\]

which proves (6).

### Exact scope

The polar part of \(T^{\Gamma_V}\) is a canonical unitary between its
initial and final support projections.  Both supports have rank
\(d^2/2\).  Neither support is naturally \(W\), whose dimension is
\(d^3/8\).  Even when these dimensions accidentally agree at \(d=4\),
the supports are different subspaces and no all-\(d\) identification has
been proved.

At \(d=6\), the dimensions are visibly different:

\[
\dim W=27,\qquad
\operatorname{rank}T^{\Gamma_V}=18.
\tag{31}
\]

Thus (26) cannot itself define a nondegenerate form on \(W\).

## 5. Exact spatial-pairing falsifier

Let \(J_\pi\) denote the tensor-permutation operator for
\(\pi\in S_3\).  A natural coordinate bilinear pairing on \(W\) obtained
from spatial symmetry has matrix

\[
C_\pi=eJ_\pi e\big|_W.
\tag{32}
\]

For the published exact real \(d=4\) witness, exact arithmetic gives:

\[
C_\pi=
\begin{cases}
I_W,&\pi=\mathrm{id},\\
\text{a rank-four operator with }C_\pi^2=C_\pi/2,
&\pi\text{ a transposition},\\
\text{a rank-two projection},
&\pi\text{ a three-cycle}.
\end{cases}
\tag{33}
\]

In the second line \(\operatorname{Tr}C_\pi=2\), and in the third line
\(\operatorname{Tr}C_\pi=2\).  These trace and polynomial identities give
the ranks in (8) without numerical singular values.

Moreover,

\[
eJ_{(123)}e=eJ_{(132)}e.
\tag{34}
\]

Every real skew-adjoint element of the spatial group algebra
\(\mathbb R[S_3]\) is a scalar multiple of

\[
J_{(123)}-J_{(132)}.
\]

Its compression vanishes by (34).  Hence no nonzero alternating form on
\(W\) comes from a real spatial-permutation closure.

Let \(\mathcal K\) be coordinate conjugation.  Since the published \(e\)
is real, \(\mathcal K\) preserves \(W\) and

\[
\mathcal K^2=I_W.
\tag{35}
\]

For nonidentity \(\pi\), the antilinear compression
\(eJ_\pi\mathcal K e\) has the same deficient rank as \(C_\pi\).
Therefore it is not antiunitary.  The identity permutation gives only
the real structure (35), not a quaternionic one.

This exact witness is enough to disprove any claim that the exceptional
relations force a nondegenerate alternating or square-\(-1\)
antiunitary **by these bare spatial operations**.  It does not exclude a
more elaborate operator-valued construction.

## 6. Odd-\(s\) abstract limitation and circularity

At three strands, the common-one Hecke block is one-dimensional
categorically and occurs in tensor space with multiplicity \(s^3\).
Every Hecke word acts as a scalar on this entire multiplicity space.

For \(s=3\), an abstract exact \(H_3(3,6)\) representation therefore has
a \(27\)-dimensional common-one block.  It can carry an ordinary real
structure of square \(+1\), and no Hecke relation asks for an alternating
form.

If an antiunitary \(\mathcal J=U\mathcal K\) of square \(-I\) did act on
an \(n\)-dimensional complex space, then

\[
U\overline U=-I_n.
\tag{36}
\]

Taking determinants gives

\[
|\det U|^2=(-1)^n,
\tag{37}
\]

so \(n\) must be even.  For \(n=s^3\), this is exactly the desired
conclusion \(2\mid s\).  Consequently, constructing such a
\(\mathcal J\) by first choosing a square-\(-1\) structure on the
multiplicity space would be circular: its existence is already
equivalent to the missing parity.

The abstract odd-\(s\) model is not a local projection
\(P\in\operatorname{End}(V\otimes V)\).  It only proves that the Hecke
block and all scalar determinant-channel operations do not impose
(36).  The full same-\(P\) tensor placement remains the unresolved datum.

## 7. The separate two-site flip product

The operator studied here is

\[
T^{\Gamma_V}
\in\operatorname{End}(W\otimes V),
\tag{38}
\]

a partial transpose of a **four-index determinant transport** built from
the three-site projection \(e\).

It must not be confused with the separate two-site operator

\[
K=H\mathsf F
\in\operatorname{End}(V\otimes V),
\tag{39}
\]

where \(\mathsf F\) flips the two local tensor factors.  The kernel
identity

\[
\ker(H\mathsf F+I)
=
(\operatorname{ran}P\cap\operatorname{Sym}^2V)
\oplus
(\ker P\cap\Lambda^2V)
\tag{40}
\]

is in fact universal; it does **not** require
\([H,\mathsf F]=0\).  Indeed,

\[
H(H\mathsf F+I)=\mathsf F+H,
\]

so

\[
\ker(H\mathsf F+I)=\ker(H+\mathsf F).
\tag{41}
\]

If \((H+\mathsf F)v=0\), then
\(\mathsf Fv=-Hv\).  Applying \(\mathsf F\) gives
\(\mathsf FHv=-v\), and therefore

\[
(H+\mathsf F)Hv=0.
\]

Thus the kernel in (41) is \(H\)-invariant.  Diagonalizing \(H\) on
this kernel gives (40): the \(H=-1\) part has \(\mathsf F=+1\), while
the \(H=+1\) part has \(\mathsf F=-1\).

There is already a purely dimensional index behind this decomposition.
Put

\[
a=\dim(\operatorname{ran}P\cap\operatorname{Sym}^2V),
\qquad
b=\dim(\ker P\cap\Lambda^2V).
\]

For arbitrary subspaces \(A,S\) of a finite-dimensional Hilbert space,

\[
\dim(A\cap S)-\dim(A^\perp\cap S^\perp)
=\dim A+\dim S-\dim\mathcal H.
\]

Apply this with \(A=\operatorname{ran}P\),
\(S=\operatorname{Sym}^2V\), and
\(\mathcal H=V\otimes V\).  Balance gives

\[
\boxed{a-b
=\frac{d^2}{2}+\frac{d(d+1)}2-d^2
=\frac d2=s.}
\tag{41a}
\]

Thus the nullity in (40) is

\[
\boxed{\dim\ker(H\mathsf F+I)=a+b=s+2b.}
\tag{41b}
\]

This is an exact reformulation of the missing parity before any
Yang--Baxter relation is used.  For comparison, the determinant gives
the same congruence in a second way.  Put

\[
K=H\mathsf F,\qquad
m_-=\dim\ker(K+I).
\tag{42}
\]

Since \(H\) and \(\mathsf F\) are unitary, so is \(K\), and

\[
\mathsf F K\mathsf F=K^*.
\tag{43}
\]

Consequently every nonreal eigenvalue of \(K\) occurs together with its
complex conjugate and with the same multiplicity.  Their contribution
to \(\det K\) is \(1\), so

\[
\det K=(-1)^{m_-}.
\tag{44}
\]

On the other hand, balance and \(d=2s\) give

\[
\det H=(-1)^{d^2/2}=1,
\]

whereas the flip has a \((-1)\)-eigenspace
\(\Lambda^2V\) of dimension \(d(d-1)/2\).  Hence

\[
\det K
=\det H\,\det\mathsf F
=(-1)^{d(d-1)/2}
=(-1)^s.
\tag{45}
\]

Combining (44) and (45),

\[
\boxed{m_-\equiv s\pmod2.}
\tag{46}
\]

Therefore proving that the space in (40) is even-dimensional for every
exceptional solution would be *exactly* a proof that \(4\mid d\).  But
none of (41)--(46) proves that evenness: it only moves the desired
parity from \(s\) to an equally parity-sensitive kernel.

The published \(d=4\) witness gives a useful exact calibration.  Even
though

\[
\operatorname{rank}[H,\mathsf F]=8,
\]

one has

\[
(H\mathsf F)^4=I,\qquad
\chi_{H\mathsf F}(x)
=(x-1)^4(x+1)^4(x^2+1)^4.
\tag{47}
\]

The two summands in (40) have dimensions \(3\) and \(1\), respectively,
so \(m_-=4\), as (46) requires.

Standardness alone cannot force this nullity to be even.  In local
dimension two, let

\[
P_{\mathrm{eq}}
=|00\rangle\langle00|+|11\rangle\langle11|.
\tag{48}
\]

It is a balanced projection with

\[
\operatorname{Tr}_1P_{\mathrm{eq}}
=\operatorname{Tr}_2P_{\mathrm{eq}}
=I_2,
\]

but for \(H_{\mathrm{eq}}=I-2P_{\mathrm{eq}}\),

\[
\dim\ker(H_{\mathrm{eq}}\mathsf F+I)=3.
\tag{49}
\]

This is not an exceptional solution: its projection cubic residual has
squared Hilbert--Schmidt norm \(4/9\).  It is an exact limitation model
showing that balance, scalar partial traces, and the tensor flip do not
provide the missing evenness.

Neither (6) nor the polar support of \(T^{\Gamma_V}\) acts on the kernel
in (40).  A proof that \(m_-\) is even must therefore use the exceptional
cubic in a new way.  Such a proof would be a genuinely operator-valued
flip argument, not a rephrasing of determinant transport or of the
determinant identity (45).

## 8. Exact replay

Run

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_determinant_transport_parity_limitation.py
```

The verifier uses exact rational and algebraic-number arithmetic.  It
checks:

- the universal factorization arithmetic in (26)--(30);
- the exact published \(d=4\) projection and all six spatial
  compressions in (33)--(34);
- the vanishing spatial alternating direction;
- the \(s=3\) dimensions in (9) and the determinant parity in
  (36)--(37).

The separate two-site flip audit has its own exact replay:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_two_site_flip_parity_reduction.py
```

It checks:

- the exact two-site flip identities (40)--(47), the noncommuting
  published \(d=4\) calibration, and the standard \(d=2\) limitation
  model (48)--(49).

## 9. Remaining target

The common-one space does carry more than its dimension: it has the open
unitary transport (5), the partial-isometry support (6), and simultaneous
embeddings at every shifted position.  The exact audit shows where those
data stop:

\[
\boxed{
\text{they do not canonically descend to an alternating or
quaternionic form on }W.
}
\]

A successful parity proof must add an operator-valued invariant that
uses the same-\(P\) tensor placement but is not a closed Hecke boundary
word, bare spatial reversal, or the partial-transpose support in (6).
The two-site flip product sharpens the target to the evenness of (40),
but equations (41)--(46) show that its determinant is only a restatement
of the missing parity, not a proof of it.
