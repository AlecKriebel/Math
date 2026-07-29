# An exact same-code counterexample to the local crossed-Hodge inertia route

## Status

This note gives an exact, interval-certified, real rank-two coefficient
matrix whose one-site two-copy block Gram is positive definite and
isotropic, whose left and right one-site marginals are maximally mixed,
and whose separate left and right critical Hessians are positive
semidefinite.  Nevertheless, the antisymmetric compression of the
partially transposed block Gram has **three** negative eigenvalues.

Thus none of the following conditions, even imposed simultaneously on
one physical site, forces crossed-Hodge negative inertia at most one:

1. common origin from one rank-two coefficient matrix;
2. positivity of the complete \(9\times9\) block Gram;
3. exact left and right local stationarity;
4. positivity of both separate local-filter Hessians.

The example has positive endpoint value.  It is not a three-copy
distillation witness, is not asserted to be stationary at the other
two physical sites, and does not disprove a statement that also uses
\(q<0\), all six sites, or the full coupled rank-two Hessian.

The exact verifier is
`verification/verify_n3_isotropic_local_stationary_counterexample.py`.
Its isolating data are
`verification/data/n3_isotropic_local_stationary.json`.

## 1. The block Gram and its local form

At a fixed qutrit site write a rank-two coefficient matrix as
\[
 C=XY^{\mathsf T},\qquad X,Y\in M_{27,2}(\mathbb R),
 \tag{1}
\]
and split
\[
 X=(X_0,X_1,X_2)^{\mathsf T},\qquad
 Y=(Y_0,Y_1,Y_2)^{\mathsf T},
 \qquad X_a,Y_p\in M_{9,2}(\mathbb R).
 \tag{2}
\]
The \(9\times9\) environment blocks are
\[
 C_{ap}=X_aY_p^{\mathsf T}.
 \tag{3}
\]
Put
\[
 \beta_{ap,bq}
 ={\cal B}_2(C_{ap},C_{bq}),\qquad
 {\cal B}_2(U,V)=
 \langle U,L^{\otimes2}(V)\rangle_{\rm HS}.
 \tag{4}
\]

Suppose that, for real \(A,B\),
\[
 \boxed{\quad
 \beta=A|\operatorname{vec}I_3\rangle
          \langle\operatorname{vec}I_3|+BI_9.
 \quad}
 \tag{5}
\]
Inverting the exact block-Gram/local-form coefficient map gives
\[
 \boxed{\quad
 h(Z,W)=
 \left(A+\frac52B\right)\langle Z,W\rangle_{\rm HS}
 -\frac A2\,\overline{\operatorname{Tr}Z}\operatorname{Tr}W.
 \quad}
 \tag{6}
\]
This can also be checked directly from the one-site recursion
\[
 h(Z,W)=
 \sum_{r,p}{\cal B}_2((ZC)_{rp},(WC)_{rp})
 -\frac12{\cal B}_2
 \left(\sum_r(ZC)_{rr},\sum_p(WC)_{pp}\right).
 \tag{7}
\]
In particular, for \(\|C\|_2=1\),
\[
 \boxed{\quad
 q=Q_3(C)=h(I,I)=\frac32(5B-A).
 \quad}
 \tag{8}
\]
Consequently the negative endpoint regime inside the isotropic
block-Gram stratum is exactly
\[
 A>5B.
 \tag{9}
\]

If the left marginal is \(\rho_L=I_3/3\), (6) gives
\[
 h(Z,I)=q\,\operatorname{Tr}(Z^\dagger\rho_L).
 \tag{10}
\]
The separate left-filter Hessian is
\[
 G_L(Z,W)
 =h(Z,W)-q\operatorname{Tr}(Z^\dagger W\rho_L).
 \tag{11}
\]
It vanishes on the scalar line and is the scalar form
\[
 \boxed{\quad
 G_L|_{M_3^0}=\frac32A\,I_{M_3^0}.
 \quad}
 \tag{12}
\]
The identical statements hold on the right when
\(\rho_R=I_3/3\).  Indeed, right multiplication merely interchanges
the row-site and column-site index pairs in the above contraction, and
both tensors in (5),
\(\delta_{ab}\delta_{pq}\) and \(\delta_{ap}\delta_{bq}\), are
invariant under that interchange.  Notice that (12) only needs
\(A\geq0\); it does not impose the endpoint condition \(A\leq5B\).

## 2. Exact counterexample

### Theorem 2.1

There are real algebraic matrices \(X,Y\in M_{27,2}(\mathbb R)\)
and a real algebraic number \(B>0\) such that
\[
 \|XY^{\mathsf T}\|_2=1,\qquad
 \operatorname{rank}(XY^{\mathsf T})=2,
 \tag{13}
\]
\[
 \rho_L=\rho_R=\frac13I_3,
 \tag{14}
\]
and
\[
 \boxed{\quad
 \beta=
 B\left(
 I_9+\frac65|\operatorname{vec}I_3\rangle
             \langle\operatorname{vec}I_3|
 \right).
 \quad}
 \tag{15}
\]
The algebraic number \(B\) lies in the rigorously certified interval
\[
 0.04323757372974235
 <B<
 0.043237575729742364.
 \tag{16}
\]

For this matrix:

1. \(\beta\succ0\);
2. the left and right stationarity equations hold;
3. both separate local Hessians are positive semidefinite, with
   traceless gap \(9B/5\);
4. on the three-dimensional antisymmetric space,
   \[
   \boxed{\quad
   P_-\beta^{\Gamma_2}P_-=-\frac B5P_-.
   \quad}
   \tag{17}
   \]

