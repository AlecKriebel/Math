# Exact block-Gram collapse at a three-copy Haar equality

## Status

This note proves an exact nonlinear consequence of the local Haar
equality
\[
 h_i(A,B)=\gamma\left(
 \langle A,B\rangle_{\rm HS}
 -\frac12\overline{\operatorname{Tr}A}\operatorname{Tr}B
 \right),\qquad A,B\in M_3.                              \tag{1}
\]
Write a three-copy coefficient matrix in \(3\times3\) blocks at the
site \(i\):
\[
 C=(C_{ab})_{a,b=0}^2,\qquad C_{ab}\in M_9,
 \tag{2}
\]
and let
\[
 {\cal B}_2(X,Y)
 =\left\langle X,{\cal L}^{\otimes2}(Y)\right\rangle_{\rm HS},
 \qquad
 {\cal L}(Y)=Y-\frac12\operatorname{Tr}(Y)I_3.            \tag{3}
\]
Then (1) forces the complete \(9\times9\) block Gram tensor to be
\[
 \boxed{\qquad
 {\cal B}_2(C_{ab},C_{cd})
 =\gamma\,\delta_{ab}\delta_{cd}.
 \qquad}                                                  \tag{4}
\]
There is no residual free tensor in (4).

Consequently, the eight-dimensional traceless coefficient space maps
to a totally isotropic subspace for \({\cal B}_2\), and
\[
 Q_2(\operatorname{Tr}_iC)=9\gamma.                       \tag{5}
\]
For the formal negative Haar equality in the current three-copy
program, \(\gamma=1/12\), so (5) would read
\[
 Q_2(\operatorname{Tr}_iC)=\frac34
 \quad\text{at every site}.                               \tag{6}
\]

The result does not by itself exclude a physical full-support
rank-two matrix.  It reduces that question to a common-factor
realizability problem recorded in Section 5.

The dependency-free exact checker is
`verification/verify_n3_haar_block_gram_collapse.py`.

## 1. Block expansion of the local form

Fix the physical site and suppress its label.  Left multiplication by
\(A\in M_3\) gives
\[
 (A^{(i)}C)_{rp}=\sum_s A_{rs}C_{sp}.                     \tag{7}
\]
The one-site recursion for the polarized endpoint form is
\[
\begin{aligned}
 h_i(A,B)
 &=
 \sum_{r,p}
 {\cal B}_2\bigl((A^{(i)}C)_{rp},(B^{(i)}C)_{rp}\bigr)\\
 &\quad
 -\frac12{\cal B}_2\left(
 \sum_r(A^{(i)}C)_{rr},
 \sum_q(B^{(i)}C)_{qq}\right).
                                                               \tag{8}
\end{aligned}
\]
Put
\[
 \beta_{sp,tq}={\cal B}_2(C_{sp},C_{tq}),\qquad
 G_{st}=\sum_p\beta_{sp,tp}.                              \tag{9}
\]
The coefficient of
\(\overline{A_{rs}}B_{qt}\) in (8) is exactly
\[
 K_{rs,qt}
 =\delta_{rq}G_{st}-\frac12\beta_{sr,tq}.                 \tag{10}
\]
On the other hand, the coefficient of the same monomial in (1) is
\[
 \gamma\delta_{rq}\delta_{st}
 -\frac\gamma2\delta_{rs}\delta_{qt}.                     \tag{11}
\]
Therefore (1) is equivalent to the eighty-one linear identities
\[
 \delta_{rq}G_{st}-\frac12\beta_{sr,tq}
 =
 \gamma\delta_{rq}\delta_{st}
 -\frac\gamma2\delta_{rs}\delta_{qt}.                     \tag{12}
\]

## 2. The collapse is unique

Solving (12) first for the uncontracted tensor gives
\[
 \beta_{sr,tq}
 =
 2\delta_{rq}(G_{st}-\gamma\delta_{st})
 +\gamma\delta_{rs}\delta_{qt}.                           \tag{13}
\]
Set \(q=r\) and sum over \(r=0,1,2\).  The left side becomes
\(G_{st}\), while the right side becomes
\[
 6(G_{st}-\gamma\delta_{st})+\gamma\delta_{st}.
 \]
