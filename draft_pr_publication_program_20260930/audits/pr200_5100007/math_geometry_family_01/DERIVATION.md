# Direct focal-conic derivation for k115

Author of this audit: independent geometry verification family. This is a verification artifact, not a priority claim. The early mechanism and challenge list were frozen before reading the submitted proof; see `EARLY_CHALLENGE_FREEZE.md`. The following direct one-focus factorization was obtained after that freeze and after reading the submission. Its ancestry is therefore recorded precisely: the tangent/conic and divisor approach was independent; comparison with the submitted proof preceded completion of the factorization.

## 1. Claim and conventions

Let

\[
 E:x^2/a^2+y^2/b^2=1,\quad a>b>0,\quad c^2=a^2-b^2,
\]

and fix a strictly nested confocal caustic

\[
 C:x^2/\alpha^2+y^2/\beta^2=1,\quad
 \alpha^2=a^2-\lambda,\quad\beta^2=b^2-\lambda,
 \quad0<\lambda<b^2.
\]

Thus \(c^2=\alpha^2-\beta^2\). Consecutive vertices \(P_i\) lie on \(E\), and each side is tangent to \(C\). Let \(Q_i\) be the intersection of the tangents to \(E\) at \(P_i,P_{i+1}\). Assume the real orbit has **least** period \(N\), with \(4\mid N\). The claim is constancy, over every real initial phase, of

\[
 R_\pm=\prod_{i=0}^{N-1}|Q_i-(\pm c,0)|.
\]

The focus, outer ellipse and caustic are fixed while phase varies. The proof covers every primitive winding compatible with them. Distances are ordinary positive Euclidean distances. Complexification below is applied only to their squared polynomial expressions.

## 2. Real parametrization derived directly from chord tangency

Use Jacobi functions with modulus \(k\), and write

\[
 k=c/\alpha\in(0,1),\qquad k'=\beta/\alpha,
 \qquad K=K(k),\quad K'=K(k').
\]

Choose the unique \(v\in(0,K)\) such that

\[
 h=\operatorname{sn}v=\sqrt\lambda/b,
 \quad C_v=\operatorname{cn}v=\beta/b>0,
 \quad D_v=\operatorname{dn}v>0.
\]

The relations

\[
 a=\alpha D_v/C_v,\qquad b=\beta/C_v,                  \tag{1}
\]

follow by squaring: \(\alpha^2D_v^2/C_v^2=(\alpha^2b^2-c^2\lambda)/\beta^2=a^2\). No canonical-parametrization theorem is needed as an unproved input.

Set \(P(w)=(a\operatorname{sn}w,b\operatorname{cn}w)\). For real \(u\), abbreviate \(s=\operatorname{sn}u,z=\operatorname{cn}u,d=\operatorname{dn}u\), and \(D_0=1-k^2h^2s^2>0\). The addition formulas give

\[
 \operatorname{sn}(u\pm v)=(sC_vD_v\pm hzd)/D_0,
\quad
 \operatorname{cn}(u\pm v)=(zC_v\mp shdD_v)/D_0.
\]

Consequently the chord through \(P(u-v),P(u+v)\) is

\[
 (sD_v/a)x+(z/b)y=C_v.                                \tag{2}
\]

Indeed, substitution yields \(C_v(s^2D_v^2+z^2)/D_0=C_v\), because \(s^2D_v^2+z^2=D_0\). Its support-function tangency test for \(C\) is

\[
 \alpha^2s^2D_v^2/a^2+\beta^2z^2/b^2=C_v^2(s^2+z^2)=C_v^2.
\]

Thus every such chord is tangent to the fixed caustic. Conversely, from each point of \(E\) the strictly nested convex caustic has exactly two distinct real tangents. The two chords joining \(P(w)\) to \(P(w+2v)\) and \(P(w-2v)\) give those two tangents. Their other endpoints are distinct, since \(0<2v<2K\). They therefore exhaust the two possible oriented Poncelet steps. Following either orientation gives the constant parameter step

