# Qutrit reduction algebra: inverse cones and complement-pair obstructions

**Research log — 2026-07-28 12:27 PDT**

**Checkpoint — 2026-07-28 12:32 PDT.**  The product-code parity formula
(25) and the simultaneous-spectral coefficients (46) were independently
replayed with exact rational arithmetic for \(1\leq n\leq8\).  The replay
was an arithmetic audit; their proofs below are uniform in \(n\).

This note audits whether the minimal polynomial of the qutrit reduction
map, together with positivity of its full tensor power, can prove the
rank-two projector endpoint inequality.

The outcome is mixed:

- there are useful exact inverse, dual-cone, complement, and orbit-Gram
  identities;
- the most direct inverse-cone proof fails on an odd-Hamming product
  equality code;
- individual even reductions and same-parity complement pairs can be
  negative on exact rank-two projections, even though the full reduction
  is positive;
- the full reduction-orbit Gram cone is strictly too weak without
  positivity and idempotence constraints;
- product-eigenvector codes do satisfy a much stronger partial-reduction
  cone, and their endpoint value and equality cases can be classified
  exactly.

No all-copy theorem or counterexample to the endpoint inequality is
obtained.

## 1. The local algebra

On \(M_3\), define
\[
\mathcal R(X)=\operatorname{Tr}(X)I_3-X.                  \tag{1}
\]
It is self-adjoint for the Hilbert--Schmidt inner product.  Since
\[
\operatorname{Tr}\mathcal R(X)=2\operatorname{Tr}X,
\]
we have
\[
\mathcal R^2(X)
=2\operatorname{Tr}(X)I_3-\mathcal R(X)
=\operatorname{Tr}(X)I_3+X
=\mathcal R(X)+2X.
\]
Thus
\[
\boxed{\quad
\mathcal R^2=\mathcal R+2I,\qquad
(\mathcal R-2I)(\mathcal R+I)=0,\qquad
\mathcal R^{-1}=\frac{\mathcal R-I}{2}.
\quad}                                                     \tag{2}
\]

The orthogonal decomposition
\[
M_3=\mathbb CI_3\oplus M_3^0                              \tag{3}
\]
diagonalizes \(\mathcal R\): its eigenvalue is \(2\) on the scalar
direction and \(-1\) on the traceless direction.  The inverse eigenvalues
are \(1/2\) and \(-1\).

Let \(T\) denote transpose in a fixed basis.  The Choi matrix of
\(\mathcal R\circ T\) is
\[
I-F=2A\succeq0,                                           \tag{4}
\]
where \(F\) is the flip and \(A=(I-F)/2\) is the antisymmetric projector.
Hence \(\mathcal R\) is completely copositive.  On
\[
H=(\mathbb C^3)^{\otimes n},
\]
write \(\mathcal R_i\) for the reduction on site \(i\), and
\[
\mathcal R_{[n]}=\prod_{i=1}^n\mathcal R_i.
\]
The tensor product of (4) is the Choi matrix after one **global**
transpose.  Therefore
\[
\boxed{\quad
X\succeq0\ \Longrightarrow\
\mathcal R_{[n]}(X)\succeq0.
\quad}                                                     \tag{5}
\]
Partial products \(\mathcal R_S\), tensored with the identity on
\(S^c\), do not inherit (5).

### 1.1 Exact boundary of the copositive polynomial family

For real \(a,b\), set
\[
\Phi_{a,b}=aI+b\mathcal R.
\]
The Choi matrix of \(\Phi_{a,b}\circ T\) is
\[
bI+(a-b)F.
\]
Its symmetric and antisymmetric eigenvalues are \(a\) and \(2b-a\).
Consequently
\[
\boxed{\quad
\Phi_{a,b}\text{ is completely copositive}
\quad\Longleftrightarrow\quad
0\leq a\leq2b.
\quad}                                                     \tag{6}
\]
In particular, \(\mathcal R+tI\) is completely copositive for
\(0\leq t\leq2\).