Hence
\[
 G_{st}=6G_{st}-5\gamma\delta_{st},
 \qquad\text{so}\qquad
 G_{st}=\gamma\delta_{st}.                                \tag{14}
\]
Substitution in (13) yields
\[
 \beta_{sr,tq}=\gamma\delta_{rs}\delta_{qt}.
 \]
Renaming the indices proves (4).

Conversely, (4) gives \(G_{st}=\gamma\delta_{st}\), and direct
substitution into (10) recovers (11).  Thus (1) and (4) are exactly
equivalent.

## 3. The totally isotropic coefficient space

Define the block-contraction map
\[
 \Phi_i(Z)=\sum_{a,b=0}^2 Z_{ab}C_{ab},
 \qquad Z\in M_3.                                        \tag{15}
\]
Polarizing (4) gives the rank-one pullback identity
\[
 \boxed{\qquad
 {\cal B}_2(\Phi_i(Z),\Phi_i(W))
 =
 \gamma\,
 \overline{\operatorname{Tr}Z}\operatorname{Tr}W.
 \qquad}                                                  \tag{16}
\]
Therefore
\[
 {\cal B}_2(\Phi_i(Z),\Phi_i(W))=0
 \quad\text{whenever }\operatorname{Tr}Z
 =\operatorname{Tr}W=0.                                  \tag{17}
\]
The traceless coefficient space has dimension eight and is generated
by the six off-diagonal matrix units and two diagonal differences.
Thus their images
\[
 \{C_{ab}:a\ne b\}
 \cup
 \{C_{00}-C_{11},\,C_{11}-C_{22}\}                        \tag{18}
\]
span a \({\cal B}_2\)-totally isotropic subspace.  Its physical
dimension is eight if \(\Phi_i\) is injective on \(M_3^0\), and is at
most eight without that additional hypothesis.

Taking \(Z=W=I_3\) in (16) proves
\[
 {\cal B}_2\left(\sum_aC_{aa},\sum_bC_{bb}\right)
 =9\gamma.
 \tag{19}
\]
Since \(\sum_aC_{aa}=\operatorname{Tr}_iC\), this is (5).

Several more pointwise consequences will be useful:
\[
\begin{aligned}
 Q_2(C_{ab})&=0 &&(a\ne b),\\
 {\cal B}_2(C_{aa},C_{bb})&=\gamma &&(a,b=0,1,2),\\
 Q_2(C_{aa}-C_{bb})&=0 &&(a,b=0,1,2).
                                                               \tag{20}
\end{aligned}
\]
The first line concerns rank-at-most-two matrices when
\(\operatorname{rank}C\le2\), so it lies on the exact equality set of
the unrestricted two-copy theorem.

## 4. A fixed-left strictness theorem for the two-copy endpoint

The unrestricted two-copy theorem is non-strict, but fixing one
singular plane reveals exactly when a zero can occur.

Let
\[
 U:\mathbb C^2\longrightarrow\mathbb C^3\otimes\mathbb C^3
 \tag{21}
\]
be an isometry.  For an arbitrary
\(W:\mathbb C^2\to\mathbb C^3\otimes\mathbb C^3\), define the positive
quadratic form
\[
 \langle W,T_UW\rangle
 =Q_2(UW^\dagger).                                       \tag{22}
\]
The unrestricted two-copy endpoint theorem says \(T_U\succeq0\).

### Theorem 4.1 (kernel forces common \(2\times2\) support)

If
\[
 \ker T_U\ne\{0\},
 \tag{23}
\]
then there are subspaces \(E,F\subseteq\mathbb C^3\), both of
dimension at most two, such that
\[
 \operatorname{ran}U\subseteq E\otimes F.                \tag{24}
\]

Thus a two-qutrit plane with full support on either qutrit has a
strictly positive fixed-left compression.  Only necessity is needed
below; no converse is asserted here.

### 4.1 Exact equality conditions

Identify vectors in
\(\mathbb C^3\otimes\mathbb C^3\) with \(3\times3\) matrices.  Choose
an orthonormal basis \(D,Z\) of \(\operatorname{ran}U\), and transform
the two columns of \(W\) by the same unitary, calling the resulting
matrices \(y,w\).  We may and will choose \(D\) singular: the
homogeneous cubic
\(\det(\alpha D+\beta Z)\) has a projective zero over \(\mathbb C\)
(and if it vanishes identically, every choice is singular).

