# Commuting squares do not yet produce the projective \(A_4\) descent

**Date:** 2026-07-29
**Scope:** arbitrary exceptional ordinary localizers, followed by an exact
finite-dimensional limitation model
**Status:** exact horizontal-relative-commutant theorem and exact first-cell
countermodel; no unconditional proof of \(4\mid d\)

## 1. Conclusion

Write \(d=2s\), and let
\[
\mathcal A_n=C^*(P_1,\ldots,P_{n-1})
\subset M_d^{\otimes n}
\]
be the represented exceptional Hecke algebra.  The finite horizontal
relative commutants of the braid factor contain no hidden enlargement:
\[
\boxed{\mathcal L_{R,n}=\mathcal A_n.}
\tag{1}
\]
Moreover, normalized partial trace over the last tensor factor maps
\(\mathcal A_{n+1}\) onto \(\mathcal A_n\).  Thus every exceptional
localizer supplies the expected finite Markov commuting squares, but their
abstract algebras, inclusion matrices, traces, and indices are exactly the
already-audited \(H_n(3,6)\) data.  They permit every integer \(s\).

The first nontrivial commuting square is even weaker than tensor locality.
There is an exact square at formal local dimension \(d=2\),
\[
\begin{array}{ccc}
\mathcal A_2&\subset&\mathcal A_3\\
\cap&&\cap\\
M_4&\subset&M_8,
\end{array}
\tag{2}
\]
with the exceptional cubic, the correct Markov expectation, and faithful
\(H_3(3,6)\) block data.  It does **not** come from a single two-site
projection in the two spatial positions:
\[
p=p_0\otimes I_2,\qquad q\ne I_2\otimes p_0.
\tag{3}
\]
The square amplifies to the correct low-level multiplicities for every
\(s\geq1\), including odd \(s\).

Consequently:

1. an inclusion-matrix, index, or first-cell argument cannot force
   \(2\mid s\);
2. the commuting square does not canonically put
   \(\mathbb C^\alpha[A_4]\cong M_2(\mathbb C)^{\oplus3}\) on an
   \(s\)-dimensional space;
3. a module-category argument still requires a new extension theorem from
   the diagonal endomorphism tower to off-diagonal morphisms and coherent
   module associators;
4. any surviving connection argument must use global flatness together
   with the repeated equality
   \(P_i=I^{\otimes i-1}\otimes P\otimes I^{\otimes n-i-1}\).

The last requirement is essentially the unresolved tensor-local
realization problem, not a consequence of the known fusion or
commuting-square data.

## 2. The represented Hecke tower is the full finite horizontal tower

Let \(E_{m-1}:M_d^{\otimes m}\to M_d^{\otimes(m-1)}\) be normalized
partial trace over the final site.  Automatic standardness gives
\[
E_{m-1}(P_{m-1})=\frac12 I.
\tag{4}
\]

The usual two-double-coset decomposition of the type-\(A\) Hecke algebra
survives passage to every quotient:
\[
\mathcal A_m
=
\mathcal A_{m-1}
+
\mathcal A_{m-1}P_{m-1}\mathcal A_{m-1}.
\tag{5}
\]
Indeed, the standard Hecke basis is indexed by \(S_m\), and
\(S_{m-1}\backslash S_m/S_{m-1}\) has the two representatives
\(1\) and the last simple transposition.  Taking the represented quotient
gives (5).
For \(x,y\in\mathcal A_{m-1}\), neither \(x\) nor \(y\) acts on the final
site, so (4) gives
\[
E_{m-1}(xP_{m-1}y)=\frac12xy.
\tag{6}
\]
Equations (5)--(6) prove
\[
E_{m-1}(\mathcal A_m)=\mathcal A_{m-1}.
\tag{7}
\]
Iterating,
\[
E_n(\mathcal A_m)\subseteq\mathcal A_n
\qquad(m\geq n).
\tag{8}
\]

By definition, \(\mathcal L_R\) is the weak closure of
\(\bigcup_m\mathcal A_m\).  Conti--Lechner, Theorem 3.8, gives
\[
E_n(\mathcal L_R)=
\mathcal L_{R,n}
=\mathcal L_R\cap M_d^{\otimes n}.
\tag{9}
\]
The target \(M_d^{\otimes n}\) is finite-dimensional.  Normality of \(E_n\),
weak density, and (8) imply
\[
\mathcal L_{R,n}\subseteq\mathcal A_n.
\]
The reverse inclusion is Conti--Lechner, Proposition 3.5(b), or follows
directly because the first \(n-1\) braid generators lie in both algebras.
This proves (1).

