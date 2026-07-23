# An all-degree fixed-41 three-point pseudo-distribution

## Status and conclusion

This is a rigorous **barrier result**, not a spherical-code construction.
The rational measures in
[`fixed41_bv_fullradial_k16_pseudodistribution.json`](../certificates/fixed41_bv_fullradial_k16_pseudodistribution.json)
satisfy:

1. every ordinary dimension-five Gegenbauer moment inequality;
2. every Bachoc--Vallentin harmonic matrix inequality \(W_k\succeq0\),
   for every \(k\geq0\) and with arbitrary radial degree;
3. positivity, the full closed three-point support condition, the prescribed
   masses, and the exact fixed-cardinality marginal identities.

Thus the complete family of fixed-cardinality two- and three-point conditions
described in `fixed41_three_point_formulation.md` is feasible at \(N=41\).
These measures do not assert that a 41-point code exists: they need not extend
to a consistent measure on four or more points, and they do not encode a
rank-five Gram matrix.

The exact certificate is
[`fixed41_bv_all_harmonics_certificate.json`](../certificates/fixed41_bv_all_harmonics_certificate.json).
Its standard-library verifier is
[`verify_fixed41_bv_all_harmonics.py`](../verifiers/verify_fixed41_bv_all_harmonics.py).

## The finite-support kernel

Write

\[
 E=\{-1,-3/4,-1/2,-1/4,0,1/4,1/2,1\}
\]

and let \(W_k\) be the \(8\)-by-\(8\) coefficient matrix defined in
`fixed41_three_point_formulation.md`.  Its entries are obtained from

\[
 Q_k(u,v,t)=
 ((1-u^2)(1-v^2))^{k/2}
 P_k^{(4)}
 \left(\frac{t-uv}{\sqrt{(1-u^2)(1-v^2)}}\right).
\tag{1}
\]

For every evaluation matrix \(V\) of radial test functions on \(E\), the
corresponding harmonic block is \(V^{\mathsf T}W_kV\).  It is therefore
enough to prove \(W_k\succeq0\) for all \(k\).

At \(k=0\), exact arithmetic gives

\[
 \ker W_0=\mathop{\rm span}
 \{(-1/40,-1/40,-1/40,-1/40,-1/40,-1/40,-1/40,1)\}.
\tag{2}
\]

The principal submatrix on the first seven coordinates has seven positive
exact \(LDL^{\mathsf T}\) pivots, so \(W_0\succeq0\) and
\(\mathop{\rm rank}W_0=7\).

For \(k>0\), both rows indexed by \(-1\) and \(1\) vanish.  It remains to show
that the active \(6\)-by-\(6\) block on

\[
 I=\{-3/4,-1/2,-1/4,0,1/4,1/2\}
\tag{3}
\]

is positive definite.

## Rational even and odd normalizations

For \(u,v\in I\), put

\[
 a_u=1-u^2,\qquad A=a_ua_v,\qquad w=t-uv,\qquad
 \Delta=A-w^2.
\tag{4}
\]

The support condition is exactly \(\Delta\geq0\).  For \(k=2m\), divide
row \(u\) and column \(u\) of the active block by \(a_u^m\).  For
\(k=2m+1\), use the same factor \(a_u^m\).  These are congruences by positive
rational diagonal matrices.  The normalized transverse kernel is

\[
 R_{2m}(A,w)=P_{2m}^{(4)}(w/\sqrt A)
\tag{5}
\]

in the even case and

\[
 R_{2m+1}(A,w)=\sqrt A\,P_{2m+1}^{(4)}(w/\sqrt A)
\tag{6}
\]

in the odd case.  Both quantities are rational.  Indeed, with
\(x=4w^2/A-2\), their same-parity recurrence is

\[
 R_{k+2}=
 \frac{(k+1)xR_k-(k-1)R_{k-2}}{k+3},
\tag{7}
\]

with initial values

