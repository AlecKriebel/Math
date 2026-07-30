# Lossless elimination of the scalar and one-body sectors in the full \(n=3\) dual

## Status

This note gives a lossless reduction of the full qutrit three-copy
Ky--Fan inequality.  For a fixed right two-plane, the scalar and all
three one-body coefficients can be eliminated exactly.  The remaining
statement contains only the three doubly-traceless pair coefficients
and one explicit inverse marginal operator.

The reduction does **not** prove the residual inequality.  An exact
two-direction example proves that the residual is not the
scalar-reflection target in disguise: one-body elimination produces a
genuinely anisotropic correction which the reflection norm and trace
data do not see.

The dependency-free exact checker is
`verification/verify_n3_full_dual_low_sector_elimination.py`.

## 1. Fixed-plane form of the full dual

Write
\[
 D=cI_{27}+\sum_{i=1}^3A_i^{(i)}
       +\sum_{i<j}B_{ij}^{(ij)},                         \tag{1}
\]
where
\[
 \operatorname{Tr}A_i=0,\qquad
 \operatorname{Tr}_iB_{ij}
 =\operatorname{Tr}_jB_{ij}=0.                          \tag{2}
\]
The exact full dual theorem asks for
\[
\boxed{
 s_1(D)^2+s_2(D)^2
 \leq24|c|^2+12\sum_i\|A_i\|_2^2
             +2\sum_{i<j}\|B_{ij}\|_2^2 .
}                                                        \tag{3}
\]

Here the constants are exactly the sector weights, with no rescaling
hidden in the notation.  Indeed, orthogonality of the
scalar/traceless decomposition gives
\[
\begin{aligned}
 \|D_0\|_2^2&=27|c|^2,\\
 \|D_1\|_2^2&=9\sum_i\|A_i\|_2^2,\\
 \|D_2\|_2^2&=3\sum_{i<j}\|B_{ij}\|_2^2.
\end{aligned}                                            \tag{3a}
\]
Substitution into the exact degree-weighted bound
\[
 s_1(D)^2+s_2(D)^2
 \leq\frac89\|D_0\|_2^2
      +\frac43\|D_1\|_2^2
      +\frac23\|D_2\|_2^2
 \tag{3b}
\]
is precisely (3).  By the established low-rank duality reduction,
(3) for every \(D\) is equivalent to
\(Q_3(C)\geq0\) for every \(\operatorname{rank}C\leq2\).

For an isometry
\[
 V:\mathbb C^2\longrightarrow
 {\cal H}:=(\mathbb C^3)^{\otimes3},
 \qquad V^\dagger V=I_2,
 \tag{4}
\]
low-rank duality gives
\[
 s_1(D)^2+s_2(D)^2
 =\max_{V^\dagger V=I_2}\|DV\|_2^2.                    \tag{5}
\]
Consequently (3) is equivalent to its fixed-plane version for every
\(V\).

Put
\[
 B=\sum_{i<j}B_{ij}^{(ij)},\qquad Y=BV,                 \tag{6}
\]
and collect the low-sector coefficients as
\[
 x=(c,A_1,A_2,A_3).
 \tag{7}
\]
Define
\[
\begin{aligned}
 L_Vx&=\left(cI+\sum_iA_i^{(i)}\right)V,\\
 \langle x,W x\rangle
 &=24|c|^2+12\sum_i\|A_i\|_2^2,\\
 p(B)&=2\sum_{i<j}\|B_{ij}\|_2^2.
\end{aligned}                                            \tag{8}
\]
The fixed-plane deficit is exactly
\[
 \Delta_V(x,B)
 =\langle x,Wx\rangle+p(B)-\|L_Vx+Y\|_2^2.              \tag{9}
\]

## 2. The explicit marginal Schur operator

Vectorize \(V\) as the unnormalized code purification
\[
 |\boldsymbol V\rangle
 =\sum_{r=0}^1v_r\otimes|r\rangle_K,\qquad
 R_V=|\boldsymbol V\rangle\langle\boldsymbol V|.
 \tag{10}
\]
Thus \(\|\boldsymbol V\|^2=2\).  For a physical site \(i\), let
\[
 e_i(X)=I_i\otimes\operatorname{Tr}_iX.                  \tag{11}
\]
Define
\[
\boxed{
 S_V
 =I-\frac1{12}\sum_{i=1}^3e_i(R_V)+\frac1{24}R_V.
}                                                        \tag{12}
\]

### Proposition 2.1

