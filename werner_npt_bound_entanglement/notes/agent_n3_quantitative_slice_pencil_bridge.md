# Quantitative slice conditioning and the almost-\(2\times2\) pencil bridge

## Status

This note closes two quantitative steps in the proposed stability
route for the unrestricted three-copy endpoint.

1. A small local block-Gram defect, together with the exact marginal
   floor at a negative minimizer, forces all six slice factors to be
   uniformly well conditioned.
2. Once a two-plane has small local-support determinants, it can be
   projected to an exact \(2\times2\)-supported plane with explicit
   error.  Two independent approximate kernel slices on the original
   plane then force the projected plane close to a fixed-factor
   plane, again with explicit constants.

The remaining unproved step is now isolated cleanly: one needs a
global quantitative fixed-left inequality which converts a small
two-copy energy into small local-support determinants.  Everything
after that implication is supplied below.

Throughout,
\[
 {\cal B}_2(D,E)
 =\langle D,{\cal L}^{\otimes2}(E)\rangle_{\rm HS},
 \qquad
 {\cal L}(A)=A-\frac12\operatorname{Tr}(A)I_3.
 \tag{1}
\]
The operator norm of \({\cal L}^{\otimes2}\) on Hilbert--Schmidt
space is one.

## 1. A robust rank-one exclusion

### Lemma 1

Let \(M\) have rank at most two.  If
\[
 \|M\|_2\geq r,\qquad
 0\leq Q_2(M)\leq\varepsilon,\qquad
 \varepsilon\leq\frac{r^2}{64},
 \tag{2}
\]
then
\[
\boxed{\qquad
 s_2(M)\geq\frac r{15}.
 \qquad}                                                   \tag{3}
\]

### Proof

Write the singular-value decomposition as
\[
 M=M_1+M_2,\qquad
 \|M_j\|_2=s_j,\qquad s_1\geq s_2\geq0,
 \]
with both \(M_j\) rank one.  The established all-copy rank-one bound
at two copies and \(\|{\cal L}^{\otimes2}\|_{\rm op}=1\) give
\[
\begin{aligned}
 Q_2(M)
 &\geq\frac14s_1^2-2s_1s_2,\\
 s_1^2&\geq\frac12\|M\|_2^2\geq\frac12r^2.
\end{aligned}                                             \tag{4}
\]
If \(s_2<s_1/10\), then
\[
 Q_2(M)>\frac1{20}s_1^2
 \geq\frac1{40}r^2>\frac1{64}r^2,
\]
contradicting (2).  Hence
\[
 s_2\geq\frac{s_1}{10}
 \geq\frac r{10\sqrt2}>\frac r{15}.
\]
\(\square\)

## 2. Conditioning all six slice factors

Let
\[
 C=XSY^\dagger,\qquad
 X^\dagger X=Y^\dagger Y=I_2,\qquad
 0\prec S\preceq I_2,
 \tag{5}
\]
and at one physical site write
\[
 X=\sum_{a=0}^2|a\rangle\otimes X_a,\qquad
 Y=\sum_{b=0}^2|b\rangle\otimes Y_b.
 \tag{6}
\]
Put
\[
 A_a=X_aS,\qquad C_{ab}=A_aY_b^\dagger.
 \tag{7}
\]

Assume the two weighted slice Grams obey
\[
\begin{aligned}
 \left(\langle A_c,A_a\rangle_{\rm HS}\right)_{a,c=0}^2
 &\succeq mI_3,\\
 \left(\langle Y_dS,Y_bS\rangle_{\rm HS}\right)_{b,d=0}^2
 &\succeq mI_3
\end{aligned}                                             \tag{8}
\]
for some \(0<m\leq1\), and that the complete block Gram satisfies
\[
 \left|
 {\cal B}_2(C_{ap},C_{bq})
 -\gamma\delta_{ap}\delta_{bq}
 \right|\leq B
 \quad(a,p,b,q=0,1,2).                                   \tag{9}
\]

### Theorem 2 (explicit slice conditioning)

If
\[
\boxed{\qquad
 B\leq\frac{\gamma m^2}{77\,760\,000},
 \qquad}                                                  \tag{10}
\]
then every one of the six two-column factors is injective and
\[
\boxed{\qquad
 s_2(A_a),\,s_2(Y_b)
 \geq
 \kappa:=
 \frac{\sqrt\gamma\,m}{6750\sqrt6}
 \qquad(a,b=0,1,2).
 \qquad}                                                  \tag{11}
\]

### Proof

