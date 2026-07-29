# Intersection one: the exact common-origin moment constraint

## Status

This note does **not** prove the intersection-one three-copy
inequality.  It identifies a nonlinear constraint which every physical
three-vector configuration satisfies and gives two exact no-go models
showing precisely where weaker versions of “common origin” stop.

Let \(w,u,v\) be the three vectors in the rank-one Gram reduction and
let \(T=\operatorname{span}\{w,u,v\}\).  In the generic
three-dimensional case choose an orthonormal basis \(e_1,e_2\) of
\(T\cap w^\perp\).  The isometry
\[
 W:\mathbb C^3\longrightarrow {\cal H},\qquad
 W|0\rangle=w,\quad W|1\rangle=e_1,\quad W|2\rangle=e_2
 \tag{1}
\]
simultaneously contains the two intersection-one planes
\(\operatorname{span}(w,u)\) and \(\operatorname{span}(w,v)\).  The
original \(u,v\) become arbitrary logical vectors \(x,y\in\mathbb C^3\);
they need not lie in \(\operatorname{span}\{|1\rangle,|2\rangle\}\).
Thus the construction below is a
three-dimensional common-origin construction, not the already solved
same-two-plane case.

Several explicit obstructions below use the orthogonal diagnostic slice
\(x=|1\rangle,y=|2\rangle\).  They are no-go results for proposed
proof mechanisms, not reductions of the full intersection-one stratum
to orthogonal triples.

The first theorem compresses the whole three-copy endpoint operator to
three single-site swap moments.  The second theorem records the first
nonlinear moment condition forced by the fact that all three moments
come from the **same** \(W\otimes W\).

Two complementary exact obstructions then show:

1. the correct swap-sector spectral windows, even together with a
   common commuting-symmetry dilation and the nonlinear leakage Gram
   condition, do not imply the desired crossed minor; and
2. requiring each of the three single-site moments separately to come
   from a genuine qutrit isometry still does not suffice.  An exact
   \(2\times2\) principal minor of the leakage Gram separates that model
   from simultaneous physical realizability.

Consequently the live datum is the conjunction of local
tensor-square/channel origin and simultaneous **rank-one Stinespring**
compatibility.  Neither separate channel origins nor a common
first-moment dilation can replace the shared underlying tensor.

The independent exact checker is
`verification/verify_n3_intersection_common_origin_moment.py`.

## 1. Three compressed swaps determine the endpoint compression

On two replicas of
\({\cal H}=H_1\otimes H_2\otimes H_3\), let \(F_i\) swap the two
copies of \(H_i\), and put
\[
 F_{\rm phys}=F_1F_2F_3.
 \tag{2}
\]
On two copies of \(E=\mathbb C^3\), let \(F\) be the logical swap and
set
\[
 J=W\otimes W,\qquad
 R_i=J^\dagger F_iJ.
 \tag{3}
\]
Because \(F_{\rm phys}J=JF\), one has
\[
 J^\dagger F_iF_jJ=R_kF
 \qquad(\{i,j,k\}=\{1,2,3\}).
 \tag{4}
\]
Indeed,
\[
 F_iF_j=F_kF_{\rm phys},
 \]
and \(F_k\) commutes with \(F_{\rm phys}\).  In particular each
\(R_i\) is self-adjoint and commutes with \(F\).

Let
\[
 Y=\prod_{i=1}^3\left(I-\frac12F_i\right),\qquad
 K=J^\dagger YJ,\qquad R=R_1+R_2+R_3.
 \tag{5}
\]
Expanding \(Y\) and using (4) gives the exact collapse
\[
 \boxed{\qquad
 K=I-\frac18F-\frac12R+\frac14RF.
 \qquad}
 \tag{6}
\]
Thus all degree-two replica information relevant at three copies is
contained in the sum of the three one-site moments.

The physical spectrum of \(Y\) gives
\[
 \frac18P_+\preceq K_+\preceq\frac98P_+,\qquad
 \frac38P_-\preceq K_-\preceq\frac{27}{8}P_-,
 \tag{7}
\]
where \(P_\pm=(I\pm F)/2\).