\[
 \delta=2v\in(0,2K),\qquad P_i=P(w_0+i\delta),           \tag{3}
\]

or its reversal. In the assumed confocal billiard setting these are precisely the two orientations of the billiard family.

The map \(P\) is injective on the real parameter circle of length \(4K\): its pair \((\operatorname{sn}w,\operatorname{cn}w)\) winds once around the unit circle, as follows from the strictly increasing real Jacobi amplitude. Hence least period \(N\) means exactly

\[
 \delta=4Kr/N,\qquad\gcd(r,N)=1,\quad0<r<N/2.           \tag{4}
\]

This derives both primitive closure and all admitted star windings. It does not identify all caustics having a given \(N\) with one caustic.

## 3. Direct tangent intersection and its real regularity

The tangent at \(P(w)\) has equation

\[
 x\operatorname{sn}w/a+y\operatorname{cn}w/b=1.
\]

Solving the two linear equations using the same addition formulas gives

\[
 Q(u)=(A\operatorname{sn}u,B\operatorname{cn}u),\quad
 A=aD_v/C_v=a^2/\alpha,\quad B=b/C_v=b^2/\beta.         \tag{5}
\]

The absolute determinant of the tangent normals is

\[
 2hC_vd/(abD_0)>0.                                    \tag{6}
\]

Thus this computation applies at every real phase, including the axes; it never divides by \(s\) or \(z\). No \(Q\) is at infinity. Also

\[
 Q_x^2/a^2+Q_y^2/b^2-1
 =h^2\operatorname{dn}^2u/C_v^2>0.                     \tag{7}
\]

So \(Q\) is outside \(E\), while both foci are inside. Every real focal distance is strictly positive. The original sequence has phase \(u=w_0+v\); that fixed offset does not restrict phase.

For comparison with a purely elementary conic computation, if \(P(\theta)=(a\cos\theta,b\sin\theta)\), and \(m=(\theta+\phi)/2,d_\theta=(\phi-\theta)/2\), then

\[
 Q=(a\cos m/\cos d_\theta,b\sin m/\cos d_\theta),
\quad
 \sin^2d_\theta=\lambda(\cos^2m/a^2+\sin^2m/b^2).
\]

Elimination yields the same outer conic

\[
 (\alpha^2/a^4)Q_x^2+(\beta^2/b^4)Q_y^2=1.
\]

Its semiaxes may switch order, and the conic can be a circle. Neither event invalidates (5).

## 4. Focal isotropic roots: a direct one-focus factorization

Define the meromorphic polynomial expression

\[
 f(u)=(Q_x(u)-c)^2+Q_y(u)^2
     =M-2Ac\operatorname{sn}u+L\operatorname{sn}^2u,
\quad M=B^2+c^2>0,\quad L=A^2-B^2.                    \tag{8}
\]

Geometrically, its complex zeros arise where the outer conic meets either isotropic line \(Q_x-c\pm iQ_y=0\) through the focus. This supplies a useful distinguished root without guessing a product identity. In fact,

\[
 A-ck=Bk',                                             \tag{9}
\]