For each diagonal block, (9) and
\(Q_2(D)\leq\|D\|_2^2\) give
\[
 \|C_{aa}\|_2^2\geq\gamma-B.
 \tag{12}
\]
Let \(D=\operatorname{diag}(C_{00},C_{11},C_{22})\), and let
\(O=C-D\).  Each diagonal block has rank at most two, so it
contributes a singular value at least
\(\sqrt{(\gamma-B)/2}\).  Therefore
\[
 s_3(D)\geq\sqrt{\frac{\gamma-B}{2}}.
 \tag{13}
\]
Since \(\operatorname{rank}C\leq2\), Weyl's inequality gives
\[
 \|O\|_2\geq\|O\|_{\rm op}\geq s_3(D).
 \tag{14}
\]
The six off-diagonal blocks are Hilbert--Schmidt orthogonal.  Thus
one of them, say \(C_{ab}\) with \(a\ne b\), obeys
\[
 \|C_{ab}\|_2
 \geq\sqrt{\frac{\gamma-B}{12}}
 \geq\sqrt{\frac\gamma{24}}=:r_0,                         \tag{15}
\]
where (10) implies \(B\leq\gamma/2\).

The same condition also implies \(B\leq r_0^2/64\).  Since
\(0\leq Q_2(C_{ab})\leq B\), Lemma 1 gives
\[
 s_2(C_{ab})\geq\frac{r_0}{15}
 =:\kappa_0=\frac{\sqrt\gamma}{30\sqrt6}.                 \tag{16}
\]
Because
\[
 \|A_a\|_{\rm op},\|Y_b\|_{\rm op}\leq1,
 \]
the product singular-value inequalities imply
\[
 s_2(A_a),s_2(Y_b)\geq\kappa_0.                          \tag{17}
\]

Now use the bipartite graph with left vertices \(A_0,A_1,A_2\),
right vertices \(Y_0,Y_1,Y_2\), and all off-diagonal edges
\((c,d)\), \(c\ne d\).  If one endpoint of an edge has least
singular value at least \(\eta\), (8) gives
\[
 \|A_cY_d^\dagger\|_2\geq\eta\sqrt m.                    \tag{18}
\]
Provided \(B\leq\eta^2m/64\), Lemma 1 propagates the least singular
value \(\eta\sqrt m/15\) to both endpoints.

Starting from the edge in (17), one round reaches every vertex
except possibly \(A_b\) and \(Y_a\), with
\[
 \kappa_1=\frac{\kappa_0\sqrt m}{15}.
\]
A second round reaches those last two vertices with
\[
 \kappa_2=\frac{\kappa_0m}{225}
 =\frac{\sqrt\gamma\,m}{6750\sqrt6}.
 \tag{19}
\]
The stricter second-round requirement is
\[
 B\leq\frac{\kappa_0^2m^2}{225\cdot64}
 =\frac{\gamma m^2}{77\,760\,000},
\]
which is exactly (10). \(\square\)

## 3. Projecting an almost-supported plane

Let \(U:\mathbb C^2\to\mathbb C^3\otimes\mathbb C^3\) be an
isometry, \(P=UU^\dagger\), and let
\[
 \rho_1=\operatorname{Tr}_2P,\qquad
 \rho_2=\operatorname{Tr}_1P,\qquad
 d_j=\det\rho_j.
 \tag{20}
\]
Define
\[
 \tau=d_1^{1/3}+d_2^{1/3}.
 \tag{21}
\]

### Lemma 3 (exact support projection)

If \(\tau<1\), there are two-planes \(E,F\subseteq\mathbb C^3\)
and a two-plane \({\cal U}_0\subseteq E\otimes F\), with isometry
\(U_0\), such that
\[
\boxed{
\begin{aligned}
 \|P-P_0\|_2&\leq\sqrt{2\tau},\\
 \|U-U_0\|_{\rm op}&\leq\sqrt{2\tau},\\
 \|H_U-H_{U_0}\|_{\rm op}&\leq2\sqrt{2\tau},
\end{aligned}}
\qquad P_0=U_0U_0^\dagger.                               \tag{22}
\]
The frame \(U_0\) in the second line is chosen in the polar gauge
relative to \(U\).

### Proof