For matrices \(A,B\), use the bilinear qutrit cross product
\[
 (A\times B)_{i\alpha}
 =
 \sum_{j,k,\beta,\gamma}
 \epsilon_{ijk}\epsilon_{\alpha\beta\gamma}
 A_{j\beta}B_{k\gamma}.                                  \tag{25}
\]
Write
\[
\begin{aligned}
 {\cal C}_D(Y)&=Y\times D,&
 {\cal C}_Z(Y)&=Y\times Z,\\
 A&={\cal C}_D^\dagger{\cal C}_D,&
 K&={\cal C}_Z^\dagger{\cal C}_D,\\
 R&=I+{\cal C}_Z^\dagger{\cal C}_Z-K^\dagger K,&
 r&=(I-A)Z.
\end{aligned}                                             \tag{26}
\]
The exact two-copy completion used in the proof of the unrestricted
theorem is
\[
\begin{aligned}
 {\cal B}(y,w)
 &=
 \|y+Kw\|^2+\|{\cal C}_Dy\|^2+\langle w,Rw\rangle,\\
 \langle D,y\rangle+\langle Z,w\rangle
 &=
 \langle D,y+Kw\rangle+\langle r,w\rangle.               \tag{27}
\end{aligned}
\]
Moreover,
\[
 R\succeq I-K^\dagger K
 \succeq(I-A)^2
 \succeq|r\rangle\langle r|.                             \tag{28}
\]
The endpoint form is one half of the defect between the two sides of
\[
 {\cal B}(y,w)\ge
 \frac12
 |\langle D,y\rangle+\langle Z,w\rangle|^2.               \tag{29}
\]

Suppose \(Q_2(UW^\dagger)=0\).  Equality must hold at every step in
(27)--(29).  Hence, for
\[
 \lambda=\langle r,w\rangle,
 \]
we have
\[
\boxed{
\begin{aligned}
 y+Kw&=\lambda D,\\
 {\cal C}_Dy&=0,\\
 {\cal C}_Zw&=0,\\
 (I-A)w&=\lambda Z,\\
 {\cal G}_P{\cal C}_Dw&=0,
\end{aligned}}                                            \tag{30}
\]
where
\[
 {\cal G}_P
 =
 2I-{\cal C}_D{\cal C}_D^\dagger
    -{\cal C}_Z{\cal C}_Z^\dagger.                       \tag{31}
\]
Here are the individual equality implications.  The exact positive
decomposition
\[
\begin{aligned}
 R-|r\rangle\langle r|
 ={}&
 {\cal C}_Z^\dagger{\cal C}_Z\\
 &+{\cal C}_D^\dagger{\cal G}_P{\cal C}_D\\
 &+\bigl((I-A)^2-|r\rangle\langle r|\bigr)                \tag{32}
\end{aligned}
\]
shows that its kernel is the intersection of the three displayed
kernels.  The last term in (32) is just the Cauchy--Schwarz defect
for the unit vector \(Z\); equality on \(w\) is precisely
\[
 (I-A)w=\langle Z,(I-A)w\rangle Z=\lambda Z.
 \]
The first two terms give the last two nontrivial conditions in (30).
Finally, equality in
\[
 \|y+Kw\|^2+|\lambda|^2
 \ge
 |\langle D,y+Kw\rangle|^2+|\lambda|^2
 \ge\frac12|\langle D,y+Kw\rangle+\lambda|^2
 \]
forces \(y+Kw=\lambda D\).  With the usual convention that the
Hilbert--Schmidt form is conjugate-linear in its first argument, the
same statements hold with the harmless corresponding conjugates of
\(\lambda\).

### 4.2 Equality classification for the reduction gap

Let
\[
 P=|D\rangle\!\rangle\langle\!\langle D|
  +|Z\rangle\!\rangle\langle\!\langle Z|,
\qquad
 \rho_1=\operatorname{Tr}_2P,\quad
 \rho_2=\operatorname{Tr}_1P.                             \tag{33}
\]
The mixed Lagrange identity identifies \({\cal G}_P\), up to entrywise
conjugation, with
\[
 G_P=\rho_1\otimes I+I\otimes\rho_2-P\succeq0.            \tag{34}
\]
We need the equality statement, not only positivity.