\[
\begin{array}{ll}
R_0=1,&R_2=(4w^2/A-1)/3,\\[2mm]
R_1=w,&R_3=2w^3/A-w.
\end{array}
\tag{8}
\]

This recurrence is the one used for the finite exact check.

## Boundary limits and an analytic tail

For \(S^3\), the normalized Gegenbauer polynomial is

\[
 P_k^{(4)}(\cos\theta)
 =\frac{\sin((k+1)\theta)}{(k+1)\sin\theta}.
\tag{9}
\]

Separate the determinant-zero atoms \(\Delta=0\) from the atoms with
\(\Delta>0\).  On the boundary, (5) equals \(1\) for even \(k\), while
(6) equals \(w\) for odd \(k\).  Let \(L_0,L_1\) be the two rational matrices
obtained from these boundary contributions, together with the diagonal pair
terms:

\[
\begin{aligned}
(L_0)_{ij}
 &=\delta_{ij}\alpha_i+
   \sum_{\substack{\Delta=0\\u=q_i,v=q_j}}c(u,v,t),\\
(L_1)_{ij}
 &=\delta_{ij}\alpha_i(1-q_i^2)+
   \sum_{\substack{\Delta=0\\u=q_i,v=q_j}}c(u,v,t)w.
\end{aligned}
\tag{10}
\]

Here \(c(u,v,t)\) is the mass of that ordered triple: the stored orbit mass
divided by the size of its permutation orbit.

Every exact \(LDL^{\mathsf T}\) pivot of both matrices is positive.  The full
lists are stored in the certificate and recomputed from the original weights
by the verifier.  Exact inversion also gives the rigorous eigenvalue margins

\[
\lambda_{\min}(L_0)\ge
\frac{397179689228432473394583328919}
     {925864373501769000000000000000}
>0.428,
\tag{11}
\]

\[
\lambda_{\min}(L_1)\ge
\frac{397179689228432473394583328919}
     {987588665068553600000000000000}
>0.402.
\tag{12}
\]

To justify these lower bounds, for a symmetric positive-definite matrix
\(L\),

\[
\lambda_{\min}(L)
=\frac1{\lambda_{\max}(L^{-1})}
\geq\frac1{\|L^{-1}\|_\infty},
\tag{13}
\]

because the one- and infinity-norms of the symmetric matrix \(L^{-1}\)
coincide.

For an interior atom, (9) gives

\[
 |R_k(A,w)|\leq
 \begin{cases}
 \displaystyle\frac{\sqrt{A/\Delta}}{k+1},&k\text{ even},\\[3mm]
 \displaystyle\frac{A/\sqrt\Delta}{k+1},&k\text{ odd}.
 \end{cases}
\tag{14}
\]

For a wholly rational bound, replace the two square-root factors by

\[
 \left\lceil\sqrt{A/\Delta}\right\rceil,\qquad
 \left\lceil\sqrt{A^2/\Delta}\right\rceil.
\tag{15}
\]

After summing these bounds entrywise, let \(B_p\) be the resulting
nonnegative matrix for parity \(p\), and let \(E_k=M_k-L_p\), where \(M_k\)
is the normalized active block.  Then

\[
 |(E_k)_{ij}|\leq\frac{(B_p)_{ij}}{k+1}.
\tag{16}
\]

Exact inversion and row summation give

\[
\begin{aligned}
\|(L_0)^{-1}E_k\|_\infty
&\leq\frac{C_0}{k+1},&
C_0&=
\frac{113075924323152880458414612061735}
     {223666156013646314321497996058}
<506,\\
\|(L_1)^{-1}E_k\|_\infty
&\leq\frac{C_1}{k+1},&
C_1&=
\frac{12425696440673780846947250163119}
     {28958716467111139137468092324}
<430.
\end{aligned}
\tag{17}
\]

The constants in (17) use the sharper exact expression

\[
C_p=\max_i\sum_h |(L_p^{-1})_{ih}|
                  \sum_j(B_p)_{hj},
\tag{18}
\]