The inverse lies strictly outside this cone:
\[
\mathcal R^{-1}=-\frac12I+\frac12\mathcal R.
\]
The Choi matrix of \(\mathcal R^{-1}\circ T\) is
\[
\frac12I-F,
\]
with eigenvalues \(-1/2\) on the symmetric subspace and \(3/2\) on the
antisymmetric subspace.  Every tensor power has Choi eigenvalues of both
signs.  Thus
\[
\boxed{\quad
(\mathcal R^{-1})^{\otimes n}
\text{ is not globally completely copositive for any }n\geq1.
\quad}                                                     \tag{7}
\]

## 2. The even-reduction target

For \(S\subseteq[n]\), put
\[
\mathcal R_S=\prod_{i\in S}\mathcal R_i,\qquad
a_S(P)=\langle P,\mathcal R_S(P)\rangle.                  \tag{8}
\]
The endpoint map is
\[
\mathcal L=\frac12(I-\mathcal R).
\]
For a rank-two orthogonal projection \(P\), the grouped rank-two
contribution cancels, and elementary parity expansion gives
\[
\boxed{\quad
Q_n(P)=2^{1-n}E_n(P),\qquad
E_n(P):=
\sum_{\substack{S\subseteq[n]\\|S|\ {\rm even}\\|S|\geq2}}
a_S(P).
\quad}                                                     \tag{9}
\]
The question in this note is whether (5) and (2) force \(E_n(P)\geq0\).

The full term is nonnegative:
\[
a_{[n]}(P)
=\operatorname{Tr}\!\left[P\,\mathcal R_{[n]}(P)\right]
\geq0.                                                     \tag{10}
\]
The proper even terms need not be nonnegative.

## 3. Exact inverse and complement identities

For every \(S\subseteq[n]\), commutativity and invertibility give
\[
\boxed{\quad
\mathcal R_{S^c}
=\mathcal R_{[n]}\mathcal R_S^{-1},\qquad
\mathcal R_S^{-1}
=2^{-|S|}\prod_{i\in S}(\mathcal R_i-I).
\quad}                                                     \tag{11}
\]
Taking Hilbert--Schmidt inner products and using self-adjointness gives
\[
\boxed{\quad
a_{S^c}(P)
=\left\langle\mathcal R_{[n]}(P),
  \mathcal R_S^{-1}(P)\right\rangle.
\quad}                                                     \tag{12}
\]
Thus
\[
\boxed{\quad
a_S(P)+a_{S^c}(P)
=\left\langle\mathcal R_{[n]}(P),
\bigl(\mathcal R_{S^c}^{-1}+\mathcal R_S^{-1}\bigr)(P)
\right\rangle.
\quad}                                                     \tag{13}
\]
Since the first factor in (12)--(13) is positive by (5), positivity of
the corresponding inverse image would be sufficient.  Sections 5 and 6
give exact counterexamples to both inverse-image assertions.

There is a second, always valid complement identity:
\[
\boxed{\quad
\left\langle\mathcal R_S(P),\mathcal R_{S^c}(P)\right\rangle
=\left\langle P,\mathcal R_{[n]}(P)\right\rangle
=a_{[n]}(P)\geq0.
\quad}                                                     \tag{14}
\]
Thus every pair of complementary reduction-orbit vectors makes a
nonnegative Hilbert--Schmidt angle.  This does **not** control the
different star-shaped quantities
\(\langle P,\mathcal R_S(P)\rangle\) appearing in \(E_n(P)\).

The inverse pairing with the same subset is also exact:
\[
\boxed{\quad
\left\langle\mathcal R_S(P),\mathcal R_S^{-1}(P)\right\rangle
=\langle P,P\rangle=2.
\quad}                                                     \tag{15}
\]
Again, neither factor in (15) need be positive.

## 4. The natural inverse preimage cone