**Lemma 4.2.**  If \(G_P\) has a nonzero kernel, then exactly one of
the following descriptions applies:

1. \(P\) is supported in a common \(2\times2\) local subspace;
2. after local unitaries,
   \[
   \operatorname{ran}P
   =
   \operatorname{span}\{
   aE_{11}+bE_{22},\,E_{33}\},
   \qquad a,b>0,\quad a^2+b^2=1.                          \tag{35}
   \]

**Proof.**
Let \(\psi\ne0\) lie in the kernel and put it in Schmidt form
\[
 \psi=\sum_{j=1}^3\sqrt{x_j}|jj\rangle,
 \qquad x_1\ge x_2\ge x_3\ge0,\qquad
 S=x_1+x_2+x_3.
 \tag{36}
\]
As in the proof of the rank-two reduction inequality,
\[
 \langle\psi,G_P\psi\rangle
 =
 -\operatorname{Tr}(P{\cal K}_\psi),
 \]
where
\[
 {\cal K}_\psi
 =
 |\psi\rangle\langle\psi|
 -\sigma_1\otimes I-I\otimes\sigma_2.                    \tag{37}
\]
On \(|ij\rangle\), \(i\ne j\), its eigenvalues are
\(-(x_i+x_j)\).  On the diagonal subspace its matrix is
\[
 H=ss^{\mathsf T}-2\operatorname{diag}(x_1,x_2,x_3),
 \qquad s=(\sqrt{x_1},\sqrt{x_2},\sqrt{x_3})^{\mathsf T}. \tag{38}
\]
The proof of positivity gives
\[
 \lambda_1({\cal K}_\psi)+\lambda_2({\cal K}_\psi)\le0.
 \tag{39}
\]
Kernel equality forces equality in (39), because the rank-two Ky--Fan
bound is the only inequality between (37) and (39).

If \(x_3>0\), then
\[
 \det(H+SI)=4x_1x_2x_3>0,
 \]
so the sum of the two largest eigenvalues inside the diagonal block is
strictly negative.  The competing off-diagonal eigenvalue is
\(-m\), \(m=x_2+x_3\).  The rank-one estimate used in the reduction
proof is strict as well, because its numerator is
\[
 x_1(x_2-x_3)^2+2(x_2+x_3)^3>0.
 \]
Thus (39) cannot be an equality.  Hence \(x_3=0\).

If \(x_2=0\), the zero eigenspace of \({\cal K}_\psi\) is
\[
 \operatorname{span}\{|2\rangle,|3\rangle\}
 \otimes
 \operatorname{span}\{|2\rangle,|3\rangle\}.             \tag{40}
\]
Equality in the Ky--Fan principle places \(\operatorname{ran}P\)
inside this common \(2\times2\) space.

If \(x_2>0\), the two largest eigenvalues are both zero and their
joint eigenspace is exactly
\[
 \operatorname{span}\{
 \sqrt{x_2}|11\rangle+\sqrt{x_1}|22\rangle,\,
 |33\rangle\}.                                           \tag{41}
\]
Because \(P\) has rank two, its range equals (41).  This is (35).
\(\square\)

### 4.3 Excluding the split full-support equality

We now prove Theorem 4.1.  First suppose the plane contains a
rank-two singular matrix.  Choose it as
\[
 D=aE_{11}+bE_{22},
 \qquad a,b>0,\quad a^2+b^2=1.                            \tag{42}
\]
If \({\cal C}_Dw=0\), then \(Kw=0\).  Equations (30) give
\[
 y=\lambda D,\qquad
 0={\cal C}_Dy=\lambda(D\times D).
 \]
But
\[
 D\times D=2abE_{33}\ne0,
 \]
so \(\lambda=0\).  Then \((I-A)w=0\), and
\[
 \|w\|^2=\langle w,Aw\rangle=\|{\cal C}_Dw\|^2=0.
 \]
This makes \(W=0\), a contradiction.  Therefore
\({\cal C}_Dw\ne0\), and Lemma 4.2 applies.