For the orthonormal diagnostic triple \(w=W|0\rangle\),
\(u=W|1\rangle\), \(v=W|2\rangle\), put
\[
 a=K_{00,00},\qquad b=K_{12,12},\qquad z=K_{02,10}.
 \tag{8}
\]
Then
\[
 a=Q_3(P_w),\qquad b=Q_3(|u\rangle\langle v|),\qquad
 z={\cal B}_3(P_w,|u\rangle\langle v|),
 \tag{9}
\]
up to the fixed harmless vectorization convention.  Hence the
intersection-one target on this slice is exactly
\[
 \boxed{\qquad
 ab-|z|^2\geq0,
 \qquad}
 \tag{10}
\]
the \((|00\rangle,|12\rangle)\) principal minor of \(K^\Gamma\).
For the full intersection-one problem, arbitrary logical
\(x,y\in\mathbb C^3\) give
\[
 K_{00,00}\,
 \langle x\otimes y,K(x\otimes y)\rangle
 \geq
 \left|\langle0\otimes y,K(x\otimes0)\rangle\right|^2.
 \tag{10a}
\]

## 2. The nonlinear leakage Gram

Let \(P=JJ^\dagger\) and define the three leakage operators
\[
 Z_i=(I-P)F_iJ.
 \tag{11}
\]
Their operator-valued Gram matrix is positive:
\[
 {\mathfrak G}=[Z_i^\dagger Z_j]_{i,j=1}^3\succeq0.
 \tag{12}
\]
The entries can be written entirely in terms of the compressed
moments.  On the diagonal,
\[
 Z_i^\dagger Z_i
 =J^\dagger F_i(I-P)F_iJ
 =I-R_i^2.
 \tag{13}
\]
For distinct \(i,j\), with remaining index \(k\),
\[
 \begin{aligned}
 Z_i^\dagger Z_j
 &=J^\dagger F_iF_jJ
   -J^\dagger F_iJJ^\dagger F_jJ\\
 &=R_kF-R_iR_j.
 \end{aligned}
 \tag{14}
\]
Therefore every physical common origin satisfies
\[
 \boxed{
 {\mathfrak G}_{ii}=I-R_i^2,\qquad
 {\mathfrak G}_{ij}=R_kF-R_iR_j\quad(i\ne j),\qquad
 {\mathfrak G}\succeq0.}
 \tag{15}
\]

In scalar form, (15) contains the nonlinear inequalities
\[
 \left|
 \langle x,(R_kF-R_iR_j)y\rangle
 \right|^2
 \leq
 \langle x,(I-R_i^2)x\rangle
 \langle y,(I-R_j^2)y\rangle.
 \tag{16}
\]
This is the first moment relation which is invisible if the three
single-site channels are studied independently.

## 3. Leakage positivity alone is still insufficient

In fact (15), even with one common commuting-symmetry dilation, carries
no more information about \(K\) than the sharp parity windows (7).

### Proposition 3.1

Let \(K=K^\dagger\) commute with \(F\) and satisfy (7).  Then there are
three commuting self-adjoint symmetries \(S_1,S_2,S_3\), an isometry
\({\cal J}\), and compressed moments
\[
 R_i={\cal J}^\dagger S_i{\cal J}
 \tag{17}
\]
such that
\[
 {\cal J}^\dagger S_1S_2S_3{\cal J}=F,\qquad
 {\cal J}^\dagger S_iS_j{\cal J}=R_kF,
 \tag{18}
\]
equation (6) holds, and the leakage Gram (15) is positive.

#### Proof

On the symmetric sector define four positive effects
\[
 \begin{aligned}
 E_{+++}&=\frac98P_+-K_+,\\
 E_{+--}=E_{-+-}=E_{--+}
 &=\frac13\left(K_+-\frac18P_+\right).
 \end{aligned}
 \tag{19}
\]
They sum to \(P_+\).  On the antisymmetric sector define
\[
 \begin{aligned}
 E_{---}&=\frac13\left(K_--\frac38P_-\right),\\
 E_{-++}=E_{+-+}=E_{++-}
 &=\frac13(P_--E_{---}).
 \end{aligned}
 \tag{20}
\]
They sum to \(P_-\).  All other effects are zero.  Thus the eight
\(E_\epsilon\) form a POVM, and their support obeys
\[
 \epsilon_1\epsilon_2\epsilon_3=F
 \tag{21}
\]
sector by sector.

Take the canonical Naimark isometry
\[
 {\cal J}x=\bigoplus_\epsilon E_\epsilon^{1/2}x
 \tag{22}
\]
and let \(S_i\) multiply the \(\epsilon\)-summand by \(\epsilon_i\).
Then the \(S_i\) are commuting symmetries and (18) follows directly.
Their identical first moments are
\[
 R_i=
 \left(\frac76P_+-\frac43K_+\right)
 +
 \left(\frac12P_--\frac49K_-\right).
 \tag{23}
\]
Substitution in (6) recovers \(K\).  Finally, the same leakage
calculation as in (11)--(15), with \({\cal J}\) in place of \(J\),
proves positivity of \({\mathfrak G}\).
\(\square\)