Let \(\mathsf{PSD}\) be the positive semidefinite cone on \(H\), and define
\[
\mathfrak C_n
:=\mathcal R_{[n]}^{-1}(\mathsf{PSD})
=\{X=X^\dagger:\mathcal R_{[n]}(X)\succeq0\}.              \tag{16}
\]
Because \(\mathcal R_{[n]}\) is invertible and self-adjoint and
\(\mathsf{PSD}\) is self-dual,
\[
\boxed{\quad
\mathfrak C_n^*
=\mathcal R_{[n]}(\mathsf{PSD})
=\{Y:\mathcal R_{[n]}^{-1}(Y)\succeq0\}.
\quad}                                                     \tag{17}
\]
Indeed, if \(X=\mathcal R_{[n]}(Z)\), \(Z\succeq0\), and
\(Y\in\mathfrak C_n\), then
\[
\langle X,Y\rangle
=\langle Z,\mathcal R_{[n]}(Y)\rangle\geq0.
\]
The converse follows by applying the same argument to the inverse
linear isomorphism.

Now define
\[
B_n(P):=\prod_{i=1}^n(I-\mathcal R_i)(P).                 \tag{18}
\]
Then
\[
2^nQ_n(P)=\langle P,B_n(P)\rangle,                        \tag{19}
\]
and the minimal polynomial gives
\[
\mathcal R_i(I-\mathcal R_i)
=\mathcal R_i-\mathcal R_i^2=-2I.
\]
Therefore
\[
\boxed{\quad
\mathcal R_{[n]}B_n(P)=(-2)^nP.
\quad}                                                     \tag{20}
\]

For even \(n\), (20) places \(B_n(P)\) in \(\mathfrak C_n\).  A dual-cone
proof of the endpoint would follow immediately if every rank-two
projection satisfied
\[
P\in\mathfrak C_n^*
\quad\Longleftrightarrow\quad
\mathcal R_{[n]}^{-1}(P)\succeq0.                          \tag{21}
\]
The equivalence is exact, but the claimed inclusion is false; see
Section 5.

For odd \(n\), (20) instead gives \(-B_n(P)\in\mathfrak C_n\).  Moreover,
\(\mathfrak C_n^*=\mathcal R_{[n]}(\mathsf{PSD})\) is contained in
\(\mathsf{PSD}\) by (5), so \(-P\notin\mathfrak C_n^*\) for a nonzero
projection.  Thus this fixed cone has the wrong orientation at every odd
copy number.

This proves an exact limitation: full-reduction positivity does generate
a canonical cone pairing, but the rank-two projection lies on the wrong
side of its dual inclusion.

## 5. Product-code theorem and inverse-cone counterexample

Let
\[
u=\bigotimes_{i=1}^nu_i,\qquad
v=\bigotimes_{i=1}^nv_i,\qquad
\langle u,v\rangle=0,
\]
and
\[
P=|u\rangle\langle u|+|v\rangle\langle v|.
\]
Put
\[
t_i=|\langle u_i,v_i\rangle|^2\in[0,1].
\]
Global orthogonality says \(\prod_it_i=0\).

For local rank-one projectors \(p_x,p_y\),
\[
\langle p_x,\mathcal R(p_y)\rangle
=1-|\langle x,y\rangle|^2,\qquad
\langle p_x,p_y\rangle=|\langle x,y\rangle|^2.            \tag{22}
\]
The two self-pair contributions vanish whenever \(S\neq\varnothing\).
The two cross orientations then factorize, giving
\[
\boxed{\quad
a_S(P)
=2\prod_{i\in S}(1-t_i)\prod_{i\notin S}t_i
\quad(S\neq\varnothing).
\quad}                                                     \tag{23}
\]
In particular every partial reduction image is positive:
\[
\mathcal R_S(P)
=\mathcal R_S(|u\rangle\langle u|)
 +\mathcal R_S(|v\rangle\langle v|)
\succeq0,                                                  \tag{24}
\]
because it is a sum of tensor products of local projectors
\(p_x\) and \(I-p_x\).

The products in (23) are the atom weights of independent Bernoulli
variables with inclusion probabilities \(1-t_i\).  The probability of an
even subset is
\[
\frac12\left[1+\prod_{i=1}^n(2t_i-1)\right].
\]
The empty atom has weight \(\prod_it_i=0\).  Consequently
\[
\boxed{\quad
E_n(P)=1+\prod_{i=1}^n(2t_i-1),\qquad
Q_n(P)=2^{1-n}
\left[1+\prod_{i=1}^n(2t_i-1)\right]\geq0.
\quad}                                                     \tag{25}
\]
Equality holds exactly when every \(t_i\in\{0,1\}\) and an odd number of
the \(t_i\)'s are zero.  Thus the familiar odd-Hamming product codes are
not merely examples; they are all equality cases in this
product-eigenvector class.