It remains only to exclude its split branch.  In that branch the
rank-two singular member in (42) is unique up to scalar, so
orthogonality fixes
\[
 Z=E_{33}
 \tag{43}
\]
up to a phase.  The equation
\({\cal C}_Zw=0\) says that the upper-left \(2\times2\) block of \(w\)
vanishes.  In the same basis,
\[
 I-{\cal C}_D^\dagger{\cal C}_D
 \]
multiplies the entries \(w_{13},w_{31}\) by \(a^2\), the entries
\(w_{23},w_{32}\) by \(b^2\), and annihilates \(w_{33}\).  Therefore
\[
 (I-A)w=\lambda E_{33}
 \]
forces
\[
 \lambda=0,\qquad w=tE_{33}.                             \tag{44}
\]
Direct cross-product contraction gives
\[
\begin{aligned}
 {\cal C}_Dw&=t(bE_{11}+aE_{22}),\\
 Kw&=tD.
\end{aligned}                                             \tag{45}
\]
The first line of (30) gives \(y=-tD\), while the second gives
\[
 0={\cal C}_Dy=-2tabE_{33}.
 \]
Thus \(t=0\), again contradicting \(W\ne0\).  The split branch is
impossible, leaving only common \(2\times2\) support.

Finally, suppose every singular matrix in the plane has rank at most
one.  Choose a rank-one singular member \(D\).  If
\({\cal C}_Dw\ne0\), Lemma 4.2 again gives either common \(2\times2\)
support or the split branch.  The latter contains a rank-two singular
member and has just been excluded.  If \({\cal C}_Dw=0\), equations
(30) give
\[
 w=\lambda Z,\qquad y=\lambda D.
 \]
Nonzero \(W\) forces \(\lambda\ne0\), and
\({\cal C}_Zw=0\) gives
\[
 Z\times Z=2\operatorname{adj}Z=0.
 \]
Thus \(Z\) also has rank at most one.  A plane spanned by two rank-one
matrices has left and right support dimensions at most two.  This
proves (24) in the remaining case and completes Theorem 4.1.

## 5. Exact remaining common-factor system

Let \(C\) have rank exactly two and take a thin singular
factorization
\[
 C=XSY^\dagger,\qquad
 X^\dagger X=Y^\dagger Y=I_2,\qquad
 S=\operatorname{diag}(s_1,s_2)>0.                        \tag{46}
\]
At the chosen site write
\[
 X=\sum_a|a\rangle\otimes X_a,\qquad
 Y=\sum_b|b\rangle\otimes Y_b,
 \qquad X_a,Y_b:\mathbb C^2\longrightarrow\mathbb C^9.
 \tag{47}
\]
Then
\[
 C_{ab}=X_aSY_b^\dagger.                                 \tag{48}
\]
The Haar equality is therefore equivalent to the structured system
\[
\boxed{\qquad
 {\cal B}_2(X_aSY_b^\dagger,X_cSY_d^\dagger)
 =\gamma\delta_{ab}\delta_{cd}
 \quad(a,b,c,d=0,1,2).
 \qquad}                                                  \tag{49}
\]
In particular, for every orthogonal pair
\(\xi,\eta\in\mathbb C^3\),
\[
 Q_2\left(
 X(\xi)S Y(\eta)^\dagger\right)=0,
 \qquad
 X(\xi)=\sum_a\xi_aX_a,\quad
 Y(\eta)=\sum_b\eta_bY_b.                                \tag{50}
\]
Indeed, (50) is (16) with the traceless rank-one coefficient
\(Z=\xi\eta^\dagger\).

Full local left and right support means that the weighted \(3\times3\)
Gram matrices
\[
\begin{aligned}
 (\rho_i^L)_{ac}
 &=\operatorname{Tr}(S^2X_c^\dagger X_a),\\
 (\rho_i^R)_{bd}
 &=\operatorname{Tr}(S^2Y_d^\dagger Y_b)
\end{aligned}                                             \tag{51}
\]
are positive definite.  This guarantees
\[
 X(\xi)S\ne0,\qquad Y(\eta)S\ne0
 \quad\text{for nonzero }\xi,\eta.                        \tag{52}
\]
It does not by itself make the six-dimensional flattenings
\((X_0,X_1,X_2)\) and \((Y_0,Y_1,Y_2)\) injective.

