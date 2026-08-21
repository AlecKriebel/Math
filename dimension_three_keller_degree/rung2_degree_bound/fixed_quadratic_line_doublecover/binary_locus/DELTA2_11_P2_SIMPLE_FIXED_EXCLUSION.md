# Provisional exclusion of the \(h=p^2\), simple-fixed-root
\(\delta=2,\{1,1\}\) row

**Status:** exact SymPy and independent PARI/GP replays pass; hostile
mathematical audit is pending.

**First recorded release (UTC):** 2026-07-25T12:56:53Z.

This work is not peer reviewed.  Exact checks are evidence about the
encoded algebra, not peer review.

## 1. Theorem and scope

In the binary fixed-quadratic line-double-cover row
\[
H_4=h(p,q)(p^2,q^2,0),
\]
no Keller counterexample lies on the exact-\(\delta=2\) incidence
\[
h=p^2,\qquad
R=p(Ap^2+Bpq+Cq^2),\qquad BC\ne0.                 \tag{1}
\]
This is the boundary-orbit mechanism in which the doubled fixed root
\(p=0\) occurs simply in \(R\), with no additional contact at \(q=0\).
It has Hilbert--Burch shape \(\{1,1\}\).

The theorem concerns only (1).  It does not exclude the other
exact-\(\delta=2,\{1,1\}\) incidence types.

## 2. The lifted \(E_6\) contact equation

Put
\[
P=p^4,\quad Q=p^2q^2,\quad
\alpha=J(Q,R),\quad\beta=-J(P,R),\quad
\gamma=J(P,Q).
\]
On \(BC\ne0\),
\[
\gcd(\alpha,\beta,\gamma)=2p^2.                   \tag{2}
\]
The mutations \(B=0\) and \(C=0\) instead have gcds
\(2p^2q\) and \(2p^3\), so they belong to \(\delta\ge3\).
The divisor \(A=0\) remains exact \(\delta=2\) and is retained below.

Set
\[
\Delta=4AC-B^2.
\]
On \(\Delta\ne0\), a polynomial basis of the two \(E_7\) tangents is
\[
\begin{aligned}
N_1&=(16Cp^2,\,-2q(3Bp-2Cq),\,3\Delta p),\\
N_2&=(-8Bp^2,\,2q(6Ap-Bq),\,3\Delta q).            \tag{3}
\end{aligned}
\]
Write \(N=sN_1+tN_2\).  The complete coefficient of \(r\) in \(E_6\)
has the form
\[
\Theta(X,Y,Z,x_5,y_5)=0,\qquad
(X,Y,Z)=(s^2,st,t^2),                              \tag{4}
\]
where \(\Theta\) is a \(6\times5\) linear coefficient matrix.  Thus
an actual tangent is not merely a vector in \(\ker\Theta\): its first
three coordinates must lie on the Veronese cone
\[
Y^2=XZ.                                            \tag{5}
\]

Take the first four coefficient rows of \(\Theta\).  Their five signed
maximal minors have common factor
\[
36864\,BC\Delta^2
\]
and primitive kernel vector
\[
\begin{aligned}
K=\big(&24AC+B^2,\,-BC,\,-32C^2,\\
      &576C^2\Delta,\,-9\Delta(32AC+B^2)\big).      \tag{6}
\end{aligned}
\]
Direct multiplication gives \(\Theta K=0\).  Since the third signed
minor is nonzero on \(BC\Delta\ne0\), \(\Theta\) has rank four there
and (6) spans its kernel.  Its basis-independent projective
intersection test is
\[
K_Y^2-K_XK_Z
 =3C^2(256AC+11B^2).                              \tag{7}
\]
Consequently every nonzero \(E_6\) tangent is obstructed except
possibly on
\[
\boxed{256AC+11B^2=0}.                             \tag{8}
\]
This is a signed-minor/Veronese certificate, not a generic-rank sample.

The basis (3) degenerates at \(\Delta=0\), which is still inside (1).
A fresh polynomial basis there is
\[
(8Cp^2,-3Bpq+2Cq^2,0),\qquad
(0,2pq,Bp+2Cq).
\]
The corresponding contact matrix again has rank four.  Its primitive
kernel vector and Veronese obstruction are
\[
(8,15B,0,192C^2,-27B^2),\qquad225B^2.             \tag{9}
\]
Thus \(\Delta=0\) has no nonzero tangent.  No pivot divisor has been
discarded.  Notice also that (8) gives
\[
\Delta=-\frac{75}{64}B^2\ne0,                     \tag{10}
\]
so (3) is valid on the sole survivor divisor.