The full copositive shadow also factorizes.  For \(s_i\geq0\),
\[
\boxed{\quad
\left\langle P,
\prod_i(\mathcal R_i+s_iI)(P)\right\rangle
=2\prod_i s_i+
2\prod_i\bigl(1+(s_i-1)t_i\bigr)\geq0.
\quad}                                                     \tag{26}
\]
This supplies an exact equality test for any attempted continuation from
the copositive interval to the inverse point \(s_i=-1\).

### 5.1 Exact inverse-cone obstruction

Choose a rank-two local qutrit projection \(Q\), a local rank-one
projection \(p\), and, for \(n\geq2\), let
\[
P_n=Q_1\otimes p_2\otimes\cdots\otimes p_n.               \tag{27}
\]
This is a rank-two orthogonal projection spanned by two product vectors
which differ at only one site, so (25) gives
\[
Q_n(P_n)=0.                                                \tag{28}
\]
The inverse formula (2) gives
\[
\mathcal R^{-1}(Q)=I-Q,\qquad
\mathcal R^{-1}(p)=\frac12I-p.                             \tag{29}
\]
Hence
\[
\boxed{\quad
\mathcal R_{[n]}^{-1}(P_n)
=(I-Q)\otimes
\bigotimes_{i=2}^n\left(\frac12I-p_i\right).
\quad}                                                     \tag{30}
\]
Each flag factor in (30) has eigenvalue \(-1/2\) on
\(\operatorname{ran}p_i\) and \(+1/2\) on its orthogonal complement.
Thus (30) has both positive and negative eigenvalues for every \(n\geq2\).
Multiplication by any global sign leaves it indefinite.

Therefore the proposed rank-two inclusion (21), its signed variant, and
positivity of \(B_n(P_n)=(-2)^n\mathcal R_{[n]}^{-1}(P_n)\) are all false.
Crucially, the counterexample is an exact endpoint equality code, so these
cones are not merely quantitatively too strong: they exclude a mandatory
boundary family.

## 6. Exact entangled-code obstructions to termwise and complement pairing

Let
\[
Q=|0\rangle\langle0|+|1\rangle\langle1|
\]
on the first qutrit and let
\[
|\phi\rangle_{23}
=\frac{|00\rangle+|11\rangle}{\sqrt2},\qquad
\phi=|\phi\rangle\langle\phi|.
\]
Put
\[
P^{(3)}=Q_1\otimes\phi_{23}.                               \tag{31}
\]
This is a rank-two orthogonal projection.

The relevant one-factor quadratic values are
\[
\langle Q,Q\rangle=2,\qquad
\langle Q,\mathcal R(Q)\rangle=2,                          \tag{32}
\]
\[
\langle\phi,\phi\rangle=1,\qquad
\langle\phi,\mathcal R_2(\phi)\rangle
=\langle\phi,\mathcal R_3(\phi)\rangle=-\frac12,\qquad
\langle\phi,\mathcal R_2\mathcal R_3(\phi)\rangle=1.       \tag{33}
\]
For example,
\[
\langle\phi,\mathcal R_2(\phi)\rangle
=\operatorname{Tr}(\operatorname{Tr}_2\phi)^2-1
=\frac12-1.
\]
Tensor-factorization gives the full table
\[
\begin{array}{c|rrrrrrrr}
S&\varnothing&1&2&3&12&13&23&123\\ \hline
a_S(P^{(3)})&2&2&-1&-1&-1&-1&2&2.
\end{array}                                                \tag{34}
\]
The even-reduction sum is
\[
-1-1+2=0.                                                  \tag{35}
\]

This one table gives several exact cone counterexamples.

1. Since \(a_{12}=-1\), the operator
   \(\mathcal R_1\mathcal R_2(P^{(3)})\) is not positive.  Thus the cone
   \(\mathcal R_S(P)\succeq0\) for every even \(S\) does not contain all
   rank-two projections.
