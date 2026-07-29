# Fusion grading, projective \(A_4\), and parity: an exact audit

**Date:** 2026-07-29
**Scope:** arbitrary exceptional ordinary localizer of dimension \(d=2s\)
**Status:** exact conditional parity mechanism and exact obstruction to the
naive descent; no unconditional proof that \(2\mid s\)

## Executive conclusion

The fusion data suggest a precise parity-bearing projective algebra, but
the matrix-localization axioms do not currently put that algebra on an
\(s\)-dimensional space.  In fact, its natural two-dimensional modules
account for the factor \(2\) in \(d=2s\), not for an additional factor
\(2\) in \(s\).

The neutral component of the \(SU(3)_3\) fusion ring is the representation
ring of \(A_4\).  Its degree-one component has the based-module rules of the three
irreducible projective \(A_4\)-representations in the nontrivial Schur
multiplier class.  The corresponding twisted group algebra is

\[
\mathbb C^\alpha[A_4]\cong
M_2(\mathbb C)\oplus M_2(\mathbb C)\oplus M_2(\mathbb C).
\tag{1}
\]

Consequently, the following *conditional* route would prove the desired
divisibility:

> If every exceptional localizer canonically supplied a unital
> \(*\)-representation
> \[
> \mathbb C^\alpha[A_4]\longrightarrow M_s(\mathbb C),
> \]
> then \(s\) would be even and hence \(4\mid d\).

The missing implication is real and load-bearing.  An ordinary
localization represents the diagonal endomorphism algebras
\(\operatorname{End}(X^{\otimes n})\); it is not a tensor or module functor
on the full fusion category.  In particular:

1. the two trivalent one-dimensional categorical channels at three
   strands are represented by subspaces of dimension \(s^3\), not by
   lines;
2. the braid algebra acts by scalars on each such multiplicity space and
   supplies no symmetric, alternating, real, or quaternionic form there;
3. the \(\mathbb Z_3\)-grading is constant on every fixed tensor power and
   therefore gives only a scalar grading character;
4. the generator \(X\) is not self-dual, so its second
   Frobenius--Schur indicator supplies no one-site bilinear form;
5. spatial tensor reversal takes the localizer \(P\) to the *flipped*
   localizer \(P^{\mathrm{op}}=FPF\).  It is not an internal symmetry of a
   general \(P\).

The last point is not merely a logical possibility.  For the published
exact \(d=4\) solution,

\[
\|P-P^{\mathrm{op}}\|_{\mathrm{HS}}^2=8,
\qquad
\|e-J_3eJ_3\|_{\mathrm{HS}}^2=14,
\tag{2}
\]

where \(e\) is the three-site common-one projection and \(J_3\) reverses
the three tensor factors.  Thus even a valid exceptional localizer need
not preserve its determinant channel under bare spatial reflection.

The direct ``grading + determinant + reflection/FS'' argument therefore
does **not** prove \(4\mid d\).  The viable sharpened target is a new
**projective descent theorem** extracting (1) on an invariantly defined
\(s\)-dimensional multiplicity space from the simultaneous placements
\(P\otimes I\) and \(I\otimes P\).  Nothing in the present tower,
duality, or reversal data performs that descent.

## 1. Exact \(SU(3)_3\) grading and the neutral \(A_4\) ring

Label the ten simple objects by

\[
(a,b),\qquad a,b\geq0,\quad a+b\leq3.
\]

Let \(X=(1,0)\).  Fusion by \(X\) is

\[
X\otimes(a,b)=
\begin{cases}
(a+1,b),&a+b<3,\\
0,&a+b=3,
\end{cases}
\oplus
\begin{cases}
(a-1,b+1),&a>0,\\
0,&a=0,
\end{cases}
\oplus
\begin{cases}
(a,b-1),&b>0,\\
0,&b=0.
\end{cases}
\tag{3}
\]

The universal \(\mathbb Z_3\)-degree is

\[
\deg(a,b)=a+2b\pmod3.
\tag{4}
\]

