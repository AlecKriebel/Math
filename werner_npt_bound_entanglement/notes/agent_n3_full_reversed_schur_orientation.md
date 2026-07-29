# The full three-copy problem as one reversed-Schur orientation inequality

## Status

This note gives an exact same-copy reduction of the **full**
unrestricted three-copy endpoint.  It does not prove the remaining
inequality.

For two left and two right singular vectors, compress the positive
replica filter
\[
 Y=\bigotimes_{i=1}^3\left(I-\frac12F_i\right)
\]
to the resulting logical two-qubit space.  Write the strictly positive
compression in \(2\times2\) logical blocks as
\[
 K=\begin{pmatrix}A&B\\ B^\dagger&D\end{pmatrix}\succ0.
\]
The endpoint theorem is equivalent to positivity of a logical partial
transpose of \(K\).  The new observation is that its determinant has
the exact form
\[
 \boxed{\quad
 \frac{\det K^\Gamma}{\det A\det D}
 =
 \det(I-X^\dagger X)
 +\|X\|_2^2-\|Z\|_2^2,
 \quad}
\]
where
\[
 X=A^{-1/2}BD^{-1/2},\qquad
 Z=A^{-1/2}B^\dagger D^{-1/2}.
\]
Since \(K\succ0\), \(X\) is a strict contraction.  Consequently the
whole unrestricted three-copy problem is precisely
\[
 \boxed{\qquad
 \|Z\|_2^2-\|X\|_2^2
 \leq
 (1-s_1(X)^2)(1-s_2(X)^2).
 \qquad}
\]
The right side is the ordinary positive Gram slack.  The left side is
the sole reversal/orientation defect.

This reduction includes the scalar, one-body, and pair components
together; it is not a pair-sector relaxation.  It also identifies
several automatic positive charts and gives an exact abstract
counterexample showing that positivity and the spectral interval of
the physical replica filter do not, by themselves, control the
orientation defect.  A proof must still use the common tensor origin
of \(A,B,D\).

The dependency-free exact checker is
`verification/verify_n3_full_reversed_schur_orientation.py`.

## 1. Logical compression and block convention

Let
\[
 U,V:\mathbb C^2\longrightarrow
 (\mathbb C^3)^{\otimes3}
\]
be isometries, and define
\[
 K(U,V)
 =(U^\dagger\otimes V^\dagger)
 Y(U\otimes V).
\tag{1}
\]
Every local factor in \(Y\) has eigenvalues \(1/2\) and \(3/2\), so
\[
 Y\succeq\frac18I,\qquad K(U,V)\succeq\frac18I_4.
\tag{2}
\]
In particular \(K\) and both diagonal logical blocks below are
invertible.

Order the logical basis by the first qubit and write
\[
 K=\begin{pmatrix}A&B\\B^\dagger&D\end{pmatrix},
\qquad A,D\in M_2,\quad A,D\succ0.
\tag{3}
\]
Partial transpose on the first logical qubit gives
\[
 K^{\Gamma_1}
 =\begin{pmatrix}A&B^\dagger\\B&D\end{pmatrix}.
\tag{4}
\]
Partial transpose on the second qubit is the full transpose of (4).
Thus the two partial transposes have the same determinant and are
positive simultaneously.

The established two-plane reduction says
\[
 Q_3(C)\geq0\quad(\operatorname{rank}C\leq2)
\quad\Longleftrightarrow\quad
 K(U,V)^\Gamma\succeq0\quad\hbox{for every }U,V.
\tag{5}
\]
Because a partial transpose of a strictly positive two-qubit operator
is strictly block-positive, it has at most one negative eigenvalue and
cannot have a negative and a zero eigenvalue simultaneously.
Consequently
\[
 K^\Gamma\succeq0
\quad\Longleftrightarrow\quad
 \det K^\Gamma\geq0.
\tag{6}
\]

## 2. Exact reversed-Schur determinant identity

### Lemma 2.1