Theorem 4.1 makes (49) substantially more rigid.  If \(\gamma>0\),
then every diagonal block is nonzero.  Every nonzero off-diagonal
block has rank two: a rank-one block would obey the strict bound
\[
 Q_2(M)\ge\frac14\|M\|_2^2
 \]
and could not have the zero value in (20).  At least one off-diagonal
block is nonzero, because otherwise \(C\) would be block diagonal with
three nonzero diagonal blocks and hence have rank at least three.

Starting from one nonzero \(C_{ab}\), \(a\ne b\), the factorization
(48) propagates rank two to every \(X_a\) and every \(Y_b\).  The
initial block makes \(X_a\) and \(Y_b\) rank two.  Let \(e\) be the
third index.  Since every \(Y_d\ne0\), \(d\ne a\), the product
\(X_aSY_d^\dagger\) would be a nonzero rank-one off-diagonal block if
\(Y_d\) had rank one.  Thus \(Y_b,Y_e\) have rank two.  Applying the
same argument down column \(b\) gives rank two for \(X_a,X_e\).
Now the off-diagonal blocks \(C_{ea}\) and \(C_{be}\) force \(Y_a\)
and \(X_b\), respectively, to have rank two.  Hence all six factors
have rank two.  An injective \(X_aS\) composed with the surjective
\(Y_b^\dagger\) has rank two, so all six off-diagonal blocks do as
well.

Applying Theorem 4.1 to them proves:
\[
\boxed{
\begin{aligned}
 \operatorname{ran}X_a&\subseteq E_{a,2}\otimes E_{a,3},\\
 \operatorname{ran}Y_b&\subseteq F_{b,2}\otimes F_{b,3},
\end{aligned}
\qquad
\dim E_{a,j},\dim F_{b,j}\le2.}                           \tag{53}
\]
More is true.  For a Zariski-open set of \(\xi\), \(X(\xi)\) has rank
two.  Outside a further proper algebraic subset one can choose
\(\eta\) with \(\eta^{\mathsf T}\xi=0\) for which \(Y(\eta)\) also has
rank two.
Equation (50) and Theorem 4.1 show that
\(\operatorname{ran}X(\xi)\) has common \(2\times2\) support.  The
corresponding \(3\times3\) flattening minors are polynomials in
\(\xi\), so vanishing on this dense open set makes them vanish for
every \(\xi\).  The same argument applies to \(Y\):
\[
\boxed{\quad
\begin{array}{l}
\text{every one-site contraction of the left code plane has}\\
\text{two-dimensional support on each of the other two sites,}
\end{array}
\quad\text{and likewise for the right code plane}.}       \tag{54}
\]

Thus the remaining exact lemma is now sharply stated:

> Can a full-local-support two-dimensional three-qutrit code plane
> satisfy the universal slice-support condition (54)?

A negative answer, applied to either singular plane, would force
\(\gamma=0\) and exclude the formal negative Haar equality.  This is
strictly smaller than (49): it is a determinantal classification of a
three-dimensional linear space of \(3\times6\) matrices of upper rank
two, simultaneously in the two physical flattenings.  The present
note does not claim that this last slice-support lemma is proved.

## 6. Compatibility with known zero examples

The standard three-copy zero
\[
 C=(|0\rangle\langle0|+|1\rangle\langle1|)
 \otimes|0\rangle\langle0|
 \otimes|0\rangle\langle0|                               \tag{55}
\]
does not contradict (4).  Although \(Q_3(C)=0\), it does not saturate
the grouped Haar equality used to derive (1).  Its local
scalar/traceless sector masses are the coefficients of
\[
 \left(\frac43+\frac23t\right)
 \left(\frac13+\frac23t\right)^2,
 \]
namely
\[
 (w_0,w_1,w_2,w_3)
 =
 \left(\frac4{27},\frac23,\frac89,\frac8{27}\right).
 \tag{56}
\]
Consequently its grouped Haar expression has the strict value
\[
 \frac14w_1-w_2+3w_3=\frac16>0.                           \tag{57}
\]
The block-Gram collapse applies only after equality in that filter,
not to every endpoint zero.
