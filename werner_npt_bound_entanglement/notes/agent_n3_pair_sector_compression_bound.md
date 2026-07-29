# A one-site compression bound for the qutrit pair sector

## Status

This is a secondary exact bound, not the sharp pair-sector theorem.
Using the established local-support boundary theorem, it proves
\[
 \|\Pi_2C\|_2^2\leq\frac{24}{31}\|C\|_2^2
 \qquad(\operatorname{rank}C\leq2).
 \tag{1}
\]
Its main use is to confine any remaining counterexample to a smaller
quantitative range.  It does not replace the correlated Hodge--Pluecker
problem.

## Proof

Normalize \(\|C\|_2=1\), and write
\[
 w_k=\|\Pi_kC\|_2^2,\qquad k=0,1,2,3.
 \tag{2}
\]
Thus \(\sum_kw_k=1\).  Fix one left physical qutrit.  For Haar-uniform
\(z\in\mathbb C^3\), let
\[
 A_z=I-|z\rangle\langle z|.
 \tag{3}
\]
The matrix \(A_zC\) has rank at most two and a two-dimensional local
left support.  The established boundary theorem therefore gives
\[
 \|\Pi_2(A_zC)\|_2^2\leq\frac23\|A_zC\|_2^2.
 \tag{4}
\]

For a normalized local operator \(X\), Haar integration gives
\[
\begin{array}{c|cc}
 &X=I/\sqrt3&\operatorname{Tr}X=0\\ \hline
 {\mathbb E}\|A_zX\|_2^2&2/3&2/3\\
 {\mathbb E}\|{\cal P}(A_zX)\|_2^2&4/9&1/36\\
 {\mathbb E}\|{\cal Q}(A_zX)\|_2^2&2/9&23/36 .
\end{array}
\tag{5}
\]
Here \({\cal P}(X)=\operatorname{Tr}(X)I/3\) and
\({\cal Q}=I-{\cal P}\).  The only nontrivial entry is
\[
 {\mathbb E}|z^\dagger Xz|^2
 =\frac{\|X\|_2^2+|\operatorname{Tr}X|^2}{12}.
 \tag{6}
\]

Average (4) and then sum over the three choices of the filtered site.
A global degree-one component contributes \(2(2/9)=4/9\), a
degree-two component contributes
\[
 \frac49+2\frac{23}{36}=\frac{31}{18},
\]
and a degree-three component contributes \(3(1/36)=1/12\).
The summed right side is \(3(2/3)(2/3)=4/3\).  Hence
\[
 \frac49w_1+\frac{31}{18}w_2+\frac1{12}w_3
 \leq\frac43,
\]
or
\[
 \boxed{\qquad
 16w_1+62w_2+3w_3\leq48.
 \qquad}
 \tag{7}
\]
Dropping the two nonnegative terms proves (1).

The dependency-free checker
`verification/verify_n3_pair_sector_compression_bound.py` verifies all
coefficient arithmetic.