The operator \(S_V\) is strictly positive.  More precisely,
\[
 \boxed{\qquad S_V\succeq\frac5{12}I. \qquad}            \tag{13}
\]
Moreover,
\[
 \boxed{\qquad
 S_V=I-L_VW^{-1}L_V^\dagger .
 \qquad}                                                  \tag{14}
\]

### Proof

Choose a Hilbert--Schmidt orthonormal basis
\((T_\alpha)_{\alpha=1}^8\) of traceless qutrit matrices.
The scalar and one-body frame operators give
\[
\begin{aligned}
 L_VW^{-1}L_V^\dagger
 ={}&\frac1{24}R_V\\
 &+\frac1{12}\sum_{i=1}^3\sum_{\alpha=1}^8
 |T_\alpha^{(i)}\boldsymbol V\rangle
 \langle T_\alpha^{(i)}\boldsymbol V|.
\end{aligned}                                            \tag{15}
\]
Completeness of the traceless matrix basis says
\[
 \sum_{\alpha=1}^8T_\alpha XT_\alpha^\dagger
 =I_3\operatorname{Tr}X-\frac13X.                       \tag{16}
\]
Applying (16) at site \(i\) to \(R_V\) turns (15) into
\[
 L_VW^{-1}L_V^\dagger
 =\frac1{12}\sum_ie_i(R_V)-\frac1{24}R_V,                \tag{17}
\]
which proves (14).

It remains to prove a uniform strict bound.  The scalar block
\[
 c\longmapsto\frac{c}{\sqrt{24}}V
 \tag{18}
\]
has squared operator norm \(2/24=1/12\).  For a one-body block,
\[
\begin{aligned}
 \left\|\frac1{\sqrt{12}}A_i^{(i)}V\right\|_2^2
 &=\frac1{12}\operatorname{Tr}
   \left(A_i^\dagger A_i\,\rho_i^V\right)\\
 &\leq\frac16\|A_i\|_2^2,
\end{aligned}                                            \tag{19}
\]
because
\[
 \rho_i^V=\operatorname{Tr}_{\widehat i}(VV^\dagger)
 \succeq0,\qquad \operatorname{Tr}\rho_i^V=2,
 \qquad \|\rho_i^V\|_\infty\leq2.                       \tag{20}
\]
Cauchy--Schwarz for the four block maps in (18)--(19)
therefore gives
\[
 \|L_VW^{-1/2}\|^2
 \leq\frac1{12}+3\frac16=\frac7{12}.                    \tag{21}
\]
Equations (14) and (21) prove (13). \(\square\)

## 3. Lossless Schur elimination

Let
\[
 K_V=W-L_V^\dagger L_V.                                 \tag{22}
\]
Proposition 2.1 implies \(K_V\succ0\).  Completing the square in
(9) gives
\[
\begin{aligned}
 \inf_x\Delta_V(x,B)
 ={}&p(B)-\|Y\|_2^2\\
 &-\left\langle
 L_V^\dagger Y,K_V^{-1}L_V^\dagger Y
 \right\rangle.
\end{aligned}                                            \tag{23}
\]
The Woodbury identity gives
\[
 S_V^{-1}
 =I+L_VK_V^{-1}L_V^\dagger.                             \tag{24}
\]
Thus (23) becomes the promised residual.

### Theorem 3.1

The full unrestricted dual inequality (3) is exactly equivalent to
\[
\boxed{
 \left\langle BV,S_V^{-1}BV\right\rangle_{\rm HS}
 \leq2\sum_{i<j}\|B_{ij}\|_2^2
}                                                        \tag{25}
\]
for every isometry \(V\) and every three doubly-traceless pair
coefficients \(B_{ij}\), with \(S_V\) given by (12).

The equivalence is lossless in both directions.  If (3) holds, then
\(\Delta_V(x,B)\geq0\) for every \(x\), so its exact infimum (23) is
nonnegative and gives (25).  Conversely, if (25) holds, then (23) is
nonnegative; since (23) is the minimum of (9), every
\(\Delta_V(x,B)\) is nonnegative.  This holds for every \(V\), and
(5) recovers (3).  In view of (3a)--(3b) and low-rank duality, (25)
is therefore equivalent to the unrestricted endpoint statement
\[
 Q_3(C)\geq0\qquad(\operatorname{rank}C\leq2).
\]

No scalar or one-body coefficient remains in (25).  The inverse is
uniformly harmless:
\[
 I\preceq S_V^{-1}\preceq\frac{12}{5}I.                 \tag{26}
\]