Let (3) be any strictly positive \(4\times4\) Hermitian block matrix
with \(2\times2\) blocks.  Put
\[
 X=A^{-1/2}BD^{-1/2},\qquad
 Z=A^{-1/2}B^\dagger D^{-1/2}.
\tag{7}
\]
Then
\[
\boxed{
\begin{aligned}
\frac{\det K}{\det A\det D}
 &=
 1-\|X\|_2^2+|\det X|^2
 =\det(I-X^\dagger X),\\
\frac{\det K^\Gamma}{\det A\det D}
 &=
 1-\|Z\|_2^2+|\det Z|^2,\\
\det K^\Gamma
 &=
 \det K+\det A\det D
 \bigl(\|X\|_2^2-\|Z\|_2^2\bigr).
\end{aligned}}
\tag{8}
\]
Moreover,
\[
 |\det X|=|\det Z|.
\tag{9}
\]

### Proof

The ordinary Schur complement gives
\[
\begin{aligned}
\det K
 &=\det A\det(D-B^\dagger A^{-1}B)\\
 &=\det A\det D\,
 \det\!\left(
 I-D^{-1/2}B^\dagger A^{-1}BD^{-1/2}
 \right)\\
 &=\det A\det D\,\det(I-X^\dagger X).
\end{aligned}
\tag{10}
\]
For a \(2\times2\) matrix \(T\),
\[
 \det(I-T^\dagger T)
 =1-\operatorname{Tr}(T^\dagger T)+|\det T|^2.
\tag{11}
\]
This proves the first line of (8).

Apply the same calculation to (4):
\[
\begin{aligned}
\det K^\Gamma
 &=\det A\det(D-BA^{-1}B^\dagger)\\
 &=\det A\det D\,
 \det(I-Z^\dagger Z),
\end{aligned}
\tag{12}
\]
which proves the second line.  Finally,
\[
 |\det X|
 =
 \frac{|\det B|}{\sqrt{\det A\det D}}
 =
 \frac{|\det B^\dagger|}{\sqrt{\det A\det D}}
 =|\det Z|.
\tag{13}
\]
Subtracting the first two formulas proves the last line of (8).
\(\square\)

There is a version avoiding matrix square roots:
\[
\boxed{
\begin{aligned}
\det K^\Gamma-\det K
=\det A\det D\bigl[
 &\operatorname{Tr}(D^{-1}B^\dagger A^{-1}B)\\
 &-\operatorname{Tr}(D^{-1}BA^{-1}B^\dagger)
\bigr].
\end{aligned}}
\tag{14}
\]
This is often the most convenient exact-algebra form.

## 3. Exact equivalence for the unrestricted endpoint

Positivity of \(K\) and (10) imply
\[
 I-X^\dagger X\succ0.
\tag{15}
\]
Thus \(s_1(X)<1\), and
\[
 \det(I-X^\dagger X)
 =(1-s_1(X)^2)(1-s_2(X)^2)>0.
\tag{16}
\]
Combining (5)--(8) gives the promised lossless statement.

### Theorem 3.1

Unrestricted qutrit three-copy endpoint positivity is equivalent to
\[
\boxed{
\|A^{-1/2}B^\dagger D^{-1/2}\|_2^2
-
\|A^{-1/2}BD^{-1/2}\|_2^2
\leq
\det\!\left(
 I-D^{-1/2}B^\dagger A^{-1}BD^{-1/2}
\right)}
\tag{17}
\]
for every physical compression (1).

Equivalently, with \(X,Z\) from (7),
\[
 \boxed{\qquad
 \|Z\|_2^2-\|X\|_2^2
 \leq(1-s_1(X)^2)(1-s_2(X)^2).
 \qquad}
\tag{18}
\]

The right side in (18) is exactly
\[
 \frac{\det K}{\det A\det D};
\tag{19}
\]
it measures the distance from singularity of the ordinary positive
Gram matrix.  No matrix-valued Schur inequality remains.  A violation
of (18) is exactly a negative three-copy Werner witness after taking
the negative eigenvector of \(K^\Gamma\).

## 4. Automatic charts

Equation (18) holds immediately whenever
\[
 \|Z\|_2\leq\|X\|_2.
\tag{20}
\]
In particular the orientation defect vanishes in each of the
following cases:

1. \(A=D\), because then \(Z=X^\dagger\);
2. more generally \(D=tA\) for a positive scalar \(t\);
3. \(B=B^\dagger\);
4. \(B=-B^\dagger\);
5. \(B=e^{i\theta}H\) for a Hermitian \(H\).