Thus the finite commuting-square tower does not add simple blocks beyond
\(H_n(3,6)\).  All local-dimension dependence is in the concrete
embedding
\[
\mathcal A_n\hookrightarrow M_{(2s)^n}
\]
and its multiplicity spaces.

## 3. Inclusion matrices and indices contain no parity

At levels two and three,
\[
\mathcal A_2\cong\mathbb C\oplus\mathbb C,
\qquad
\mathcal A_3\cong
\mathbb C\oplus M_2(\mathbb C)\oplus\mathbb C.
\tag{10}
\]
Ordering the level-three blocks as endpoint, generic, endpoint, the
inclusion matrix and represented multiplicities are
\[
G=
\begin{pmatrix}
1&1&0\\
0&1&1
\end{pmatrix},
\qquad
m_2=
\begin{pmatrix}2s^2\\2s^2\end{pmatrix},
\qquad
m_3=
\begin{pmatrix}s^3\\3s^3\\s^3\end{pmatrix}.
\tag{11}
\]
They obey
\[
\boxed{Gm_3=(2s)m_2}
\tag{12}
\]
for every integer \(s\).  Also
\[
(1,1)m_2=(2s)^2,\qquad
(1,2,1)m_3=(2s)^3.
\tag{13}
\]

At every level the general formula is
\[
m_{\lambda,n}=D_\lambda s^n,
\]
so all higher inclusion identities are equally integral for odd \(s\).
Both the horizontal braid-subfactor index and the Yang--Baxter
endomorphism index are exactly \(4\), independently of \(s\).  The ambient
one-site matrix inclusion has multiplicity \(d=2s\), but its index
\(d^2=4s^2\) is again integral for every \(s\).

No index or inclusion-matrix denominator produces \(2\mid s\).

## 4. An exact first commuting square at formal dimension two

The following model isolates precisely what a commuting square forgets.
Write
\[
\mathbb C^8=
\mathbb C^2_A\otimes\mathbb C^2_B\otimes\mathbb C^2_C.
\]
Let
\[
\Phi_\pm=\frac{|00\rangle\pm|11\rangle}{\sqrt2},
\qquad
\Psi_\pm=\frac{|01\rangle\pm|10\rangle}{\sqrt2}
\]
be the Bell basis on \(B\otimes C\), and let \(U_0,U_1,U_2,U_3\)
be their rank-one projections in the displayed order.  Put
\[
\omega=e^{2\pi i/3},
\qquad
T=U_1+\omega U_2+\omega^2U_3.
\tag{14}
\]
Then
\[
T^*T=TT^*=I-U_0,
\qquad
\operatorname{Tr}_C(T)=0,
\tag{15}
\]
because every Bell projection has partial trace \(I_2/2\) and
\(1+\omega+\omega^2=0\).

Relative to the \(A=0,1\) decomposition, define
\[
h_1=
\begin{pmatrix}I_4&0\\0&-I_4\end{pmatrix},
\tag{16}
\]
\[
h_2=
\begin{pmatrix}
-\frac13I_4+\frac43U_0&
\frac{2\sqrt2}{3}T\\[1mm]
\frac{2\sqrt2}{3}T^*&
\frac13I_4-\frac43U_0
\end{pmatrix}.
\tag{17}
\]
On the two Bell lines \(A=0,\Phi_+\) and \(A=1,\Phi_+\), the pair gives
the common \(+1\) and common \(-1\) blocks.  On the other three paired
Bell lines it is the standard two-reflection block
\[
h_1=
\begin{pmatrix}1&0\\0&-1\end{pmatrix},
\qquad
h_2=
\begin{pmatrix}
-\frac13&\frac{2\sqrt2}{3}\zeta\\
\frac{2\sqrt2}{3}\bar\zeta&\frac13
\end{pmatrix},
\qquad |\zeta|=1.
\tag{18}
\]
It follows immediately that
\[
h_i=h_i^*,\qquad h_i^2=I,\qquad\operatorname{Tr}h_i=0,
\tag{19}
\]
and direct \(2\times2\) multiplication gives
\[
h_1h_2h_1-h_2h_1h_2=\frac13(h_1-h_2).
\tag{20}
\]