Let the eigenvalues of \(\rho_j\) be
\(\lambda_{j,1}\geq\lambda_{j,2}\geq\lambda_{j,3}\).
Since
\[
 d_j=\lambda_{j,1}\lambda_{j,2}\lambda_{j,3}
 \geq\lambda_{j,3}^3,
\]
we have \(\lambda_{j,3}\leq d_j^{1/3}\).  Take \(E,F\) to be the
top two eigenspaces of the two marginals.  Then
\[
\begin{aligned}
 \ell
 &:=
 \operatorname{Tr}\bigl(P(I-P_E\otimes P_F)\bigr)\\
 &\leq
 \operatorname{Tr}\bigl(P((I-P_E)\otimes I)\bigr)
 +\operatorname{Tr}\bigl(P(I\otimes(I-P_F))\bigr)\\
 &=\lambda_{1,3}+\lambda_{2,3}
 \leq\tau.                                               \tag{23}
\end{aligned}
\]
Since \(\ell<1\), the projection
\((P_E\otimes P_F)U\) has rank two.  Let \(U_0\) be its polar
isometry.  The principal-angle identities give
\[
 \|P-P_0\|_2^2=2\ell,\qquad
 \|U-U_0\|_{\rm op}\leq\sqrt{2\ell}.                     \tag{24}
\]

For arbitrary \(W,Z:\mathbb C^2\to
\mathbb C^3\otimes\mathbb C^3\), expand
\[
\begin{aligned}
 &{\cal B}_2(UW^\dagger,UZ^\dagger)
 -{\cal B}_2(U_0W^\dagger,U_0Z^\dagger)\\
 &\quad=
 {\cal B}_2((U-U_0)W^\dagger,UZ^\dagger)
 +{\cal B}_2(U_0W^\dagger,(U-U_0)Z^\dagger).
\end{aligned}
\]
Since \(\|{\cal L}^{\otimes2}\|_{\rm op}=1\), its modulus is at most
\[
 2\|U-U_0\|_{\rm op}\|W\|_2\|Z\|_2.
\]
This proves the final line of (22). \(\square\)

## 4. Quantitative distance to a factor plane

For a two-plane \({\cal U}\subset\mathbb C^2\otimes\mathbb C^2\),
let \(M_{\cal U}\) be its symmetric annihilator-pencil matrix from
`notes/agent_n2_qubit_support_second_kernel_gap.md`, and put
\[
 \mu=\|M_{\cal U}\|_2.
 \tag{25}
\]

### Lemma 4 (minor-to-factor distance)

There is a fixed-factor plane \({\cal F}\) such that
\[
\boxed{\qquad
 \|P_{\cal U}-P_{\cal F}\|_2\leq\sqrt{8\mu}.
 \qquad}                                                  \tag{26}
\]

### Proof

It is enough to prove the assertion for the bilinear annihilator
plane
\({\cal L}=\overline{{\cal U}^{\perp}}\), because complex
conjugation preserves projector distance and factor planes, while
orthogonal complementation preserves projector distance and
interchanges the two factor rulings.  Choose an orthonormal matrix
frame \(A,B\) of \({\cal L}\).
Local unitaries and a scalar phase put
\[
 A=\begin{pmatrix}a&0\\0&b\end{pmatrix},
 \qquad a\geq b\geq0,\qquad a^2+b^2=1.
 \tag{27}
\]
Write
\[
 B=\begin{pmatrix}p&q\\r&s\end{pmatrix}.
 \tag{28}
\]
The entries of \(M_{\cal U}\) are
\[
 (M_{\cal U})_{11}=2ab,\qquad
 (M_{\cal U})_{12}=as+bp,\qquad
 (M_{\cal U})_{22}=2(ps-qr),
 \tag{29}
\]
up to common unit phases which do not affect the estimates.

Assume first that \(\mu\leq1/2\).  From (29),
\[
 b\leq\frac{\mu}{\sqrt2}.
 \tag{30}
\]
Orthogonality of \(A,B\) gives \(ap+bs=0\).  Since
\[
 a^2-b^2\geq\sqrt{1-\mu^2}\geq\frac{\sqrt3}{2},
\]
the middle equation in (29) gives
\[
 |s|\leq\frac{2\mu}{\sqrt3},\qquad
 |p|\leq\frac{2\mu^2}{\sqrt3}.                           \tag{31}
\]
The last equation in (29) then gives
\[
 |qr|
 \leq |ps|+\frac\mu2
 \leq\frac{4\mu^3}{3}+\frac\mu2
 \leq\frac{5\mu}{6}.                                    \tag{32}
\]
Hence
\[
 \min\{|q|^2,|r|^2\}\leq\frac{5\mu}{6}.                 \tag{33}
\]

If \(|r|\leq|q|\), compare \({\cal L}\) with the fixed-row plane
\(\operatorname{span}\{E_{11},E_{12}\}\); if
\(|q|\leq|r|\), compare it with the fixed-column plane
\(\operatorname{span}\{E_{11},E_{21}\}\).  In either case the
leakage is at most
\[
 b^2+|s|^2+\min\{|q|^2,|r|^2\}
 \leq\frac{7\mu}{4}<4\mu.                               \tag{34}
\]
For two rank-two projections, squared Frobenius distance is twice
the leakage, proving (26) in this case.

