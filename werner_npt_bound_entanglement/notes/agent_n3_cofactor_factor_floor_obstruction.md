# Exact obstruction to a factorized cofactor floor

## Status

This note gives an exact counterexample to the tempting strengthening
\[
 M_{Q,2}(R)\stackrel{?}{\succeq}
 6\det(\rho_1)\det(\rho_2)(2I-R),                         \tag{1}
\]
even under the correct normalization
\(\operatorname{Tr}_{12}R=I_K\), and even for a rank-two \(R\).
Here
\[
 M_{Q,2}(R)=(2E_1-I)(2E_2-I)(R).                         \tag{2}
\]

Inequality (1) would have been useful because, for a rank-two \(R\)
of trace two with nonzero eigenvalue product \(g\),
\[
 2I-R\succeq\frac g2 I,
\]
so (1) would imply the desired scalar boundary floor
\[
 M_{Q,2}(R)\succeq
 3g\det(\rho_1)\det(\rho_2)I.                            \tag{3}
\]
The counterexample below invalidates only this factorized route.  It
does not violate (3).

## 1. Rank-one seed

On \(K\otimes H_1\otimes H_2\), with dimensions \(2,3,3\), put
\[
 |A\rangle
 =|0\rangle_K|00\rangle
 +\frac1{\sqrt2}|1\rangle_K(|11\rangle+|22\rangle).
\tag{4}
\]
Then
\[
 \operatorname{Tr}_{12}|A\rangle\langle A|=I_K
\tag{5}
\]
and both physical marginals are
\[
 \rho_1=\rho_2=\operatorname{diag}(1,\tfrac12,\tfrac12),
 \qquad
 d:=\det\rho_1\det\rho_2=\frac1{16}.                     \tag{6}
\]
For \(R_0=|A\rangle\langle A|\), exact contraction gives
\[
\begin{aligned}
 \chi_{M_{Q,2}(R_0)}(\lambda)
 &=(\lambda-4)^5(\lambda-3)^4(\lambda-2)^7
   (\lambda^2-4\lambda+2),\\
 \chi_{M_{Q,2}(R_0)-\frac38(2I-R_0)}(\lambda)
 &\doteq
 (4\lambda-13)^5(4\lambda-9)^4(4\lambda-5)^7
 (4\lambda^2-13\lambda-1).
\end{aligned}                                             \tag{7}
\]
Thus the proposed residual in (1) has the exact negative eigenvalue
\[
 \frac{13-\sqrt{185}}8<0.                                \tag{8}
\]
The endpoint operator itself remains strictly positive:
\[
 \lambda_{\min}M_{Q,2}(R_0)=2-\sqrt2>0.                  \tag{9}
\]

## 2. Exact rank-two continuation

The failure is not an artifact of the rank-one endpoint.  Define the
orthogonal balanced vector
\[
 |B\rangle
 =|0\rangle_K|01\rangle+|1\rangle_K|02\rangle             \tag{10}
\]
and, for \(0<t<2\), put
\[
 R_t=\left(1-\frac t2\right)|A\rangle\langle A|
       +\frac t2|B\rangle\langle B|.                      \tag{11}
\]
Both \(A\) and \(B\) have squared norm two, are orthogonal, and have
auxiliary marginal \(I_K\).  Hence
\[
\begin{gathered}
 R_t\succeq0,\qquad \operatorname{rank}R_t=2,\qquad
 \operatorname{Tr}_{12}R_t=I_K,\\
 \operatorname{spec}_{+}(R_t)=\{2-t,t\},\qquad
 g=t(2-t).
\end{gathered}                                             \tag{12}
\]
The physical marginals are
\[
\begin{aligned}
 \rho_1(t)&=\operatorname{diag}
 (1+\tfrac t2,\tfrac12-\tfrac t4,\tfrac12-\tfrac t4),\\
 \rho_2(t)&=\operatorname{diag}
 (1-\tfrac t2,\tfrac12+\tfrac t4,\tfrac12+\tfrac t4),
\end{aligned}                                             \tag{13}
\]
and therefore
\[
 d(t):=\det\rho_1(t)\det\rho_2(t)
 =\frac{(4-t^2)^3}{1024}.                                \tag{14}
\]

Take the exact test vector
\[
 |x\rangle
 =-2|0,0,0\rangle
 +\frac1{\sqrt2}|1,1,1\rangle
 +\frac1{\sqrt2}|1,2,2\rangle ,
 \qquad \|x\|^2=5.                                       \tag{15}
\]
Direct contraction gives
\[
\begin{aligned}
 \langle x,M_{Q,2}(R_t)x\rangle&=3+4t,\\
 \langle x,(2I-R_t)x\rangle&=\frac{18+t}{2},\\
 \langle x,[M_{Q,2}(R_t)-6d(t)(2I-R_t)]x\rangle
 &=
 \frac{
 3t^7+54t^6-36t^5-648t^4+144t^3
 +2592t^2+3904t-384
 }{1024}.
\end{aligned}                                             \tag{16}
\]
At the rational value \(t=1/100\), the last quantity is
\[
 -\frac{34470066248354597}{102400000000000000}<0.         \tag{17}
\]
This is an exact rank-two counterexample to (1) satisfying every
normalization needed by the boundary problem.

For clarity, it is not a counterexample to the scalar target (3).  On
the same vector, at \(t=1/100\),
\[
 \langle x,
 [M_{Q,2}(R_t)-3g\,d(t)I]x\rangle>0.                     \tag{18}
\]
No operator claim is inferred from (18); it only confirms that the
displayed separating vector attacks the discarded factorization, not
the live scalar inequality.

The dependency-free exact checker is
`verification/verify_n3_cofactor_factor_floor_obstruction.py`.

## 3. Equal marginals do not determine the rank-one spectrum

There is also a precise obstruction to diagonalizing the rank-one
problem using only the spectra, or even the full matrices, of the two
physical marginals.  Besides the isometry in (4), consider
\[
\begin{aligned}
 |C\rangle={}&
 \frac1{\sqrt2}|0\rangle_K(|00\rangle+|11\rangle)\\
 &+\frac1{\sqrt2}|1\rangle_K(|02\rangle+|20\rangle).
\end{aligned}                                             \tag{19}
\]
Both \(A\) and \(C\) have auxiliary marginal \(I_K\), and both have
the *same two physical marginal matrices*
\[
 \rho_1=\rho_2=\operatorname{diag}(1,\tfrac12,\tfrac12).
\tag{20}
\]
Nevertheless,
\[
\begin{aligned}
 \chi_{M_{Q,2}(|A\rangle\langle A|)}(\lambda)
 &=(\lambda-4)^5(\lambda-3)^4(\lambda-2)^7
   (\lambda^2-4\lambda+2),\\
 \chi_{M_{Q,2}(|C\rangle\langle C|)}(\lambda)
 &=(\lambda-1)(\lambda-2)^2(\lambda-3)^6(\lambda-4)^3
   (\lambda^2-5\lambda+5)^3 .
\end{aligned}                                             \tag{21}
\]
In particular, the two least eigenvalues are \(2-\sqrt2\) and \(1\),
respectively.  Thus a general rank-one diagonalization must retain
matrix-pencil information beyond the two local marginal spectra.
This does not rule out a lower bound expressed only through marginal
invariants; it rules out an exact spectral formula based only on them.
