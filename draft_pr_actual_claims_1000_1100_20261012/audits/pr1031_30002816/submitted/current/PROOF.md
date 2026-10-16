# A separable-state section of a Grassmann orbitope

**Status:** accepted mathematical reduction after independent AI-assisted audit; no conventional human peer-review, journal-acceptance, or novelty claim. Written 9 October 2026. Target: 30002816 / OWR-13498-004.

## 1. Precise claim and external input

Let $X_{k,n}$ be the set of decomposable unit $k$-vectors in $\Lambda^k\mathbb R^n$, with both orientations included, and let $C_{k,n}=\operatorname{conv}(X_{k,n})$. Let $I(X_{k,n})$ be its real vanishing ideal. The OWR conjecture says that, for every real linear functional $\ell$, if $\delta=\max_{p\in X_{k,n}}\ell(p)$, then

\[
 \delta-\ell=\sum_j h_j^2\pmod {I(X_{k,n})},\qquad \deg h_j\leq1.
\]

The polynomials $h_j$ are affine, so constants are allowed.

**Theorem.** The convex body $C_{4,12}$ has no finite semidefinite lift. Consequently there exists a real linear functional $\ell$ on $\Lambda^4\mathbb R^{12}$ for which its supporting function $\max_{X_{4,12}}\ell-\ell$ has no such affine-linear SOS representation. One can require the coefficients of $\ell$ to be rational, though the argument does not give an explicit coefficient list or an explicit value of its maximum.

The only non-elementary theorem used in the reduction is the following established external input:

**Fawzi's obstruction, specialized.** The convex body
\[
 \operatorname{Sep}(3,3)
 =\operatorname{conv}\{xx^*\otimes yy^*:x,y\in\mathbb C^3,
                  \|x\|=\|y\|=1\}
\]
has no finite semidefinite lift. Here a lift permits an arbitrary finite-dimensional spectrahedron and a linear projection; it is not restricted to an unprojected LMI or to a particular relaxation hierarchy.