Every successor in (3) has degree one larger.  Hence all summands of
\(X^{\otimes n}\) have the same degree \(n\bmod3\).  On the diagonal
endomorphism algebra at fixed \(n\), the grading character is therefore a
single scalar.  It does not split the tensor-space multiplicity and cannot
impose a parity.

Put

\[
\mathbf1=(0,0),\qquad
g=(3,0),\qquad
g^2=(0,3),\qquad
Y=(1,1).
\]

These are exactly the degree-zero simples, and exact fusion-matrix
calculation gives

\[
g^3=\mathbf1,\qquad gY=Y,
\qquad
Y^2=\mathbf1+g+g^2+2Y.
\tag{5}
\]

Equation (5) is the Grothendieck ring of
\(\operatorname{Rep}(A_4)\): the three one-dimensional representations
are \(\mathbf1,g,g^2\), and \(Y\) is the real three-dimensional
representation.

The degree-one simples form the orbit

\[
X_0=(1,0),\qquad X_1=(2,1),\qquad X_2=(0,2),
\]

with

\[
gX_i=X_{i+1},\qquad
YX_i=X_0+X_1+X_2
\quad (i\bmod3).
\tag{6}
\]

These are exactly the module-fusion rules of the three irreducible
projective \(A_4\)-representations belonging to the nontrivial Schur
multiplier class.

## 2. The exact conditional parity algebra

Let \(2T=Q_8\rtimes\mathbb Z_3\) be the binary tetrahedral group.  Its
central element \(z=-1\in Q_8\) has order two and

\[
2T/\langle z\rangle\cong A_4.
\]

The nontrivial twisted group algebra of \(A_4\) can be written

\[
B_-=
\mathbb C[2T]/(z+1).
\tag{7}
\]

It has complex dimension \(12\).  Let \(I_q,J_q,K_q\) be the standard
two-dimensional quaternion matrices and put

\[
T=\frac{-I+I_q+J_q+K_q}{2}.
\]

Then

\[
T^3=I,\qquad
TI_qT^{-1}=K_q,\qquad
TJ_qT^{-1}=I_q,\qquad
TK_qT^{-1}=J_q.
\tag{8}
\]

If \(\omega=e^{2\pi i/3}\), replacing \(T\) by
\(\omega^rT\), \(r=0,1,2\), gives three two-dimensional representations
of \(2T\), all with \(z\mapsto-I\).  On the quotient basis

\[
\{qT^a:q\in\{1,I_q,J_q,K_q\},\ a=0,1,2\},
\]

the direct sum of these three representations has exact determinant

\[
46656=6^6\ne0.
\tag{9}
\]

It is therefore an isomorphism

\[
B_-\xrightarrow{\ \cong\ }M_2(\mathbb C)^{\oplus3},
\]

proving (1) without relying on character-table nomenclature.

### Conditional parity lemma

Every finite-dimensional unital \(*\)-representation of \(B_-\) is a
direct sum of two-dimensional simple modules.  If it acts on
\(\mathbb C^s\), then

\[
s=2(k_0+k_1+k_2)
\]

for nonnegative integers \(k_i\).  Thus \(s\) is even.

This is a valid parity lemma.  What has not been proved is that an
arbitrary exceptional \(P\) produces such an action on a space of
dimension \(s=d/2\).

There is an important stronger limitation.  The *natural* place for this
projective algebra to act is the local space \(V\) itself.  For every
integer \(s\), projection onto any one of the three simple summands gives
a unital representation

\[
B_-\longrightarrow M_2(\mathbb C)\otimes I_s
\subset M_{2s}(\mathbb C).
\tag{10}
\]

Thus a projective \(A_4\)-action on \(V\) forces only
\(2\mid d\), which is already known.  To obtain \(2\mid s\), one must
prove that a *second copy* of the nontrivial projective class acts on the
multiplicity factor rather than on the categorical two-dimensional
factor.  Fusion-ring terminology alone does not make that second copy
exist.

## 3. What the localizer actually supplies at three strands

For every exceptional solution, the exact tower multiplicities are

\[
m_{\lambda,n}=D_\lambda s^n,
\qquad d=2s.
\tag{11}
\]

At \(n=3\),

