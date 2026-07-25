# A full-interval 41-row counterexample to the split-kernel abstraction

## Status

This note strengthens `split_kernel_abstract_barrier.md`.  It gives exact
order-41 matrices
\[
A\succeq0,\qquad B\succeq0,\qquad R=A+B,\qquad
K=R-\frac3{10}J
\]
that satisfy
\[
\begin{aligned}
&\operatorname{rank}A=5,& A_{ii}&=1/2,\\
&\operatorname{rank}B=14,&B_{ii}&=4/5,\\
&\operatorname{rank}R=19,&R_{ii}&=13/10,\\
&&-\frac{21}{80}&<R_{ij}<\frac3{10}\quad(i\ne j).
\end{aligned}                                      \tag{1}
\]
Thus \(K_{ii}=1\), \(K_{ij}<0\), \(\operatorname{rank}K=19\), and \(K\)
has exactly one negative eigenvalue.  Both split Ky Fan constraints also
hold.

This is not a spherical code.  Although every \(R_{ij}\) lies in the
entrywise range of \(t^2+t/2-1/5\), the candidate linear source \(G=2A\)
has some entries greater than \(1/2\), and the two factors do not obey the
nonlinear common-source identity \(B=(4/5)P_2[2A]\).

## Rationally weighted Fourier projectors

Index rows by \(\mathbb Z/41\mathbb Z\).  Let
\[
(P_0)_{ij}=\frac1{41}
\]
be the constant rank-one projector.  For
\(1\leq k\leq20\), let
\[
(P_k)_{ij}=\frac2{41}
\cos\left(\frac{2\pi k(i-j)}{41}\right).           \tag{2}
\]
The real Fourier orthogonality relations show that these are mutually
orthogonal PSD projectors, with
\[
\operatorname{rank}P_0=1,\qquad\operatorname{rank}P_k=2.
\]

Use the positive rational weights
\[
\alpha=\frac1{10^7}(2630231,3658274,3711495)
\]
on frequencies \(0,1,15\), and
\[
\beta=\frac1{10^7}
(1683899,1670847,1242944,1308499,1262961,1573008,1257842)
\]
on frequencies \(3,5,6,7,12,16,18\).  Both weight lists sum to one.
Define
\[
\begin{aligned}
A={}&\frac{41}{2}\alpha_0P_0
+\frac{41}{4}\alpha_1P_1
+\frac{41}{4}\alpha_2P_{15},\\
B={}&\frac{82}{5}\sum_{j=1}^7\beta_jP_{k_j}.
\end{aligned}                                      \tag{3}
\]
Every coefficient in (3) is positive, and the frequency sets are
disjoint.  Hence
\[
\operatorname{rank}A=1+2+2=5,\quad
\operatorname{rank}B=14,\quad
\operatorname{rank}R=19.
\]
The projector diagonals give
\[
A_{ii}=\frac12\sum\alpha_j=\frac12,\qquad
B_{ii}=\frac45\sum\beta_j=\frac45.
\]

For a nonzero cyclic difference \(h\), equation (3) becomes
\[
\begin{aligned}
R(h)={}&\frac12\left[
\alpha_0+\alpha_1\cos\frac{2\pi h}{41}
+\alpha_2\cos\frac{30\pi h}{41}\right]\\
&+\frac45\sum_{j=1}^7\beta_j
\cos\frac{2\pi k_jh}{41}.                         \tag{4}
\end{aligned}
\]
The exact interval certificate described below proves the stronger
buffered bounds
\[
-\frac{21}{80}+\frac1{2000}
<R(h)<
\frac3{10}-\frac1{2000}
\qquad(1\leq h\leq40).                            \tag{5}
\]

## Exact directed verification of the cosines

No floating-point value is used in the proof of (5).  The verifier first
encloses \(\pi\) using Machin's identity
\[
\pi=16\arctan(1/5)-4\arctan(1/239).               \tag{6}
\]
For completeness, if \(a=\arctan(1/5)\) and
\(b=\arctan(1/239)\), exact tangent addition gives
\[
\tan(4a)=\frac{120}{119},\qquad
\tan(4a-b)=1.
\]
The angles lie in the appropriate first-quadrant ranges, proving
\(4a-b=\pi/4\).

For \(0<x<1\), the alternating series
\[
\arctan x=\sum_{n\geq0}\frac{(-1)^nx^{2n+1}}{2n+1}
\]
gives directed rational lower and upper bounds after 30 terms at \(1/5\)
and eight terms at \(1/239\).  For every residue
\(1\leq r\leq20\), these bounds enclose
\(2\pi r/41\).

Finally, after its first two terms the cosine series has decreasing term
magnitudes throughout \([0,\pi]\).  Twenty-four terms therefore give
directed rational enclosures, with the next term supplying the error.
Cosine monotonicity on \([0,\pi]\) handles the rational angle interval.
Substitution into (4), using positivity of every rational weight, proves
(5) exactly.  Symmetry
\(\cos(2\pi k(41-h)/41)=\cos(2\pi kh/41)\) reduces the check to 20
residues.

## Spectrum after the rank-one shift

The constant Fourier eigenvalue of \(R\) is
\[
\lambda_0=\frac{41}{2}\alpha_0.
\]
All 18 nonconstant eigenvalues on the selected Fourier modes are positive,
and the other 22 eigenvalues vanish.  Since
\[
\lambda_0-\frac{3}{10}\cdot41<0,
\]
the shift \(K=R-(3/10)J\) replaces the positive constant eigenvalue by
one negative eigenvalue and leaves every other eigenspace unchanged.
Thus
\[
\operatorname{rank}K=19,\qquad n_-(K)=1.           \tag{7}
\]
Equation (5) gives \(K_{ij}<0\) for all \(i\ne j\).

Because \(R=A+B\) with the stated ranks and traces,
\[
\sum_{i=1}^5\lambda_i(R)\geq\operatorname{tr}A
=\frac{41}{2},
\]
\[
\sum_{i=1}^{14}\lambda_i(R)\geq\operatorname{tr}B
=\frac{164}{5}.
\]
These are exactly the split Ky Fan constraints at \(N=41\).

## What the counterexample rules out

No upper-bound proof can use only:

1. \(R\succeq0\), its rank, diagonal, or full off-diagonal interval;
2. the decomposition into PSD rank-5 and rank-14 constant-diagonal
   summands;
3. the two split trace/Ky Fan inequalities;
4. the rank, inertia, diagonal, sign pattern, or full entry interval of
   \(K=R-(3/10)J\).

All of these hold in the exact order-41 construction.

The surviving gaps are the entrywise kissing inequality on the linear
summand and the nonlinear relation between the summands.  In a genuine
code,
\[
A=\frac12G,\qquad
B=G\circ G-\frac15J.
\]
The Fourier counterexample has \(2A_{ij}>1/2\) at cyclic difference three
and deliberately does not satisfy the displayed relation.  A successful
quadratic-kernel proof must use this common-source information, or an
equivalent higher-cycle identity, rather than only separate spectral
information about \(R,A,B\).

## Reproduction

Run

```sh
python3 verifiers/verify_split_kernel_full_interval.py
python3 -m unittest tests.test_split_kernel_full_interval -v
```

The verifier uses only integer and rational arithmetic.  Its interval
enclosures are directed by construction.
