# Pair-centered purity obstruction and the sharp Haar envelope

## Status

This note records one exact obstruction and one exact scalar theorem
for the pair-centered criticality program.

First, the proposed six-purity certificate
\[
 \sum_{i=1}^3\sum_{\bullet=L,R}
 \left\|
 \operatorname{Herm}\operatorname{Tr}_{\widehat i}
 Z^\bullet
 \right\|_2^2
 \geq
 3c^2-\frac12qc,
 \qquad
 Z^L=CD^\dagger,\quad Z^R=D^\dagger C,
 \tag{1}
\]
where
\[
 q=Q_3(C),\qquad D=\Pi _2C,\qquad c=\|D\|_2^2,
 \tag{2}
\]
is false even at a balanced rank-two quotient-critical endpoint zero.
The counterexample is the rank-two orthogonal projection
\[
 \boxed{
 C=
 |\Phi _3\rangle\langle\Phi _3|_{13}
 \otimes
 (|0\rangle\langle0|+|1\rangle\langle1|)_2.
 }
 \tag{3}
\]
It has exact deficit
\[
 -\frac{2048}{2187}
 \tag{4}
\]
in (1).  This identifies a genuine equality orbit which any
zero-compatible critical inequality must preserve.

Second, let \(H=H^\dagger\), \(\operatorname{Tr}H=1\), and let
\({\cal R}(H)\) be the qutrit Haar divided difference from the global
quotient-criticality theorem.  We prove the sharp fixed-purity
envelope
\[
 \boxed{
 {\cal R}(H)\geq \rho(\operatorname{Tr}H^2),
 }
 \tag{5}
\]
with an explicit piecewise algebraic function \(\rho\).  Combining
this with criticality and the triple-Hodge fusion gives the exact
depth bound
\[
 \boxed{
 -\frac qc\leq
 \frac{135}{800+272{\cal P}},
 \qquad
 {\cal P}=\sum_{i=1}^3
 \rho\!\left(
 \max_{\bullet=L,R}\operatorname{Tr}(H_i^\bullet)^2
 \right).
 }
 \tag{6}
\]

The envelope is optimal as a one-matrix statement.  It also explains
precisely why purity plus the critical Haar inequalities cannot by
themselves finish the problem: the right side of (6) stays positive
for every finite \({\cal P}\).  A further same-\(C\) relation, or a
second-variation inequality which vanishes on (3), remains necessary.

The dependency-free exact checker is
`verification/verify_n3_pair_centered_purity_nogo.py`.

## 1. The exact flag--Bell obstruction

Put
\[
 P_\Phi=|\Phi _3\rangle\langle\Phi _3|,
 \qquad
 |\Phi _3\rangle=\frac1{\sqrt3}
 \sum_{r=0}^2|rr\rangle,
 \qquad
 P_2=|0\rangle\langle0|+|1\rangle\langle1|.
 \tag{7}
\]
With the physical tensor factors in the order \(1,2,3\), take
\[
 C=P_\Phi^{(13)}\otimes P_2^{(2)}.
 \tag{8}
\]
Both factors are orthogonal projections of ranks one and two, so
\[
 C=C^\dagger=C^2,\qquad \operatorname{rank}C=2.
 \tag{9}
\]

Let \(\Pi_S\) denote the scalar/traceless operator sector whose
traceless sites are exactly \(S\).  A direct orthogonal decomposition
gives, in mask order \(S=000,\ldots,111\),
\[
 \boxed{
 \left(\|\Pi_SC\|_2^2\right)_S
 =
 \left(
 \frac4{27},0,\frac2{27},0,0,\frac{32}{27},0,\frac{16}{27}
 \right).
 }
 \tag{10}
\]
Equivalently the masses in degrees \(0,1,2,3\) are
\[
 (x,a,c,d)
 =
 \left(\frac4{27},\frac2{27},\frac{32}{27},\frac{16}{27}\right).
 \tag{11}
\]
Using the exact sector formulas
\[
\begin{aligned}
 q&=-\frac18x+\frac14a-\frac12c+d,\\
 G&=\frac14a-c+3d,\\
 \Xi&=-5x+4a-\frac12c+\frac74d,
\end{aligned}
\tag{12}
\]
we obtain
\[
 \boxed{
 q=0,\qquad c=\frac{32}{27},\qquad
 G=\frac{11}{18},\qquad a=\frac2{27},\qquad\Xi=0.
 }
 \tag{13}
\]