The crucial missing condition is that \({\cal J}\) in Proposition 3.1
must equal \(W\otimes W\), with the symmetries coming from local swaps.
That Veronese/tensor-square requirement is not implied by the moment
conditions.

### 3.2 Exact negative crossed minor

Here is a short rational example.  In the computational basis
\[
 00,01,02,10,11,12,20,21,22,
 \]
take
\[
 K=
 \begin{pmatrix}
 1/4&0&0&0&0&0&0&0&0\\
 0&5/8&1/8&0&0&0&3/8&0&0\\
 0&1/8&5/8&3/8&0&0&0&0&0\\
 0&0&3/8&5/8&0&0&1/8&0&0\\
 0&0&0&0&3/5&0&0&0&1/5\\
 0&0&0&0&0&2/5&0&0&0\\
 0&3/8&0&1/8&0&0&5/8&0&0\\
 0&0&0&0&0&0&0&2/5&0\\
 0&0&0&0&1/5&0&0&0&3/5
 \end{pmatrix}.
 \tag{24}
\]
It commutes with \(F\).  Its symmetric-sector spectrum is
\[
 \left\{\frac18,\frac14,\frac25,\frac25,\frac45,\frac98\right\},
 \tag{25}
\]
and its antisymmetric-sector spectrum is
\[
 \left\{\frac38,\frac25,\frac78\right\}.
 \tag{26}
\]
Thus (7) holds.  Proposition 3.1 supplies a common
commuting-symmetry dilation and a positive leakage Gram.

Nevertheless,
\[
 a=\frac14,\qquad b=\frac25,\qquad z=\frac38,
 \]
and hence
\[
 \boxed{\qquad
 ab-|z|^2=\frac1{10}-\frac9{64}=-\frac{13}{320}.
 \qquad}
 \tag{27}
\]
This is not a physical Werner witness.  It proves that the nonlinear
leakage relation and all replica-pair spectral data still do not
enforce the tensor-square common origin.

## 4. Separate one-cut channel origins are also insufficient

We now impose the opposite half of the missing structure.  Each
\(R_i\) below is individually the compression of a genuine swap by a
qutrit isometry, but the three isometries are not jointly compatible.

Let \(V_i:\mathbb C^3\to\mathbb C^2\otimes\mathbb C^2\) have the
following real \(4\times3\) matrices:
\[
 V_1=
 \begin{pmatrix}
 5/13&0&0\\
 0&1&0\\
 0&0&1\\
 -12/13&0&0
 \end{pmatrix},\quad
 V_2=
 \begin{pmatrix}
 1&0&0\\
 0&3/5&4/5\\
 0&-4/5&3/5\\
 0&0&0
 \end{pmatrix},\quad
 V_3=
 \begin{pmatrix}
 1&0&0\\
 0&5/13&0\\
 0&0&1\\
 0&12/13&0
 \end{pmatrix}.
 \tag{28}
\]
They obey \(V_i^\dagger V_i=I_3\).  If \(S_i\) swaps the first
\(\mathbb C^2\) factors of two copies, put
\[
 R_i=(V_i^\dagger\otimes V_i^\dagger)
 S_i(V_i\otimes V_i).
 \tag{29}
\]
Each \(R_i\) therefore has an exact one-cut tensor-square origin.  Its
complementary swap moment is \(R_iF\).  In particular all individual
Choi/partial-transpose Gram constraints hold.

Define \(K\) from these three \(R_i\)'s by (6).  Exact contraction gives
\[
 a=\frac{42961}{228488},\qquad
 b=\frac{48457}{105625},\qquad
 z=\frac9{25},
 \tag{30}
\]
and
\[
 \boxed{\qquad
 ab-|z|^2
 =-\frac{209202211}{4826809000}<0.
 \qquad}
 \tag{31}
\]
This \(K\) still obeys all the sharp physical parity windows (7).
For a compact exact certificate, use the orthogonal rational bases
\[
 00,11,22,01+10,02+20,12+21
 \quad\hbox{and}\quad
 01-10,02-20,12-21.
 \tag{32}
\]
The four shifted parity blocks
\[
 K_+-\frac18P_+,\quad
 \frac98P_+-K_+,\quad
 K_--\frac38P_-,\quad
 \frac{27}{8}P_--K_-
 \tag{33}
\]
have rational \(LDL^\dagger\) pivots, respectively,
\[
 \begin{aligned}
 &(1800/28561,\ 72/625,\ 72/169),\\
 &(26761/28561,\ 553/625,\ 481/553,\
   266/169,\ 2,\ 646370071/489137558),\\
 &(11637/4225,\ 56154/72839,\ 58125/3163342),\\
 &(13713/4225,\ 2964336/772499,\
   118483821/20873866).
 \end{aligned}
 \tag{34}
\]
All are positive.  The first block has rank three; the other displayed
pivots use full-rank principal blocks.  The verifier reconstructs the
four matrices and their exact factorizations.

