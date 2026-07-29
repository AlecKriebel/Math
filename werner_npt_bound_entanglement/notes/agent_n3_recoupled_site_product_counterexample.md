# Exact site-product counterexample to recoupled block positivity

## Result

Let
\[
 {\cal B}=\widehat{\cal K}-L\widehat{\cal K}R
\]
be the recoupled four-species operator from the local \(S_4\) reduction
of the qutrit pair-sector determinant.  It is **not** block positive
across
\[
 (L_1L_2):(R_1R_2).
\]
In fact, it is negative on a vector which is also a product across the
three physical sites:
\[
 \boxed{\qquad
 \langle a\otimes b,{\cal B}(a\otimes b)\rangle=-\frac19.
 \qquad}                                                   \tag{1}
\]

This is not a counterexample to the physical pair-sector inequality.
The third local factors below are maximally entangled between the two
replica species.  Thus \(a\) and \(b\) are not rank-one across
\(L_1:L_2\) and \(R_1:R_2\).

The independent exact checker is
`verification/verify_n3_recoupled_site_product_counterexample.py`.

## 1. The vectors

At each site use species order
\[
 (L_1,L_2,R_1,R_2)
\]
and put
\[
 \Phi_3=\frac1{\sqrt3}\sum_{j=0}^2|j,j\rangle .
\]
Choose the left and right two-replica factors
\[
\begin{array}{c|ccc}
 &1&2&3\\ \hline
 a_i&|0,1\rangle&|0,0\rangle&\Phi_3\\
 b_i&|0,1\rangle&|1,1\rangle&\Phi_3 .
\end{array}                                                \tag{2}
\]
Then
\[
 a=a_1\otimes a_2\otimes a_3,\qquad
 b=b_1\otimes b_2\otimes b_3.                             \tag{3}
\]

Let
\[
 f_1=(L_1\,R_1),\quad f_2=(L_2\,R_2),\quad
 \ell=(L_1\,L_2),\quad r=(R_1\,R_2).
\]
For \(x,y\in\{0,1\}\), define the local direct and crossed moments
\[
\begin{aligned}
 d_i(x,y)
 &=\langle a_i\otimes b_i,
          f_1^x f_2^y(a_i\otimes b_i)\rangle,\\
 e_i(x,y)
 &=\langle a_i\otimes b_i,
          \ell f_1^x f_2^y r(a_i\otimes b_i)\rangle .
\end{aligned}                                             \tag{4}
\]
In the order \((x,y)=(0,0),(0,1),(1,0),(1,1)\), direct basis
contraction gives
\[
\begin{array}{c|cc}
i&d_i&e_i\\ \hline
1&(1,1,1,1)&(0,0,0,1)\\
2&(1,0,0,0)&(1,0,0,0)\\
3&(1,\tfrac13,\tfrac13,1)&
  (1,\tfrac13,\tfrac13,1).
\end{array}                                                \tag{5}
\]

## 2. Exact contraction

For a mask \(S\subseteq\{1,2,3\}\), put
\[
 c_S=c_{|S|},\qquad
 (c_0,c_1,c_2,c_3)
 =\left(2,-1,\frac23,-\frac13\right).                    \tag{6}
\]
The expansion of the two copies of \(\widehat Y\) gives
\[
\begin{aligned}
 \langle a b,\widehat{\cal K}\,a b\rangle
 &=\sum_{S,T}c_Sc_T
   \prod_i d_i(1_{i\in S},1_{i\in T}),\\
 \langle a b,L\widehat{\cal K}R\,a b\rangle
 &=\sum_{S,T}c_Sc_T
   \prod_i e_i(1_{i\in S},1_{i\in T}).
\end{aligned}                                             \tag{7}
\]

The site-two table forces its two mask bits to vanish in both sums.
For the direct contraction, summing over the free site-one bit changes
the coefficient vector at site three to
\[
 (c_0+c_1,\ c_1+c_2)=\left(1,-\frac13\right).
\]
Using the site-three matrix from (5) therefore gives
\[
 \langle a b,\widehat{\cal K}\,a b\rangle
 =
 \begin{pmatrix}1&-\frac13\end{pmatrix}
 \begin{pmatrix}1&\frac13\\[1mm]\frac13&1\end{pmatrix}
 \begin{pmatrix}1\\-\frac13\end{pmatrix}
 =\frac89.                                                \tag{8}
\]

For the crossed contraction, the site-one table instead forces both
site-one mask bits to equal one.  Its coefficient vector is
\[
 (c_1,c_2)=\left(-1,\frac23\right),
\]
and hence
\[
 \langle a b,L\widehat{\cal K}R\,a b\rangle
 =
 \begin{pmatrix}-1&\frac23\end{pmatrix}
 \begin{pmatrix}1&\frac13\\[1mm]\frac13&1\end{pmatrix}
 \begin{pmatrix}-1\\\frac23\end{pmatrix}
 =1.                                                      \tag{9}
\]
Subtracting (9) from (8) proves (1).

## 3. The exact missing Segre condition

Regard each two-replica vector as the vectorization of a coefficient
matrix.  The six local matrices in (2) have ranks
\[
\begin{array}{c|ccc}
 &1&2&3\\ \hline
 a_i&1&1&3\\
 b_i&1&1&3 .
\end{array}                                                \tag{10}
\]
Thus the counterexample violates local replica separability only at
the third site.

Within the site-product relaxation, the smallest additional condition
which excludes this example is that every local two-replica factor
have coefficient-matrix rank one.  For the actual physical
four-vector problem the intrinsic condition is stronger and
frame-independent:
\[
 a=u_1\otimes u_2,\qquad b=v_1\otimes v_2,                \tag{11}
\]
so the global coefficient matrices of \(a\) and \(b\) have rank one
across \(L_1:L_2\) and \(R_1:R_2\).  The physical code also imposes
\[
 \langle u_1,u_2\rangle=\langle v_1,v_2\rangle=0.         \tag{12}
\]

Consequently neither grouped block positivity nor physical-site
factorization is a viable relaxation.  Any successful recoupled proof
must retain the global two-plane Segre/Pluecker origin (11)--(12).

The exact hierarchy is now:

1. the unrestricted local-\(S_4\) ambient space has expectation
   \(-24\), on a vector of grouped Schmidt rank \(64\);
2. even a product across \((L_1L_2):(R_1R_2)\), separately factorized
   over the three physical sites, has expectation \(-1/9\); the two
   grouped factors in (3) each have replica Schmidt rank \(3\);
3. the physical four-fold Segre locus has replica Schmidt ranks
   \(1\) and \(1\), together with (12), and remains unresolved.

Thus the new counterexample removes two nested linear or
tensor-product relaxations without touching the actual common-plane
inequality.