These are statements about the logical Gram blocks, not assumptions
on the original coefficient matrix.  They expose the remaining locus
as genuinely reversed and nonnormal: its reversed normalized
coherence must have strictly larger Hilbert--Schmidt norm than the
ordinary normalized coherence.

## 5. Exact abstract obstruction

The common physical origin of the three blocks is indispensable.
Positivity of \(K\), even together with the exact spectral interval
of the physical filter, does not imply (18).

Take
\[
 m=\frac12,\qquad
 |\Phi_2\rangle=|00\rangle+|11\rangle,\qquad
 K_*=mI_4+|\Phi_2\rangle\langle\Phi_2|.
\tag{21}
\]
Then
\[
 \operatorname{spec}K_*=
 \left(\frac52,\frac12,\frac12,\frac12\right),
\tag{22}
\]
which lies inside the physical filter interval
\([1/8,27/8]\).  In the block convention (3),
\[
 A=\begin{pmatrix}3/2&0\\0&1/2\end{pmatrix},\quad
 D=\begin{pmatrix}1/2&0\\0&3/2\end{pmatrix},\quad
 B=\begin{pmatrix}0&1\\0&0\end{pmatrix}.
\tag{23}
\]
Partial transpose gives
\[
 \operatorname{spec}K_*^\Gamma
 =\left(\frac32,\frac32,\frac32,-\frac12\right),
\tag{24}
\]
so
\[
 \det K_*=\frac5{16},\qquad
 \det K_*^\Gamma=-\frac{27}{16}.
\tag{25}
\]
Here
\[
 \det A\det D=\frac9{16},\qquad
 \det(I-X^\dagger X)=\frac59,\qquad
 \|Z\|_2^2-\|X\|_2^2=\frac{32}{9}.
\tag{26}
\]
Thus the ordinary Schur slack is positive, but the orientation defect
overwhelms it exactly.

The example is not asserted to be a compression (1).  It proves that
a successful argument cannot use only:

* positivity of the logical Gram;
* its universal lower and upper spectral bounds; or
* the ordinary Schur contraction.

The remaining physical lemma is precisely to control the orientation
defect in (18) using the shared three-fold tensor compression.

## 6. The orientation defect is a logical transfer determinant

The inverse-block expression has a basis-free channel interpretation.
Let
\[
 e_0=\frac{I}{\sqrt2},\quad
 e_1=\frac{X}{\sqrt2},\quad
 e_2=\frac{Y}{\sqrt2},\quad
 e_3=\frac{Z}{\sqrt2}
\tag{27}
\]
be the oriented Hilbert--Schmidt orthonormal Hermitian Pauli basis.
Regard \(K\) as the Choi matrix of the Hermiticity-preserving logical
map
\[
 \Lambda:M_2\longrightarrow M_2,\qquad
 J(\Lambda)=K.
\tag{28}
\]
Its real Pauli transfer matrix is
\[
 T(\Lambda)_{\mu\nu}
 =\operatorname{Tr}\bigl(e_\mu\Lambda(e_\nu)\bigr).
\tag{29}
\]

### Theorem 6.1 (Choi-transfer determinant identity)

For every Hermitian \(K\in M_2\otimes M_2\), with the Choi convention
in (28),
\[
 \boxed{\qquad
 \det K^\Gamma=\det K-\det T(\Lambda).
 \qquad}
\tag{30}
\]
Consequently the full unrestricted three-copy theorem is equivalent
to
\[
 \boxed{\qquad
 \det T(\Lambda_{U,V})\leq\det K(U,V)
 \quad\hbox{for every physical pair }U,V.
 \qquad}
\tag{31}
\]

### Proof

Use the block notation (3) and write
\[
 B=H+iG,\qquad H=H^\dagger,\quad G=G^\dagger.
\tag{32}
\]
For a Hermitian \(2\times2\) matrix \(R\), write
\[
 R=r_0I+r_1X+r_2Y+r_3Z
\tag{33}
\]
and denote its real coefficient row by \(r=(r_0,r_1,r_2,r_3)\).
Let \(a,d,h,g\) be the rows belonging to \(A,D,H,G\), and put
\[
 \Delta=\det\begin{pmatrix}a\\d\\h\\g\end{pmatrix}.
\tag{34}
\]