\[
X^{\otimes3}
=\mathbf1\oplus g\oplus2Y
\tag{12}
\]

at the fusion-ring level.  The two one-dimensional categorical endpoints
\(\mathbf1\) and \(g\) are the common-zero and common-one simple
Hecke blocks (up to the normalization convention).  In the ordinary
tensor-space representation, each block has rank

\[
\boxed{s^3}.
\tag{13}
\]

If \(p=P_{12}\) and \(q=P_{23}\), their projections are

\[
e_1=\frac32pqp-\frac12p,\qquad
e_0=\frac32(I-p)(I-q)(I-p)-\frac12(I-p).
\tag{14}
\]

On \(\operatorname{ran}e_1\), both \(p\) and \(q\) act as \(I\).  On
\(\operatorname{ran}e_0\), both act as \(0\).  Hence every element of the
three-strand braid/Hecke algebra acts by a scalar on either multiplicity
space.  No polynomial in the local braid generators can define a
nontrivial complex structure, antiunitary, or alternating form there.

For \(s=3\), the two spaces in (13) each have dimension \(27\).  All
three-strand and all-strand multiplicities remain integral.  On a
\(27\)-dimensional common-one block, every \(R_i\) acts as \(-I\), so the
identity matrix is a nondegenerate invariant **symmetric** bilinear form.
An alternating nondegenerate form cannot exist in odd dimension, but the
braid action does not ask for one.  This is an exact countermodel to any
parity argument using only the scalar determinant-channel braid action.

The categorical determinant morphism

\[
\mathbf1\longrightarrow X^{\otimes3}
\]

is a line.  The matrix localization does not send it to a chosen vector:
it sends the corresponding *endomorphism block* to a rank-\(s^3\)
projection.  Replacing that projection by a trivalent tensor, or
factoring its range canonically as

\[
\operatorname{ran}e_0\stackrel{?}{\cong}
(\mathbb C^s)^{\otimes3},
\tag{15}
\]

adds precisely the functorial information absent from the definition.

## 4. Frobenius--Schur and projective-representation checks

The generating object is not self-dual:

\[
X^*=(0,1)\ne(1,0)=X,
\qquad
\operatorname{Hom}(\mathbf1,X^{\otimes2})=0.
\tag{16}
\]

Thus the ordinary second Frobenius--Schur mechanism does not put a
bilinear form on the one-site local space.

In the exact \(A_4\) based-ring model, the self-dual neutral object \(Y\)
is modeled by the real three-dimensional representation, so that model
contributes a symmetric rather than quaternionic form.  This statement is
only about the audited representation-ring model; a categorical
Frobenius--Schur indicator would require associator and duality data that
the localizer does not preserve.  The word ``quaternionic'' in the older
realization refers instead to the binary-tetrahedral/projective algebra
in Section 2.  That algebra would force parity only after an action on
\(\mathbb C^s\) has been constructed.

Indeed, the standard projective spinor carries the antiunitary

\[
\mathcal J_2=
\begin{pmatrix}0&1\\-1&0\end{pmatrix}K,
\qquad
\mathcal J_2^2=-I_2,
\tag{17}
\]

where \(K\) is entrywise conjugation.  On
\(\mathbb C^2\otimes\mathbb C^s\), the antiunitary
\(\mathcal J_2\otimes K_s\) squares to \(-I_{2s}\) for **every** \(s\),
including odd \(s\).  A quaternionic form on the categorical spinor
therefore explains evenness of \(d\), not divisibility of \(d\) by four.
A second quaternionic form on \(\mathbb C^s\) would force the desired
parity, but is precisely the unproved descent.

There is also no parity from the cyclic grading by itself.  Every
projective complex representation of \(\mathbb Z_3\) can be rephased to
an honest one: if \(U^3=\lambda I\), choose \(\mu^3=\lambda^{-1}\) and
replace \(U\) by \(\mu U\).  A possible third-cohomology associator
class is data of a monoidal category, not data contained in the
diagonal Hecke tower.  Importing it into the local matrix problem again
requires a functorial descent theorem.

## 5. Spatial reversal is external, not an internal FS operator