If \(\mu>1/2\), the leakage from \({\cal L}\) to any rank-two
factor plane is at most two.  Thus it is at most \(4\mu\), and the
same projector-distance conclusion follows. \(\square\)

## 5. The complete almost-boundary bridge

### Theorem 5

Let \(U,P,d_j,\tau\) be as in Section 3, with \(\tau<1\).
Suppose \(W_1,W_2\) satisfy
\[
 \left(\langle W_p,W_q\rangle_{\rm HS}\right)_{p,q=1}^2
 \succeq\eta I_2,\qquad
 \|W_p\|_2\leq R,                                        \tag{35}
\]
and
\[
 |\langle W_p,H_UW_q\rangle|\leq B
 \qquad(p,q=1,2).                                        \tag{36}
\]
Put
\[
 B_0=B+2R^2\sqrt{2\tau}.                                 \tag{37}
\]
Then the exact \(2\times2\)-supported projection
\({\cal U}_0\) from Lemma 3 obeys
\[
\boxed{
\begin{aligned}
 \|M_{{\cal U}_0}\|_2^2&\leq\frac{40B_0}{\eta},\\
 \left|\det\operatorname{mat}(\Lambda z)\right|^2
 &\leq\frac{10B_0}{\eta}\|z\|^4.
\end{aligned}}                                           \tag{38}
\]
Moreover, there is a fixed-factor plane \({\cal F}\) with
\[
\boxed{\qquad
 \|P-P_{\cal F}\|_2
 \leq
 \sqrt{2\tau}
 +\sqrt8\left(\frac{40B_0}{\eta}\right)^{1/4}.
 \qquad}                                                  \tag{39}
\]

### Proof

Lemma 3 and (35) show that all four entries of
\[
 \bigl(\langle W_p,H_{U_0}W_q\rangle\bigr)_{p,q=1}^2
\]
have modulus at most \(B_0\).  The Gram floor remains \(\eta I_2\).
Corollary 5.1 of
`notes/agent_n2_qubit_support_second_kernel_gap.md`—or directly its
min--max proof—gives (38).  Lemma 4 and the triangle inequality give
(39). \(\square\)

## 6. Substitution of the negative-minimizer constants

At a hypothetical negative global minimizer, write
\[
 q=-\delta,\qquad
 \gamma=\frac{2\delta}{3},\qquad
 m=\frac{\delta}{1+2\delta}.
 \tag{40}
\]
The exact marginal-floor theorem supplies (8), while quantitative
Haar isotropy supplies (9) with
\[
 B=4752\sqrt{15}\,\sqrt{g_i}.                            \tag{41}
\]
If (10) holds, Theorem 2 gives
\[
 \kappa^2m
 =\frac{\gamma m^3}{273\,375\,000}.                      \tag{42}
\]

For a fixed row slice \(A_a\), take the two indices \(p\ne a\).
The corresponding vectors
\[
 W_p=Y_p(A_a^\dagger A_a)^{1/2}
\]
have Gram at least \(\kappa^2mI_2\), norm at most \(\sqrt2\), and
their \(H_{\operatorname{ran}A_a}\)-Gram entries have modulus at
most \(B\).  Thus Theorem 5 applies with
\[
 \eta=\frac{\gamma m^3}{273\,375\,000},\qquad
 R^2=2,\qquad
 B_0=B+4\sqrt{2\tau_a},                                  \tag{43}
\]
as soon as the support-determinant quantity \(\tau_a\) is known.
The identical statement holds for every left and right slice plane.

The only missing implication in this chain is therefore a bound on
\(\tau_a\) from the approximate fixed-left kernel.  For example, the
numerically sharp but presently unproved inequality
\[
 H_U\succeq
 \frac{\det\rho_1+\det\rho_2}{4}\,I                      \tag{44}
\]
would give, from one vector of squared norm at least \(\eta\),
\[
 d_1+d_2\leq\frac{4B}{\eta},\qquad
 \tau\leq2^{2/3}\left(\frac{4B}{\eta}\right)^{1/3}.
 \tag{45}
\]
Equations (39), (43), and (45) would then make the entire
slice-to-factor-pencil passage explicit.  Thus (44), or any weaker
global determinant gap with an explicit modulus, is the remaining
local analytic frontier; neither projection to the boundary nor
conditioning of the common slices remains an obstruction.