The square-root-free orientation formula (14), together with
\[
 \operatorname{adj}R=r_0I-r_1X-r_2Y-r_3Z,
\tag{35}
\]
gives
\[
 \det K^\Gamma-\det K=8\Delta.
\tag{36}
\]
Here is a direct audit of the only sign-sensitive step.  If
\[
 P=A^{-1},\qquad Q=D^{-1},
\]
then
\[
\begin{aligned}
&\det A\det D\,
 \operatorname{Tr}\!\left[
 D^{-1}B^\dagger A^{-1}B
 -D^{-1}BA^{-1}B^\dagger\right]\\
&\qquad
 =4\,\operatorname{Im}
 \operatorname{Tr}\bigl(
 \operatorname{adj}D\,G\,
 \operatorname{adj}A\,H\bigr)
 =8\Delta.
\end{aligned}
\tag{37}
\]
The last equality follows by multiplying Pauli matrices:
\[
 \operatorname{Im}\operatorname{Tr}(R_1R_2R_3R_4)
 =
 2\left[
 (r_{10}r_2+r_{20}r_1)\cdot(r_3\times r_4)
 +(r_1\times r_2)\cdot(r_{30}r_4+r_{40}r_3)
 \right],
\tag{38}
\]
and then using the sign reversal in both adjugates (35).

The four columns of \(T(\Lambda)\), expressed in the coefficient
coordinates (33), are
\[
 a+d,\qquad 2h,\qquad2g,\qquad a-d,
\tag{39}
\]
because
\[
\begin{aligned}
\Lambda(I)&=A+D,&
\Lambda(X)&=B+B^\dagger=2H,\\
\Lambda(Y)&=i(B^\dagger-B)=2G,&
\Lambda(Z)&=A-D.
\end{aligned}
\tag{40}
\]
The change of columns from \((a,d,h,g)\) to (39) has determinant
\(-8\).  Therefore
\[
 \det T(\Lambda)=-8\Delta.
\tag{41}
\]
Equations (36) and (41) prove (30).  Combining (30) with (5)--(6)
proves (31).
\(\square\)

Thus the “orientation defect” is not an auxiliary coordinate
quantity:
\[
 \boxed{\qquad
 \det T(\Lambda)
 =\det A\det D\bigl(\|Z\|_2^2-\|X\|_2^2\bigr).
 \qquad}
\tag{42}
\]
If the physical logical channel reverses orientation,
\(\det T(\Lambda)\leq0\), endpoint positivity is automatic.  Only
orientation-preserving physical compressions remain.

## 7. Exact common-code Pluecker formula

The channel in Theorem 6.1 is intrinsically the compression of one
fixed three-fold physical map.  Define
\[
 \Psi_d(R)=\operatorname{Tr}(R)I_d-\frac12R^{\mathsf T}.
\tag{43}
\]
Its Choi matrix is
\[
 J(\Psi_d)=I-\frac12F.
\tag{44}
\]
For the three-copy qutrit problem put
\[
 \Psi=\Psi_3^{\otimes3}.
\tag{45}
\]
Directly from the Choi matrix elements in (1),
\[
\boxed{\qquad
 \Lambda_{U,V}(R)
 =
 V^\dagger\Psi\bigl(\overline U R U^{\mathsf T}\bigr)V.
 \qquad}
\tag{46}
\]

Let \({\mathfrak h}_m\) be the real Hilbert space of Hermitian
\(m\times m\) matrices.  Define the isometric operator-system
embeddings
\[
\begin{aligned}
 {\cal E}_{\overline U}:{\mathfrak h}_2&\longrightarrow
 {\mathfrak h}_{27},
 &R&\longmapsto\overline U R U^{\mathsf T},\\
 {\cal E}_{V}:{\mathfrak h}_2&\longrightarrow
 {\mathfrak h}_{27},
 &R&\longmapsto V R V^\dagger.
\end{aligned}
\tag{47}
\]
Compression is the adjoint of the second embedding, so (46) is
\[
 \Lambda_{U,V}
 ={\cal E}_V^*\Psi{\cal E}_{\overline U}.
\tag{48}
\]