because, with \(t=h^2,q=1-t\),
\(A=\alpha(1-k^2t)/q\), \(B=\alpha k'/q\), and \(c=\alpha k\).
At \(\operatorname{sn}u=1/k\), one has \(\operatorname{cn}^2u=-k'^2/k^2\), so (9) proves \(f=0\). Equivalently \(2Ac=kM+L/k\).

The second root is determined by the product of roots. The double-angle formulas, obtained by setting the two arguments equal in the addition laws, give

\[
 \frac{\operatorname{cn}\delta}{\operatorname{dn}\delta}
 =\frac{1-2t+k^2t^2}{1-2k^2t+k^2t^2},
\qquad
 \frac{L}{M}=k^2\frac{\operatorname{cn}\delta}{\operatorname{dn}\delta}.
\]

Therefore the squared distance factors **uniformly**, even when \(L=0\), as

\[
 \boxed{f(u)=M(1-k\operatorname{sn}u)
 \left(1-k\frac{\operatorname{cn}\delta}{\operatorname{dn}\delta}
                 \operatorname{sn}u\right).}           \tag{10}
\]

This directly factors the one-focus quantity, rather than first multiplying the quantities for the two foci. The only denominator in (10) is \(\operatorname{dn}\delta>0\). Since \(|\operatorname{cn}\delta|<\operatorname{dn}\delta\) for \(0<\delta<2K\), each factor is positive for real \(u\). In particular, the focal factorization has no hidden real zeros or phase-dependent sign choices.

## 5. Exact divisor on the one-focus torus

Work on

\[
 T_1=\mathbb C/(4K\mathbb Z+2iK'\mathbb Z),\quad p=iK'.
\]

This is the correct period torus for \(\operatorname{sn}u\) and hence for (8). It is deliberately different from the smaller real-period torus of the submitted paired function. The needed standard analytic facts are: \(\operatorname{sn}\) has precisely two simple poles \(p,p+2K\) on \(T_1\), and

\[
 \operatorname{sn}(z+K+p)=\frac{\operatorname{dn}z}
                                      {k\operatorname{cn}z}.
                                                               \tag{11}
\]

These are authenticated by [NIST DLMF Table 22.4.1](https://dlmf.nist.gov/22.4#T1) and [Table 22.4.3](https://dlmf.nist.gov/22.4#T3). Simplicity of the poles is also recorded in that section. No period of \(\operatorname{cn}\) is incorrectly substituted: (8) involves only \(\operatorname{sn}\), since \(\operatorname{cn}^2=1-\operatorname{sn}^2\).

Suppose first \(\delta\ne K\). The first factor in (10) has a double zero at \(p+K\). Indeed (11) at \(z=0\) gives \(\operatorname{sn}(p+K)=1/k\); its first derivative vanishes there, and its second derivative is \(k'^2/k\ne0\), by the differential equation
\(\operatorname{sn}''=-(1+k^2)\operatorname{sn}+2k^2\operatorname{sn}^3\).

The other factor vanishes at exactly

\[
 p+K+\delta,\quad p+K-\delta,
\]

by (11). These points are distinct on \(T_1\): otherwise \(2\delta\in4K\mathbb Z+2iK'\mathbb Z\), impossible for \(0<\delta<2K\). Neither is a pole unless \(\delta=K\), and neither equals \(p+K\). Their common \(\operatorname{sn}\) value is \(\operatorname{dn}\delta/(k\operatorname{cn}\delta)\), of absolute value strictly greater than \(1/k\), so it is not a branch value \(\pm1,\pm1/k\). The zeros are simple. Alternatively the two exhibited distinct zeros exhaust the degree-two second factor.

Each pole of \(\operatorname{sn}\) is an order-two pole of \(f\), since \(L\ne0\). Hence

\[
 \boxed{\operatorname{div}(f)=2[p+K]+[p+K+\delta]+[p+K-\delta]
                          -2[p]-2[p+2K].}              \tag{12}
\]

For \(\delta=K\), (10) is \(f=M(1-k\operatorname{sn}u)\), so

\[
 \boxed{\operatorname{div}(f)=2[p+K]-[p]-[p+2K].}        \tag{13}
\]

Equation (4) shows that \(\delta=K\) with a primitive orbit forces \(N=4,r=1\). This is precisely the circular outer-locus case. It is explicitly treated as a degree drop, with no division by \(A^2-B^2\).

## 6. Cyclic cancellation and positive distances

Let \(G=\{j\delta:0\le j<N\}\subset T_1\). By (4), translation by \(\delta\) has exact order \(N\). When \(4\mid N\), the coprime integer \(r\) has an inverse modulo \(N\), and therefore \(K\in G\); also \(2K\in G\). All points in (12) belong to the single coset \(p+G\).

Consider

\[
 \mathcal F(u)=\prod_{j=0}^{N-1}f(u+j\delta).            \tag{14}
\]

Summing translates of (12), every point of \(p+G\) receives zero multiplicity \(2+1+1=4\) and pole multiplicity \(2+2=4\). Thus \(\operatorname{div}\mathcal F=0\). The same computation with (13) gives \(2-1-1=0\) in the exceptional four-periodic case. A meromorphic function on a compact connected torus with zero divisor is a finite nonzero constant: all poles are removable and the holomorphic function is constant by the maximum principle.

For real phase, (7) or (10) gives \(f(u)>0\). Thus

\[
 R_+(u)^2=\mathcal F(u)>0
\]

is a fixed positive number, and \(R_+\) is its unique positive square root. There is no complex square-root branch choice. For the other focus,

\[
 f_-(u)=f_+(u+2K),
\]

because \(Q(u+2K)=-Q(u)\). Its constant product has the same value. Orientation reversal merely permutes the distances. This proves the exact claim for every primitive admissible rotation and real phase.

As an explicit exceptional-case check, \(N=4\) gives \(A=B=\sqrt{a^2+b^2}\), \(M=2a^2\), and \(k'^2=b^4/a^4\). Quarter shifts yield
\(\prod_{j=0}^3(1-k\operatorname{sn}(u+jK))=k'^2\): pair opposite terms to get \(\operatorname{dn}^2u\operatorname{dn}^2(u+K)=k'^2\). Thus the **ordinary** four-distance product is \(R_+=R_-=4a^2b^2\), not its square.

## 7. Adversarial parity check

The same divisor gives a useful independent negative control. For any primitive proper elliptical-caustic orbit of least period \(N\ge3\), \(K\in G\) holds **if and only if** \(4\mid N\). Also \(2K\in G\) holds if and only if \(N\) is even. Away from the already isolated \(N=4\) case, the divisor of (14) is

\[
 4\sum_{x\in p+K+G}[x]
 -2\sum_{x\in p+G}[x]
 -2\sum_{x\in p+2K+G}[x].                              \tag{15}
\]

If \(N\equiv2\pmod4\), the two pole cosets coincide and the zero coset is disjoint. If \(N\) is odd, all three cosets are disjoint. The divisor is nonzero in either case, so the real focal product cannot be constant (otherwise analytic continuation would make (14) constant). Thus within this strict noncircular model the primitive divisibility condition is necessary as well as sufficient. Repeating a nonconstant primitive orbit cannot make its product constant; repeating an already constant orbit takes a power.

## 8. Boundary and provenance limits

- The original circle \(a=b\) is excluded from this complex-torus proof. Directly its focus is the center and each outer vertex has radius \(a/\cos(\pi r/N)\), so its focal product is constant for any admitted primitive period.
- \(\lambda=0\) and \(\lambda=b^2\) are excluded. At the first endpoint \(v=0\) and adjacent tangents coincide; at the second \(\beta=0,k=1\), so the caustic and compact elliptic torus degenerate. No uniform endpoint conclusion is silently inferred.
- \(A=B\) is allowed: it occurs exactly at \(\delta=K\), and was handled above.
- Extremely small positive \(\lambda\), or \(k\) near 1, can make finite-precision calculations ill-conditioned. The exact inequalities (6), (7), (10) and the divisor proof remain valid at every strictly interior parameter.
- No statement about hyperbolic caustics, nonconfocal Poncelet pairs, historical novelty, or current openness follows from this audit.

The Jacobi addition laws used in deriving (2) and (5) are authenticated by [DLMF 22.8.1–22.8.3](https://dlmf.nist.gov/22.8#i); the double-angle formulas in (10) follow by substitution and also appear in [DLMF 22.6.6–22.6.7](https://dlmf.nist.gov/22.6#ii). The differential identities used for multiplicity follow from the inverse elliptic integral and are authenticated by [DLMF 22.13](https://dlmf.nist.gov/22.13). These are standard analytic inputs, not novel claims.