2. The complement pair \(S=12,S^c=3\) has
   \[
   a_{12}+a_3=-2<0.                                       \tag{36}
   \]
   Nevertheless, the true complement-orbit angle (14) is
   \[
   \left\langle\mathcal R_{12}(P^{(3)}),
   \mathcal R_3(P^{(3)})\right\rangle
   =a_{123}=2>0.                                          \tag{37}
   \]
   Hence the positive angle supplied by global copositivity does not
   control either star term or their sum.
3. By (12), the negative value \(a_3=-1\) means that
   \(\mathcal R_{12}^{-1}(P^{(3)})\) has negative
   Hilbert--Schmidt pairing with the positive operator
   \(\mathcal R_{123}(P^{(3)})\).  It therefore cannot be positive.

For an obstruction involving complements of the **same parity**, append a
pure product flag:
\[
p_4=|0\rangle\langle0|,\qquad
P^{(4)}=P^{(3)}\otimes p_4.                               \tag{38}
\]
Since
\[
\langle p_4,\mathcal R(p_4)\rangle=0,
\]
every \(a_S(P^{(4)})\) with \(4\in S\) vanishes, while the values not
containing \(4\) remain those in (34).  In particular,
\[
\boxed{\quad
a_{12}(P^{(4)})+a_{34}(P^{(4)})=-1+0=-1.
\quad}                                                     \tag{39}
\]
The total even-reduction sum still vanishes:
\[
E_4(P^{(4)})
=a_{12}+a_{13}+a_{23}=(-1)+(-1)+2=0.                     \tag{40}
\]

For even \(n\), a tempting proof is to pair every proper even \(S\) with
its even complement \(S^c\), use \(a_{[n]}\geq0\), and prove each pair
nonnegative.  Equation (39) refutes that program already at \(n=4\).
It also refutes the operator cone
\[
\mathcal R_{12}(P)+\mathcal R_{34}(P)\succeq0,
\]
because its Hilbert--Schmidt pairing with \(P^{(4)}\succeq0\) is negative.
By relabelling the flagged construction, either member of a complement
pair can carry the negative term.  Thus no positive weighted two-term
complement pairing can be universal.

Finally, (13) and (39) imply that the inverse-pair image
\[
\bigl(\mathcal R_{12}^{-1}+\mathcal R_{34}^{-1}\bigr)
(P^{(4)})
\]
is not positive: its inner product with the positive
\(\mathcal R_{[4]}(P^{(4)})\) equals \(-1\).

## 7. The exact reduction-orbit Gram cone

The minimal polynomial does generate a closed positive semidefinite
moment matrix.  Let
\[
X_S=\mathcal R_S(P).
\]
Then \(G=(G_{S,T})_{S,T\subseteq[n]}\), with
\[
G_{S,T}=\langle X_S,X_T\rangle,
\]
is a Gram matrix and hence positive semidefinite.  Reducing repeated
factors with \(\mathcal R_i^2=\mathcal R_i+2I\) gives
\[
\boxed{\quad
G_{S,T}
=\sum_{J\subseteq S\cap T}
2^{|S\cap T|-|J|}
a_{S\triangle T\ \cup J}.
\quad}                                                     \tag{41}
\]
Two useful diagonal consequences are
\[
\boxed{\quad
\|\mathcal R_S(P)\|_2^2
=\sum_{J\subseteq S}2^{|S|-|J|}a_J\geq0,
\quad}                                                     \tag{42}
\]
and, because
\[
(\mathcal R^{-1})^2=\frac{3I-\mathcal R}{4},
\]
\[
\boxed{\quad
\|\mathcal R_S^{-1}(P)\|_2^2
=4^{-|S|}
\sum_{J\subseteq S}3^{|S|-|J|}(-1)^{|J|}a_J\geq0.
\quad}                                                     \tag{43}
\]
The negative values in (34) satisfy all these Gram inequalities.  Thus
norm-square positivity does not restore termwise signs.

### 7.1 Simultaneous spectral form