There is a useful stronger multiplication identity.  Since the only
degree-two sector is the fully traceless \(13\)-component tensored
with the scalar part of \(P_2\),
\[
 D=\Pi _2C
 =
 \frac23\left(P_\Phi-\frac19I_{13}\right)\otimes I_2.
 \tag{14}
\]
Consequently
\[
 \boxed{
 CD^\dagger=D^\dagger C=\frac{16}{27}C.
 }
 \tag{15}
\]
There is no conflict with orthogonality of \(\Pi _2\): it is an
orthogonal projection on the operator Hilbert space, whereas \(D\)
need not be an idempotent operator.

Define
\[
\begin{aligned}
 X_i^L&=\operatorname{Herm}
 \operatorname{Tr}_{\widehat i}(CD^\dagger),\\
 X_i^R&=\operatorname{Herm}
 \operatorname{Tr}_{\widehat i}(D^\dagger C),\\
 H_i^{L,R}&=c^{-1}X_i^{L,R}.
\end{aligned}
\tag{16}
\]
Equation (15) and the marginals of (8) give, on both the left and
right,
\[
 \boxed{
 H_1=H_3=\frac13I_3,\qquad
 H_2=\frac12P_2.
 }
 \tag{17}
\]
Thus all six matrices are positive, have trace one, and obey
\[
 H_i^{L,R}\preceq\frac12I_3.
 \tag{18}
\]
Their total normalized purity and the corresponding raw quartic are
\[
\begin{aligned}
 \sum_{i,\bullet}\operatorname{Tr}(H_i^\bullet)^2
 &=2\left(\frac13+\frac12+\frac13\right)=\frac73,\\
 \sum_{i,\bullet}\|X_i^\bullet\|_2^2
 &=\frac73c^2=\frac{7168}{2187}.
\end{aligned}
\tag{19}
\]
Substitution into (1) gives
\[
 \sum_{i,\bullet}\|X_i^\bullet\|_2^2
 -3c^2+\frac12qc
 =
 -\frac23c^2
 =
 -\frac{2048}{2187}.
 \tag{20}
\]
The doubled quartic polynomial is therefore
\[
 qc-6c^2+2\sum_{i,\bullet}\|X_i^\bullet\|_2^2
 =-\frac{4096}{2187}.
 \tag{21}
\]

Finally, (8) is quotient-critical at \(\lambda=q/c=0\).  Indeed
\[
 L(P_2)=P_2-I_3=-|2\rangle\langle2|,
 \tag{22}
\]
so \(L^{\otimes3}(C)\) has its second-site row and column support
orthogonal to the singular planes of \(C\).  Hence
\[
 \boxed{
 C\,L^{\otimes3}(C)=
 L^{\otimes3}(C)\,C=0.
 }
 \tag{23}
\]
These are exactly the normal-space Euler equations for a rank-two
projection at \(\lambda=0\).

The weakest affine repair suggested by this example is
\[
 \sum_{i,\bullet}\|X_i^\bullet\|_2^2
 \stackrel{?}{\geq}
 \frac73c^2-\frac12qc.
 \tag{24}
\]
The example saturates (24).  At present (24) is a candidate, not a
theorem.

## 2. Sharp lower envelope of the Haar functional

Let the eigenvalues of a trace-one Hermitian \(3\times3\) matrix be
\[
 x\geq y\geq z,\qquad x+y+z=1,
 \tag{25}
\]
and put
\[
 P=x^2+y^2+z^2\geq\frac13.
 \tag{26}
\]
Recall
\[
 {\cal R}(H)=
 \sum_{\nu\in\{x,y,z\},\,\nu>1/2}
 \frac{(\nu-\frac12)^3}
 {\displaystyle\prod_{\nu'\ne\nu}(\nu-\nu')},
 \tag{27}
\]
with the continuous divided-difference interpretation at repeated
eigenvalues.