Set
\[
p=\frac{I-h_1}{2},\qquad q=\frac{I-h_2}{2},
\qquad
p_0=\operatorname{diag}(0,0,1,1)\in M_4.
\tag{21}
\]
Then
\[
p=p_0\otimes I_2,
\qquad
pqp-qpq=\frac13(p-q),
\qquad
\operatorname{rank}p=\operatorname{rank}q=4.
\tag{22}
\]
The six matrices
\[
I,\ p,\ q,\ pq,\ qp,\ pqp
\tag{23}
\]
are linearly independent.  Idempotence removes repeated letters, the
cubic exchanges \(pqp\) and \(qpq\), and multiplication of that identity
reduces every alternating word of length at least four.  Hence (23) spans
\(\operatorname{alg}(p,q)\).  Their
unnormalized final-qubit partial traces are, respectively,
\[
2I_4,\quad2p_0,\quad I_4,\quad p_0,\quad p_0,\quad p_0.
\tag{24}
\]
Therefore the trace-preserving expectation
\[
E_C=\frac12\operatorname{Tr}_C
\]
maps \(\operatorname{alg}(p,q)\) onto
\(\operatorname{alg}(p_0)\).  This proves that (2) is a commuting square.

The spectrum of \(pqp\) is
\[
0^{(4)},\qquad 1^{(1)},\qquad
\left(\frac13\right)^{(3)}.
\tag{25}
\]
Thus the algebra in (23) is a faithful copy of
\(\mathbb C\oplus M_2\oplus\mathbb C\) with exactly the exceptional
\(H_3(3,6)\) multiplicities for \(s=1\).

This is not an ordinary \(d=2\) localizer.  In the fixed tensor
factorization,
\[
\boxed{\|q-I_2\otimes p_0\|_{\mathrm{HS}}^2=4.}
\tag{26}
\]
The two adjacent generators are not the two spatial placements of one
two-site projection.  Hence the model does not conflict with the known
nonexistence theorem in dimension two.

Tensoring the level-\(n\) spaces with
\((\mathbb C^s)^{\otimes n}\), and reordering base and spectator factors,
amplifies (2) to the multiplicities (11) for every \(s\geq1\).  It still
does not repair (3).

## 5. Why the projective \(A_4\) action does not descend

The parity mechanism from the neutral fusion component is valid only
conditionally:
\[
\mathbb C^\alpha[A_4]\cong M_2(\mathbb C)^{\oplus3}
\quad\Longrightarrow\quad
\text{every unital module has even dimension}.
\tag{27}
\]
The missing step is an action of (27) on \(\mathbb C^s\).

Equation (1) sharpens the failure.  The horizontal relative commutants are
only the diagonal endomorphism algebras
\(\operatorname{End}(X^{\otimes n})\).  For a determinant endpoint
projection \(e\in\mathcal A_3\),
\[
e\mathcal A_3e=\mathbb Ce,
\qquad
\operatorname{rank}_{M_{d^3}}e=s^3.
\tag{28}
\]
Closed Hecke boundary words continue to act trivially on this
multiplicity, as proved in the determinant-boundary corner theorem.
The ambient corner
\[
eM_{d^3}e\cong M_{s^3}
\]
is large, but the commuting square does not select a copy of \(M_s\), a
cube-root tensor factorization, or the twisted algebra (27) inside it.

Finite braid image adds no action on that corner.  In the forced
decomposition
\[
V^{\otimes n}
\cong
\bigoplus_\lambda
S_{\lambda,n}\otimes
\mathbb C^{D_\lambda s^n},
\tag{29}
\]
the braid image spans \(\mathcal A_n\), so it acts as
\[
\bigoplus_\lambda
\operatorname{End}(S_{\lambda,n})\otimes I_{D_\lambda s^n}.
\tag{30}
\]
The abstract finite braid group is the same canonical finite group for
every faithful exceptional representation; the local dimension changes
only the identity multiplicities in (30).  A projective action on those
multiplicities would have to come from a newly constructed commutant
symmetry, not from finite image itself.