Decompose operator Hilbert space using (3).  For \(T\subseteq[n]\), let
\(P_T\) be the component scalar exactly on \(T^c\) and traceless exactly
on \(T\), and put
\[
w_T=\|P_T\|_2^2\geq0.
\]
Then
\[
\boxed{\quad
a_S
=\sum_{T\subseteq[n]}
2^{|S\setminus T|}(-1)^{|S\cap T|}w_T.
\quad}                                                     \tag{44}
\]
Conversely, nonnegative \(w_T\)'s give an abstract Gram representation
of (41).  Thus the orbit-Gram cone is exactly the nonnegative
simultaneous-spectral cone; it contains no projection idempotence by
itself.

Summing (44) over the nonempty even subsets gives
\[
E_n=\sum_{T\subseteq[n]}c_{n,|T|}w_T,                     \tag{45}
\]
where
\[
\boxed{\quad
c_{n,0}=\frac{3^n+(-1)^n}{2}-1,
\qquad
c_{n,t}=(-1)^{n-t}2^{t-1}-1\quad(t\geq1).
\quad}                                                     \tag{46}
\]
To prove (46), assign the local eigenvalue \(2\) outside \(T\) and
\(-1\) inside \(T\).  The sum over all even subsets is
\[
\frac12\left[
\prod_i(1+\lambda_i)+\prod_i(1-\lambda_i)
\right],
\]
and one then subtracts the empty subset.

The coefficients (46) have both signs.  Therefore Gram positivity and the
minimal polynomial alone cannot prove \(E_n\geq0\).

There is an exact rank-two-moment counterexample at \(n=3\).  Set
\[
w_\varnothing=\frac4{27},\qquad
w_{\{1,2\}}=\frac{50}{27},\qquad
w_T=0\ \text{otherwise}.                                  \tag{47}
\]
These weights satisfy the trace and norm moments of a rank-two projection:
\[
w_\varnothing=\frac{|\operatorname{Tr}P|^2}{3^3},
\qquad
\sum_Tw_T=2.                                               \tag{48}
\]
They also give a positive full-reduction quadratic form,
\[
\sum_T2^{3-|T|}(-1)^{|T|}w_T
=8\frac4{27}+2\frac{50}{27}
=\frac{44}{9}>0.                                          \tag{49}
\]
But \(c_{3,0}=12\) and \(c_{3,2}=-3\), so
\[
\boxed{\quad
E_3
=12\frac4{27}-3\frac{50}{27}
=-\frac{34}{9}<0.
\quad}                                                     \tag{50}
\]
The vector (47) is not asserted to come from a positive projection.  Its
role is exact and limited: it proves that the minimal-polynomial orbit
Gram cone, even with the rank-two trace and norm moments and the
nonnegative full-reduction quadratic form, is insufficient.  A successful
argument must use operator positivity and nonlinear idempotence, not only
the orbit moment matrix.

## 8. Cone audit

The proposed routes have the following exact status.

1. **Full reduction image.**  The theorem
   \(\mathcal R_{[n]}(P)\succeq0\) is true, but it yields only the
   complement angle (14), not the star terms in \(E_n\).
2. **All even partial images.**  False by
   \(\mathcal R_{12}(P^{(3)})\not\succeq0\).
3. **Same-parity complement-pair positivity.**  False by (39), already
   for a rank-two projection at \(n=4\).
4. **Inverse preimage/dual-cone inclusion.**  False on the product
   equality family (27)--(30).
5. **Positive inverse-pair image.**  False by (13) and (39).
6. **Reduction-orbit Gram cone.**  The PSD Gram identities
   (41)--(43) are true, but (47)--(50) are an exact moment-cone
   counterexample to sufficiency.
7. **Product-eigenvector cone.**  True: all partial reductions are
   positive, (25) proves the endpoint, and equality is exactly the
   odd-Hamming orthogonal/identical family.

The surviving possibility is a cone that retains positivity and
idempotence of the common rank-two projection while allowing cyclic
cancellation among several noncomplementary even reductions.  Neither the
local minimal polynomial nor global complete copositivity encodes that
nonlinear compatibility on its own.