### Theorem

For every trace-one Hermitian \(H\),
\[
 {\cal R}(H)\geq\rho(P),
 \tag{28}
\]
where
\[
 \rho(P)=0,\qquad \frac13\leq P\leq\frac12,
 \tag{29}
\]
and, for \(1/2<P\leq3\),
\[
\begin{aligned}
 \alpha&=\frac{\sqrt{6P-2}-1}{6},\\
 \rho(P)&=
 \frac{2\alpha^2(3+16\alpha)}
 {(1+6\alpha)^2}.
\end{aligned}
\tag{30}
\]
For \(P\geq3\), put
\[
 t=\frac{2+\sqrt{18P-5}}6.
 \tag{31}
\]
Then
\[
 \rho(P)=
 \frac{3t^2-3t+\frac12}{6t-1}.
 \tag{32}
\]
The bound is attained for every \(P\).  At \(P=3\), both formulas
give
\[
 \alpha=\frac12,\qquad t=\frac32,\qquad
 \rho(3)=\frac{11}{32}.
 \tag{33}
\]
The function \(\rho\) is continuous and nondecreasing.

### Proof

If \(x\leq1/2\), then \(y,z\leq1/2\) and
\(z=1-x-y\geq0\).  Such spectra have \(P\leq1/2\) and
\({\cal R}=0\).  Conversely, the spectra interpolating from
\((1/3,1/3,1/3)\) to \((1/2,1/2,0)\) realize every
\(P\in[1/3,1/2]\).  This proves (29).

Assume \(P>1/2\).  At least one and at most two eigenvalues exceed
\(1/2\).

In the one-active regime write
\[
 x=\frac12+a,\qquad a>0,\qquad y,z\leq\frac12.
 \tag{34}
\]
At fixed \(P\), eliminating \(y,z\) gives
\[
 {\cal R}
 =
 \frac{a^3}{3a^2+a+\frac14-\frac12P}.
 \tag{35}
\]
The sign of its derivative with respect to \(a\) is the sign of
\[
 3a^2+2a+\frac34-\frac32P.
 \tag{36}
\]
The smallest admissible \(a\) occurs on the boundary
\[
 (x,y,z)=\left(\frac12+a,\frac12,-a\right),
 \qquad
 P=\frac12+a+2a^2.
 \tag{37}
\]
At that boundary (36) equals \(a/2>0\), and (36) increases with
\(a\).  Hence the one-active minimum is attained at (37).

In the two-active regime write
\[
 x=\frac12+a,\qquad y=\frac12+b,\qquad
 z=-(a+b),\qquad a\geq b>0.
 \tag{38}
\]
Set
\[
 s=a+b,\qquad p=ab,\qquad t=s+\frac12.
 \tag{39}
\]
Then
\[
 P=\frac12+s+2s^2-2p.
 \tag{40}
\]
At fixed \(P\), the allowed interval in \(s\) runs from \(p=0\),
which is the common boundary (37), to \(p=s^2/4\), where \(a=b\).
A direct divided-difference simplification gives
\[
 {\cal R}
 =
 -\frac12+
 \frac{t^3}{3t^2-t+\frac14-\frac12P}.
 \tag{41}
\]
The derivative sign is the sign of
\[
 3t^2-2t+\frac34-\frac32P.
 \tag{42}
\]
At the lower endpoint (42) is negative.  At the upper endpoint
\(a=b\), it changes sign exactly at
\[
 t=\frac32,\qquad P=3.
 \tag{43}
\]
Therefore, for \(1/2<P\leq3\), (41) decreases throughout the
allowed interval and is minimized at \(a=b=\alpha\).  There
\[
 P=\frac12+2\alpha+6\alpha^2,
 \tag{44}
\]
which gives the value of \(\alpha\) in (30), and the repeated-node
divided difference is
\[
 {\cal R}
 =
 \frac{2\alpha^2(3+16\alpha)}
 {(1+6\alpha)^2}.
 \tag{45}
\]