not a floating-point matrix norm.

The matrix \(L_p^{-1}E_k\) is similar to the symmetric matrix
\(L_p^{-1/2}E_kL_p^{-1/2}\).  If its infinity norm is less than one, all
eigenvalues of the latter lie in \((-1,1)\).  Hence
\(L_p+E_k\) is positive definite.  Formula (17) proves this for every
\(k\geq506\).

## Finite exact check

For \(1\leq k\leq505\), the verifier builds the normalized matrix \(M_k\)
using (7)--(8) and computes an exact rational \(LDL^{\mathsf T}\)
decomposition.  All \(3030\) pivots are strictly positive.  The least one is
the sixth pivot at \(k=3\):

\[
\frac{
197794309263049812001825456561375774155305921465821859451864015060080757474120979487105976743261
}{
39469349842659853229517093154679564863658026786444004637710806146749391402445520561400000000000000
}>0.
\tag{19}
\]

This finite exact check, (17), and the \(k=0\) calculation prove
\(W_k\succeq0\) for every \(k\geq0\).

## All ordinary two-point moments

The original certificate checked

\[
1+\sum_i\alpha_iP_k^{(5)}(q_i)>0
\tag{20}
\]

only through degree \(100\).  The following gives an all-degree proof.
Separate the atom at \(-1\).  Its weight is

\[
\alpha_{-1}=\frac{2223963080457}{3125000000000},
\qquad
1-\alpha_{-1}
=\frac{901036919543}{3125000000000}.
\tag{21}
\]

For \(-1<t<1\), the standard integral representation

\[
P_k^{(5)}(t)=\frac2\pi\int_0^\pi
\left(t+i\sqrt{1-t^2}\cos\phi\right)^k\sin^2\phi\,d\phi
\tag{22}
\]

and elementary Gaussian integration imply

\[
|P_k^{(5)}(t)|
\leq
\frac{\pi^2\sqrt{2\pi}}
     {4[k(1-t^2)]^{3/2}}
<\frac{31}{5[k(1-t^2)]^{3/2}}.
\tag{23}
\]

The last rational inequality follows from
\(\pi<22/7\) and \(\sqrt{2\pi}<251/100\).
For the six interior atoms in the order (3), exact upper bounds for
\((1-t^2)^{-3/2}\) are

\[
4,\quad\frac85,\quad\frac65,\quad1,\quad\frac65,\quad\frac85.
\tag{24}
\]

Their weighted sum is

\[
B=\frac{2859016043631419}{50000000000000}.
\tag{25}
\]

Relative to the endpoint margin in (21), the tail constant is

\[
\frac{(31/5)B}{1-\alpha_{-1}}
=\frac{88629497352573989}{72082953563440},
\tag{26}
\]

whose square is strictly less than \(115^3\).  Thus (20) is strict for every
\(k\geq115\).  Exact recurrence evaluation for \(1\leq k\leq114\) is also
strict; its minimum occurs at \(k=3\) and equals

\[
\frac{197167927189}{128000000000000}>0.
\tag{27}
\]

This proves (20) in every degree.

## Reproduction and numerical-rigor boundary

From the project directory, run

```text
python3 verifiers/verify_fixed41_bv_all_harmonics.py
```

The source pseudo-distribution is pinned by SHA-256

```text
8c016c5ab1770f930d3f31f5448ffef7731616dd7025b29c43828760064b4d88
```

The verifier uses `fractions.Fraction`, integer square roots, exact
Gauss--Jordan inversion, and exact \(LDL^{\mathsf T}\) pivots.  No solver,
eigenvalue routine, floating-point tolerance, or rounded trigonometric value
is trusted.

Determinant-zero triples are not discarded: they form the limiting matrices
\(L_0,L_1\).  The endpoints \(u=\pm1\) and the exceptional two-point atom
\(t=-1\) are handled separately and exactly.  All support inequalities are
closed inequalities, so the argument includes every boundary case.