Use the oriented Pauli basis (27) and set
\[
\begin{aligned}
 \Omega_{\overline U}
 &=
 \bigwedge_{\mu=0}^3{\cal E}_{\overline U}(e_\mu),\\
 \Omega_V
 &=
 \bigwedge_{\mu=0}^3{\cal E}_{V}(e_\mu).
\end{aligned}
\tag{49}
\]
These are unit decomposable four-vectors in
\(\bigwedge^4{\mathfrak h}_{27}\).  The determinant of a matrix of
pairings is an exterior pairing, so (48) gives the exact formula
\[
\boxed{\qquad
 \det T(\Lambda_{U,V})
 =
 \left\langle
 \Omega_V,\,
 \bigl(\bigwedge\nolimits^4\Psi\bigr)
 \Omega_{\overline U}
 \right\rangle.
 \qquad}
\tag{50}
\]

In a fixed orthonormal Hermitian eigenbasis
\((F_\alpha)\) of \(\Psi\), let
\[
 \Psi(F_\alpha)=\lambda_\alpha F_\alpha
\tag{51}
\]
and define the fourth Pluecker coordinates
\[
 p_I(U)=
 \det\left[
 \left\langle
 F_{\alpha_r},{\cal E}_U(e_\mu)
 \right\rangle
 \right]_{\substack{1\leq r\leq4\\0\leq\mu\leq3}},
 \qquad
 I=\{\alpha_1<\cdots<\alpha_4\}.
\tag{52}
\]
Then (50) is the finite weighted paired-Pluecker sum
\[
\boxed{\qquad
 \det T(\Lambda_{U,V})
 =
 \sum_{|I|=4}
 \left(\prod_{\alpha\in I}\lambda_\alpha\right)
 p_I(V)p_I(\overline U).
 \qquad}
\tag{53}
\]
All coordinates are real in the Hermitian basis, and
\[
 \sum_{|I|=4}p_I(U)^2=1
\tag{54}
\]
because (47) is isometric.

The vectors in (49) are much more special than arbitrary unit
decomposable four-vectors.  The complexification of
\(\operatorname{ran}{\cal E}_U\) is
\[
 \operatorname{ran}U\otimes
 \overline{\operatorname{ran}U},
\tag{55}
\]
so its top exterior vector is the paired Segre--Pluecker image of the
single decomposable code bivector
\[
 \omega_U=u_0\wedge u_1.
\tag{56}
\]
Thus (53) uses exactly the common left/right rank-two code geometry
missing from the abstract block obstruction.

The positive side of (31) has an equally intrinsic exterior form.
Put
\[
 \phi_{ab}=Y^{1/2}(u_a\otimes v_b),
\qquad a,b\in\{0,1\}.
\tag{57}
\]
Their Gram matrix is \(K(U,V)\).  Hence Gram--Cauchy--Binet gives
\[
\boxed{\qquad
 \det K(U,V)
 =
 \left\|
 \phi_{00}\wedge\phi_{01}\wedge
 \phi_{10}\wedge\phi_{11}
 \right\|^2.
 \qquad}
\tag{58}
\]

Combining (31), (50), and (58) produces a single lossless,
common-origin exterior inequality for the full three-copy endpoint:
\[
\boxed{
\left\langle
\Omega_V,\,
\bigl(\bigwedge\nolimits^4\Psi\bigr)\Omega_{\overline U}
\right\rangle
\leq
\left\|
\bigwedge_{a,b=0}^1
Y^{1/2}(u_a\otimes v_b)
\right\|^2.}
\tag{59}
\]
Unlike sector arithmetic, both sides in (59) arise from the same two
code bivectors \(\omega_U,\omega_V\).  A counterexample to (59) is
exactly a physical unrestricted three-copy witness; a proof of (59)
is exactly the desired theorem.

## Research log

- **2026-07-29 15:20 PDT.** Reduced the full two-plane
  partial-transpose determinant to the ordinary positive Gram
  determinant minus one scalar reversed-coherence orientation defect.
  Isolated the exact inequality (18), its automatic charts, and the
  abstract spectral-interval obstruction (21)--(26).
- **2026-07-29 17:40 PDT.** Identified the orientation defect with
  the determinant of the physical logical Pauli transfer matrix,
  proving \(\det K^\Gamma=\det K-\det T(\Lambda)\).
  Expressed that determinant as the paired fourth-exterior contraction
  (50)/(53) of the common left and right code Pluecker vectors, and
  expressed \(\det K\) as the Gram-volume square (58).  The remaining
  theorem is the single physical paired-Pluecker inequality (59).