For \(P>3\), (42) has one zero inside the allowed interval:
\[
 t=\frac{2+\sqrt{18P-5}}6.
 \tag{46}
\]
Equation (41) decreases before and increases after that point.
At the critical point, (42) reduces its denominator and gives
\[
 {\cal R}
 =
 \frac{3t^2-3t+\frac12}{6t-1},
 \tag{47}
\]
proving (32).  These spectra are admissible because the critical
point lies between the \(p=0\) and \(p=s^2/4\) endpoints precisely
when \(P\geq3\).

The displayed minimizing spectra prove sharpness.  Continuity at the
two transitions is immediate from the formulas.  Monotonicity follows
on the interior critical branch by differentiating (41) with respect
to \(P\) at its minimizing \(t\); the derivative is positive.  It is
equally direct from (45) on the repeated-top branch. \(\square\)

## 3. Consequence at a negative quotient-critical point

For the pair-centered matrices of a hypothetical negative global
quotient minimizer, the established critical Haar inequalities are
\[
 g_i\geq\frac{16(-q)}{15}{\cal R}(H_i^L),
 \qquad
 g_i\geq\frac{16(-q)}{15}{\cal R}(H_i^R).
 \tag{48}
\]
Define
\[
\begin{aligned}
 P_i^\star&=
 \max\left\{
 \operatorname{Tr}(H_i^L)^2,
 \operatorname{Tr}(H_i^R)^2
 \right\},\\
 {\cal P}&=\sum_{i=1}^3\rho(P_i^\star).
\end{aligned}
\tag{49}
\]
Because \(\rho\) is nondecreasing, (28) and (48) imply
\[
 \boxed{
 G=\sum_i g_i\geq\frac{16(-q)}{15}{\cal P}.
 }
 \tag{50}
\]

The exact fusion identity is
\[
 q+\frac{27}{160}c
 =
 \frac{51}{160}G
 +\frac9{128}a+\frac1{40}\Xi.
 \tag{51}
\]
Put \(r=-q/c>0\).  Dividing (51) by \(c\), using (50), and retaining
the two nonnegative remainder terms gives
\[
 \boxed{
 r\left(1+\frac{17}{50}{\cal P}\right)
 \leq
 \frac{27}{160}
 -\frac9{128}\frac ac
 -\frac1{40}\frac{\Xi}{c}.
 }
 \tag{52}
\]
Discarding the remainders proves (6).

This is the sharp scalar consequence of the present Haar and purity
information.  It does not close any finite unbalanced regime:
the bound in (6) is strictly positive for finite \({\cal P}\).

## 4. What remains in the balanced locus

If a trace-one Hermitian \(3\times3\) matrix obeys
\[
 H\preceq\frac12I_3,
 \tag{53}
\]
then all its eigenvalues actually lie in \([0,1/2]\): the two largest
sum to at most one, so the smallest, which is one minus that sum, is
nonnegative.  Consequently
\[
 \frac13\leq\operatorname{Tr}H^2\leq\frac12,
 \qquad {\cal R}(H)=0.
 \tag{54}
\]
The example (3) lies in this balanced locus and has \(q=0\).  Thus:

* no strict balanced critical gap can hold at the endpoint boundary;
* the original coefficient \(3\) in (1) is impossible;
* any replacement must vanish on at least the flag--Bell orbit (3);
* balanced negative exclusion
  \[
  H_i^{L,R}\preceq\frac12I_3\ \forall i
  \quad\Longrightarrow\quad q\geq0
  \tag{55}
  \]
  remains consistent and sharp, but is not proved here.

Even if the repaired candidate (24) were true, in normalized form it
would give only
\[
 \sum_{i,\bullet}\operatorname{Tr}(H_i^\bullet)^2
 \geq\frac73+\frac r2.
 \tag{56}
\]
Balancedness supplies the upper bound \(3\), so (56) implies merely
\(r\leq4/3\), far too weak to contradict \(r>0\).  The required next
ingredient is therefore not another independent purity bound.  It is
a coupled normal-space or second-variation inequality which:

1. vanishes on the exact orbit (3);
2. is nonnegative on every rank-two tangent direction there; and
3. becomes strictly coercive when \(\lambda=q/c<0\).

This is the zero-compatible residual problem.