Let \(F\) be tensor flip on \(V\otimes V\), and define

\[
P^{\mathrm{op}}=FPF.
\tag{18}
\]

Let \(J_n\) reverse the order of \(n\) tensor factors.  A direct basis
calculation gives

\[
J_nP_{i,i+1}(P)J_n
=P_{n-i,n-i+1}(P^{\mathrm{op}}).
\tag{19}
\]

Consequently \(J_n\) intertwines the tower of \(P\) with the tower of
\(P^{\mathrm{op}}\).  It is an internal reflection of the tower of \(P\)
only after one adds a coherent identification of \(P^{\mathrm{op}}\) with
\(P\).  Such an identification is not part of the exceptional-class
relations.

For the common-one projection in (14), equation (19) gives

\[
J_3e_1(P)J_3=e_1(P^{\mathrm{op}}),
\tag{20}
\]

not \(e_1(P)\) in general.

The published exact \(d=4\) solution supplies a decisive valid example.
Exact algebraic arithmetic gives

\[
\operatorname{Tr}e_1=8,
\qquad
\operatorname{Tr}\!\left(e_1J_3e_1J_3\right)=1,
\tag{21}
\]

and hence (2).  Bare reversal therefore does not preserve the
determinant channel.  The same witness is real, so entrywise complex
conjugation does preserve the channel but squares to \(+I\), not \(-I\).
Neither available operation yields a forced quaternionic structure.

Shifted common-one projections do provide canonical partial isometries
between *different* subspaces, for example
\[
2e_{234}e_{123}:
\operatorname{ran}e_{123}\longrightarrow
\operatorname{ran}e_{234}.
\]
They do not close to an antiunitary on one fixed \(s\)-dimensional
space.  Closing the chain by a cyclic permutation again introduces
\(P^{\mathrm{op}}\) at the boundary.

## 6. Exact limitation and the remaining viable theorem

The following statements are now sharply separated.

### Proved

1. The neutral fusion ring is \(R(A_4)\), and its degree-one based module
   agrees with the nontrivial projective \(A_4\) module.
2. The associated twisted algebra is \(M_2^{\oplus3}\).
3. Any action of that algebra on \(\mathbb C^s\) forces \(2\mid s\).
4. The Hecke tower and determinant blocks do not themselves supply such
   an action.
5. Tensor reversal maps \(P\) to \(P^{\mathrm{op}}\), and the exact
   published solution shows that this need not preserve the determinant
   channel.

### Not proved

It remains possible that the *full simultaneous spatial placement*
\[
P_{12}=P\otimes I,\qquad P_{23}=I\otimes P
\]
forces a subtler projective action that is invisible in the diagonal
tower.  The audit does not rule that out.

A precise sufficient theorem would be:

> **Projective descent target.** For every exceptional \(P\) on
> \(V=\mathbb C^{2s}\), construct invariantly a Hilbert space \(M(P)\) of
> dimension \(s\) and a unital \(*\)-homomorphism
> \[
> \mathbb C^\alpha[A_4]\longrightarrow\operatorname{End}(M(P)).
> \]

Section 2 would then prove \(2\mid s\) in one line.  Any proposed
construction must explain why \(M(P)\) has dimension \(s\), rather than
\(s^3\), and why it is independent of a noncanonical decomposition of
the central multiplicity spaces.  Neither fusion multiplicities,
Frobenius--Schur indicators, the \(\mathbb Z_3\)-grading, nor bare spatial
reversal supplies those two facts.

## 7. Exact replay

Run

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_fusion_anomaly_parity.py
```

The verifier uses exact SymPy arithmetic.  It checks:

- the ten-object \(SU(3)_3\) fusion graph and \(\mathbb Z_3\)-grading;
- the \(A_4\) neutral fusion relations and projective degree-one module;
- the exact binary-tetrahedral quotient isomorphism
  \(B_-\cong M_2^{\oplus3}\), including determinant \(6^6\);
- all multiplicity recurrences for the odd test value \(s=3\);
- the scalar determinant-block limitation;
- the exact flip and three-site reversal defects (2) for the published
  \(d=4\) solution.