## 3. The survivor is one stabilizer orbit

The invariant of the coefficients in (1) under diagonal pencil
rescaling and a nonzero rescaling of \(R\) is \(AC/B^2\).  Condition
(8) fixes it to \(-11/256\).  Explicitly, take
\[
\beta=1,\qquad\alpha=\frac{16C}{B},\qquad
\rho=\frac{B}{16C^2}.
\]
The change \((p,q)\mapsto(\alpha p,\beta q)\), followed by the
third-target rescaling \(\rho\), sends the coefficient triple to
\[
(A,B,C)=(-11,16,1).                                \tag{11}
\]
Hence it is enough to retain the rational normal form
\[
R=p(-11p^2+16pq+q^2).                              \tag{12}
\]
The normalization is stated explicitly; neither the tangent nor the
quadratic \(r\)-coefficients is silently normalized away.

For (12), the mandatory nonzero \(E_7/E_6\) contact family is
\[
\begin{aligned}
(U_r,V_r,T_r)
 &=k(4p^2,\,6pq+q^2,\,15p+30q),\\
([r^2]H_{2,1},[r^2]H_{2,2})
 &=(6k^2,9k^2).                                    \tag{13}
\end{aligned}
\]
For \(k=0\), (4)--(9) force all \(r\)-dependent nonlinear terms to
vanish.  The remaining constant \(E_6\) block is the full-rank
\(\mathcal M_1\) block of the \(\{1,1\}\) stratum, so all nonlinear
terms are binary.  The established degree-four plane-field and
birational Keller exit then makes the map an automorphism.

## 4. Full \(E_5\) obstruction on \(k\ne0\)

Retain arbitrary binary parts
\[
U_0,V_0\in\mathbb C[p,q]_3,\qquad
T_0,A_0,B_0\in\mathbb C[p,q]_2,
\]
both linear-in-\(r\) coefficients of \(A,B\), and all nine entries of
the linear part \(L=(\ell_{ij})\).  Write
\[
\begin{aligned}
U_0&=u_0p^3+u_1p^2q+u_2pq^2+u_3q^3,\\
V_0&=v_0p^3+v_1p^2q+v_2pq^2+v_3q^3,\\
T_0&=t_0p^2+t_1pq+t_2q^2.
\end{aligned}
\]
The complete constant \(E_6\) solve has rank six and gives
\[
\begin{aligned}
[r]A={}&k(-4t_2+3u_0+3u_1+108v_3)p\\
       &+k\left(\frac32u_1+6u_2+6v_3\right)q,\\
[r]B={}&3k(v_0+v_1)p\\
       &+k\left(-\frac12t_1+10t_2+\frac32v_1
                 +6v_2-\frac{621}{2}v_3\right)q,\\
\ell_{33}={}&k(2t_0-t_1+113t_2-3375v_3),\\
u_3={}&0.                                           \tag{14}
\end{aligned}
\]
A decisive \(6\times6\) minor is \(-49152k\), so (14) is
specialization-safe on \(k\ne0\).

After substituting the full solution (14), with every still-free lower
coefficient retained, the highest \(r\)-coefficient of \(E_5\) is
\[
[r^2]E_5
=-24k^3(72p^3+7p^2q-11pq^2+q^3).                 \tag{15}
\]
Its \(p^3\)-coefficient is \(-1728k^3\ne0\).  Thus the only nonzero
\(E_6\) contact orbit fails \(E_5\).

Combining the all-binary exit with (15) proves the theorem.

## 5. Verification

Run

```text
./verify_delta2_11_p2_simple_fixed_strict.sh
```

The strict wrapper requires exact whitelisted transcripts from both
SymPy and PARI/GP.  Each system reconstructs the signed-minor kernel,
the \(\Delta=0\) endpoint, the \(B=0,C=0,A=0\) mutations, the rational
survivor, the full \(E_6\) solve, and the decisive \(E_5\) coefficient.

The cited plane-field and birational Keller theorems are mathematical
inputs and are not verified by the computer algebra scripts.  Their
field/descent hypotheses are recorded in
`../../WORKING_FIXED_CUBIC_LINE_ROW.md`, Section 4.

This proof was developed with AI assistance.