The minimizing low-sector coefficients are also explicit.  Write
\[
 Z=S_V^{-1}BV.
 \tag{27}
\]
Then
\[
\boxed{
\begin{aligned}
 c_*&=\frac1{24}\operatorname{Tr}(V^\dagger Z),\\
 A_{i,*}
 &=\frac1{12}
 \left(\operatorname{Tr}_{\widehat i}(ZV^\dagger)\right)_0,
\end{aligned}}                                           \tag{28}
\]
where the subscript \(0\) denotes the traceless part.  These are
unique because \(K_V\succ0\).

## 4. Why this is not the reflection residual

Eliminating only the scalar in the strengthened reflection frontier
produces
\[
 \|BV\|_2^2+
 \frac1{16}\left|\operatorname{Tr}(V^\dagger BV)\right|^2
 \leq2\sum_{i<j}\|B_{ij}\|_2^2.                         \tag{29}
\]
Equation (25) contains more information.  The following exact pair
of directions has identical data on both sides of (29), but distinct
left sides in (25).

Take
\[
 V=(|000\rangle,|111\rangle)                            \tag{30}
\]
and put
\[
 H=E_{00}-\frac12E_{11}-\frac12E_{22}.                  \tag{31}
\]
Only \(B_{12}\) is nonzero.  Define
\[
\begin{aligned}
 B_{12}^{(a)}
 &=E_{10}\otimes H,\\
 B_{12}^{(b)}
 &=E_{10}\otimes E_{10}
 +\frac12E_{02}\otimes E_{02}
 +\frac12E_{12}\otimes E_{12}.
\end{aligned}                                            \tag{32}
\]
Every local factor in (32) is traceless, and orthogonality of the
matrix units gives
\[
 \|B_{12}^{(a)}\|_2^2
 =\|B_{12}^{(b)}\|_2^2=\frac32.                         \tag{33}
\]
Their two outputs are
\[
\begin{aligned}
 Y_a=B^{(a)}V&=(|100\rangle,0),\\
 Y_b=B^{(b)}V&=(|110\rangle,0).
\end{aligned}                                            \tag{34}
\]
Consequently, for both \(r=a,b\),
\[
 \|Y_r\|_2^2=1,\qquad
 \operatorname{Tr}(V^\dagger Y_r)=0,\qquad
 p(B^{(r)})=3.                                          \tag{35}
\]
Thus the reflection residual (29) sees the identical inequality
\(1\leq3\).

On the other hand, with
\[
 |\boldsymbol V\rangle=|000,0\rangle+|111,1\rangle,
 \tag{36}
\]
direct contraction gives
\[
\begin{aligned}
 e_1(R_V)Y_a&=Y_a,&
 e_2(R_V)Y_a=e_3(R_V)Y_a=R_VY_a&=0,\\
 e_i(R_V)Y_b&=0\quad(i=1,2,3),&
 R_VY_b&=0.
\end{aligned}                                            \tag{37}
\]
Equation (12) therefore gives
\[
 S_VY_a=\frac{11}{12}Y_a,\qquad
 S_VY_b=Y_b.                                             \tag{38}
\]
Hence
\[
\boxed{
 \langle Y_a,S_V^{-1}Y_a\rangle=\frac{12}{11},
 \qquad
 \langle Y_b,S_V^{-1}Y_b\rangle=1.
}                                                        \tag{39}
\]
The two directions have the same pair norm, output norm, and scalar
compression, but the full low-sector elimination distinguishes them.
Thus no reduction depending only on the reflection quantities in
(29) can be lossless.

For an independent direct check, the unique optimal low coefficients
are
\[
 c_*=0,\qquad
 A_{1,*}=\frac1{11}E_{10},\qquad
 A_{2,*}=A_{3,*}=0
 \tag{40}
\]
for \(B^{(a)}\), and all four vanish for \(B^{(b)}\).  The minimized
deficits are respectively
\[
 3-\frac{12}{11}=\frac{21}{11},
 \qquad
 3-1=2.                                                  \tag{41}
\]

## 5. Remaining exact lemma

After lossless elimination, the entire unrestricted three-copy
problem is the single pair-coefficient inequality (25):
\[
 \left\|S_V^{-1/2}
 \left(\sum_{i<j}B_{ij}^{(ij)}\right)V\right\|_2^2
 \leq2\sum_{i<j}\|B_{ij}\|_2^2.                         \tag{42}
\]
The operator \(S_V\) is an explicit function of one code plane and
its three two-body logical marginals.  Relative to the pair-only
frontier, the sole new issue is the positive frame correction
\[
 S_V^{-1}-I
 =L_V(W-L_V^\dagger L_V)^{-1}L_V^\dagger.               \tag{43}
\]
A proof must pay for this correction from the slack of the
pair-only action; it cannot replace it by the scalar reflection
penalty alone.