Hence the crossed-Hodge compression has negative inertia three.

### Proof

The existence, uniqueness in an explicit rational box, normalization,
and factor ranks are certified in Section 3 below.  Accept those facts
temporarily and put \(A=6B/5\).

The eigenvalues of (15) are \(B\), with multiplicity eight, and
\[
 B+3A=\frac{23}{5}B
 \tag{18}
\]
on the line spanned by \(\operatorname{vec}I_3\).  This proves
\(\beta\succ0\).

Equations (8), (12), and \(A=6B/5\) give
\[
 q=\frac{57}{10}B>0,\qquad
 G_L|_{M_3^0}=G_R|_{M_3^0}=\frac95B\,I.
 \tag{19}
\]
Together with (14), this proves stationarity and the separate Hessian
claims.

Finally,
\[
 \left(
 |\operatorname{vec}I_3\rangle
 \langle\operatorname{vec}I_3|
 \right)^{\Gamma_2}=F_3.
 \tag{20}
\]
The flip is \(-I\) on \(\bigwedge^2\mathbb C^3\).  Therefore
\[
 P_-\beta^{\Gamma_2}P_-
 =(B-A)P_-=-\frac B5P_-,
 \]
which proves (17).  \(\square\)

## 3. Exact interval certificate

This section specifies the algebraic numbers in Theorem 2.1 without
printing 108 long decimal expansions in the proof.

Order the unknowns as
\[
 z=(X_{000},\ldots,X_{26,1},
     Y_{000},\ldots,Y_{26,1},B)\in\mathbb R^{109}.
 \tag{21}
\]
The data file records:

* an exact binary-rational center \(z_0\);
* 56 free coordinate indices;
* the exact binary-rational radius \(r\) whose hexadecimal encoding in
  the file is the nearest binary64 number to \(10^{-9}\).

The other 53 coordinates are fixed at their recorded binary-rational
values.  On the 56 free coordinates impose the following 56
polynomial equations:

1. the 45 upper-triangular entries of
   \[
   \beta-B\left(
   I_9+\frac65|\operatorname{vec}I_3\rangle
              \langle\operatorname{vec}I_3|
   \right)=0;
   \tag{22}
   \]
2. five independent equations saying
   \(\rho_L\) is scalar;
3. five independent equations saying
   \(\rho_R\) is scalar;
4. \(\|XY^{\mathsf T}\|_2^2=1\).

All coefficients are rational.  Let \(F:\mathbb R^{56}\to
\mathbb R^{56}\) be this square polynomial system and let
\[
 {\cal X}=z_{0,\mathrm{free}}+[-r,r]^{56}.
 \tag{23}
\]
The verifier evaluates \(F(z_0)\) and an outward-rounded interval
extension \(J_F({\cal X})\).  For a floating-point approximate inverse
\(R\) of the midpoint Jacobian it evaluates the Krawczyk set
\[
 K({\cal X})
 =
 z_0-RF(z_0)
 +(I-RJ_F({\cal X}))({\cal X}-z_0).
 \tag{24}
\]
Every arithmetic endpoint is rounded outwards with IEEE `nextafter`.
The verifier also checks that the interval derivative of the fixed
point map \(x\mapsto x-RF(x)\) has row-sum norm strictly below one.
The verified strict inclusion margin is
\[
 \boxed{\quad
 \operatorname{dist}\bigl(
 K({\cal X}),\partial{\cal X}\bigr)
 >9.9939\times10^{-10}.
 \quad}
 \tag{25}
\]
The contraction mapping theorem applied to
\[
 x\longmapsto x-RF(x),
 \tag{26}
\]
therefore gives a unique zero of \(F\) in \({\cal X}\).

Two explicitly checked \(2\times2\) factor minors remain separated
from zero throughout the box:
\[
 \det X_{\{13,22\},\{0,1\}}<0,\qquad
 \det Y_{\{12,20\},\{0,1\}}>0.
 \tag{27}
\]
Thus \(X\) and \(Y\) both have column rank two, so
\(XY^{\mathsf T}\) has rank exactly two.  The certified \(B\)-interval
is positive.  This completes the deferred existence and rank proof.

Because the zero is isolated and the system has rational
coefficients, all 56 free coordinates are real algebraic numbers.

## 4. What this eliminates, and what survives

The appealing implication
\[
 \beta\succeq0
 \quad\Longrightarrow\quad
 \operatorname{inertia}_-
 (P_-\beta^{\Gamma_2}P_-)\leq1
 \tag{28}
\]
is false even before stationarity is added.  Theorem 2.1 proves the
stronger failure after adding the actual same-\(C\) factorization,
balanced marginals, two-sided stationarity, and both separate
local-filter Hessians.

The exact isotropic arithmetic also identifies the relevant surviving
question:
\[
 \boxed{\qquad
 \text{Does physical isotropic }\beta
 \text{ always obey }A\leq5B?
 \qquad}
 \tag{29}
\]
By (8), (29) is precisely three-copy endpoint positivity within this
isotropic block-Gram stratum.  The counterexample has
\[
 \frac AB=\frac65,
 \tag{30}
\]
far below the negative threshold \(5\).  It therefore supplies no
evidence against (29).

Equivalently, (29) is the sharp overlap inequality
\[
 Q_2(\operatorname{Tr}_i C)
 \leq2\sum_{a,p}Q_2(C_{ap}).
 \tag{31}
\]
This is exactly the one-site recursion for \(Q_3(C)\), so merely
rewriting it does not prove it.  A successful argument must use a
nonlinear same-code constraint beyond positive block-Gram geometry
and the separate one-site critical forms.