### 4.1 The minimal nonlinear separator

The model (28)--(31) is excluded by one \(2\times2\) principal minor of
the common-origin leakage Gram.  Index the three block rows of
\({\mathfrak G}\) by \(i=0,1,2\), and inside each block use the logical
pair basis \(00,01,\ldots,22\).  On the two coordinates
\[
 (i=1,01),\qquad(i=2,01),
 \]
the Gram matrix (15) would have to contain
\[
 \begin{pmatrix}
 0&135/169\\
 135/169&144/169
 \end{pmatrix}.
 \tag{35}
\]
Its determinant is
\[
 \boxed{\qquad
 -\frac{18225}{28561}<0.
 \qquad}
 \tag{36}
\]
Equivalently, one diagonal leakage norm is zero while its proposed
cross inner product is nonzero.  This is the smallest possible exact
certificate that the three legitimate one-cut channels do not arise
from one common \(W\).

## 5. Even individual origin plus leakage positivity is insufficient

One can satisfy both abstractions at once and still violate the crossed
minor.  This shows that the rank-one common-Stinespring tensor is not a
cosmetic strengthening of the first-moment conditions.

Let \(V:\mathbb C^3\to\mathbb C^3\otimes\mathbb C^2\) be the rational
isometry
\[
 V=
 \begin{pmatrix}
 3/13&0&0\\
 0&20/29&21/29\\
 0&-21/29&20/29\\
 0&0&0\\
 12/13&0&0\\
 -4/13&0&0
 \end{pmatrix}.
 \tag{37}
\]
Let \(R\) be its genuine one-cut swap moment, as in (29), and set
\[
 R_1=R_2=R_3=R.
 \tag{38}
\]
On the logical symmetric sector the spectrum of \(R\) is
\[
 \left\{0,1,1,1,\frac{153}{169},
              \frac{3937}{28561}\right\},
 \tag{39}
\]
while on the logical antisymmetric sector it is
\[
 \left\{0,-\frac7{169},-\frac{153}{169}\right\}.
 \tag{40}
\]
Consequently
\[
 -\frac13P_+\preceq R_+\preceq P_+,\qquad
 -P_-\preceq R_-\preceq\frac13P_-.
 \tag{41}
\]

For three identical moments, the leakage Gram has diagonal block
\(D=I-R^2\) and off-diagonal block \(C=RF-R^2\).  Its two block
eigenvalues are
\[
 D-C=I-RF
 \tag{42}
\]
with multiplicity two, and
\[
 D+2C=I+2RF-3R^2
 \tag{43}
\]
with multiplicity one.  On the \(F=+1\) sector, (43) factors as
\[
 (I-R)(I+3R),
 \tag{44}
\]
and on the \(F=-1\) sector it factors as
\[
 (I+R)(I-3R).
 \tag{45}
\]
Equations (39)--(41) therefore prove
\({\mathfrak G}\succeq0\) exactly.  Equivalently, Proposition 3.1
provides a common commuting-symmetry dilation for this identical
triple.  At the same time each \(R_i\) separately has the genuine
tensor-square origin (37).

Nevertheless, the formal \(K\) from (6) has
\[
 a=\frac{30289}{228488},\qquad
 b=\frac{442681}{707281},\qquad
 z=\frac{89145}{142129},
 \tag{46}
\]
and
\[
 \boxed{\qquad
 ab-|z|^2
 =-\frac{50166283391}{161605221128}<0.
 \qquad}
 \tag{47}
\]
Its parity spectrum lies in (7), as follows directly from (39)--(41)
and (6).

This is again a formal obstruction, not a physical Werner witness.
The next lemma proves exactly that no single tripartite \(W\) realizes
the three copies of \(R\).  What (47) proves is that the conjunction of

1. a genuine tensor-square origin for each one-cut moment;
2. the complement identities;
3. a positive simultaneous leakage Gram; and
4. all sharp parity spectral windows

still does not algebraically imply the target.  A proof must use that
the three one-cut channels are compatible marginals of **one common
rank-one Stinespring tensor**.