This is Theorem 1 of H. Fawzi, *The set of separable states has no finite semidefinite representation except in dimension 3×2*, Commun. Math. Phys. **386** (2021), 1319–1335, [DOI](https://doi.org/10.1007/s00220-021-04163-2). The published text's definition of a semidefinite lift is on p.1320; Theorem 1 and its explicit application to $\operatorname{Sep}(3,3)$ are on p.1321. The [published-version PDF](https://www.repository.cam.ac.uk/bitstreams/e6e52df9-b317-4616-9462-c79a3cb4844b/download) was read. Fawzi allows Hermitian LMIs, so the obstruction in particular excludes real-symmetric LMIs. The proof below does not claim to reprove his theorem.

## 2. A compact first moment lift forced by affine-linear SOS

We first record the implication needed from the conjecture, including the compactness detail. Let $X\subseteq S^{N-1}\subseteq\mathbb R^N$ be any nonempty compact set. Write $p=(p_1,\ldots,p_N)$, and set
\[
 J_2=I(X)\cap\mathbb R[p]_{\leq2}.
\]
This is a finite-dimensional vector space; choose any basis of it. For a symmetric $(N+1)\times(N+1)$ matrix $M$, let $L_M$ be the functional on polynomials of degree at most two given by
\[
 L_M(1)=M_{00},\quad L_M(p_i)=M_{0i},\quad
 L_M(p_ip_j)=M_{ij}.
\]
Consider the finite spectrahedron
\[
 \mathcal S_X=\{M\succeq0:M_{00}=1, L_M(g)=0\ (g\in J_2)\},
 \qquad
 T_X=\{(M_{01},\ldots,M_{0N}):M\in\mathcal S_X\}.
\]
The equations only need be imposed on the chosen finite basis of $J_2$. Since $1-\sum_i p_i^2\in J_2$, every feasible matrix satisfies
\[
 \sum_{i=1}^N M_{ii}=1,\qquad\operatorname{tr}M=2.
\]
A positive semidefinite matrix with trace 2 is bounded in every entry. Thus $\mathcal S_X$ is closed and bounded, hence compact, and $T_X$ is compact. In particular, no closure of a nonclosed projection is being silently inserted.

For $p\in X$, the matrix $(1,p)(1,p)^T$ belongs to $\mathcal S_X$; hence $\operatorname{conv}(X)\subseteq T_X$. Suppose now that every supporting function $\delta-\ell$, with $\delta=\max_X\ell$, is a sum of squares of affine forms on $X$. If $h_j(p)=a_j^T(1,p)$, then
\[
 g=\delta-\ell-\sum_jh_j^2\in J_2.
\]
Consequently every $M\in\mathcal S_X$, with projected point $x$, satisfies
\[
 \delta-\ell(x)=\sum_j a_j^TMa_j\geq0.
\]
The intersection of all supporting halfspaces of the compact convex set $\operatorname{conv}(X)$ is the set itself. Thus $T_X\subseteq\operatorname{conv}(X)$. We conclude
\[
 T_X=\operatorname{conv}(X).
\]
So the all-supporting-functions affine-linear SOS property implies a finite semidefinite lift, indeed this compact lift of size $N+1$. No duality attainment theorem is needed.

## 3. The Kähler face, with orientations fixed

Identify $V=\mathbb R^{12}$ with the underlying real Euclidean space of $E=\mathbb C^6$. Use the real orthonormal basis
\[
 e_1,f_1,e_2,f_2,\ldots,e_6,f_6,
 \qquad Je_j=f_j,\quad Jf_j=-e_j.
\]
Define the two-form $\omega=\sum_{j=1}^6 e_j^*\wedge f_j^*$, so $\omega(u,v)=\langle Ju,v\rangle$, and the four-form $\Phi=\omega^2/2$.

For every $p\in X_{4,12}$, $\Phi(p)\leq1$. Moreover, $\Phi(p)=1$ holds exactly when $p$ represents a complex two-dimensional subspace of $E$ with its complex orientation.

Here is a direct verification of this familiar Wirtinger statement. For the underlying real four-plane $P$, the restriction of $\omega$ has a real skew-symmetric matrix. Its two skew singular values have absolute value at most 1, since the compression $P_PJ|_P$ of the orthogonal map $J$ has operator norm at most 1. The value of $\omega^2/2$ on an oriented orthonormal basis is the Pfaffian, the signed product of those two values. Therefore its absolute value is at most 1. Equality $\Phi(p)=1$ forces both singular values to have absolute value 1. Then $\|P_PJv\|=\|v\|=\|Jv\|$ for every $v\in P$, so the component of $Jv$ perpendicular to $P$ is zero. Hence $P$ is $J$-invariant. Of its two orientations, precisely the complex orientation gives Pfaffian $+1$. Conversely, a complex-orthonormal pair $a,b\in E$, regarded as real vectors, gives the positively oriented real orthonormal frame $a,Ja,b,Jb$, on which $\Phi=1$.

It follows that the exposed face
\[
 F=C_{4,12}\cap\{\Phi=1\}
\]
is exactly the convex hull of these positively oriented complex two-planes. Indeed, in any finite convex combination of elements of $X_{4,12}$ with value 1, every positive-weight summand must itself have value 1. Finite combinations suffice by the definition of convex hull (or Carathéodory's theorem); the hull is compact.

## 4. An explicit real-linear projector embedding

Let $W=\Lambda^2_{\mathbb C}E$, of complex dimension 15, with its induced Hermitian inner product and the orthonormal basis indexed by increasing pairs $I=(i,j)$. Write $\operatorname{Herm}(W)$ for the real vector space of Hermitian operators on $W$.

In $V_{\mathbb C}=V\otimes_{\mathbb R}\mathbb C$, set
\[
 u_j=(e_j-if_j)/\sqrt2,\qquad
 u_I=u_i\wedge u_j.
\]
The $u_j$ form a basis of the $+i$ eigenspace of $J$, and their conjugates form a basis of the $-i$ eigenspace. Define
\[
 A:\operatorname{Herm}(W)\longrightarrow\Lambda^4_{\mathbb R}V,
 \qquad A(H)=\sum_{I,J}H_{IJ}\,u_I\wedge\overline{u_J}. \tag{4.1}
\]
This formula, initially in the complexification, is real: complex conjugation changes $H_{IJ}$ to $H_{JI}$, and interchanging the two exterior factors of degree two has sign $+1$. Thus conjugation leaves the sum fixed. It is manifestly real-linear.

The 225 elements $u_I\wedge\overline{u_J}$ form a complex basis of the $(2,2)$-type subspace. Hence the formula is injective on all matrices, and in particular $A$ is injective on the 225-dimensional real space $\operatorname{Herm}(W)$. Equivalently, using $w_j=e_j-if_j$, the formula is
\[
 A(H)=\frac14\sum_{I,J}H_{IJ}\,w_i\wedge w_j\wedge\overline{w_r}\wedge\overline{w_s},
 \quad I=(i,j), J=(r,s), \tag{4.2}
\]
which has rational real coefficients on the standard real Hermitian matrix basis.

For $a=(a_j)\in E$, let $\widehat a=\sum_j a_j u_j$. Regarding $a$ as a real vector, we have
\[
 a=(\widehat a+\overline{\widehat a})/\sqrt2,\qquad
 Ja=i(\widehat a-\overline{\widehat a})/\sqrt2,\qquad
 a\wedge Ja=-i\widehat a\wedge\overline{\widehat a}.
\]
Therefore, for every $a,b\in E$, with $z=a\wedge b\in W$,
\[
 A(zz^*)=\widehat a\wedge\widehat b\wedge
              \overline{\widehat a}\wedge\overline{\widehat b}
          =a\wedge Ja\wedge b\wedge Jb. \tag{4.3}
\]
The sign is positive: the two factors $-i$ first give $-1$, and moving $\overline{\widehat a}$ past $\widehat b$ gives another $-1$.

Every decomposable unit bivector $z\in W$ has a factorization $z=a\wedge b$ with $a,b$ complex-orthonormal (absorb its unit complex phase into one basis vector). Equation (4.3) then has real norm 1 and the positive complex orientation. Conversely every generating point of $F$ arises this way. Hence
\[
 F=A(K),\qquad
 K=\operatorname{conv}\{zz^*:z\in\Lambda^2\mathbb C^6
          \text{ decomposable}, \|z\|=1\}. \tag{4.4}
\]
This is a linear isomorphism of convex sets onto the image, not just a nonlinear parametrization. In these conventions $\Phi(A(H))=\operatorname{tr}H$; this follows by evaluating on the Hermitian matrix basis, or directly by noting that the coefficient of $e_i\wedge f_i\wedge e_j\wedge f_j$ is $H_{(i,j),(i,j)}$, and summing over $i<j$.

## 5. A two-hyperplane section is $\operatorname{Sep}(3,3)$

Split $E=U\oplus Z$ orthogonally, with
\[
 U=\mathbb C\{e_1,e_2,e_3\},\qquad
 Z=\mathbb C\{e_4,e_5,e_6\}.
\]
Here the symbols $e_j$ in these complex spans mean the standard complex coordinate vectors; their real and imaginary parts are the $e_j,f_j$ fixed above. There is an orthogonal splitting
\[
 W=(\Lambda^2U)\oplus B\oplus(\Lambda^2Z),\qquad B=U\wedge Z.
\]
Let $D=(\Lambda^2U)\oplus(\Lambda^2Z)$, and let $P_D$ be its orthogonal projector. Set
\[
 K_0=\{H\in K:\operatorname{tr}(P_DH)=0\}.
\]
For any convex expression $H=\sum_t\lambda_t z_tz_t^*\in K$, with $\lambda_t>0$, $\sum_t\lambda_t=1$, we have
\[
 0=\operatorname{tr}(P_DH)=\sum_t\lambda_t\|P_Dz_t\|^2.
\]
Every summand is nonnegative. Thus each $z_t\in B$; there is no cancellation between summands. This also proves $H$ is supported on $B$. Equivalently, one may use the standard PSD zero-trace implication. The stronger summand statement above ensures the desired convex-hull identity, not merely matrix support.

We next verify exactly which decomposable bivectors lie in $B$. Define the unitary identification
\[
 T:U\otimes_{\mathbb C}Z\longrightarrow B,\qquad T(x\otimes y)=x\wedge y.
\]
A nonzero decomposable bivector $z=a\wedge b\in B$ necessarily equals $x\wedge y$ for some $x\in U,y\in Z$. To see this, write $a=a_U+a_Z$, $b=b_U+b_Z$. Its $\Lambda^2U$ and $\Lambda^2Z$ components vanish, so $a_U,b_U$ are linearly dependent, as are $a_Z,b_Z$. Neither span can be zero: otherwise $a,b$ lie in the other summand and $a\wedge b\in B$ would force $z=0$. Choose nonzero $x,y$ spanning these respective one-dimensional projections and write
\[
 a=\alpha x+\gamma y,\qquad b=\beta x+\delta y.
\]
Then $z=(\alpha\delta-\beta\gamma)x\wedge y$, with nonzero scalar. Absorb that scalar into $x$. Conversely $x\wedge y$ is decomposable and belongs to $B$. Thus $T^{-1}(z)$ is precisely a rank-one tensor.

Because $U\perp Z$, $\|x\wedge y\|=\|x\|\|y\|$. For unit $z$, the factors may therefore be rescaled to have norm 1 each, with the irrelevant unit phase absorbed into a factor. Under $T$,
\[
 (x\wedge y)(x\wedge y)^*\longleftrightarrow
 (x\otimes y)(x\otimes y)^*=xx^*\otimes yy^*.
\]
The zero-trace argument and its converse prove the exact equality
\[
 K_0\cong\operatorname{Sep}(3,3). \tag{5.1}
\]

For completeness, the section can be expressed in the original real ambient space by two explicit linear equations. Let
\[
 \omega_U=\sum_{j=1}^3 e_j^*\wedge f_j^*,\qquad
 \omega_Z=\sum_{j=4}^6 e_j^*\wedge f_j^*,\qquad
 Q=(\omega_U^2+\omega_Z^2)/2.
\]
By the coefficient calculation following (4.4), $Q(A(H))=\operatorname{tr}(P_DH)$. Hence
\[
 C_{4,12}\cap\{\Phi=1, Q=0\}=A(K_0)\cong\operatorname{Sep}(3,3). \tag{5.2}
\]
No assertion that $Q\geq0$ on all of $C_{4,12}$ is needed or used; it is nonnegative on the face $F$. The two equations are imposed simultaneously.

## 6. The contradiction and the failing supporting function

Finite semidefinite representability is preserved by affine sections and by linear maps. Indeed, if $C=\pi(S)$, then $C\cap\{L(x)=b\}$ is the image under $\pi$ of $S\cap\{L(\pi(s))=b\}$, a spectrahedron with additional affine equalities. A linear inverse defined on an image subspace may be extended linearly to the ambient vector space. Thus (5.2) would give a finite semidefinite lift of $\operatorname{Sep}(3,3)$ if $C_{4,12}$ had one. Fawzi's theorem excludes this. Consequently $C_{4,12}$ has no finite semidefinite lift.

Apply Section 2 to $X=X_{4,12}\subset S^{494}$, since $N=\binom{12}{4}=495$. If all supporting functions were affine-linear SOS on $X$, the compact spectrahedron of size 496 in Section 2 would lift $C_{4,12}$, a contradiction. This proves the claimed failure of the universal conjecture at $(4,12)$.

There is also a precise existential separating description of a failing form. The compact moment relaxation $T_X$ strictly contains $C_{4,12}$, since equality would give a lift. Choose $x\in T_X\setminus C_{4,12}$. Strict separation gives a real coefficient vector $c$ such that
\[
 c\cdot x>\max_{p\in X}c\cdot p.
\]
Both $x$ and $X$ are bounded, so this strict inequality persists under a sufficiently small perturbation of $c$. Choose a rational $c'$ in that neighborhood. With $\ell(p)=c'\cdot p$ and $\delta=\max_X\ell$, the same matrix $M\in\mathcal S_X$ lifting $x$ gives $\delta-\ell(x)<0$, whereas an affine-linear SOS representation would give a nonnegative value by Section 2. Thus a rational-coefficient failing $\ell$ exists. This is an existence proof, not an explicit rational certificate file or a coefficient-level example.

Because the coordinate vectors and their negatives lie in $X$, a nonzero $\ell$ has $\delta>0$. Dividing by $\delta$ gives a calibration of comass 1 and the same obstruction. The proof leaves all lower-dimensional cases, including $n\leq7$, untouched.

## 7. Relation to Harvey–Lawson's question

The pointwise version of Harvey–Lawson Question 6.5 asks whether a comass-one form $\varphi$ admits linear forms $\psi_j$ with
\[
 \varphi(p)^2+\sum_j\psi_j(p)^2=\|p\|^2
\]
on all decomposable vectors. Such an identity immediately supplies the affine-linear SOS
\[
 1-\varphi=\tfrac12(1-\varphi)^2+\tfrac12\sum_j\psi_j^2
\]
on unit decomposable vectors. Thus the failing calibration above also fails that pointwise completion property. Regard it as a constant differential four-form on $\mathbb R^{12}$; it is closed, so this is within the usual definition of a calibration. No locally varying completion can exist at any point if the pointwise algebraic completion fails.

The converse equivalence, recorded as Approach 1, can also be checked directly. Suppose $1-\varphi(p)=\|a+Bp\|^2$ on $X$. Evaluating at $p$ and $-p$, and using that $X$ spans the ambient exterior space, yields $B^Ta=-\varphi/2$, while $\|a\|^2+\|Bp\|^2=1$ on $X$. Choose $p_0\in X$ with $\varphi(p_0)=1$. Then $Bp_0=-a$; evaluating at $-p_0$ gives $2=4\|a\|^2$. Thus $\|a\|^2=1/2$. If $P$ is the orthogonal projection in the target of $B$ onto $a^\perp$, then
\[
 \|\sqrt2 PBp\|^2=1-\varphi(p)^2\quad(p\in X).
\]
Scaling extends this to all decomposable vectors. This confirms the affine-degree and normalization conventions used throughout.

## 8. Audit boundaries

The accepted proof is an elementary reduction to Fawzi's established theorem, not a numerical SDP infeasibility claim. It does not infer nonrepresentability from nonexposed faces. It does not use a polar-representation assertion for the full Grassmann representation. It does not claim that the obstruction appears already for $G_{3,6}$, that dimension 12 is minimal, or that a particular coefficient-level calibration has been constructed. Priority and whether the reduction has appeared elsewhere remain unestablished. The full independent audit is included in AUDIT_REPORT.md; priority remains unestablished.

The accompanying exact-arithmetic script checks coordinate normalization, reality, rank, the two section functionals, the product-projector identity, and the mixed Plücker/minor relation. These checks support the elementary bridge; they are not substitutes for the argument or for Fawzi's theorem.