The exact \(s=1\) square makes this logical gap concrete.  Any rule that
extracted a unital representation of
\(\mathbb C^\alpha[A_4]\) on the \(s\)-dimensional factor from the first
commuting square alone would produce a one-dimensional module when
\(s=1\), which is impossible by (27).  Therefore no such extraction can
depend only on the data present in (2).

## 6. Module-category hypotheses that are not automatic

Galindo--Hong--Rowell distinguish three notions:

1. an ordinary localization in finite-dimensional Hilbert spaces;
2. a quasi-localization, in which a nontrivial associator changes the
   spatial placement of braid generators;
3. a weak localization, equivalently a monoidal functor to
   \(\operatorname{Bimod}(A)\) for a semisimple algebra \(A\).

Their Proposition 4.21 gives a weak localization for every fusion
category, and Section 5.6 gives this \(SU(3)_3\) sequence a
two-dimensional unitary quasi-localization.  Neither construction makes
the two adjacent generators equal to \(P\otimes I\) and \(I\otimes P\) in
one strict tensor product.

Conversely, an ordinary matrix localization represents only
\[
\operatorname{End}(X^{\otimes n})
\longrightarrow
\operatorname{End}(V^{\otimes n}).
\tag{31}
\]
It does not specify images of
\(\operatorname{Hom}(X^{\otimes m},X^{\otimes n})\) for \(m\ne n\), nor
evaluation maps, determinant isometries, module objects, or module
associators.  A module category requires precisely this off-diagonal and
coherent data.

An automatic upgrade of (31) to a fiber functor is impossible: the
published \(d=4\) localization exists, whereas Galindo--Hong--Rowell
Theorem 5.27 proves that \(\mathcal C(\mathfrak{sl}_3,6)\) has no fiber
functor.  An upgrade to a multi-object module category is not ruled out,
but one must first construct its base algebra, objects, and coherence
maps.  None is canonically determined by (1), (7), or the inclusion
matrices.

Thus classifications of \(SU(3)_3\) nimreps, module categories, or
Ocneanu cells cannot be imported as an obstruction until the following
new theorem is proved:

> **Required extension theorem.** Every exceptional strict localizer
> canonically extends from the diagonal tower (31) to a specified finite
> module category, and the module dimension corresponding to the
> projective \(A_4\) sector is exactly \(s=d/2\).

No audited source proves this statement, and the first-cell model shows
that its conclusion is not formal from commuting squares.

## 7. What remains viable

A full flat-connection formulation remains potentially useful, but it
must retain more than the finite squares:

- the same two-site \(P\) at every adjacent position;
- compatibility of the left and right tensor shifts;
- translation invariance across all levels;
- enough off-diagonal intertwiners to define the claimed module action;
- a proof that the relevant projective algebra acts on dimension \(s\),
  rather than on \(2s\), \(s^3\), or an uncontrolled corner.

If these conditions produce (27) on \(\mathbb C^s\), parity follows.
At present they are exactly the missing projective-descent theorem.

## 8. Exact replay

Run

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_d2_commuting_square_limitation.py
```

The verifier constructs (14)--(22) over
\(\mathbb Q(\sqrt2,\sqrt3,i)\), verifies both cubic forms, all partial
traces in (24), the six-dimensional algebra, spectrum (25), defect (26),
and the amplified inclusion identity (12).  Its retained output is
`results/d2_commuting_square_limitation_exact.txt`.

## 9. Sources and scope

- R. Conti and G. Lechner, *Yang--Baxter endomorphisms*, Theorem 3.8 and
  Proposition 3.5: finite horizontal relative commutants and commuting
  squares.
- C. Galindo, S.-M. Hong, and E. C. Rowell, *Generalized and
  quasi-localizations of braid group representations*, Definitions
  4.16 and 4.20, Proposition 4.21, Remark 4.22, and Section 5.6:
  quasi- and weak-localization distinctions.

This note does not construct a \(d=2\) or \(d=6\) Yang--Baxter matrix and
does not rule one out.  It proves that parity is absent from the finite
horizontal tower, its inclusion/index data, and its first nontrivial
commuting-square cell.  A stronger global flatness or tensor-local
descent theorem remains open.