### 5.1 An exact common-Stinespring separator

The failure of common marginal compatibility is visible in a short
inequality of independent use.

#### Lemma 5.1 (product-column compatibility)

Let \(y,z\in H_1\otimes H_2\otimes H_3\) be orthonormal.  Suppose every
one-site reduction of \(P_y\) is pure.  Put
\[
 \rho_i^z=\operatorname{Tr}_{\bar i}P_z,\qquad
 \tau_i=\operatorname{Tr}_{\bar i}|z\rangle\langle y|.
 \tag{48}
\]
Then
\[
 \boxed{\qquad
 2\sum_{i=1}^3\|\tau_i\|_2^2
 \leq
 \sum_{i=1}^3
 \operatorname{Tr}(\rho_i^z\rho_i^y).
 \qquad}
 \tag{49}
\]

#### Proof

Purity of all three reductions implies
\[
 y=b_1\otimes b_2\otimes b_3.
 \tag{50}
\]
Let \(P_i=|b_i\rangle\langle b_i|\), inserted at site \(i\).  Direct
contraction gives
\[
 \operatorname{Tr}(\rho_i^z\rho_i^y)
 =\langle z,P_i z\rangle,
 \qquad
 \|\tau_i\|_2^2
 =\langle z,P_jP_k z\rangle.
 \tag{51}
\]
The commuting projection
\[
 N=\sum_iP_i-2\sum_{i<j}P_iP_j
 \tag{52}
\]
has eigenvalues \(0,1,0,-3\) on the sectors with respectively
\(0,1,2,3\) occupied \(b\)-coordinates.  Its only negative sector is
the line \(\mathbb Cy\).  Since \(z\perp y\),
\(\langle z,Nz\rangle\geq0\), which is exactly (49).
\(\square\)

Apply the lemma to the identical-channel model.  In the logical vectors
\[
 z=|0\rangle,\qquad
 y=\frac{20|1\rangle+21|2\rangle}{29},
 \tag{53}
\]
the isometry (37) gives
\[
 Vy=|0\rangle\otimes|1\rangle
 \tag{54}
\]
and
\[
 Vz=\frac1{13}
 \left(3|00\rangle+12|20\rangle-4|21\rangle\right).
 \tag{55}
\]
Thus its output channel has
\[
 \operatorname{Tr}(\rho^z\rho^y)=\frac9{169},\qquad
 \|\mathcal N(|z\rangle\langle y|)\|_2^2=\frac{16}{169}.
 \tag{56}
\]
If three copies of the moment \(R\) came from one common tripartite
isometry \(W\), the moment identities would force (56) at every site,
while purity would force \(Wy\) to be product.  Lemma 5.1 would then
read
\[
 2\cdot3\cdot\frac{16}{169}
 \leq
 3\cdot\frac9{169},
 \tag{57}
\]
that is \(96\leq27\), a contradiction.

Equation (49) is therefore an exact common-rank-one-Stinespring
realizability inequality which is independent of the leakage Gram.  It
separates the strongest formal model in this note from the physical
variety.

## 6. The strictly smaller remaining lemma

The intersection-one problem can now be stated without the earlier
independent \(G,T\) abstraction.

> **Common-origin crossed-minor lemma.**  Let
> \(W:\mathbb C^3\to H_1\otimes H_2\otimes H_3\) be an isometry, define
> \(R_i\) by (3), and define \(K\) by (6).  Then for every unit
> \(x,y\in\mathbb C^3\),
> \[
> K_{00,00}\,
> \langle x\otimes y,K(x\otimes y)\rangle
> \geq
> \left|
> \langle 0\otimes y,K(x\otimes0)\rangle
> \right|^2.
> \tag{58}
> \]

Compared with the original three-vector formula, (37) has eliminated
all subset contractions in favor of three Hermitian contractions
\(R_i\).  These obey:

1. the linear complement identities (4);
2. the individual channel/tensor-square Gram constraints;
3. the simultaneous nonlinear leakage constraint (15); and
4. the stronger fact that all three channel Choi tensors are marginals
   of one rank-one Stinespring tensor \(W\).

Sections 3--5 prove successively that the parity windows, the
simultaneous leakage Gram, and even separate tensor-square channel
origins do not imply (58), alone or in the first-moment conjunction
described above.  Lemma 5.1 supplies one exact consequence of the
common rank-one Stinespring compatibility in item (4), but only on the
product-column boundary.  A global family of such compatibility
inequalities is the remaining frontier.
